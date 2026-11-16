# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/force-closure-test/. The authors are listed in prov/ZZXTNV.jsonl.

"""Force-closure test by a linear program in exact arithmetic.

A wrench is written moment first. A planar wrench is (m_z, f_x, f_y) and a
spatial wrench is (m_x, m_y, m_z, f_x, f_y, f_z). The contact normal points
into the object. Each contact is a pair (p, n) of a point and a unit inward
normal, in the object frame.

The test builds the primitive wrenches (one per edge of each linearized
friction cone), checks that they span the wrench space, and then solves the
linear feasibility problem F k = 0, k >= 1 with a phase-one simplex method
and Bland's rule. All arithmetic is in fractions.Fraction, so the answer is
exact for the given (rational) data. A float input is converted to the exact
rational value of the float.

The module force_closure_test.py (the name that the page uses) re-exports
these functions. The code lives here because tools treat a file whose name
ends in _test.py as a test file.
"""

import math
from fractions import Fraction

FRICTIONLESS = "frictionless"
HARD = "hard"
SOFT = "soft"


def _q(x):
    """Return x as a Fraction, exactly."""
    return x if isinstance(x, Fraction) else Fraction(x)


def _cross3(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def _unit_circle(j, k):
    """Return (cos, sin) of 2 pi j / k, exact at multiples of 90 degrees."""
    if (4 * j) % k == 0:
        quarter = (4 * j // k) % 4
        return [(1, 0), (0, 1), (-1, 0), (0, -1)][quarter]
    angle = 2.0 * math.pi * j / k
    return math.cos(angle), math.sin(angle)


def _tangent_basis(n):
    """Return two tangent vectors t1, t2 with (t1, t2, n) orthonormal."""
    # Cross n with the coordinate axis that is least aligned with it.
    axis = min(range(3), key=lambda i: abs(n[i]))
    e = [0, 0, 0]
    e[axis] = 1
    t1 = _cross3(n, e)
    s = t1[0] * t1[0] + t1[1] * t1[1] + t1[2] * t1[2]
    if s != 1:
        r = math.sqrt(float(s))
        t1 = [float(v) / r for v in t1]
    t2 = _cross3(n, t1)
    return t1, t2


def cone_edges(n, mu, k=4):
    """Edges of the linearized friction cone at a contact with inward normal n.

    In the plane the cone has exactly two edges n + mu t and n - mu t, with t
    the normal turned by +90 degrees, so the cone is exact and k is not used.
    In space the k edges n + mu (cos(2 pi j/k) t1 + sin(2 pi j/k) t2) lie on
    the circular cone, so the pyramid is inside it (an inner approximation).
    With mu = 0 the cone is the single ray n.
    """
    if mu == 0:
        return [list(n)]
    if len(n) == 2:
        t = [-n[1], n[0]]
        return [[n[0] + mu * t[0], n[1] + mu * t[1]],
                [n[0] - mu * t[0], n[1] - mu * t[1]]]
    t1, t2 = _tangent_basis(n)
    edges = []
    for j in range(k):
        c, s = _unit_circle(j, k)
        edges.append([n[i] + mu * (c * t1[i] + s * t2[i]) for i in range(3)])
    return edges


def contact_wrench(p, f, moment=None):
    """Wrench (p x f + moment, f) of a force f applied at the point p."""
    if len(p) == 2:
        return [p[0] * f[1] - p[1] * f[0], f[0], f[1]]
    m = _cross3(p, f)
    if moment is not None:
        m = [m[i] + moment[i] for i in range(3)]
    return m + list(f)


def primitive_wrenches(contacts, mu=0, k=4, model=HARD, gamma=0):
    """Return the list W of primitive wrenches, as lists of Fractions.

    model is FRICTIONLESS, HARD (point contact with friction) or SOFT (soft
    finger, spatial only). A soft finger has the friction cone |f_t| <= mu f_n
    and the torsion limit |m_n| <= gamma f_n; each cone edge appears twice,
    with the moment +gamma n and -gamma n about the normal.
    """
    W = []  # @line L1
    for p, n in contacts:  # @line L2
        if model == FRICTIONLESS:
            edges = [list(n)]
        else:
            edges = cone_edges(n, mu, k)
        for f in edges:  # @line L3
            if model == SOFT:
                for sign in (1, -1):
                    w = contact_wrench(p, f, [sign * gamma * v for v in n])
                    W.append([_q(v) for v in w])  # @line L4
            else:
                W.append([_q(v) for v in contact_wrench(p, f)])  # @line L4
    return W


def rank(rows):
    """Rank of a matrix given as a list of rows, by exact Gaussian elimination."""
    M = [[_q(v) for v in row] for row in rows]
    if not M:
        return 0
    r = 0
    cols = len(M[0])
    for c in range(cols):
        pivot = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if pivot is None:
            continue
        M[r], M[pivot] = M[pivot], M[r]
        for i in range(r + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


def phase_one(A, b):
    """Find y >= 0 with A y = b, or return None if there is none.

    Phase one of the simplex method on a dense tableau, with Bland's rule
    for the entering and the leaving variable, so it always stops.
    """
    m = len(A)
    nv = len(A[0]) if m else 0
    T = []
    for i in range(m):  # @line L10
        row = [_q(v) for v in A[i]] + [_q(b[i])]
        if row[-1] < 0:
            row = [-v for v in row]
        T.append(row)
    for i in range(m):  # @line L11
        T[i] = T[i][:nv] + [Fraction(int(r == i)) for r in range(m)] + [T[i][nv]]
    basis = [nv + i for i in range(m)]
    total = nv + m
    cost = [0] * nv + [1] * m
    while True:  # @line L12
        red = [cost[j] - sum(cost[basis[i]] * T[i][j] for i in range(m))
               for j in range(total)]  # @line L13
        value = sum(T[i][total] for i in range(m) if basis[i] >= nv)
        if value == 0 or all(rc >= 0 for rc in red):  # @line L14
            break
        enter = next(j for j in range(total) if red[j] < 0)  # @line L15
        best = None  # @line L16
        for i in range(m):
            if T[i][enter] > 0:
                ratio = T[i][total] / T[i][enter]
                if best is None or ratio < best[0] or (
                        ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        # The phase-one cost is at least 0, so a negative reduced cost always
        # has a positive entry in its column and best is never None.
        r = best[1]
        piv = T[r][enter]  # @line L17
        T[r] = [v / piv for v in T[r]]
        for i in range(m):
            if i != r and T[i][enter] != 0:
                f = T[i][enter]
                T[i] = [a - f * c for a, c in zip(T[i], T[r])]
        basis[r] = enter
    x = [Fraction(0)] * total  # @line L18
    for i in range(m):
        x[basis[i]] = T[i][total]
    if any(x[nv + i] != 0 for i in range(m)):
        return None
    return x[:nv]


def force_closure_of_wrenches(W):
    """Decide whether the wrenches W positively span the wrench space.

    Returns (True, k) with k a list of Fractions, every k_i >= 1 and
    sum_i k_i W_i = 0, or (False, None).
    """
    if not W:
        return False, None
    d = len(W[0])
    N = len(W)
    F = [[_q(W[j][i]) for j in range(N)] for i in range(d)]  # @line L5
    if rank(F) < d:  # @line L6
        return False, None
    b = [-sum(row) for row in F]
    y = phase_one(F, b)  # @line L7
    if y is None:  # @line L8
        return False, None
    return True, [1 + v for v in y]  # @line L9


def force_closure(contacts, mu=0, k=4, model=HARD, gamma=0):
    """Force-closure test of a grasp on its linearized friction cones.

    contacts is a list of (p, n): the contact point and the unit inward
    normal, with 2 or 3 coordinates. Returns (closed, k) as in
    force_closure_of_wrenches. With model FRICTIONLESS (or mu = 0) the test
    decides first-order form closure.
    """
    W = primitive_wrenches(contacts, mu, k, model, gamma)
    return force_closure_of_wrenches(W)
