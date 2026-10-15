"""Exact probabilities for a balanced one-per-cell plus one-bonus-cell design."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import random


def inclusion_probability(cell_size: int, cell_count: int) -> float:
    """For each cell, draw one; uniformly choose one cell for a second draw."""
    if cell_size < 2 or cell_count < 1:
        raise ValueError("all cells must contain at least two candidates")
    return (1.0 + 1.0 / cell_count) / cell_size


def balanced_random_controls(
    cells: Mapping[tuple[str, str], Sequence[str]], *, seed: int
) -> tuple[list[str], tuple[str, str]]:
    """Sample from sorted candidates; no outcome-adaptive redraw or exclusion."""
    ordered_cells = sorted(cells)
    if len(ordered_cells) != 9:
        raise ValueError("expected the full 3×3 model-domain design")
    for cell in ordered_cells:
        candidates = cells[cell]
        if len(candidates) < 2 or len(candidates) != len(set(candidates)):
            raise ValueError("cell needs at least two distinct candidates")
    rng = random.Random(seed)
    bonus_cell = ordered_cells[rng.randrange(len(ordered_cells))]
    selected = []
    for cell in ordered_cells:
        selected.extend(rng.sample(sorted(cells[cell]), 2 if cell == bonus_cell else 1))
    if len(selected) != 10 or len(set(selected)) != 10:
        raise AssertionError("balanced sampler returned an invalid sample")
    return selected, bonus_cell
