# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hypervolume-indicator/. The authors are listed in prov/X557ES.jsonl.

import itertools
import random
from fractions import Fraction

from hypervolume_indicator import contributions, hypervolume, hypervolume_2d, weakly_dominates_set


def inclusion_exclusion(points, ref):
    pts = [x for x in points if all(u < v for u, v in zip(x, ref))]
    total = Fraction(0)
    for k in range(1, len(pts) + 1):
        for sub in itertools.combinations(pts, k):
            corner = [max(c) for c in zip(*sub)]
            vol = Fraction(1)
            for u, v in zip(corner, ref):
                vol *= v - u
            total += (-1) ** (k + 1) * vol
    return total


def grid_count(points, ref):
    """Count the unit cells [z, z + 1) with integer z whose corner z is weakly dominated."""
    pts = [x for x in points if all(u < v for u, v in zip(x, ref))]
    if not pts:
        return 0
    low = [min(c) for c in zip(*pts)]
    ranges = [range(lo, r) for lo, r in zip(low, ref)]
    return sum(1 for z in itertools.product(*ranges) if any(all(a <= b for a, b in zip(x, z)) for x in pts))


def test_example() -> None:
    a = [(1, 4), (2, 2), (4, 1)]
    b = [(1, 4), (3, 3), (4, 1)]
    assert hypervolume(a, (5, 5)) == 11 and contributions(a, (5, 5)) == [1, 4, 1]
    assert hypervolume(b, (5, 5)) == 8 and contributions(b, (5, 5)) == [2, 1, 2]
    c = [(1, 2, 3), (2, 3, 1), (3, 1, 2)]
    assert hypervolume(c, (4, 4, 4)) == 13 and contributions(c, (4, 4, 4)) == [3, 3, 3]
    # points that do not strictly dominate the reference point add nothing
    assert hypervolume(a + [(5, 0), (0, 6)], (5, 5)) == 11


def test_reference_point_changes_the_order() -> None:
    a, b = [(0, 2)], [(1, 1)]
    assert hypervolume(a, (3, 3)) == 3 < hypervolume(b, (3, 3)) == 4
    assert hypervolume(a, (3, 10)) == 24 > hypervolume(b, (3, 10)) == 18


def test_against_inclusion_exclusion_and_grid() -> None:
    rng = random.Random(3)
    for _ in range(300):
        p, n = rng.randint(1, 4), rng.randint(0, 6)
        ref = tuple([8] * p)
        pts = [tuple(rng.randint(0, 9) for _ in range(p)) for _ in range(n)]
        hv = hypervolume(pts, ref)
        assert hv == inclusion_exclusion(pts, ref) == grid_count(pts, ref)
        frac = [tuple(Fraction(rng.randint(0, 40), rng.randint(1, 5)) for _ in range(p)) for _ in range(n)]
        assert hypervolume(frac, ref) == inclusion_exclusion(frac, ref)
        if p == 2:
            assert hypervolume_2d(pts, ref) == hv


def test_pareto_compliance() -> None:
    rng = random.Random(9)
    strict = 0
    for _ in range(600):
        p = rng.randint(2, 3)
        ref = tuple([10] * p)
        a = [tuple(rng.randint(0, 9) for _ in range(p)) for _ in range(rng.randint(1, 5))]
        # b: points weakly dominated by a, and sometimes a point of a removed
        b = [tuple(min(9, u + rng.randint(0, 2)) for u in rng.choice(a)) for _ in range(rng.randint(1, 5))]
        assert weakly_dominates_set(a, b)
        ha, hb = hypervolume(a, ref), hypervolume(b, ref)
        assert ha >= hb
        if not weakly_dominates_set(b, a):
            assert ha > hb
            strict += 1
        else:
            assert ha == hb
    assert strict > 100
