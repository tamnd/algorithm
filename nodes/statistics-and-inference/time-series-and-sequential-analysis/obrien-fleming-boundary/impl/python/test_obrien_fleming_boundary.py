# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/obrien-fleming-boundary/. The authors are listed in prov/C11SHN.jsonl.
import math
import random

import pytest

from obrien_fleming_boundary import (
    boundary_constant,
    cross_on_score_scale,
    crossing_probabilities,
    expected_information,
    norm_quantile,
    obrien_fleming_boundary,
    pocock_boundary,
    total_crossing,
)


def phi(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def upper(x: float) -> float:
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def two_look_quadrature(c1: float, c2: float, t1: float, n: int = 400) -> float:
    """P(|Z1| >= c1 or (|Z1| < c1 and |Z2| >= c2)) with Z2 | Z1 = z ~ N(sqrt(t1) z, 1 - t1).

    One-dimensional composite Simpson rule on the z scale: an oracle that does
    not share the score-scale recursion of the code under test.
    """
    s, v = math.sqrt(t1), math.sqrt(1.0 - t1)
    h = 2.0 * c1 / n
    acc = 0.0
    for i in range(n + 1):
        z = -c1 + i * h
        w = 1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)
        acc += w * phi(z) * (upper((c2 - s * z) / v) + upper((c2 + s * z) / v))
    return 2.0 * upper(c1) + acc * h / 3.0


def test_one_look_is_the_fixed_sample_test():
    c, bounds = obrien_fleming_boundary(1)
    assert abs(c - 1.959964) < 1e-6
    assert bounds == [c]
    p, _ = pocock_boundary(1)
    assert abs(p - c) < 1e-9


def test_worked_example_five_looks():
    c, bounds = obrien_fleming_boundary(5)
    assert abs(c - 2.0401) < 1e-4
    expected = [4.5617, 3.2256, 2.6337, 2.2809, 2.0401]
    assert all(abs(a - b) < 1e-4 for a, b in zip(bounds, expected))
    p, pb = pocock_boundary(5)
    assert abs(p - 2.4132) < 1e-4
    assert all(abs(x - p) < 1e-12 for x in pb)


@pytest.mark.parametrize("k", [2, 3, 4, 5])
def test_total_level_is_alpha(k):
    for kind in ("obrien-fleming", "pocock"):
        _, bounds = boundary_constant(kind, k)
        assert abs(total_crossing(bounds, list(range(1, k + 1))) - 0.05) < 1e-6


def test_grid_doubling_converges():
    info = [1.0, 2.0, 3.0, 4.0, 5.0]
    p8, p16, p32 = (cross_on_score_scale(2.0401, info, r=r) for r in (8, 16, 32))
    assert abs(p16 - p32) < 1e-8
    assert abs(p8 - p32) < 1e-7


def test_score_scale_cross_matches_z_scale():
    info = [1.0, 2.0, 3.0, 4.0, 5.0]
    for c in (1.8, 2.04, 2.3):
        z_bounds = [c * math.sqrt(5.0 / i) for i in info]
        assert abs(cross_on_score_scale(c, info) - total_crossing(z_bounds, info)) < 1e-12


def test_crossing_decreases_in_c():
    info = [1.0, 2.0, 3.0]
    values = [cross_on_score_scale(c, info) for c in (1.5, 1.8, 2.0, 2.2, 2.5)]
    assert all(a > b for a, b in zip(values, values[1:]))


def test_two_looks_against_quadrature():
    for kind in ("obrien-fleming", "pocock"):
        _, (c1, c2) = boundary_constant(kind, 2)
        assert abs(two_look_quadrature(c1, c2, 0.5) - 0.05) < 1e-7


def test_random_two_look_boundaries_against_quadrature():
    rng = random.Random(20260314)
    for _ in range(500):
        t1 = rng.uniform(0.1, 0.9)
        c1 = rng.uniform(1.0, 4.0)
        c2 = rng.uniform(1.0, 4.0)
        got = total_crossing([c1, c2], [t1, 1.0])
        # Both sides use Simpson grids; their discretization errors stay below 5e-7.
        assert abs(got - two_look_quadrature(c1, c2, t1)) < 5e-7


def test_monte_carlo_level_and_stage_split():
    rng = random.Random(7)
    _, bounds = obrien_fleming_boundary(5)
    reps = 20000
    hits = 0
    for _ in range(reps):
        s = 0.0
        for k in range(1, 6):
            s += rng.gauss(0.0, 1.0)
            if abs(s / math.sqrt(k)) >= bounds[k - 1]:
                hits += 1
                break
    se = math.sqrt(0.05 * 0.95 / reps)
    assert abs(hits / reps - 0.05) < 4 * se


def test_unequal_information_and_drift():
    info = [0.3, 0.7, 1.0]
    c, bounds = obrien_fleming_boundary(3, info=info)
    assert abs(total_crossing(bounds, info) - 0.05) < 1e-6
    # Under drift the rejection probability rises, and early stops cut the expected information.
    assert total_crossing(bounds, [i * 10 for i in info], theta=1.0) > 0.5
    assert expected_information(bounds, [i * 10 for i in info], theta=1.0) < 10.0
    parts = crossing_probabilities(bounds, info)
    assert all(abs(u - l) < 1e-12 for u, l in parts)


def test_inflation_factor_five_looks():
    fixed = (norm_quantile(0.975) + norm_quantile(0.9)) ** 2
    for kind, want in (("obrien-fleming", 1.0265), ("pocock", 1.2065)):
        _, bounds = boundary_constant(kind, 5)

        def power(imax: float) -> float:
            return total_crossing(bounds, [k / 5 * imax for k in range(1, 6)], theta=1.0)

        lo, hi = fixed, 2 * fixed
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if power(mid) < 0.9 else (lo, mid)
        assert abs(lo / fixed - want) < 1e-3


def test_bad_input():
    with pytest.raises(ValueError):
        obrien_fleming_boundary(3, info=[1.0, 2.0])
    with pytest.raises(ValueError):
        total_crossing([2.0, 2.0], [1.0, 1.0])
    with pytest.raises(ValueError):
        boundary_constant("haybittle", 3)
