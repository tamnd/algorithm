# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-empirical-interpolation-method/. The authors are listed in prov/RHRTRM.jsonl.
import itertools
import math
import random

import pytest

from discrete_empirical_interpolation_method import deim, deim_approx, gauss_solve, inv_norm2, jacobi_eigh, pod

N = 100
XS = [-1 + 2 * i / (N - 1) for i in range(N)]
MUS = [1 + (math.pi - 1) * i / 50 for i in range(51)]
TEST = [1 + (math.pi - 1) * (i + 0.5) / 20 for i in range(20)]


def s(x, mu):
    return (1 - x) * math.cos(3 * math.pi * mu * (x + 1)) * math.exp(-(1 + x) * mu)


def norm(v):
    return math.sqrt(sum(t * t for t in v))


def orthonormal(cols):
    out = []
    for c in cols:
        w = list(c)
        for _ in range(2):
            for q in out:
                d = sum(a * b for a, b in zip(q, w))
                w = [a - d * b for a, b in zip(w, q)]
        nw = norm(w)
        out.append([t / nw for t in w])
    return out


def proj_err(u, f):
    c = [sum(a * b for a, b in zip(uj, f)) for uj in u]
    return norm([f[i] - sum(cj * uj[i] for cj, uj in zip(c, u)) for i in range(len(f))])


def factor(u, p):
    return inv_norm2([[u[j][pi] for j in range(len(u))] for pi in p])


def test_hand_example():
    u = [[1.0, 3.0, 2.0], [2.0, 1.0, 4.0]]
    p = deim(u)
    assert p == [1, 2]
    assert deim_approx(u, p, [1.0, 1.0]) == pytest.approx([0.5, 1.0, 1.0])


def test_jacobi_against_the_definition():
    rng = random.Random(4)
    for n in (2, 3, 6):
        b = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
        a = [[b[i][j] + b[j][i] for j in range(n)] for i in range(n)]
        lam, v = jacobi_eigh(a)
        assert all(lam[i] >= lam[i + 1] for i in range(n - 1))
        assert sum(lam) == pytest.approx(sum(a[i][i] for i in range(n)))
        for k in range(n):
            col = [v[i][k] for i in range(n)]
            av = [sum(a[i][j] * col[j] for j in range(n)) for i in range(n)]
            assert av == pytest.approx([lam[k] * t for t in col], abs=1e-10)
            for k2 in range(n):
                col2 = [v[i][k2] for i in range(n)]
                assert sum(x * y for x, y in zip(col, col2)) == pytest.approx(1.0 if k == k2 else 0.0, abs=1e-12)
    # 2 by 2 closed form
    lam, _ = jacobi_eigh([[2.0, 1.0], [1.0, 2.0]])
    assert lam == pytest.approx([3.0, 1.0])


def test_pod_projection_error_is_the_tail_of_the_singular_values():
    rng = random.Random(5)
    snaps = [[rng.gauss(0, 1) for _ in range(12)] for _ in range(7)]
    for m in (1, 3, 5):
        u, sig = pod(snaps, m)
        assert sum(proj_err(u, f) ** 2 for f in snaps) == pytest.approx(sum(t * t for t in sig[m:]), rel=1e-8)


def test_structure_on_random_bases():
    rng = random.Random(6)
    for _ in range(30):
        n, m = rng.randint(6, 12), rng.randint(1, 5)
        u = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(m)]
        p = deim(u)
        assert len(set(p)) == m
        # P^T U is nonsingular, the approximation interpolates at p and reproduces the span
        f = [rng.gauss(0, 1) for _ in range(n)]
        fh = deim_approx(u, p, [f[i] for i in p])
        assert [fh[i] for i in p] == pytest.approx([f[i] for i in p], abs=1e-9)
        a = [rng.gauss(0, 1) for _ in range(m)]
        v = [sum(aj * uj[i] for aj, uj in zip(a, u)) for i in range(n)]
        assert deim_approx(u, p, [v[i] for i in p]) == pytest.approx(v, abs=1e-8)


def test_error_bound_and_factor_bounds_against_brute_force():
    rng = random.Random(7)
    for _ in range(20):
        n, m = rng.randint(5, 8), rng.randint(1, 4)
        u = orthonormal([[rng.gauss(0, 1) for _ in range(n)] for _ in range(m)])
        p = deim(u)
        fac = factor(u, p)
        for _ in range(5):
            f = [rng.gauss(0, 1) for _ in range(n)]
            fh = deim_approx(u, p, [f[i] for i in p])
            assert norm([a - b for a, b in zip(f, fh)]) <= fac * proj_err(u, f) * (1 + 1e-9) + 1e-12
        # the best index set by brute force is at least as good; DEIM is within the proved bounds
        best = min(_safe_factor(u, list(q)) for q in itertools.combinations(range(n), m))
        assert best <= fac * (1 + 1e-9)
        assert fac <= (1 + math.sqrt(2 * n)) ** (m - 1) / max(abs(t) for t in u[0]) * (1 + 1e-9)
        assert fac < math.sqrt(n * m / 3) * 2 ** m


def _safe_factor(u, q):
    """||(P^T U)^-1||_2 for the index set q, or infinity if P^T U is singular."""
    try:
        gauss_solve([[u[j][pi] for j in range(len(u))] for pi in q], [1.0] * len(q))
        return factor(u, q)
    except (ValueError, ZeroDivisionError):
        return math.inf


def test_example_run():
    snaps = [[s(x, mu) for x in XS] for mu in MUS]
    modes, sig = pod(snaps, 20)
    assert sig[0] == pytest.approx(24.8, rel=1e-2) and sig[10] == pytest.approx(0.476, rel=1e-2)
    p = deim(modes)
    assert p[:6] == [0, 12, 16, 21, 25, 38]
    for m, fac_ref in ((2, 2.79), (10, 7.11), (20, 5.66)):
        u, pm = modes[:m], p[:m]
        fac = factor(u, pm)
        assert fac == pytest.approx(fac_ref, rel=1e-2)
        for mu in TEST:
            f = [s(x, mu) for x in XS]
            fh = deim_approx(u, pm, [f[i] for i in pm])
            assert norm([a - b for a, b in zip(f, fh)]) <= fac * proj_err(u, f) * (1 + 1e-6) + 1e-12
