# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-anonymity-approximation/. The authors are listed in prov/3CXF3J.jsonl.
"""The forest algorithm of Aggarwal et al. for k-anonymity by cell suppression, with ratio 3k - 3.

The input is a list of n rows, each a tuple of d values. The output groups the rows into
clusters of k to 3k - 3 rows and replaces by None each cell of a column on which the rows
of its cluster differ. The tree splitting uses explicit stacks, not recursion.
"""

from typing import Hashable, Optional, Sequence

Row = tuple[Hashable, ...]


def hamming(x: Sequence[Hashable], y: Sequence[Hashable]) -> int:
    """The number of positions where x and y differ."""
    return sum(1 for a, b in zip(x, y) if a != b)


def build_forest(rows: Sequence[Row], k: int) -> list[tuple[int, int]]:
    """Return the directed edges (u, x) of the forest: each tree has at least k vertices,
    and its total weight is at most the cost of an optimal k-anonymous suppression.

    Precondition: 2 <= k <= len(rows).
    Cost: O(n^2 d) time for the weights and O(n^2) for the n - 1 merges at most.
    """
    n = len(rows)
    w = [[hamming(rows[i], rows[j]) for j in range(n)] for i in range(n)]  # @line L1
    label = list(range(n))  # @line L2
    root = list(range(n))  # root[t] is the vertex of tree t with no outgoing edge
    edges: list[tuple[int, int]] = []
    while True:
        size: dict[int, int] = {}
        for t in label:
            size[t] = size.get(t, 0) + 1
        small = [t for t in size if size[t] < k]
        if not small:  # @line L3
            break
        t = min(small, key=lambda s: root[s])
        u = root[t]  # @line L4
        x = min((v for v in range(n) if label[v] != t), key=lambda v: (w[u][v], v))  # @line L5
        edges.append((u, x))  # @line L6
        target = label[x]
        for v in range(n):
            if label[v] == t:
                label[v] = target
    return edges


def _decompose(vec: list[Row], real: list[bool], adj: dict[int, set[int]], k: int) -> tuple[set[int], set[int]]:
    """Split one tree (the vertex set of adj) with s >= 3k - 2 row vertices into two trees,
    each with at least k row vertices. May add one Steiner vertex to vec, real and adj.
    The walk only goes down in the tree rooted at r, so one call takes O(t log t) time
    for a tree of t vertices.
    """
    s = sum(1 for v in adj if real[v])
    r = min(v for v in adj if real[v])
    # Root the tree at r once, with an explicit stack, and count the row vertices of each subtree.
    parent = {r: -1}
    order = [r]
    stack = [r]
    while stack:
        v = stack.pop()
        for y in adj[v]:
            if y not in parent:
                parent[y] = v
                order.append(y)
                stack.append(y)
    cnt = {v: (1 if real[v] else 0) for v in order}
    for v in reversed(order):
        if parent[v] >= 0:
            cnt[parent[v]] += cnt[v]
    u = r  # @line L12

    def side(y: int) -> int:
        """The row vertices on the side of y when the edge u-y is cut."""
        return cnt[y] if parent[y] == u else s - cnt[u]

    while True:
        c = min(adj[u], key=lambda y: (-side(y), y))
        phi = side(c)  # @line L13
        if phi <= s - k:  # @line L14
            break
        u = c
    children = sorted(adj[u], key=lambda y: (-side(y), y))

    def subtree(top: int) -> set[int]:
        """The vertices on the side of top when the edge u-top is cut."""
        out = {top}
        st = [top]
        while st:
            v = st.pop()
            for y in adj[v]:
                if y != u and y not in out:
                    out.add(y)
                    st.append(y)
        return out

    if phi >= k:  # @line L15
        part = subtree(c)
        adj[u].discard(c)
        adj[c].discard(u)
        return part, set(adj) - part
    group: set[int] = set()  # @line L16
    taken: list[int] = []
    got = 0
    for y in children:
        if got >= k:
            break
        group |= subtree(y)
        taken.append(y)
        got += side(y)
    steiner = len(vec)  # @line L17
    vec.append(vec[u])
    real.append(False)
    adj[steiner] = set()
    for y in taken:
        adj[u].discard(y)
        adj[y].discard(u)
        adj[y].add(steiner)
        adj[steiner].add(y)
    group.add(steiner)
    return group, set(adj) - group


def anonymize(rows: Sequence[Row], k: int) -> tuple[list[list[int]], list[tuple[Optional[Hashable], ...]], int]:
    """Return (clusters, table, cost). The clusters partition the row indices; each has
    between k and 3k - 3 rows. In table, each cell of a column on which the rows
    of its cluster differ is None. The cost is the number of None cells, and it is at
    most (3k - 3) times the optimal cost.

    Precondition: 2 <= k <= len(rows), and all rows have the same length d.
    Cost: O(n^2 d) time for the weights and the forest, O(n^2 log n) time for at most
    n / k splits of O(n log n) each, and O(n^2) space.
    """
    n = len(rows)
    edges = build_forest(rows, k)
    vec: list[Row] = list(rows)
    real = [True] * n
    adj_all: dict[int, set[int]] = {v: set() for v in range(n)}
    for u, x in edges:
        adj_all[u].add(x)
        adj_all[x].add(u)
    seen: set[int] = set()
    trees: list[set[int]] = []  # @line L7
    for v in range(n):
        if v not in seen:
            comp = {v}
            st = [v]
            while st:
                y = st.pop()
                for z in adj_all[y]:
                    if z not in comp:
                        comp.add(z)
                        st.append(z)
            seen |= comp
            trees.append(comp)
    done: list[set[int]] = []
    work = trees
    while work:  # @line L8
        t = work.pop()
        if sum(1 for v in t if real[v]) <= 3 * k - 3:
            done.append(t)
            continue
        adj = {v: set(y for y in adj_all[v] if y in t) for v in t}
        a, b = _decompose(vec, real, adj, k)  # @line L9
        for v in adj:
            adj_all[v] = adj[v]
        work.append(a)
        work.append(b)
    clusters = sorted(sorted(v for v in t if real[v]) for t in done)
    table: list[tuple[Optional[Hashable], ...]] = [tuple(r) for r in rows]
    cost = 0
    d = len(rows[0])
    for cl in clusters:  # @line L10
        differ = [j for j in range(d) if len({rows[i][j] for i in cl}) > 1]
        cost += len(cl) * len(differ)
        for i in cl:
            table[i] = tuple(None if j in differ else rows[i][j] for j in range(d))
    return clusters, table, cost  # @line L11
