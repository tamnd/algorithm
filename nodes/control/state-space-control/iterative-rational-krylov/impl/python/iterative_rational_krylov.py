# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-rational-krylov/. The authors are listed in prov/P106V2.jsonl.

"""The iterative rational Krylov algorithm (IRKA) for SISO systems.

For G(s) = c (s I - A)^(-1) b with A Hurwitz, IRKA looks for a reduced model
G_r of order r that satisfies the first-order conditions for a local minimum
of the H2 error ||G - G_r||_H2: G_r must interpolate G and G' at the mirror
images -lambda_i of its own poles lambda_i.

One step takes shifts s_1, ..., s_r (closed under conjugation), builds

    V = [(s_1 I - A)^(-1) b, ..., (s_r I - A)^(-1) b]
    W = [(s_1 I - A^T)^(-1) c^T, ..., (s_r I - A^T)^(-1) c^T]

and the Petrov-Galerkin model A_r = (W^T V)^(-1) W^T A V,
b_r = (W^T V)^(-1) W^T b, c_r = c V. Then the new shifts are -eig(A_r).
The step stops when the shifts stop moving.

For a conjugate pair of shifts the two complex columns are replaced by the
real and imaginary parts of one of them. That leaves the column space the
same, so the reduced transfer function is the same, and all reduced
matrices are real. The bases are orthonormalized for conditioning; that also
leaves the spaces the same.
"""

import math

from ctlmat import charpoly, eye, kron, mul, polyroots, solve, transpose, unvec, vec

__all__ = [
    "project", "irka", "default_shifts", "transfer", "transfer_derivative",
    "h2_norm", "h2_error", "poles",
]


def _gram_schmidt(cols):
    """Orthonormalize real column vectors (twice, for stability)."""
    out = []
    for v in cols:
        w = list(v)
        for _ in range(2):
            for q in out:
                h = sum(x * y for x, y in zip(q, w))
                w = [x - h * y for x, y in zip(w, q)]
        nrm = math.sqrt(sum(x * x for x in w))
        if nrm == 0.0:
            raise ValueError("the projection basis is rank deficient")
        out.append([x / nrm for x in w])
    return out


def _real_basis(mat, vec_b, shifts):
    """Return real columns spanning {(s I - mat)^(-1) vec_b : s in shifts}."""
    n = len(mat)
    cols = []
    for s in shifts:
        if s.imag < 0:
            continue
        m = [[(s if i == j else 0) - mat[i][j] for j in range(n)] for i in range(n)]
        if s.imag == 0:
            x = solve([[float(v.real) for v in row] for row in m], [float(v) for v in vec_b])
            cols.append(x)
        else:
            x = solve(m, [complex(v) for v in vec_b])
            cols.append([v.real for v in x])
            cols.append([v.imag for v in x])
    return _gram_schmidt(cols)


def poles(a):
    """Return the eigenvalues of a small real matrix (roots of its characteristic polynomial)."""
    return polyroots(charpoly([[float(v) for v in row] for row in a]))


def project(a, b, c, shifts):
    """Return (A_r, b_r, c_r) of the rational Krylov projection at the shifts.

    a is n by n, b is a flat list of length n (the input column), c is a
    flat list (the output row). shifts is a list of complex numbers, closed
    under conjugation. The result interpolates G and G' at every shift.
    """
    af = [[float(v) for v in row] for row in a]
    v_cols = _real_basis(af, b, shifts)  # @line L3
    w_cols = _real_basis(transpose(af), c, shifts)
    r = len(v_cols)
    if r != len(w_cols) or r != len(shifts):
        raise ValueError("shifts must be closed under conjugation")
    v = transpose(v_cols)
    w = transpose(w_cols)
    wt = w_cols
    e = mul(wt, v)
    ar = solve(e, mul(mul(wt, af), v))  # @line L4
    br = solve(e, [sum(wt[i][k] * b[k] for k in range(len(b))) for i in range(r)])
    cr = [sum(c[k] * v[k][j] for k in range(len(c))) for j in range(r)]
    return ar, br, cr


def default_shifts(a, r):
    """Return r real shifts spread geometrically over the spectrum scale of A.

    The ends are 1 / ||A^(-1)||_inf and ||A||_inf, which bound the smallest
    and largest eigenvalue magnitudes from below and above.
    """
    af = [[float(v) for v in row] for row in a]
    inv_a = solve(af, eye(len(af)))
    lo = 1.0 / max(sum(abs(x) for x in row) for row in inv_a)
    hi = max(sum(abs(x) for x in row) for row in af)
    if r == 1:
        return [complex(math.sqrt(lo * hi))]
    return [complex(lo * (hi / lo) ** (k / (r - 1))) for k in range(r)]


def _shift_key(s):
    return (round(s.real, 12), s.imag)


def irka(a, b, c, r, shifts=None, tol=1e-10, maxiter=200):
    """Run IRKA. Returns (A_r, b_r, c_r, shifts, iterations, converged).

    shifts are the final shifts, equal to -eig(A_r) at convergence. The
    iteration stops when the largest relative change of the sorted shifts
    is below tol, or after maxiter steps.
    """
    s = list(shifts) if shifts is not None else default_shifts(a, r)  # @line L1
    s = sorted((complex(x) for x in s), key=_shift_key)
    for it in range(1, maxiter + 1):  # @line L2
        ar, br, cr = project(a, b, c, s)
        new = sorted((-z for z in poles(ar)), key=_shift_key)  # @line L5
        change = max(abs(x - y) / abs(y) for x, y in zip(new, s))
        s = new
        if change < tol:  # @line L6
            return ar, br, cr, s, it, True  # @line L7
    return ar, br, cr, s, maxiter, False  # @line L8


def transfer(a, b, c, s):
    """Return c (s I - A)^(-1) b."""
    n = len(a)
    m = [[(s if i == j else 0) - a[i][j] for j in range(n)] for i in range(n)]
    x = solve([[complex(v) for v in row] for row in m], [complex(v) for v in b])
    return sum(ci * xi for ci, xi in zip(c, x))


def transfer_derivative(a, b, c, s):
    """Return G'(s) = -c (s I - A)^(-2) b."""
    n = len(a)
    m = [[complex((s if i == j else 0) - a[i][j]) for j in range(n)] for i in range(n)]
    x = solve(m, [complex(v) for v in b])
    y = solve(m, x)
    return -sum(ci * yi for ci, yi in zip(c, y))


def _lyap(a, q):
    n = len(a)
    big = [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(kron(eye(n), a), kron(a, eye(n)))]
    return unvec(solve(big, [-v for v in vec(q)]), n, n)


def h2_norm(a, b, c):
    """Return ||c (s I - A)^(-1) b||_H2 = sqrt(c P c^T), A P + P A^T + b b^T = 0."""
    af = [[float(v) for v in row] for row in a]
    p = _lyap(af, [[float(x) * float(y) for y in b] for x in b])
    val = sum(float(c[i]) * p[i][j] * float(c[j]) for i in range(len(c)) for j in range(len(c)))
    return math.sqrt(max(val, 0.0))


def h2_error(a, b, c, ar, br, cr):
    """Return ||G - G_r||_H2 from the Lyapunov equation of the error system.

    Both A and A_r must be Hurwitz.
    """
    n, r = len(a), len(ar)
    ae = [[float(a[i][j]) for j in range(n)] + [0.0] * r for i in range(n)]
    ae += [[0.0] * n + [float(ar[i][j]) for j in range(r)] for i in range(r)]
    be = [float(v) for v in b] + [float(v) for v in br]
    ce = [float(v) for v in c] + [-float(v) for v in cr]
    return h2_norm(ae, be, ce)
