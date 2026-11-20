# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/turbo-equalization/. The authors are listed in prov/XNK681.jsonl.

import itertools
import math
import random

import pytest

from turbo_equalization import bcjr_decoder, bcjr_equalizer, deinterleave, encode, interleave, turbo_equalize

PROAKIS_B = [0.407, 0.815, 0.407]


def lse(values):
    top = max(values)
    return top + math.log(sum(math.exp(v - top) for v in values))


def channel(x, h):
    return [sum(h[l] * x[m - l] for l in range(len(h)) if 0 <= m - l < len(x)) for m in range(len(x) + len(h) - 1)]


def wilson(k, n, z=3.29):
    p = k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return mid - half, mid + half


def test_encoder_impulse_response_is_seven_and_five():
    assert encode([1]) == [1, 1, 1, 0, 1, 1]
    assert encode([1, 0, 1, 1]) == [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1]


def test_interleaver_round_trip():
    perm = list(range(10))
    random.Random(2).shuffle(perm)
    v = [float(i) for i in range(10)]
    assert deinterleave(interleave(v, perm), perm) == v


def test_equalizer_matches_brute_force_posteriors():
    rng = random.Random(1)
    t, s2 = 8, 0.6
    y = [rng.gauss(0, 1) for _ in range(t + 2)]
    la = [rng.uniform(-2, 2) for _ in range(t)]
    le = bcjr_equalizer(y, PROAKIS_B, s2, la)
    num = [[] for _ in range(t)]
    den = [[] for _ in range(t)]
    for xs in itertools.product((1, -1), repeat=t):
        c = channel(xs, PROAKIS_B)
        w = -sum((a - b) ** 2 for a, b in zip(y, c)) / (2 * s2) + sum(x * l / 2 for x, l in zip(xs, la))
        for i in range(t):
            (num if xs[i] == 1 else den)[i].append(w)
    for i in range(t):
        assert abs(le[i] - (lse(num[i]) - lse(den[i]) - la[i])) < 1e-9


def test_equalizer_without_isi_is_the_awgn_llr():
    y = [0.3, -1.2, 0.05]
    le = bcjr_equalizer(y, [0.8], 0.5, [1.0, -2.0, 0.0])
    for v, l in zip(y, le):
        assert abs(l - 2 * 0.8 * v / 0.5) < 1e-12


def test_decoder_matches_brute_force_posteriors():
    rng = random.Random(3)
    k = 6
    lc = [rng.uniform(-3, 3) for _ in range(2 * (k + 2))]
    lu, le = bcjr_decoder(lc)
    ub = [[[], []] for _ in range(k)]
    cb = [[[], []] for _ in range(len(lc))]
    for u in itertools.product((0, 1), repeat=k):
        c = encode(list(u))
        w = sum((1 - 2 * b) * l / 2 for b, l in zip(c, lc))
        for i in range(k):
            ub[i][u[i]].append(w)
        for j in range(len(c)):
            cb[j][c[j]].append(w)
    for i in range(k):
        assert abs(lu[i] - (lse(ub[i][0]) - lse(ub[i][1]))) < 1e-9
    for j in range(len(lc)):
        assert abs(le[j] - (lse(cb[j][0]) - lse(cb[j][1]) - lc[j])) < 1e-9


def test_second_iteration_lowers_the_bit_error_rate():
    rng = random.Random(11)
    k, ebn0_db = 3000, 3.5
    s2 = 1 / 10 ** (ebn0_db / 10)
    u = [rng.randint(0, 1) for _ in range(k)]
    c = encode(u)
    perm = list(range(len(c)))
    rng.shuffle(perm)
    x = [1 - 2 * b for b in interleave(c, perm)]
    y = [v + rng.gauss(0, math.sqrt(s2)) for v in channel(x, PROAKIS_B)]
    first, second = turbo_equalize(y, PROAKIS_B, s2, perm, 2)
    e1 = sum((l < 0) != b for l, b in zip(first, u))
    e2 = sum((l < 0) != b for l, b in zip(second, u))
    assert e1 >= 100
    assert wilson(e2, k)[1] < wilson(e1, k)[0]


def test_bad_input():
    with pytest.raises(ValueError):
        encode([2])
    with pytest.raises(ValueError):
        bcjr_equalizer([0.0, 0.0], [1.0, 0.5], 0.5, [0.0, 0.0])
    with pytest.raises(ValueError):
        bcjr_equalizer([0.0], [1.0], 0.0, [0.0])
    with pytest.raises(ValueError):
        bcjr_decoder([0.0] * 5)
    with pytest.raises(ValueError):
        turbo_equalize([0.0] * 5, [1.0], 0.5, [0, 0, 1, 2, 3], 1)
