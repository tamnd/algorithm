# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-coffee/. The authors are listed in prov/RYMMF1.jsonl.

"""A small version of T-Coffee (Notredame, Higgins and Heringa 2000).

1. Primary library: for every pair of sequences, one optimal global alignment
   and the best local alignment. Each aligned residue pair gets the percent
   identity of the alignment it comes from; a pair found by both alignments
   gets the sum of the two weights. (T-Coffee uses ClustalW for the global
   alignments and the ten best non-intersecting Lalign local alignments.)
2. Extension: W'(x, y) = W(x, y) + sum over residues z of the other sequences
   of min(W(x, z), W(z, y)).
3. Progressive alignment along a neighbor-joining tree, in which two columns
   score the average extended weight of their residue pairs and gaps cost 0.

A residue is a pair (sequence index, position). Weights are Fractions.
"""

from fractions import Fraction

GAP = "-"


def pair_score(x: str, y: str) -> int:
    """Score of the pairwise alignments that build the library and of the SP check."""
    if x == GAP and y == GAP:
        return 0
    if x == GAP or y == GAP:
        return -2
    return 1 if x == y else -1


def sp_score(rows: list[str]) -> int:
    return sum(pair_score(a, b) for i in range(len(rows)) for j in range(i + 1, len(rows))
               for a, b in zip(rows[i], rows[j]))


def global_pairs(s: str, t: str) -> list[tuple[int, int]]:
    """Matched positions of one optimal global alignment (Needleman-Wunsch)."""
    m, n = len(s), len(t)
    f = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        f[i][0] = -2 * i
    for j in range(1, n + 1):
        f[0][j] = -2 * j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            f[i][j] = max(f[i - 1][j - 1] + pair_score(s[i - 1], t[j - 1]), f[i - 1][j] - 2, f[i][j - 1] - 2)
    out, i, j = [], m, n
    while i and j:
        if f[i][j] == f[i - 1][j - 1] + pair_score(s[i - 1], t[j - 1]):
            out.append((i - 1, j - 1)); i -= 1; j -= 1
        elif f[i][j] == f[i - 1][j] - 2:
            i -= 1
        else:
            j -= 1
    return out[::-1]


def local_pairs(s: str, t: str) -> list[tuple[int, int]]:
    """Matched positions of one best local alignment (Smith-Waterman); empty if no positive score."""
    m, n = len(s), len(t)
    h = [[0] * (n + 1) for _ in range(m + 1)]
    best, bi, bj = 0, 0, 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            h[i][j] = max(0, h[i - 1][j - 1] + pair_score(s[i - 1], t[j - 1]), h[i - 1][j] - 2, h[i][j - 1] - 2)
            if h[i][j] > best:
                best, bi, bj = h[i][j], i, j
    out, i, j = [], bi, bj
    while i and j and h[i][j] > 0:
        if h[i][j] == h[i - 1][j - 1] + pair_score(s[i - 1], t[j - 1]):
            out.append((i - 1, j - 1)); i -= 1; j -= 1
        elif h[i][j] == h[i - 1][j] - 2:
            i -= 1
        else:
            j -= 1
    return out[::-1]


def percent_identity(s: str, t: str, pairs) -> Fraction:
    return Fraction(100 * sum(s[p] == t[q] for p, q in pairs), len(pairs)) if pairs else Fraction(0)


def primary_library(seqs: list[str]) -> dict:
    """W[(i, p), (j, q)] for residues of different sequences, stored in both orders."""
    w = {}
    for i in range(len(seqs)):
        for j in range(i + 1, len(seqs)):
            for pairs in (global_pairs(seqs[i], seqs[j]), local_pairs(seqs[i], seqs[j])):
                pid = percent_identity(seqs[i], seqs[j], pairs)
                for p, q in pairs:
                    x, y = (i, p), (j, q)
                    w[x, y] = w[y, x] = w.get((x, y), 0) + pid
    return w


def extend_library(w: dict, seqs: list[str]) -> dict:
    """W'(x, y) = W(x, y) + sum over z in a third sequence of min(W(x, z), W(z, y))."""
    partners = {}
    for x, z in w:
        partners.setdefault(x, {})[z] = w[x, z]
    ext = {}
    k = len(seqs)
    for i in range(k):
        for j in range(i + 1, k):
            for p in range(len(seqs[i])):
                x = (i, p)
                px = partners.get(x, {})
                for q in range(len(seqs[j])):
                    y = (j, q)
                    py = partners.get(y, {})
                    total = w.get((x, y), 0)
                    for z, wxz in px.items():
                        if z[0] != j and z in py:
                            total += min(wxz, py[z])
                    if total:
                        ext[x, y] = ext[y, x] = total
    return ext


def neighbor_joining_order(d: list[list[Fraction]]):
    """Neighbor joining; returns a rooted binary tree (nested pairs of leaf indices)
    whose root is the last join."""
    nodes = {i: i for i in range(len(d))}
    dist = {(i, j): d[i][j] for i in range(len(d)) for j in range(len(d))}
    nxt = len(d)
    while len(nodes) > 2:
        ids = sorted(nodes)
        r = len(ids)
        tot = {a: sum(dist[a, b] for b in ids if b != a) for a in ids}
        _, a, b = min(((r - 2) * dist[a, b] - tot[a] - tot[b], a, b)
                      for x, a in enumerate(ids) for b in ids[x + 1:])
        for c in ids:
            if c not in (a, b):
                dist[nxt, c] = dist[c, nxt] = (dist[a, c] + dist[b, c] - dist[a, b]) / 2
        dist[nxt, nxt] = 0
        nodes[nxt] = (nodes.pop(a), nodes.pop(b))
        nxt += 1
    a, b = sorted(nodes)
    return (nodes[a], nodes[b])


def group_align(xr: list[str], xi: list[int], yr: list[str], yi: list[int], ext: dict) -> list[str]:
    """Profile DP with column score = average extended weight over residue pairs, gaps 0."""
    m, n = len(xr[0]), len(yr[0])
    pos_x = [[] for _ in range(m)]  # residues of each column of X
    for r, s in zip(xi, xr):
        c = 0
        for p, ch in enumerate(s):
            if ch != GAP:
                pos_x[p].append((r, c)); c += 1
    pos_y = [[] for _ in range(n)]
    for r, s in zip(yi, yr):
        c = 0
        for p, ch in enumerate(s):
            if ch != GAP:
                pos_y[p].append((r, c)); c += 1
    size = len(xr) * len(yr)

    def col(a, b):
        return Fraction(sum(ext.get((x, y), 0) for x in pos_x[a] for y in pos_y[b]), size)  # @line L7

    f = [[Fraction(0)] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            f[i][j] = max(f[i - 1][j - 1] + col(i - 1, j - 1), f[i - 1][j], f[i][j - 1])  # @line L8
    cols, i, j = [], m, n
    while i or j:
        if i and j and f[i][j] == f[i - 1][j - 1] + col(i - 1, j - 1):
            cols.append((i - 1, j - 1)); i -= 1; j -= 1
        elif i and f[i][j] == f[i - 1][j]:
            cols.append((i - 1, None)); i -= 1
        else:
            cols.append((None, j - 1)); j -= 1
    cols.reverse()
    rows = ["".join(GAP if a is None else s[a] for a, _ in cols) for s in xr]
    rows += ["".join(GAP if b is None else s[b] for _, b in cols) for s in yr]
    return rows  # @line L9


def progressive(t, seqs, ext) -> dict[int, str]:
    if isinstance(t, int):
        return {t: seqs[t]}
    a, b = progressive(t[0], seqs, ext), progressive(t[1], seqs, ext)
    ia, ib = sorted(a), sorted(b)
    rows = group_align([a[i] for i in ia], ia, [b[i] for i in ib], ib, ext)
    return dict(zip(ia + ib, rows))


def library_score(rows: list[str], ext: dict) -> Fraction:
    """Sum of extended weights of all residue pairs that share a column."""
    idx = [[None] * len(r) for r in rows]
    for r, s in enumerate(rows):
        c = 0
        for p, ch in enumerate(s):
            if ch != GAP:
                idx[r][p] = c; c += 1
    total = Fraction(0)
    for p in range(len(rows[0]) if rows else 0):
        res = [(r, idx[r][p]) for r in range(len(rows)) if idx[r][p] is not None]
        for x in range(len(res)):
            for y in range(x + 1, len(res)):
                total += ext.get((res[x], res[y]), 0)
    return total


def t_coffee(seqs: list[str]) -> list[str]:
    """Return a multiple alignment of seqs, rows in input order."""
    k = len(seqs)
    if k <= 1:
        return list(seqs)
    w = primary_library(seqs)  # @line L1
    ext = extend_library(w, seqs)  # @line L2
    d = [[Fraction(0)] * k for _ in range(k)]
    for i in range(k):
        for j in range(i + 1, k):
            pairs = global_pairs(seqs[i], seqs[j])
            d[i][j] = d[j][i] = 1 - percent_identity(seqs[i], seqs[j], pairs) / 100  # @line L3
    tree = neighbor_joining_order(d)  # @line L4
    aln = progressive(tree, seqs, ext)  # @line L5
    return [aln[i] for i in range(k)]  # @line L6
