from typing import Any, TypedDict


class OpsAgentState(TypedDict, total=False):
    order_id: str
    investigation: dict[str, Any]
    analysis: str
    approved: bool
    action_result: dict[str, Any]
    status: str