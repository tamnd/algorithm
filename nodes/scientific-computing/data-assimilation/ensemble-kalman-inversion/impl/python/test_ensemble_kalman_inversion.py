# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-kalman-inversion/. The authors are listed in prov/421ZWN.jsonl.

import math
import random

import scimat
from ensemble_kalman_inversion import eki, eki_step, ensemble_moments


def exact_ensemble(m0, P0, N, rng):
    """N members whose sample mean is m0 and sample covariance is P0 exactly."""
    n = len(m0)
    rows = []
    for _ in range(n):
        v = [rng.gauss(0, 1) for _ in range(N)]
        for u in [[1.0 / math.sqrt(N)] * N] + rows:
            c = scimat.dot(u, v)
            v = [a - c * b for a, b in zip(v, u)]
        nv = scimat.norm2(v)
        rows.append([a / nv for a in v])
    L = scimat.cholesky(P0)
    Z = [[math.sqrt(N - 1) * a for a in row] for row in rows]
    return [[m0[j] + sum(L[j][k] * Z[k][i] for k in range(n)) for j in range(n)] for i in range(N)]


def posterior(m0, P0, A, y, Gamma):
    """Exact mean and covariance of u given y = A u + noise, noise ~ N(0, Gamma), u ~ N(m0, P0)."""
    PAt = scimat.matmul(P0, scimat.transpose(A))
    S = scimat.add(scimat.matmul(A, PAt), Gamma)
    K = scimat.transpose(scimat.solve(S, scimat.transpose(PAt)))
    m = scimat.add(m0, scimat.matvec(K, scimat.sub(y, scimat.matvec(A, m0))))
    return m, scimat.sub(P0, scimat.matmul(K, scimat.transpose(PAt)))


def close(ens, m, P, tol=1e-9):
    em, eP = ensemble_moments(ens)
    for a in range(len(m)):
        assert abs(em[a] - m[a]) < tol * (1 + abs(m[a]))
        for b in range(len(m)):
            assert abs(eP[a][b] - P[a][b]) < tol * (1 + abs(P[a][b]))


def linear_problem(seed, d=3, p=2):
    rng = random.Random(seed)
    A = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(p)]
    L = [[rng.uniform(-1, 1) for _ in range(p)] for _ in range(p)]
    Gamma = scimat.add(scimat.matmul(L, scimat.transpose(L)), scimat.scale(0.3, scimat.eye(p)))
    B = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(d)]
    P0 = scimat.add(scimat.matmul(B, scimat.transpose(B)), scimat.scale(0.2, scimat.eye(d)))
    m0 = [rng.gauss(0, 1) for _ in range(d)]
    y = [rng.gauss(0, 2) for _ in range(p)]
    return rng, A, Gamma, P0, m0, y


def test_scalar_check_value():
    s = 1 / math.sqrt(2.0)
    ident = lambda u: u
    sq = eki_step([[-s], [s]], ident, [1.0], [[1.0]], mode="sqrt")
    m, P = ensemble_moments(sq)
    assert abs(m[0] - 0.5) < 1e-12 and abs(P[0][0] - 0.5) < 1e-12
    no = eki_step([[-s], [s]], ident, [1.0], [[1.0]], mode="none")
    m, P = ensemble_moments(no)
    assert abs(m[0] - 0.5) < 1e-12 and abs(P[0][0] - 0.25) < 1e-12


def test_page_example():
    ident = lambda u: u
    hist = eki([[-1.0], [1.0]], ident, [1.0], [[1.0]], h=0.5, steps=2, mode="none")
    assert abs(hist[1][0][0]) < 1e-12 and abs(hist[1][1][0] - 1.0) < 1e-12
    assert abs(hist[2][0][0] - 0.2) < 1e-12 and abs(hist[2][1][0] - 1.0) < 1e-12
    m, P = ensemble_moments(hist[2])
    assert abs(m[0] - 0.6) < 1e-12 and abs(P[0][0] - 0.32) < 1e-12
    hist = eki([[-1.0], [1.0]], ident, [1.0], [[1.0]], h=0.5, steps=2, mode="sqrt")
    m, P = ensemble_moments(hist[2])
    assert abs(m[0] - 2 / 3) < 1e-12 and abs(P[0][0] - 2 / 3) < 1e-12


def test_subspace_property():
    rng = random.Random(4)
    d, N = 6, 4
    ens0 = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(N)]
    G = lambda u: [math.sin(u[0]) + u[1] * u[2], u[3] ** 2 - u[4], math.exp(0.2 * u[5])]
    for mode in ("perturbed", "none", "sqrt"):
        hist = eki(ens0, G, [0.3, -0.2, 1.1], scimat.scale(0.1, scimat.eye(3)), h=0.25, steps=4, mode=mode, rng=random.Random(5))
        basis = []
        for u in ens0:
            v = list(u)
            for b in basis:
                v = scimat.sub(v, scimat.scale(scimat.dot(v, b), b))
            basis.append(scimat.scale(1 / scimat.norm2(v), v))
        for u in hist[-1]:
            r = list(u)
            for b in basis:
                r = scimat.sub(r, scimat.scale(scimat.dot(r, b), b))
            assert scimat.norm2(r) < 1e-9 * (1 + scimat.norm2(u))


def test_sqrt_tempering_gives_the_exact_posterior():
    for seed in range(3):
        rng, A, Gamma, P0, m0, y = linear_problem(seed)
        ens0 = exact_ensemble(m0, P0, 6, rng)
        G = lambda u: scimat.matvec(A, u)
        m, P = posterior(m0, P0, A, y, Gamma)
        close(eki(ens0, G, y, Gamma, h=1.0, steps=1, mode="sqrt")[-1], m, P)
        close(eki(ens0, G, y, Gamma, h=0.25, steps=4, mode="sqrt")[-1], m, P)


def test_none_mode_covariance_is_the_kalman_one_minus_K_Gamma_K():
    rng, A, Gamma, P0, m0, y = linear_problem(11)
    h = 0.5
    ens = exact_ensemble(m0, P0, 7, rng)
    out = eki_step(ens, lambda u: scimat.matvec(A, u), y, Gamma, h=h, mode="none")
    Gh = scimat.scale(1 / h, Gamma)
    m, Pk = posterior(m0, P0, A, y, Gh)
    PAt = scimat.matmul(P0, scimat.transpose(A))
    K = scimat.transpose(scimat.solve(scimat.add(scimat.matmul(A, PAt), Gh), scimat.transpose(PAt)))
    P = scimat.sub(Pk, scimat.matmul(scimat.matmul(K, Gh), scimat.transpose(K)))
    close(out, m, P)


def test_perturbed_mode_with_many_members_is_near_the_posterior():
    rng = random.Random(12)
    N = 4000
    ens0 = [[rng.gauss(0, 1)] for _ in range(N)]
    hist = eki(ens0, lambda u: u, [1.0], [[1.0]], h=0.25, steps=4, mode="perturbed", rng=rng)
    m, P = ensemble_moments(hist[-1])
    assert abs(m[0] - 0.5) < 0.05 and abs(P[0][0] - 0.5) < 0.05


def test_nonlinear_misfit_decreases_without_derivatives():
    G = lambda u: [u[0] + u[1] ** 2 / 2, math.exp(0.3 * u[0]) - u[1]]
    y = G([0.7, -0.4])
    rng = random.Random(3)
    ens0 = [[rng.gauss(0, 1), rng.gauss(0, 1)] for _ in range(20)]
    hist = eki(ens0, G, y, scimat.scale(0.01, scimat.eye(2)), h=1.0, steps=40, mode="none")
    misfit = [scimat.norm2(scimat.sub(G(ensemble_moments(e)[0]), y)) for e in hist]
    spread = [sum(ensemble_moments(e)[1][a][a] for a in range(2)) for e in hist]
    assert misfit[0] > 1.0 and misfit[-1] < 0.01
    assert all(b < a for a, b in zip(spread, spread[1:]))
    m = ensemble_moments(hist[-1])[0]
    assert abs(m[0] - 0.7) < 0.02 and abs(m[1] + 0.4) < 0.02
