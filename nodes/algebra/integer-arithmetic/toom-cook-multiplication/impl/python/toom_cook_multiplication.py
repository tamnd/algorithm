# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/toom-cook-multiplication/. The authors are listed in prov/KFMRJ2.jsonl.

"""Toom-3 multiplication of limb arrays, with Bodrato's evaluation and
interpolation sequence at the points 0, 1, -1, -2 and infinity.

Limb arrays are lists of ints in [0, 2^w), least significant limb first.
Signed intermediate values are pairs (sign, magnitude) with sign in {1, -1}
and a trimmed magnitude limb array. A generic Toom-k on Python ints shows the
general method.
"""

from fractions import Fraction


def _trim(a: list[int]) -> list[int]:
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def _cmp(a: list[int], b: list[int]) -> int:
    a, b = _trim(a), _trim(b)
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    for x, y in zip(reversed(a), reversed(b)):
        if x != y:
            return -1 if x < y else 1
    return 0


def _add_mag(a: list[int], b: list[int], w: int) -> list[int]:
    mask = (1 << w) - 1
    if len(a) < len(b):
        a, b = b, a
    out, carry = [], 0
    for i, x in enumerate(a):
        t = x + (b[i] if i < len(b) else 0) + carry
        out.append(t & mask)
        carry = t >> w
    if carry:
        out.append(carry)
    return _trim(out)


def _sub_mag(a: list[int], b: list[int], w: int) -> list[int]:
    """a - b for magnitudes with a >= b."""
    mask = (1 << w) - 1
    out, borrow = [], 0
    for i, x in enumerate(a):
        t = x - (b[i] if i < len(b) else 0) - borrow
        borrow = 1 if t < 0 else 0
        out.append(t & mask)
    if borrow:
        raise ValueError("negative magnitude")
    return _trim(out)


def s_add(x: tuple, y: tuple, w: int) -> tuple:
    (sx, a), (sy, b) = x, y
    if sx == sy:
        return sx, _add_mag(a, b, w)
    c = _cmp(a, b)
    if c >= 0:
        return (sx if c > 0 else 1), _sub_mag(a, b, w)
    return sy, _sub_mag(b, a, w)


def s_sub(x: tuple, y: tuple, w: int) -> tuple:
    return s_add(x, (-y[0], y[1]), w)


def s_mul_small(x: tuple, d: int, w: int) -> tuple:
    mask = (1 << w) - 1
    out, carry = [], 0
    for v in x[1]:
        t = v * d + carry
        out.append(t & mask)
        carry = t >> w
    while carry:
        out.append(carry & mask)
        carry >>= w
    return x[0], _trim(out)


def s_div_exact(x: tuple, d: int, w: int) -> tuple:
    """x / d for a small d that divides x exactly (long division by one limb)."""
    out, r = [0] * len(x[1]), 0
    for i in range(len(x[1]) - 1, -1, -1):
        t = (r << w) | x[1][i]
        out[i], r = divmod(t, d)
    if r:
        raise ValueError("division is not exact")
    return x[0], _trim(out)


def _schoolbook(a: list[int], b: list[int], w: int) -> list[int]:
    mask = (1 << w) - 1
    c = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        carry = 0
        for j, y in enumerate(b):
            t = c[i + j] + x * y + carry
            c[i + j] = t & mask
            carry = t >> w
        c[i + len(b)] = carry
    return c


def _pad(a: list[int], n: int) -> list[int]:
    return list(a) + [0] * (n - len(a))


class Stats:
    def __init__(self) -> None:
        self.calls = 0
        self.leaves = 0
        self.max_depth = 0


def toom3(a: list[int], b: list[int], w: int = 8, threshold: int = 3, st: Stats | None = None, depth: int = 0) -> list[int]:
    """Product of two limb arrays of the same length n, as 2n limbs.

    Five recursive products of k + 1 limbs, where k = ceil(n / 3); the depth is
    about log3(n / threshold).
    """
    n = len(a)
    if n != len(b):
        raise ValueError("toom3() needs operands of the same length")
    if w < 3:
        raise ValueError("the values at the points need w >= 3")
    if st is not None:
        st.calls += 1
        st.max_depth = max(st.max_depth, depth)
    if n <= max(threshold, 2):  # @line L1
        if st is not None:
            st.leaves += 1
        return _schoolbook(a, b, w)
    k = (n + 2) // 3  # @line L2: a = a2 x^2 + a1 x + a0 with x = beta^k
    a0, a1, a2 = a[:k], a[k:2 * k], a[2 * k:]
    b0, b1, b2 = b[:k], b[k:2 * k], b[2 * k:]

    def evaluate(c0, c1, c2):  # @line L3: values at 0, 1, -1, -2, infinity
        p0, q1, q2 = (1, _trim(c0)), (1, _trim(c1)), (1, _trim(c2))
        p = s_add(p0, q2, w)
        p1 = s_add(p, q1, w)
        pm1 = s_sub(p, q1, w)
        pm2 = s_sub(s_mul_small(s_add(pm1, q2, w), 2, w), p0, w)
        return [p0, p1, pm1, pm2, q2]

    ea, eb = evaluate(a0, a1, a2), evaluate(b0, b1, b2)
    r = []
    for (sa, ma), (sb, mb) in zip(ea, eb):  # @line L4: five products of k + 1 limbs
        prod = toom3(_pad(ma, k + 1), _pad(mb, k + 1), w, threshold, st, depth + 1)
        r.append((sa * sb, _trim(prod)))
    v0, v1, vm1, vm2, vinf = r
    r0, r4 = v0, vinf  # @line L5: interpolation (Bodrato's sequence)
    r3 = s_div_exact(s_sub(vm2, v1, w), 3, w)
    r1 = s_div_exact(s_sub(v1, vm1, w), 2, w)
    r2 = s_sub(vm1, v0, w)
    r3 = s_add(s_div_exact(s_sub(r2, r3, w), 2, w), s_mul_small(r4, 2, w), w)
    r2 = s_sub(s_add(r2, r1, w), r4, w)
    r1 = s_sub(r1, r3, w)
    c = [0] * (2 * n + 4 * k + 2)  # @line L6: c = r0 + r1 x + r2 x^2 + r3 x^3 + r4 x^4
    for i, (sg, mag) in enumerate((r0, r1, r2, r3, r4)):
        if mag and sg < 0:
            raise ValueError("negative coefficient")
        shifted = [0] * (i * k) + mag
        c = _add_mag(c, shifted, w)
    return _pad(c, 2 * n)[: 2 * n]


def toom3_multiply(a: list[int], b: list[int], w: int = 8, threshold: int = 3) -> list[int]:
    """Product of limb arrays of any lengths, as len(a) + len(b) limbs (pads the shorter)."""
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        return [0] * (m + n)
    L = max(m, n)
    c = toom3(_pad(a, L), _pad(b, L), w, threshold)
    return c[: m + n]


def toom_k(x: int, y: int, k: int, digits: int, threshold: int = 1, counter: list[int] | None = None) -> int:
    """Generic Toom-k on nonnegative Python ints of at most `digits` limbs of 8 binary digits.

    Splits into k pieces of ceil(digits / k) limbs, evaluates at the 2k - 1 points
    0, 1, -1, 2, -2, ... and infinity, multiplies recursively and interpolates
    exactly with rational Lagrange coefficients.
    """
    if digits <= max(threshold, k + 1) or k < 2:
        if counter is not None:
            counter[0] += 1
        return x * y
    h = -(-digits // k)
    X = 1 << (8 * h)
    xs = [(x >> (8 * h * i)) & (X - 1) for i in range(k)]
    ys = [(y >> (8 * h * i)) & (X - 1) for i in range(k)]
    pts = [0]
    j = 1
    while len(pts) < 2 * k - 2:
        pts.append(j)
        if len(pts) < 2 * k - 2:
            pts.append(-j)
        j += 1
    vals = []
    for t in pts:
        u = sum(c * t**i for i, c in enumerate(xs))
        v = sum(c * t**i for i, c in enumerate(ys))
        s = (u < 0) != (v < 0)
        size = -(-max(abs(u).bit_length(), abs(v).bit_length(), 1) // 8)  # h + O(log k) limbs
        pr = toom_k(abs(u), abs(v), k, size, threshold, counter)
        vals.append(-pr if s else pr)
    top = toom_k(xs[-1], ys[-1], k, h, threshold, counter)  # the value at infinity
    # remove the leading term, then interpolate the remaining 2k - 2 coefficients
    m = 2 * k - 2
    rest = [vals[i] - top * pts[i] ** m for i in range(m)]
    coef = [Fraction(0)] * m
    for i in range(m):
        num, den = [Fraction(1)], Fraction(1)
        for j2 in range(m):
            if j2 != i:
                num = [Fraction(0)] + num
                for t in range(len(num) - 1):
                    num[t] -= pts[j2] * num[t + 1]
                den *= pts[i] - pts[j2]
        for t in range(m):
            coef[t] += rest[i] * num[t] / den
    coefs = [int(c) for c in coef] + [top]
    assert all(c.denominator == 1 for c in coef)
    return sum(c << (8 * h * i) for i, c in enumerate(coefs))
