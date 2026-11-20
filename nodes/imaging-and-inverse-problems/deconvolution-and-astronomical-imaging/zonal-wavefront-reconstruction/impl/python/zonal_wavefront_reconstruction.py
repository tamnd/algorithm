# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zonal-wavefront-reconstruction/. The authors are listed in prov/4DD2FS.jsonl.
"""Zonal wavefront reconstruction: least squares phase from slope data.

The phase is an N x N list of rows phi[i][j]: row i is the y index and
column j the x index, with grid spacing h. Slope data are stored as
"slope times h", that is as phase differences, in a pair (dx, dy):

- Hudgin: dx[i][j] = phi[i][j+1] - phi[i][j] (N rows, N - 1 columns) and
  dy[i][j] = phi[i+1][j] - phi[i][j] (N - 1 rows, N columns).
- Fried: one subaperture per square of four phase points, both arrays
  (N - 1) x (N - 1), each slope the mean of the two edge differences.
- Southwell: slopes sx, sy measured at the phase points (N x N); the mean
  of two neighbor slopes times h is the difference between them, which
  gives Hudgin data (southwell_to_hudgin).

reconstruct() solves the normal equations G^T G phi = G^T s by conjugate
gradients and returns the minimum norm least squares solution. Works with
float and with fractions.Fraction values (exact arithmetic).
"""


def _zeros(n1, n2, like=0):
    return [[0 * like for _ in range(n2)] for _ in range(n1)]


def hudgin_forward(phi):
    """G phi for the Hudgin geometry: neighbor differences along x and y."""
    n = len(phi)
    dx = [[phi[i][j + 1] - phi[i][j] for j in range(n - 1)] for i in range(n)]
    dy = [[phi[i + 1][j] - phi[i][j] for j in range(n)] for i in range(n - 1)]
    return dx, dy


def hudgin_adjoint(s, n):
    """G^T s for the Hudgin geometry: minus the backward divergence of (dx, dy)."""
    dx, dy = s
    out = _zeros(n, n)
    for i in range(n):
        for j in range(n - 1):
            out[i][j + 1] += dx[i][j]
            out[i][j] -= dx[i][j]
    for i in range(n - 1):
        for j in range(n):
            out[i + 1][j] += dy[i][j]
            out[i][j] -= dy[i][j]
    return out


def fried_forward(phi):
    """G phi for the Fried geometry: the mean x and y differences of each 2 x 2 square."""
    n = len(phi)
    dx = [[(phi[i][j + 1] + phi[i + 1][j + 1] - phi[i][j] - phi[i + 1][j]) / 2
           for j in range(n - 1)] for i in range(n - 1)]
    dy = [[(phi[i + 1][j] + phi[i + 1][j + 1] - phi[i][j] - phi[i][j + 1]) / 2
           for j in range(n - 1)] for i in range(n - 1)]
    return dx, dy


def fried_adjoint(s, n):
    """G^T s for the Fried geometry."""
    dx, dy = s
    out = _zeros(n, n)
    for i in range(n - 1):
        for j in range(n - 1):
            a, b = dx[i][j] / 2, dy[i][j] / 2
            out[i][j + 1] += a
            out[i + 1][j + 1] += a
            out[i][j] -= a
            out[i + 1][j] -= a
            out[i + 1][j] += b
            out[i + 1][j + 1] += b
            out[i][j] -= b
            out[i][j + 1] -= b
    return out


GEOMETRIES = {
    "hudgin": (hudgin_forward, hudgin_adjoint),
    "fried": (fried_forward, fried_adjoint),
}


def southwell_to_hudgin(sx, sy, h=1):
    """Southwell data: slopes at the phase points. Returns Hudgin difference data.

    The model is phi[i][j+1] - phi[i][j] = h (sx[i][j] + sx[i][j+1]) / 2, and
    the same along y, so the normal matrix is the one of Hudgin.
    """
    n = len(sx)
    dx = [[h * (sx[i][j] + sx[i][j + 1]) / 2 for j in range(n - 1)] for i in range(n)]
    dy = [[h * (sy[i][j] + sy[i + 1][j]) / 2 for j in range(n)] for i in range(n - 1)]
    return dx, dy


def null_space(geometry, n):
    """An orthogonal basis of the null space of G: piston, and for Fried also the waffle mode.

    For odd n the checkerboard (-1)^(i+j) has the sum 1, so its mean is
    removed to make it orthogonal to the piston.
    """
    piston = [[1] * n for _ in range(n)]
    if geometry == "fried":
        waffle = [[1 if (i + j) % 2 == 0 else -1 for j in range(n)] for i in range(n)]
        if n % 2 == 1:
            c = 1 / (n * n)
            waffle = [[v - c for v in row] for row in waffle]
        return [piston, waffle]
    return [piston]


def _dot(a, b):
    return sum(p * q for ra, rb in zip(a, b) for p, q in zip(ra, rb))


def _sdot(s, t):
    return _dot(s[0], t[0]) + _dot(s[1], t[1])


def _axpy(x, a, y):
    return [[p + a * q for p, q in zip(rx, ry)] for rx, ry in zip(x, y)]


def project_out_null(phi, geometry):
    """Remove the components of phi along the null space modes (they are orthogonal)."""
    n = len(phi)
    for z in null_space(geometry, n):
        c = _dot(z, phi) / _dot(z, z)
        phi = _axpy(phi, -c, z)
    return phi


def residual_norm2(phi, s, geometry):
    """||G phi - s||^2."""
    fwd = GEOMETRIES[geometry][0]
    g = fwd(phi)
    return sum((p - q) ** 2 for a, b in zip(g, s) for ra, rb in zip(a, b) for p, q in zip(ra, rb))


def reconstruct(s, n, geometry="hudgin", iters=None, tol=0):
    """Minimum norm least squares phase from difference data s = (dx, dy).

    Conjugate gradients on G^T G phi = G^T s from phi = 0. Stops after iters
    steps (default n * n) or when ||r|| <= tol ||b||. With Fraction data and
    tol = 0 it stops at the exact solution.
    """
    fwd, adj = GEOMETRIES[geometry]
    if iters is None:
        iters = n * n
    b = adj(s, n)  # @line L1
    phi = _zeros(n, n)  # @line L2
    r = b
    p = r
    rr = _dot(r, r)
    stop = tol * tol * rr
    for _ in range(iters):  # @line L3
        if rr == 0 or rr <= stop:
            break
        q = adj(fwd(p), n)  # @line L4
        a = rr / _dot(p, q)  # @line L5
        phi = _axpy(phi, a, p)  # @line L6
        r = _axpy(r, -a, q)  # @line L7
        rr_new = _dot(r, r)  # @line L8
        p = _axpy(r, rr_new / rr, p)
        rr = rr_new
    phi = project_out_null(phi, geometry)  # @line L9
    return phi  # @line L10


def normal_matrix(geometry, n):
    """The dense n^2 x n^2 matrix G^T G, built column by column (for tests)."""
    fwd, adj = GEOMETRIES[geometry]
    cols = []
    for k in range(n * n):
        e = _zeros(n, n)
        e[k // n][k % n] = 1
        col = adj(fwd(e), n)
        cols.append([v for row in col for v in row])
    return [[cols[c][r] for c in range(n * n)] for r in range(n * n)]
