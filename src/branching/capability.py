"""Conservative checkpoint capability classification for WP6."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Capability(str, Enum):
    UNSUPPORTED = "UNSUPPORTED"
    AGENT_ONLY_INPUT_AVAILABLE = "AGENT_ONLY_INPUT_AVAILABLE"
    CLOSED_LOOP_REPLAY_CANDIDATE = "CLOSED_LOOP_REPLAY_CANDIDATE"
    CLOSED_LOOP_VALIDATED = "CLOSED_LOOP_VALIDATED"


@dataclass(frozen=True)
class CapabilityEvidence:
    exact_agent_effective_request: bool = False
    batch_results_checkpoint: bool = False
    environment_prefix_replay_code: bool = False
    agent_user_state_reconstruction_code: bool = False
    two_independent_restores: bool = False
    agent_request_signature_equal: bool = False
    user_state_signature_equal: bool = False
    environment_signature_equal: bool = False
    tool_pending_policy_signature_equal: bool = False
    isolated_environment_clones: bool = False
    external_session_state_controlled: bool = False


def classify_capability(evidence: CapabilityEvidence) -> Capability:
    """Never promote batch resume or DB equality into decision-level fidelity."""
    if not evidence.exact_agent_effective_request:
        return Capability.UNSUPPORTED
    code_candidate = (evidence.environment_prefix_replay_code
                      and evidence.agent_user_state_reconstruction_code)
    if not code_candidate:
        return Capability.AGENT_ONLY_INPUT_AVAILABLE
    full_fidelity = all((evidence.two_independent_restores,
                         evidence.agent_request_signature_equal,
                         evidence.user_state_signature_equal,
                         evidence.environment_signature_equal,
                         evidence.tool_pending_policy_signature_equal,
                         evidence.isolated_environment_clones,
                         evidence.external_session_state_controlled))
    return Capability.CLOSED_LOOP_VALIDATED if full_fidelity else Capability.CLOSED_LOOP_REPLAY_CANDIDATE
