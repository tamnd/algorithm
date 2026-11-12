# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/successive-cancellation-decoding/. The authors are listed in prov/CTNMA4.jsonl.

import itertools
import random
from fractions import Fraction

import successive_cancellation_decoding as scd
from successive_cancellation_decoding import (bec_bhattacharyya, f_exact, f_min_sum, leaf_llrs,
                                              polar_transform, sc_decode, sc_decode_bec)

INFO8 = [3, 5, 6, 7]
FROZEN8 = [i not in INFO8 for i in range(8)]


def codebook(n, info):
    out = []
    for msg in itertools.product((0, 1), repeat=len(info)):
        u = [0] * n
        for i, b in zip(info, msg):
            u[i] = b
        out.append((u, polar_transform(u)))
    return out


def ml(lam, book):
    """Brute force ML on a binary-input channel: maximize sum (1 - 2 x_j) lam_j. None on a tie."""
    scores = sorted(((sum((1 - 2 * b) * l for b, l in zip(x, lam)), u) for u, x in book),
                    reverse=True)
    if len(scores) > 1 and abs(scores[0][0] - scores[1][0]) < 1e-9:
        return None
    return scores[0][1]


def rank_gf2(rows):
    basis, r = [], 0
    for row in rows:
        v = int("".join(map(str, row)) or "0", 2)
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
            r += 1
    return r


def test_worked_example():
    lam = [-3.0, 2.0, 1.0, -4.0, -1.0, -2.0, -3.0, 2.0]
    u, x = sc_decode(lam, FROZEN8, f_min_sum)
    assert u == [0, 0, 0, 1, 0, 1, 1, 0]
    assert x == [1, 0, 0, 1, 0, 1, 1, 0]
    assert leaf_llrs(lam, FROZEN8, f_min_sum) == [-1.0, 1.0, 0.0, -4.0, 2.0, -6.0, -6.0, 16.0]
    assert sc_decode(lam, FROZEN8)[0] == u


def test_sc_differs_from_ml():
    lam = [4.0, -1.0, -2.0, 3.0, -1.0, 6.0, -1.0, 3.0]
    book = codebook(8, INFO8)
    assert sc_decode(lam, FROZEN8, f_min_sum)[0] == [0] * 8
    assert ml(lam, book) == [0, 0, 0, 1, 0, 1, 1, 1]
    # with the exact f, SC on the [4, 3, 2] single parity check code also differs from ML
    lam4 = [0.2, 1.3, 3.0, -0.3]
    fr = [True, False, False, False]
    assert sc_decode(lam4, fr)[1] == [0, 0, 0, 0]
    assert polar_transform(ml(lam4, codebook(4, [1, 2, 3]))) == [1, 0, 0, 1]


def test_sc_equals_ml_on_rate_one_and_repetition_codes():
    rng = random.Random(11)
    for n in (2, 4, 8):
        for info in (list(range(n)), [n - 1]):
            fr = [i not in info for i in range(n)]
            book = codebook(n, info)
            for _ in range(300):
                lam = [rng.gauss(0.3, 2.0) for _ in range(n)]
                want = ml(lam, book)
                if want is not None:
                    assert sc_decode(lam, fr)[0] == want


def test_noiseless_round_trip():
    rng = random.Random(12)
    for n in (1, 2, 4, 8, 16, 32, 64):
        for _ in range(20):
            fr = [rng.random() < 0.5 for _ in range(n)]
            u = [0 if fr[i] else rng.randrange(2) for i in range(n)]
            x = polar_transform(u)
            lam = [5.0 if b == 0 else -5.0 for b in x]
            for f in (f_exact, f_min_sum):
                assert sc_decode(lam, fr, f) == (u, x)


def test_operation_count():
    calls = {"f": 0, "g": 0}

    def fc(a, b):
        calls["f"] += 1
        return f_min_sum(a, b)

    old_g = scd.g

    def gc(a, b, u):
        calls["g"] += 1
        return old_g(a, b, u)

    scd.g = gc
    try:
        for n in range(1, 9):
            calls["f"] = calls["g"] = 0
            sc_decode([1.0] * (1 << n), [False] * (1 << n), fc)
            assert calls["f"] == calls["g"] == n * (1 << n) // 2
    finally:
        scd.g = old_g


def test_bec_leaf_erasure_probability_is_exact():
    # Genie-aided SC on BEC(eps): leaf i is erased with probability z_i exactly.
    for n in (1, 2, 3):
        big = 1 << n
        eps = Fraction(1, 3)
        z = bec_bhattacharyya(n, eps)
        prob = [Fraction(0)] * big
        for mask in range(1 << big):
            y = [None if (mask >> j) & 1 else 0 for j in range(big)]
            w = bin(mask).count("1")
            p = eps ** w * (1 - eps) ** (big - w)
            _, er = sc_decode_bec(y, [False] * big, genie=[0] * big)
            for i in range(big):
                if er[i]:
                    prob[i] += p
        assert prob == z


def test_bec_sc_versus_ml_exact():
    n, eps = 8, Fraction(1, 2)
    gen = [polar_transform([int(i == j) for j in range(n)]) for i in INFO8]
    p_sc = p_ml = Fraction(0)
    for mask in range(1 << n):
        er_pos = [(mask >> j) & 1 for j in range(n)]
        w = sum(er_pos)
        p = eps ** w * (1 - eps) ** (n - w)
        _, er = sc_decode_bec([None if e else 0 for e in er_pos], FROZEN8)
        sc_fail = any(er[i] for i in INFO8)
        cols = [[row[j] for j in range(n) if not er_pos[j]] for row in gen]
        ml_fail = rank_gf2(cols) < len(INFO8)
        assert sc_fail or not ml_fail  # ML is never worse than SC
        p_sc += p * sc_fail
        p_ml += p * ml_fail
    assert p_sc == Fraction(115, 256)
    assert p_ml == Fraction(107, 256)


def test_bec_llr_form_agrees_with_symbolic_form():
    rng = random.Random(13)
    for _ in range(600):
        n = 1 << rng.randrange(1, 6)
        fr = [rng.random() < 0.5 for _ in range(n)]
        u = [0 if fr[i] else rng.randrange(2) for i in range(n)]
        x = polar_transform(u)
        e = rng.random()
        y = [None if rng.random() < e else b for b in x]
        ub, er = sc_decode_bec(y, fr)
        if any(er[i] for i in range(n) if not fr[i]):
            continue
        assert ub == u
        lam = [0.0 if v is None else (40.0 if v == 0 else -40.0) for v in y]
        assert sc_decode(lam, fr)[0] == u
