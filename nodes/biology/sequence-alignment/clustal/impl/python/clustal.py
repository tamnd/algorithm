# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clustal/. The authors are listed in prov/CZRQ68.jsonl.

"""A small ClustalW-style progressive aligner.

Steps: pairwise global alignments give distances 1 - identity, neighbor
joining gives an unrooted guide tree, midpoint rooting makes it rooted,
branch lengths give sequence weights, and profiles are aligned in postorder
with a weighted average of pair scores. Scores are maximized. The gap
penalty is linear; ClustalW's position-specific gap rules are left out.
"""

from fractions import Fraction
from typing import Callable

GAP = "-"
Score = Callable[[str, str], int]


def dna_score(x: str, y: str) -> int:
    """Match +1, mismatch -1, letter against gap -2, gap against gap 0."""
    if x == GAP and y == GAP:
        return 0
    if x == GAP or y == GAP:
        return -2
    return 1 if x == y else -1


def nw(s: str, t: str, score: Score) -> tuple[int, str, str]:
    """Needleman-Wunsch: an optimal global alignment of s and t, maximizing the score."""
    n, m = len(s), len(t)
    f = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        f[i][0] = f[i - 1][0] + score(s[i - 1], GAP)
    for j in range(1, m + 1):
        f[0][j] = f[0][j - 1] + score(GAP, t[j - 1])
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            f[i][j] = max(f[i - 1][j - 1] + score(s[i - 1], t[j - 1]),
                          f[i - 1][j] + score(s[i - 1], GAP),
                          f[i][j - 1] + score(GAP, t[j - 1]))
    a, b, i, j = [], [], n, m
    while i or j:
        if i and j and f[i][j] == f[i - 1][j - 1] + score(s[i - 1], t[j - 1]):
            a.append(s[i - 1]); b.append(t[j - 1]); i -= 1; j -= 1
        elif i and f[i][j] == f[i - 1][j] + score(s[i - 1], GAP):
            a.append(s[i - 1]); b.append(GAP); i -= 1
        else:
            a.append(GAP); b.append(t[j - 1]); j -= 1
    return f[n][m], "".join(reversed(a)), "".join(reversed(b))


def identity_distance(a: str, b: str) -> Fraction:
    """1 - (identical pairs / aligned letter pairs), on one pairwise alignment."""
    pairs = [(x, y) for x, y in zip(a, b) if x != GAP and y != GAP]
    if not pairs:
        return Fraction(1)
    return 1 - Fraction(sum(x == y for x, y in pairs), len(pairs))


def neighbor_joining(d: list[list[Fraction]]) -> dict[int, dict[int, Fraction]]:
    """Saitou-Nei neighbor joining. Leaves are 0..n-1; returns an adjacency map with
    branch lengths. Negative lengths are set to 0."""
    n = len(d)
    adj: dict[int, dict[int, Fraction]] = {i: {} for i in range(n)}
    if n == 2:
        adj[0][1] = adj[1][0] = max(d[0][1], Fraction(0))
    if n <= 2:
        return adj
    dist = {(i, j): d[i][j] for i in range(n) for j in range(n)}
    active = list(range(n))
    nxt = n
    while len(active) > 2:
        r = len(active)
        tot = {i: sum(dist[i, j] for j in active) for i in active}
        best = None
        for x in range(r):
            for y in range(x + 1, r):
                i, j = active[x], active[y]
                q = (r - 2) * dist[i, j] - tot[i] - tot[j]
                if best is None or q < best[0]:
                    best = (q, i, j)
        _, i, j = best
        li = dist[i, j] / 2 + (tot[i] - tot[j]) / (2 * (r - 2))
        lj = dist[i, j] - li
        u = nxt
        nxt += 1
        adj[u] = {}
        for v, ln in ((i, li), (j, lj)):
            adj[u][v] = adj[v][u] = max(ln, Fraction(0))
        for m in active:
            if m not in (i, j):
                dist[u, m] = dist[m, u] = (dist[i, m] + dist[j, m] - dist[i, j]) / 2
        dist[u, u] = Fraction(0)
        active = [m for m in active if m not in (i, j)] + [u]
    a, b = active
    adj[a][b] = adj[b][a] = max(dist[a, b], Fraction(0))
    return adj


def _paths_from(adj, src):
    """Distance and parent of every node, from src."""
    dist, par, stack = {src: Fraction(0)}, {src: None}, [src]
    while stack:
        u = stack.pop()
        for v, ln in adj[u].items():
            if v not in dist:
                dist[v], par[v] = dist[u] + ln, u
                stack.append(v)
    return dist, par


def midpoint_root(adj, leaves: list[int]):
    """Root the tree at the middle of its longest leaf-to-leaf path.
    Returns (root, children map, branch length to parent)."""
    adj = {u: dict(nb) for u, nb in adj.items()}
    if len(leaves) == 1:
        return leaves[0], {leaves[0]: []}, {leaves[0]: Fraction(0)}
    best = None
    for a in leaves:
        dist, _ = _paths_from(adj, a)
        for b in leaves:
            if b > a and (best is None or dist[b] > best[0]):
                best = (dist[b], a, b)
    diam, a, b = best
    dist, par = _paths_from(adj, a)
    half = diam / 2
    v = b
    while dist[par[v]] > half:  # walk up from b to the edge that holds the midpoint
        v = par[v]
    u = par[v]
    root = max(adj) + 1
    ln = adj[u].pop(v)
    adj[v].pop(u)
    adj[root] = {u: half - dist[u], v: dist[v] - half}
    adj[u][root] = half - dist[u]
    adj[v][root] = dist[v] - half
    children, up, stack, seen = {}, {root: Fraction(0)}, [root], {root}
    while stack:
        x = stack.pop()
        children[x] = []
        for y, l in adj[x].items():
            if y not in seen:
                seen.add(y)
                children[x].append(y)
                up[y] = l
                stack.append(y)
    assert ln == adj[root][u] + adj[root][v]
    return root, children, up


def sequence_weights(root, children, up, leaves: list[int]) -> dict[int, Fraction]:
    """ClustalW-style weights: each edge length is shared equally by the leaves below it."""
    below: dict[int, int] = {}

    def count(x):
        below[x] = 1 if not children[x] else sum(count(y) for y in children[x])
        return below[x]

    count(root)
    w: dict[int, Fraction] = {}

    def walk(x, acc):
        if x != root:
            acc += up[x] / below[x]
        if not children[x]:
            w[x] = acc
        for y in children[x]:
            walk(y, acc)

    walk(root, Fraction(0))
    if all(w[x] == 0 for x in leaves):
        return {x: Fraction(1) for x in leaves}
    return w


def profile_align(xr, xw, yr, yw, score: Score):
    """Align two groups of rows (with weights) as blocks, maximizing the weighted
    average pair score of columns. Gaps are inserted as whole columns."""
    m = len(xr[0]) if xr else 0
    n = len(yr[0]) if yr else 0
    if sum(xw) == 0:  # a group of identical sequences on zero-length branches
        xw = [Fraction(1)] * len(xr)
    if sum(yw) == 0:
        yw = [Fraction(1)] * len(yr)
    norm = sum(xw) * sum(yw)

    def col(xc, yc):
        return sum(a * b * score(p, q) for p, a in zip(xc, xw) for q, b in zip(yc, yw)) / norm

    xcols = [[r[p] for r in xr] for p in range(m)]
    ycols = [[r[p] for r in yr] for p in range(n)]
    gx = [GAP] * len(xr)
    gy = [GAP] * len(yr)
    f = [[Fraction(0)] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        f[i][0] = f[i - 1][0] + col(xcols[i - 1], gy)
    for j in range(1, n + 1):
        f[0][j] = f[0][j - 1] + col(gx, ycols[j - 1])
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            f[i][j] = max(f[i - 1][j - 1] + col(xcols[i - 1], ycols[j - 1]),
                          f[i - 1][j] + col(xcols[i - 1], gy),
                          f[i][j - 1] + col(gx, ycols[j - 1]))
    out, i, j = [], m, n
    while i or j:
        if i and j and f[i][j] == f[i - 1][j - 1] + col(xcols[i - 1], ycols[j - 1]):
            out.append(xcols[i - 1] + ycols[j - 1]); i -= 1; j -= 1
        elif i and f[i][j] == f[i - 1][j] + col(xcols[i - 1], gy):
            out.append(xcols[i - 1] + gy); i -= 1
        else:
            out.append(gx + ycols[j - 1]); j -= 1
    out.reverse()
    return ["".join(c[r] for c in out) for r in range(len(xr) + len(yr))]


def clustal(seqs: list[str], score: Score = dna_score) -> list[str]:
    """Return a multiple alignment of seqs, rows in input order."""
    k = len(seqs)
    if k <= 1:
        return list(seqs)
    d = [[Fraction(0)] * k for _ in range(k)]
    for i in range(k):  # @line L1
        for j in range(i + 1, k):
            _, a, b = nw(seqs[i], seqs[j], score)
            d[i][j] = d[j][i] = identity_distance(a, b)
    unrooted = neighbor_joining(d)  # @line L2
    leaves = list(range(k))
    root, children, up = midpoint_root(unrooted, leaves)  # @line L3
    w = sequence_weights(root, children, up, leaves)  # @line L4
    groups = {}
    for v in leaves:  # @line L5
        groups[v] = ([seqs[v]], [w[v]], [v])

    def post(x):  # @line L6
        if not children[x]:
            return groups[x]
        (ar, aw, ai), (br, bw, bi) = [post(y) for y in children[x]]
        rows = profile_align(ar, aw, br, bw, score)  # @line L7
        return rows, aw + bw, ai + bi

    rows, _, ids = post(root)
    result = [""] * k
    for r, i in zip(rows, ids):
        result[i] = r
    return result  # @line L8


def sp_score(rows: list[str], score: Score = dna_score) -> int:
    """Sum-of-pairs score; gap against gap scores 0."""
    return sum(score(a, b) for i in range(len(rows)) for j in range(i + 1, len(rows))
               for a, b in zip(rows[i], rows[j]))
