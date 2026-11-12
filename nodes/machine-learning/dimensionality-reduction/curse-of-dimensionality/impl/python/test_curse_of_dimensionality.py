# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/curse-of-dimensionality/. The authors are listed in prov/QWKNH3.jsonl.

from fractions import Fraction
import math
import random

import pytest

from curse_of_dimensionality import (
    ball_volume,
    ball_volume_exact,
    contrast_experiment,
    edge_for_fraction,
    grid_cells,
    median_nn_distance,
    relative_contrast,
    samples_for_error,
    shell_fraction,
    stone_rate,
)


def test_exact_ball_volumes_for_small_d() -> None:
    expected = {
        0: (Fraction(1), 0),
        1: (Fraction(2), 0),
        2: (Fraction(1), 1),
        3: (Fraction(4, 3), 1),
        4: (Fraction(1, 2), 2),
        5: (Fraction(8, 15), 2),
        6: (Fraction(1, 6), 3),
    }
    for d, cj in expected.items():
        assert ball_volume_exact(d) == cj
        c, j = cj
        assert ball_volume(d) == pytest.approx(float(c) * math.pi ** j, rel=1e-12)


def test_gamma_formula_matches_recursion() -> None:
    for d in range(0, 40):
        c, j = ball_volume_exact(d)
        assert ball_volume(d) == pytest.approx(float(c) * math.pi ** j, rel=1e-12)
    assert ball_volume(3, 2.0) == pytest.approx(32 * math.pi / 3)


def test_volume_peaks_at_five_and_goes_to_zero() -> None:
    vols = [ball_volume(d) for d in range(0, 60)]
    assert max(range(60), key=lambda d: vols[d]) == 5
    assert all(vols[d + 1] < vols[d] for d in range(5, 59))
    assert vols[20] == pytest.approx(math.pi ** 10 / math.factorial(10))
    assert vols[59] < 1e-15
    assert ball_volume(10) / 2 ** 10 == pytest.approx(0.00249, abs=1e-5)


def test_shell_edge_and_grid() -> None:
    assert shell_fraction(2, 0.01) == pytest.approx(0.0199)
    assert shell_fraction(500, 0.01) > 0.99
    assert edge_for_fraction(0.1, 10) == pytest.approx(0.794, abs=1e-3)
    assert edge_for_fraction(0.01, 10) == pytest.approx(0.631, abs=1e-3)
    assert median_nn_distance(500, 10) == pytest.approx(0.518, abs=1e-3)
    assert grid_cells(10, 10) == 10 ** 10
    assert grid_cells(2, 64) == 2 ** 64


def test_median_nn_distance_by_simulation() -> None:
    rng = random.Random(5)
    n, d, trials = 50, 4, 400

    def uniform_in_ball() -> list[float]:
        while True:
            p = [rng.uniform(-1, 1) for _ in range(d)]
            if sum(x * x for x in p) <= 1:
                return p

    nearest = sorted(
        min(math.sqrt(sum(x * x for x in uniform_in_ball())) for _ in range(n)) for _ in range(trials)
    )
    assert nearest[trials // 2] == pytest.approx(median_nn_distance(n, d), abs=0.03)


def test_relative_contrast_shrinks_with_dimension() -> None:
    rng = random.Random(2024)
    contrasts = {d: contrast_experiment(d, 100, 20, rng) for d in (2, 10, 100, 1000)}
    assert contrasts[2] > contrasts[10] > contrasts[100] > contrasts[1000]
    assert contrasts[2] > 5
    assert contrasts[1000] < 0.15
    assert relative_contrast([[3.0, 0.0], [0.0, 1.0]], [0.0, 0.0]) == pytest.approx(2.0)
    with pytest.raises(ValueError):
        relative_contrast([[1.0, 1.0]], [1.0, 1.0])


def test_stone_rates() -> None:
    assert stone_rate(10 ** 4, 2, 4) == pytest.approx(10 ** -2)
    assert samples_for_error(0.01, 2, 2) == pytest.approx(1000)
    assert samples_for_error(0.01, 2, 10) == pytest.approx(10 ** 7)
    assert samples_for_error(0.01, 2, 20) == pytest.approx(10 ** 12)
    for d in (1, 3, 7):
        assert stone_rate(samples_for_error(0.05, 1.5, d), 1.5, d) == pytest.approx(0.05)
