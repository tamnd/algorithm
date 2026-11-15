# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-hyperplane-method/. The authors are listed in prov/RCRHT9.jsonl.
"""Lamport's hyperplane method for a perfect loop nest with constant distances.

A loop nest of depth k is given by its iteration space, a list of affine
constraints (a, b) that mean a . i + b >= 0, and by the list of its nonzero
dependence distance vectors. The method finds an integer time function pi
with pi . d >= 1 for every distance d. All iterations i with the same value
t = pi . i form one front; the fronts run in increasing t, and the
iterations of one front can run in parallel.

The code follows the page: time_function builds pi from the innermost
level outward (lines L1 to L7), hyperplane_matrix completes pi to a
unimodular matrix T (line L8), and wavefronts scans the transformed space
with Fourier-Motzkin bounds (lines L9 to L11).
"""

from fractions import Fraction
from itertools import product
from math import ceil, floor


def lex_positive(d):
    """True when the first nonzero entry of d is positive."""
    for x in d:
        if x != 0:
            return x > 0
    return False


def leading_level(d):
    """Index of the first nonzero entry of d."""
    for l, x in enumerate(d):
        if x != 0:
            return l
    raise ValueError("zero vector has no leading level")


def time_function(distances, k=None):
    """Return pi with pi[k-1] = 1, pi[l] >= 0 and pi . d >= 1 for every d.

    Every distance must be lexicographically positive. Level l (from the
    innermost outward) gets the smallest nonnegative pi[l] that makes
    pi . d >= 1 for every d whose first nonzero entry is at l.
    """
    distances = [tuple(d) for d in distances]
    if k is None:
        if not distances:
            raise ValueError("give k when there are no distances")
        k = len(distances[0])
    for d in distances:
        if len(d) != k:
            raise ValueError("distance of the wrong length")
        if not lex_positive(d):
            raise ValueError("distance %r is not lexicographically positive" % (d,))
    pi = [0] * k
    pi[k - 1] = 1  # @line L1
    for l in range(k - 2, -1, -1):  # @line L2
        need = 0  # @line L3
        for d in distances:  # @line L4
            if leading_level(d) != l:
                continue
            rest = sum(pi[m] * d[m] for m in range(l + 1, k))  # @line L5
            need = max(need, ceil(Fraction(1 - rest, d[l])))  # @line L6
        pi[l] = need  # @line L7
    return pi


def check_time_function(pi, distances):
    """True when pi . d >= 1 for every distance d."""
    return all(sum(p * x for p, x in zip(pi, d)) >= 1 for d in distances)


def hyperplane_matrix(pi):
    """Rows pi, e_1, ..., e_{k-1}: unimodular when pi[k-1] = 1."""
    k = len(pi)
    if pi[k - 1] != 1:
        raise ValueError("the last entry of pi must be 1")
    rows = [list(pi)] + [[1 if c == l else 0 for c in range(k)] for l in range(k - 1)]  # @line L8
    return rows


def inverse_map(pi, y):
    """The iteration i with T i = y, for T = hyperplane_matrix(pi)."""
    k = len(pi)
    i = [0] * k
    for l in range(k - 1):
        i[l] = y[l + 1]
    i[k - 1] = y[0] - sum(pi[l] * y[l + 1] for l in range(k - 1))  # @line L11
    return tuple(i)


def box(bounds):
    """Constraints of the box lo_l <= i_l <= hi_l."""
    k = len(bounds)
    cons = []
    for l, (lo, hi) in enumerate(bounds):
        e = [0] * k
        e[l] = 1
        cons.append((tuple(e), -lo))
        cons.append((tuple(-x for x in e), hi))
    return cons


def _norm(cons):
    return [(tuple(Fraction(x) for x in a), Fraction(b)) for a, b in cons]


def _eliminate(cons, v):
    """Fourier-Motzkin: remove variable v from the constraints."""
    pos = [c for c in cons if c[0][v] > 0]
    neg = [c for c in cons if c[0][v] < 0]
    out = [c for c in cons if c[0][v] == 0]
    for ap, bp in pos:
        for an, bn in neg:
            sp, sn = -an[v], ap[v]
            a = tuple(sp * x + sn * y for x, y in zip(ap, an))
            out.append((a, sp * bp + sn * bn))
    seen, res = set(), []
    for c in out:
        if c not in seen:
            seen.add(c)
            res.append(c)
    return res


def scan(constraints, k):
    """All integer points of {y : a . y + b >= 0}, in lexicographic order.

    The space must be bounded. Level v uses the constraints with the
    variables after v eliminated, so its bounds are exact for real points;
    an empty inner range makes the recursion skip the outer value.
    """
    levels = [None] * k
    cur = _norm(constraints)
    for v in range(k - 1, -1, -1):
        levels[v] = [c for c in cur if any(x != 0 for x in c[0][:v + 1]) or c[1] < 0]
        cur = _eliminate(cur, v)
    if any(b < 0 for a, b in cur):
        return
    y = [0] * k

    def rec(v):
        lo, hi = None, None
        for a, b in levels[v]:
            s = b + sum(a[u] * y[u] for u in range(v))
            if a[v] > 0:
                t = ceil(-s / a[v])
                lo = t if lo is None else max(lo, t)
            elif a[v] < 0:
                t = floor(s / -a[v])
                hi = t if hi is None else min(hi, t)
            elif s < 0:
                return
        if lo is None or hi is None:
            raise ValueError("the space is not bounded")
        for x in range(lo, hi + 1):
            y[v] = x
            if v == k - 1:
                yield tuple(y)
            else:
                yield from rec(v + 1)

    yield from rec(0)


def wavefronts(constraints, k, pi):
    """List of (t, front) in increasing t; front lists the iterations with pi . i = t.

    The space {i : a . i + b >= 0} is mapped by T = hyperplane_matrix(pi),
    i = S y, so a constraint becomes (a S) . y + b >= 0. The scan in y
    runs y_1 = t outermost (L9); inside a front, i_1, ..., i_{k-1} are
    the remaining loops (L10) and i_k is computed (L11).
    """
    hyperplane_matrix(pi)
    # Columns of S = T^{-1}: i_l = y_{l+1} for l < k - 1, i_{k-1} = y_0 - sum pi_l y_{l+1}.
    S = [[0] * k for _ in range(k)]
    for l in range(k - 1):
        S[l][l + 1] = 1
    S[k - 1][0] = 1
    for l in range(k - 1):
        S[k - 1][l + 1] = -pi[l]
    ycons = []
    for a, b in constraints:
        ay = tuple(sum(a[r] * S[r][c] for r in range(k)) for c in range(k))
        ycons.append((ay, b))
    fronts = []
    for y in scan(ycons, k):
        i = inverse_map(pi, y)
        if fronts and fronts[-1][0] == y[0]:
            fronts[-1][1].append(i)  # @line L10
        else:
            fronts.append((y[0], [i]))  # @line L9
    return fronts


def fewest_fronts(distances, points, max_coeff=3):
    """Brute-force search over pi in [0, max_coeff]^k with pi . d >= 1.

    Returns (number of fronts, pi) with the fewest distinct values of
    pi . i over the given points. A comparison tool for small nests, not
    part of Lamport's method.
    """
    points = list(points)
    k = len(points[0])
    best = None
    for pi in product(range(max_coeff + 1), repeat=k):
        if not check_time_function(pi, distances):
            continue
        n = len({sum(p * x for p, x in zip(pi, i)) for i in points})
        if best is None or n < best[0]:
            best = (n, list(pi))
    return best
