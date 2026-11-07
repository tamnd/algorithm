# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-raphson-division/. The authors are listed in prov/NDCZEW.jsonl.

"""Division by a Newton reciprocal, with the precision doubled at each step.

reciprocal(D) returns R = floor(4^B / D) for a divisor D of exactly B binary
digits. It calls itself on the top half of D, does one Newton step
X <- X + X (4^B - D X) / 4^B, and corrects the result with additions only.
divide(A, D) uses R to divide A in blocks of B binary digits.

Python ints are used as bit strings: additions, subtractions, shifts and
comparisons. Every product goes through mul(), which multiplies limb arrays in
radix 2^8 by Karatsuba's method, and the Stats object counts the products.
"""


class Stats:
    def __init__(self) -> None:
        self.products = 0
        self.product_digits = 0  # the sum of the lengths of the larger factors
        self.corrections = 0
        self.max_corrections = 0
        self.depth = 0


W = 8
MASK = (1 << W) - 1


def to_limbs(x: int, w: int = W) -> list[int]:
    out = []
    while x:
        out.append(x & ((1 << w) - 1))
        x >>= w
    return out


def from_limbs(d: list[int], w: int = W) -> int:
    v = 0
    for x in reversed(d):
        v = (v << w) | x
    return v


def _school(a: list[int], b: list[int]) -> list[int]:
    c = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        carry = 0
        for j, y in enumerate(b):
            t = c[i + j] + x * y + carry
            c[i + j] = t & MASK
            carry = t >> W
        c[i + len(b)] = carry
    return c


def _karatsuba(a: list[int], b: list[int]) -> list[int]:
    """Product of limb arrays of the same length n, as 2n limbs."""
    n = len(a)
    if n <= 16:
        return _school(a, b)
    h = (n + 1) // 2
    a0, a1 = a[:h], a[h:] + [0] * (2 * h - n)
    b0, b1 = b[:h], b[h:] + [0] * (2 * h - n)
    z0 = from_limbs(_karatsuba(a0, b0))
    z2 = from_limbs(_karatsuba(a1, b1))
    s, t = from_limbs(a0) + from_limbs(a1), from_limbs(b0) + from_limbs(b1)
    cs, ct = s >> (W * h), t >> (W * h)  # carry bits of the sums
    s0, t0 = s & ((1 << (W * h)) - 1), t & ((1 << (W * h)) - 1)
    m = from_limbs(_karatsuba(_pad(to_limbs(s0), h), _pad(to_limbs(t0), h)))
    m += ((cs * t0 + ct * s0) << (W * h)) + ((cs * ct) << (2 * W * h))
    z1 = m - z0 - z2
    c = z0 + (z1 << (W * h)) + (z2 << (2 * W * h))
    return _pad(to_limbs(c), 2 * n)[: 2 * n]


def _pad(a: list[int], n: int) -> list[int]:
    return a + [0] * (n - len(a))


def mul(x: int, y: int, st: Stats | None = None) -> int:
    """x * y for x, y >= 0, through limb arrays."""
    a, b = to_limbs(x), to_limbs(y)
    n = max(len(a), len(b))
    if st is not None:
        st.products += 1
        st.product_digits += max(x.bit_length(), y.bit_length())
    if n == 0:
        return 0
    return from_limbs(_karatsuba(_pad(a, n), _pad(b, n)))


def reciprocal(D: int, st: Stats | None = None, depth: int = 0) -> int:
    """floor(4^B / D), where B = D.bit_length() >= 1."""
    B = D.bit_length()
    if B < 1:
        raise ZeroDivisionError("division by zero")
    if st is not None:
        st.depth = max(st.depth, depth)
    if B <= 8:  # @line L1: base case, one short division
        return (1 << (2 * B)) // D
    h = (B + 1) // 2  # @line L2: the top h binary digits of D
    Dh = D >> (B - h)
    Xh = reciprocal(Dh, st, depth + 1)  # @line L3: floor(4^h / Dh), recursively
    X = Xh << (B - h)  # @line L4: about 4^B / D, with about h correct digits
    E = (1 << (2 * B)) - mul(D, X, st)  # @line L5: the residual 4^B - D X
    if E >= 0:  # @line L6: X <- X + X E / 4^B, one Newton step
        X = X + (mul(X, E, st) >> (2 * B))
    else:
        X = X - ((mul(X, -E, st) + (1 << (2 * B)) - 1) >> (2 * B))
    E = (1 << (2 * B)) - mul(D, X, st)  # @line L7: correct with additions only
    c = 0
    while E < 0:
        X -= 1
        E += D
        c += 1
    while E >= D:
        X += 1
        E -= D
        c += 1
    if st is not None:
        st.corrections += c
        st.max_corrections = max(st.max_corrections, c)
    return X  # @line L8


def divide_block(U: int, D: int, R: int, B: int, st: Stats | None = None) -> tuple[int, int]:
    """(U // D, U % D) for 0 <= U < D * 2^B, with R = floor(4^B / D)."""
    q = mul(U, R, st) >> (2 * B)  # @line L9: q <= U / D < q + 2, so q is the quotient or one less
    r = U - mul(q, D, st)
    while r >= D:  # @line L10: at most one correction
        q += 1
        r -= D
    return q, r


def divide(A: int, D: int, st: Stats | None = None) -> tuple[int, int]:
    """(A // D, A % D) for A >= 0 and D > 0, in blocks of B binary digits."""
    if D <= 0:
        raise ZeroDivisionError("division by zero")
    if A < 0:
        raise ValueError("A must be nonnegative")
    B = D.bit_length()
    R = reciprocal(D, st)
    blocks = []
    x = A
    while x:
        blocks.append(x & ((1 << B) - 1))
        x >>= B
    q, r = 0, 0
    for blk in reversed(blocks):  # schoolbook division with digits of B binary digits
        U = (r << B) | blk  # U < D 2^B since r < D
        qd, r = divide_block(U, D, R, B, st)
        q = (q << B) | qd
    return q, r


def divide_limbs(a: list[int], d: list[int], w: int = 8) -> tuple[list[int], list[int]]:
    """Quotient and remainder of limb arrays in radix 2^w; the quotient has len(a) limbs."""
    A, D = from_limbs(a, w), from_limbs(d, w)
    q, r = divide(A, D)
    return _pad(to_limbs(q, w), len(a)), _pad(to_limbs(r, w), len(d))
