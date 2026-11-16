# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-consensus-protocol/. The authors are listed in prov/GHGHQ7.jsonl.

import math
import random
from fractions import Fraction

from laplacian_consensus_protocol import (
    continuous_consensus,
    discrete_consensus,
    laplacian,
    max_degree,
    switching_consensus,
)

PATH3 = [(0, 1), (1, 2)]


def random_connected(rng: random.Random, r: int, extra: int) -> list:
    edges = [(i, rng.randrange(i), rng.choice([1, 2, 3])) for i in range(1, r)]
    for _ in range(extra):
        i, j = rng.sample(range(r), 2)
        edges.append((i, j, rng.choice([1, 2, 3])))
    return edges


def solve_left_kernel(lap: list) -> list:
    """Brute force: solve w^T L = 0 with sum(w) = 1 by exact Gaussian elimination."""
    r = len(lap)
    rows = [[Fraction(lap[i][j]) for i in range(r)] + [Fraction(0)] for j in range(r)]
    rows[-1] = [Fraction(1)] * r + [Fraction(1)]
    for c in range(r):
        p = next(k for k in range(c, r) if rows[k][c] != 0)
        rows[c], rows[p] = rows[p], rows[c]
        for k in range(r):
            if k != c and rows[k][c] != 0:
                f = rows[k][c] / rows[c][c]
                rows[k] = [a - f * b for a, b in zip(rows[k], rows[c])]
    return [rows[i][r] / rows[i][i] for i in range(r)]


def test_laplacian_path3() -> None:
    assert laplacian(3, PATH3) == [[1, -1, 0], [-1, 2, -1], [0, -1, 1]]
    # trace 4 = 0 + 1 + 3, and the sum of the 2x2 principal minors 3 = 0*1 + 0*3 + 1*3
    lap = laplacian(3, PATH3)
    assert sum(lap[i][i] for i in range(3)) == 4
    minors = sum(lap[i][i] * lap[j][j] - lap[i][j] * lap[j][i] for i in range(3) for j in range(i + 1, 3))
    assert minors == 3


def test_path3_discrete_exact() -> None:
    eps = Fraction(1, 4)
    for k in range(6):
        x = discrete_consensus(3, PATH3, [0, 3, 6], eps, k)
        d = 3 * Fraction(3, 4) ** k
        assert x == [3 - d, 3, 3 + d]


def test_path3_continuous_closed_form() -> None:
    for t in (0.5, 1.0, 3.0):
        x = continuous_consensus(3, PATH3, [0, 3, 6], t, 0.01)
        want = [3 - 3 * math.exp(-t), 3, 3 + 3 * math.exp(-t)]
        assert max(abs(a - b) for a, b in zip(x, want)) < 1e-9


def test_sum_is_invariant_on_undirected_graphs() -> None:
    rng = random.Random(1)
    for _ in range(40):
        r = rng.randrange(2, 8)
        edges = random_connected(rng, r, rng.randrange(4))
        eps = Fraction(1, 2 * max_degree(r, edges))
        x0 = [Fraction(rng.randrange(-20, 21)) for _ in range(r)]
        for k in (1, 2, 5):
            assert sum(discrete_consensus(r, edges, x0, eps, k)) == sum(x0)


def test_converges_to_average() -> None:
    rng = random.Random(2)
    for _ in range(40):
        r = rng.randrange(2, 9)
        edges = random_connected(rng, r, rng.randrange(5))
        eps = 0.9 / max_degree(r, edges)
        x0 = [rng.uniform(-10, 10) for _ in range(r)]
        avg = sum(x0) / r
        x = discrete_consensus(r, edges, x0, eps, 4000)
        assert max(abs(v - avg) for v in x) < 1e-6


def test_rate_on_path_graphs() -> None:
    # Path with r nodes: eigenvalues 2 - 2 cos(k pi / r). With eps = 1/4 the error
    # contracts by rho = max |1 - eps lambda| over the nonzero eigenvalues.
    rng = random.Random(3)
    for r in (3, 5, 8):
        edges = [(i, i + 1) for i in range(r - 1)]
        lams = [2 - 2 * math.cos(k * math.pi / r) for k in range(1, r)]
        rho = max(abs(1 - 0.25 * lam) for lam in lams)
        x0 = [rng.uniform(-5, 5) for _ in range(r)]
        avg = sum(x0) / r
        e0 = math.sqrt(sum((v - avg) ** 2 for v in x0))
        for k in (5, 20, 60):
            x = discrete_consensus(r, edges, x0, 0.25, k)
            ek = math.sqrt(sum((v - avg) ** 2 for v in x))
            assert ek <= rho ** k * e0 * (1 + 1e-9) + 1e-12


def test_disconnected_graph_gives_component_averages() -> None:
    edges = [(0, 1), (2, 3), (3, 4)]
    x = discrete_consensus(5, edges, [0.0, 4.0, 1.0, 2.0, 6.0], 0.3, 3000)
    want = [2.0, 2.0, 3.0, 3.0, 3.0]
    assert max(abs(a - b) for a, b in zip(x, want)) < 1e-9


def test_directed_limit_is_left_eigenvector_average() -> None:
    rng = random.Random(4)
    for _ in range(25):
        r = rng.randrange(3, 7)
        # a directed cycle makes the graph strongly connected; add random chords
        edges = [(i, (i + 1) % r, rng.choice([1, 2])) for i in range(r)]
        for _ in range(rng.randrange(4)):
            i, j = rng.sample(range(r), 2)
            edges.append((i, j, rng.choice([1, 2, 3])))
        lap = laplacian(r, edges, directed=True)
        w = solve_left_kernel(lap)
        assert all(v > 0 for v in w)
        x0 = [rng.uniform(-5, 5) for _ in range(r)]
        want = sum(float(wi) * xi for wi, xi in zip(w, x0))
        eps = 0.9 / max_degree(r, edges, directed=True)
        x = discrete_consensus(r, edges, x0, eps, 5000, directed=True)
        assert max(abs(v - want) for v in x) < 1e-6


def test_directed_leader_follower_chain() -> None:
    # agent 0 hears nobody, 1 hears 0, 2 hears 1: a rooted spanning tree.
    edges = [(1, 0), (2, 1)]
    x = discrete_consensus(3, edges, [5.0, -1.0, 2.0], 0.5, 200, directed=True)
    assert max(abs(v - 5.0) for v in x) < 1e-9


def test_balanced_directed_graph_gives_average() -> None:
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    x0 = [1.0, 7.0, -2.0, 6.0]
    x = discrete_consensus(4, edges, x0, 0.5, 400, directed=True)
    assert max(abs(v - 3.0) for v in x) < 1e-9


def test_switching_union_connected() -> None:
    # Each graph alone is disconnected, but their union is the path 0-1-2-3.
    sets = [[(0, 1), (2, 3)], [(1, 2)]]
    x0 = [Fraction(8), Fraction(0), Fraction(4), Fraction(0)]
    assert switching_consensus(4, sets, x0, Fraction(1, 2), 1) == [4, 4, 2, 2]
    x = switching_consensus(4, sets, x0, Fraction(1, 2), 2)
    assert x == [4, 3, 3, 2]
    assert sum(x) == sum(x0)
    xf = switching_consensus(4, sets, [8.0, 0.0, 4.0, 0.0], 0.4, 400)
    assert max(abs(v - 3.0) for v in xf) < 1e-9


def test_large_step_diverges() -> None:
    # eps above 2 / lambda_max breaks the protocol: lambda_max = 3 on the path P3.
    # The start (0, 6, 0) has its error (-2, 4, -2) along the eigenvector of 3.
    x = discrete_consensus(3, PATH3, [0.0, 6.0, 0.0], 0.9, 30)
    assert abs(x[0] - 2.0) > 1.0
