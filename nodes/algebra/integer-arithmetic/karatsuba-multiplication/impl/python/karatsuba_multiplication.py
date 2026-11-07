# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karatsuba-multiplication/. The authors are listed in prov/QWY1MV.jsonl.

# Limb arrays are lists of ints in [0, 2^w), least significant limb first.


def _trim(a: list[int]) -> list[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def _add_into(c: list[int], a: list[int], shift: int, w: int) -> None:
    """c += a * beta^shift, in place; c must be long enough for the result."""
    mask = (1 << w) - 1
    carry = 0
    i = 0
    for i, x in enumerate(a):
        t = c[shift + i] + x + carry
        c[shift + i] = t & mask
        carry = t >> w
    k = shift + len(a)
    while carry:
        t = c[k] + carry
        c[k] = t & mask
        carry = t >> w
        k += 1


def _add(a: list[int], b: list[int], w: int) -> list[int]:
    if len(a) < len(b):
        a, b = b, a
    c = list(a) + [0]
    _add_into(c, b, 0, w)
    return c


def _sub_in_place(c: list[int], a: list[int], w: int) -> None:
    """c -= a, in place, where c >= a as numbers."""
    mask = (1 << w) - 1
    borrow = 0
    for i in range(len(c)):
        t = c[i] - (a[i] if i < len(a) else 0) - borrow
        borrow = 1 if t < 0 else 0
        c[i] = t & mask
        if i >= len(a) and not borrow:
            break
    if borrow:
        raise ValueError("negative result")


def schoolbook(a: list[int], b: list[int], w: int, counter: list[int] | None = None) -> list[int]:
    """The base case: len(a) * len(b) limb products."""
    mask = (1 << w) - 1
    c = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        carry = 0
        for j, y in enumerate(b):
            t = c[i + j] + x * y + carry
            c[i + j] = t & mask
            carry = t >> w
        c[i + len(b)] = carry
    if counter is not None:
        counter[0] += len(a) * len(b)
    return c


def _sum_product(a0, a1, b0, b1, w, threshold, counter, mul) -> list[int]:
    """(a0 + a1)(b0 + b1) as 2h + 2 limbs, with one recursive product of h limbs.

    a0 + a1 = s + ca beta^h with a carry bit ca, and the same for b, so
    (a0 + a1)(b0 + b1) = s t + (ca t + cb s) beta^h + ca cb beta^(2h).
    """
    h = len(a0)
    sa, sb = _add(a0, a1, w), _add(b0, b1, w)  # h + 1 limbs each
    ca, cb = sa.pop(), sb.pop()
    z = mul(sa, sb, w, threshold, counter) + [0, 0]
    if ca:
        _add_into(z, sb, h, w)
    if cb:
        _add_into(z, sa, h, w)
    if ca and cb:
        _add_into(z, [1], 2 * h, w)
    return z


def karatsuba(a: list[int], b: list[int], w: int = 8, threshold: int = 4, counter: list[int] | None = None) -> list[int]:
    """Product of two limb arrays of the same length n, as 2n limbs.

    Recursion: three products of about n/2 limbs, so depth about log2(n / threshold).
    """
    n = len(a)
    if n != len(b):
        raise ValueError("karatsuba() needs operands of the same length")
    if n <= max(threshold, 1):  # @line L1
        return schoolbook(a, b, w, counter)
    h = (n + 1) // 2  # @line L2: a = a0 + a1 beta^h, b = b0 + b1 beta^h
    a0, a1 = a[:h], a[h:] + [0] * (2 * h - n)
    b0, b1 = b[:h], b[h:] + [0] * (2 * h - n)
    z0 = karatsuba(a0, b0, w, threshold, counter)  # @line L3
    z2 = karatsuba(a1, b1, w, threshold, counter)  # @line L4
    z1 = _sum_product(a0, a1, b0, b1, w, threshold, counter, karatsuba)  # @line L5
    _sub_in_place(z1, z0, w)
    _sub_in_place(z1, z2, w)  # now z1 = a0 b1 + a1 b0
    c = [0] * (4 * h + 2)  # @line L6: c = z0 + z1 beta^h + z2 beta^(2h)
    _add_into(c, z0, 0, w)
    _add_into(c, _trim(z1), h, w)
    _add_into(c, z2, 2 * h, w)
    return c[: 2 * n]


def karatsuba_multiply(a: list[int], b: list[int], w: int = 8, threshold: int = 4) -> list[int]:
    """Product of limb arrays of any lengths m and n, as m + n limbs.

    If the lengths are close, the shorter is padded with zeros. If one is less
    than half the other, the longer is cut into blocks of the shorter length,
    and each block is multiplied by Karatsuba (the unbalanced case).
    """
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        return [0] * (m + n)
    if m < n:
        a, b, m, n = b, a, n, m
    c = [0] * (m + n + 1)
    if 2 * n <= m:
        for start in range(0, m, n):
            block = a[start:start + n]
            block = block + [0] * (n - len(block))
            _add_into(c, _trim(karatsuba(block, b, w, threshold)), start, w)
    else:
        p = karatsuba(a, b + [0] * (m - n), w, threshold)
        _add_into(c, _trim(p), 0, w)
    return c[: m + n]


def karatsuba_square(a: list[int], w: int = 8, threshold: int = 4) -> list[int]:
    """a^2 with three half-size squarings: (a0 + a1)^2 - a0^2 - a1^2 = 2 a0 a1."""
    n = len(a)
    if n <= max(threshold, 1):
        return schoolbook(a, a, w)
    h = (n + 1) // 2
    a0, a1 = a[:h], a[h:] + [0] * (2 * h - n)
    z0 = karatsuba_square(a0, w, threshold)
    z2 = karatsuba_square(a1, w, threshold)
    z1 = _sum_product(a0, a1, a0, a1, w, threshold, None, lambda x, y, w_, t_, c_: karatsuba_square(x, w_, t_))
    _sub_in_place(z1, z0, w)
    _sub_in_place(z1, z2, w)
    c = [0] * (4 * h + 2)
    _add_into(c, z0, 0, w)
    _add_into(c, _trim(z1), h, w)
    _add_into(c, z2, 2 * h, w)
    return c[: 2 * n]


def multiply_signed(x: int, y: int, w: int = 8, threshold: int = 4) -> int:
    """Signed product of Python ints through limb arrays: sign rule and magnitudes."""
    def limbs(v: int) -> list[int]:
        out = []
        while v:
            out.append(v & ((1 << w) - 1))
            v >>= w
        return out

    c = karatsuba_multiply(limbs(abs(x)), limbs(abs(y)), w, threshold)
    v = 0
    for d in reversed(c):
        v = (v << w) | d
    return -v if (x < 0) != (y < 0) else v
