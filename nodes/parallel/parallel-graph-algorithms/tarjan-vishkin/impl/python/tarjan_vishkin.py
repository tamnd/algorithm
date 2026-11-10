# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tarjan-vishkin/. The authors are listed in prov/91X4KQ.jsonl.

"""Tarjan-Vishkin biconnected components, simulated one PRAM step at a time.

Each parallel step reads the state from before the step. Concurrent writes to
one cell follow the arbitrary rule, with a seeded generator as the arbiter.

Precondition: n >= 0, edges is a list of pairs (u, v) with 0 <= u, v < n,
u != v, and no pair occurs twice (a simple undirected graph).
Cost: the spanning forest and the connectivity of the auxiliary graph use
Shiloach-Vishkin with full shortcuts, O(log^2 n) span each; the Euler tour is
ranked by pointer jumping, O(log n) span and O(n log n) work; the low and high
values come from a sparse table, O(n log n) work and O(log n) span. The rules
of the auxiliary graph take O(n + m) work and O(1) span.
"""

import math
import random


class Cost:
    """Counters for work, span and the iterations of the two connectivity calls."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.sv_iterations = 0

    def step(self, work: int, span: int = 1) -> None:
        self.work += work
        self.span += span


def _arbitrary(P: list[int], writes: list[tuple[int, int, int]], rng: random.Random) -> dict[int, int]:
    """Arbitrary CRCW rule. writes holds (address, value, tag); returns the tag of the winner at each address."""
    by: dict[int, list[tuple[int, int]]] = {}
    for a, v, t in writes:
        by.setdefault(a, []).append((v, t))
    won = {}
    for a, cands in by.items():
        v, t = rng.choice(cands)
        P[a] = v
        won[a] = t
    return won


def _stars(P: list[int]) -> list[bool]:
    st = [True] * len(P)
    for v in range(len(P)):
        if P[v] != P[P[v]]:
            st[v] = False
            st[P[P[v]]] = False
    return [st[v] and st[P[v]] for v in range(len(P))]


def sv_forest(n: int, arcs: list[tuple[int, int, int]], rng: random.Random, c: Cost) -> tuple[list[int], list[int]]:
    """Shiloach-Vishkin with full shortcuts. arcs holds (u, v, tag) in both directions.

    Returns the star labels and the tags of the winning hooks, which form a spanning forest.
    """
    P = list(range(n))
    tags: list[int] = []
    c.step(n)
    while True:
        c.sv_iterations += 1
        old = P[:]
        st = _stars(P)
        won = _arbitrary(P, [(P[u], P[v], t) for u, v, t in arcs if st[u] and P[u] > P[v]], rng)
        received = {old[P[r]] for r in won}
        stag = [st[v] and old[v] not in won and old[v] not in received for v in range(n)]
        won2 = _arbitrary(P, [(P[u], P[v], t) for u, v, t in arcs if stag[u] and P[u] != P[v]], rng)
        tags += list(won.values()) + list(won2.values())
        steps = 9
        P = [P[P[v]] for v in range(n)]
        while any(P[v] != P[P[v]] for v in range(n)):
            P = [P[P[v]] for v in range(n)]
            steps += 2
        c.step(steps * (n + len(arcs)), steps)
        if P == old:
            return P, tags


def euler_preorder(n: int, tree_edges: list[tuple[int, int]], roots: list[int], c: Cost) -> tuple[list[int], list[int], list[int]]:
    """Root the forest at a new vertex z = n joined to every root; return parent, pre and nd for 0..n.

    The Euler tour of the tree is ranked by pointer jumping, and pre and nd come from a prefix sum.
    """
    z = n
    nbrs: list[list[int]] = [[] for _ in range(n + 1)]
    for u, v in tree_edges:
        nbrs[u].append(v)
        nbrs[v].append(u)
    for r in roots:
        nbrs[z].append(r)
        nbrs[r].append(z)
    for v in range(n + 1):
        nbrs[v].sort()
    lg = max(1, math.ceil(math.log2(n + 2)))
    c.step((n + len(tree_edges)) * lg, lg)  # sorting the arcs by tail
    where = {}
    for v in range(n + 1):
        for k, u in enumerate(nbrs[v]):
            where[(v, u)] = k
    arcs = [(u, v) for u in range(n + 1) for v in nbrs[u]]
    idx = {a: i for i, a in enumerate(arcs)}
    L = len(arcs)
    succ = [-1] * L
    for i, (u, v) in enumerate(arcs):
        k = where[(v, u)]
        succ[i] = idx[(v, nbrs[v][(k + 1) % len(nbrs[v])])]
    last = idx[(nbrs[z][-1], z)]
    succ[last] = -1  # the tour starts at (z, first neighbour) and ends at (last neighbour, z)
    c.step(L)
    # list ranking by pointer jumping: rank = number of arcs after this one
    rank = [0 if s == -1 else 1 for s in succ]
    nxt = succ[:]
    while any(s != -1 for s in nxt):
        rank = [rank[i] + (rank[nxt[i]] if nxt[i] != -1 else 0) for i in range(L)]
        nxt = [nxt[nxt[i]] if nxt[i] != -1 else -1 for i in range(L)]
        c.step(L)
    pos = [L - 1 - r for r in rank]
    parent = [-1] * (n + 1)
    tour = [0] * L
    for i, (u, v) in enumerate(arcs):
        tour[pos[i]] = i
        if pos[i] < pos[idx[(v, u)]]:
            parent[v] = u
    c.step(L)
    # prefix sum of the forward flags in tour order
    cnt = [0] * L
    run = 0
    for p in range(L):
        u, v = arcs[tour[p]]
        run += parent[v] == u
        cnt[p] = run
    c.step(2 * L, 2 * max(1, math.ceil(math.log2(L))))
    pre = [0] * (n + 1)
    nd = [n + 1] * (n + 1)
    for v in range(n):
        p = parent[v]
        pre[v] = cnt[pos[idx[(p, v)]]]
        nd[v] = (pos[idx[(v, p)]] - pos[idx[(p, v)]] + 1) // 2
    c.step(n + 1)
    return parent, pre, nd


def _sparse(a: list[int], f, c: Cost) -> list[list[int]]:
    t = [a[:]]
    k = 1
    while 2 * k <= len(a):
        prev = t[-1]
        t.append([f(prev[i], prev[i + k]) for i in range(len(a) - 2 * k + 1)])
        c.step(len(a))
        k *= 2
    return t


def _query(t: list[list[int]], f, i: int, j: int) -> int:
    k = (j - i + 1).bit_length() - 1
    return f(t[k][i], t[k][j - (1 << k) + 1])


def tarjan_vishkin(
    n: int,
    edges: list[tuple[int, int]],
    rng: random.Random | None = None,
    cost: Cost | None = None,
    tree: list[int] | None = None,
) -> list[int]:
    """Return a block label for each edge: two edges get the same label if and only if they are in one biconnected component.

    tree, if given, is the list of the indices of the edges of a spanning forest; otherwise Shiloach-Vishkin finds one.
    """
    rng = rng if rng is not None else random.Random(0)
    c = cost if cost is not None else Cost()
    m = len(edges)
    if n == 0:
        return []
    both = [(u, v, i) for i, (u, v) in enumerate(edges)] + [(v, u, i) for i, (u, v) in enumerate(edges)]
    if tree is None:
        P, tree = sv_forest(n, both, rng, c)  # @line L1
    else:
        given = set(tree)
        P, _ = sv_forest(n, [a for a in both if a[2] in given], rng, c)
    is_tree = [False] * m
    for i in tree:
        is_tree[i] = True
    roots = [v for v in range(n) if P[v] == v]  # @line L2
    parent, pre, nd = euler_preorder(n, [edges[i] for i in tree], roots, c)  # @line L3
    # @line L4 (parent, pre and nd come from the ranked tour)
    lo = pre[:]
    hi = pre[:]
    for i, (u, v) in enumerate(edges):  # @line L5
        if not is_tree[i]:
            lo[u], hi[u] = min(lo[u], pre[v]), max(hi[u], pre[v])
            lo[v], hi[v] = min(lo[v], pre[u]), max(hi[v], pre[u])
    c.step(n + m)
    by_pre_lo = [0] * (n + 1)
    by_pre_hi = [0] * (n + 1)
    for v in range(n + 1):
        by_pre_lo[pre[v]] = lo[v]
        by_pre_hi[pre[v]] = hi[v]
    tlo = _sparse(by_pre_lo, min, c)
    thi = _sparse(by_pre_hi, max, c)
    low = [_query(tlo, min, pre[v], pre[v] + nd[v] - 1) for v in range(n + 1)]  # @line L6
    high = [_query(thi, max, pre[v], pre[v] + nd[v] - 1) for v in range(n + 1)]
    c.step(n + 1)
    aux: list[tuple[int, int, int]] = []
    for i, (a, b) in enumerate(edges):  # @line L7
        if not is_tree[i]:
            v, w = (a, b) if pre[a] < pre[b] else (b, a)
            if pre[v] + nd[v] <= pre[w]:
                aux += [(v, w, i), (w, v, i)]
    for i, (a, b) in enumerate(edges):  # @line L8
        if is_tree[i]:
            w = b if parent[b] == a else a
            v = parent[w]
            if v != n and (low[w] < pre[v] or high[w] >= pre[v] + nd[v]):
                aux += [(v, w, i), (w, v, i)]
    c.step(m)
    label, _ = sv_forest(n, aux, rng, c)  # @line L9
    block = [0] * m
    for i, (a, b) in enumerate(edges):  # @line L10
        if is_tree[i]:
            block[i] = label[b if parent[b] == a else a]
        else:
            block[i] = label[b if pre[a] < pre[b] else a]
    c.step(m)
    return block  # @line L11
