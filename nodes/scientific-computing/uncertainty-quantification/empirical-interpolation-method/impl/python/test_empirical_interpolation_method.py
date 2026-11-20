# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-interpolation-method/. The authors are listed in prov/003ET5.jsonl.
import random

import pytest

from empirical_interpolation_method import EIM, eim_offline, sup_norm

XS = [i / 200 for i in range(201)]
TRAIN = [0.05 + 0.019 * i for i in range(51)]


def g_inv(x, mu):
    return 1.0 / (x + mu)


def dense_solve(a, b):
    """Reference: Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [list(row) + [bi] for row, bi in zip(a, b)]
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(m[i][k]))
        m[k], m[p] = m[p], m[k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            for j in range(k, n + 1):
                m[i][j] -= f * m[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def table_function(vectors):
    """g(x, mu) for a table: mu is an index into the list of grid vectors, x a grid index."""
    return lambda x, mu: vectors[mu][x]


def test_hand_example():
    xs = [0.0, 0.5, 1.0]
    eim, errs = eim_offline(lambda x, mu: 1.0 + mu * x * x, xs, [1.0, 3.0], 1e-12, 5)
    assert eim.mus == [3.0, 1.0]
    assert [xs[p] for p in eim.pts] == [1.0, 0.0]
    assert eim.q[0] == pytest.approx([0.25, 0.4375, 1.0])
    assert eim.q[1] == pytest.approx([1.0, 0.75, 0.0])
    assert eim.b == [[1.0, 0.0], [0.25, 1.0]]
    assert errs[:2] == [4.0, 0.5] and errs[2] < 1e-15
    # the function is affine in mu, so two terms reproduce every mu
    assert eim.coefficients([3.0, 1.0]) == pytest.approx([3.0, 0.25])
    assert eim.interpolate([1.0, 1.5, 3.0]) == pytest.approx([1.0, 1.5, 3.0])


def test_structure_on_random_tables():
    rng = random.Random(1)
    for _ in range(20):
        npts, nf = rng.randint(6, 12), rng.randint(3, 6)
        vecs = [[rng.gauss(0, 1) for _ in range(npts)] for _ in range(nf)]
        eim, errs = eim_offline(table_function(vecs), list(range(npts)), list(range(nf)), 1e-9, nf)
        m = len(eim.q)
        assert len(set(eim.pts)) == m and len(set(eim.mus)) == m
        for i in range(m):
            assert eim.b[i][i] == 1.0
            for j in range(m):
                if j <= i:
                    assert eim.b[i][j] == eim.q[j][eim.pts[i]]
                else:
                    # q_j vanishes at the earlier points up to rounding; B stores an exact 0
                    assert eim.b[i][j] == 0.0 and abs(eim.q[j][eim.pts[i]]) < 1e-12
        assert all(sup_norm(q) <= 1.0 + 1e-12 for q in eim.q)
        # interpolation against a dense reference solve, and the interpolation property
        for v in vecs:
            ref = dense_solve(eim.b, [v[p] for p in eim.pts])
            assert eim.coefficients([v[p] for p in eim.pts]) == pytest.approx(ref, rel=1e-9, abs=1e-9)
            iv = eim.interpolate(v)
            assert [iv[p] for p in eim.pts] == pytest.approx([v[p] for p in eim.pts], abs=1e-9)


def test_termination_and_exactness_on_a_finite_set():
    rng = random.Random(2)
    for _ in range(10):
        npts, nf = 10, rng.randint(2, 5)
        vecs = [[rng.gauss(0, 1) for _ in range(npts)] for _ in range(nf)]
        eim, errs = eim_offline(table_function(vecs), list(range(npts)), list(range(nf)), 1e-9, 100)
        assert len(eim.q) <= nf and errs[-1] <= 1e-9


def test_lebesgue_constant_bound_and_inequality():
    rng = random.Random(3)
    eim, errs = eim_offline(g_inv, XS, TRAIN, 1e-8, 40)
    for m in range(1, len(eim.q) + 1):
        sub = EIM()
        sub.pts, sub.q, sub.b = eim.pts[:m], eim.q[:m], [row[:m] for row in eim.b[:m]]
        lam = sub.lebesgue_constant()
        assert 1.0 - 1e-12 <= lam <= 2 ** m - 1 + 1e-9
        # ||g - I g|| <= (1 + Lambda) ||g - v|| for every v in the span: try perturbed interpolants
        for mu in rng.sample(TRAIN, 5):
            gv = [g_inv(x, mu) for x in XS]
            err = sup_norm([a - b for a, b in zip(gv, sub.interpolate(gv))])
            c = sub.coefficients([gv[p] for p in sub.pts])
            for _ in range(5):
                a = [cj + rng.gauss(0, 1e-3 * (1 + abs(cj))) for cj in c]
                v = [sum(aj * qj[k] for aj, qj in zip(a, sub.q)) for k in range(len(XS))]
                assert err <= (1 + lam) * sup_norm([s - t for s, t in zip(gv, v)]) * (1 + 1e-9) + 1e-12


def test_example_run():
    eim, errs = eim_offline(g_inv, XS, TRAIN, 1e-8, 40)
    assert len(eim.q) == 11
    assert eim.mus[:3] == pytest.approx([0.05, 0.126, 0.544])
    assert [XS[p] for p in eim.pts[:3]] == pytest.approx([0.0, 0.08, 0.505])
    assert errs[0] == pytest.approx(20.0) and errs[1] == pytest.approx(1.802, rel=1e-3)
    assert errs[-1] <= 1e-8 < errs[-2]
    assert eim.lebesgue_constant() == pytest.approx(3.528, rel=1e-3)


def test_online_stage_uses_only_the_magic_points():
    eim, errs = eim_offline(g_inv, XS, TRAIN, 1e-8, 40)
    gv = [g_inv(x, 0.3) for x in XS]
    other = [t if k in eim.pts else 1e6 for k, t in enumerate(gv)]
    assert eim.interpolate(other) == eim.interpolate(gv)
