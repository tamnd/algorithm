# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coloring-scc/. The authors are listed in prov/R4EPTY.jsonl.

import math
import random

from coloring_scc import Cost, coloring_scc


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
        n = rng.randint(1, 60)
        p = rng.choice([0.01, 0.03, 0.06, 0.15, 0.5])
        es = [(i, j) for i in range(n) for j in range(n) if i != j and rng.random() < p]
        if rng.random() < 0.3:  # a DAG
            es = [(i, j) for i, j in es if i < j]
        out.append((n, es))
    return out


def test_example() -> None:
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 3), (5, 0), (5, 6), (6, 5), (4, 7)]
    c = Cost()
    comp = coloring_scc(8, edges, cost=c, label=list(range(8)))
    assert comp == [2, 2, 2, 4, 4, 6, 6, 7]  # each SCC is named by its root
    assert c.iterations == 2


def test_against_tarjan() -> None:
    rng = random.Random(13)
    runs = 0
    for n, edges in family(rng):
        want = tarjan(n, edges)
        for _ in range(4):
            comp = coloring_scc(n, edges, random.Random(rng.random()))
            assert same_partition(comp, want)
            runs += 1
    assert runs >= 500


def test_reverse_path_with_fixed_labels_is_sequential() -> None:
    # the arcs go from larger to smaller labels: only one root per iteration
    for n in (1, 5, 40):
        c = Cost()
        coloring_scc(n, [(i + 1, i) for i in range(n - 1)], cost=c, label=list(range(n)))
        assert c.iterations == n


def test_iterations_on_random_graphs() -> None:
    # random digraphs with 2n arcs and random labels: c = 1, the mean number of iterations
    # stays below log2 n; on the reverse path, random labels give a mean below 2 log2 n
    rng = random.Random(14)
    for n in (64, 256, 1024):
        it = 0
        for _ in range(5):
            es = [(rng.randrange(n), rng.randrange(n)) for _ in range(2 * n)]
            c = Cost()
            coloring_scc(n, es, random.Random(rng.random()), c)
            it += c.iterations
        assert it / 5 <= math.log2(n)
        it = 0
        for _ in range(5):
            c = Cost()
            coloring_scc(n, [(i + 1, i) for i in range(n - 1)], random.Random(rng.random()), c)
            it += c.iterations
        assert it / 5 <= 2 * math.log2(n)
