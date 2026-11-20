# SPDX-License-Identifier: MIT
# Shared helper of the imaging and inverse problems pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Dense linear algebra on lists of rows (float, complex or Fraction entries).

A matrix is a list of rows. A vector is a list of numbers. The inner product
is <u, v> = sum_i conj(u_i) v_i, linear in the second argument, so that the
adjoint A^H satisfies <A x, y> = <x, A^H y>.
"""

import math


def _flat(x):
    """Flatten a list of rows (an image) into one list; a vector is returned as is."""
    if x and isinstance(x[0], (list, tuple)):
        return [v for row in x for v in row]
    return x


def zeros(m, n):
    """The m x n zero matrix."""
    return [[0.0] * n for _ in range(m)]


def eye(n):
    """The n x n identity matrix."""
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = 1.0
    return out


def transpose(a):
    """A^T."""
    return [list(col) for col in zip(*a)]


def conj_transpose(a):
    """A^H, the conjugate transpose."""
    return [[v.conjugate() for v in col] for col in zip(*a)]


def matmul(a, b):
    """The product A B."""
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a, x):
    """The product A x."""
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def rmatvec(a, y):
    """The product A^H y."""
    n = len(a[0]) if a else 0
    out = [0.0] * n
    for row, yi in zip(a, y):
        if yi == 0:
            continue
        for j, v in enumerate(row):
            out[j] += v.conjugate() * yi
    return out


def dot(u, v):
    """<u, v> = sum_i conj(u_i) v_i. Images (lists of rows) are flattened."""
    return sum(a.conjugate() * b for a, b in zip(_flat(u), _flat(v)))


def norm2(x):
    """The Euclidean norm. Images (lists of rows) are flattened."""
    return math.sqrt(sum(abs(v) ** 2 for v in _flat(x)))


def solve(a, b):
    """Solve A x = b by Gaussian elimination with partial pivoting.

    b is a vector or a matrix (a list of rows). A must be square and
    nonsingular; a zero pivot raises ValueError. Fractions stay exact.
    """
    n = len(a)
    vec = not (b and isinstance(b[0], (list, tuple)))
    rhs = [[bi] for bi in b] if vec else [list(r) for r in b]
    m = [list(row) + rhs[i] for i, row in enumerate(a)]
    w = len(m[0])
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / piv
            if f != 0:
                mr, mc = m[r], m[c]
                for j in range(c, w):
                    mr[j] -= f * mc[j]
    x = [[0.0] * (w - n) for _ in range(n)]
    for r in range(n - 1, -1, -1):
        for j in range(w - n):
            s = m[r][n + j] - sum(m[r][k] * x[k][j] for k in range(r + 1, n))
            x[r][j] = s / m[r][r]
    return [row[0] for row in x] if vec else x


def cholesky(a):
    """Lower triangular L with A = L L^H for a Hermitian positive definite A."""
    n = len(a)
    low = zeros(n, n)
    for j in range(n):
        d = a[j][j] - sum(abs(low[j][k]) ** 2 for k in range(j))
        d = d.real if isinstance(d, complex) else d
        if not d > 0:
            raise ValueError("matrix is not positive definite")
        ljj = math.sqrt(d)
        low[j][j] = ljj
        for i in range(j + 1, n):
            s = a[i][j] - sum(low[i][k] * low[j][k].conjugate() for k in range(j))
            low[i][j] = s / ljj
    return low


def cho_solve(low, b):
    """Solve (L L^H) x = b, with L from cholesky."""
    n = len(low)
    z = [0.0] * n
    for i in range(n):
        z[i] = (b[i] - sum(low[i][k] * z[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = z[i] - sum(low[k][i].conjugate() * x[k] for k in range(i + 1, n))
        x[i] = s / low[i][i].conjugate()
    return x


def _rot_params(app, aqq, apq):
    """c, s of the Jacobi rotation that zeroes the (p, q) entry of [[app, apq], [apq, aqq]]."""
    theta = (aqq - app) / (2.0 * apq)
    t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
    c = 1.0 / math.sqrt(1.0 + t * t)
    return c, c * t


def sym_eig(a, tol=1e-15, max_sweeps=100):
    """Eigenvalues (ascending) and eigenvectors (as columns) of a real symmetric matrix.

    Cyclic Jacobi method. Returns (w, Q) with A = Q diag(w) Q^T.
    """
    n = len(a)
    m = [[float(v) for v in row] for row in a]
    q = eye(n)
    for _ in range(max_sweeps):
        off = sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        scale = sum(m[i][i] ** 2 for i in range(n)) + off
        if off <= (tol * tol) * scale or off == 0.0:
            break
        for p in range(n - 1):
            for r in range(p + 1, n):
                apq = m[p][r]
                if apq == 0.0:
                    continue
                c, s = _rot_params(m[p][p], m[r][r], apq)
                for k in range(n):
                    mkp, mkr = m[k][p], m[k][r]
                    m[k][p] = c * mkp - s * mkr
                    m[k][r] = s * mkp + c * mkr
                mp, mr = m[p], m[r]
                for k in range(n):
                    mpk, mrk = mp[k], mr[k]
                    mp[k] = c * mpk - s * mrk
                    mr[k] = s * mpk + c * mrk
                m[p][r] = m[r][p] = 0.0
                for k in range(n):
                    qkp, qkr = q[k][p], q[k][r]
                    q[k][p] = c * qkp - s * qkr
                    q[k][r] = s * qkp + c * qkr
    order = sorted(range(n), key=lambda i: m[i][i])
    w = [m[i][i] for i in order]
    qs = [[q[k][i] for i in order] for k in range(n)]
    return w, qs


def _complete(cols, m):
    """Replace zero columns of an m-row column list by unit vectors orthogonal to the others."""
    for idx, col in enumerate(cols):
        if any(v != 0.0 for v in col):
            continue
        for e in range(m):
            cand = [0.0] * m
            cand[e] = 1.0
            for _ in range(2):
                for jdx, other in enumerate(cols):
                    if jdx == idx or not any(v != 0.0 for v in other):
                        continue
                    h = sum(a * b for a, b in zip(other, cand))
                    cand = [a - h * b for a, b in zip(cand, other)]
            nrm = math.sqrt(sum(v * v for v in cand))
            if nrm > 0.5:
                cols[idx] = [v / nrm for v in cand]
                break
    return cols


def svd(a, tol=1e-15, max_sweeps=100):
    """Thin SVD of a real m x n matrix by one-sided Jacobi (Hestenes).

    Returns (U, S, V) with p = min(m, n): U is m x p, S a list of p values in
    descending order, V is n x p, U^T U = I, V^T V = I and A = U diag(S) V^T.
    """
    m, n = len(a), len(a[0])
    if m < n:
        v, s, u = svd(transpose(a), tol, max_sweeps)
        return u, s, v
    cols = [[float(a[i][j]) for i in range(m)] for j in range(n)]
    vcols = [[1.0 if i == j else 0.0 for i in range(n)] for j in range(n)]
    for _ in range(max_sweeps):
        rotated = False
        for p in range(n - 1):
            for r in range(p + 1, n):
                cp, cr = cols[p], cols[r]
                alpha = sum(x * x for x in cp)
                beta = sum(x * x for x in cr)
                gamma = sum(x * y for x, y in zip(cp, cr))
                if gamma == 0.0 or abs(gamma) <= tol * math.sqrt(alpha * beta):
                    continue
                rotated = True
                c, s = _rot_params(alpha, beta, gamma)
                cols[p] = [c * x - s * y for x, y in zip(cp, cr)]
                cols[r] = [s * x + c * y for x, y in zip(cp, cr)]
                vp, vr = vcols[p], vcols[r]
                vcols[p] = [c * x - s * y for x, y in zip(vp, vr)]
                vcols[r] = [s * x + c * y for x, y in zip(vp, vr)]
        if not rotated:
            break
    sig = [math.sqrt(sum(x * x for x in col)) for col in cols]
    # A column below 1e-150 times the largest one is zero to working precision;
    # its squares underflow, so its direction carries no information.
    floor = max(sig) * 1e-150 if sig else 0.0
    sig = [t if t > floor and t > 1e-150 else 0.0 for t in sig]
    order = sorted(range(n), key=lambda j: -sig[j])
    s_out = [sig[j] for j in order]
    ucols = [[x / sig[j] for x in cols[j]] if sig[j] > 0.0 else [0.0] * m for j in order]
    ucols = _complete(ucols, m)
    u = [[ucols[j][i] for j in range(n)] for i in range(m)]
    v = [[vcols[j][i] for j in order] for i in range(n)]
    return u, s_out, v


def adjoint_gap(apply_a, apply_ah, x, y):
    """|<A x, y> - <x, A^H y>| / (||A x|| ||y||) for given functions A and A^H.

    x and y may be vectors or images (lists of rows). If the denominator is
    zero, the absolute gap is returned.
    """
    ax = apply_a(x)
    gap = abs(dot(ax, y) - dot(x, apply_ah(y)))
    den = norm2(ax) * norm2(y)
    return gap / den if den > 0.0 else gap
