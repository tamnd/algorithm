# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variance-shadow-maps/. The authors are listed in prov/BNWA0B.jsonl.

import random
from fractions import Fraction

from variance_shadow_maps import (
    box_filter,
    chebyshev_upper_bound,
    lit_fraction,
    moments,
    reduce_bleeding,
    vsm_lookup,
)


def random_map(rng, w, h):
    return [[Fraction(rng.randrange(0, 33), 32) for _ in range(w)] for _ in range(h)]


def box_taps(s, i, j, r):
    h, w = len(s), len(s[0])
    return [s[y][x] for y in range(max(j - r, 0), min(j + r + 1, h))
            for x in range(max(i - r, 0), min(i + r + 1, w))]


def test_light_bleeding_numbers():
    # Half the texels at depth 1 and half at depth 2, receiver at 3.
    d = [Fraction(1), Fraction(2)]
    m1 = sum(d) / 2
    m2 = sum(x * x for x in d) / 2
    assert chebyshev_upper_bound(m1, m2, 3) == Fraction(1, 10)
    assert lit_fraction(d, 3) == 0
    # Two occluders at 1 and 9 over a receiver at 10.
    d = [Fraction(1), Fraction(9)]
    m1 = sum(d) / 2
    m2 = sum(x * x for x in d) / 2
    assert chebyshev_upper_bound(m1, m2, 10) == Fraction(16, 41)
    assert lit_fraction(d, 10) == 0


def test_summed_area_filter_equals_direct_box():
    rng = random.Random(1)
    for _ in range(20):
        w, h = rng.randrange(3, 12), rng.randrange(3, 12)
        s = random_map(rng, w, h)
        for r in range(3):
            fm = box_filter(moments(s), r)
            for j in range(h):
                for i in range(w):
                    taps = box_taps(s, i, j, r)
                    assert fm[j][i][0] == sum(taps) / len(taps)
                    assert fm[j][i][1] == sum(t * t for t in taps) / len(taps)


def test_upper_bound_on_the_lit_fraction():
    rng = random.Random(2)
    for _ in range(40):
        s = random_map(rng, 9, 9)
        r = rng.randrange(0, 3)
        fm = box_filter(moments(s), r)
        for _ in range(20):
            i, j = rng.randrange(9), rng.randrange(9)
            t = Fraction(rng.randrange(0, 40), 32)
            p = vsm_lookup(fm, i, j, t)
            assert 0 <= p <= 1
            assert p >= lit_fraction(box_taps(s, i, j, r), t)


def test_exact_for_one_planar_occluder_and_one_planar_receiver():
    rng = random.Random(3)
    for _ in range(300):
        d_occ = Fraction(rng.randrange(0, 32), 64)
        d_rec = d_occ + Fraction(rng.randrange(1, 32), 64)
        k = rng.randrange(1, 9)
        n = rng.randrange(k + 1, 20)
        depths = [d_occ] * k + [d_rec] * (n - k)
        m1 = sum(depths) / n
        m2 = sum(x * x for x in depths) / n
        assert chebyshev_upper_bound(m1, m2, d_rec) == lit_fraction(depths, d_rec)


def test_sharp_for_every_mean_and_variance():
    # Cantelli is attained by the two-point law at t and m - v / (t - m).
    rng = random.Random(4)
    for _ in range(200):
        m = Fraction(rng.randrange(0, 50), 64)
        v = Fraction(rng.randrange(1, 50), 4096)
        t = m + Fraction(rng.randrange(1, 40), 64)
        q = v / (v + (t - m) ** 2)
        a = m - v / (t - m)
        assert q * t + (1 - q) * a == m
        assert q * t * t + (1 - q) * a * a - m * m == v
        assert chebyshev_upper_bound(m, v + m * m, t) == q


def test_min_variance_and_bleeding_reduction():
    assert chebyshev_upper_bound(Fraction(1, 2), Fraction(1, 4), Fraction(1, 2)) == 1
    assert chebyshev_upper_bound(Fraction(1, 2), Fraction(1, 4), Fraction(3, 4)) == 0
    p = chebyshev_upper_bound(Fraction(1, 2), Fraction(1, 4), Fraction(1, 2) + Fraction(1, 100),
                              min_var=Fraction(1, 10000))
    assert p == Fraction(1, 2)
    rng = random.Random(5)
    for _ in range(200):
        p = Fraction(rng.randrange(0, 101), 100)
        a = Fraction(rng.randrange(0, 100), 100)
        q = reduce_bleeding(p, a)
        assert 0 <= q <= p
        if p <= a:
            assert q == 0
    assert reduce_bleeding(Fraction(1, 10), Fraction(1, 5)) == 0
    assert reduce_bleeding(Fraction(16, 41), Fraction(1, 5)) == Fraction(39, 164)


def test_float_path_agrees():
    rng = random.Random(6)
    s = random_map(rng, 8, 8)
    fe = box_filter(moments(s), 1)
    sf = [[float(d) for d in row] for row in s]
    ff = box_filter(moments(sf), 1)
    for j in range(8):
        for i in range(8):
            t = 0.7
            assert abs(vsm_lookup(fe, i, j, Fraction(7, 10)) - vsm_lookup(ff, i, j, t)) < 1e-9
