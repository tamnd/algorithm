# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-clustering/. The authors are listed in prov/5FFE0B.jsonl.


def _normalize(m: list[list[float]], n: int, prune: float) -> None:
    """Scale each column of m to sum 1, set entries below prune to 0, and scale again."""
    for j in range(n):
        s = sum(m[i][j] for i in range(n))
        for i in range(n):
            m[i][j] /= s
        for i in range(n):
            if m[i][j] < prune:
                m[i][j] = 0.0
        s = sum(m[i][j] for i in range(n))
        for i in range(n):
            m[i][j] /= s


def _product(a: list[list[float]], b: list[list[float]], n: int) -> list[list[float]]:
    """The product a b of two n by n matrices, skipping the zero entries of a."""
    c = [[0.0] * n for _ in range(n)]
    for i in range(n):
        ci = c[i]
        for k in range(n):
            x = a[i][k]
            if x != 0.0:
                bk = b[k]
                for j in range(n):
                    ci[j] += x * bk[j]
    return c


def markov_clustering(
    n: int,
    edges: list[tuple[int, int, float]],
    expansion: int = 2,
    inflation: float = 2.0,
    loop_weight: float = 1.0,
    prune: float = 1e-6,
    tol: float = 1e-9,
    max_iter: int = 1000,
) -> tuple[list[list[int]], int]:
    """Return (clusters, iterations) of MCL on an undirected weighted graph on 0 .. n-1.

    edges holds triples (u, v, w) with w > 0; a pair given twice adds its
    weights and u == v adds to the self-loop. Every vertex gets an extra
    self-loop of weight loop_weight. One iteration is expansion (the power
    M^expansion), inflation (each entry to the power inflation) and column
    normalization, with entries below prune set to 0 (prune must be below
    1/n). The loop stops when no entry changed by more than tol, or after
    max_iter iterations. The clusters are the connected components of the
    graph with an edge {i, j} for each nonzero entry of the last matrix,
    each sorted, in order of their smallest vertex. Dense arithmetic, so one
    iteration costs O(n^3) time.
    """
    if n == 0:
        return [], 0
    a = [[0.0] * n for _ in range(n)]  # @line L1
    for u, v, w in edges:
        a[u][v] += w
        if u != v:
            a[v][u] += w
    for v in range(n):
        a[v][v] += loop_weight
    m = [row[:] for row in a]  # @line L2
    _normalize(m, n, 0.0)
    t = 0
    while True:  # @line L3
        old = m  # @line L4
        x = m  # @line L5
        for _ in range(expansion - 1):
            x = _product(x, m, n)
        m = [[v ** inflation for v in row] for row in x]  # @line L6
        _normalize(m, n, prune)  # @line L7
        t += 1
        change = max(abs(m[i][j] - old[i][j]) for i in range(n) for j in range(n))
        if change <= tol or t >= max_iter:  # @line L8
            break
    parent = list(range(n))  # @line L9

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n):
        for j in range(n):
            if m[i][j] > 0.0:
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[max(ri, rj)] = min(ri, rj)
    groups: dict[int, list[int]] = {}  # @line L10
    for v in range(n):
        groups.setdefault(find(v), []).append(v)
    return sorted(groups.values()), t
