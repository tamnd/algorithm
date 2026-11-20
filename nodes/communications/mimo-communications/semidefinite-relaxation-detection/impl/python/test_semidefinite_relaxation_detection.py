# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semidefinite-relaxation-detection/. The authors are listed in prov/QN7FSW.jsonl.

import math
import random

import pytest

import cbb
import constel
from semidefinite_relaxation_detection import (
    _real_model,
    dual_bound,
    homogeneous_matrix,
    jacobi_min_eig,
    mixing_method,
    sdr_detect,
)


def metric(y, h, pts, idx):
    return cbb.norm2(cbb.sub(y, cbb.matvec(h, [pts[i] for i in idx])))


def rand_case(rng, m, n, pts, n0):
    h = [[cbb.cn(rng, 1.0) for _ in range(n)] for _ in range(m)]
    idx = [rng.randrange(len(pts)) for _ in range(n)]
    y = cbb.awgn(rng, cbb.matvec(h, [pts[i] for i in idx]), n0)
    return y, h, idx


def objective(q, u):
    n = len(q)
    return sum(q[i][j] * sum(a * b for a, b in zip(u[i], u[j])) for i in range(n) for j in range(n))


def test_example():
    h = [[2, 1], [1, 1]]
    y = [0.5, 0.6]
    pts = constel.pam(2)
    g, yr, _ = _real_model(y, h, pts)
    q = homogeneous_matrix(g, yr)
    want = [[5, 3, -1.6], [3, 2, -1.1], [-1.6, -1.1, 0.61]]
    assert all(abs(q[i][j] - want[i][j]) < 1e-12 for i in range(3) for j in range(3))
    info = {}
    assert sdr_detect(y, h, pts, info=info) == [0, 1] == constel.ml_vector(y, h, pts)
    assert abs(info["metric"] - 0.61) < 1e-12
    # the relaxation is not tight here: its value is about 0.5972 < 0.61
    assert 0.5971 < info["lower"] <= info["relaxed"] + 1e-12 < 0.5973


def test_homogeneous_metric():
    rng = random.Random(1901)
    for pts, m, n in ((constel.qam(4), 3, 2), (constel.pam(2), 2, 3)):
        for _ in range(10):
            y, h, _ = rand_case(rng, m, n, pts, 0.5)
            g, yr, kind = _real_model(y, h, pts)
            q = homogeneous_matrix(g, yr)
            idx = [rng.randrange(len(pts)) for _ in range(n)]
            x = [pts[i] for i in idx]
            a = 1.0 if kind == "pam" else 1.0 / math.sqrt(2.0)
            b = [v.real / a for v in x] + ([v.imag / a for v in x] if kind == "qam" else [])
            for t in (1.0, -1.0):
                v = [t * c for c in b] + [t]
                val = sum(q[i][j] * v[i] * v[j] for i in range(len(v)) for j in range(len(v)))
                assert abs(val - metric(y, h, pts, idx)) < 1e-9


def test_jacobi_min_eig():
    assert abs(jacobi_min_eig([[2, 1], [1, 2]]) - 1.0) < 1e-12
    assert abs(jacobi_min_eig([[4, 1, 0], [1, 3, 1], [0, 1, 2]]) - (3 - math.sqrt(3))) < 1e-12
    rng = random.Random(1902)
    for n in (2, 4, 7):
        for _ in range(5):
            a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
            a = [[a[i][j] + a[j][i] for j in range(n)] for i in range(n)]
            e = jacobi_min_eig(a)
            # A - e I is positive semidefinite, and A - (e + 1e-6) I is not
            shifted = [[a[i][j] - (e - 1e-9 if i == j else 0.0) for j in range(n)] for i in range(n)]
            cbb.cholesky(shifted)
            with pytest.raises(ValueError):
                cbb.cholesky([[a[i][j] - (e + 1e-6 if i == j else 0.0) for j in range(n)] for i in range(n)])


def test_mixing_method_monotone():
    rng = random.Random(1903)
    y, h, _ = rand_case(rng, 3, 3, constel.qam(4), 0.5)
    g, yr, _ = _real_model(y, h, constel.qam(4))
    q = homogeneous_matrix(g, yr)
    prev = math.inf
    for k in range(1, 15):
        u, _ = mixing_method(q, 5, k, random.Random(7), tol=0.0)
        assert all(abs(sum(c * c for c in v) - 1.0) < 1e-12 for v in u)
        val = objective(q, u)
        assert val <= prev + 1e-12
        prev = val


def test_lower_bound_is_valid():
    rng = random.Random(1904)
    for pts, m, n in ((constel.qam(4), 2, 2), (constel.pam(2), 4, 4), (constel.qam(4), 3, 3)):
        for t in range(6):
            y, h, _ = rand_case(rng, m, n, pts, 1.0)
            info = {}
            got = sdr_detect(y, h, pts, seed=t, info=info)
            dml = metric(y, h, pts, constel.ml_vector(y, h, pts))
            assert info["lower"] <= dml + 1e-9 <= info["metric"] + 2e-9
            assert abs(info["metric"] - metric(y, h, pts, got)) < 1e-9
            # an arbitrary point of the sphere also gives a valid bound
            g, yr, _ = _real_model(y, h, pts)
            q = homogeneous_matrix(g, yr)
            u = [[rng.gauss(0, 1) for _ in range(3)] for _ in q]
            u = [[c / math.sqrt(sum(d * d for d in v)) for c in v] for v in u]
            assert dual_bound(q, u)[0] <= dml + 1e-9


def test_noiseless_exact():
    rng = random.Random(1906)
    for pts, m, n in ((constel.qam(4), 3, 3), (constel.pam(2), 3, 4)):
        for t in range(5):
            y, h, idx = rand_case(rng, m, n, pts, 0.0)
            info = {}
            assert sdr_detect(y, h, pts, seed=t, info=info) == idx
            assert abs(info["metric"]) < 1e-9 and info["lower"] < 1e-9 and info["lower"] > -1e-4


def test_bad_arguments():
    with pytest.raises(ValueError):
        sdr_detect([0j], [[1]], constel.qam(16))
    with pytest.raises(ValueError):
        sdr_detect([0j], [[1]], constel.psk(4))
    with pytest.raises(ValueError):
        sdr_detect([0j], [[1]], constel.pam(2), draws=-1)


def test_measured_agreement():
    """Measurement, seed 1905: 3x3 4-QAM, i.i.d. Rayleigh, 5 dB, 40 vectors."""
    rng = random.Random(1905)
    pts = constel.qam(4)
    n0 = cbb.undb(-5)
    sdr_ok = zf_ok = certified = 0
    for t in range(40):
        y, h, _ = rand_case(rng, 3, 3, pts, n0)
        ml = constel.ml_vector(y, h, pts)
        info = {}
        got = sdr_detect(y, h, pts, seed=t, info=info)
        sdr_ok += got == ml
        hh = cbb.herm(h)
        z = cbb.solve(cbb.matmul(hh, h), cbb.matvec(hh, y))
        zf_ok += [constel.ml_detect(v, pts) for v in z] == ml
        if info["metric"] - info["lower"] < 1e-6:
            certified += 1
            assert got == ml
    # measured on CPython 3: SDR 39 of 40, ZF 30 of 40, 21 certified
    assert sdr_ok >= 37 and zf_ok <= 33 and certified >= 15
