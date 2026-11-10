# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-election/. The authors are listed in prov/5X8NA5.jsonl.

import random

from tree_election import diameter, random_tree, tree_election


def page_tree() -> tuple[list[list[int]], list[int]]:
    edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (5, 6), (6, 7)]
    adj: list[list[int]] = [[] for _ in range(8)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj, [4, 9, 2, 5, 7, 1, 3, 6]


def test_page_example() -> None:
    adj, ids = page_tree()
    res = tree_election(adj, ids, sync=True, wakeup=False)
    assert res["leaders"] == [1] and res["saturated"] == [3, 5]
    assert res["counts"] == {"W": 0, "M": 8, "L": 6} and res["time"] == 5
    assert res["known"] == [9] * 8


def test_page_example_one_starter() -> None:
    adj, ids = page_tree()
    res = tree_election(adj, ids, [0], sync=True)
    assert res["leaders"] == [1] and res["messages"] == 21


def test_tiny_trees() -> None:
    assert tree_election([[]], [5])["leaders"] == [0]
    res = tree_election([[1], [0]], [3, 8], [0], sync=True)
    assert res["leaders"] == [1] and res["counts"] == {"W": 1, "M": 2, "L": 0}


def test_exact_counts_on_random_trees() -> None:
    for n in range(2, 40):
        for s in range(25):
            rng = random.Random(1000 * n + s)
            adj = random_tree(n, rng)
            ids = rng.sample(range(1, 10**6), n)
            init = rng.sample(range(n), rng.randint(1, n))
            for sync in (False, True):
                res = tree_election(adj, ids, init, seed=s, sync=sync)
                k = res["starters"]
                assert res["counts"] == {"W": n + k - 2, "M": n, "L": n - 2}
                assert res["messages"] == 3 * n + k - 4
                assert res["leaders"] == [ids.index(max(ids))]
                assert res["known"] == [max(ids)] * n
                a, b = res["saturated"]
                assert b in adj[a]
                if sync:
                    assert k == len(init)
                    assert res["time"] <= 3 * diameter(adj) + 1


def test_without_wakeup_uses_2n_minus_2() -> None:
    for n in range(2, 60):
        for s in range(10):
            rng = random.Random(77 * n + s)
            adj = random_tree(n, rng)
            ids = rng.sample(range(1, 10**6), n)
            res = tree_election(adj, ids, seed=s, wakeup=False)
            assert res["messages"] == 2 * n - 2
            assert res["leaders"] == [ids.index(max(ids))]


def test_paths_and_stars() -> None:
    for n in range(2, 30):
        path = [[w for w in (v - 1, v + 1) if 0 <= w < n] for v in range(n)]
        star = [list(range(1, n))] + [[0] for _ in range(1, n)]
        for adj in (path, star):
            ids = list(range(n))
            for s in range(5):
                res = tree_election(adj, ids, [n - 1], seed=s)
                assert res["leaders"] == [n - 1] and res["messages"] == 3 * n - 3


def test_large_tree() -> None:
    rng = random.Random(5)
    adj = random_tree(2000, rng)
    ids = rng.sample(range(10**7), 2000)
    res = tree_election(adj, ids, [0, 1, 2], seed=1)
    assert res["leaders"] == [ids.index(max(ids))]
