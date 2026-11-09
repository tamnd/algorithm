# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lenstra-algorithm/. The authors are listed in prov/RQXSN0.jsonl.

import itertools
import math
from collections.abc import Sequence
from fractions import Fraction

Num = int | Fraction
Vec = list[Fraction]
Mat = list[list[Fraction]]


def dot(u: Sequence[Num], v: Sequence[Num]) -> Fraction:
    return sum((Fraction(p) * q for p, q in zip(u, v)), Fraction(0))


def solve(rows: Sequence[Sequence[Num]], rhs: Sequence[Num]) -> Vec | None:
    """Solve a square linear system exactly; None if it is singular."""
    n = len(rows)
    m = [[Fraction(v) for v in r] + [Fraction(t)] for r, t in zip(rows, rhs)]
    for col in range(n):
        piv = next((i for i in range(col, n) if m[i][col] != 0), None)
        if piv is None:
            return None
        m[col], m[piv] = m[piv], m[col]
        for i in range(n):
            if i != col and m[i][col] != 0:
                f = m[i][col] / m[col][col]
                m[i] = [x - f * y for x, y in zip(m[i], m[col])]
    return [m[i][n] / m[i][i] for i in range(n)]


def det(mat: Sequence[Sequence[Num]]) -> Fraction:
    n = len(mat)
    m = [[Fraction(v) for v in r] for r in mat]
    d = Fraction(1)
    for col in range(n):
        piv = next((i for i in range(col, n) if m[i][col] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            d = -d
        d *= m[col][col]
        for i in range(col + 1, n):
            f = m[i][col] / m[col][col]
            m[i] = [x - f * y for x, y in zip(m[i], m[col])]
    return d


def inverse(mat: Sequence[Sequence[Num]]) -> Mat:
    n = len(mat)
    cols = [solve(mat, [int(i == j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def vertices(a: Sequence[Sequence[Num]], b: Sequence[Num], n: int) -> list[tuple[Fraction, ...]]:
    """All vertices of P = {x : a x <= b}, by trying every set of n rows."""
    found = set()
    for rows in itertools.combinations(range(len(a)), n):
        x = solve([a[i] for i in rows], [b[i] for i in rows])
        if x is not None and all(dot(a[i], x) <= b[i] for i in range(len(a))):
            found.add(tuple(x))
    return sorted(found)


def normal_vector(vecs: Sequence[Sequence[Fraction]], n: int) -> Vec | None:
    """A nonzero vector orthogonal to all vecs, or None if they span Q^n."""
    rows = [list(v) for v in vecs if any(v)]
    pivots: list[int] = []
    r = 0
    for col in range(n):
        piv = next((i for i in range(r, len(rows)) if rows[i][col] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        rows[r] = [x / rows[r][col] for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        pivots.append(col)
        r += 1
    free = next((j for j in range(n) if j not in pivots), None)
    if free is None:
        return None
    d = [Fraction(0)] * n
    d[free] = Fraction(1)
    for i, col in enumerate(pivots):
        d[col] = -rows[i][free]
    return d


def primitive(d: Sequence[Fraction]) -> list[int]:
    """Scale a nonzero rational vector to an integer vector with gcd 1."""
    lcm = 1
    for v in d:
        lcm = lcm * v.denominator // math.gcd(lcm, v.denominator)
    z = [int(v * lcm) for v in d]
    g = 0
    for v in z:
        g = math.gcd(g, v)
    return [v // g for v in z]


def to_first_unit(d: Sequence[int]) -> list[list[int]]:
    """A unimodular integer matrix W with d^T W = e_1^T, for a primitive d."""
    n = len(d)
    w = [[int(i == j) for j in range(n)] for i in range(n)]
    r = list(d)
    for j in range(1, n):
        a0, aj = r[0], r[j]
        if aj == 0:
            continue
        # extended Euclid: p a0 + q aj = g
        old_r, cur_r, old_s, cur_s, old_t, cur_t = a0, aj, 1, 0, 0, 1
        while cur_r != 0:
            k = old_r // cur_r
            old_r, cur_r = cur_r, old_r - k * cur_r
            old_s, cur_s = cur_s, old_s - k * cur_s
            old_t, cur_t = cur_t, old_t - k * cur_t
        g, p, q = old_r, old_s, old_t
        for i in range(n):
            c0, cj = w[i][0], w[i][j]
            w[i][0], w[i][j] = p * c0 + q * cj, (-aj // g) * c0 + (a0 // g) * cj
        r[0], r[j] = g, 0
    if r[0] < 0:
        for i in range(n):
            w[i][0] = -w[i][0]
    return w


def gso(basis: Sequence[Sequence[int]], q: Mat) -> tuple[Mat, Vec]:
    """Gram-Schmidt coefficients mu and squared lengths of b_i*, in the form q."""
    n = len(basis)

    def ip(u, v):
        return dot(u, [dot(row, v) for row in q])

    star: list[Vec] = []
    mu = [[Fraction(0)] * n for _ in range(n)]
    norms: Vec = []
    for i in range(n):
        v = [Fraction(t) for t in basis[i]]
        for j in range(i):
            mu[i][j] = ip(basis[i], star[j]) / norms[j]
            v = [x - mu[i][j] * y for x, y in zip(v, star[j])]
        star.append(v)
        norms.append(ip(v, v))
    return mu, norms


def lll(basis: list[list[int]], q: Mat) -> list[list[int]]:
    """LLL reduction (delta = 3/4) of an integer basis in the form x^T q y."""
    b = [list(v) for v in basis]
    n = len(b)
    k = 1
    while k < n:
        mu, _ = gso(b, q)
        for j in range(k - 1, -1, -1):
            r = round(mu[k][j])
            if r != 0:
                b[k] = [x - r * y for x, y in zip(b[k], b[j])]
                mu, _ = gso(b, q)
        mu, norms = gso(b, q)
        if norms[k] >= (Fraction(3, 4) - mu[k][k - 1] ** 2) * norms[k - 1]:
            k += 1
        else:
            b[k], b[k - 1] = b[k - 1], b[k]
            k = max(k - 1, 1)
    return b


def nearest_plane(basis: Sequence[Sequence[int]], q: Mat, target: Sequence[Fraction]) -> list[int]:
    """Babai's nearest plane: an integer point y with |y - target|^2 <= sum |b_i*|^2 / 4."""
    n = len(basis)
    mu, norms = gso(basis, q)
    star: list[Vec] = []
    for i in range(n):
        v = [Fraction(t) for t in basis[i]]
        for j in range(i):
            v = [x - mu[i][j] * y for x, y in zip(v, star[j])]
        star.append(v)
    t = [Fraction(v) for v in target]
    y = [0] * len(target)
    for i in range(n - 1, -1, -1):
        k = round(dot(t, [dot(row, star[i]) for row in q]) / norms[i])
        t = [x - k * z for x, z in zip(t, basis[i])]
        y = [x + k * z for x, z in zip(y, basis[i])]
    return y


def feasible_point(
    a: Sequence[Sequence[Num]], b: Sequence[Num], trace: list | None = None
) -> list[int] | None:
    """An integer point of the bounded polyhedron {x : a x <= b}, or None."""
    n = len(a[0]) if a else 0
    if n == 0:  # @line L1
        return [] if all(t >= 0 for t in b) else None
    vs = vertices(a, b, n)  # @line L2
    if not vs:
        return None
    diffs = [[x - y for x, y in zip(v, vs[0])] for v in vs[1:]]
    d_rat = normal_vector(diffs, n)  # @line L3
    if d_rat is not None:
        d = primitive(d_rat)
        level = dot(d, vs[0])
        if trace is not None:
            trace.append(("flat", n, tuple(d), level))
        if level.denominator != 1:
            return None
        return slice_and_recurse(a, b, d, [int(level)], trace)
    simplex = max(itertools.combinations(vs, n + 1), key=lambda s: abs(det([[x - y for x, y in zip(v, s[0])] for v in s[1:]])))  # @line L4
    v0 = simplex[0]
    cols = [[x - y for x, y in zip(v, v0)] for v in simplex[1:]]
    vmat = [[cols[j][i] for j in range(n)] for i in range(n)]
    t = inverse(vmat)
    g = [[Fraction(1) if i == j else Fraction(1, 2) for j in range(n)] for i in range(n)]
    tg = [[dot([t[k][i] for k in range(n)], [g[k][j] for k in range(n)]) for j in range(n)] for i in range(n)]
    q = [[dot(tg[i], [t[k][j] for k in range(n)]) for j in range(n)] for i in range(n)]  # @line L5
    center = [sum((v[i] for v in simplex), Fraction(0)) / (n + 1) for i in range(n)]
    basis = lll([[int(i == j) for j in range(n)] for i in range(n)], q)  # @line L6
    y = nearest_plane(basis, q, center)  # @line L7
    if all(dot(row, y) <= bi for row, bi in zip(a, b)):  # @line L8
        if trace is not None:
            trace.append(("round", n, tuple(y)))
        return y
    binv = inverse([[basis[j][i] for j in range(n)] for i in range(n)])  # @line L9
    d = [int(v) for v in binv[n - 1]]
    values = [dot(d, v) for v in vs]
    lo, hi = math.ceil(min(values)), math.floor(max(values))
    if trace is not None:
        trace.append(("branch", n, tuple(d), lo, hi))
    return slice_and_recurse(a, b, d, range(lo, hi + 1), trace)  # @line L10


def slice_and_recurse(a, b, d: list[int], levels, trace) -> list[int] | None:
    """Try each hyperplane d x = k, in one dimension less."""
    n = len(d)
    w = to_first_unit(d)
    aw = [[sum(Fraction(row[i]) * w[i][j] for i in range(n)) for j in range(n)] for row in a]
    for k in levels:  # @line L11
        sub_a = [row[1:] for row in aw]
        sub_b = [Fraction(bi) - row[0] * k for row, bi in zip(aw, b)]
        z = feasible_point(sub_a, sub_b, trace)
        if z is not None:
            full = [k] + z
            return [sum(w[i][j] * full[j] for j in range(n)) for i in range(n)]
    return None  # @line L12


def lenstra_maximize(
    c: Sequence[int],
    a: Sequence[Sequence[Num]],
    b: Sequence[Num],
    box: Sequence[tuple[int, int]],
) -> tuple[str, list[int] | None, int | None]:
    """Maximize c x over integer x with a x <= b and box[j][0] <= x_j <= box[j][1].

    The box makes the polyhedron bounded. Returns ("optimal", x, value) or
    ("infeasible", None, None).
    """
    n = len(c)
    rows = [list(r) for r in a]
    rhs = [Fraction(t) for t in b]
    for j, (lo, hi) in enumerate(box):
        rows += [[int(k == j) for k in range(n)], [-int(k == j) for k in range(n)]]
        rhs += [Fraction(hi), Fraction(-lo)]
    x = feasible_point(rows, rhs)
    if x is None:
        return "infeasible", None, None
    if not any(c):
        return "optimal", x, 0
    top = math.floor(max(dot(c, v) for v in vertices(rows, rhs, n)))
    low = int(dot(c, x))
    while low < top:
        mid = (low + top + 1) // 2
        y = feasible_point(rows + [[-v for v in c]], rhs + [Fraction(-mid)])
        if y is None:
            top = mid - 1
        else:
            x, low = y, int(dot(c, y))
    return "optimal", x, low
