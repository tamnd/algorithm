# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learned-primal-dual/. The authors are listed in prov/8N7P4C.jsonl.

import random

from learned_primal_dual import (
    cp_maps,
    gradient_maps,
    l1_prox,
    learned_primal_dual,
    least_squares_dual_prox,
    residual_network,
)


def matvec(a, x):
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def rmatvec(a, y):
    return [sum(a[i][j] * y[i] for i in range(len(a))) for j in range(len(a[0]))]


def blur(kernel):
    """Periodic convolution with a kernel centered at index 0, and its adjoint (the correlation)."""
    def apply(x):
        n = len(x)
        return [sum(kernel[k] * x[(i - k) % n] for k in range(len(kernel))) for i in range(n)]

    def adjoint(y):
        n = len(y)
        return [sum(kernel[k] * y[(i + k) % n] for k in range(len(kernel))) for i in range(n)]
    return apply, adjoint


def chambolle_pock(apply_a, apply_at, y, lam, tau, sigma, iters, n, m):
    """Chambolle-Pock for (1/2)||A x - y||^2 + lam ||x||_1, written out directly."""
    x, xbar, h = [0.0] * n, [0.0] * n, [0.0] * m
    for _ in range(iters):
        ax = apply_a(xbar)
        h = [(hi + sigma * axi - sigma * yi) / (1.0 + sigma) for hi, axi, yi in zip(h, ax, y)]
        ath = apply_at(h)
        v = [xi - tau * gi for xi, gi in zip(x, ath)]
        t = tau * lam
        new = [vi - t if vi > t else vi + t if vi < -t else 0.0 for vi in v]
        xbar = [2.0 * a - b for a, b in zip(new, x)]
        x = new
    return x


def lpd_with_cp_maps(apply_a, apply_at, y, lam, tau, sigma, iters, n, m):
    gamma, lam_map = cp_maps(l1_prox(tau * lam), least_squares_dual_prox(sigma), tau, sigma)
    return learned_primal_dual(y, apply_a, apply_at, [gamma] * iters, [lam_map] * iters,
                               [[0.0] * n, [0.0] * n], [[0.0] * m])


def test_adjoint_of_the_blur_operator():
    rng = random.Random(11)
    apply_a, apply_at = blur([0.5, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2])
    for _ in range(5):
        x = [rng.gauss(0.0, 1.0) for _ in range(16)]
        y = [rng.gauss(0.0, 1.0) for _ in range(16)]
        ax, aty = apply_a(x), apply_at(y)
        gap = abs(sum(a * b for a, b in zip(ax, y)) - sum(a * b for a, b in zip(x, aty)))
        norm = sum(a * a for a in ax) ** 0.5 * sum(b * b for b in y) ** 0.5
        assert gap <= 1e-10 * norm


def test_cp_maps_give_chambolle_pock_on_a_matrix():
    rng = random.Random(5)
    m, n = 5, 8
    a = [[rng.gauss(0.0, 0.4) for _ in range(n)] for _ in range(m)]
    y = [rng.gauss(0.0, 1.0) for _ in range(m)]
    def fa(x): return matvec(a, x)
    def fat(h): return rmatvec(a, h)
    for k in (1, 2, 3, 7, 20):
        u = lpd_with_cp_maps(fa, fat, y, 0.1, 0.5, 0.5, k, n, m)
        v = chambolle_pock(fa, fat, y, 0.1, 0.5, 0.5, k, n, m)
        assert max(abs(p - q) for p, q in zip(u, v)) <= 1e-12


def test_cp_maps_give_chambolle_pock_on_a_blur():
    rng = random.Random(6)
    apply_a, apply_at = blur([0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25])
    y = [rng.gauss(0.0, 1.0) for _ in range(12)]
    u = lpd_with_cp_maps(apply_a, apply_at, y, 0.05, 0.9, 0.9, 30, 12, 12)
    v = chambolle_pock(apply_a, apply_at, y, 0.05, 0.9, 0.9, 30, 12, 12)
    assert max(abs(p - q) for p, q in zip(u, v)) <= 1e-12


def test_scalar_example():
    def ident(x): return list(x)
    xs = [lpd_with_cp_maps(ident, ident, [1.0], 0.5, 0.5, 0.5, k, 1, 1)[0] for k in (1, 2, 3, 4)]
    assert abs(xs[0]) < 1e-15
    assert abs(xs[1] - 1 / 36) < 1e-15
    assert abs(xs[2] - 13 / 108) < 1e-15
    assert abs(xs[3] - 149 / 648) < 1e-15
    assert abs(lpd_with_cp_maps(ident, ident, [1.0], 0.5, 0.5, 0.5, 200, 1, 1)[0] - 0.5) < 1e-9


def test_cp_maps_reach_the_lasso_solution_of_the_lista_example():
    a = [[1.0, 0.0, 0.6], [0.0, 1.0, 0.8]]
    def fa(x): return matvec(a, x)
    def fat(h): return rmatvec(a, h)
    x = lpd_with_cp_maps(fa, fat, [0.6, 0.8], 0.1, 0.5, 0.5, 3000, 3, 2)
    assert max(abs(p - q) for p, q in zip(x, [0.0, 0.0, 0.9])) < 1e-8


def test_gradient_maps_give_landweber():
    gamma, lam = gradient_maps(0.01)
    def ident(x): return list(x)
    x = learned_primal_dual([1.0], ident, ident, [gamma] * 100, [lam] * 100, [[0.0]], [[0.0]])
    assert abs(x[0] - (1.0 - 0.99 ** 100)) < 1e-12
    assert abs(x[0] - 0.63397) < 5e-6


def test_given_networks_and_call_counts():
    rng = random.Random(21)
    n_p, n_d, m, n, iters = 3, 2, 6, 6, 4
    apply_a, apply_at = blur([0.6, 0.2, 0.0, 0.0, 0.0, 0.2])
    calls = {"a": 0, "at": 0}

    def counted_a(x):
        calls["a"] += 1
        return apply_a(x)

    def counted_at(h):
        calls["at"] += 1
        return apply_at(h)

    def split(v, parts, size):
        return [v[i * size:(i + 1) * size] for i in range(parts)]

    dual_maps, primal_maps = [], []
    for _ in range(iters):
        dnet = residual_network(rng, n_d * m + 2 * m, n_d * m, 8, 0.3)
        pnet = residual_network(rng, n_p * n + n, n_p * n, 8, 0.3)
        dual_maps.append(lambda h, ax, y, f=dnet: split(f([t for v in h for t in v] + ax + y), n_d, m))
        primal_maps.append(lambda x, ath, f=pnet: split(f([t for v in x for t in v] + ath), n_p, n))
    y = [rng.gauss(0.0, 1.0) for _ in range(m)]
    x0 = [[0.0] * n for _ in range(n_p)]
    h0 = [[0.0] * m for _ in range(n_d)]
    out1 = learned_primal_dual(y, counted_a, counted_at, dual_maps, primal_maps, x0, h0)
    assert calls == {"a": iters, "at": iters}
    out2 = learned_primal_dual(y, apply_a, apply_at, dual_maps, primal_maps, x0, h0)
    assert out1 == out2 and len(out1) == n
    assert any(abs(t) > 1e-6 for t in out1)
