# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-backward-scc/. The authors are listed in prov/5T2WQ4.jsonl.

import math
import random

from forward_backward_scc import Cost, fw_bw_scc


def tarjan(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Sequential Tarjan SCC with an explicit stack."""
    out: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        out[u].append(v)
    index = [-1] * n
    low = [0] * n
    on = [False] * n
    stack: list[int] = []
    comp = [-1] * n
    counter = ncomp = 0
    for s in range(n):
        if index[s] != -1:
            continue
        work = [(s, 0)]
        index[s] = low[s] = counter
        counter += 1
        stack.append(s)
        on[s] = True
        while work:
            v, i = work[-1]
            if i < len(out[v]):
                work[-1] = (v, i + 1)
                w = out[v][i]
                if index[w] == -1:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on[w] = True
                    work.append((w, 0))
                elif on[w]:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    while True:
                        w = stack.pop()
                        on[w] = False
                        comp[w] = ncomp
                        if w == v:
                            break
                    ncomp += 1
    return comp


def same_partition(a: list[int], b: list[int]) -> bool:
    fwd: dict[int, int] = {}
    bwd: dict[int, int] = {}
    for x, y in zip(a, b):
        if fwd.setdefault(x, y) != y or bwd.setdefault(y, x) != x:
            return False
    return True


def family(rng: random.Random) -> list[tuple[int, list[tuple[int, int]]]]:
    out = []
    for n in (1, 2, 7, 30):
        out.append((n, []))
        out.append((n, [(i, i + 1) for i in range(n - 1)]))  # directed path
        out.append((n, [(i, (i + 1) % n) for i in range(n)]))  # directed cycle
        out.append((n, [(0, i) for i in range(1, n)]))  # out-star
        out.append((n, [(i, j) for i in range(n) for j in range(n) if i != j]))  # complete
        out.append((n, [(i, i) for i in range(n)] + [(i, i + 1) for i in range(n - 1)] * 2))  # loops and parallel arcs
    for _ in range(140):
        n = rng.randint(1, 70)
        p = rng.choice([0.01, 0.03, 0.06, 0.15, 0.5])
        es = [(i, j) for i in range(n) for j in range(n) if i != j and rng.random() < p]
        if rng.random() < 0.3:  # a DAG: keep the arcs going up
            es = [(i, j) for i, j in es if i < j]
        out.append((n, es))
    return out


def test_example() -> None:
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 3), (5, 0), (5, 6), (6, 5), (4, 7)]
    c = Cost()
    comp = fw_bw_scc(8, edges, cost=c, pick=min)
    groups = sorted(sorted(v for v in range(8) if comp[v] == k) for k in set(comp))
    assert groups == [[0, 1, 2], [3, 4], [5, 6], [7]]
    assert c.depth == 2 and c.parts == 3


def test_against_tarjan() -> None:
    rng = random.Random(11)
    runs = 0
    for n, edges in family(rng):
        want = tarjan(n, edges)
        for trim in (True, False, True, False):
            comp = fw_bw_scc(n, edges, random.Random(rng.random()), trim=trim)
            assert same_partition(comp, want)
            runs += 1
    assert runs >= 500


def test_disjoint_cycles_are_sequential() -> None:
    # k disjoint directed triangles: trimming removes nothing, and each level finds one triangle
    for k in (1, 5, 40):
        es = [(3 * i + j, 3 * i + (j + 1) % 3) for i in range(k) for j in range(3)]
        c = Cost()
        comp = fw_bw_scc(3 * k, es, random.Random(k), c)
        assert len(set(comp)) == k
        assert c.depth == k


def test_depth_and_work_on_random_graphs() -> None:
    # random digraphs with m = 2n arcs. With trimming: c = 0.5, the mean recursion depth stays
    # below 0.5 log2 n, and the mean work below 5 (n + m). Without trimming the depth grows
    # linearly: every vertex that is its own SCC needs its own pivot.
    rng = random.Random(12)
    for n in (64, 256, 1024):
        depth = work = 0
        for _ in range(10):
            es = [(rng.randrange(n), rng.randrange(n)) for _ in range(2 * n)]
            c = Cost()
            fw_bw_scc(n, es, random.Random(rng.random()), c, trim=True)
            depth += c.depth
            work += c.work
        assert depth / 10 <= 0.5 * math.log2(n)
        assert work / 10 <= 5 * (n + 2 * n)
    n = 1024
    depth = 0
    for _ in range(5):
        es = [(rng.randrange(n), rng.randrange(n)) for _ in range(2 * n)]
        c = Cost()
        fw_bw_scc(n, es, random.Random(rng.random()), c, trim=False)
        depth += c.depth
    assert depth / 5 >= n / 16
