# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mac-grid/. The authors are listed in prov/NKCN2S.jsonl.

"""The operations of a 2D MAC grid, written out on plain arrays.

The arrays follow the layout of macgrid.py: p[i][j] at ((i + 1/2) dx, (j + 1/2) dx),
u[i][j] at (i dx, (j + 1/2) dx) and v[i][j] at ((i + 1/2) dx, j dx). A cell outside
the grid is SOLID. The functions use only + - * / and comparisons, so they also run on
fractions.Fraction values, which lets the tests check the identities exactly.

The file also has the two periodic Laplacians of the page: the MAC (staggered) one and
the collocated one with central differences, to show the checkerboard null space.
"""

import math
from fractions import Fraction

from macgrid import AIR, FLUID, SOLID


def label_of(label, i, j):
    """The label of cell (i, j); a cell outside the grid is SOLID."""
    if 0 <= i < len(label) and 0 <= j < len(label[0]):
        return label[i][j]
    return SOLID


def sample(q, x, y, dx, ox, oy):
    """Bilinear sample at (x, y) of q, where q[a][b] is at ((a + ox) dx, (b + oy) dx)."""
    na, nb = len(q), len(q[0])
    if na < 2 or nb < 2:
        raise ValueError("sample needs at least 2 by 2 values")
    fx = min(max(x / dx - ox, 0), na - 1)  # @line L1
    fy = min(max(y / dx - oy, 0), nb - 1)
    a = min(int(math.floor(fx)), na - 2)  # @line L2
    b = min(int(math.floor(fy)), nb - 2)
    s, t = fx - a, fy - b
    return ((1 - s) * (1 - t) * q[a][b] + (1 - s) * t * q[a][b + 1]  # @line L3
            + s * (1 - t) * q[a + 1][b] + s * t * q[a + 1][b + 1])


def divergence(u, v, dx):
    """The divergence of every cell: (u[i+1][j] - u[i][j] + v[i][j+1] - v[i][j]) / dx."""
    nx, ny = len(v), len(u[0])
    return [[(u[i + 1][j] - u[i][j] + v[i][j + 1] - v[i][j]) / dx  # @line L4
             for j in range(ny)] for i in range(nx)]


def gradient_update(u, v, p, label, dt, rho, dx):
    """Subtract dt / (rho dx) times the pressure difference on each open face, in place.

    A face is open if no side is SOLID and at least one side is FLUID. AIR cells have p = 0.
    """
    nx, ny = len(p), len(p[0])
    s = dt / (rho * dx)

    def pr(i, j):
        return 0 if label[i][j] == AIR else p[i][j]

    for i in range(1, nx):  # @line L5
        for j in range(ny):
            a, c = label[i - 1][j], label[i][j]
            if a == SOLID or c == SOLID or (a != FLUID and c != FLUID):
                continue
            u[i][j] = u[i][j] - s * (pr(i, j) - pr(i - 1, j))  # @line L6
    for i in range(nx):  # @line L7
        for j in range(1, ny):
            a, c = label[i][j - 1], label[i][j]
            if a == SOLID or c == SOLID or (a != FLUID and c != FLUID):
                continue
            v[i][j] = v[i][j] - s * (pr(i, j) - pr(i, j - 1))


def poisson_system(u, v, label, dt, rho, dx):
    """The dense pressure system A p = b over the FLUID cells, in row-major cell order.

    Returns (cells, A, b). Row k of A has the number of non-SOLID neighbors on the
    diagonal and -1 for each FLUID neighbor. b = -(rho dx / dt) times the face flux sum.
    """
    nx, ny = len(label), len(label[0])
    cells = [(i, j) for i in range(nx) for j in range(ny) if label[i][j] == FLUID]
    idx = {c: k for k, c in enumerate(cells)}
    n = len(cells)
    a_mat = [[0] * n for _ in range(n)]
    b = [0] * n
    for k, (i, j) in enumerate(cells):
        for (a, c) in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
            lab = label_of(label, a, c)
            if lab == SOLID:
                continue
            a_mat[k][k] += 1  # @line L8
            if lab == FLUID:
                a_mat[k][idx[(a, c)]] -= 1  # @line L9
        b[k] = -rho * dx / dt * (u[i + 1][j] - u[i][j] + v[i][j + 1] - v[i][j])  # @line L10
    return cells, a_mat, b


def periodic_mac_laplacian(n):
    """The matrix of D G on an n by n periodic MAC grid with dx = 1 (the 5-point Laplacian)."""
    m = n * n
    a = [[Fraction(0)] * m for _ in range(m)]
    for i in range(n):
        for j in range(n):
            k = i * n + j
            for (di, dj) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a[k][((i + di) % n) * n + (j + dj) % n] += 1
            a[k][k] -= 4
    return a


def periodic_collocated_laplacian(n):
    """The matrix of D G on an n by n periodic collocated grid, both by central differences.

    The gradient is (p[i+1] - p[i-1]) / 2, so D G reaches two cells away and skips the
    direct neighbors: the stencil is (p[i+2] - 2 p[i] + p[i-2]) / 4 in each axis.
    """
    m = n * n
    a = [[Fraction(0)] * m for _ in range(m)]
    q = Fraction(1, 4)
    for i in range(n):
        for j in range(n):
            k = i * n + j
            for (di, dj) in ((2, 0), (-2, 0), (0, 2), (0, -2)):
                a[k][((i + di) % n) * n + (j + dj) % n] += q
            a[k][k] -= 4 * q
    return a


def nullity(a):
    """The dimension of the null space of a square matrix of Fractions, by exact elimination."""
    m = [list(row) for row in a]
    n = len(m)
    rank = 0
    for col in range(n):
        piv = next((r for r in range(rank, n) if m[r][col] != 0), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        for r in range(n):
            if r != rank and m[r][col] != 0:
                f = m[r][col] / m[rank][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[rank])]
        rank += 1
    return n - rank
