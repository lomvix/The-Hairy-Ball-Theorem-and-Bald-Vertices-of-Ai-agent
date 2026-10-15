"""Lossless message fingerprints and conservative surface cues for WP5 state audit.

These are properties of the archived effective Agent request, not inferred hidden
user state, verified identity, or semantic intent labels.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any


_EMAIL = re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.I)
_YES = frozenset({"yes", "yes please", "yep", "yeah", "correct", "confirmed", "confirm", "go ahead", "sure", "是", "确认", "好的", "对", "可以"})
_NO = frozenset({"no", "no thanks", "nope", "cancel that", "不", "不要", "否", "取消"})


def digest(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def confirmation_cue(content: str) -> str:
    text = " ".join(content.casefold().strip().rstrip(".!?。！？,，").split())
    if text in _YES:
        return "AFFIRMATIVE_LITERAL"
    if text in _NO:
        return "NEGATIVE_LITERAL"
    return "NOT_EXPLICIT_LITERAL"


def _payload(message: dict[str, Any]) -> dict[str, Any]:
    # Tool-call IDs are request-local linkage IDs; preserve them separately in
    # full-message hashes, but exclude them from the payload equivalence check.
    return {key: message.get(key) for key in ("role", "content", "name")
            if key in message}


def describe_effective_request(request: dict[str, Any]) -> dict[str, Any]:
    messages = request.get("messages")
    if not isinstance(messages, list) or not messages:
        raise ValueError("effective request has no messages")
    if any(not isinstance(message, dict) or message.get("role") not in
           {"system", "developer", "user", "assistant", "tool"} for message in messages):
        raise ValueError("effective request contains an invalid role")
    users = [message for message in messages if message["role"] == "user"]
    tools = [message for message in messages if message["role"] == "tool"]
    agents = [message for message in messages if message["role"] == "assistant"]
    policies = [message for message in messages if message["role"] in {"system", "developer"}]
    if not users or not policies:
        raise ValueError("effective request lacks user or policy observation")
    if any(not isinstance(message.get("content"), str) for message in users + tools + policies):
        raise ValueError("non-Agent message has non-text content")
    user_texts = [message["content"] for message in users]
    latest_cue = confirmation_cue(user_texts[-1])
    goal_evidence = [text for text in user_texts
                     if confirmation_cue(text) == "NOT_EXPLICIT_LITERAL"]
    # This is exact text evidence, not a normalized or validated user goal.
    non_agent = [message for message in messages if message["role"] != "assistant"]
    identity_text = "\n".join(user_texts)
    contact_cues = []
    if _EMAIL.search(identity_text):
        contact_cues.append("EMAIL_PATTERN_PRESENT")
    return {
        "message_count": len(messages),
        "user_message_count": len(users),
        "tool_message_count": len(tools),
        "prior_agent_message_count": len(agents),
        "latest_user_hash": digest(_payload(users[-1])),
        "prior_user_sequence_hash": digest([_payload(message) for message in users[:-1]]),
        "full_user_sequence_hash": digest([_payload(message) for message in users]),
        "latest_tool_hash": digest(_payload(tools[-1])) if tools else None,
        "full_tool_sequence_hash": digest([_payload(message) for message in tools]),
        "policy_sequence_hash": digest([_payload(message) for message in policies]),
        "non_agent_payload_sequence_hash": digest([_payload(message) for message in non_agent]),
        "non_agent_exact_sequence_hash": digest(non_agent),
        "agent_exact_sequence_hash": digest(agents),
        "request_goal_evidence_hash": digest(goal_evidence),
        "request_goal_evidence_count": len(goal_evidence),
        "identity_contact_cues": contact_cues,
        "latest_user_confirmation_cue": latest_cue,
        "tool_schema_hash": digest(request.get("tools", [])),
    }


def compare_pair(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    equal = lambda key: a[key] == b[key]
    payload = equal("non_agent_payload_sequence_hash")
    exact = equal("non_agent_exact_sequence_hash")
    agent_diff = not equal("agent_exact_sequence_hash")
    return {
        "latest_user_equal": equal("latest_user_hash"),
        "prior_user_sequence_equal": equal("prior_user_sequence_hash"),
        "full_user_sequence_equal": equal("full_user_sequence_hash"),
        "latest_tool_equal": equal("latest_tool_hash"),
        "full_tool_sequence_equal": equal("full_tool_sequence_hash"),
        "policy_sequence_equal": equal("policy_sequence_hash"),
        "goal_evidence_equal": equal("request_goal_evidence_hash"),
        "identity_contact_cues_equal": equal("identity_contact_cues"),
        "latest_confirmation_cue_equal": equal("latest_user_confirmation_cue"),
        "non_agent_payload_sequence_equal": payload,
        "non_agent_exact_sequence_equal": exact,
        "agent_exact_sequence_different": agent_diff,
        "isolation_status": ("AGENT_HISTORY_ONLY_PAYLOAD_MATCH" if payload and agent_diff else
                             "NON_AGENT_OBSERVATION_DIFFERS" if not payload else
                             "NO_AGENT_HISTORY_CONTRAST"),
    }
