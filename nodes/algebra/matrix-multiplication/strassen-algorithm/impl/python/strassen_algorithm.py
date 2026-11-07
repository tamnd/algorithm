# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strassen-algorithm/. The authors are listed in prov/MZ8PBV.jsonl.

Matrix = list[list[int]]


def _classical(a: Matrix, b: Matrix, p: int, mod: int | None) -> Matrix:
    m = len(b)
    c = [[0] * p for _ in range(len(a))]
    for i, row in enumerate(a):
        ci = c[i]
        for k in range(m):
            aik = row[k]
            if aik:
                bk = b[k]
                for j in range(p):
                    ci[j] += aik * bk[j]
        if mod is not None:
            c[i] = [x % mod for x in ci]
    return c


def _add(x: Matrix, y: Matrix, mod: int | None) -> Matrix:
    if mod is None:
        return [[u + v for u, v in zip(r, s)] for r, s in zip(x, y)]
    return [[(u + v) % mod for u, v in zip(r, s)] for r, s in zip(x, y)]


def _sub(x: Matrix, y: Matrix, mod: int | None) -> Matrix:
    if mod is None:
        return [[u - v for u, v in zip(r, s)] for r, s in zip(x, y)]
    return [[(u - v) % mod for u, v in zip(r, s)] for r, s in zip(x, y)]


def _block(x: Matrix, r0: int, r1: int, c0: int, c1: int) -> Matrix:
    return [row[c0:c1] for row in x[r0:r1]]


def strassen_algorithm(a: Matrix, b: Matrix, p: int | None = None, mod: int | None = None, n0: int = 1) -> Matrix:
    """Return a * b by Strassen's seven-product recursion.

    a is n x m and b is m x p (lists of rows); pass p when m = 0. The ring is
    Z, or Z/mod Z when mod is set. Inputs with a side of at most n0 (n0 >= 1)
    use the classical product; odd sides are padded by one zero row or column
    at each level. Cost: O(n^(log2 7)) ring operations for n x n inputs;
    recursion depth O(log max(n, m, p)).
    """
    if n0 < 1:
        raise ValueError("the cutoff n0 must be at least 1")
    n, m = len(a), len(b)
    if p is None:
        p = len(b[0]) if m > 0 else 0
    if any(len(row) != m for row in a) or any(len(row) != p for row in b):
        raise ValueError("the shapes do not match")
    return _strassen(a, b, n, m, p, mod, n0)


def _strassen(a: Matrix, b: Matrix, n: int, m: int, p: int, mod: int | None, n0: int) -> Matrix:
    if min(n, m, p) <= n0:  # @line L1
        return _classical(a, b, p, mod)
    if n % 2 or m % 2 or p % 2:  # @line L2
        n2, m2, p2 = n + n % 2, m + m % 2, p + p % 2
        ap = [row + [0] * (m2 - m) for row in a] + [[0] * m2 for _ in range(n2 - n)]
        bp = [row + [0] * (p2 - p) for row in b] + [[0] * p2 for _ in range(m2 - m)]
        cp = _strassen(ap, bp, n2, m2, p2, mod, n0)
        return [row[:p] for row in cp[:n]]
    h, k, q = n // 2, m // 2, p // 2  # @line L3
    a11, a12 = _block(a, 0, h, 0, k), _block(a, 0, h, k, m)
    a21, a22 = _block(a, h, n, 0, k), _block(a, h, n, k, m)
    b11, b12 = _block(b, 0, k, 0, q), _block(b, 0, k, q, p)
    b21, b22 = _block(b, k, m, 0, q), _block(b, k, m, q, p)

    def rec(x: Matrix, y: Matrix) -> Matrix:
        return _strassen(x, y, h, k, q, mod, n0)

    m1 = rec(_add(a11, a22, mod), _add(b11, b22, mod))  # @line L4
    m2 = rec(_add(a21, a22, mod), b11)  # @line L5
    m3 = rec(a11, _sub(b12, b22, mod))  # @line L6
    m4 = rec(a22, _sub(b21, b11, mod))  # @line L7
    m5 = rec(_add(a11, a12, mod), b22)  # @line L8
    m6 = rec(_sub(a21, a11, mod), _add(b11, b12, mod))  # @line L9
    m7 = rec(_sub(a12, a22, mod), _add(b21, b22, mod))  # @line L10
    c11 = _add(_sub(_add(m1, m4, mod), m5, mod), m7, mod)  # @line L11
    c12 = _add(m3, m5, mod)  # @line L12
    c21 = _add(m2, m4, mod)  # @line L13
    c22 = _add(_add(_sub(m1, m2, mod), m3, mod), m6, mod)  # @line L14
    return [r + s for r, s in zip(c11, c12)] + [r + s for r, s in zip(c21, c22)]  # @line L15


def count_operations(n: int, n0: int = 1) -> int:
    """Ring operations of the method on n x n inputs with n a power of two: 7 T(n/2) + 18 (n/2)^2."""
    if n <= n0:
        return 2 * n**3 - n**2
    return 7 * count_operations(n // 2, n0) + 18 * (n // 2) ** 2
