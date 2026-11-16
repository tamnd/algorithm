# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/view-graph/. The authors are listed in prov/P4TY5D.jsonl.

import itertools
import math
import random

from view_graph import ViewGraph, _mul, _tr, rotation_angle


def rot(axis, th):
    n = math.sqrt(sum(a * a for a in axis))
    x, y, z = (a / n for a in axis)
    c, s, d = math.cos(th), math.sin(th), 1 - math.cos(th)
    return [[c + x * x * d, x * y * d - z * s, x * z * d + y * s],
            [y * x * d + z * s, c + y * y * d, y * z * d - x * s],
            [z * x * d - y * s, z * y * d + x * s, c + z * z * d]]


def random_rot(rng):
    return rot([rng.gauss(0, 1) for _ in range(3)], rng.uniform(0, math.pi))


def true_graph(seed, n=7, p=0.6):
    """Cameras with X_c = R X + t and the exact relative poses on random pairs."""
    rng = random.Random(seed)
    rs = [random_rot(rng) for _ in range(n)]
    ts = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(n)]
    g = ViewGraph()
    for i in range(n):
        g.add_view(i)
    for i, j in itertools.combinations(range(n), 2):
        if j == i + 1 or rng.random() < p:
            rij = _mul(rs[j], _tr(rs[i]))
            tij = [ts[j][a] - sum(rij[a][b] * ts[i][b] for b in range(3)) for a in range(3)]
            g.add_edge(i, j, rij, tij, rng.randint(10, 500))
    return rs, ts, g


def close(a, b, tol=1e-9):
    return all(abs(x - y) < tol for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_reverse_edge_is_the_inverse_pose():
    rs, ts, g = true_graph(1)
    for i, j, _ in g.edges():
        r, t, _ = g.relative(i, j)
        rb, tb, _ = g.relative(j, i)
        assert close(_mul(rb, r), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        # X_i = R_ji (R_ij X_i + t_ij) + t_ji, so R_ji t_ij + t_ji = 0
        assert max(abs(sum(rb[a][b] * t[b] for b in range(3)) + tb[a]) for a in range(3)) < 1e-12
        # the stored translation maps camera i to camera j
        assert max(abs(ts[j][a] - sum(r[a][b] * ts[i][b] for b in range(3)) - t[a]) for a in range(3)) < 1e-12


def brute_force_max_tree_weight(nodes, edges):
    best = None
    for subset in itertools.combinations(edges, len(nodes) - 1):
        parent = {v: v for v in nodes}

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        ok = True
        for i, j, _ in subset:
            a, b = find(i), find(j)
            if a == b:
                ok = False
                break
            parent[a] = b
        if ok:
            w = sum(e[2] for e in subset)
            best = w if best is None else max(best, w)
    return best


def test_maximum_spanning_tree_matches_brute_force():
    for seed in range(5):
        _, _, g = true_graph(seed, n=6, p=0.5)
        tree = g.maximum_spanning_tree()
        assert len(tree) == 5
        wt = sum(g.relative(i, j)[2] for i, j in tree)
        assert wt == brute_force_max_tree_weight(list(range(6)), g.edges())


def test_chained_rotations_are_exact_up_to_the_gauge():
    rs, _, g = true_graph(2, n=8)
    tree = g.maximum_spanning_tree()
    est = g.chain_rotations(tree, 3)
    assert sorted(est) == list(range(8))
    for i in range(8):
        # est_i = R_i R_3^T for exact data
        assert close(est[i], _mul(rs[i], _tr(rs[3])))


def test_cycle_error_finds_a_bad_edge():
    rs, _, g = true_graph(3, n=5, p=1.0)
    assert g.cycle_error(0, 1, 2) < 1e-7
    r, t, w = g.relative(1, 2)
    g.add_edge(1, 2, _mul(rot([0, 0, 1], 0.3), r), t, w)
    assert abs(g.cycle_error(0, 1, 2) - 0.3) < 1e-9
    assert abs(g.cycle_error(2, 1, 0) - 0.3) < 1e-9
    assert g.cycle_error(0, 1, 3) < 1e-7


def test_components_after_edge_removal():
    g = ViewGraph()
    eye = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    for i, j in [(0, 1), (1, 2), (3, 4)]:
        g.add_edge(i, j, eye, [1.0, 0.0, 0.0], 5)
    g.add_view(5)
    assert g.components() == [[0, 1, 2], [3, 4], [5]]
    g.remove_edge(1, 2)
    assert g.components() == [[0, 1], [2], [3, 4], [5]]
    assert len(g.maximum_spanning_tree()) == 2
    assert rotation_angle(eye) == 0.0
