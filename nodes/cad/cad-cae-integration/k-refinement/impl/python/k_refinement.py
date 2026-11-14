# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-refinement/. The authors are listed in prov/H90MTM.jsonl.

"""k-refinement of a clamped B-spline curve: raise the degree, then insert knots.

A curve is (t, p, P): a clamped knot vector t (the end values have
multiplicity p + 1, interior values at most p), the degree p and the control
points P, each a tuple of numbers. Use Fraction for exact results.
"""

from fractions import Fraction


def distinct(t):
    """Distinct knot values with their multiplicities, in order."""
    out = []
    for x in t:
        if out and out[-1][0] == x:
            out[-1][1] += 1
        else:
            out.append([x, 1])
    return [(x, m) for x, m in out]


def find_span(t, p, u):
    """Index k with t[k] <= u < t[k+1] and p <= k <= len(t) - p - 2."""
    n = len(t) - p - 2
    if u >= t[n + 1]:
        k = n
        while t[k] == t[k + 1]:
            k -= 1
        return k
    k = p
    while not (t[k] <= u < t[k + 1]):
        k += 1
    return k


def eval_piece(t, p, P, k, u):
    """de Boor's algorithm with the polynomial piece of span k (t[k] < t[k+1])."""
    d = [list(P[j]) for j in range(k - p, k + 1)]
    for r in range(1, p + 1):
        for j in range(p, r - 1, -1):
            i = k - p + j
            a = (u - t[i]) / (t[i + p + 1 - r] - t[i])
            d[j] = [(1 - a) * x + a * y for x, y in zip(d[j - 1], d[j])]
    return tuple(d[p])


def evaluate(t, p, P, u):
    return eval_piece(t, p, P, find_span(t, p, Fraction(u)), Fraction(u))


def insert_knot(t, p, P, x):
    """Boehm's algorithm: insert x once. The curve does not change."""
    k = find_span(t, p, x)
    Q = []
    for i in range(len(P) + 1):
        if i <= k - p:
            Q.append(tuple(P[i]))
        elif i > k:
            Q.append(tuple(P[i - 1]))
        else:
            a = (x - t[i]) / (t[i + p] - t[i])
            Q.append(tuple((1 - a) * u + a * v for u, v in zip(P[i - 1], P[i])))
    return t[: k + 1] + [x] + t[k + 1 :], Q


def insertion_matrix(t, p, t_fine):
    """Matrix A with (control points on t_fine) = A (control points on t)."""
    n = len(t) - p - 1
    extra = list(t_fine)
    for x in t:
        extra.remove(x)
    cols = []
    for j in range(n):
        tt, Q = list(t), [(Fraction(int(i == j)),) for i in range(n)]
        for x in extra:
            tt, Q = insert_knot(tt, p, Q, x)
        cols.append([q[0] for q in Q])
    return [[cols[j][i] for j in range(n)] for i in range(len(cols[0]))]


def solve_exact(A, B):
    """Solve A X = B for a matrix A with full column rank. Raise if no solution."""
    m, n = len(A), len(A[0])
    M = [list(A[i]) + list(B[i]) for i in range(m)]
    piv_rows = []
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if M[i][c] != 0), None)
        if piv is None:
            raise ValueError("matrix has no full column rank")
        M[r], M[piv] = M[piv], M[r]
        f = M[r][c]
        M[r] = [v / f for v in M[r]]
        for i in range(m):
            if i != r and M[i][c] != 0:
                g = M[i][c]
                M[i] = [a - g * b for a, b in zip(M[i], M[r])]
        piv_rows.append(r)
        r += 1
    for i in range(r, m):
        if any(v != 0 for v in M[i][n:]):
            raise ValueError("the data is not in the coarse space")
    return [tuple(M[i][n:]) for i in range(n)]


def elevate_bezier(Q):
    """Raise one Bezier piece of degree p = len(Q) - 1 to degree p + 1."""
    p = len(Q) - 1
    R = [tuple(Q[0])]
    for i in range(1, p + 1):
        a = Fraction(i, p + 1)
        R.append(tuple(a * x + (1 - a) * y for x, y in zip(Q[i - 1], Q[i])))
    R.append(tuple(Q[p]))
    return R


def elevate(t, p, P):
    """Degree elevation: the same curve as a spline of degree p + 1.

    Each distinct knot value gets one more copy, so the smoothness C^(p - m)
    at a knot of multiplicity m is kept.
    """
    tb, Q = list(t), [tuple(q) for q in P]
    for x, m in distinct(t)[1:-1]:  # @line L4
        for _ in range(p - m):
            tb, Q = insert_knot(tb, p, Q, x)
    pieces = len(distinct(t)) - 1
    R = []
    for e in range(pieces):  # @line L5
        piece = elevate_bezier(Q[e * p : e * p + p + 1])
        R.extend(piece if e == 0 else piece[1:])
    t_new = []
    for x, m in distinct(t):  # @line L6
        t_new.extend([x] * (m + 1))
    t_bez = []
    for j, (x, m) in enumerate(distinct(t)):
        end = j == 0 or j == len(distinct(t)) - 1
        t_bez.extend([x] * (p + 2 if end else p + 1))
    A = insertion_matrix(t_new, p + 1, t_bez)
    P_new = solve_exact(A, R)  # @line L7
    return t_new, P_new  # @line L8


def k_refine(t, p, P, r, X):
    """Raise the degree by r, then insert the knots X (each once)."""
    t, P = list(t), [tuple(q) for q in P]
    for _ in range(r):  # @line L1
        t, P = elevate(t, p, P)
        p += 1
    for x in X:  # @line L2
        t, P = insert_knot(t, p, P, Fraction(x))
    return t, p, P  # @line L3


def h_then_p(t, p, P, r, X):
    """The other order: insert the knots X first, then raise the degree by r."""
    t, P = list(t), [tuple(q) for q in P]
    for x in X:
        t, P = insert_knot(t, p, P, Fraction(x))
    for _ in range(r):
        t, P = elevate(t, p, P)
        p += 1
    return t, p, P


def derivative(t, p, P):
    """Control points and knots of the derivative curve, of degree p - 1."""
    D = []
    for i in range(len(P) - 1):
        h = t[i + p + 1] - t[i + 1]
        if h == 0:
            D.append(tuple(0 * x for x in P[i]))
        else:
            D.append(tuple(p * (y - x) / h for x, y in zip(P[i], P[i + 1])))
    return t[1:-1], p - 1, D


def jumps(t, p, P, x, orders):
    """Jump of each derivative order at the interior knot x, right minus left."""
    out = []
    for d in range(max(orders) + 1):
        if d in orders:
            kl = max(k for k in range(len(t) - 1) if t[k] < t[k + 1] and t[k + 1] == x)
            kr = min(k for k in range(len(t) - 1) if t[k] == x and t[k] < t[k + 1])
            left = eval_piece(t, p, P, kl, x)
            right = eval_piece(t, p, P, kr, x)
            out.append(tuple(b - a for a, b in zip(left, right)))
        t, p, P = derivative(t, p, P)
    return out
