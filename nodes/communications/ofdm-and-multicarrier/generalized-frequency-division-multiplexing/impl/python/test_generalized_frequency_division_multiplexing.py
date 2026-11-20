# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-frequency-division-multiplexing/. The authors are listed in prov/36P3DR.jsonl.

import cmath
import math
import random

import cbb
from generalized_frequency_division_multiplexing import (
    channel,
    equalize,
    matched_filter,
    mmse,
    modulation_matrix,
    rc_prototype,
    transmit,
    zero_forcing,
)

QAM16 = [complex(a, b) / math.sqrt(10) for a in (-3, -1, 1, 3) for b in (-3, -1, 1, 3)]


def test_prototype():
    g = rc_prototype(4, 3, 0.5)
    assert abs(cbb.norm2(g) - 1) < 1e-12
    assert max(abs(v.imag) for v in g) < 1e-12
    assert max(abs(g[n] - g[(12 - n) % 12]) for n in range(12)) < 1e-12


def test_one_subsymbol_is_ofdm():
    k = 8
    A = modulation_matrix(rc_prototype(k, 1, 0.5), k, 1)
    for n in range(k):
        for c in range(k):
            assert abs(A[n][c] - cmath.exp(2j * math.pi * c * n / k) / math.sqrt(k)) < 1e-12


def test_even_m_is_singular_and_odd_m_is_not():
    for m in (2, 4):
        assert abs(cbb.det(modulation_matrix(rc_prototype(4, m, 0.5), 4, m))) < 1e-10
    for m in (3, 5):
        assert abs(cbb.det(modulation_matrix(rc_prototype(4, m, 0.5), 4, m))) > 0.1


def test_zero_forcing_round_trip_through_a_channel():
    rng = random.Random(1)
    for k, m in ((4, 3), (8, 5)):
        n, cp = k * m, 4
        A = modulation_matrix(rc_prototype(k, m, 0.5), k, m)
        d = [rng.choice(QAM16) for _ in range(n)]
        h = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(cp + 1)]
        s = transmit(A, d, cp)
        assert len(s) == n + cp
        x = equalize(channel(s, h), n, cp, h)
        dh = zero_forcing(A, x)
        assert max(abs(u - v) for u, v in zip(dh, d)) < 1e-9


def test_matched_filter_has_self_interference():
    rng = random.Random(2)
    k, m = 8, 5
    A = modulation_matrix(rc_prototype(k, m, 0.5), k, m)
    d = [rng.choice(QAM16) for _ in range(k * m)]
    x = transmit(A, d, 0)
    mf = matched_filter(A, x)
    assert max(abs(u - v) for u, v in zip(mf, d)) > 0.05
    # MMSE with a vanishing noise variance tends to zero forcing
    mm = mmse(A, x, 1e-12)
    assert max(abs(u - v) for u, v in zip(mm, d)) < 1e-6
