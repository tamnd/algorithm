# SPDX-License-Identifier: MIT
# Shared helper of the communications pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Complex baseband tools for the communications pages.

Vectors are lists of complex numbers. Matrices are lists of rows. The
functions here are plain building blocks: small linear algebra, convolution,
the DFT as a direct sum, the Gaussian Q function, dB conversion, complex
Gaussian noise and the Wilson score interval. No page algorithm (equalizer,
estimator, synchronizer, detector, precoder, demapper or power allocation)
lives in this file.

Conventions (prompts of the communications area):
- dft is X[k] = sum_n x[n] e^(-j 2 pi k n / N) with no factor; idft has 1/N.
- udft and uidft are the unitary pair, with 1/sqrt(N) on both sides.
- qfunc(x) = 0.5 erfc(x / sqrt(2)); it never computes 1 - Phi(x).
- cn(rng, var) draws CN(0, var): real and imaginary parts are independent
  with variance var / 2 each, so E|w|^2 = var.
"""

import cmath
import math
import random


# ---------------------------------------------------------------- vectors and matrices


def zeros(rows: int, cols: int | None = None) -> list:
    """A zero vector of length rows, or a rows by cols zero matrix."""
    if cols is None:
        return [0j] * rows
    return [[0j] * cols for _ in range(rows)]


def eye(n: int) -> list[list[complex]]:
    """The n by n identity matrix."""
    return [[1 + 0j if i == k else 0j for k in range(n)] for i in range(n)]


def add(a: list, b: list) -> list:
    """Elementwise a + b for two vectors or two matrices of the same shape."""
    if len(a) != len(b):
        raise ValueError("shapes differ")
    if a and isinstance(a[0], list):
        return [add(r, s) for r, s in zip(a, b)]
    return [x + y for x, y in zip(a, b)]


def sub(a: list, b: list) -> list:
    """Elementwise a - b for two vectors or two matrices of the same shape."""
    if len(a) != len(b):
        raise ValueError("shapes differ")
    if a and isinstance(a[0], list):
        return [sub(r, s) for r, s in zip(a, b)]
    return [x - y for x, y in zip(a, b)]


def scale(c: complex, a: list) -> list:
    """The scalar c times a vector or a matrix."""
    if a and isinstance(a[0], list):
        return [scale(c, r) for r in a]
    return [c * x for x in a]


def matmul(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    """The matrix product a b."""
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("inner dimensions differ")
    cols = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in cols] for row in a]


def matvec(a: list[list[complex]], x: list[complex]) -> list[complex]:
    """The matrix times vector product a x."""
    if a and len(a[0]) != len(x):
        raise ValueError("inner dimensions differ")
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def herm(a: list) -> list:
    """The conjugate transpose of a matrix. A vector gives its conjugate."""
    if a and isinstance(a[0], list):
        return [[complex(a[i][k]).conjugate() for i in range(len(a))] for k in range(len(a[0]))]
    return [complex(x).conjugate() for x in a]


def dot(x: list[complex], y: list[complex]) -> complex:
    """The inner product x^H y = sum of conj(x_i) y_i."""
    if len(x) != len(y):
        raise ValueError("lengths differ")
    return sum(complex(p).conjugate() * q for p, q in zip(x, y))


def norm2(x: list) -> float:
    """The squared Euclidean norm sum |x_i|^2 (squared Frobenius norm for a matrix)."""
    if x and isinstance(x[0], list):
        return sum(norm2(r) for r in x)
    return sum(abs(v) ** 2 for v in x)


# ---------------------------------------------------------------- linear systems


def _lu(a: list[list[complex]]) -> tuple[list[list[complex]], list[int], int]:
    """LU factorization with partial pivoting. Returns (lu, perm, sign)."""
    n = len(a)
    if any(len(r) != n for r in a):
        raise ValueError("matrix is not square")
    m = [[complex(v) for v in r] for r in a]
    perm = list(range(n))
    sign = 1
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(m[i][k]))
        if abs(m[p][k]) == 0.0:
            raise ValueError("matrix is singular")
        if p != k:
            m[k], m[p] = m[p], m[k]
            perm[k], perm[p] = perm[p], perm[k]
            sign = -sign
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            m[i][k] = f
            if f != 0:
                rk, ri = m[k], m[i]
                for c in range(k + 1, n):
                    ri[c] -= f * rk[c]
    return m, perm, sign


def _lu_solve(lu: list[list[complex]], perm: list[int], b: list[complex]) -> list[complex]:
    n = len(lu)
    y = [complex(b[perm[i]]) for i in range(n)]
    for i in range(n):
        for c in range(i):
            y[i] -= lu[i][c] * y[c]
    for i in range(n - 1, -1, -1):
        for c in range(i + 1, n):
            y[i] -= lu[i][c] * y[c]
        y[i] /= lu[i][i]
    return y


def solve(a: list[list[complex]], b: list) -> list:
    """Solve a x = b by Gaussian elimination with partial pivoting.

    b is a vector, or a matrix whose columns are right-hand sides.
    Raises ValueError if a is singular.
    """
    lu, perm, _ = _lu(a)
    if b and isinstance(b[0], list):
        cols = [list(c) for c in zip(*b)]
        xs = [_lu_solve(lu, perm, c) for c in cols]
        return [list(r) for r in zip(*xs)]
    if len(b) != len(a):
        raise ValueError("lengths differ")
    return _lu_solve(lu, perm, b)


def inv(a: list[list[complex]]) -> list[list[complex]]:
    """The inverse of a square matrix."""
    return solve(a, eye(len(a)))


def det(a: list[list[complex]]) -> complex:
    """The determinant of a square matrix (0 for a singular matrix)."""
    try:
        lu, _, sign = _lu(a)
    except ValueError as e:
        if "singular" in str(e):
            return 0j
        raise
    d = complex(sign)
    for i in range(len(lu)):
        d *= lu[i][i]
    return d


def cholesky(a: list[list[complex]]) -> list[list[complex]]:
    """The lower triangular L with a = L L^H, for a Hermitian positive definite a.

    Raises ValueError if a is not positive definite (to rounding).
    """
    n = len(a)
    low = zeros(n, n)
    for i in range(n):
        for k in range(i + 1):
            s = complex(a[i][k]) - sum(low[i][c] * low[k][c].conjugate() for c in range(k))
            if i == k:
                if s.real <= 0.0:
                    raise ValueError("matrix is not positive definite")
                low[i][i] = complex(math.sqrt(s.real))
            else:
                low[i][k] = s / low[k][k].real
    return low


# ---------------------------------------------------------------- convolution and the DFT


def conv(a: list[complex], b: list[complex]) -> list[complex]:
    """Linear convolution, of length len(a) + len(b) - 1."""
    if not a or not b:
        return []
    out = [0j] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for k, y in enumerate(b):
            out[i + k] += x * y
    return out


def cconv(a: list[complex], b: list[complex], n: int | None = None) -> list[complex]:
    """Circular convolution of length n (default: the longer length).

    Both inputs are padded with zeros to length n, or must not be longer than n.
    """
    if n is None:
        n = max(len(a), len(b))
    if len(a) > n or len(b) > n:
        raise ValueError("input longer than n")
    out = [0j] * n
    for i, x in enumerate(a):
        for k, y in enumerate(b):
            out[(i + k) % n] += x * y
    return out


def _twiddles(n: int, sign: int) -> list[complex]:
    return [cmath.exp(sign * 2j * math.pi * t / n) for t in range(n)]


def dft(x: list[complex]) -> list[complex]:
    """X[k] = sum over n of x[n] e^(-j 2 pi k n / N), as a direct O(N^2) sum."""
    n = len(x)
    w = _twiddles(n, -1)
    return [sum(x[t] * w[(k * t) % n] for t in range(n)) for k in range(n)]


def idft(xf: list[complex]) -> list[complex]:
    """x[n] = (1/N) sum over k of X[k] e^(j 2 pi k n / N), the inverse of dft."""
    n = len(xf)
    w = _twiddles(n, 1)
    return [sum(xf[k] * w[(k * t) % n] for k in range(n)) / n for t in range(n)]


def udft(x: list[complex]) -> list[complex]:
    """The unitary DFT: dft(x) / sqrt(N)."""
    s = 1.0 / math.sqrt(len(x)) if x else 1.0
    return [v * s for v in dft(x)]


def uidft(xf: list[complex]) -> list[complex]:
    """The unitary inverse DFT: sqrt(N) idft(X), the inverse of udft."""
    s = math.sqrt(len(xf)) if xf else 1.0
    return [v * s for v in idft(xf)]


# ---------------------------------------------------------------- Q function and dB


def qfunc(x: float) -> float:
    """Q(x) = P(Z > x) for a standard normal Z, computed as 0.5 erfc(x / sqrt(2))."""
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def qinv(p: float) -> float:
    """The x with Q(x) = p, for 0 < p < 1, by bisection on Q (which decreases)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if qfunc(mid) > p:
            lo = mid
        else:
            hi = mid
        if hi - lo <= 1e-15 * max(1.0, abs(mid)):
            break
    return 0.5 * (lo + hi)


def db(x: float) -> float:
    """10 log10(x), for a ratio of powers or energies."""
    return 10.0 * math.log10(x)


def undb(d: float) -> float:
    """10^(d / 10), the inverse of db."""
    return 10.0 ** (d / 10.0)


# ---------------------------------------------------------------- noise and statistics


def cn(rng: random.Random, var: float) -> complex:
    """One sample of CN(0, var): independent real and imaginary parts of variance var / 2."""
    s = math.sqrt(var / 2.0)
    return complex(rng.gauss(0.0, s), rng.gauss(0.0, s))


def awgn(rng: random.Random, x: list[complex], n0: float) -> list[complex]:
    """x plus independent CN(0, n0) noise on each sample."""
    return [v + cn(rng, n0) for v in x]


def wilson(k: int, n: int, z: float = 3.29) -> tuple[float, float]:
    """The Wilson score interval for k successes in n trials (z = 3.29 is about 0.999 two-sided)."""
    if n <= 0 or not 0 <= k <= n:
        raise ValueError("need 0 <= k <= n and n > 0")
    p = k / n
    z2 = z * z
    den = 1.0 + z2 / n
    mid = (p + z2 / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / den
    return max(0.0, mid - half), min(1.0, mid + half)
