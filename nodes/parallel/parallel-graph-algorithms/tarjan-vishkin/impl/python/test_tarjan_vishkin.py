# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tarjan-vishkin/. The authors are listed in prov/91X4KQ.jsonl.

import math
import random

from tarjan_vishkin import Cost, euler_preorder, tarjan_vishkin


def hopcroft_tarjan(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Sequential biconnected components with an edge stack and an explicit DFS stack."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    disc = [-1] * n
    low = [0] * n
    block = [-1] * len(edges)
    t = 0
    nb = 0
    for s in range(n):
        if disc[s] != -1:
            continue
        disc[s] = low[s] = t
        t += 1
        stack = [(s, -1, 0)]
        estack: list[int] = []
        while stack:
            u, pe, k = stack[-1]
            if k < len(adj[u]):
                stack[-1] = (u, pe, k + 1)
                w, i = adj[u][k]
                if i == pe:
                    continue
                if disc[w] == -1:
                    estack.append(i)
                    disc[w] = low[w] = t
                    t += 1
                    stack.append((w, i, 0))
                elif disc[w] < disc[u]:
                    estack.append(i)
                    low[u] = min(low[u], disc[w])
            else:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[u])
                    if low[u] >= disc[p]:
                        while True:
                            e = estack.pop()
                            block[e] = nb
                            if e == pe:
                                break
                        nb += 1
    return block


def same_partition(a: list[int], b: list[int]) -> bool:
    fwd: dict[int, int] = {}
    bwd: dict[int, int] = {}
    for x, y in zip(a, b):
        if fwd.setdefault(x, y) != y or bwd.setdefault(y, x) != x:
            return False
    return True


EXAMPLE = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
EXAMPLE_TREE = [0, 1, 2, 4, 5, 6]  # the BFS tree from 0; the nontree edges are {2,3} and {5,6}


def test_example() -> None:
    c = Cost()
    parent, pre, nd = euler_preorder(7, [EXAMPLE[i] for i in EXAMPLE_TREE], [0], c)
    assert pre == [1, 2, 7, 3, 4, 5, 6, 0]
    assert nd == [7, 5, 1, 4, 3, 1, 1, 8]
    assert parent[:7] == [7, 0, 0, 1, 3, 4, 4]
    for seed in range(10):
        block = tarjan_vishkin(7, EXAMPLE, random.Random(seed), Cost(), EXAMPLE_TREE)
        assert same_partition(block, [0, 0, 0, 0, 1, 2, 2, 2])
        assert same_partition(tarjan_vishkin(7, EXAMPLE, random.Random(seed)), [0, 0, 0, 0, 1, 2, 2, 2])


def family(rng: random.Random) -> list[tuple[int, list[tuple[int, int]]]]:
    out = []
    for n in (1, 2, 3, 6, 15):
        out.append((n, []))
        out.append((n, [(i, i + 1) for i in range(n - 1)]))
        out.append((n, [(0, i) for i in range(1, n)]))
        if n >= 3:
            out.append((n, [(i, (i + 1) % n) for i in range(n)]))
        out.append((n, [(i, j) for i in range(n) for j in range(i + 1, n)]))
    for _ in range(230):
        n = rng.randint(1, 30)
        p = rng.choice([0.03, 0.08, 0.15, 0.3, 0.6])
        es = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        perm = list(range(n))
        rng.shuffle(perm)
        es = [(perm[u], perm[v]) for u, v in es]
        rng.shuffle(es)
        out.append((n, es))
    # chains of cycles joined at cut vertices, and cycles joined by bridges
    for _ in range(30):
        es = []
        k = 0
        for _ in range(rng.randint(1, 5)):
            size = rng.randint(1, 5)
            cyc = [k] + list(range(k + 1, k + size + 1))
            if size >= 2:
                es += [(cyc[i], cyc[(i + 1) % len(cyc)]) for i in range(len(cyc))]
            else:
                es.append((k, k + 1))
            k += size
        out.append((k + 1, es))
    return out


def test_against_hopcroft_tarjan() -> None:
    rng = random.Random(11)
    runs = 0
    for n, edges in family(rng):
        want = hopcroft_tarjan(n, edges)
        for _ in range(2):
            c = Cost()
            got = tarjan_vishkin(n, edges, random.Random(rng.random()), c)
            assert same_partition(got, want)
            lg = math.log2(n + 2)
            assert c.span <= 12 * lg * lg + 40  # O(log^2 n) span with c = 12
            runs += 1
    assert runs >= 500
