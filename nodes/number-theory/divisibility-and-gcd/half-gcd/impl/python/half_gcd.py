# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/half-gcd/. The authors are listed in prov/NZPF3Q.jsonl.

"""Half-GCD: a divide and conquer gcd for arbitrary precision integers.

``half_gcd(a, b)`` runs the Euclidean algorithm on a > b >= 0 up to the
first remainder below 2^m, with m = ceil(bitlength(a) / 2), and returns the
pair reached together with the 2 x 2 matrix of the quotients used. It finds
most quotients from the leading halves of the numbers, by two recursive calls
on numbers of about half the length. ``fast_gcd`` calls it in a loop.

Cost: O(M(n) log n) bit operations for n-bit inputs, where M(n) is the cost
of one n-bit multiplication. Python multiplies with Karatsuba's method, so
M(n) = O(n^1.59) here. The recursion depth is about log2(n / threshold).
"""

Matrix = tuple[int, int, int, int]  # (m00, m01, m10, m11), row by row

IDENTITY: Matrix = (1, 0, 0, 1)


def _mul(m: Matrix, n: Matrix) -> Matrix:
    a, b, c, d = m
    e, f, g, h = n
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)


def _times_q(m: Matrix, q: int) -> Matrix:
    """Return m times the quotient matrix [[q, 1], [1, 0]]."""
    a, b, c, d = m
    return (a * q + b, a, c * q + d, c)


def _fixup(
    r: Matrix, qs: list[int], a: int, b: int, limit: int
) -> tuple[Matrix, list[int], int, int]:
    """Apply r^-1 to (a, b), then undo trailing quotients until valid.

    Unless every quotient is undone (then r is the identity and the result is
    (a, b) itself), the result satisfies alpha > beta > 0 and alpha >= limit,
    which makes it a pair of consecutive Euclidean remainders of (a, b).
    """
    m00, m01, m10, m11 = r
    det = m00 * m11 - m01 * m10  # +1 or -1
    alpha = det * (m11 * a - m01 * b)  # @line L11
    beta = det * (m00 * b - m10 * a)
    while qs and not (alpha > beta > 0 and alpha >= limit):  # @line L12
        q = qs.pop()
        a0, a1, a2, a3 = r
        r = (a1, a0 - q * a1, a3, a2 - q * a3)  # r times [[0, 1], [1, -q]]
        alpha, beta = q * alpha + beta, alpha
    return r, qs, alpha, beta  # @line L13


def half_gcd(
    a: int, b: int, threshold: int = 64
) -> tuple[Matrix, list[int], int, int]:
    """Run Euclid on a > b >= 0 until the first remainder below 2^m.

    Precondition: a > b >= 0 (a == b > 0 is also accepted), threshold >= 2.
    Returns (M, qs, alpha, beta): qs are the Euclidean quotients used,
    M = [[q1, 1], [1, 0]] ... [[qk, 1], [1, 0]], (a, b) = M (alpha, beta),
    and alpha >= 2^m > beta with m = ceil(bitlength(a) / 2).
    """
    if a < b or b < 0:
        raise ValueError("half_gcd needs a >= b >= 0")
    n = a.bit_length()
    m = (n + 1) // 2  # @line L1
    limit = 1 << m
    mat: Matrix = IDENTITY
    qs: list[int] = []
    if b < limit:  # @line L2
        return mat, qs, a, b
    if n <= threshold:  # @line L3
        while b >= limit:
            q, rem = divmod(a, b)
            a, b = b, rem
            mat = _times_q(mat, q)
            qs.append(q)
        return mat, qs, a, b
    r, rq, _, _ = half_gcd(a >> m, b >> m, threshold)  # @line L4
    mat, qs, a, b = _fixup(r, rq, a, b, limit)  # @line L5
    if b >= limit:  # @line L6
        q, rem = divmod(a, b)
        a, b = b, rem
        mat = _times_q(mat, q)
        qs.append(q)
        if b >= limit and 2 * (a.bit_length() - m) < n:  # @line L7
            k = 2 * m - a.bit_length()
            s, sq, _, _ = half_gcd(a >> k, b >> k, threshold)
            s, sq, a, b = _fixup(s, sq, a, b, limit)  # @line L8
            mat = _mul(mat, s)
            qs.extend(sq)
    while b >= limit:  # @line L9
        q, rem = divmod(a, b)
        a, b = b, rem
        mat = _times_q(mat, q)
        qs.append(q)
    return mat, qs, a, b  # @line L10


def fast_gcd(a: int, b: int, threshold: int = 64) -> int:
    """Return gcd(a, b) >= 0 for any integers, with gcd(0, 0) = 0.

    Signs are dropped first. Cost O(M(n) log n) bit operations.
    """
    a, b = abs(a), abs(b)  # @line L14
    if a < b:
        a, b = b, a
    while b.bit_length() > threshold:  # @line L15
        _, _, a, b = half_gcd(a, b, threshold)
        if b != 0:
            a, b = b, a % b
    while b != 0:  # @line L16
        a, b = b, a % b
    return a  # @line L17
