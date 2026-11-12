# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/channel-polarization-theorem/. The authors are listed in prov/Q74BAQ.jsonl.

import math
from fractions import Fraction

from channel_polarization_theorem import (bec, bec_log2_z, bec_z, bhattacharyya,
                                          bhattacharyya_of_table, bsc, channel_tree,
                                          fraction_below, minus, plus, polarization_fractions,
                                          symmetric_capacity, synthetic_channel)


def test_bec_synthetic_channels_are_becs_with_the_recursion():
    eps = 0.3
    for n in (1, 2):
        z = bec_z(n, eps)
        for i in range(1 << n):
            t = synthetic_channel(bec(eps), n, i)
            assert math.isclose(bhattacharyya_of_table(t), z[i], abs_tol=1e-12)
            erased = 0.0
            for p0, p1 in t.values():
                # each output either fixes u_i or says nothing about it: a BEC
                assert p0 == 0 or p1 == 0 or math.isclose(p0, p1)
                if p0 > 0 and p1 > 0:
                    erased += p0
            assert math.isclose(erased, z[i], abs_tol=1e-12)


def test_recursion_order_matches_brute_force_on_bsc():
    w = bsc(0.1)
    tree = channel_tree(w, 2)
    for i in range(4):
        t = synthetic_channel(w, 2, i)
        assert math.isclose(bhattacharyya_of_table(t), bhattacharyya(tree[i]), abs_tol=1e-12)


def test_single_step_identities():
    for w in (bsc(0.11), bsc(0.3), bec(0.4), ([0.5, 0.3, 0.2], [0.1, 0.3, 0.6])):
        z, i = bhattacharyya(w), symmetric_capacity(w)
        wm, wp = minus(w), plus(w)
        assert math.isclose(symmetric_capacity(wm) + symmetric_capacity(wp), 2 * i, abs_tol=1e-12)
        assert math.isclose(bhattacharyya(wp), z * z, abs_tol=1e-12)
        assert z - 1e-12 <= bhattacharyya(wm) <= 2 * z - z * z + 1e-12
    z = bhattacharyya(bsc(0.11))
    assert bhattacharyya(minus(bsc(0.11))) < 2 * z - z * z - 0.05  # strict off the BEC
    z = bhattacharyya(bec(0.4))
    assert math.isclose(bhattacharyya(minus(bec(0.4))), 2 * z - z * z)


def test_capacity_is_conserved():
    for w in (bsc(0.2), bec(0.25)):
        tree = channel_tree(w, 2)
        assert math.isclose(sum(symmetric_capacity(c) for c in tree), 4 * symmetric_capacity(w),
                            abs_tol=1e-9)


def test_mean_is_kept_exactly():
    for eps in (Fraction(1, 2), Fraction(1, 3), Fraction(4, 5)):
        for n in range(7):
            z = bec_z(n, eps)
            assert sum(z) / len(z) == eps


def test_variance_term_decays_as_proved():
    # a_n = mean of z (1 - z) satisfies a_(n+1) = a_n - mean(q^2) <= a_n - a_n^2 <= 1/(n + 4)
    for eps in (0.5, 0.2, 0.9):
        prev = None
        for n in range(16):
            z = bec_z(n, eps)
            a = sum(v * (1 - v) for v in z) / len(z)
            assert a <= 1 / (n + 4) + 1e-12
            if prev is not None:
                assert a <= prev - prev * prev + 1e-12
            prev = a


def test_fractions_tend_to_capacity():
    eps, delta = 0.3, 0.01
    mids = []
    for n in (5, 10, 15, 20):
        good, bad, mid = polarization_fractions(n, eps, delta)
        mids.append(mid)
        assert mid <= 1 / (delta * (1 - delta) * (n + 4))
        assert good <= (1 - eps) / (1 - delta) + 1e-12  # from E[1 - Z] = 1 - eps
    assert mids == sorted(mids, reverse=True)
    good, bad, mid = polarization_fractions(20, eps, delta)
    assert abs(good - 0.7) < 0.02 and abs(bad - 0.3) < 0.02


def test_rate_of_polarization_direction():
    # beta < 1/2: the fraction with Z <= 2^(-N^beta) grows toward 1 - eps;
    # beta > 1/2: it falls.
    small = [fraction_below(n, 0.5, 0.4) for n in (10, 15, 20)]
    large = [fraction_below(n, 0.5, 0.6) for n in (10, 15, 20)]
    assert small == sorted(small) and small[-1] < 0.5
    assert large == sorted(large, reverse=True)


def test_log_domain_matches_direct():
    z = bec_z(10, 0.4)
    lz = bec_log2_z(10, 0.4)
    for a, b in zip(z, lz):
        if a > 1e-300:
            assert math.isclose(math.log2(a), b, rel_tol=1e-9, abs_tol=1e-9)
