# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chambolle-projection-algorithm/. The authors are listed in prov/R2YTGF.jsonl.

import itertools
import math
import random

from chambolle_projection_algorithm import (
    chambolle_projection,
    chambolle_step,
    div,
    dual_energy,
    dual_residual,
    energy,
    grad,
)


def brute_force_1d(f: list[float], lam: float) -> list[float]:
    """Exact 1D TV denoising: try every sign pattern of the differences.

    For a pattern s, runs with s = 0 merge into segments; on a segment S the
    value is mean(S) - lam (s_left - s_right) / |S|. The pattern of the true
    minimizer gives the true minimizer, so the best candidate is exact.
    """
    n = len(f)
    best, best_val = None, math.inf
    for s in itertools.product((-1, 0, 1), repeat=n - 1):
        segs, start = [], 0
        for b in range(n - 1):
            if s[b] != 0:
                segs.append((start, b + 1))
                start = b + 1
        segs.append((start, n))
        u = []
        for k, (a, b) in enumerate(segs):
            sl = s[a - 1] if a > 0 else 0
            sr = s[b - 1] if b < n else 0
            v = sum(f[a:b]) / (b - a) - lam * (sl - sr) / (b - a)
            u.extend([v] * (b - a))
        val = energy([u], [f], lam)
        if val < best_val:
            best, best_val = u, val
    return best


def test_adjoint() -> None:
    rng = random.Random(1)
    for n1, n2 in ((1, 5), (3, 4), (5, 2)):
        u = [[rng.uniform(-1, 1) for _ in range(n2)] for _ in range(n1)]
        p = ([[rng.uniform(-1, 1) for _ in range(n2)] for _ in range(n1)],
             [[rng.uniform(-1, 1) for _ in range(n2)] for _ in range(n1)])
        g1, g2 = grad(u)
        lhs = sum(g1[i][j] * p[0][i][j] + g2[i][j] * p[1][i][j] for i in range(n1) for j in range(n2))
        d = div(p)
        rhs = -sum(u[i][j] * d[i][j] for i in range(n1) for j in range(n2))
        assert abs(lhs - rhs) < 1e-12


def test_step_image() -> None:
    f = [[0.0, 0.0, 4.0, 4.0] for _ in range(4)]
    u, _ = chambolle_projection(f, 1.0, iters=3000, tol=1e-10)
    for row in u:
        for a, b in zip(row, (0.5, 0.5, 3.5, 3.5)):
            assert abs(a - b) < 1e-4


def test_brute_force_1d() -> None:
    rng = random.Random(7)
    for _ in range(8):
        n = rng.randint(2, 6)
        f = [float(rng.randint(-3, 3)) for _ in range(n)]
        lam = rng.choice((0.3, 0.7, 1.5))
        u, _ = chambolle_projection([f], lam, iters=20000, tol=1e-11)
        ref = brute_force_1d(f, lam)
        assert max(abs(a - b) for a, b in zip(u[0], ref)) < 1e-4


def test_monotone_and_feasible() -> None:
    rng = random.Random(3)
    f = [[rng.uniform(0, 5) for _ in range(5)] for _ in range(4)]
    lam = 0.8
    p = ([[0.0] * 5 for _ in range(4)], [[0.0] * 5 for _ in range(4)])
    r = dual_residual(f, lam, p)
    for _ in range(200):
        p = chambolle_step(f, lam, 0.125, p)
        r2 = dual_residual(f, lam, p)
        assert r2 <= r + 1e-12
        r = r2
        assert all(math.hypot(a, b) <= 1 + 1e-12 for r1, r2_ in zip(*p) for a, b in zip(r1, r2_))


def test_gap_certificate_and_mean() -> None:
    rng = random.Random(5)
    f = [[rng.uniform(0, 5) for _ in range(4)] for _ in range(4)]
    lam = 0.5
    u, p = chambolle_projection(f, lam, iters=5000, tol=1e-7)
    gap = energy(u, f, lam) - dual_energy(p, f, lam)
    assert -1e-9 <= gap <= 1e-7
    mean_f = sum(map(sum, f)) / 16
    mean_u = sum(map(sum, u)) / 16
    assert abs(mean_f - mean_u) < 1e-12
    # Small random moves do not lower the energy below the dual bound.
    for _ in range(20):
        v = [[a + rng.uniform(-0.01, 0.01) for a in row] for row in u]
        assert energy(v, f, lam) >= dual_energy(p, f, lam) - 1e-12


def test_large_lambda_gives_mean() -> None:
    f = [[1.0, 2.0], [3.0, 6.0]]
    u, _ = chambolle_projection(f, 100.0, iters=2000, tol=1e-12)
    for row in u:
        for a in row:
            assert abs(a - 3.0) < 1e-5
