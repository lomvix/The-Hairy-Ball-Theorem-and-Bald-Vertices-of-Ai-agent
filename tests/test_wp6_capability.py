from dataclasses import replace

from src.branching.capability import Capability, CapabilityEvidence, classify_capability


def test_batch_checkpoint_is_not_decision_checkpoint():
    assert classify_capability(CapabilityEvidence(batch_results_checkpoint=True)) == Capability.UNSUPPORTED


def test_exact_request_only_allows_agent_only_input_scope():
    evidence = CapabilityEvidence(exact_agent_effective_request=True,
                                  batch_results_checkpoint=True)
    assert classify_capability(evidence) == Capability.AGENT_ONLY_INPUT_AVAILABLE


def test_environment_replay_code_is_candidate_not_validated_restore():
    evidence = CapabilityEvidence(exact_agent_effective_request=True,
                                  environment_prefix_replay_code=True,
                                  agent_user_state_reconstruction_code=True,
                                  environment_signature_equal=True)
    assert classify_capability(evidence) == Capability.CLOSED_LOOP_REPLAY_CANDIDATE


def test_user_or_session_mismatch_rejects_closed_loop_validation():
    complete = CapabilityEvidence(**{field: True for field in CapabilityEvidence.__dataclass_fields__})
    assert classify_capability(complete) == Capability.CLOSED_LOOP_VALIDATED
    assert classify_capability(replace(complete, user_state_signature_equal=False)) != Capability.CLOSED_LOOP_VALIDATED
    assert classify_capability(replace(complete, external_session_state_controlled=False)) != Capability.CLOSED_LOOP_VALIDATED
