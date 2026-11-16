# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/square-root-sam/. The authors are listed in prov/ZY48RG.jsonl.

import math
import random

import pytest

from square_root_sam import (
    RHS,
    back_substitute,
    bearing_range,
    block_minimum_degree,
    cholesky_factor,
    columns,
    dense,
    givens_qr,
    linearize,
    nnz,
    odometry,
    prior,
    square_root_sam,
    total_error,
    wrap,
)

LANDMARKS = [(2.0, 0.5), (3.5, 2.5), (1.5, 4.0), (-0.5, 2.5), (0.5, -1.0), (2.5, 3.5)]
OD_S = [0.02, 0.02, 0.01]
BR_S = [0.05, 0.02]


def step(p, u):
    c, s = math.cos(p[2]), math.sin(p[2])
    return [p[0] + c * u[0] - s * u[1], p[1] + s * u[0] + c * u[1], wrap(p[2] + u[2])]


def build(seed, steps=12, noise=True, max_range=3.0):
    """Return (factors, true values, initial guess by dead reckoning)."""
    rng = random.Random(seed)
    u = [1.0, 0.0, 2.0 * math.pi / steps]
    truth = {("x", 0): [0.0, 0.0, 0.0]}
    for t in range(1, steps + 1):
        truth[("x", t)] = step(truth[("x", t - 1)], u)
    for j, m in enumerate(LANDMARKS):
        truth[("l", j)] = list(m)
    fs = [prior(("x", 0), [0.0, 0.0, 0.0], [1e-3, 1e-3, 1e-3])]
    guess = {("x", 0): [0.0, 0.0, 0.0]}
    for t in range(1, steps + 1):
        z = [v + (rng.gauss(0, s) if noise else 0.0) for v, s in zip(u, OD_S)]
        fs.append(odometry(("x", t - 1), ("x", t), z, OD_S))
        guess[("x", t)] = step(guess[("x", t - 1)], z)
    seen = set()
    for t in range(steps + 1):
        x = truth[("x", t)]
        for j, m in enumerate(LANDMARKS):
            dx, dy = m[0] - x[0], m[1] - x[1]
            r = math.hypot(dx, dy)
            if r > max_range:
                continue
            z = [r, wrap(math.atan2(dy, dx) - x[2])]
            if noise:
                z = [z[0] + rng.gauss(0, BR_S[0]), wrap(z[1] + rng.gauss(0, BR_S[1]))]
            fs.append(bearing_range(("x", t), ("l", j), z, BR_S))
            if j not in seen:
                g = guess[("x", t)]
                guess[("l", j)] = [g[0] + z[0] * math.cos(g[2] + z[1]), g[1] + z[0] * math.sin(g[2] + z[1])]
                seen.add(j)
    return fs, truth, guess


def dense_lstsq(rows, n):
    """Solve the normal equations A^T A x = A^T b by Gaussian elimination."""
    a, b = dense(rows, n)
    m = [[sum(r[i] * r[j] for r in a) for j in range(n)] + [sum(r[i] * bb for r, bb in zip(a, b))] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for k in range(c, n + 1):
                m[r][k] -= f * m[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


def test_noise_free_problem_converges_to_the_truth_with_zero_residual():
    fs, truth, guess = build(1, noise=False)
    theta, _, it = square_root_sam(fs, guess)
    assert it <= 3
    assert total_error(fs, theta) < 1e-18
    for v, x in truth.items():
        assert max(abs(wrap(a - b)) if k == 2 else abs(a - b) for k, (a, b) in enumerate(zip(theta[v], x))) < 1e-9


def test_givens_r_matches_cholesky_r_and_gives_the_least_squares_step():
    fs, _, guess = build(2)
    order = block_minimum_degree(fs)
    _, n = columns(order)
    rows = linearize(fs, guess, order)
    r, count = givens_qr(rows, n)
    assert count > 0
    rc = cholesky_factor(rows, n)
    for i in range(n):
        sign = 1.0 if r[i][i] > 0 else -1.0
        for j in range(n):
            assert abs(sign * r[i].get(j, 0.0) - rc[i][j]) < 1e-8 * max(1.0, abs(rc[i][i]))
    delta = back_substitute(r, n)
    ref = dense_lstsq(rows, n)
    assert max(abs(a - b) for a, b in zip(delta, ref)) < 1e-8


def test_r_has_no_entry_below_the_diagonal():
    fs, _, guess = build(3)
    order = block_minimum_degree(fs)
    _, n = columns(order)
    r, _ = givens_qr(linearize(fs, guess, order), n)
    assert all(k >= c for c, row in r.items() for k in row if k != RHS)


def test_the_ordering_changes_the_fill_but_not_the_solution():
    fs, _, guess = build(4)
    md = block_minimum_degree(fs)
    natural = sorted(md, key=lambda v: (v[0] == "l", v[1]))  # x_0, ..., x_T, then l_0, ...
    landmarks_first = sorted(md, key=lambda v: (v[0] == "x", v[1]))  # l_0, ..., then x_0, ...
    sizes = {}
    sols = []
    for name, order in (("md", md), ("natural", natural), ("landmarks_first", landmarks_first)):
        _, n = columns(order)
        r, _ = givens_qr(linearize(fs, guess, order), n)
        sizes[name] = nnz(r)
        theta, _, _ = square_root_sam(fs, guess, order)
        sols.append(theta)
    # Minimum degree is a heuristic; on this problem it beats both simple orders.
    assert sizes["md"] < sizes["natural"] < sizes["landmarks_first"]
    for t in sols[1:]:
        for v in t:
            assert max(abs(a - b) for a, b in zip(t[v], sols[0][v])) < 1e-8


def test_noisy_solution_has_zero_gradient():
    fs, truth, guess = build(5)
    theta, _, it = square_root_sam(fs, guess)
    assert it < 20
    order = block_minimum_degree(fs)
    _, n = columns(order)
    a, b = dense(linearize(fs, theta, order), n)
    grad = [sum(row[c] * bb for row, bb in zip(a, b)) for c in range(n)]
    assert max(abs(g) for g in grad) < 1e-6
    assert total_error(fs, theta) < total_error(fs, guess)


def test_ordering_is_a_permutation_of_the_variables():
    fs, truth, _ = build(6)
    order = block_minimum_degree(fs)
    assert sorted(order) == sorted(truth)


def test_missing_prior_is_rank_deficient():
    fs, _, guess = build(7)
    fs = fs[1:]
    order = block_minimum_degree(fs)
    _, n = columns(order)
    with pytest.raises(ValueError):
        givens_qr(linearize(fs, guess, order), n)
