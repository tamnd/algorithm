# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kuhn-algorithm/. The authors are listed in prov/H8SH4G.jsonl.

import random

from kuhn_algorithm import kuhn_algorithm


def check_matching(n_left, n_right, adj, mate_left):
    """The result is a matching that uses only edges of the graph. Returns its size."""
    used = set()
    for u, v in enumerate(mate_left):
        if v is None:
            continue
        assert v in adj[u]
        assert v not in used
        used.add(v)
    return len(used)


def brute_nu(n_left, adj):
    """Oracle: the largest matching, by trying every choice for each left vertex."""
    best = 0

    def rec(u, used, size):
        nonlocal best
        if size + (n_left - u) <= best:
            return
        if u == n_left:
            best = size
            return
        for v in set(adj[u]):
            if v not in used:
                rec(u + 1, used | {v}, size + 1)
        rec(u + 1, used, size)

    rec(0, frozenset(), 0)
    return best


def test_example():
    # left 1, 2, 3, 4 are 0..3; right a, b, c, d are 0..3
    adj = [[0, 1], [0, 2], [0], [2, 3]]
    mate = kuhn_algorithm(4, 4, adj)
    assert mate == [1, 2, 0, 3]


def test_no_perfect_matching():
    # left 2 and 3 both see only a: at most 3 of 4 left vertices can be matched
    adj = [[0, 1], [0], [0], [2, 3]]
    mate = kuhn_algorithm(4, 4, adj)
    assert check_matching(4, 4, adj, mate) == 3


def test_empty_and_edgeless():
    assert kuhn_algorithm(0, 0, []) == []
    assert kuhn_algorithm(0, 5, []) == []
    assert kuhn_algorithm(3, 0, [[], [], []]) == [None, None, None]
    assert kuhn_algorithm(2, 2, [[], []]) == [None, None]


def test_complete_and_parallel_edges():
    adj = [[0, 1, 2]] * 3
    assert check_matching(3, 3, adj, kuhn_algorithm(3, 3, adj)) == 3
    adj = [[0, 0, 0], [0, 0]]
    assert check_matching(2, 1, adj, kuhn_algorithm(2, 1, adj)) == 1


def test_long_augmenting_path_no_recursion_limit():
    # left j sees right j and j + 1 and takes j; the last left vertex sees only right 0,
    # so its augmenting path runs through all n earlier left vertices
    n = 3000
    adj = [[j, j + 1] for j in range(n)] + [[0]]
    mate = kuhn_algorithm(n + 1, n + 1, adj)
    assert check_matching(n + 1, n + 1, adj, mate) == n + 1
    assert mate[n] == 0 and mate[0] == 1 and mate[n - 1] == n


def test_random_against_brute_force():
    rng = random.Random(4127)
    for _ in range(600):
        nl, nr = rng.randint(0, 7), rng.randint(0, 7)
        p = rng.random()
        adj = [[v for v in range(nr) if rng.random() < p] for _ in range(nl)]
        mate = kuhn_algorithm(nl, nr, adj)
        assert check_matching(nl, nr, adj, mate) == brute_nu(nl, adj)
