from src.investigation import investigate_order
from src.approval import request_human_approval
from src.actions import execute_operational_action
from src.policy_evaluator import evaluate_policy_indicators


def investigation_node(state):
    """
    Run the business investigation for the requested order.
    """

    order_id = state["order_id"]

    investigation = investigate_order(order_id)

    if "error" in investigation:
        return {
            "investigation": investigation,
            "status": "Error"
        }

    return {
        "investigation": investigation,
        "status": "Investigated"
    }


def approval_node(state):
    """
    Request explicit human approval before
    executing a consequential operational action.
    """

    investigation = state["investigation"]

    approved = request_human_approval(
        investigation
    )

    if approved:
        return {
            "approved": True,
            "status": "Approved"
        }

    return {
        "approved": False,
        "status": "Rejected"
    }


def action_node(state):
    """
    Execute the controlled operational action only
    after explicit human approval.
    """

    if not state.get("approved", False):
        return {
            "action_result": {
                "status": "Not Executed",
                "reason": "Human approval was not granted."
            },
            "status": "Rejected"
        }

    investigation = state["investigation"]

    action_result = execute_operational_action(
        investigation
    )

    return {
        "action_result": action_result,
        "status": "Completed"
    }

from langchain_groq import ChatGroq

from src.config import GROQ_TEMPERATURE


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=GROQ_TEMPERATURE
)


def analysis_node(state):
    """
    Use the LLM to summarize the structured investigation
    without making unsupported policy interpretations.
    """

    investigation = state["investigation"]
    policy_evaluation = investigation["policy_evaluation"]

    indicators = policy_evaluation["policy_indicators"]

    detected_indicators = [
        name
        for name, detected in indicators.items()
        if detected
    ]

    if detected_indicators:
        policy_summary = (
            "One or more policy indicators were detected "
            "by the deterministic evaluation."
        )
    else:
        policy_summary = (
            "No policy indicators were detected "
            "by the deterministic evaluation."
        )

    prompt = f"""
You are OpsAgent, a factual business operations investigation assistant.

Your task is to summarize the investigation using ONLY the
provided investigation evidence and deterministic policy evaluation.

STRICT RULES:

1. Use ONLY information explicitly contained in the investigation.
2. Never invent facts, numbers, causes, recommendations, or rules.
3. Do not create or modify policy thresholds.
4. Do not treat the ML threshold as a business-policy threshold.
5. Report the exact late-delivery probability without interpreting it.
6. Report the exact model prediction and configured threshold without
   interpreting the prediction as a business or policy conclusion.
7. Do not infer causation from feature values.
8. 8. Do not compare the model probability with the configured model
   threshold to make a business or policy conclusion.
9. Use the deterministic policy indicators as the authoritative
   evaluation of the listed policy indicators.
10. If a policy indicator is False, state that it was not detected.
11. If a policy indicator is True, state that it was detected.
12. Do not conclude that an order is or is not "high-risk" unless
    the retrieved policy explicitly defines that conclusion.
13. Do not invent additional policy indicators.
14. Do not determine that an operational action is required unless
    the policy evidence explicitly establishes that.
15. Important operational actions require human approval as stated
    in the policy.
16. Do not execute any action.

INVESTIGATION:

{investigation}

Use EXACTLY these sections:

1. Investigation Facts
   - Report the relevant observed order and feature values.

2. Model Prediction
   - Report the exact late-delivery probability.
   - Report the exact model prediction.
   - Report the configured model threshold.

3. Policy Indicator Evaluation
   - Report each deterministic policy indicator.
   - Clearly state whether each indicator was detected or not detected.
   - Do not create additional interpretations.

4. Relevant Policy Guidance
   - Report only policy statements explicitly present in the
     retrieved policy evidence.

5. Evidence-Based Considerations
   - Use the exact policy evaluation summary provided below.
   - Do not generate your own conclusion about the policy indicators.
   - Do not interpret the model prediction or model threshold.

DETERMINISTIC POLICY SUMMARY:

{policy_summary}
"""

    response = llm.invoke(prompt)

    return {
        "analysis": response.content,
        "status": "Analyzed"
    }