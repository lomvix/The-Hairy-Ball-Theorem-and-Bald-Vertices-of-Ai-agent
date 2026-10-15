"""Request-local Agent-history interventions for a prospective Agent-only study."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


GREETING = "Hi! How can I help you today?"
PLACEBO_GREETING = "Hello! How may I help you today?"
MASKED_HISTORY = "[Earlier assistant message omitted from this transcript.]"


def target_message_index(request: dict[str, Any]) -> int | None:
    messages = request.get("messages")
    if not isinstance(messages, list) or len(messages) < 5:
        return None
    if (messages[0].get("role") != "system" or messages[1].get("role") != "assistant"
            or messages[1].get("content") != GREETING or messages[1].get("tool_calls")):
        return None
    last = messages[-1]
    target = messages[-2]
    if (last.get("role") != "user" or not isinstance(last.get("content"), str)
            or len(last["content"]) < 40 or target.get("role") != "assistant"
            or not isinstance(target.get("content"), str) or not target["content"].strip()
            or target.get("tool_calls") or len(messages) - 2 == 1):
        return None
    return len(messages) - 2


def make_variant(request: dict[str, Any], arm: str) -> tuple[dict[str, Any], int | None]:
    target = target_message_index(request)
    if target is None:
        raise ValueError("request is not eligible for Agent-history intervention")
    variant = copy.deepcopy(request)
    if arm == "A_BASELINE":
        changed = None
    elif arm == "B_HISTORY_MASK":
        variant["messages"][target]["content"] = MASKED_HISTORY
        changed = target
    elif arm == "C_GREETING_PLACEBO":
        variant["messages"][1]["content"] = PLACEBO_GREETING
        changed = 1
    else:
        raise ValueError("unknown intervention arm")
    assert_only_agent_text_change(request, variant, changed)
    return variant, changed


def assert_only_agent_text_change(original: dict[str, Any], variant: dict[str, Any],
                                  changed_index: int | None) -> None:
    left = copy.deepcopy(original)
    right = copy.deepcopy(variant)
    if changed_index is not None:
        if (left["messages"][changed_index].get("role") != "assistant"
                or right["messages"][changed_index].get("role") != "assistant"):
            raise ValueError("non-Agent message changed")
        right["messages"][changed_index]["content"] = left["messages"][changed_index]["content"]
    if left != right:
        raise ValueError("intervention changed more than one Agent text field")


def selection_key(seed: str, decision_id: str) -> str:
    return hashlib.sha256(f"{seed}:{decision_id}".encode("utf-8")).hexdigest()


def choose_anchors(rows: list[dict[str, Any]], eligible_ids: set[str],
                   *, seed: str, per_domain_split: int = 2) -> list[dict[str, Any]]:
    chosen = []
    for split in ("TEST", "CURATION_DIAGNOSTIC"):
        for domain in ("airline", "retail", "telecom"):
            pool = [row for row in rows if row["decision_id"] in eligible_ids
                    and row["split"] == split and row["domain"] == domain]
            pool.sort(key=lambda row: selection_key(seed, row["decision_id"]))
            seen_tasks: set[str] = set()
            for row in pool:
                if row["task_uid"] not in seen_tasks:
                    chosen.append(row)
                    seen_tasks.add(row["task_uid"])
                    if len(seen_tasks) == per_domain_split:
                        break
            if len(seen_tasks) != per_domain_split:
                raise ValueError(f"insufficient distinct tasks for {split}/{domain}")
    return chosen


def request_fingerprint(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
