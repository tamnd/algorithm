# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/acyclic-join-evaluation/. The authors are listed in prov/K0Q46K.jsonl.

import heapq
import itertools
import random

from acyclic_join_evaluation import gyo_join_tree, has_running_intersection


def prufer_trees(r):
    """All labeled trees on r nodes, as parent lists rooted at node 0."""
    if r == 1:
        yield [-1]
        return
    for seq in itertools.product(range(r), repeat=r - 2):
        degree = [1] * r
        for x in seq:
            degree[x] += 1
        leaves = [i for i in range(r) if degree[i] == 1]
        heapq.heapify(leaves)
        adj = [[] for _ in range(r)]
        for x in seq:
            leaf = heapq.heappop(leaves)
            adj[leaf].append(x)
            adj[x].append(leaf)
            degree[x] -= 1
            if degree[x] == 1:
                heapq.heappush(leaves, x)
        u, w = heapq.heappop(leaves), heapq.heappop(leaves)
        adj[u].append(w)
        adj[w].append(u)
        parent, stack = [-1] * r, [0]
        seen = {0}
        while stack:
            v = stack.pop()
            for y in adj[v]:
                if y not in seen:
                    seen.add(y)
                    parent[y] = v
                    stack.append(y)
        yield parent


def brute_acyclic(edges):
    return any(has_running_intersection(edges, p) for p in prufer_trees(len(edges)))


def test_tree_count() -> None:
    assert sum(1 for _ in prufer_trees(5)) == 5 ** 3


def test_examples() -> None:
    tri = ["AB", "BC", "CA"]
    assert gyo_join_tree(tri) is None
    p = gyo_join_tree(["ABC", "AB", "BC", "CA"])     # alpha-acyclic, not beta-acyclic
    assert p is not None and has_running_intersection(["ABC", "AB", "BC", "CA"], p)
    path = ["AB", "BC", "CD"]
    assert has_running_intersection(path, gyo_join_tree(path))
    assert gyo_join_tree(["AB", "BC", "CD", "DA"]) is None          # 4-cycle
    assert gyo_join_tree([]) == [] and gyo_join_tree(["A"]) == [-1]
    assert has_running_intersection(["AB", "CD"], gyo_join_tree(["AB", "CD"]))  # disconnected
    assert not has_running_intersection(path, [-1, 0, 0])          # AB-CD edge breaks C


def test_against_brute_force() -> None:
    rng = random.Random(11)
    acyclic = cyclic = 0
    for _ in range(600):
        r = rng.randrange(1, 6)
        edges = ["".join(sorted(rng.sample("ABCDE", rng.randrange(1, 4)))) for _ in range(r)]
        p = gyo_join_tree(edges)
        assert (p is not None) == brute_acyclic(edges)
        if p is not None:
            assert has_running_intersection(edges, p)
            acyclic += 1
        else:
            cyclic += 1
    assert acyclic > 50 and cyclic > 50
