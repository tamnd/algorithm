# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fredman-khachiyan-algorithm/. The authors are listed in prov/FEAKXY.jsonl.

import itertools
import random

from fredman_khachiyan_algorithm import dual_witness, is_dual, minimal_transversals


def evaluate(dnf, x):
    return any(set(t) <= x for t in dnf)


def brute_dual(f, g, variables):
    for r in range(len(variables) + 1):
        for x in itertools.combinations(variables, r):
            x = set(x)
            if evaluate(f, x) == evaluate(g, set(variables) - x):
                return False
    return True


def brute_transversals(edges, vertices):
    hits = []
    for r in range(len(vertices) + 1):
        for t in itertools.combinations(vertices, r):
            s = set(t)
            if all(s & set(e) for e in edges) and not any(set(h) <= s for h in hits):
                hits.append(t)
    return sorted(sorted(t) for t in hits)


def random_hypergraph(rng, n, m):
    return [rng.sample(range(n), rng.randint(1, n)) for _ in range(m)]


def check_witness(f, g, variables):
    x = dual_witness(f, g)
    if x is None:
        return True
    assert set(x) <= set(variables)
    assert evaluate(f, set(x)) == evaluate(g, set(variables) - set(x))
    return False


def test_transversals_against_brute_force() -> None:
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 8)
        edges = random_hypergraph(rng, n, rng.randint(1, 6))
        vertices = sorted({v for e in edges for v in e})
        assert minimal_transversals(edges) == brute_transversals(edges, vertices)


def test_duality_against_brute_force() -> None:
    rng = random.Random(23)
    for _ in range(400):
        n = rng.randint(1, 7)
        variables = list(range(n))
        f = random_hypergraph(rng, n, rng.randint(1, 5))
        tr = brute_transversals(f, sorted({v for e in f for v in e}))
        g = [list(t) for t in tr]
        if g and rng.random() < 0.5:
            g.pop(rng.randrange(len(g)))
        if rng.random() < 0.3:
            g.append(rng.sample(variables, rng.randint(1, n)))
        expected = brute_dual(f, g, variables)
        assert is_dual(f, g) == expected
        assert check_witness(f, g, variables) == expected


def test_random_pairs_witness() -> None:
    rng = random.Random(7)
    for _ in range(400):
        n = rng.randint(0, 6)
        variables = list(range(n))
        f = [rng.sample(variables, rng.randint(0, n)) for _ in range(rng.randint(0, 4))]
        g = [rng.sample(variables, rng.randint(0, n)) for _ in range(rng.randint(0, 4))]
        assert check_witness(f, g, variables) == brute_dual(f, g, variables)


def test_known_duals() -> None:
    # One term and its singletons.
    assert is_dual([[0, 1, 2, 3]], [[0], [1], [2], [3]])
    # A perfect matching and the choice of one end from each edge.
    matching = [[0, 1], [2, 3], [4, 5]]
    choices = [list(t) for t in itertools.product([0, 1], [2, 3], [4, 5])]
    assert is_dual(matching, choices)
    assert minimal_transversals(matching) == sorted(choices)
    # Threshold: the k-subsets of n and the (n - k + 1)-subsets are dual.
    for n in range(1, 7):
        for k in range(1, n + 1):
            f = list(itertools.combinations(range(n), k))
            g = list(itertools.combinations(range(n), n - k + 1))
            assert is_dual(f, g)
            assert is_dual(g, f)
    # Duality is symmetric, and a pair that misses one term is not dual.
    assert not is_dual(matching, choices[1:])


def test_edge_cases() -> None:
    # Constant 0 (no terms) and constant 1 (the empty term) are dual.
    assert is_dual([], [[]])
    assert is_dual([[]], [])
    assert not is_dual([], [])
    assert not is_dual([[]], [[]])
    # No edges: the empty set is the only minimal transversal.
    assert minimal_transversals([]) == [[]]
    # An empty edge cannot be hit.
    assert minimal_transversals([[]]) == []
    assert minimal_transversals([[3]]) == [[3]]
    # Repeated and non-minimal terms do not change the function.
    assert is_dual([[0], [0], [0, 1]], [[0]])
    assert minimal_transversals([[0, 1], [0, 1, 2], [0, 1]]) == [[0], [1]]


def test_larger_instance() -> None:
    rng = random.Random(3)
    edges = random_hypergraph(rng, 12, 9)
    vertices = sorted({v for e in edges for v in e})
    assert minimal_transversals(edges) == brute_transversals(edges, vertices)
