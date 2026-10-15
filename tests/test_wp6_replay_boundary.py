import pytest

from src.branching.replay_boundary import post_initial_messages


def test_post_initial_messages_exact_boundary() -> None:
    initial = [{"role": "assistant", "content": "hello"}]
    later = [{"role": "user", "content": "help"},
             {"role": "assistant", "tool_calls": [{"id": "call_1"}]},
             {"role": "tool", "content": "done"}]
    assert post_initial_messages(initial, initial + later) == later


@pytest.mark.parametrize(
    ("initial", "decision", "message"),
    [
        ([{"role": "user"}], [], "longer"),
        ([{"role": "assistant", "content": "one"}],
         [{"role": "assistant", "content": "two"}], "does not begin"),
        ([{"role": "assistant", "tool_calls": [{"id": "call_1"}]}],
         [{"role": "assistant", "tool_calls": [{"id": "call_1"}]},
          {"role": "tool", "content": "done"}], "pending tool call"),
        ([{"role": "assistant", "content": "hello"}],
         [{"role": "assistant", "content": "hello"},
          {"role": "tool", "content": "orphan"}], "splits a tool call"),
    ],
)
def test_post_initial_messages_rejects_unfaithful_boundary(
    initial: list[dict], decision: list[dict], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        post_initial_messages(initial, decision)
