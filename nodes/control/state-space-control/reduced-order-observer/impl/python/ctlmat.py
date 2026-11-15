# SPDX-License-Identifier: MIT
# Shared helper of the control pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small dense linear algebra and polynomial routines for the control pages.

Conventions:
- A matrix is a list of rows. Entries are int, float, Fraction or complex.
- A vector is a flat list of scalars. matvec, dot, solve (with a vector
  right side), vec and unvec use flat lists.
- A polynomial is a list of coefficients, highest power first, so
  [1, 3, 2] is s^2 + 3 s + 2.
- Routines that divide (solve, inv, det, charpoly) compute in Fraction when
  every entry is an int or a Fraction, so the result is exact. With float or
  complex entries they compute in floating point.
- transpose does not conjugate complex entries.

Floating point tolerances:
- expm: scaling and squaring with a Taylor series; the scaled matrix has
  infinity norm at most 1/2 and the series stops when a term is below
  2^-60 times the sum. For matrices that are not far from normal the relative
  error is near 1e-14.
- polyroots: Durand-Kerner iteration, then a Newton polish. Simple roots of a
  well conditioned polynomial come out with a relative error near 1e-12 (the
  tests ask for 1e-9). A root of multiplicity k is ill conditioned: its error
  grows like 1e-16^(1/k), about 1e-8 for a double root and 1e-3 for a
  fourfold root. For real coefficients the output is closed under
  conjugation.
- is_pos_def with float entries: the matrix must be symmetric within
  1e-12 times its largest entry, and the Cholesky pivots of A - margin I must
  be positive.

This file holds no algorithm of a control page.
"""

import cmath
import math
from fractions import Fraction

__all__ = [
    "zeros", "eye", "add", "sub", "scale", "mul", "transpose", "matvec",
    "dot", "norm2", "block", "kron", "vec", "unvec", "solve", "inv", "det",
    "trace", "charpoly", "polyval", "polyadd", "polymul", "polyder",
    "polyroots", "expm", "mat_power", "is_symmetric", "is_pos_def",
]


def _is_exact(v):
    return isinstance(v, (int, Fraction))


def _all_exact(*mats):
    for m in mats:
        for row in m:
            if isinstance(row, list):
                for v in row:
                    if not _is_exact(v):
                        return False
            elif not _is_exact(row):
                return False
    return True


def _to_fraction(a):
    return [[Fraction(v) for v in row] for row in a]


def _shape(a):
    return len(a), (len(a[0]) if a else 0)


def zeros(n, m=None):
    """Return the n by m zero matrix (n by n if m is None), with int entries."""
    if m is None:
        m = n
    return [[0] * m for _ in range(n)]


def eye(n):
    """Return the n by n identity matrix, with int entries."""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def add(a, b):
    """Return a + b."""
    if _shape(a) != _shape(b):
        raise ValueError("add: shapes differ")
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def sub(a, b):
    """Return a - b."""
    if _shape(a) != _shape(b):
        raise ValueError("sub: shapes differ")
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(c, a):
    """Return the scalar c times the matrix a."""
    return [[c * x for x in row] for row in a]


def mul(a, b):
    """Return the matrix product a b."""
    n, k = _shape(a)
    k2, m = _shape(b)
    if k != k2:
        raise ValueError("mul: inner dimensions differ")
    bt = list(zip(*b)) if b else []
    out = []
    for row in a:
        out_row = []
        for col in bt:
            s = 0
            for x, y in zip(row, col):
                s += x * y
            out_row.append(s)
        out.append(out_row)
    return out


def transpose(a):
    """Return the transpose of a (no complex conjugation)."""
    return [list(col) for col in zip(*a)]


def matvec(a, x):
    """Return the vector a x, for a flat list x."""
    if a and len(a[0]) != len(x):
        raise ValueError("matvec: dimensions differ")
    out = []
    for row in a:
        s = 0
        for v, w in zip(row, x):
            s += v * w
        out.append(s)
    return out


def dot(x, y):
    """Return sum of x_i y_i (no complex conjugation)."""
    if len(x) != len(y):
        raise ValueError("dot: lengths differ")
    s = 0
    for v, w in zip(x, y):
        s += v * w
    return s


def _sym_eigvals(s):
    """Eigenvalues of a real symmetric float matrix by cyclic Jacobi."""
    n = len(s)
    a = [list(map(float, row)) for row in s]
    for _ in range(100):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        diag = sum(a[i][i] ** 2 for i in range(n))
        if off <= 1e-30 * max(diag, 1e-300):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - sn * akq
                    a[k][q] = sn * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - sn * aqk
                    a[q][k] = sn * apk + c * aqk
    return [a[i][i] for i in range(n)]


def norm2(x):
    """Return the 2-norm.

    For a flat vector this is the Euclidean norm. For a matrix it is the
    induced 2-norm (the largest singular value), computed from the
    eigenvalues of M^T M by the Jacobi method, where M is a real matrix with
    the same singular values. The result is a float.
    """
    if not x:
        return 0.0
    if not isinstance(x[0], list):
        return math.sqrt(sum(abs(complex(v)) ** 2 for v in x))
    if any(isinstance(v, complex) for row in x for v in row):
        re = [[complex(v).real for v in row] for row in x]
        im = [[complex(v).imag for v in row] for row in x]
        m = block([[re, scale(-1, im)], [im, re]])
    else:
        m = [[float(v) for v in row] for row in x]
    g = mul(transpose(m), m)
    lam = max(_sym_eigvals(g))
    return math.sqrt(max(lam, 0.0))


def block(rows):
    """Build a matrix from a list of rows of blocks.

    A block is a matrix, or the int 0 for a zero block whose size is taken
    from the other blocks in its block row and block column.
    """
    heights = []
    for r in rows:
        h = None
        for b in r:
            if isinstance(b, list):
                h = len(b)
                break
        if h is None:
            raise ValueError("block: a block row has no matrix block")
        heights.append(h)
    ncols = len(rows[0])
    widths = []
    for j in range(ncols):
        w = None
        for r in rows:
            if isinstance(r[j], list):
                w = len(r[j][0]) if r[j] else 0
                break
        if w is None:
            raise ValueError("block: a block column has no matrix block")
        widths.append(w)
    out = []
    for r, h in zip(rows, heights):
        if len(r) != ncols:
            raise ValueError("block: block rows have different lengths")
        for i in range(h):
            line = []
            for b, w in zip(r, widths):
                if isinstance(b, list):
                    if len(b) != h or (b and len(b[0]) != w):
                        raise ValueError("block: block sizes do not match")
                    line.extend(b[i])
                elif b == 0:
                    line.extend([0] * w)
                else:
                    raise ValueError("block: a scalar block must be 0")
            out.append(line)
    return out


def kron(a, b):
    """Return the Kronecker product of a and b."""
    n, m = _shape(a)
    p, q = _shape(b)
    return [[a[i // p][j // q] * b[i % p][j % q] for j in range(m * q)] for i in range(n * p)]


def vec(a):
    """Stack the columns of a into one flat list."""
    n, m = _shape(a)
    return [a[i][j] for j in range(m) for i in range(n)]


def unvec(v, n, m=None):
    """Inverse of vec: return the n by m matrix whose stacked columns are v."""
    if m is None:
        m = len(v) // n
    if n * m != len(v):
        raise ValueError("unvec: length does not match the shape")
    return [[v[j * n + i] for j in range(m)] for i in range(n)]


def solve(a, b):
    """Solve a x = b by Gaussian elimination with partial pivoting.

    b is a flat vector or a matrix; the result has the same form. With int
    and Fraction entries the result is exact (Fraction). Raises ValueError
    if a is singular (an exactly zero pivot).
    """
    n, m = _shape(a)
    if n != m:
        raise ValueError("solve: matrix is not square")
    is_vec = not (b and isinstance(b[0], list))
    rhs = [[v] for v in b] if is_vec else [list(row) for row in b]
    if len(rhs) != n:
        raise ValueError("solve: right side has the wrong length")
    if _all_exact(a, rhs):
        aa = _to_fraction(a)
        rhs = _to_fraction(rhs)
    else:
        aa = [list(row) for row in a]
    k = len(rhs[0]) if rhs else 0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(aa[r][c]))
        if aa[p][c] == 0:
            raise ValueError("solve: matrix is singular")
        if p != c:
            aa[c], aa[p] = aa[p], aa[c]
            rhs[c], rhs[p] = rhs[p], rhs[c]
        piv = aa[c][c]
        for r in range(c + 1, n):
            f = aa[r][c] / piv
            if f == 0:
                continue
            row_r, row_c = aa[r], aa[c]
            for j in range(c, n):
                row_r[j] -= f * row_c[j]
            rr, rc = rhs[r], rhs[c]
            for j in range(k):
                rr[j] -= f * rc[j]
    x = [[0] * k for _ in range(n)]
    for c in range(n - 1, -1, -1):
        for j in range(k):
            s = rhs[c][j]
            for t in range(c + 1, n):
                s -= aa[c][t] * x[t][j]
            x[c][j] = s / aa[c][c]
    return [row[0] for row in x] if is_vec else x


def inv(a):
    """Return the inverse of a (exact with int and Fraction entries)."""
    return solve(a, eye(len(a)))


def det(a):
    """Return the determinant of a by elimination with partial pivoting.

    With int and Fraction entries the result is an exact Fraction.
    """
    n, m = _shape(a)
    if n != m:
        raise ValueError("det: matrix is not square")
    aa = _to_fraction(a) if _all_exact(a) else [list(row) for row in a]
    d = Fraction(1) if _all_exact(a) else 1.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(aa[r][c]))
        if aa[p][c] == 0:
            return d * 0
        if p != c:
            aa[c], aa[p] = aa[p], aa[c]
            d = -d
        piv = aa[c][c]
        d *= piv
        for r in range(c + 1, n):
            f = aa[r][c] / piv
            if f == 0:
                continue
            for j in range(c, n):
                aa[r][j] -= f * aa[c][j]
    return d


def trace(a):
    """Return the sum of the diagonal entries of a."""
    s = 0
    for i in range(len(a)):
        s += a[i][i]
    return s


def charpoly(a):
    """Return [1, a_1, ..., a_n] with det(s I - A) = s^n + a_1 s^(n-1) + ... + a_n.

    Uses the Faddeev-LeVerrier recursion M_k = A M_(k-1) + a_(k-1) I,
    a_k = -trace(A M_k) / k. Exact with int and Fraction entries.
    """
    n, m = _shape(a)
    if n != m:
        raise ValueError("charpoly: matrix is not square")
    aa = _to_fraction(a) if _all_exact(a) else [list(row) for row in a]
    coeffs = [1]
    mk = zeros(n)
    for k in range(1, n + 1):
        mk = mul(aa, mk)
        c = coeffs[-1]
        for i in range(n):
            mk[i][i] += c
        am = mul(aa, mk)
        coeffs.append(-trace(am) / k)
    return coeffs


def polyval(p, x):
    """Evaluate the polynomial p at x by Horner's rule."""
    s = 0
    for c in p:
        s = s * x + c
    return s


def _strip(p):
    i = 0
    while i < len(p) - 1 and p[i] == 0:
        i += 1
    return list(p[i:]) if p else [0]


def polyadd(p, q):
    """Return p + q, with exactly zero leading coefficients removed."""
    n = max(len(p), len(q))
    pp = [0] * (n - len(p)) + list(p)
    qq = [0] * (n - len(q)) + list(q)
    return _strip([x + y for x, y in zip(pp, qq)])


def polymul(p, q):
    """Return the product p q."""
    if not p or not q:
        return [0]
    out = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return _strip(out)


def polyder(p):
    """Return the derivative of p."""
    n = len(p) - 1
    if n <= 0:
        return [0]
    return _strip([c * (n - i) for i, c in enumerate(p[:-1])])


def polyroots(p, tol=1e-15, maxiter=1000):
    """Return the complex roots of p, sorted by real part, then imaginary part.

    Durand-Kerner (Weierstrass) iteration from points on a circle, stopped
    when every relative correction is below tol, then a Newton polish of
    each root. For real coefficients the roots are made exactly real or
    exact conjugate pairs. See the module notes for the accuracy.
    """
    c = [complex(v) for v in p]
    while c and c[0] == 0:
        c.pop(0)
    if not c:
        raise ValueError("polyroots: zero polynomial")
    real_coeffs = all(v.imag == 0 for v in c)
    origin = 0
    while len(c) > 1 and c[-1] == 0:
        c.pop()
        origin += 1
    n = len(c) - 1
    a = [v / c[0] for v in c]
    if n == 0:
        z = []
    elif n == 1:
        z = [-a[1]]
    else:
        r = 2.0 * max(abs(a[k]) ** (1.0 / k) for k in range(1, n + 1))
        if r == 0:
            r = 1.0
        z = [r * cmath.exp(1j * (2 * math.pi * k / n + 0.4)) for k in range(n)]
        for _ in range(maxiter):
            worst = 0.0
            for i in range(n):
                den = 1.0 + 0j
                for j in range(n):
                    if j != i:
                        den *= z[i] - z[j]
                if den == 0:
                    z[i] += 1e-8 * (1 + abs(z[i])) * cmath.exp(1j * (i + 1))
                    worst = 1.0
                    continue
                d = polyval(a, z[i]) / den
                z[i] -= d
                worst = max(worst, abs(d) / (1.0 + abs(z[i])))
            if worst < tol:
                break
        dp = polyder(a)
        for i in range(n):
            zi = z[i]
            fz = abs(polyval(a, zi))
            for _ in range(5):
                der = polyval(dp, zi)
                if der == 0 or fz == 0:
                    break
                step = polyval(a, zi) / der
                if abs(step) > 1e-6 * (1.0 + abs(zi)):
                    break
                znew = zi - step
                fnew = abs(polyval(a, znew))
                if fnew >= fz:
                    break
                zi, fz = znew, fnew
            z[i] = zi
    z = z + [0j] * origin
    if real_coeffs:
        thr = 1e-9
        upper = [v for v in z if v.imag > thr * (1 + abs(v))]
        lower = [v for v in z if v.imag < -thr * (1 + abs(v))]
        reals = [complex(v.real, 0.0) for v in z if abs(v.imag) <= thr * (1 + abs(v))]
        # A cluster of close roots can leave more roots above the real axis
        # than below it (or the other way). The extra roots nearest to the
        # axis are then taken as real, so the output is closed under
        # conjugation.
        if len(upper) < len(lower):
            upper, lower = [v.conjugate() for v in lower], [v.conjugate() for v in upper]
        upper.sort(key=lambda v: v.imag)
        extra = len(upper) - len(lower)
        reals += [complex(v.real, 0.0) for v in upper[:extra]]
        upper = upper[extra:]
        out = list(reals)
        rest = list(lower)
        for u in upper:
            w = min(rest, key=lambda v: abs(v - u.conjugate()))
            rest.remove(w)
            re = (u.real + w.real) / 2
            im = (u.imag - w.imag) / 2
            out.append(complex(re, im))
            out.append(complex(re, -im))
        z = out
    return sorted(z, key=lambda v: (v.real, v.imag))


def _norm_inf(a):
    return max((sum(abs(v) for v in row) for row in a), default=0.0)


def expm(a):
    """Return e^A in floating point by scaling and squaring with a Taylor series.

    A is scaled by 2^-s so that its infinity norm is at most 1/2, the Taylor
    series of the scaled matrix is summed until a term is below 2^-60 of the
    sum, and the result is squared s times. Entries of the result are float
    (complex if A has complex entries).
    """
    n, m = _shape(a)
    if n != m:
        raise ValueError("expm: matrix is not square")
    cplx = any(isinstance(v, complex) for row in a for v in row)
    conv = complex if cplx else float
    x = [[conv(v) for v in row] for row in a]
    nrm = _norm_inf(x)
    s = 0
    while nrm > 0.5:
        nrm /= 2.0
        s += 1
    x = scale(conv(2.0 ** -s), x)
    e = [[conv(1.0 if i == j else 0.0) for j in range(n)] for i in range(n)]
    term = [row[:] for row in e]
    for k in range(1, 60):
        term = scale(1.0 / k, mul(term, x))
        e = add(e, term)
        tn = _norm_inf(term)
        if tn == 0.0 or tn <= 2.0 ** -60 * _norm_inf(e):
            break
    for _ in range(s):
        e = mul(e, e)
    return e


def mat_power(a, k):
    """Return A^k for an int k by repeated squaring (A^0 = I; k < 0 uses inv)."""
    n, m = _shape(a)
    if n != m:
        raise ValueError("mat_power: matrix is not square")
    if k < 0:
        a = inv(a)
        k = -k
    result = eye(n)
    base = [list(row) for row in a]
    while k:
        if k & 1:
            result = mul(result, base)
        k >>= 1
        if k:
            base = mul(base, base)
    return result


def is_symmetric(a, tol=0):
    """Return True if a is square and |a_ij - a_ji| <= tol for all i, j."""
    n, m = _shape(a)
    if n != m:
        return False
    return all(abs(a[i][j] - a[j][i]) <= tol for i in range(n) for j in range(i + 1, n))


def is_pos_def(a, margin=0):
    """Return True if a is symmetric and a - margin I is positive definite.

    With int and Fraction entries (and an exact margin) the test is exact:
    every leading principal minor of a - margin I must be positive
    (Sylvester's criterion), computed in Fraction. With float entries the
    matrix must be symmetric within 1e-12 times its largest entry, and the
    Cholesky factorization of a - margin I must have positive pivots.
    Complex entries are not accepted.
    """
    n, m = _shape(a)
    if n != m:
        return False
    if any(isinstance(v, complex) for row in a for v in row):
        raise ValueError("is_pos_def: complex entries are not accepted")
    if _all_exact(a) and _is_exact(margin):
        b = [[Fraction(a[i][j]) - (Fraction(margin) if i == j else 0) for j in range(n)] for i in range(n)]
        if not is_symmetric(b):
            return False
        return all(det([row[:k] for row in b[:k]]) > 0 for k in range(1, n + 1))
    b = [[float(a[i][j]) - (float(margin) if i == j else 0.0) for j in range(n)] for i in range(n)]
    big = max((abs(float(v)) for row in a for v in row), default=0.0)
    if not is_symmetric(b, 1e-12 * max(big, 1e-300)):
        return False
    low = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d = b[j][j] - sum(low[j][k] ** 2 for k in range(j))
        if not d > 0.0:
            return False
        low[j][j] = math.sqrt(d)
        for i in range(j + 1, n):
            low[i][j] = (b[i][j] - sum(low[i][k] * low[j][k] for k in range(j))) / low[j][j]
    return True


def _self_test():
    a = [[0, 1], [-2, -3]]
    assert charpoly(a) == [1, 3, 2]
    assert det(a) == 2
    assert mul(inv(a), a) == eye(2)
    assert solve(a, [1, 0]) == [Fraction(-3, 2), Fraction(1)]
    r = polyroots([1, 3, 2])
    assert abs(r[0] + 2) < 1e-12 and abs(r[1] + 1) < 1e-12
    t = 0.7
    e = expm([[0.0, t], [-t, 0.0]])
    want = [[math.cos(t), math.sin(t)], [-math.sin(t), math.cos(t)]]
    assert max(abs(e[i][j] - want[i][j]) for i in range(2) for j in range(2)) < 1e-14
    assert is_pos_def([[Fraction(5, 4), Fraction(1, 4)], [Fraction(1, 4), Fraction(1, 4)]])
    assert not is_pos_def([[1, 2], [2, 1]])
    assert abs(norm2([[3.0, 0.0], [0.0, -4.0]]) - 4.0) < 1e-12
    return True


if __name__ == "__main__":
    _self_test()
