# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-phase-unwrapping/. The authors are listed in prov/FX5THR.jsonl.
"""Unweighted least squares phase unwrapping by the method of Ghiglia and Romero (1994).

The input is a wrapped phase image psi[i][j] (rows i = 0 .. m-1, columns
j = 0 .. n-1) with values in (-pi, pi]. The output phi minimizes

    sum (phi[i][j+1] - phi[i][j] - dx[i][j])^2 + sum (phi[i+1][j] - phi[i][j] - dy[i][j])^2

over all real images, where dx and dy are the wrapped differences of psi. The
normal equations are the discrete Poisson equation with Neumann boundary
conditions, which the two-dimensional DCT-II diagonalizes. phi is defined up to
an additive constant; this code returns the solution with zero mean.

The DCT here is computed by direct sums, O(m n (m + n)). A fast DCT gives
O(m n log(m n)).
"""

import math

TWO_PI = 2.0 * math.pi


def wrap(x):
    """The wrapping operator W: the value of x - 2 pi k in (-pi, pi]."""
    y = math.fmod(x + math.pi, TWO_PI)
    if y <= 0.0:
        y += TWO_PI
    return y - math.pi


def wrapped_gradients(psi):
    """dx[i][j] = W(psi[i][j+1] - psi[i][j]) for j < n - 1, dy[i][j] = W(psi[i+1][j] - psi[i][j]) for i < m - 1."""
    m, n = len(psi), len(psi[0])
    dx = [[wrap(psi[i][j + 1] - psi[i][j]) for j in range(n - 1)] for i in range(m)]
    dy = [[wrap(psi[i + 1][j] - psi[i][j]) for j in range(n)] for i in range(m - 1)]
    return dx, dy


def divergence(dx, dy, m, n):
    """rho[i][j] = dx[i][j] - dx[i][j-1] + dy[i][j] - dy[i-1][j], with missing terms taken as zero."""
    rho = [[0.0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            v = 0.0
            if j < n - 1:
                v += dx[i][j]
            if j > 0:
                v -= dx[i][j - 1]
            if i < m - 1:
                v += dy[i][j]
            if i > 0:
                v -= dy[i - 1][j]
            rho[i][j] = v
    return rho


def _dct_matrix(n):
    """c[k][t] = cos(pi k (2 t + 1) / (2 n)), the DCT-II basis."""
    return [[math.cos(math.pi * k * (2 * t + 1) / (2.0 * n)) for t in range(n)] for k in range(n)]


def dct2(x):
    """Two-dimensional DCT-II: X[k][l] = sum_{i, j} x[i][j] cos(pi k (2i+1) / 2m) cos(pi l (2j+1) / 2n)."""
    m, n = len(x), len(x[0])
    cm, cn = _dct_matrix(m), _dct_matrix(n)
    rows = [[sum(x[i][j] * cn[l][j] for j in range(n)) for l in range(n)] for i in range(m)]
    return [[sum(cm[k][i] * rows[i][l] for i in range(m)) for l in range(n)] for k in range(m)]


def idct2(xh):
    """The inverse of dct2: x[i][j] = (1 / (m n)) sum_{k, l} w_k w_l X[k][l] cos(..) cos(..), w_0 = 1, w_k = 2."""
    m, n = len(xh), len(xh[0])
    cm, cn = _dct_matrix(m), _dct_matrix(n)
    wm = [1.0] + [2.0] * (m - 1)
    wn = [1.0] + [2.0] * (n - 1)
    cols = [[sum(wm[k] * cm[k][i] * xh[k][l] for k in range(m)) / m for l in range(n)] for i in range(m)]
    return [[sum(wn[l] * cn[l][j] * cols[i][l] for l in range(n)) / n for j in range(n)] for i in range(m)]


def neumann_laplacian(phi):
    """The five point Laplacian with mirror (Neumann) boundary: the sum over the existing neighbours of phi[q] - phi[p]."""
    m, n = len(phi), len(phi[0])
    out = [[0.0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            v = 0.0
            for a, b in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                if 0 <= a < m and 0 <= b < n:
                    v += phi[a][b] - phi[i][j]
            out[i][j] = v
    return out


def unwrap_least_squares(psi):
    """Return the zero mean least squares unwrapped phase of the wrapped image psi."""
    m, n = len(psi), len(psi[0])
    dx, dy = wrapped_gradients(psi)  # @line L1
    rho = divergence(dx, dy, m, n)  # @line L2
    rh = dct2(rho)  # @line L3
    ph = [[0.0] * n for _ in range(m)]
    for k in range(m):
        for l in range(n):
            if k == 0 and l == 0:
                continue  # @line L5
            den = 2.0 * math.cos(math.pi * k / m) + 2.0 * math.cos(math.pi * l / n) - 4.0
            ph[k][l] = rh[k][l] / den  # @line L4
    phi = idct2(ph)  # @line L6
    return phi  # @line L7


def residues(psi):
    """Residue charges: r[i][j] = (loop sum of wrapped differences around the 2 x 2 square at (i, j)) / (2 pi)."""
    m, n = len(psi), len(psi[0])
    out = [[0] * (n - 1) for _ in range(m - 1)]
    for i in range(m - 1):
        for j in range(n - 1):
            s = (wrap(psi[i][j + 1] - psi[i][j]) + wrap(psi[i + 1][j + 1] - psi[i][j + 1])
                 + wrap(psi[i + 1][j] - psi[i + 1][j + 1]) + wrap(psi[i][j] - psi[i + 1][j]))
            out[i][j] = round(s / TWO_PI)
    return out


def least_squares_cost(phi, psi):
    """The objective: the squared misfit between the gradient of phi and the wrapped gradients of psi."""
    dx, dy = wrapped_gradients(psi)
    m, n = len(psi), len(psi[0])
    c = sum((phi[i][j + 1] - phi[i][j] - dx[i][j]) ** 2 for i in range(m) for j in range(n - 1))
    c += sum((phi[i + 1][j] - phi[i][j] - dy[i][j]) ** 2 for i in range(m - 1) for j in range(n))
    return c
