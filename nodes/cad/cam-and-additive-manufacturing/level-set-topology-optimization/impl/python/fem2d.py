# SPDX-License-Identifier: MIT
# Shared helper of the cm1 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Plane stress finite elements on a grid of unit square bilinear (Q4) elements.

The grid has nelx x nely elements. Node (i, j), with 0 <= i <= nelx and
0 <= j <= nely, is at the point (i, j) and has the number i (nely + 1) + j.
Its degrees of freedom are 2 n (x displacement) and 2 n + 1 (y displacement).
Element (ex, ey) has the number ex nely + ey and the nodes (ex, ey),
(ex + 1, ey), (ex + 1, ey + 1), (ex, ey + 1), counterclockwise.

The helper has no optimization in it. It builds the element stiffness matrix
exactly, assembles the global matrix with one factor per element, and solves
it with a banded LDL^T factorization that works with float or Fraction.
"""

from fractions import Fraction
from operator import mul


def q4_stiffness(nu):
    """The 8 x 8 stiffness matrix of a unit square Q4 element for E = 1.

    The integrand B^T D B is a polynomial of degree at most 2 in each
    coordinate, so the 3 x 3 Simpson rule is exact, and the result is an
    exact Fraction matrix.
    """
    nu = Fraction(nu)
    c = 1 / (1 - nu * nu)
    d = [[c, c * nu, 0], [c * nu, c, 0], [0, 0, c * (1 - nu) / 2]]
    rule = [(Fraction(0), Fraction(1, 6)), (Fraction(1, 2), Fraction(2, 3)), (Fraction(1), Fraction(1, 6))]
    corners = [(0, 0), (1, 0), (1, 1), (0, 1)]
    ke = [[Fraction(0)] * 8 for _ in range(8)]
    for x, wx in rule:
        for y, wy in rule:
            b = [[Fraction(0)] * 8 for _ in range(3)]
            for a, (cx, cy) in enumerate(corners):
                fx, gx = (x, 1) if cx else (1 - x, -1)
                fy, gy = (y, 1) if cy else (1 - y, -1)
                dx, dy = gx * fy, fx * gy  # derivatives of N_a = fx fy
                b[0][2 * a] = dx
                b[1][2 * a + 1] = dy
                b[2][2 * a] = dy
                b[2][2 * a + 1] = dx
            db = [[sum(d[r][s] * b[s][k] for s in range(3)) for k in range(8)] for r in range(3)]
            for i in range(8):
                for j in range(8):
                    ke[i][j] += wx * wy * sum(b[r][i] * db[r][j] for r in range(3))
    return ke


def node(nely, i, j):
    return i * (nely + 1) + j


def element_dofs(nelx, nely):
    """The 8 degrees of freedom of every element, in element order."""
    out = []
    for ex in range(nelx):
        for ey in range(nely):
            ns = [node(nely, ex, ey), node(nely, ex + 1, ey), node(nely, ex + 1, ey + 1), node(nely, ex, ey + 1)]
            out.append([k for n in ns for k in (2 * n, 2 * n + 1)])
    return out


def element_center(nely, e):
    ex, ey = divmod(e, nely)
    return ex + 0.5, ey + 0.5


def ldl_band(rows, b):
    """Factor a symmetric positive definite band matrix as L D L^T.

    rows[i] holds the entries K[i][s], ..., K[i][i] with s = max(0, i - b).
    Returns (low, diag): low[i] holds L[i][s .. i-1] and diag holds D.
    """
    m = len(rows)
    low, diag = [], []
    for i in range(m):
        s = max(0, i - b)
        a = rows[i]
        w = []  # w[l - s] = L[i][l] D[l]
        li = []
        for j in range(s, i):
            sj = max(0, j - b)
            t = a[j - s] - sum(map(mul, w[: j - s], low[j][s - sj: j - sj]))
            w.append(t)
            li.append(t / diag[j])
        diag.append(a[i - s] - sum(map(mul, w, li)))
        low.append(li)
    return low, diag


def ldl_solve(low, diag, f, b):
    m = len(diag)
    y = list(f)
    for i in range(m):
        s = max(0, i - b)
        y[i] -= sum(map(mul, low[i], y[s:i]))
    z = [y[i] / diag[i] for i in range(m)]
    for i in range(m - 1, -1, -1):
        s = max(0, i - b)
        zi = z[i]
        for k, lik in enumerate(low[i]):
            z[s + k] -= lik * zi
    return z


def solve(nelx, nely, ke, scale, force, fixed):
    """Solve K u = f with K = sum_e scale[e] ke_e and u = 0 on the fixed dofs.

    force is a dict {dof: value}; returns the full displacement list.
    """
    ndof = 2 * (nelx + 1) * (nely + 1)
    fixed = set(fixed)
    index, free = {}, []
    for k in range(ndof):
        if k not in fixed:
            index[k] = len(free)
            free.append(k)
    edofs = element_dofs(nelx, nely)
    b = 2 * nely + 5
    zero = 0 * scale[0]
    rows = [[zero] * (min(i, b) + 1) for i in range(len(free))]
    for e, dofs in enumerate(edofs):
        se = scale[e]
        for p in range(8):
            gi = index.get(dofs[p])
            if gi is None:
                continue
            row, s = rows[gi], max(0, gi - b)
            for q in range(8):
                gj = index.get(dofs[q])
                if gj is not None and gj <= gi:
                    row[gj - s] += se * ke[p][q]
    f = [force.get(k, zero) for k in free]
    low, diag = ldl_band(rows, b)
    uf = ldl_solve(low, diag, f, b)
    u = [zero] * ndof
    for k, v in zip(free, uf):
        u[k] = v
    return u


def element_energies(nelx, nely, ke, u):
    """u_e^T ke u_e for every element (twice the strain energy for E = 1)."""
    out = []
    for dofs in element_dofs(nelx, nely):
        ue = [u[k] for k in dofs]
        out.append(sum(ue[p] * sum(map(mul, ke[p], ue)) for p in range(8)))
    return out


def dense_solve(a, f):
    """Gaussian elimination with partial pivoting, a reference for the tests."""
    n = len(f)
    m = [list(a[i]) + [f[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            t = m[r][c] / m[c][c]
            if t:
                for k in range(c, n + 1):
                    m[r][k] -= t * m[c][k]
    x = [0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x
