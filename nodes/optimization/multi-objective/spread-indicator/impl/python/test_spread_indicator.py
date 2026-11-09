# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spread-indicator/. The authors are listed in prov/B4114Q.jsonl.

import math
import random

from spread_indicator import deb_spread, extremes, generalized_spread, spacing

E1, E2 = (0, 4), (4, 0)
R = [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]


def weakly_dominates_set(a, b):
    return all(any(all(u <= v for u, v in zip(x, y)) for x in a) for y in b)


def test_hand_values() -> None:
    assert extremes(R) == [(4, 0), (0, 4)]
    assert deb_spread([(0, 4), (2, 2), (4, 0)], E1, E2) == 0
    assert math.isclose(deb_spread([(1, 3), (3, 1)], E1, E2), 0.5)
    assert math.isclose(deb_spread([(0, 4), (1, 3), (2, 2), (4, 0)], E1, E2), 1 / 3)
    assert spacing([(0, 4), (2, 2), (4, 0)]) == 0
    # L1 nearest distances 2, 2, 2, 4: mean 5/2, squared deviations 1/4 * 3 + 9/4 = 3, over 3
    assert math.isclose(spacing([(0, 4), (1, 3), (2, 2), (4, 0)]), 1)


def test_spread_is_not_pareto_compliant() -> None:
    b = [(0, 4), (2, 2), (4, 0)]
    a = b + [(1, 3)]
    assert weakly_dominates_set(a, b) and not weakly_dominates_set(b, a)  # a is better than b
    assert deb_spread(b, E1, E2) == 0 < deb_spread(a, E1, E2)
    assert generalized_spread(b, R) == 0
    assert math.isclose(generalized_spread(a, R), 3 / 10)


def test_dominated_set_ties_a_better_set() -> None:
    # c is dominated point by point by the front points; it ties a better set in Delta and the front in spacing
    front = [(0, 4), (2, 2), (4, 0)]
    c = [(1, 5), (3, 3), (5, 1)]
    a = front + [(1, 3)]
    assert weakly_dominates_set(front, c) and not weakly_dominates_set(c, front)
    assert math.isclose(deb_spread(c, E1, E2), 1 / 3) and math.isclose(deb_spread(a, E1, E2), 1 / 3)
    assert spacing(c) == 0 == spacing(front)  # spacing does not see convergence at all


def test_ranges_and_invariance() -> None:
    rng = random.Random(6)
    for _ in range(500):
        a = [(rng.randint(0, 20), rng.randint(0, 20)) for _ in range(rng.randint(2, 8))]
        if len(set(a)) < 2:
            continue
        d = deb_spread(a, (0, 20), (20, 0))
        g = generalized_spread(a, [(0, 20), (20, 0)])
        assert 0 <= d and 0 <= g
        # scaling all objectives by the same factor does not change the values
        a2 = [(3 * x, 3 * y) for x, y in a]
        assert math.isclose(deb_spread(a2, (0, 60), (60, 0)), d, abs_tol=1e-12)
        assert math.isclose(generalized_spread(a2, [(0, 60), (60, 0)]), g, abs_tol=1e-12)
