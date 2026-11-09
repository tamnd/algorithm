# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-sat-algorithm/. The authors are listed in prov/7XSPN7.jsonl.

import itertools
import random

from two_sat_algorithm import tarjan_components, two_sat_algorithm


def satisfies(clauses: list[list[int]], x: list[bool]) -> bool:
    return all(any(x[abs(l) - 1] == (l > 0) for l in c) for c in clauses)


def brute_force_sat(n: int, clauses: list[list[int]]) -> bool:
    return any(satisfies(clauses, list(bits)) for bits in itertools.product([False, True], repeat=n))


EXAMPLE = [[1, 2], [-1, 3], [-2, 3], [-3, 4], [-4, -1]]


def test_example() -> None:
    x = two_sat_algorithm(4, EXAMPLE)
    assert x == [False, True, True, True]
    assert satisfies(EXAMPLE, x)


def test_example_unsat() -> None:
    f = EXAMPLE + [[1, -2]]
    assert two_sat_algorithm(4, f) is None
    assert not brute_force_sat(4, f)


def test_edges() -> None:
    assert two_sat_algorithm(0, []) == []
    assert two_sat_algorithm(3, []) is not None
    assert two_sat_algorithm(1, [[]]) is None
    assert two_sat_algorithm(1, [[1]]) == [True]
    assert two_sat_algorithm(1, [[-1]]) == [False]
    assert two_sat_algorithm(1, [[1], [-1]]) is None
    assert two_sat_algorithm(1, [[1, -1]]) is not None  # a tautology
    assert two_sat_algorithm(2, [[1, 1], [-1, 2]]) == [True, True]
    # the four clauses over x1 and x2: unsatisfiable
    assert two_sat_algorithm(2, [[1, 2], [1, -2], [-1, 2], [-1, -2]]) is None


def test_components_reverse_topological() -> None:
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(1, 12)
        adj = [[rng.randrange(n) for _ in range(rng.randint(0, 3))] for _ in range(n)]
        comp = tarjan_components(adj)
        reach = [{v} for v in range(n)]
        for v in range(n):
            todo = [v]
            while todo:
                u = todo.pop()
                for w in adj[u]:
                    if w not in reach[v]:
                        reach[v].add(w)
                        todo.append(w)
        for u in range(n):
            for w in range(n):
                same = w in reach[u] and u in reach[w]
                assert (comp[u] == comp[w]) == same
            for w in adj[u]:
                assert comp[u] >= comp[w]


def test_random_against_brute_force() -> None:
    rng = random.Random(1979)
    sat = unsat = 0
    for _ in range(1500):
        n = rng.randint(1, 10)
        m = rng.randint(0, 3 * n)
        f = []
        for _ in range(m):
            width = 1 if rng.random() < 0.15 else 2
            f.append([rng.randint(1, n) * rng.choice([1, -1]) for _ in range(width)])
        x = two_sat_algorithm(n, f)
        expected = brute_force_sat(n, f)
        if x is None:
            assert not expected
            unsat += 1
        else:
            assert len(x) == n and satisfies(f, x)
            sat += 1
    assert sat > 300 and unsat > 300


def test_long_chain_no_recursion_limit() -> None:
    n = 5000
    f = [[-v, v + 1] for v in range(1, n)] + [[1]]
    x = two_sat_algorithm(n, f)
    assert x == [True] * n
    assert two_sat_algorithm(n, f + [[-n]]) is None
