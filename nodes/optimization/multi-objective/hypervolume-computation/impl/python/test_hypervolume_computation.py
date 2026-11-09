# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hypervolume-computation/. The authors are listed in prov/BQ3B9A.jsonl.

import itertools
import random
from fractions import Fraction

from hypervolume_computation import hv2d, hv3d, hypervolume


def inclusion_exclusion(points, ref):
    pts = [x for x in points if all(u < v for u, v in zip(x, ref))]
    total = Fraction(0)
    for k in range(1, len(pts) + 1):
        for sub in itertools.combinations(pts, k):
            vol = Fraction(1)
            for u, v in zip([max(c) for c in zip(*sub)], ref):
                vol *= v - u
            total += (-1) ** (k + 1) * vol
    return total


def grid_count(points, ref):
    pts = [x for x in points if all(u < v for u, v in zip(x, ref))]
    if not pts:
        return 0
    ranges = [range(min(c), r) for c, r in zip(zip(*pts), ref)]
    return sum(1 for z in itertools.product(*ranges) if any(all(a <= b for a, b in zip(x, z)) for x in pts))


def test_example_trace() -> None:
    pts = [(1, 2, 3), (2, 3, 1), (3, 1, 2)]
    trace = []
    total = hv3d(pts, (4, 4, 4), lambda q, vol, area: trace.append((q, vol, area)))
    assert trace == [((2, 3, 1), 0, 2), ((3, 1, 2), 2, 4), ((1, 2, 3), 6, 7)]
    assert total == 13 == inclusion_exclusion(pts, (4, 4, 4))
    assert hv2d([(1, 4), (2, 2), (4, 1)], (5, 5)) == 11


def test_ties_and_duplicates() -> None:
    ref = (5, 5, 5)
    pts = [(1, 1, 1), (1, 1, 1), (1, 2, 1), (2, 1, 1), (1, 1, 3), (0, 4, 2), (0, 4, 2), (4, 0, 4)]
    assert hv3d(pts, ref) == inclusion_exclusion(pts, ref) == grid_count(pts, ref)
    assert hv3d([], ref) == 0 and hv3d([(5, 1, 1)], ref) == 0


def test_against_inclusion_exclusion_and_grid() -> None:
    rng = random.Random(4)
    for _ in range(400):
        p, n = rng.randint(1, 5), rng.randint(0, 7)
        ref = tuple([7] * p)
        pts = [tuple(rng.randint(0, 8) for _ in range(p)) for _ in range(n)]
        hv = hypervolume(pts, ref)
        assert hv == inclusion_exclusion(pts, ref)
        if p <= 4:
            assert hv == grid_count(pts, ref)
        frac = [tuple(Fraction(rng.randint(0, 30), rng.randint(1, 4)) for _ in range(p)) for _ in range(n)]
        assert hypervolume(frac, ref) == inclusion_exclusion(frac, ref)


def test_sweeps_agree_on_larger_sets() -> None:
    rng = random.Random(8)
    for _ in range(30):
        n = rng.randint(20, 80)
        ref = (50, 50, 50)
        pts = [tuple(rng.randint(0, 49) for _ in range(3)) for _ in range(n)]
        z_cuts = sorted({q[2] for q in pts} | {50})
        # slice by hand with the 2D sweep, as a reference for the 3D sweep
        want = 0
        for lo, hi in zip(z_cuts, z_cuts[1:]):
            want += (hi - lo) * hv2d([q[:2] for q in pts if q[2] <= lo], ref[:2])
        assert hv3d(pts, ref) == want
