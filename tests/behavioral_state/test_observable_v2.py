import pytest

from src.behavioral_state.observable_v2 import compare_pair, describe_effective_request


def request(*messages):
    return {"messages": [{"role": "system", "content": "Policy"}, *messages],
            "tools": [{"function": {"name": "lookup"}}]}


def test_prior_user_difference_survives_same_latest_user_and_tool() -> None:
    first = describe_effective_request(request(
        {"role": "user", "content": "Please cancel my order. Email: a@example.com"},
        {"role": "assistant", "content": "I can help."},
        {"role": "tool", "content": "order found", "tool_call_id": "call-a"},
        {"role": "user", "content": "yes"}))
    second = describe_effective_request(request(
        {"role": "user", "content": "Please change my order. Email: a@example.com"},
        {"role": "assistant", "content": "I can help."},
        {"role": "tool", "content": "order found", "tool_call_id": "call-b"},
        {"role": "user", "content": "yes"}))
    pair = compare_pair(first, second)
    assert pair["latest_user_equal"] and pair["latest_tool_equal"]
    assert not pair["prior_user_sequence_equal"]
    assert not pair["non_agent_payload_sequence_equal"]
    assert first["latest_user_confirmation_cue"] == "AFFIRMATIVE_LITERAL"
    assert first["identity_contact_cues"] == ["EMAIL_PATTERN_PRESENT"]


def test_agent_only_contrast_and_call_id_are_distinguished() -> None:
    a = describe_effective_request(request(
        {"role": "user", "content": "Need an order update"},
        {"role": "assistant", "content": "Looking it up"},
        {"role": "tool", "content": "found", "tool_call_id": "call-a"},
        {"role": "user", "content": "Continue"}))
    b = describe_effective_request(request(
        {"role": "user", "content": "Need an order update"},
        {"role": "assistant", "content": "Checking status"},
        {"role": "tool", "content": "found", "tool_call_id": "call-b"},
        {"role": "user", "content": "Continue"}))
    pair = compare_pair(a, b)
    assert pair["isolation_status"] == "AGENT_HISTORY_ONLY_PAYLOAD_MATCH"
    assert not pair["non_agent_exact_sequence_equal"]


def test_invalid_or_missing_observation_rejected() -> None:
    with pytest.raises(ValueError, match="no messages"):
        describe_effective_request({"messages": []})
    with pytest.raises(ValueError, match="non-text"):
        describe_effective_request(request({"role": "user", "content": ["future"]}))


def test_order_number_is_not_identity_contact_evidence() -> None:
    state = describe_effective_request(request(
        {"role": "user", "content": "My order number is 1234567890"}))
    assert state["identity_contact_cues"] == []
