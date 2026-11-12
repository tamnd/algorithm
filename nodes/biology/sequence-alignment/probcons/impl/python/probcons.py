# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probcons/. The authors are listed in prov/VPNKKD.jsonl.

"""A small version of ProbCons (Do, Mahabhashyam, Brudno and Batzoglou 2005) for DNA.

1. Posterior probabilities P_xy(i, j) that residue i of x is aligned with
   residue j of y, by forward-backward on a three-state pair-HMM.
2. Expected accuracy E(x, y): the maximum expected accuracy (MEA) score of the
   pair divided by the length of the shorter sequence.
3. Probabilistic consistency, applied twice:
   P'_xy = (1 / k) * sum over all sequences z of P_xz P_zy, with P_xx = I.
4. Guide tree: merge the two clusters of highest E;
   E(xy, z) = E(x, y) * (E(x, z) + E(y, z)) / 2.
5. Progressive alignment: two columns score the sum of P'_xy(i, j) over their
   residue pairs, and gaps score 0.
6. Iterative refinement: split the rows at random into two groups and realign.

The pair-HMM parameters below are fixed; ProbCons trains its own by EM.
"""

import random

GAP = "-"
DELTA, EPS = 0.2, 0.4  # gap open and gap extend probabilities
P_SAME, P_DIFF, Q = 0.2, 0.2 / 12, 0.25  # match emissions and insert emission
TOL = 1e-12


def pair_score(x: str, y: str) -> int:
    """Score for the SP check: match +1, mismatch -1, letter against gap -2, gap-gap 0."""
    if x == GAP and y == GAP:
        return 0
    if x == GAP or y == GAP:
        return -2
    return 1 if x == y else -1


def sp_score(rows: list[str]) -> int:
    return sum(pair_score(a, b) for i in range(len(rows)) for j in range(i + 1, len(rows))
               for a, b in zip(rows[i], rows[j]))


def emit(a: str, b: str) -> float:
    return P_SAME if a == b else P_DIFF


# transition probabilities t[from][to] over states 0 = M, 1 = X (gap in y), 2 = Y (gap in x)
TRANS = [[1 - 2 * DELTA, DELTA, DELTA], [1 - EPS, EPS, 0.0], [1 - EPS, 0.0, EPS]]


def posteriors(x: str, y: str) -> list[list[float]]:
    """P[i][j] = probability that x[i] and y[j] are aligned, under the pair-HMM,
    by the forward and backward algorithms. Paths start in M at (0, 0)."""
    m, n = len(x), len(y)
    f = [[[0.0] * 3 for _ in range(n + 1)] for _ in range(m + 1)]
    f[0][0][0] = 1.0
    for i in range(m + 1):
        for j in range(n + 1):
            if i and j:
                f[i][j][0] = emit(x[i - 1], y[j - 1]) * sum(f[i - 1][j - 1][s] * TRANS[s][0] for s in range(3))
            if i:
                f[i][j][1] = Q * sum(f[i - 1][j][s] * TRANS[s][1] for s in range(3))
            if j:
                f[i][j][2] = Q * sum(f[i][j - 1][s] * TRANS[s][2] for s in range(3))
    z = sum(f[m][n])
    b = [[[0.0] * 3 for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(m, -1, -1):
        for j in range(n, -1, -1):
            for s in range(3):
                if i == m and j == n:
                    b[i][j][s] = 1.0
                    continue
                v = 0.0
                if i < m and j < n:
                    v += TRANS[s][0] * emit(x[i], y[j]) * b[i + 1][j + 1][0]
                if i < m:
                    v += TRANS[s][1] * Q * b[i + 1][j][1]
                if j < n:
                    v += TRANS[s][2] * Q * b[i][j + 1][2]
                b[i][j][s] = v
    return [[f[i][j][0] * b[i][j][0] / z for j in range(1, n + 1)] for i in range(1, m + 1)]


def transpose(p: list[list[float]], m: int, n: int) -> list[list[float]]:
    """The n by m transpose of an m by n matrix (works when m or n is 0)."""
    return [[p[i][j] for i in range(m)] for j in range(n)]


def mea_score(p: list[list[float]], m: int, n: int) -> float:
    """Largest sum of p[i][j] over the matched pairs of an alignment (gaps score 0)."""
    f = [[0.0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            f[i][j] = max(f[i - 1][j - 1] + p[i - 1][j - 1], f[i - 1][j], f[i][j - 1])
    return f[m][n]


def consistency(post: dict, seqs: list[str]) -> dict:
    """One pass: P'_xy = (1/k) sum_z P_xz P_zy, z over all sequences, with P_xx = identity."""
    k = len(seqs)

    def mat(x, z):
        if x == z:
            return [[1.0 if i == j else 0.0 for j in range(len(seqs[x]))] for i in range(len(seqs[x]))]
        return post[x, z]

    new = {}
    for x in range(k):
        for y in range(x + 1, k):
            m, n = len(seqs[x]), len(seqs[y])
            acc = [[0.0] * n for _ in range(m)]
            for z in range(k):
                a, b = mat(x, z), mat(z, y)
                for i in range(m):
                    for t in range(len(seqs[z])):
                        if a[i][t]:
                            row, bt = acc[i], b[t]
                            for j in range(n):
                                row[j] += a[i][t] * bt[j]
            new[x, y] = [[v / k for v in r] for r in acc]
            new[y, x] = transpose(new[x, y], m, n)
    return new


def guide_tree(e: dict, k: int):
    """Merge the two clusters with the highest expected accuracy;
    E(xy, z) = E(x, y) * (E(x, z) + E(y, z)) / 2. Ties go to the smallest ids."""
    clusters = {i: i for i in range(k)}
    sim = dict(e)
    nxt = k
    while len(clusters) > 1:
        ids = sorted(clusters)
        _, a, b = max((sim[a, b], -a, -b) for x, a in enumerate(ids) for b in ids[x + 1:])
        a, b = -a, -b
        for c in ids:
            if c not in (a, b):
                sim[nxt, c] = sim[c, nxt] = sim[a, b] * (sim[a, c] + sim[b, c]) / 2
        clusters[nxt] = (clusters.pop(a), clusters.pop(b))
        nxt += 1
    return next(iter(clusters.values()))


def residues(row: str) -> list:
    """For each column, the position of the residue of this row, or None for a gap."""
    out, c = [], 0
    for ch in row:
        if ch == GAP:
            out.append(None)
        else:
            out.append(c)
            c += 1
    return out


def group_align(xr, xi, yr, yi, post) -> list[str]:
    """Profile MEA: two columns score sum of P_xy(i, j) over their residue pairs; gaps 0."""
    m, n = len(xr[0]), len(yr[0])
    rx = [residues(r) for r in xr]
    ry = [residues(r) for r in yr]

    def col(a, b):
        return sum(post[s, t][px[a]][py[b]] for s, px in zip(xi, rx) if px[a] is not None
                   for t, py in zip(yi, ry) if py[b] is not None)

    f = [[0.0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            f[i][j] = max(f[i - 1][j - 1] + col(i - 1, j - 1), f[i - 1][j], f[i][j - 1])
    cols, i, j = [], m, n
    while i or j:
        if i and j and abs(f[i][j] - (f[i - 1][j - 1] + col(i - 1, j - 1))) < TOL:
            cols.append((i - 1, j - 1)); i -= 1; j -= 1
        elif i and abs(f[i][j] - f[i - 1][j]) < TOL:
            cols.append((i - 1, None)); i -= 1
        else:
            cols.append((None, j - 1)); j -= 1
    cols.reverse()
    return ([("".join(GAP if a is None else r[a] for a, _ in cols)) for r in xr]
            + [("".join(GAP if b is None else r[b] for _, b in cols)) for r in yr])


def expected_score(rows: list[str], post: dict) -> float:
    """Sum over row pairs and columns of the posterior of the residue pair in the column."""
    res = [residues(r) for r in rows]
    total = 0.0
    for s in range(len(rows)):
        for t in range(s + 1, len(rows)):
            for a, b in zip(res[s], res[t]):
                if a is not None and b is not None:
                    total += post[s, t][a][b]
    return total


def drop_gap_columns(rows: list[str]) -> list[str]:
    keep = [p for p in range(len(rows[0])) if any(r[p] != GAP for r in rows)] if rows else []
    return ["".join(r[p] for p in keep) for r in rows]


def progressive(t, seqs, post) -> dict[int, str]:
    if isinstance(t, int):
        return {t: seqs[t]}
    a, b = progressive(t[0], seqs, post), progressive(t[1], seqs, post)
    ia, ib = sorted(a), sorted(b)
    return dict(zip(ia + ib, group_align([a[i] for i in ia], ia, [b[i] for i in ib], ib, post)))


def refine(aln: dict[int, str], post: dict, rounds: int, rng: random.Random) -> dict[int, str]:
    ids = sorted(aln)
    for _ in range(rounds):  # @line L6
        side = [rng.random() < 0.5 for _ in ids]
        if all(side) or not any(side):
            continue
        ia = [i for i, s in zip(ids, side) if s]
        ib = [i for i, s in zip(ids, side) if not s]
        xa = drop_gap_columns([aln[i] for i in ia])  # @line L7
        xb = drop_gap_columns([aln[i] for i in ib])
        aln = dict(zip(ia + ib, group_align(xa, ia, xb, ib, post)))  # @line L8
    return aln


def probcons(seqs: list[str], reps: int = 2, rounds: int = 100, seed: int = 0) -> list[str]:
    """Return a multiple alignment of DNA sequences, rows in input order."""
    k = len(seqs)
    if k <= 1:
        return list(seqs)
    post = {}
    for x in range(k):
        for y in range(x + 1, k):
            post[x, y] = posteriors(seqs[x], seqs[y])  # @line L1
            post[y, x] = transpose(post[x, y], len(seqs[x]), len(seqs[y]))
    e = {}
    for x in range(k):
        for y in range(x + 1, k):
            short = min(len(seqs[x]), len(seqs[y]))
            e[x, y] = e[y, x] = mea_score(post[x, y], len(seqs[x]), len(seqs[y])) / short if short else 0.0  # @line L2
    for _ in range(reps):
        post = consistency(post, seqs)  # @line L3
    tree = guide_tree(e, k)  # @line L4
    aln = progressive(tree, seqs, post)  # @line L5
    aln = refine(aln, post, rounds, random.Random(seed))
    return [aln[i] for i in range(k)]  # @line L9
