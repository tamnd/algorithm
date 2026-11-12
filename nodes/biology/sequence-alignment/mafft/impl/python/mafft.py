# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mafft/. The authors are listed in prov/4TVG52.jsonl.

"""A small version of MAFFT's FFT-NS-2 strategy (Katoh and others 2002) for DNA.

Each alignment column becomes a vector of nucleotide frequencies. The
correlation of two groups at every lag is computed with the FFT; the lags with
the highest peaks are searched for homologous segments with a sliding window;
a dynamic program picks a collinear chain of segments; and the group
alignment is a profile dynamic program that is forced through the center of
each chosen segment. The guide tree comes from shared k-tuples and UPGMA, and
FFT-NS-2 repeats the progressive pass with a tree from the first alignment.

Small sizes: k-tuples of length 2 (MAFFT uses 6), windows of 4 sites (30),
4 peaks (20); threshold 0.7 per site as in the paper. Linear gap penalty, and
the second guide tree comes from percent identity in the first alignment.
"""

import cmath
from collections import Counter
from fractions import Fraction

GAP = "-"
ALPHABET = "ACGT"
WINDOW, THRESHOLD, PEAKS, TUPLE = 4, Fraction(7, 10), 4, 2


def pair_score(x: str, y: str) -> int:
    """Match +1, mismatch -1, letter against gap -2, gap against gap 0."""
    if x == GAP and y == GAP:
        return 0
    if x == GAP or y == GAP:
        return -2
    return 1 if x == y else -1


def sp_score(rows: list[str]) -> int:
    return sum(pair_score(a, b) for i in range(len(rows)) for j in range(i + 1, len(rows))
               for a, b in zip(rows[i], rows[j]))


def fft(a: list[complex], invert: bool = False) -> list[complex]:
    """Iterative radix-2 FFT; len(a) must be a power of two."""
    n = len(a)
    a = list(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= n:
        w = cmath.exp((2j if invert else -2j) * cmath.pi / size)
        for start in range(0, n, size):
            wk = 1
            for t in range(size // 2):
                u, v = a[start + t], a[start + t + size // 2] * wk
                a[start + t], a[start + t + size // 2] = u + v, u - v
                wk *= w
        size *= 2
    if invert:
        a = [x / n for x in a]
    return a


def column_vectors(rows: list[str]) -> list[list[Fraction]]:
    """Frequency of each nucleotide in each column; gaps add nothing."""
    n = len(rows)
    return [[Fraction(sum(r[p] == a for r in rows), n) for a in ALPHABET] for p in range(len(rows[0]))]


def correlation(u: list[list[Fraction]], v: list[list[Fraction]]) -> dict[int, float]:
    """c(lag) = sum over sites n and letters a of u[n][a] * v[n + lag][a], for all lags,
    by FFT in O(N log N)."""
    m, n = len(u), len(v)
    size = 1
    while size < m + n:
        size *= 2
    total = [0j] * size
    for a in range(len(ALPHABET)):
        fu = fft([complex(u[m - 1 - i][a]) if i < m else 0j for i in range(size)])  # reversed
        fv = fft([complex(v[i][a]) if i < n else 0j for i in range(size)])
        total = [t + x * y for t, x, y in zip(total, fu, fv)]
    conv = fft(total, invert=True)
    # conv[m - 1 + lag] = sum_n u[n] . v[n + lag]
    return {lag: conv[m - 1 + lag].real for lag in range(-(m - 1), n)}


def find_segments(u, v, lag: int) -> list[tuple[int, int, int, Fraction]]:
    """Segments (i, j, length, score) on the diagonal j = i + lag, made of the sites
    covered by windows of WINDOW sites whose mean score is at least THRESHOLD."""
    sites = [i for i in range(len(u)) if 0 <= i + lag < len(v)]
    score = {i: sum(x * y for x, y in zip(u[i], v[i + lag])) for i in sites}
    covered = set()
    for s in range(len(sites) - WINDOW + 1):
        win = sites[s:s + WINDOW]
        if sum(score[i] for i in win) >= THRESHOLD * WINDOW:
            covered.update(win)
    segs, run = [], []
    for i in sites + [None]:
        if i is not None and i in covered:
            run.append(i)
        elif run:
            segs.append((run[0], run[0] + lag, len(run), sum(score[x] for x in run)))
            run = []
    return segs


def chain_segments(segs):
    """Collinear chain of segments with the largest total score (no overlap in either
    sequence). Returns the chosen segments in order."""
    segs = sorted(segs)
    best, prev = [], []
    for b, (i, j, ln, sc) in enumerate(segs):
        best.append(sc)
        prev.append(None)
        for a in range(b):
            ia, ja, la, _ = segs[a]
            if ia + la <= i and ja + la <= j and best[a] + sc > best[b]:
                best[b], prev[b] = best[a] + sc, a
    if not segs:
        return []
    b = max(range(len(segs)), key=lambda x: (best[x], -x))
    out = []
    while b is not None:
        out.append(segs[b])
        b = prev[b]
    return out[::-1]


def profile_nw(xr: list[str], yr: list[str]) -> list[str]:
    """Align two groups as blocks; column score = average pair score across groups."""
    m = len(xr[0]) if xr else 0
    n = len(yr[0]) if yr else 0
    na, nb = len(xr), len(yr)
    xc = [[r[p] for r in xr] for p in range(m)]
    yc = [[r[p] for r in yr] for p in range(n)]
    gx, gy = [GAP] * na, [GAP] * nb

    def col(p, q):
        return Fraction(sum(pair_score(a, b) for a in p for b in q), na * nb)

    f = [[Fraction(0)] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        f[i][0] = f[i - 1][0] + col(xc[i - 1], gy)
    for j in range(1, n + 1):
        f[0][j] = f[0][j - 1] + col(gx, yc[j - 1])
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            f[i][j] = max(f[i - 1][j - 1] + col(xc[i - 1], yc[j - 1]),
                          f[i - 1][j] + col(xc[i - 1], gy), f[i][j - 1] + col(gx, yc[j - 1]))
    out, i, j = [], m, n
    while i or j:
        if i and j and f[i][j] == f[i - 1][j - 1] + col(xc[i - 1], yc[j - 1]):
            out.append(xc[i - 1] + yc[j - 1]); i -= 1; j -= 1
        elif i and f[i][j] == f[i - 1][j] + col(xc[i - 1], gy):
            out.append(xc[i - 1] + gy); i -= 1
        else:
            out.append(gx + yc[j - 1]); j -= 1
    out.reverse()
    return ["".join(c[r] for c in out) for r in range(na + nb)]


def anchors_for(xr: list[str], yr: list[str]) -> list[tuple[int, int]]:
    """Column pairs (i, j) that the group alignment must match: segment centers."""
    u, v = column_vectors(xr), column_vectors(yr)
    c = correlation(u, v)  # @line L7
    lags = sorted(c, key=lambda lag: (-round(c[lag], 9), lag))[:PEAKS]
    segs = [s for lag in lags for s in find_segments(u, v, lag)]  # @line L8
    chain = chain_segments(segs)  # @line L9
    return [(i + ln // 2, j + ln // 2) for i, j, ln, _ in chain]  # @line L10


def group_align(xr: list[str], yr: list[str]) -> list[str]:
    """MAFFT-style group-to-group alignment through the anchors."""
    out = [""] * (len(xr) + len(yr))
    pi = pj = 0
    for ai, aj in anchors_for(xr, yr) + [(len(xr[0]), len(yr[0]))]:  # @line L11
        piece = profile_nw([r[pi:ai] for r in xr], [r[pj:aj] for r in yr]) if (ai > pi or aj > pj) else []
        if piece:
            out = [o + p for o, p in zip(out, piece)]
        if ai < len(xr[0]):
            out = [o + c for o, c in zip(out, [r[ai] for r in xr] + [r[aj] for r in yr])]
        pi, pj = ai + 1, aj + 1
    return out  # @line L12


def tuple_distance(x: str, y: str) -> Fraction:
    """1 - T_xy / min(T_xx, T_yy), T = shared k-tuples counted with multiplicity."""
    cx = Counter(x[i:i + TUPLE] for i in range(len(x) - TUPLE + 1))
    cy = Counter(y[i:i + TUPLE] for i in range(len(y) - TUPLE + 1))
    txy = sum(min(c, cy[t]) for t, c in cx.items())
    m = min(sum(cx.values()), sum(cy.values()))
    return Fraction(1) if m == 0 else 1 - Fraction(txy, m)


def identity_distance(a: str, b: str) -> Fraction:
    pairs = [(x, y) for x, y in zip(a, b) if x != GAP and y != GAP]
    return Fraction(1) if not pairs else 1 - Fraction(sum(x == y for x, y in pairs), len(pairs))


def upgma(d):
    """UPGMA. A tree is a leaf index or a pair; ties go to the smallest cluster ids."""
    k = len(d)
    clusters = {i: (i, 1) for i in range(k)}
    dist = {(i, j): d[i][j] for i in range(k) for j in range(k) if i != j}
    nxt = k
    while len(clusters) > 1:
        ids = sorted(clusters)
        _, a, b = min((dist[a, b], a, b) for x, a in enumerate(ids) for b in ids[x + 1:])
        (ta, na), (tb, nb) = clusters.pop(a), clusters.pop(b)
        for c in clusters:
            dist[nxt, c] = dist[c, nxt] = (dist[a, c] * na + dist[b, c] * nb) / (na + nb)
        clusters[nxt] = ((ta, tb), na + nb)
        nxt += 1
    return next(iter(clusters.values()))[0]


def progressive(t, seqs) -> dict[int, str]:
    if isinstance(t, int):
        return {t: seqs[t]}
    a, b = progressive(t[0], seqs), progressive(t[1], seqs)
    ia, ib = sorted(a), sorted(b)
    return dict(zip(ia + ib, group_align([a[i] for i in ia], [b[i] for i in ib])))


def mafft(seqs: list[str]) -> list[str]:
    """FFT-NS-2: return a multiple alignment of DNA sequences, rows in input order."""
    k = len(seqs)
    if k <= 1:
        return list(seqs)
    d = [[tuple_distance(a, b) for b in seqs] for a in seqs]  # @line L1
    tree = upgma(d)  # @line L2
    aln = progressive(tree, seqs)  # @line L3
    d = [[identity_distance(aln[i], aln[j]) for j in range(k)] for i in range(k)]
    tree = upgma(d)  # @line L4
    aln = progressive(tree, seqs)  # @line L5
    return [aln[i] for i in range(k)]  # @line L6
