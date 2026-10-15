import copy

import pytest

from src.behavioral_state.history_intervention import (
    GREETING, MASKED_HISTORY, PLACEBO_GREETING, assert_only_agent_text_change,
    choose_anchors, make_variant, target_message_index,
)


def fixture_request():
    return {"model": "openai/example", "tools": [{"function": {"name": "lookup"}}],
            "messages": [
                {"role": "system", "content": "Policy"},
                {"role": "assistant", "content": GREETING},
                {"role": "user", "content": "I need some help with my order."},
                {"role": "assistant", "content": "I can check the order details for you."},
                {"role": "user", "content": "Please tell me the delivery date for order number 123456."},
            ]}


def test_three_arms_change_only_intended_agent_text() -> None:
    source = fixture_request()
    assert target_message_index(source) == 3
    for arm, index in (("A_BASELINE", None), ("B_HISTORY_MASK", 3),
                       ("C_GREETING_PLACEBO", 1)):
        variant, changed = make_variant(source, arm)
        assert changed == index
        assert_only_agent_text_change(source, variant, changed)
        assert [m for m in source["messages"] if m["role"] != "assistant"] == [
            m for m in variant["messages"] if m["role"] != "assistant"]
    assert make_variant(source, "B_HISTORY_MASK")[0]["messages"][3]["content"] == MASKED_HISTORY
    assert make_variant(source, "C_GREETING_PLACEBO")[0]["messages"][1]["content"] == PLACEBO_GREETING
    assert source["messages"][3]["content"] != MASKED_HISTORY


def test_tool_call_or_short_latest_user_is_ineligible() -> None:
    source = fixture_request()
    source["messages"][3]["tool_calls"] = [{"id": "x"}]
    assert target_message_index(source) is None
    source = fixture_request()
    source["messages"][-1]["content"] = "yes"
    assert target_message_index(source) is None
    with pytest.raises(ValueError, match="not eligible"):
        make_variant(source, "B_HISTORY_MASK")


def test_non_agent_mutation_rejected_and_task_selection_unique() -> None:
    source = fixture_request()
    variant = copy.deepcopy(source)
    variant["messages"][-1]["content"] += " now"
    with pytest.raises(ValueError, match="more than one"):
        assert_only_agent_text_change(source, variant, 3)
    rows = [{"decision_id": f"d{i}", "task_uid": f"t{i // 2}",
             "split": split, "domain": domain}
            for split in ("TEST", "CURATION_DIAGNOSTIC")
            for domain in ("airline", "retail", "telecom")
            for i in range(4)]
    # Decision IDs need to be unique across strata.
    for n, row in enumerate(rows):
        row["decision_id"] += f"_{n}"
        row["task_uid"] += f"_{row['split']}_{row['domain']}"
    selected = choose_anchors(rows, {r["decision_id"] for r in rows}, seed="fixed")
    assert len(selected) == 12
    assert len({r["task_uid"] for r in selected}) == 12
