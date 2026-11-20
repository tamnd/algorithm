# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filter-bank-multicarrier/. The authors are listed in prov/E8S9AK.jsonl.

import cmath
import math
import random

from filter_bank_multicarrier import (
    PHYDYAS_K4,
    analyze,
    half_sine,
    oqam_destagger,
    oqam_stagger,
    phydyas,
    pulse,
    signal_length,
    synthesize,
)

QAM16 = [complex(a, b) / math.sqrt(10) for a in (-3, -1, 1, 3) for b in (-3, -1, 1, 3)]


def gram(g, M, slots):
    length = signal_length(slots, g, M)
    P = {(k, m): pulse(k, m, g, M, length) for m in range(slots) for k in range(M)}
    out = {}
    keys = list(P)
    for i, u in enumerate(keys):
        for v in keys[i:]:
            out[(u, v)] = sum(x * y.conjugate() for x, y in zip(P[u], P[v]))
    return out


def test_prototypes():
    for g in (half_sine(8), phydyas(8)):
        assert abs(sum(v * v for v in g) - 1) < 1e-12
        assert max(abs(g[n] - g[len(g) - 1 - n]) for n in range(len(g))) < 1e-12
    assert abs(PHYDYAS_K4[1] ** 2 + PHYDYAS_K4[3] ** 2 - 1) < 1e-7
    assert len(phydyas(8)) == 31


def test_half_sine_is_exactly_real_orthogonal():
    G = gram(half_sine(8), 8, 6)
    for (u, v), ip in G.items():
        want = 1.0 if u == v else 0.0
        assert abs(ip.real - want) < 1e-12
    # the imaginary parts do not vanish: the pulses are not complex orthogonal
    assert max(abs(ip.imag) for ip in G.values()) > 0.4


def test_phydyas_is_nearly_real_orthogonal():
    G = gram(phydyas(8), 8, 10)
    err = max(abs(ip.real - (1.0 if u == v else 0.0)) for (u, v), ip in G.items())
    assert err < 3e-4
    assert max(abs(ip.imag) for ip in G.values()) > 0.5


def test_round_trip_half_sine():
    rng = random.Random(1)
    M, S = 8, 5
    c = [[rng.choice(QAM16) for _ in range(M)] for _ in range(S)]
    a = oqam_stagger(c)
    s = synthesize(a, half_sine(M), M)
    ah = analyze(s, 2 * S, half_sine(M), M)
    ch = oqam_destagger(ah)
    assert max(abs(x - y) for r1, r2 in zip(c, ch) for x, y in zip(r1, r2)) < 1e-9


def test_round_trip_phydyas_is_close():
    rng = random.Random(2)
    M, S = 8, 4
    g = phydyas(M)
    c = [[rng.choice(QAM16) for _ in range(M)] for _ in range(S)]
    ch = oqam_destagger(analyze(synthesize(oqam_stagger(c), g, M), 2 * S, g, M))
    err = max(abs(x - y) for r1, r2 in zip(c, ch) for x, y in zip(r1, r2))
    assert err < 5e-3


def out_of_band(g, M, edge, points=512):
    tot = out = 0.0
    for i in range(points):
        f = (i - points / 2) / points
        p = abs(sum(v * cmath.exp(-2j * math.pi * f * n) for n, v in enumerate(g))) ** 2
        tot += p
        if abs(f) * M > edge:
            out += p
    return out / tot


def test_spectral_containment():
    M = 16
    rect = [1 / math.sqrt(M)] * M
    assert out_of_band(rect, M, 2) > 1e-2
    assert out_of_band(phydyas(M), M, 2) < 1e-6
