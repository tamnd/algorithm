# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/se-sync/. The authors are listed in prov/ZTRAGF.jsonl.

import math
import random

from se_sync import (
    angle,
    certificate,
    connection_laplacian,
    local_search,
    matmul,
    objective,
    relaxed_cost,
    riemannian_gradient_norm,
    rot,
    se_sync,
    set_block,
    symmetric_eigen,
    transpose,
)


def wrap(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def random_problem(seed, n, extra, sigma):
    """Random rotations, a spanning path plus extra edges, angle noise sigma (rad)."""
    rng = random.Random(seed)
    truth = [0.0] + [rng.uniform(-math.pi, math.pi) for _ in range(n - 1)]
    pairs = [(i, i + 1) for i in range(n - 1)]
    while len(pairs) < n - 1 + extra:
        i, j = sorted(rng.sample(range(n), 2))
        if (i, j) not in pairs:
            pairs.append((i, j))
    edges = [(i, j, rot(truth[j] - truth[i] + rng.gauss(0.0, sigma)), 1.0) for i, j in pairs]
    return truth, edges


def angles(rs):
    return [angle(r) for r in rs]


def test_cost_is_the_trace_form():
    _, edges = random_problem(1, 6, 5, 0.3)
    rng = random.Random(2)
    rs = [rot(rng.uniform(-3, 3)) for _ in range(6)]
    y = [[0.0] * 12 for _ in range(2)]
    for i, r in enumerate(rs):
        set_block(y, i, r)
    q = connection_laplacian(6, edges)
    assert abs(objective(edges, rs) - relaxed_cost(q, y)) < 1e-9


def test_noise_free_problem_is_solved_exactly_and_certified():
    truth, edges = random_problem(3, 8, 8, 0.0)
    out = se_sync(8, edges)
    assert out["upper"] < 1e-10 and abs(out["lower"]) < 1e-10
    for a, b in zip(angles(out["rotations"]), truth):
        assert abs(wrap(a - b)) < 1e-6


def test_low_noise_certifies_a_global_optimum():
    truth, edges = random_problem(4, 10, 10, 0.1)
    out = se_sync(10, edges)
    assert out["lam_min"] >= -1e-6 * 4
    # tight relaxation: the rounded solution attains the lower bound
    assert out["upper"] - out["lower"] < 1e-6 * max(1.0, out["upper"])
    assert max(abs(wrap(a - b)) for a, b in zip(angles(out["rotations"]), truth)) < 0.3


def test_certificate_vanishes_on_the_solution():
    _, edges = random_problem(5, 7, 6, 0.2)
    q = connection_laplacian(7, edges)
    y = [[0.0] * 14 for _ in range(2)]
    for i in range(7):
        set_block(y, i, rot(0.0))
    y, _ = local_search(q, y, 7)
    s = certificate(q, y, 7)
    # first order condition: Y S = 0, so S has the rows of Y in its null space
    ys = matmul(y, s)
    assert max(abs(x) for row in ys for x in row) < 1e-5
    assert riemannian_gradient_norm(q, y, 7) < 1e-4


def test_brute_force_on_three_rotations():
    for seed in range(3):
        truth, edges = random_problem(10 + seed, 3, 1, 0.8)
        edges = [(i, j, r, w) for (i, j, r, _), w in zip(edges, (1.0, 2.0, 0.5))]
        out = se_sync(3, edges)
        # grid over the two free angles, then a local refinement
        best = (float("inf"), 0.0, 0.0)
        steps = 72
        for a in range(steps):
            for b in range(steps):
                t1, t2 = 2 * math.pi * a / steps, 2 * math.pi * b / steps
                f = objective(edges, [rot(0.0), rot(t1), rot(t2)])
                if f < best[0]:
                    best = (f, t1, t2)
        f, t1, t2 = best
        h = 2 * math.pi / steps
        while h > 1e-9:
            moved = False
            for d1, d2 in ((h, 0), (-h, 0), (0, h), (0, -h)):
                g = objective(edges, [rot(0.0), rot(t1 + d1), rot(t2 + d2)])
                if g < f:
                    f, t1, t2, moved = g, t1 + d1, t2 + d2, True
            if not moved:
                h /= 2
        assert out["lower"] <= f + 1e-9
        assert abs(out["upper"] - f) < 1e-7


def twisted_cycle(n, k):
    """A noise-free cycle of n identity measurements, started at the winding k state."""
    edges = [(i, (i + 1) % n, rot(0.0), 1.0) for i in range(n)]
    start = [rot(2.0 * math.pi * k * i / n) for i in range(n)]
    return edges, start


def test_twisted_cycle_is_a_critical_point_that_the_certificate_rejects():
    n = 9
    edges, start = twisted_cycle(n, 1)
    q = connection_laplacian(n, edges)
    y = [[0.0] * (2 * n) for _ in range(2)]
    for i, r in enumerate(start):
        set_block(y, i, r)
    # every rotation is balanced between its two neighbors
    assert riemannian_gradient_norm(q, y, n) < 1e-9
    # the local search cannot leave it in rank 2
    y2, _ = local_search(q, [list(row) for row in y], n)
    assert abs(relaxed_cost(q, y2) - relaxed_cost(q, y)) < 1e-9
    vals, _ = symmetric_eigen(certificate(q, y, n))
    assert vals[0] < -0.1
    # the staircase escapes and finds the global optimum, cost 0
    out = se_sync(n, edges, start=start)
    assert out["rank"] >= 3
    assert out["upper"] < 1e-8
    assert out["history"][0][2] < -0.1


def test_eigen_solver_matches_a_known_matrix():
    rng = random.Random(7)
    a = [[rng.uniform(-1, 1) for _ in range(6)] for _ in range(6)]
    s = [[a[i][j] + a[j][i] for j in range(6)] for i in range(6)]
    vals, vecs = symmetric_eigen(s)
    for k, lam in enumerate(vals):
        v = [vecs[i][k] for i in range(6)]
        sv = [sum(s[i][j] * v[j] for j in range(6)) for i in range(6)]
        assert max(abs(x - lam * y) for x, y in zip(sv, v)) < 1e-10
    assert vals == sorted(vals)
    vt = transpose(vecs)
    eye = matmul(vt, vecs)
    assert max(abs(eye[i][j] - (1.0 if i == j else 0.0)) for i in range(6) for j in range(6)) < 1e-10
