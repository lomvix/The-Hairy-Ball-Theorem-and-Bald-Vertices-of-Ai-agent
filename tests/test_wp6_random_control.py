from collections import Counter

import pytest

from src.branching.random_control import balanced_random_controls, inclusion_probability


def test_balanced_random_controls_are_reproducible_and_cover_nine_cells() -> None:
    cells = {(f"model_{m}", f"domain_{d}"): [f"{m}-{d}-{i}" for i in range(20)]
             for m in range(3) for d in range(3)}
    first, bonus = balanced_random_controls(cells, seed=20261014)
    second, again = balanced_random_controls(cells, seed=20261014)
    assert first == second and bonus == again
    counts = Counter(tuple(value.split("-")[:2]) for value in first)
    assert len(counts) == 9
    assert sorted(counts.values()) == [1] * 8 + [2]


def test_exact_inclusion_probability_for_equal_cells() -> None:
    # One guaranteed draw plus a 1/9 chance that this cell receives a second.
    assert inclusion_probability(20, 9) == pytest.approx(10 / (9 * 20))


@pytest.mark.parametrize("size,count", [(0, 9), (1, 9), (2, 0)])
def test_inclusion_probability_rejects_invalid_frame(size: int, count: int) -> None:
    with pytest.raises(ValueError):
        inclusion_probability(size, count)
