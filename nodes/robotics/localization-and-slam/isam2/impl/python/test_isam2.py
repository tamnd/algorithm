# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isam2/. The authors are listed in prov/32NTDV.jsonl.

import math
import random

from isam2 import ISAM2, Between, Prior, linearize, whitened_error, wrap

OD = [0.05, 0.05, 0.02]
LC = [0.05, 0.05, 0.02]
STEPS = 12


def compose(p, u):
    c, s = math.cos(p[2]), math.sin(p[2])
    return [p[0] + c * u[0] - s * u[1], p[1] + s * u[0] + c * u[1], wrap(p[2] + u[2])]


def between(a, b):
    c, s = math.cos(a[2]), math.sin(a[2])
    dx, dy = b[0] - a[0], b[1] - a[1]
    return [c * dx + s * dy, -s * dx + c * dy, wrap(b[2] - a[2])]


def stream(seed, laps=2, noise=True):
    """Yield (new factors, new values) per pose: two laps of a 12-sided polygon."""
    rng = random.Random(seed)
    u = [1.0, 0.0, 2.0 * math.pi / STEPS]
    truth = [[0.0, 0.0, 0.0]]
    for _ in range(laps * STEPS):
        truth.append(compose(truth[-1], u))
    guess = {0: [0.0, 0.0, 0.0]}
    out = [([Prior(0, [0.0, 0.0, 0.0], [1e-3, 1e-3, 1e-3])], {0: [0.0, 0.0, 0.0]})]
    for t in range(1, laps * STEPS + 1):
        z = between(truth[t - 1], truth[t])
        if noise:
            z = [z[0] + rng.gauss(0, OD[0]), z[1] + rng.gauss(0, OD[1]), wrap(z[2] + rng.gauss(0, OD[2]))]
        fs = [Between(t - 1, t, z, OD)]
        guess[t] = compose(guess[t - 1], z)
        if t >= STEPS:
            w = between(truth[t - STEPS], truth[t])
            if noise:
                w = [w[0] + rng.gauss(0, LC[0]), w[1] + rng.gauss(0, LC[1]), wrap(w[2] + rng.gauss(0, LC[2]))]
            fs.append(Between(t - STEPS, t, w, LC))
        out.append((fs, {t: list(guess[t])}))
    return out, truth


def dense_system(factors, theta, keys):
    pos = {k: 3 * i for i, k in enumerate(keys)}
    n = 3 * len(keys)
    lam = [[0.0] * n for _ in range(n)]
    eta = [0.0] * n
    for f in factors:
        g = linearize(f, theta)
        for (u, w), blk in g.lam.items():
            for r in range(3):
                for c in range(3):
                    lam[pos[u] + r][pos[w] + c] += blk[r][c]
        for u, vec in g.eta.items():
            for r in range(3):
                eta[pos[u] + r] += vec[r]
    return lam, eta


def dense_solve(a, b):
    n = len(a)
    m = [list(a[r]) + [b[r]] for r in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            if f:
                for k in range(c, n + 1):
                    m[r][k] -= f * m[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


def batch_gauss_newton(factors, theta, iters=20):
    keys = sorted(theta)
    theta = {k: list(v) for k, v in theta.items()}
    for _ in range(iters):
        lam, eta = dense_system(factors, theta, keys)
        dx = dense_solve(lam, eta)
        for i, k in enumerate(keys):
            x = [a + b for a, b in zip(theta[k], dx[3 * i:3 * i + 3])]
            x[2] = wrap(x[2])
            theta[k] = x
        if max(abs(v) for v in dx) < 1e-12:
            break
    return theta


def check_tree(isam):
    cliques = isam.cliques()
    frontal_count = {}
    for c in cliques:
        for v in c.frontals:
            frontal_count[v] = frontal_count.get(v, 0) + 1
        if c.parent is None:
            assert c.sep == [] and c in isam.roots
        else:
            assert c in c.parent.children
            # running intersection: the separator lies in the parent clique
            assert set(c.sep) <= set(c.parent.frontals) | set(c.parent.sep)
        for i, v in enumerate(c.frontals):
            assert set(c.conds[v].parents) <= set(c.frontals[i + 1:]) | set(c.sep)
    assert frontal_count == {v: 1 for v in isam.theta}


def tree_quadratic(isam, keys):
    """Return (Lambda, eta) = sum over the conditionals of [R S]^T [R S] and [R S]^T d."""
    pos = {k: 3 * i for i, k in enumerate(keys)}
    n = 3 * len(keys)
    lam = [[0.0] * n for _ in range(n)]
    eta = [0.0] * n
    for c in isam.cliques():
        for v, cond in c.conds.items():
            blocks = [(v, cond.r)] + [(p, cond.s[p]) for p in cond.parents]
            for u, bu in blocks:
                for w, bw in blocks:
                    for r in range(3):
                        for col in range(3):
                            lam[pos[u] + r][pos[w] + col] += sum(bu[k][r] * bw[k][col] for k in range(3))
                for r in range(3):
                    eta[pos[u] + r] += sum(bu[k][r] * cond.d[k] for k in range(3))
    return lam, eta


def test_without_relinearization_delta_equals_the_dense_solve_after_every_update():
    data, _ = stream(1)
    isam = ISAM2(beta=float("inf"), alpha=0.0)
    for t, (fs, vals) in enumerate(data):
        isam.update(fs, vals)
        if t % 4 == 0 or t == len(data) - 1:
            keys = sorted(isam.theta)
            lam, eta = dense_system(isam.factors, isam.theta, keys)
            ref = dense_solve(lam, eta)
            got = [x for k in keys for x in isam.delta[k]]
            assert max(abs(a - b) for a, b in zip(got, ref)) < 1e-9


def test_tree_invariants_and_square_root_information_hold_with_relinearization():
    data, _ = stream(2)
    isam = ISAM2(beta=0.05, alpha=0.0)
    for t, (fs, vals) in enumerate(data):
        isam.update(fs, vals)
        check_tree(isam)
        if t % 6 == 0 or t == len(data) - 1:
            keys = sorted(isam.theta)
            lam, eta = dense_system(isam.factors, isam.theta, keys)
            tl, te = tree_quadratic(isam, keys)
            assert max(abs(a - b) for r1, r2 in zip(lam, tl) for a, b in zip(r1, r2)) < 1e-6
            assert max(abs(a - b) for a, b in zip(eta, te)) < 1e-6


def test_tiny_threshold_and_empty_updates_reach_the_batch_optimum():
    data, _ = stream(3)
    isam = ISAM2(beta=1e-12, alpha=0.0)
    init = {}
    for fs, vals in data:
        isam.update(fs, vals)
        init.update(vals)
    for _ in range(6):
        isam.update()
    est = isam.estimate()
    ref = batch_gauss_newton(isam.factors, init)
    assert max(abs(wrap(a - b)) for k in ref for a, b in zip(est[k], ref[k])) < 1e-8


def test_default_threshold_is_close_to_batch_and_eliminates_few_cliques():
    data, truth = stream(4)
    isam = ISAM2(beta=0.1, alpha=0.0)
    init, elim, total = {}, 0, 0
    for fs, vals in data:
        isam.update(fs, vals)
        init.update(vals)
        elim += isam.last_stats["eliminated_cliques"]
        total += isam.last_stats["total_cliques"]
    est = isam.estimate()
    ref = batch_gauss_newton(isam.factors, init)
    assert max(abs(wrap(a - b)) for k in ref for a, b in zip(est[k], ref[k])) < 0.05
    cost_isam = sum(whitened_error(f, est) for f in isam.factors)
    cost_ref = sum(whitened_error(f, ref) for f in isam.factors)
    assert cost_ref <= cost_isam < 1.5 * cost_ref
    assert elim < total


def test_wildfire_threshold_skips_cliques_and_stays_close():
    data, _ = stream(5)
    exact = ISAM2(beta=float("inf"), alpha=0.0)
    lazy = ISAM2(beta=float("inf"), alpha=1e-3)
    for fs, vals in data:
        exact.update(fs, vals)
        lazy.update(fs, vals)
    assert max(abs(a - b) for k in exact.delta for a, b in zip(exact.delta[k], lazy.delta[k])) < 0.05
    assert lazy.last_stats["solved_cliques"] <= exact.last_stats["solved_cliques"]


def test_noise_free_stream_has_zero_error():
    data, truth = stream(6, noise=False)
    isam = ISAM2(beta=0.1, alpha=0.0)
    for fs, vals in data:
        isam.update(fs, vals)
    est = isam.estimate()
    for t, x in enumerate(truth):
        assert max(abs(wrap(a - b)) for a, b in zip(est[t], x)) < 1e-9
    assert sum(whitened_error(f, est) for f in isam.factors) < 1e-16
