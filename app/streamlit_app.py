import sys
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------
# Project path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.graph_nodes import (
    investigation_node,
    analysis_node,
    action_node,
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="OpsAgent",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🤖 OpsAgent")

st.subheader(
    "Autonomous Business Operations Investigation"
)

st.write(
    "Investigate an e-commerce order using business data, "
    "machine learning, RAG policy evidence, and human approval."
)


# ---------------------------------------------------------
# Order input
# ---------------------------------------------------------

order_id = st.text_input(
    "Enter Order ID",
    placeholder="e481f51cbdc54678b7cc49136f2d6af7"
)


if st.button(
    "🔍 Investigate Order",
    use_container_width=False
):

    if not order_id.strip():

        st.warning(
            "Please enter an Order ID."
        )

    else:

        # Clear previous approval/action state
        st.session_state.pop(
            "approved",
            None
        )

        st.session_state.pop(
            "action_result",
            None
        )

        with st.spinner(
            "Running OpsAgent investigation..."
        ):

            state = {
                "order_id": order_id.strip()
            }

            # Step 1: Investigation
            state.update(
                investigation_node(state)
            )

            # Step 2: LLM analysis
            if state.get("status") != "Error":

                state.update(
                    analysis_node(state)
                )

        # Save investigation state
        st.session_state["ops_state"] = state


# ---------------------------------------------------------
# Display investigation
# ---------------------------------------------------------

if "ops_state" in st.session_state:

    state = st.session_state["ops_state"]

    # -----------------------------------------------------
    # Error handling
    # -----------------------------------------------------

    if state.get("status") == "Error":

        st.error(
            state["investigation"].get(
                "error",
                "Investigation failed."
            )
        )

    else:

        investigation = state["investigation"]

        model_prediction = investigation[
            "model_prediction"
        ]

        policy_evaluation = investigation[
            "policy_evaluation"
        ]

        # -------------------------------------------------
        # Investigation completed
        # -------------------------------------------------

        st.success(
            "Investigation completed successfully."
        )

        st.divider()

        st.header(
            "📦 Order Investigation"
        )

        # -------------------------------------------------
        # Main metrics
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Order ID",
                state["order_id"]
            )

        with col2:

            st.metric(
                "Late Delivery Probability",
                model_prediction[
                    "late_delivery_probability"
                ]
            )

        with col3:

            st.metric(
                "Risk",
                model_prediction[
                    "risk"
                ]
            )

        # -------------------------------------------------
        # Prediction features
        # -------------------------------------------------

        with st.expander(
            "🔍 Prediction Features",
            expanded=False
        ):

            st.json(
                investigation.get(
                    "prediction_features",
                    {}
                )
            )

        # -------------------------------------------------
        # Policy evaluation
        # -------------------------------------------------

        st.divider()

        st.header(
            "📊 Policy Indicator Evaluation"
        )

        indicators = policy_evaluation[
            "policy_indicators"
        ]

        for name, detected in indicators.items():

            status = (
                "Detected"
                if detected
                else "Not detected"
            )

            st.write(
                f"**{name}:** {status}"
            )

        # -------------------------------------------------
        # LLM analysis
        # -------------------------------------------------

        st.divider()

        st.header(
            "🧠 LLM Analysis"
        )

        with st.expander(
            "View investigation analysis",
            expanded=True
        ):

            st.markdown(
                state.get(
                    "analysis",
                    "No analysis available."
                )
            )

        # -------------------------------------------------
        # Retrieved policy evidence
        # -------------------------------------------------

        st.divider()

        st.header(
            "📚 Retrieved Policy Evidence"
        )

        with st.expander(
            "View policy evidence",
            expanded=False
        ):

            st.text(
                investigation.get(
                    "policy_evidence",
                    "No policy evidence available."
                )
            )

        # -------------------------------------------------
        # Human approval
        # -------------------------------------------------

        st.divider()

        st.header(
            "👤 Human Approval"
        )

        st.warning(
            "A human must approve the operational "
            "action before it can be executed."
        )

        # -------------------------------------------------
        # Approval buttons
        # -------------------------------------------------

        if st.session_state.get(
            "approved"
        ) is None:

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Approve Action",
                    use_container_width=True
                ):

                    st.session_state[
                        "approved"
                    ] = True

                    st.rerun()

            with col2:

                if st.button(
                    "❌ Reject Action",
                    use_container_width=True
                ):

                    st.session_state[
                        "approved"
                    ] = False

                    st.rerun()

        # -------------------------------------------------
        # Rejected
        # -------------------------------------------------

        if st.session_state.get(
            "approved"
        ) is False:

            st.error(
                "Action rejected. "
                "No operational action was executed."
            )

        # -------------------------------------------------
        # Approved
        # -------------------------------------------------

        elif st.session_state.get(
            "approved"
        ) is True:

            st.success(
                "Human approval received."
            )

            # Execute only once
            if "action_result" not in st.session_state:

                state["approved"] = True

                action_result = action_node(
                    state
                )

                st.session_state[
                    "action_result"
                ] = action_result

            # -------------------------------------------------
            # Action result
            # -------------------------------------------------

            st.subheader(
                "⚙️ Action Result"
            )

            st.json(
                st.session_state[
                    "action_result"
                ]["action_result"]
            )