"""Pure, fail-closed checks for the archived task-initialization replay boundary."""

from __future__ import annotations

from typing import Any


def post_initial_messages(
    initial_trajectory: list[dict[str, Any]],
    decision_trajectory: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return only messages after initialization, rejecting partial tool exchanges."""
    if len(initial_trajectory) > len(decision_trajectory):
        raise ValueError("initialization trajectory is longer than decision trajectory")
    if decision_trajectory[:len(initial_trajectory)] != initial_trajectory:
        raise ValueError("decision trajectory does not begin with archived initialization prefix")
    if initial_trajectory and initial_trajectory[-1].get("tool_calls"):
        raise ValueError("initialization ends with a pending tool call")
    remainder = decision_trajectory[len(initial_trajectory):]
    if remainder and remainder[0].get("role") == "tool":
        raise ValueError("initialization boundary splits a tool call/result pair")
    return remainder
