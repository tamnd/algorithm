# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stewart-trinkle-time-stepping/. The authors are listed in prov/EWJYN8.jsonl.
"""Stewart-Trinkle time stepping for one planar rigid body above the ground line y = 0.

The body has the generalized coordinates q = (x, y, theta): the position of its
center of mass in meters and its angle in radians. Its velocity is
v = (x', y', theta'). Contact points are given in body coordinates. Each contact
has a normal impulse c_n, two friction impulses beta (along +x and -x, so the
planar friction cone has k = 2 edges) and a slack lambda. One step solves one
linear complementarity problem (LCP) in these impulses with Lemke's method.
"""

import math
from itertools import product

PIVOT_TOL = 1e-12


def lemke(A, b, max_pivots=500):
    """Solve the LCP: find z >= 0 with w = A z + b >= 0 and z . w = 0.

    Lemke's complementary pivoting method with the covering vector of ones and
    the lexicographic ratio test. Returns z, or None when the method ends on a
    secondary ray (then it gives no solution).
    """
    m = len(b)
    if all(bi >= 0.0 for bi in b):  # @line L11
        return [0.0] * m
    # Tableau of w - A z - e z0 = b. Columns: w_0..w_(m-1), z_0..z_(m-1), z0, rhs.
    cols = 2 * m + 2
    T = []
    for i in range(m):  # @line L12
        row = [0.0] * cols
        row[i] = 1.0
        for j in range(m):
            row[m + j] = -A[i][j]
        row[2 * m] = -1.0
        row[2 * m + 1] = float(b[i])
        T.append(row)
    basis = list(range(m))  # basic variable of each row: index into the columns
    z0 = 2 * m
    # The first pivot: z0 enters, the row with the smallest b leaves.
    # Among ties, the largest index keeps the tableau lexicographically positive.
    r = 0
    for i in range(m):  # @line L13
        if b[i] <= b[r]:
            r = i
    entering = z0
    for _ in range(max_pivots):  # @line L14
        _pivot(T, r, entering)  # @line L15
        leaving = basis[r]
        basis[r] = entering
        if leaving == z0:  # @line L16
            break
        entering = leaving + m if leaving < m else leaving - m  # @line L17
        r = _lex_ratio_row(T, entering, m)  # @line L18
        if r is None:  # @line L19
            return None
    else:
        return None
    z = [0.0] * m
    for i, var in enumerate(basis):  # @line L20
        if m <= var < 2 * m:
            z[var - m] = max(T[i][-1], 0.0)
    if z0 in basis and T[basis.index(z0)][-1] > 1e-9:
        return None
    return z


def _pivot(T, r, c):
    """Make column c a unit column with its 1 in row r."""
    p = T[r][c]
    T[r] = [t / p for t in T[r]]
    for i in range(len(T)):
        if i != r:
            f = T[i][c]
            if f != 0.0:
                Ti, Tr = T[i], T[r]
                T[i] = [a - f * bb for a, bb in zip(Ti, Tr)]


def _lex_ratio_row(T, c, m):
    """The leaving row for the entering column c, by the lexicographic minimum ratio test.

    The rows compete on (rhs, B^-1 row) / T[i][c]; the columns of the w variables
    hold B^-1. Returns None when no entry of column c is positive (a ray).
    """
    best, best_key = None, None
    for i in range(len(T)):
        a = T[i][c]
        if a > PIVOT_TOL:
            key = [T[i][-1] / a] + [T[i][j] / a for j in range(m)]
            if best is None or _lex_less(key, best_key):
                best, best_key = i, key
    return best


def _lex_less(u, v, tol=1e-11):
    for a, bb in zip(u, v):
        if a < bb - tol * (1.0 + abs(bb)):
            return True
        if a > bb + tol * (1.0 + abs(bb)):
            return False
    return False


class PlanarBody:
    """A rigid body in the plane: mass m (kg), inertia I about the center of mass
    (kg m^2), friction coefficient mu, and contact points in body coordinates (m)."""

    def __init__(self, m, I, mu, points):
        self.m, self.I, self.mu = m, I, mu
        self.points = [tuple(p) for p in points]

    def minv(self):
        return [1.0 / self.m, 1.0 / self.m, 1.0 / self.I]


def contact_data(q, p):
    """Gap phi, normal row n and tangent row d of the body point p at the configuration q.

    phi = y + r_y is the height of the point. n = d phi / dq = (0, 1, r_x).
    d = (1, 0, -r_y) maps v to the x velocity of the point.
    """
    c, s = math.cos(q[2]), math.sin(q[2])
    rx = c * p[0] - s * p[1]
    ry = s * p[0] + c * p[1]
    return q[1] + ry, [0.0, 1.0, rx], [1.0, 0.0, -ry]


def build_lcp(body, q, v, h, f_ext, eps):
    """Form the LCP of one step. Returns (A, b, v_star, cols, phis) where cols holds
    the generalized directions of the impulse variables (normals, then friction edges)."""
    minv = body.minv()
    v_star = [v[i] + h * minv[i] * f_ext[i] for i in range(3)]  # @line L2
    N, D, phis = [], [], []
    for p in body.points:  # @line L3
        phi, n, d = contact_data(q, p)
        if phi <= eps:
            N.append(n)
            phis.append(phi)
            D.append(d)
            D.append([-x for x in d])
    c = len(N)
    if c == 0:
        return None, None, v_star, [], []
    G = N + D  # the 3c directions of c_n and beta, as rows

    def ip(a, bb):  # a^T M^-1 b with a diagonal M
        return sum(a[i] * minv[i] * bb[i] for i in range(3))

    size = 4 * c
    A = [[0.0] * size for _ in range(size)]
    for i in range(3 * c):  # @line L4
        for j in range(3 * c):
            A[i][j] = ip(G[i], G[j])
    for i in range(c):  # @line L5
        A[c + 2 * i][3 * c + i] = 1.0  # E
        A[c + 2 * i + 1][3 * c + i] = 1.0
        A[3 * c + i][i] = body.mu  # U
        A[3 * c + i][c + 2 * i] = -1.0  # -E^T
        A[3 * c + i][c + 2 * i + 1] = -1.0
    b = [0.0] * size
    for i in range(c):  # @line L6
        b[i] = sum(N[i][k] * v_star[k] for k in range(3)) + phis[i] / h
    for j in range(2 * c):
        b[c + j] = sum(D[j][k] * v_star[k] for k in range(3))
    return A, b, v_star, G, phis


def velocity_from_impulses(body, v_star, G, z):
    """v+ = v* + M^-1 (N c_n + D beta)."""
    minv = body.minv()
    P = [0.0, 0.0, 0.0]
    for i, g in enumerate(G):
        for k in range(3):
            P[k] += g[k] * z[i]
    return [v_star[k] + minv[k] * P[k] for k in range(3)], P


def step(body, q, v, h, g=9.81, f_ext=None, eps=0.01):
    """One step of length h. f_ext is the applied generalized force (F_x, F_y, torque)
    besides gravity. Returns (q_next, v_next, z) where z = (c_n, beta, lambda)."""
    f = [0.0, -body.m * g, 0.0]  # @line L1
    if f_ext is not None:
        f = [f[i] + f_ext[i] for i in range(3)]
    A, b, v_star, G, _ = build_lcp(body, q, v, h, f, eps)
    if A is None:
        v_next, z = v_star, []
    else:
        z = lemke(A, b)  # @line L7
        if z is None:
            raise ArithmeticError("Lemke's method ended on a ray")
        v_next, _ = velocity_from_impulses(body, v_star, G, z)  # @line L8
    q_next = [q[k] + h * v_next[k] for k in range(3)]  # @line L9
    return q_next, v_next, z


def simulate(body, q, v, h, steps, g=9.81, f_ext=None, eps=0.01):
    for _ in range(steps):  # @line L10
        q, v, _ = step(body, q, v, h, g, f_ext, eps)
    return q, v


def lcp_residual(A, b, z):
    """The largest violation of z >= 0, w >= 0 and z_i w_i = 0."""
    w = [sum(A[i][j] * z[j] for j in range(len(z))) + b[i] for i in range(len(b))]
    r = 0.0
    for zi, wi in zip(z, w):
        r = max(r, -zi, -wi, abs(zi * wi))
    return r


def solve_dense(A, rhs):
    """Gaussian elimination with partial pivoting. Returns None for a singular matrix."""
    n = len(rhs)
    M = [list(A[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        p = max(range(col, n), key=lambda i: abs(M[i][col]))
        if abs(M[p][col]) < 1e-12:
            return None
        M[col], M[p] = M[p], M[col]
        for i in range(col + 1, n):
            f = M[i][col] / M[col][col]
            if f != 0.0:
                for j in range(col, n + 1):
                    M[i][j] -= f * M[col][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def lcp_enumerate(A, b, tol=1e-9):
    """All solutions of the LCP with a nonsingular basis, by trying each of the 2^m
    complementary cases: for each index, either z_i = 0 or w_i = 0."""
    m = len(b)
    sols = []
    for pattern in product((0, 1), repeat=m):
        S = [i for i in range(m) if pattern[i]]
        z = [0.0] * m
        if S:
            zs = solve_dense([[A[i][j] for j in S] for i in S], [-b[i] for i in S])
            if zs is None:
                continue
            for k, i in enumerate(S):
                z[i] = zs[k]
        if lcp_residual(A, b, z) <= tol:
            sols.append(z)
    return sols
