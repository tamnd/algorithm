# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-conjugate/. The authors are listed in prov/VCH05B.jsonl.

import random
from fractions import Fraction as F

from convex_conjugate import discrete_conjugate, lower_hull


def brute(xs, fs, s):
    return max(s * x - f for x, f in zip(xs, fs))


def test_square_example():
    xs = [-2, -1, 0, 1, 2]
    fs = [x * x for x in xs]
    slopes = [F(-3), F(-1), F(0), F(1, 2), F(1), F(3), F(4), F(5)]
    assert discrete_conjugate(xs, fs, slopes) == [2, 0, 0, 0, 0, 2, 4, 6]
    # the continuous conjugate s^2/4 lies below, since the samples are a subset of R
    for s, v in zip(slopes, discrete_conjugate(xs, fs, slopes)):
        assert v <= s * s / 4


def test_piecewise_linear_hinge():
    # f = max(0, x) sampled on -3..3. The conjugate is 0 for s in [0, 1].
    # Outside, the maximum is at an end point: f*(2) = 6 - 3 and f*(-1) = 3 - 0.
    xs = list(range(-3, 4))
    fs = [max(0, x) for x in xs]
    assert discrete_conjugate(xs, fs, [F(0), F(1, 2), F(1)]) == [0, 0, 0]
    assert discrete_conjugate(xs, fs, [F(2), F(-1)]) == [3, 3]


def test_random_against_brute_force():
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 12)
        xs = [F(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(n)]
        fs = [F(rng.randint(-30, 30), rng.randint(1, 3)) for _ in range(n)]
        slopes = [F(rng.randint(-40, 40), rng.randint(1, 5)) for _ in range(rng.randint(1, 15))]
        got = discrete_conjugate(xs, fs, slopes)
        assert got == [brute(xs, fs, s) for s in slopes]


def test_fenchel_young_and_biconjugate():
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randint(2, 10)
        xs = sorted({F(rng.randint(-10, 10)) for _ in range(n)})
        fs = [F(rng.randint(-10, 10)) for _ in xs]
        hull = lower_hull(list(zip(xs, fs)))
        edge = [(y2 - y1) / (x2 - x1) for (x1, y1), (x2, y2) in zip(hull, hull[1:])]
        slopes = edge + [F(rng.randint(-30, 30), 3) for _ in range(10)]
        conj = discrete_conjugate(xs, fs, slopes)
        for x, f in zip(xs, fs):
            for s, c in zip(slopes, conj):
                assert f + c >= s * x  # Fenchel-Young
        # f**(x) over these slopes: never above f, equal at hull vertices
        vertices = dict(hull)
        for x, f in zip(xs, fs):
            bic = max(s * x - c for s, c in zip(slopes, conj))
            assert bic <= f
            if x in vertices and vertices[x] == f and len(hull) >= 2:
                assert bic == f
