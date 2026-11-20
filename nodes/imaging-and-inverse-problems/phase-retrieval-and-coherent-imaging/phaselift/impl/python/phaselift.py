# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phaselift/. The authors are listed in prov/K3F300.jsonl.

"""PhaseLift for phase retrieval (Candes, Strohmer and Voroninski 2013).

The data are y_r = |a_r^H x|^2 = a_r^H (x x^H) a_r, which are linear in the
lifted matrix X = x x^H. PhaseLift replaces the rank one condition by
X >= 0 (positive semidefinite) and solves

    minimize tr(X)  subject to  A(X) = y,  X >= 0,   A(X)_r = a_r^H X a_r.

This file solves the penalized form

    minimize F(X) = (1/2) ||A(X) - y||^2 + lam tr(X)  over X >= 0

by projected gradient steps with the step 1 / L, L = sum_r ||a_r||^4 >= ||A||^2.
With lam = 0 it finds a point of {X >= 0 : A(X) = y}; Candes and Li (2014)
show that for m >= c0 n Gaussian vectors this set is the single point x x^H.
The estimate of x is the top eigenvector of X times the root of its eigenvalue.

Hermitian matrices are lists of rows of complex numbers. The projection onto
the positive semidefinite cone uses the real form [[B, -C], [C, B]] of
X = B + iC and the Jacobi eigenvalue method of the shared helper.
"""

import math
import random

from imgla import svd, sym_eig


def gaussian_design(rng, m, n):
    """m sampling vectors with entries N(0, 1/2) + i N(0, 1/2)."""
    s = math.sqrt(0.5)
    return [[complex(rng.gauss(0.0, s), rng.gauss(0.0, s)) for _ in range(n)] for _ in range(m)]


def inner(a, v):
    """<a, v> = a^H v."""
    return sum(complex(u).conjugate() * w for u, w in zip(a, v))


def norm(v):
    """The Euclidean norm of a vector."""
    return math.sqrt(sum(abs(w) ** 2 for w in v))


def measure(a_rows, x):
    """The phaseless data y_r = |a_r^H x|^2."""
    return [abs(inner(a, x)) ** 2 for a in a_rows]


def lift(x):
    """The rank one matrix x x^H."""
    return [[complex(u) * complex(v).conjugate() for v in x] for u in x]


def apply_a(a_rows, mat):
    """A(X)_r = a_r^H X a_r, a real number for Hermitian X."""
    out = []
    for a in a_rows:
        xa = [sum(row[j] * a[j] for j in range(len(a))) for row in mat]
        out.append(inner(a, xa).real)
    return out


def apply_a_adjoint(a_rows, v):
    """A^*(v) = sum_r v_r a_r a_r^H."""
    n = len(a_rows[0])
    out = [[0j] * n for _ in range(n)]
    for a, vr in zip(a_rows, v):
        for i in range(n):
            c = vr * a[i]
            row = out[i]
            for j in range(n):
                row[j] += c * a[j].conjugate()
    return out


def frob_inner(p, q):
    """Re tr(P^H Q), the real inner product of matrices."""
    return sum((complex(u).conjugate() * v).real for rp, rq in zip(p, q) for u, v in zip(rp, rq))


def frob_norm(p):
    """The Frobenius norm."""
    return math.sqrt(sum(abs(v) ** 2 for row in p for v in row))


def trace(p):
    """The trace, a real number for Hermitian P."""
    return sum(p[i][i] for i in range(len(p))).real


def hermitian_eig(mat):
    """Eigenvalues (ascending) and unit eigenvectors of a Hermitian matrix.

    The real form R = [[B, -C], [C, B]] of X = B + iC has each eigenvalue of X
    twice; the eigenvector (p, q) of R gives the eigenvector p + iq of X. One
    vector of each pair is kept, by a Gram-Schmidt test.
    """
    n = len(mat)
    real_form = [[mat[i][j].real for j in range(n)] + [-mat[i][j].imag for j in range(n)] for i in range(n)]
    real_form += [[mat[i][j].imag for j in range(n)] + [mat[i][j].real for j in range(n)] for i in range(n)]
    w, q = sym_eig(real_form)
    vals, vecs = [], []
    for k in sorted(range(2 * n), key=lambda t: -w[t]):
        v = [complex(q[i][k], q[i + n][k]) for i in range(n)]
        for u in vecs:
            c = inner(u, v)
            v = [vi - c * ui for vi, ui in zip(v, u)]
        s = norm(v)
        if s > 0.5 and len(vecs) < n:
            vecs.append([vi / s for vi in v])
            vals.append(w[k])
    order = sorted(range(n), key=lambda t: vals[t])
    return [vals[t] for t in order], [vecs[t] for t in order]


def psd_project(mat):
    """The nearest positive semidefinite matrix in the Frobenius norm.

    Spectral clipping X+ = sum_k max(w_k, 0) u_k u_k^H, done on the real form:
    R+ = Q diag(max(w, 0)) Q^T has the same block form, and X+ = R+_11 + i R+_21.
    """
    n = len(mat)
    real_form = [[mat[i][j].real for j in range(n)] + [-mat[i][j].imag for j in range(n)] for i in range(n)]
    real_form += [[mat[i][j].imag for j in range(n)] + [mat[i][j].real for j in range(n)] for i in range(n)]
    w, q = sym_eig(real_form)
    keep = [k for k in range(2 * n) if w[k] > 0.0]
    out = [[0j] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            b = sum(w[k] * (q[i][k] * q[j][k] + q[i + n][k] * q[j + n][k]) for k in keep) / 2.0
            c = sum(w[k] * (q[i + n][k] * q[j][k] - q[i][k] * q[j + n][k]) for k in keep) / 2.0
            out[i][j] = complex(b, c)
    return out


def real_rows(a_rows):
    """The m x n^2 real matrix of A in an orthonormal basis of the Hermitian matrices.

    The basis is E_ii, (E_ij + E_ji) / sqrt 2 and i (E_ij - E_ji) / sqrt 2 for
    i < j, orthonormal for Re tr(P^H Q). The coordinates of a a^H are |a_i|^2,
    sqrt 2 Re(a_i conj(a_j)) and sqrt 2 Im(a_i conj(a_j)).
    """
    n = len(a_rows[0])
    out = []
    for a in a_rows:
        row = [abs(a[i]) ** 2 for i in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                p = a[i] * a[j].conjugate()
                row += [math.sqrt(2.0) * p.real, math.sqrt(2.0) * p.imag]
        out.append(row)
    return out


def op_norm_sq(a_rows):
    """||A||^2, the largest eigenvalue of A^* A, from the singular values of real_rows."""
    _, s, _ = svd(real_rows(a_rows))
    return s[0] ** 2


def objective(a_rows, y, mat, lam=0.0):
    """F(X) = (1/2) ||A(X) - y||^2 + lam tr(X)."""
    r = [u - v for u, v in zip(apply_a(a_rows, mat), y)]
    return 0.5 * sum(t * t for t in r) + lam * trace(mat)


def phaselift(a_rows, y, iters, lam=0.0, x0=None, record=None, big_l=None):
    """Projected gradient for min F(X) over X >= 0. Returns X.

    The step is 1 / L with L = ||A||^2 (times 1 + 1e-9 against rounding) unless
    big_l is given; any L >= ||A||^2, such as sum_r ||a_r||^4, is safe. x0 is the
    start matrix (zero by default). If record is a list, X_0 .. X_iters are
    appended to it.
    """
    n = len(a_rows[0])
    if big_l is None:
        big_l = op_norm_sq(a_rows) * (1.0 + 1e-9)  # @line L1
    mat = [[0j] * n for _ in range(n)] if x0 is None else [list(row) for row in x0]  # @line L2
    if record is not None:
        record.append(mat)
    for _ in range(iters):  # @line L3
        resid = [u - v for u, v in zip(apply_a(a_rows, mat), y)]  # @line L4
        grad = apply_a_adjoint(a_rows, resid)  # @line L5
        for i in range(n):
            grad[i][i] += lam
        step = [[mat[i][j] - grad[i][j] / big_l for j in range(n)] for i in range(n)]
        mat = psd_project(step)  # @line L6
        if record is not None:
            record.append(mat)
    return mat  # @line L7


def extract(mat):
    """The vector sqrt(w_max) u_max from the top eigenpair of X."""
    w, v = hermitian_eig(mat)
    return [math.sqrt(max(w[-1], 0.0)) * c for c in v[-1]]


def dist(z, x):
    """min over phi of ||z - e^{i phi} x||."""
    c = inner(x, z)
    phase = c / abs(c) if abs(c) > 0.0 else 1.0
    return norm([u - phase * v for u, v in zip(z, x)])


def random_hermitian(rng, n):
    """A random Hermitian matrix, for tests."""
    g = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)] for _ in range(n)]
    return [[(g[i][j] + g[j][i].conjugate()) / 2.0 for j in range(n)] for i in range(n)]


def demo(seed=1, n=4, m=24, iters=300):
    """dist(extract(X_k), x) for a random unit x; a small measurement."""
    rng = random.Random(seed)
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
    s = norm(x)
    x = [v / s for v in x]
    a = gaussian_design(rng, m, n)
    mat = phaselift(a, measure(a, x), iters)
    return dist(extract(mat), x), frob_norm([[u - v for u, v in zip(r1, r2)] for r1, r2 in zip(mat, lift(x))])
