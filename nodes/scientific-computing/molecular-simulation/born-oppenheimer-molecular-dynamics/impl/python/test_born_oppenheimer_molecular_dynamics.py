# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/born-oppenheimer-molecular-dynamics/. The authors are listed in prov/KR4Y5Q.jsonl.
import math
import random

import pytest

from born_oppenheimer_molecular_dynamics import ToyModel, bomd, jacobi_eigen

X0 = [0.0, 1.1, 2.0, 3.2]
V0 = [0.3, -0.2, 0.1, -0.2]
MASSES = [1.0] * 4


def test_jacobi_on_two_by_two():
    vals, _ = jacobi_eigen([[2.0, 1.0], [1.0, 3.0]])
    assert vals == pytest.approx([(5 - math.sqrt(5)) / 2, (5 + math.sqrt(5)) / 2], abs=1e-14)


def test_jacobi_on_random_symmetric_matrix():
    rng = random.Random(1)
    n = 5
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            a[i][j] = a[j][i] = rng.uniform(-1, 1)
    vals, vecs = jacobi_eigen(a)
    assert vals == sorted(vals)
    for k in range(n):
        col = [vecs[i][k] for i in range(n)]
        av = [sum(a[i][j] * col[j] for j in range(n)) for i in range(n)]
        assert max(abs(p - vals[k] * q) for p, q in zip(av, col)) < 1e-12
        for l in range(n):
            dot = sum(vecs[i][k] * vecs[i][l] for i in range(n))
            assert dot == pytest.approx(1.0 if k == l else 0.0, abs=1e-12)


def test_dimer_without_repulsion_term_matches_closed_form():
    # E(r) = -2 t0 e^{-(r - 1)} + e^{-2 (r - 1)}: minimum E = -1 at r = 1, E'' = 2.
    model = ToyModel(u=0.0)
    for r in (0.8, 1.0, 1.3):
        assert model.scf([0.0, r])[1] == pytest.approx(-2 * math.exp(-(r - 1)) + math.exp(-2 * (r - 1)), abs=1e-12)
    e = [model.scf([0.0, r])[1] for r in (0.99, 1.0, 1.01)]
    assert e[1] == pytest.approx(-1.0, abs=1e-12)
    assert (e[0] - 2 * e[1] + e[2]) / 1e-4 == pytest.approx(2.0, abs=1e-3)


def test_scf_gives_lowest_eigenvector_of_its_own_matrix():
    model = ToyModel(u=1.0)
    c, _, res, _ = model.scf(X0)
    assert res < 1e-10
    h0 = model.hopping(X0)
    h = [[h0[i][j] + (c[i] ** 2 if i == j else 0.0) for j in range(4)] for i in range(4)]
    vals, vecs = jacobi_eigen(h)
    assert abs(sum(c[i] * vecs[i][0] for i in range(4))) == pytest.approx(1.0, abs=1e-9)


def test_hellmann_feynman_force_matches_finite_differences_only_at_scf():
    model = ToyModel(u=1.0)
    c, _, _, _ = model.scf(X0)
    f = model.forces(X0, c)
    for k in range(4):
        xp, xm = list(X0), list(X0)
        xp[k] += 1e-5
        xm[k] -= 1e-5
        fd = -(model.scf(xp)[1] - model.scf(xm)[1]) / 2e-5
        assert f[k] == pytest.approx(fd, abs=1e-7)
    # One SCF iteration from a flat density leaves an orbital that is not stationary.
    c1, _, res, _ = model.scf(X0, max_iter=1)
    assert res > 0.05
    assert max(abs(p - q) for p, q in zip(model.forces(X0, c1), f)) > 0.02
    assert sum(f) == pytest.approx(0.0, abs=1e-12)


def test_tight_scf_conserves_energy_with_second_order_fluctuations():
    model = ToyModel(u=1.0)
    e1 = bomd(model, list(X0), list(V0), MASSES, 0.05, 500)
    e2 = bomd(model, list(X0), list(V0), MASSES, 0.025, 1000)
    s1, s2 = max(e1) - min(e1), max(e2) - min(e2)
    assert s1 < 1e-3
    assert math.log2(s1 / s2) == pytest.approx(2.0, abs=0.4)


def test_loose_scf_drifts():
    model = ToyModel(u=1.0)
    tight = bomd(model, list(X0), list(V0), MASSES, 0.05, 1000)
    loose = bomd(model, list(X0), list(V0), MASSES, 0.05, 1000, max_iter=1)
    assert abs(loose[-1] - loose[0]) > 100 * abs(tight[-1] - tight[0])
    assert abs(loose[-1] - loose[0]) > 0.01
