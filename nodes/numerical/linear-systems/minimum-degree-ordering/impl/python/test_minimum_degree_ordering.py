# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-degree-ordering/. The authors are listed in prov/3FDE64.jsonl.

import itertools
import random

from minimum_degree_ordering import (
    cholesky_pattern, fill_and_flops, fill_edges, graph_from_dense, graph_from_edges,
    ldlt_pattern_exact, minimum_degree, minimum_degree_quotient,
)


def random_graph(rng, n, p):
    return graph_from_edges(n, [(i, j) for i in range(n) for j in range(i) if rng.random() < p])


def grid(k):
    e = []
    for i in range(k):
        for j in range(k):
            v = i * k + j
            if j + 1 < k:
                e.append((v, v + 1))
            if i + 1 < k:
                e.append((v, v + k))
    return graph_from_edges(k * k, e)


def rcm(adj):
    """A plain reverse Cuthill-McKee from a minimum-degree vertex, for comparison."""
    n = len(adj)
    seen, order = [False] * n, []
    for s in sorted(range(n), key=lambda v: (len(adj[v]), v)):
        if seen[s]:
            continue
        seen[s] = True
        order.append(s)
        h = len(order) - 1
        while h < len(order):
            v = order[h]
            h += 1
            for w in sorted((w for w in adj[v] if not seen[w]), key=lambda w: (len(adj[w]), w)):
                seen[w] = True
                order.append(w)
    return order[::-1]


def test_edge_cases():
    assert minimum_degree([]) == []
    assert minimum_degree_quotient([]) == []
    assert minimum_degree([[]]) == [0]
    k5 = graph_from_edges(5, [(i, j) for i in range(5) for j in range(i)])
    assert fill_edges(k5, minimum_degree(k5)) == 0
    empty = [[] for _ in range(4)]
    assert minimum_degree(empty) == [0, 1, 2, 3]


def test_permutation_and_greedy_choice():
    rng = random.Random(11)
    for _ in range(150):
        n = rng.randint(1, 25)
        g = random_graph(rng, n, rng.uniform(0.05, 0.5))
        order = minimum_degree(g)
        assert sorted(order) == list(range(n))
        # replay: each chosen vertex has least degree in the current elimination graph
        cur = [set(nb) for nb in g]
        alive = set(range(n))
        for v in order:
            assert len(cur[v]) == min(len(cur[w]) for w in alive)
            assert v == min(w for w in alive if len(cur[w]) == len(cur[v]))
            nb = cur[v]
            for w in nb:
                cur[w].discard(v)
                cur[w] |= nb - {w}
            alive.discard(v)


def test_quotient_graph_matches_elimination_graph():
    rng = random.Random(12)
    for _ in range(150):
        n = rng.randint(1, 30)
        g = random_graph(rng, n, rng.uniform(0.05, 0.4))
        st = {}
        assert minimum_degree_quotient(g, "exact", st) == minimum_degree(g)
        # storage of the quotient graph never exceeds that of the original graph
        assert st["storage"] <= sum(len(nb) for nb in g)


def test_approximate_degree_is_an_upper_bound_and_exact_with_two_elements():
    rng = random.Random(13)
    exact_cases = 0
    for _ in range(150):
        n = rng.randint(2, 30)
        g = random_graph(rng, n, rng.uniform(0.05, 0.4))
        st = {}
        order = minimum_degree_quotient(g, "approximate", st)
        assert sorted(order) == list(range(n))
        assert st["storage"] <= sum(len(nb) for nb in g)
        for approx, exact, ne in st.get("checks", []):
            assert approx >= exact
            if ne <= 2:
                assert approx == exact
                exact_cases += 1
    assert exact_cases > 1000


def test_tree_has_no_fill():
    rng = random.Random(14)
    for _ in range(100):
        n = rng.randint(1, 60)
        g = graph_from_edges(n, [(i, rng.randrange(i)) for i in range(1, n)])
        assert fill_edges(g, minimum_degree(g)) == 0
        assert fill_edges(g, minimum_degree_quotient(g, "approximate")) == 0


def test_not_optimal_on_two_cliques():
    def clique(s):
        return [(a, b) for a in s for b in s if a < b]
    g = graph_from_edges(9, clique([0, 1, 2, 3]) + clique([5, 6, 7, 8]) + [(4, 0), (4, 5)])
    order = minimum_degree(g)
    assert order[0] == 4  # the unique vertex of degree 2
    assert fill_edges(g, order) == 1
    assert fill_edges(g, [1, 2, 3, 6, 7, 8, 0, 4, 5]) == 0  # a perfect elimination ordering


def test_against_brute_force_minimum_fill():
    rng = random.Random(15)
    worse = 0
    for _ in range(25):
        n = 6
        g = random_graph(rng, n, rng.uniform(0.3, 0.6))
        best = min(fill_edges(g, list(p)) for p in itertools.permutations(range(n)))
        md = fill_edges(g, minimum_degree(g))
        assert md >= best
        worse += md > best
    assert worse < 25  # usually optimal on tiny graphs, but not always


def test_symbolic_pattern_matches_exact_ldlt():
    rng = random.Random(16)
    equal = 0
    for _ in range(40):
        n = rng.randint(1, 12)
        g = random_graph(rng, n, rng.uniform(0.1, 0.5))
        a = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in g[i]:
                if j < i:
                    a[i][j] = a[j][i] = -rng.randint(1, 9)
        for i in range(n):
            a[i][i] = 1 + sum(abs(x) for x in a[i])  # strictly diagonally dominant, so SPD
        assert graph_from_dense(a) == g
        order = minimum_degree(g)
        sym = {(i, k) for k, col in enumerate(cholesky_pattern(g, order)) for i in col}
        num = ldlt_pattern_exact(a, order)
        assert num <= sym
        equal += num == sym
    assert equal >= 36  # cancellation is rare with random values


def test_grid_fill_against_natural_and_rcm():
    for k, ratio in ((8, 0.8), (16, 0.7), (24, 0.6)):
        g = grid(k)
        n = k * k
        nat = fill_and_flops(g, list(range(n)))
        r = fill_and_flops(g, rcm(g))
        md = fill_and_flops(g, minimum_degree(g))
        amd = fill_and_flops(g, minimum_degree_quotient(g, "approximate"))
        assert md[0] < r[0] <= nat[0]
        assert md[1] < ratio * r[1]
        assert abs(amd[0] - md[0]) <= 0.05 * md[0]


def test_three_by_three_grid_example():
    g = grid(3)
    order = minimum_degree(g)
    assert order == [0, 2, 6, 8, 1, 3, 4, 5, 7]
    assert fill_edges(g, order) == 5
    assert fill_edges(g, list(range(9))) == 8
    assert fill_and_flops(g, order) == (17, 39)
