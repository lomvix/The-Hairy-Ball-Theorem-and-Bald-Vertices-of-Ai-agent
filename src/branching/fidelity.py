"""WP6 two-restore fidelity contract; pure checks, no simulator or API calls."""

from __future__ import annotations

from dataclasses import dataclass, fields


@dataclass(frozen=True)
class CheckpointSignature:
    agent_effective_request_hash: str | None
    agent_message_history_hash: str | None
    user_simulator_context_hash: str | None
    user_simulator_internal_state_hash: str | None
    environment_semantic_hash: str | None
    tool_state_hash: str | None
    pending_actions_hash: str | None
    policy_tool_schema_config_hash: str | None
    memory_snapshot_hash: str | None
    orchestrator_turn_phase: str | None
    external_session_state_hash: str | None


@dataclass(frozen=True)
class FidelityResult:
    status: str
    mismatched_fields: tuple[str, ...]
    missing_fields: tuple[str, ...]
    restore_count: int


def validate_two_restores(
    reference: CheckpointSignature,
    restore_a: CheckpointSignature,
    restore_b: CheckpointSignature,
    *,
    restore_a_id: str,
    restore_b_id: str,
    isolated_clones: bool,
    external_session_controlled: bool,
    persistent_memory_present: bool,
) -> FidelityResult:
    """Closed-loop PASS requires every causal component in two distinct restores."""
    required = {field.name for field in fields(CheckpointSignature)}
    if not persistent_memory_present:
        required.remove("memory_snapshot_hash")
    if not external_session_controlled:
        # A missing external-session hash is not silently ignored: return FAIL.
        required.remove("external_session_state_hash")
    missing = set()
    mismatched = set()
    if not restore_a_id or not restore_b_id or restore_a_id == restore_b_id:
        missing.add("two_distinct_restore_ids")
    for name in required:
        values = [getattr(item, name) for item in (reference, restore_a, restore_b)]
        if any(value is None or value == "" for value in values):
            missing.add(name)
        elif len(set(values)) != 1:
            mismatched.add(name)
    if not isolated_clones:
        missing.add("isolated_environment_clones")
    if not external_session_controlled:
        missing.add("external_session_state_control")
    if not persistent_memory_present and any(item.memory_snapshot_hash is not None
                                             for item in (reference, restore_a, restore_b)):
        mismatched.add("memory_presence_declaration")
    status = "CLOSED_LOOP_FIDELITY_PASS" if not missing and not mismatched else "CLOSED_LOOP_FIDELITY_FAIL"
    return FidelityResult(status=status, mismatched_fields=tuple(sorted(mismatched)),
                          missing_fields=tuple(sorted(missing)), restore_count=2)
