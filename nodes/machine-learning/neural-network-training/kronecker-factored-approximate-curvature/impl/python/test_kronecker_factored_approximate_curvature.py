# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kronecker-factored-approximate-curvature/. The authors are listed in prov/CAQ103.jsonl.

import math
import random
from fractions import Fraction as F

from kronecker_factored_approximate_curvature import (backward, damping_pi, factor_stats, fisher_quadratic, forward,
                                                      init_mlp, inverse, kfac, kfac_direction, kron, loss,
                                                      loss_grad, matmul, outer, solve, trace, transpose, unvec, vec)


def _rand_matrix(rng, n, m):
    return [[F(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(m)] for _ in range(n)]


def _spd(rng, n):
    b = _rand_matrix(rng, n, n)
    return [[x + (n if i == j else 0) for j, x in enumerate(r)] for i, r in enumerate(matmul(b, transpose(b)))]


def test_kronecker_inverse_identity_exact() -> None:
    rng = random.Random(1)
    a, g = _spd(rng, 2), _spd(rng, 3)
    assert inverse(kron(a, g)) == kron(inverse(a), inverse(g))


def test_vec_identity_exact() -> None:
    rng = random.Random(2)
    a, g, x = _rand_matrix(rng, 2, 2), _rand_matrix(rng, 3, 3), _rand_matrix(rng, 3, 2)
    k = kron(a, g)
    lhs = [sum(r[j] * v for j, v in enumerate(vec(x))) for r in k]
    assert lhs == vec(matmul(matmul(g, x), transpose(a)))


def test_single_example_fisher_block_is_a_kronecker_product() -> None:
    # vec(g abar^T) = abar kron g, so its outer product is (abar abar^T) kron (g g^T).
    rng = random.Random(3)
    abar = [F(rng.randint(-5, 5), 3) for _ in range(3)] + [F(1)]
    g = [F(rng.randint(-5, 5), 7) for _ in range(2)]
    v = vec(outer(g, abar))
    assert v == [a * b for a in abar for b in g]
    assert outer(v, v) == kron(outer(abar, abar), outer(g, g))


def test_expected_output_factor_is_diag_p_minus_p_p() -> None:
    # Sum over sampled targets y ~ p of (p - e_y)(p - e_y)^T.
    p = [F(1, 2), F(1, 3), F(1, 6)]
    total = [[F(0)] * 3 for _ in range(3)]
    for y, py in enumerate(p):
        d = [pk - (1 if k == y else 0) for k, pk in enumerate(p)]
        total = [[t + py * x for t, x in zip(tr, xr)] for tr, xr in zip(total, outer(d, d))]
    assert total == [[(p[i] if i == j else 0) - p[i] * p[j] for j in range(3)] for i in range(3)]


def test_backprop_matches_finite_differences() -> None:
    rng = random.Random(4)
    ws = init_mlp([3, 4, 3], rng)
    batch = [([rng.gauss(0, 1) for _ in range(3)], rng.randrange(3)) for _ in range(5)]
    grads = loss_grad(ws, batch, eta=0.01)
    h = 1e-6
    for l, i, j in ((0, 1, 2), (0, 3, 3), (1, 0, 4), (1, 2, 1)):
        ws[l][i][j] += h
        up = loss(ws, batch, 0.01)
        ws[l][i][j] -= 2 * h
        down = loss(ws, batch, 0.01)
        ws[l][i][j] += h
        assert math.isclose(grads[l][i][j], (up - down) / (2 * h), rel_tol=1e-5, abs_tol=1e-8)


def test_direction_equals_explicit_kronecker_solve() -> None:
    rng = random.Random(5)
    ws = init_mlp([3, 4, 2], rng)
    batch = [([rng.gauss(0, 1) for _ in range(3)], rng.randrange(2)) for _ in range(20)]
    A, G = factor_stats(ws, batch, rng)
    grads = loss_grad(ws, batch)
    gamma2 = 0.3
    delta = kfac_direction(grads, A, G, gamma2)
    for gw, a, g, d in zip(grads, A, G, delta):
        pi, c = damping_pi(a, g), math.sqrt(gamma2)
        ad = [[a[i][j] + (pi * c if i == j else 0) for j in range(len(a))] for i in range(len(a))]
        gd = [[g[i][j] + (c / pi if i == j else 0) for j in range(len(g))] for i in range(len(g))]
        x = solve(kron(ad, gd), [[v] for v in vec(gw)])
        expect = unvec([-r[0] for r in x], len(gw), len(gw[0]))
        for r1, r2 in zip(d, expect):
            assert all(math.isclose(p, q, rel_tol=1e-9, abs_tol=1e-12) for p, q in zip(r1, r2))


def test_pi_minimizes_the_trace_of_the_cross_terms() -> None:
    # tr(pi I kron G + (1/pi) A kron I) = pi dA tr G + dG tr A / pi.
    rng = random.Random(6)
    a = [[float(x) for x in r] for r in _spd(rng, 3)]
    g = [[float(x) for x in r] for r in _spd(rng, 2)]
    cost = lambda p: p * 3 * trace(g) + 2 * trace(a) / p
    best = cost(damping_pi(a, g))
    assert all(cost(damping_pi(a, g) * f) >= best for f in (0.5, 0.9, 0.99, 1.01, 1.1, 2.0))


def test_fisher_quadratic_matches_explicit_fisher() -> None:
    rng = random.Random(7)
    ws = init_mlp([2, 3, 2], rng)
    batch = [([rng.gauss(0, 1) for _ in range(2)], 0) for _ in range(4)]
    d = [[[rng.gauss(0, 1) for _ in row] for row in w] for w in ws]
    explicit = 0.0
    for x, _ in batch:
        abar, p = forward(ws, x)
        for y, py in enumerate(p):
            gw, _ = backward(ws, abar, [pk - (1.0 if k == y else 0.0) for k, pk in enumerate(p)])
            dot = sum(a * b for w1, w2 in zip(gw, d) for r1, r2 in zip(w1, w2) for a, b in zip(r1, r2))
            explicit += py * dot * dot / len(batch)
    assert math.isclose(fisher_quadratic(ws, batch, d), explicit, rel_tol=1e-9)


def test_kfac_trains_a_small_classifier() -> None:
    rng = random.Random(8)
    data = []
    for _ in range(80):
        x = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        data.append((x, int(x[0] * x[1] > 0)))
    ws = init_mlp([2, 6, 2], rng)
    start = loss(ws, data)
    ws, hist = kfac(ws, data, 60, rng, batch_size=40, lam=1.0)
    assert loss(ws, data) < 0.5 * start
