# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/muscle/. The authors are listed in prov/VY1X3J.jsonl.

"""A small version of MUSCLE (Edgar 2004) for DNA.

Stage 1: k-mer distance, UPGMA tree, progressive alignment with the
log-expectation (LE) profile score. Stage 2: Kimura distance from the first
alignment, a second UPGMA tree, and realignment of the subtrees whose leaf
sets changed. Stage 3: refinement by tree-dependent restricted partitioning,
accepting a change only if the sum-of-pairs score improves.

Simplifications: a toy DNA substitution model in place of VTML 240, no
compressed alphabet, and a linear gap penalty scaled by column occupancy in
place of MUSCLE's position-specific affine gaps.
"""

import math
from collections import Counter
from fractions import Fraction

GAP = "-"
ALPHABET = "ACGT"
P_SAME, P_DIFF = 0.16, 0.03  # joint pair probabilities: 4 * 0.16 + 12 * 0.03 = 1
P_BG = 0.25
GAP_PENALTY = 1.5


def pair_score(x: str, y: str) -> float:
    """Log-odds pair score used by the SP objective; gap against gap is 0."""
    if x == GAP and y == GAP:
        return 0.0
    if x == GAP or y == GAP:
        return -GAP_PENALTY
    return math.log((P_SAME if x == y else P_DIFF) / (P_BG * P_BG))


def sp_score(rows: list[str]) -> float:
    return sum(pair_score(a, b) for i in range(len(rows)) for j in range(i + 1, len(rows))
               for a, b in zip(rows[i], rows[j]))


def kmer_distance(x: str, y: str, k: int = 2) -> Fraction:
    """1 - (shared k-mers, counted with multiplicity) / (k-mers in the shorter sequence)."""
    denom = min(len(x), len(y)) - k + 1
    if denom <= 0:
        return Fraction(1)
    cx = Counter(x[i:i + k] for i in range(len(x) - k + 1))
    cy = Counter(y[i:i + k] for i in range(len(y) - k + 1))
    shared = sum(min(c, cy[t]) for t, c in cx.items())
    return 1 - Fraction(shared, denom)


def kimura_distance(a: str, b: str) -> float:
    """Kimura's protein correction -ln(1 - D - D^2/5) of the fraction D of differing
    letter pairs in two aligned rows; capped where the formula breaks down."""
    pairs = [(x, y) for x, y in zip(a, b) if x != GAP and y != GAP]
    if not pairs:
        return 3.0
    d = sum(x != y for x, y in pairs) / len(pairs)
    arg = 1 - d - d * d / 5
    return 3.0 if arg <= math.exp(-3.0) else -math.log(arg)


def upgma(d) -> tuple:
    """UPGMA. A tree is a leaf index or a pair (left, right). Ties: smallest pair of
    cluster ids."""
    k = len(d)
    clusters = {i: (i, 1) for i in range(k)}
    dist = {(i, j): d[i][j] for i in range(k) for j in range(k) if i != j}
    nxt = k
    while len(clusters) > 1:
        ids = sorted(clusters)
        _, a, b = min((dist[a, b], a, b) for x, a in enumerate(ids) for b in ids[x + 1:])
        (ta, na), (tb, nb) = clusters.pop(a), clusters.pop(b)
        for c in clusters:
            v = (dist[a, c] * na + dist[b, c] * nb) / (na + nb)
            dist[nxt, c] = dist[c, nxt] = v
        clusters[nxt] = ((ta, tb), na + nb)
        nxt += 1
    return next(iter(clusters.values()))[0]


def leaves(t) -> frozenset:
    return frozenset([t]) if isinstance(t, int) else leaves(t[0]) | leaves(t[1])


def _freq(col: list[str]):
    n = len(col)
    c = Counter(col)
    return {a: c[a] / n for a in ALPHABET}, c[GAP] / n


def le_score(xc: list[str], yc: list[str]) -> float:
    """Log-expectation score of two columns:
    (1 - f_xG)(1 - f_yG) log sum_ij f_xi f_yj p_ij / (p_i p_j), with f over the
    letters among all rows of each column."""
    fx, gx = _freq(xc)
    fy, gy = _freq(yc)
    if gx == 1 or gy == 1:
        return -GAP_PENALTY * ((1 - gx) + (1 - gy))  # one side is all gaps
    sx, sy = 1 - gx, 1 - gy
    tot = sum((fx[a] / sx) * (fy[b] / sy) * (P_SAME if a == b else P_DIFF) / (P_BG * P_BG)
              for a in ALPHABET for b in ALPHABET)
    return sx * sy * math.log(tot)


def profile_align(xr: list[str], yr: list[str]) -> list[str]:
    """Align two groups of rows as blocks, maximizing the sum of LE column scores."""
    m, n = len(xr[0]), len(yr[0])
    xc = [[r[p] for r in xr] for p in range(m)]
    yc = [[r[p] for r in yr] for p in range(n)]
    gx, gy = [GAP] * len(xr), [GAP] * len(yr)
    f = [[0.0] * (n + 1) for _ in range(m + 1)]
    tb = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        f[i][0], tb[i][0] = f[i - 1][0] + le_score(xc[i - 1], gy), 1
    for j in range(1, n + 1):
        f[0][j], tb[0][j] = f[0][j - 1] + le_score(gx, yc[j - 1]), 2
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            f[i][j], tb[i][j] = max((f[i - 1][j - 1] + le_score(xc[i - 1], yc[j - 1]), 0),
                                    (f[i - 1][j] + le_score(xc[i - 1], gy), -1),
                                    (f[i][j - 1] + le_score(gx, yc[j - 1]), -2))
            tb[i][j] = -tb[i][j]
    out, i, j = [], m, n
    while i or j:
        if tb[i][j] == 0:
            out.append(xc[i - 1] + yc[j - 1]); i -= 1; j -= 1
        elif tb[i][j] == 1:
            out.append(xc[i - 1] + gy); i -= 1
        else:
            out.append(gx + yc[j - 1]); j -= 1
    out.reverse()
    return ["".join(c[r] for c in out) for r in range(len(xr) + len(yr))]


def shape(t):
    """Canonical form of a subtree: children ordered by their smallest leaf."""
    if isinstance(t, int):
        return t
    a, b = shape(t[0]), shape(t[1])
    return (a, b) if min(leaves(t[0])) < min(leaves(t[1])) else (b, a)


def progressive(t, seqs, cache: dict) -> dict[int, str]:
    """Align along tree t. cache maps a subtree shape to an alignment {leaf: row};
    a subtree with the same shape as one aligned before is reused, not realigned."""
    key = shape(t)
    if key in cache:
        return cache[key]
    if isinstance(t, int):
        res = {t: seqs[t]}
    else:
        a = progressive(t[0], seqs, cache)
        b = progressive(t[1], seqs, cache)
        ia, ib = sorted(a), sorted(b)
        rows = profile_align([a[i] for i in ia], [b[i] for i in ib])
        res = dict(zip(ia + ib, rows))
    cache[key] = res
    return res


def drop_gap_columns(rows: list[str]) -> list[str]:
    keep = [p for p in range(len(rows[0])) if any(r[p] != GAP for r in rows)]
    return ["".join(r[p] for p in keep) for r in rows]


def edges_by_depth(t):
    """Leaf sets below each non-root node, deepest first (ties: as found)."""
    out = []

    def walk(x, depth):
        if not isinstance(x, int):
            walk(x[0], depth + 1)
            walk(x[1], depth + 1)
        out.append((depth, leaves(x)))

    walk(t[0], 1)
    walk(t[1], 1)
    out.sort(key=lambda e: -e[0])
    return [s for _, s in out]


def refine(aln: dict[int, str], t, max_passes: int = 8) -> dict[int, str]:
    """Tree-dependent restricted partitioning; accept only if SP improves."""
    ids = sorted(aln)
    if isinstance(t, int):
        return aln
    best = sp_score([aln[i] for i in ids])
    order = edges_by_depth(t)
    for _ in range(max_passes):  # @line L7
        improved = False  # @line L8
        for side in order:  # @line L9
            xi = [i for i in ids if i in side]
            yi = [i for i in ids if i not in side]
            xr = drop_gap_columns([aln[i] for i in xi])  # @line L10
            yr = drop_gap_columns([aln[i] for i in yi])
            new = dict(zip(xi + yi, profile_align(xr, yr)))  # @line L11
            sc = sp_score([new[i] for i in ids])
            if sc > best + 1e-9:  # @line L12
                aln, best, improved = new, sc, True
        if not improved:  # @line L13
            break
    return aln


def muscle(seqs: list[str], max_passes: int = 8) -> list[str]:
    """Return a multiple alignment of DNA sequences (rows in input order)."""
    k = len(seqs)
    if k <= 1:
        return list(seqs)
    d1 = [[kmer_distance(a, b) for b in seqs] for a in seqs]  # @line L1
    tree1 = upgma(d1)  # @line L2
    cache: dict = {}
    msa1 = progressive(tree1, seqs, cache)  # @line L3
    d2 = [[kimura_distance(msa1[i], msa1[j]) for j in range(k)] for i in range(k)]  # @line L4
    tree2 = upgma(d2)  # @line L5
    msa2 = progressive(tree2, seqs, cache)  # @line L6
    final = refine(msa2, tree2, max_passes)
    return [final[i] for i in range(k)]  # @line L14
