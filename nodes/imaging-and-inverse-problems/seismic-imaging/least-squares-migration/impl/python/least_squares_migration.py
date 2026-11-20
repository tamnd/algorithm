# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-migration/. The authors are listed in prov/H0YJBB.jsonl.
"""Least-squares migration (LSM): CGLS on the normal equations of a Born modeling operator.

Conventions (the imaging and inverse problems pages):
- The image m is a reflectivity on a grid, flattened row by row; the data d
  is a zero-offset section, flattened by time sample and then trace.
- The modeling operator L maps m to d. Migration is the adjoint L^T, and
  least-squares migration minimizes ||L m - d||^2 by the conjugate gradient
  method on L^T L m = L^T d (CGLS), with one product by L and one by L^T per
  iteration.
- The example operator is a zero-offset Born-Kirchhoff operator in the
  constant velocity v, with the exploding reflector traveltime
  tau = 2 r / v, r = sqrt(z^2 + (x - x_r)^2), the weight
  (z / r) / sqrt(r) (obliquity and 2D spreading) and a Ricker wavelet.
  It is stored as sparse rows, so L^T is its exact transpose.

Cost per iteration: one product with L and one with L^T, plus O(n + m)
for vectors; for the sparse example that is O(nnz(L)).
"""

import math


def ricker(t, f0):
    """The Ricker wavelet (1 - 2 a) exp(-a) with a = (pi f0 t)^2, peak frequency f0."""
    a = (math.pi * f0 * t) ** 2
    return (1.0 - 2.0 * a) * math.exp(-a)


def born_kirchhoff_operator(nt, dt, nx, dx, nz, dz, z_top, vel, f0, cut=2.5):
    """Sparse rows of the zero-offset Born-Kirchhoff operator in constant velocity.

    Image point (i, j) is at x = j dx, z = z_top + i dz (z_top > 0); column
    i * nx + j. Data row k * nx + r holds time k dt at the trace x_r = r dx.
    The entry is dx * (z / r) / sqrt(r) * ricker(k dt - 2 r / vel, f0), kept
    where |k dt - 2 r / vel| < cut / f0. Returns a list of nt * nx rows of
    (column, weight) pairs.
    """
    rows = [[] for _ in range(nt * nx)]
    half = cut / f0
    for i in range(nz):
        z = z_top + i * dz
        for j in range(nx):
            col = i * nx + j
            for r in range(nx):
                dist = math.hypot(z, (j - r) * dx)
                tau = 2.0 * dist / vel
                w = dx * (z / dist) / math.sqrt(dist)
                k0 = max(0, math.ceil((tau - half) / dt))
                k1 = min(nt - 1, math.floor((tau + half) / dt))
                for k in range(k0, k1 + 1):
                    rows[k * nx + r].append((col, w * ricker(k * dt - tau, f0)))
    return rows


def matvec(rows, x):
    """y = L x for sparse rows."""
    return [sum(w * x[c] for c, w in row) for row in rows]


def rmatvec(rows, y, n):
    """x = L^T y for sparse rows and n columns."""
    out = [0.0] * n
    for row, yi in zip(rows, y):
        if yi != 0.0:
            for c, w in row:
                out[c] += w * yi
    return out


def damped(apply_l, apply_lt, d, n, eps):
    """The operators and data of min ||L m - d||^2 + eps ||m||^2 as one least squares problem.

    The stacked operator is [L; sqrt(eps) I] and the stacked data is [d; 0].
    """
    nd = len(d)
    c = math.sqrt(eps)
    return (lambda x: apply_l(x) + [c * v for v in x],
            lambda r: [a + c * b for a, b in zip(apply_lt(r[:nd]), r[nd:])],
            list(d) + [0.0] * n)


def least_squares_migration(apply_l, apply_lt, d, n, iters):
    """CGLS for min ||L m - d||, started at m = 0.

    apply_l(m) and apply_lt(r) are the modeling and migration operators. Returns
    the image after iters steps and the list of the residual norms ||d - L m_k||.
    For a damped problem, pass the operators and data returned by damped().
    """
    m = [0.0] * n
    r = list(d)  # @line L1
    s = apply_lt(r)  # @line L2
    p = list(s)
    gamma = sum(v * v for v in s)
    norms = [math.sqrt(sum(v * v for v in r))]
    for _ in range(iters):  # @line L3
        if gamma == 0.0:  # @line L4
            break
        q = apply_l(p)  # @line L5
        alpha = gamma / sum(v * v for v in q)  # @line L6
        m = [a + alpha * b for a, b in zip(m, p)]  # @line L7
        r = [a - alpha * b for a, b in zip(r, q)]  # @line L8
        s = apply_lt(r)  # @line L9
        gnew = sum(v * v for v in s)
        p = [a + (gnew / gamma) * b for a, b in zip(s, p)]  # @line L10
        gamma = gnew
        norms.append(math.sqrt(sum(v * v for v in r)))
    return m, norms  # @line L11
