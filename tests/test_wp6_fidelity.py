from dataclasses import replace

from src.branching.fidelity import CheckpointSignature, validate_two_restores


def _signature():
    return CheckpointSignature(
        agent_effective_request_hash="a", agent_message_history_hash="h",
        user_simulator_context_hash="u", user_simulator_internal_state_hash="ui",
        environment_semantic_hash="e", tool_state_hash="t", pending_actions_hash="p",
        policy_tool_schema_config_hash="c", memory_snapshot_hash=None,
        orchestrator_turn_phase="USER_TO_AGENT", external_session_state_hash="s")


def test_two_exact_isolated_restores_pass():
    signature = _signature()
    result = validate_two_restores(signature, signature, signature,
                                   restore_a_id="restore_a", restore_b_id="restore_b",
                                   isolated_clones=True, external_session_controlled=True,
                                   persistent_memory_present=False)
    assert result.status == "CLOSED_LOOP_FIDELITY_PASS"
    assert result.restore_count == 2


def test_matching_environment_alone_does_not_prove_user_restoration():
    signature = _signature()
    changed = replace(signature, user_simulator_internal_state_hash="different")
    result = validate_two_restores(signature, signature, changed,
                                   restore_a_id="restore_a", restore_b_id="restore_b",
                                   isolated_clones=True, external_session_controlled=True,
                                   persistent_memory_present=False)
    assert result.status == "CLOSED_LOOP_FIDELITY_FAIL"
    assert "user_simulator_internal_state_hash" in result.mismatched_fields


def test_unknown_server_session_cannot_pass():
    signature = _signature()
    result = validate_two_restores(signature, signature, signature,
                                   restore_a_id="restore_a", restore_b_id="restore_b",
                                   isolated_clones=True, external_session_controlled=False,
                                   persistent_memory_present=False)
    assert result.status == "CLOSED_LOOP_FIDELITY_FAIL"
    assert "external_session_state_control" in result.missing_fields


def test_missing_pending_or_clone_is_failure():
    signature = _signature()
    changed = replace(signature, pending_actions_hash=None)
    result = validate_two_restores(signature, changed, signature,
                                   restore_a_id="restore_a", restore_b_id="restore_b",
                                   isolated_clones=False, external_session_controlled=True,
                                   persistent_memory_present=False)
    assert result.status == "CLOSED_LOOP_FIDELITY_FAIL"
    assert "pending_actions_hash" in result.missing_fields
    assert "isolated_environment_clones" in result.missing_fields


def test_duplicate_restore_identifier_is_rejected():
    signature = _signature()
    result = validate_two_restores(signature, signature, signature,
                                   restore_a_id="same", restore_b_id="same",
                                   isolated_clones=True, external_session_controlled=True,
                                   persistent_memory_present=False)
    assert "two_distinct_restore_ids" in result.missing_fields
