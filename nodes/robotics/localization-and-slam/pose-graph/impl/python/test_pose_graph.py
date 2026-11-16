# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pose-graph/. The authors are listed in prov/4A941D.jsonl.

import math
import random

import pytest

from pose_graph import PoseGraph, compose, exp_se2, inverse, log_se2, wrap

# A square of side 2 m driven counterclockwise: four poses, then back to the start.
TRUE = [(0.0, 0.0, 0.0), (2.0, 0.0, math.pi / 2), (2.0, 2.0, -math.pi), (0.0, 2.0, -math.pi / 2)]
OM = [[100.0, 0.0, 0.0], [0.0, 100.0, 0.0], [0.0, 0.0, 400.0]]  # 0.1 m and 0.05 rad


def between(a, b):
    return compose(inverse(a), b)


def square(noise=0.0, seed=1, reverse_loop=False):
    rng = random.Random(seed)
    g = PoseGraph()
    for i in range(4):
        g.add_vertex(i)
    pairs = [(0, 1), (1, 2), (2, 3), (0, 3) if reverse_loop else (3, 0)]
    for i, j in pairs:
        z = between(TRUE[i], TRUE[j])
        z = (z[0] + rng.gauss(0, noise), z[1] + rng.gauss(0, noise), wrap(z[2] + rng.gauss(0, noise)))
        g.add_edge(i, j, z, OM)
    return g


def dense_solve(a, b):
    """Gaussian elimination with partial pivoting (reference solver of the test)."""
    n = len(a)
    m = [list(a[r]) + [b[r]] for r in range(n)]
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


def test_exp_log_round_trip():
    rng = random.Random(3)
    for _ in range(200):
        v = (rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(-3.1, 3.1))
        w = log_se2(exp_se2(v))
        assert all(abs(p - q) < 1e-12 for p, q in zip(v, w))
    for t in (0.0, 1e-9, 1e-7, -1e-7):
        w = log_se2(exp_se2((1.0, -2.0, t)))
        assert abs(w[0] - 1.0) < 1e-12 and abs(w[1] + 2.0) < 1e-12


def test_consistent_graph_has_zero_residual():
    for rev in (False, True):
        g = square(reverse_loop=rev)
        for i in range(4):
            g.X[i] = TRUE[i]
        assert g.cost() < 1e-24
        assert sorted(g.neighbors(0)) == [1, 3]


def test_spanning_tree_initialization_recovers_true_poses():
    for rev in (False, True):
        g = square(reverse_loop=rev)
        assert g.initialize(0) == {0, 1, 2, 3}
        for i in range(4):
            assert all(abs(wrap(p - q)) < 1e-12 for p, q in zip(g.X[i], TRUE[i]))
        assert g.cost() < 1e-20


def test_initialization_leaves_other_components_alone():
    g = square()
    g.add_vertex(9, (5.0, 5.0, 1.0))
    assert 9 not in g.initialize(0)
    assert g.X[9] == (5.0, 5.0, 1.0)


def test_noisy_loop_closure_error():
    g = square(noise=0.05, seed=7)
    g.initialize(0)
    # BFS from 0 reaches 1 and 3 by edges 0 and 3, then 2 by edge 1.
    # Edge 2 (from 2 to 3) is the only edge outside the tree.
    for k in (0, 1, 3):
        assert all(abs(c) < 1e-12 for c in g.residual(k))
    assert g.edge_cost(2) > 0.0
    assert abs(g.cost() - g.edge_cost(2)) < 1e-12


def test_block_pattern_matches_edges():
    g = square()
    g.add_vertex(4)
    g.add_edge(3, 4, (1.0, 0.0, 0.0), OM)
    g.initialize(0)
    hb, _ = g.assemble()
    off = {(u, v) for (u, v) in hb if u != v}
    want = set()
    for i, j, _, _ in g.E:
        want |= {(i, j), (j, i)}
    assert off == want
    assert {(u, u) for u in range(5)} <= set(hb)


def test_gradient_matches_numerical_gradient_of_cost():
    g = square(noise=0.1, seed=2)
    g.initialize(0)
    g.X[2] = compose(g.X[2], (0.1, -0.2, 0.15))
    _, grad = g.assemble()
    base = dict(g.X)
    for u in range(4):
        for c in range(3):
            d = [0.0, 0.0, 0.0]
            d[c] = 1e-5
            g.X[u] = compose(base[u], exp_se2(d))
            fp = g.cost()
            d[c] = -1e-5
            g.X[u] = compose(base[u], exp_se2(d))
            fm = g.cost()
            g.X[u] = base[u]
            assert abs((fp - fm) / 2e-5 - 2.0 * grad[u][c]) < 1e-5


def gauss_newton_with_dense_solve(g, anchor, iters):
    ids = [i for i in sorted(g.X) if i != anchor]
    pos = {v: 3 * n for n, v in enumerate(ids)}
    for _ in range(iters):
        hb, grad = g.assemble()
        n = 3 * len(ids)
        a = [[0.0] * n for _ in range(n)]
        b = [0.0] * n
        for (u, v), blk in hb.items():
            if u in pos and v in pos:
                for r in range(3):
                    for c in range(3):
                        a[pos[u] + r][pos[v] + c] = blk[r][c]
        for u, gv in grad.items():
            if u in pos:
                for r in range(3):
                    b[pos[u] + r] = -gv[r]
        dx = dense_solve(a, b)
        for u in ids:
            g.X[u] = compose(g.X[u], exp_se2(dx[pos[u]:pos[u] + 3]))
    return g


def test_assembled_system_drives_gradient_to_zero():
    g = square(noise=0.05, seed=7)
    g.add_vertex(4)
    g.add_edge(1, 4, (1.0, 0.5, 0.2), OM)
    g.add_edge(2, 4, between(TRUE[2], compose(TRUE[1], (1.05, 0.45, 0.25))), OM)
    g.initialize(0)
    c0 = g.cost()
    gauss_newton_with_dense_solve(g, 0, 8)
    _, grad = g.assemble()
    assert g.cost() < c0
    assert max(abs(x) for u, gv in grad.items() if u != 0 for x in gv) < 1e-7


def test_errors():
    g = PoseGraph()
    g.add_vertex(0)
    with pytest.raises(ValueError):
        g.add_vertex(0)
    with pytest.raises(ValueError):
        g.add_edge(0, 1, (0, 0, 0), OM)
