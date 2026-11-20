# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-related-multiple-elimination/. The authors are listed in prov/JC2TNG.jsonl.

import cmath
import math
import random

import imgkit as ik
import imgla as la
from surface_related_multiple_elimination import (
    add_surface_multiples,
    estimate_surface_scalar,
    srme,
    srme_direct,
    srme_iterative,
    srme_trace,
)


def one_reflector_spectrum(n, tau, r):
    """P = r z / (1 + r z), z = exp(-2 pi i k tau / n): one reflector under a free surface."""
    out = []
    for k in range(n):
        z = cmath.exp(-2j * math.pi * k * tau / n)
        out.append(r * z / (1 + r * z))
    return out


def max_diff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def random_matrix(rng, n, scale):
    return [[complex(rng.gauss(0.0, scale), rng.gauss(0.0, scale)) for _ in range(n)] for _ in range(n)]


def test_one_reflector_trace_has_the_expected_multiples():
    n, tau, r = 64, 8, 0.5
    tr = [v.real for v in ik.idft(one_reflector_spectrum(n, tau, r))]
    # The series r, -r^2, r^3, .. wraps around the period of 64 samples.
    wrap = 1.0 / (1.0 - r ** 8)
    for m in range(1, 8):
        assert abs(tr[m * tau] - (-1) ** (m + 1) * r ** m * wrap) < 1e-12
    assert max(abs(tr[i]) for i in range(n) if i % tau) < 1e-12


def test_direct_srme_leaves_only_the_primary():
    n, tau, r = 64, 8, 0.5
    tr = [v.real for v in ik.idft(one_reflector_spectrum(n, tau, r))]
    out = srme_trace(tr, a=-1.0)
    expect = [r if i == tau else 0.0 for i in range(n)]
    assert max(abs(p - q) for p, q in zip(out, expect)) < 1e-12


def test_first_prediction_is_the_autoconvolution():
    n, tau, r = 64, 8, 0.5
    spec = one_reflector_spectrum(n, tau, r)
    tr = [v.real for v in ik.idft(spec)]
    auto = ik.circ_conv(tr, tr)
    pred = [v.real for v in ik.idft([s * s for s in spec])]
    assert max(abs(p - q) for p, q in zip(auto, pred)) < 1e-12
    # The first-order multiple r^2 at 2 tau comes from the primary convolved with itself.
    assert abs(pred[2 * tau] - r * r) < 0.01


def test_iteration_converges_geometrically():
    n, tau, r = 32, 4, 0.4
    tr = [v.real for v in ik.idft(one_reflector_spectrum(n, tau, r))]
    expect = [r if i == tau else 0.0 for i in range(n)]
    errs = []
    for k in (5, 10, 20, 40):
        out = srme_trace(tr, a=-1.0, iters=k)
        errs.append(max(abs(p - q) for p, q in zip(out, expect)))
    assert errs[0] > errs[1] > errs[2] > errs[3]
    assert errs[3] < 1e-6
    # The worst frequency has |a P| = r / (1 - r) = 2/3.
    assert errs[3] / errs[2] < (2.0 / 3.0) ** 20 * 1.5


def test_matrix_relation_and_exact_recovery():
    rng = random.Random(1)
    n = 4
    data, surface, truth = [], [], []
    for _ in range(3):
        p0 = random_matrix(rng, n, 0.15)
        a = cmath.exp(1j * rng.uniform(0.0, 2.0 * math.pi)) * -1.0
        p = add_surface_multiples(p0, a)
        rel = [[x + a * y for x, y in zip(r0, rq)] for r0, rq in zip(p0, la.matmul(p0, p))]
        assert max_diff(rel, p) < 1e-12
        data.append(p)
        surface.append(a)
        truth.append(p0)
    out = srme(data, surface)
    for o, t in zip(out, truth):
        assert max_diff(o, t) < 1e-12
    out_it = srme(data, surface, iters=60)
    for o, t in zip(out_it, truth):
        assert max_diff(o, t) < 1e-9


def test_direct_and_iterative_agree():
    rng = random.Random(2)
    p = random_matrix(rng, 5, 0.1)
    a = -0.8 + 0.3j
    d = srme_direct(p, a)
    it = srme_iterative(p, a, 80)
    assert max_diff(d, it) < 1e-10


def test_adaptive_scalar_is_close_to_the_true_operator():
    # Minimum-energy subtraction is a heuristic: it lands near, not on, a = -1.
    n, tau, r = 64, 8, 0.5
    data = [[[v]] for v in one_reflector_spectrum(n, tau, r)]
    p0 = data
    s = 0j
    for _ in range(6):
        pred = [[[q[0][0] * p[0][0]]] for q, p in zip(p0, data)]
        s = estimate_surface_scalar(data, pred)
        p0 = [[[p[0][0] - s * m[0][0]]] for p, m in zip(data, pred)]
    assert abs(s + 1.0) < 0.1
    assert abs(s.imag) < 1e-12
