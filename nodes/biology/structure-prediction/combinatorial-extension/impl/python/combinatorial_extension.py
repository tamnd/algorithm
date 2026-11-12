# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combinatorial-extension/. The authors are listed in prov/J6984A.jsonl.

"""Combinatorial extension (CE), Shindyalov and Bourne (1998), C-alpha only,
distances in angstrom.

An aligned fragment pair (AFP) (i, j) matches residues i .. i+m-1 of A with
j .. j+m-1 of B (m = 8 in the paper). A path is a list of AFPs; the next AFP
starts right after the last one in both chains, or after a gap of at most G
residues in exactly one chain (G = 30). With the paper's distances
  D(p, p)  the mean |dA - dB| over the m*m residue pairs of one AFP   (eq. 7)
  D(p, q)  the mean |dA - dB| over m "independent" pairs of two AFPs (eq. 6)
the path grows one AFP at a time while
  (9)  D(q, q) < D0,
  (10) the mean of D(p, q) over the AFPs p of the path < D1,
  (11) the mean of D over all ordered pairs of the extended path < D1,
with D0 = 3 and D1 = 4. ce uses the paper's "best" strategy: among the
candidates that pass (9) and (10), take the one with the least mean (10),
and stop when (11) fails. Each AFP that passes (9) is tried as a start, and a
start whose longest possible path cannot beat the best path is skipped.

ce_all is the "all" strategy, an exhaustive search over every extension that
passes (9), (10) and (11); its cost is exponential.

The final optimization of the paper (dynamic programming on the superposed
structures) is not part of this file. Standard library only.
"""

import math

Vec = tuple[float, float, float]
Afp = tuple[int, int]


def distance_matrix(pts: list[Vec]) -> list[list[float]]:
    return [[math.dist(p, q) for q in pts] for p in pts]


def d_self(dA, dB, p: Afp, m: int) -> float:
    """Eq. (7): (1/m^2) sum over k, l of |dA(i+k, i+l) - dB(j+k, j+l)|."""
    i, j = p
    return sum(abs(dA[i + k][i + l] - dB[j + k][j + l]) for k in range(m) for l in range(m)) / (m * m)


def d_pair(dA, dB, p: Afp, q: Afp, m: int) -> float:
    """Eq. (6): the two end-to-end pairs and the m - 2 'crossing' pairs, averaged."""
    (pa, pb), (qa, qb) = p, q
    s = abs(dA[pa][qa] - dB[pb][qb]) + abs(dA[pa + m - 1][qa + m - 1] - dB[pb + m - 1][qb + m - 1])
    for k in range(1, m - 1):
        s += abs(dA[pa + k][qa + m - 1 - k] - dB[pb + k][qb + m - 1 - k])
    return s / m


def successors(p: Afp, n_a: int, n_b: int, m: int, gap: int) -> list[Afp]:
    """Path conditions (1) to (5): no gap, or a gap of 1 .. gap residues in exactly one chain."""
    pa, pb = p
    out = []
    for g in range(gap + 1):
        for q in ((pa + m + g, pb + m),) if g == 0 else ((pa + m + g, pb + m), (pa + m, pb + m + g)):
            if q[0] + m <= n_a and q[1] + m <= n_b:
                out.append(q)
    return out


def max_path_length(p: Afp, n_a: int, n_b: int, m: int) -> int:
    """An upper bound on the number of AFPs of any path that starts at p."""
    return 1 + min((n_a - m - p[0]) // m, (n_b - m - p[1]) // m)


def alignment_of(path: list[Afp], m: int) -> list[tuple[int, int]]:
    return [(i + k, j + k) for i, j in path for k in range(m)]


def ce(a: list[Vec], b: list[Vec], m: int = 8, gap: int = 30, d0: float = 3.0,
       d1: float = 4.0) -> list[Afp]:
    """The longest path built by the 'best' strategy; ties keep the first one found."""
    n_a, n_b = len(a), len(b)
    if n_a < m or n_b < m:
        return []
    dA, dB = distance_matrix(a), distance_matrix(b)  # @line L1
    good = {}
    for i in range(n_a - m + 1):  # @line L2
        for j in range(n_b - m + 1):
            s = d_self(dA, dB, (i, j), m)
            if s < d0:  # criterion (9)
                good[(i, j)] = s
    best: list[Afp] = []  # @line L3
    for start in sorted(good):  # @line L4
        if max_path_length(start, n_a, n_b, m) <= len(best):  # @line L5
            continue
        path = [start]  # @line L6
        total = good[start]  # the sum of D over all ordered pairs of the path
        while True:  # @line L7
            cands = []
            for q in successors(path[-1], n_a, n_b, m, gap):  # @line L8
                if q not in good:
                    continue
                cross = sum(d_pair(dA, dB, p, q, m) for p in path)
                if cross / len(path) < d1:  # criterion (10)
                    cands.append((cross / len(path), q, cross))
            if not cands:  # @line L9
                break
            _, q, cross = min(cands)  # @line L10
            new_total = total + 2.0 * cross + good[q]
            if new_total / (len(path) + 1) ** 2 >= d1:  # @line L11
                break
            path.append(q)  # @line L12
            total = new_total
        if len(path) > len(best):  # @line L13
            best = path
    return best  # @line L14


def ce_all(a: list[Vec], b: list[Vec], m: int = 8, gap: int = 30, d0: float = 3.0,
           d1: float = 4.0) -> list[Afp]:
    """The 'all' strategy: the longest path over every sequence of extensions that
    pass (9), (10) and (11); among the longest, the one of least mean (11).
    Exponential time; for small inputs and for tests."""
    n_a, n_b = len(a), len(b)
    if n_a < m or n_b < m:
        return []
    dA, dB = distance_matrix(a), distance_matrix(b)
    good = {(i, j): d_self(dA, dB, (i, j), m) for i in range(n_a - m + 1) for j in range(n_b - m + 1)}
    good = {p: s for p, s in good.items() if s < d0}
    best: list[Afp] = []
    best_key = (0, 0.0)

    def grow(path: list[Afp], total: float) -> None:
        nonlocal best, best_key
        key = (len(path), -total / len(path) ** 2)
        if key > best_key:
            best, best_key = list(path), key
        for q in successors(path[-1], n_a, n_b, m, gap):
            if q not in good:
                continue
            cross = sum(d_pair(dA, dB, p, q, m) for p in path)
            if cross / len(path) >= d1:
                continue
            new_total = total + 2.0 * cross + good[q]
            if new_total / (len(path) + 1) ** 2 >= d1:
                continue
            path.append(q)
            grow(path, new_total)
            path.pop()

    for start in sorted(good):
        grow([start], good[start])
    return best


def rmsd_of_alignment(a: list[Vec], b: list[Vec], pairs: list[tuple[int, int]]) -> float:
    """Least RMSD of the aligned residues (Horn's quaternion method, power iteration on a shifted matrix)."""
    xs = [a[i] for i, _ in pairs]
    ys = [b[j] for _, j in pairs]
    n = len(xs)
    if n == 0:
        return 0.0
    cx = [sum(p[k] for p in xs) / n for k in range(3)]
    cy = [sum(p[k] for p in ys) / n for k in range(3)]
    s = [[0.0] * 3 for _ in range(3)]
    ga = gb = 0.0
    for p, q in zip(xs, ys):
        u = [p[k] - cx[k] for k in range(3)]
        v = [q[k] - cy[k] for k in range(3)]
        ga += sum(c * c for c in u)
        gb += sum(c * c for c in v)
        for r in range(3):
            for c in range(3):
                s[r][c] += u[r] * v[c]
    (sxx, sxy, sxz), (syx, syy, syz), (szx, szy, szz) = s
    nm = [[sxx + syy + szz, syz - szy, szx - sxz, sxy - syx],
          [syz - szy, sxx - syy - szz, sxy + syx, szx + sxz],
          [szx - sxz, sxy + syx, -sxx + syy - szz, syz + szy],
          [sxy - syx, szx + sxz, syz + szy, -sxx - syy + szz]]
    shift = ga + gb + 1.0  # makes every eigenvalue positive, so squaring finds the largest
    mat = [[nm[i][j] + (shift if i == j else 0.0) for j in range(4)] for i in range(4)]
    for _ in range(60):
        mat = [[sum(mat[i][k] * mat[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        big = max(abs(c) for row in mat for c in row)
        mat = [[c / big for c in row] for row in mat]
    col = max(range(4), key=lambda c: sum(mat[r][c] ** 2 for r in range(4)))
    q = [mat[r][col] for r in range(4)]
    norm = math.sqrt(sum(c * c for c in q))
    q = [c / norm for c in q]
    lam = sum(q[i] * nm[i][j] * q[j] for i in range(4) for j in range(4))
    return math.sqrt(max(ga + gb - 2.0 * lam, 0.0) / n)
