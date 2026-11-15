# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wolf-lam-locality-algorithm/. The authors are listed in prov/SBSZSV.jsonl.
"""Wolf and Lam's data locality optimizing algorithm, for small perfect nests.

A nest of depth k has rectangular bounds, a list of constant dependence
distance vectors, and array accesses. An access is (array, H, c): at
iteration i it touches the element H i + c of a row-major array, so the
last subscript walks memory with stride 1.

Reuse is described by vector spaces (Wolf and Lam, PLDI 1991, Section 4):
  self-temporal  R_ST = ker H
  self-spatial   R_SS = ker H_S, where H_S is H with its last row zeroed
  group reuse    two accesses with the same array and H (a uniformly
                 generated set) share data when H r = c1 - c2 for some r
                 in the localized space L (temporal), or the same with
                 H_S and c_S (spatial).
The localized space L is the span of the loops that run inside one tile.
For each candidate set I of loops the cost, in memory accesses per
iteration, is the sum over uniformly generated sets of
  (g_S + (g_T - g_S) / l) / (l^e * s^dim(R_ST n L)),
with e = 0 if R_ST n L = R_SS n L and e = 1 otherwise; l is the number of
elements in a cache line and s the trip count of a localized loop.

Wolf and Lam make I innermost and fully permutable with a heuristic over
skewing, reversal and permutation (SRP). This code instead tries every
signed permutation that puts the loops of I innermost and then skews the
band by the construction of the loop skewing page. With k <= 3 that is a
few dozen candidates, and it finds a band whenever a signed permutation
with I innermost is legal.
"""

from fractions import Fraction
from itertools import combinations, permutations, product


# ---------------------------------------------------------------- linear algebra

def _rref(rows, ncols):
    m = [[Fraction(x) for x in r] for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        p = next((q for q in range(r, len(m)) if m[q][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = 1 / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for q in range(len(m)):
            if q != r and m[q][c] != 0:
                f = m[q][c]
                m[q] = [x - f * y for x, y in zip(m[q], m[r])]
        piv.append(c)
        r += 1
        if r == len(m):
            break
    return m[:r], piv


def rank(vectors, k):
    """Rank of a list of vectors of length k."""
    if not vectors:
        return 0
    return len(_rref(vectors, k)[1])


def nullspace(M, k):
    """A basis of {x in Q^k : M x = 0}."""
    if not M:
        return [tuple(Fraction(int(c == j)) for c in range(k)) for j in range(k)]
    R, piv = _rref(M, k)
    free = [c for c in range(k) if c not in piv]
    basis = []
    for f in free:
        x = [Fraction(0)] * k
        x[f] = Fraction(1)
        for row, p in zip(R, piv):
            x[p] = -row[f]
        basis.append(tuple(x))
    return basis


def mat_vec(M, v):
    return tuple(sum(Fraction(a) * b for a, b in zip(row, v)) for row in M)


def spatial(H):
    """H_S: H with the row of the last (contiguous) subscript set to zero."""
    return [list(r) for r in H[:-1]] + [[0] * len(H[-1])]


def reuse_spaces(H, k):
    """(basis of R_ST, basis of R_SS) for the access matrix H."""
    return nullspace(H, k), nullspace(spatial(H), k)


def unit(j, k):
    return tuple(Fraction(int(c == j)) for c in range(k))


def dim_intersection(A, B, k):
    """dim(span A n span B) = dim A + dim B - dim(A + B)."""
    return rank(A, k) + rank(B, k) - rank(list(A) + list(B), k)


def in_image(H, L, v, k):
    """True when H r = v for some r in span L."""
    cols = [mat_vec(H, b) for b in L]
    n = len(v)
    return rank(cols + [tuple(v)], n) == rank(cols, n) if cols else all(x == 0 for x in v)


# ---------------------------------------------------------------- cost model

def uniformly_generated_sets(accesses):
    """Group accesses by (array, H); each group lists its offset vectors."""
    groups = {}
    for arr, H, c in accesses:
        key = (arr, tuple(tuple(r) for r in H))
        groups.setdefault(key, [])
        if tuple(c) not in groups[key]:
            groups[key].append(tuple(c))
    return groups


def count_classes(H, offsets, L, k):
    """Number of classes of offsets under c1 ~ c2 iff H r = c1 - c2 for some r in L."""
    parent = list(range(len(offsets)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in combinations(range(len(offsets)), 2):
        diff = tuple(x - y for x, y in zip(offsets[a], offsets[b]))
        if in_image(H, L, diff, k):
            parent[find(a)] = find(b)
    return len({find(x) for x in range(len(offsets))})


def set_cost(H, offsets, L, k, line, s, spaces=None):
    """Memory accesses per iteration for one uniformly generated set."""
    R_ST, R_SS = spaces if spaces is not None else reuse_spaces(H, k)
    HS = spatial(H)
    off_s = [tuple(list(c[:-1]) + [0]) for c in offsets]
    g_T = count_classes(H, offsets, L, k)
    g_S = count_classes(HS, off_s, L, k)
    dst = dim_intersection(R_ST, L, k)
    dss = dim_intersection(R_SS, L, k)
    e = 0 if dst == dss else 1
    return (Fraction(g_S) + Fraction(g_T - g_S, line)) / (Fraction(line) ** e * Fraction(s) ** dst)


def nest_cost(accesses, I, k, line=8, s=100):
    """Total cost when the loops in I are localized (L = span of their axes)."""
    L = [unit(j, k) for j in sorted(I)]
    total = Fraction(0)
    for (arr, H), offs in uniformly_generated_sets(accesses).items():
        total += set_cost([list(r) for r in H], offs, L, k, line, s)
    return total


# ---------------------------------------------------------------- legality and the band

def lex_nonneg(v):
    for x in v:
        if x != 0:
            return x > 0
    return True


def make_band(distances, I, k):
    """A unimodular T that runs the loops not in I outside and the loops of I
    as an innermost fully permutable band, or None.

    T = (skew of the band) x (signed permutation). Returns (T, m) with m = |I|.
    """
    I = sorted(I)
    O = [j for j in range(k) if j not in I]
    m = len(I)
    for po in permutations(O):
        for so in product((1, -1), repeat=len(O)):
            outer = [tuple(sg * d[j] for sg, j in zip(so, po)) for d in distances]
            if not all(lex_nonneg(v) for v in outer):
                continue
            free = [d for d, v in zip(distances, outer) if not any(v)]
            for pb in permutations(I):
                for sb in product((1, -1), repeat=m):
                    band = [[sg * d[j] for sg, j in zip(sb, pb)] for d in free]
                    if not all(lex_nonneg(v) and any(v) for v in band):
                        continue
                    # Skew loop by loop: b'_l = b_l + f_l (b'_1 + ... + b'_{l-1}).
                    f = [0] * m
                    cur = [list(v) for v in band]
                    for l in range(1, m):
                        f[l] = max([0] + [-v[l] for v in cur])
                        for v in cur:
                            v[l] = v[l] + f[l] * sum(v[:l])
                    rows = []
                    for sg, j in zip(so, po):
                        rows.append([sg * int(c == j) for c in range(k)])
                    brows = []
                    for l, (sg, j) in enumerate(zip(sb, pb)):
                        r = [sg * int(c == j) for c in range(k)]
                        for q in range(l):
                            r = [x + f[l] * y for x, y in zip(r, brows[q])]
                        brows.append(r)
                    return rows + brows, m
    return None


def transformed(T, d):
    return tuple(sum(a * x for a, x in zip(row, d)) for row in T)


def wolf_lam(accesses, distances, k, line=8, s=100):
    """Choose the localized loops and the transformation.

    Returns a dict with I (the localized loops), cost, T and m (the band size).
    """
    groups = uniformly_generated_sets(accesses)
    spaces = {key: reuse_spaces([list(r) for r in key[1]], k) for key in groups}  # @line L1
    best = None  # @line L2
    subsets = [I for size in range(k + 1) for I in combinations(range(k), size)]
    for I in subsets:  # @line L3
        band = make_band(distances, I, k)  # @line L4
        if band is None:  # @line L5
            continue
        L = [unit(j, k) for j in I]  # @line L6
        cost = sum(
            (set_cost([list(r) for r in key[1]], offs, L, k, line, s, spaces[key]) for key, offs in groups.items()),
            Fraction(0),
        )  # @line L7
        if best is None or cost < best["cost"]:  # @line L8
            best = {"I": I, "cost": cost, "T": band[0], "m": band[1]}
    return best


def tiled_order(points, T, m, B):
    """Iterations in the order of the transformed nest, with the innermost m
    loops tiled by B when m >= 2 (line L9)."""
    k = len(T)

    def key(i):
        y = transformed(T, i)
        outer, band = y[:k - m], y[k - m:]
        tiles = tuple(x // B for x in band) if m >= 2 else ()  # @line L9
        return outer + tiles + band

    return sorted(points, key=key)
