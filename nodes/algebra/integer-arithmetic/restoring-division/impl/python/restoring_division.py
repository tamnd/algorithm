# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/restoring-division/. The authors are listed in prov/7J9632.jsonl.

"""Restoring binary division on limb arrays.

Numbers are lists of limbs in radix 2**w, least significant limb first. The
partial remainder R is kept in n + 1 limbs, where n is the number of limbs of
the divisor, and a negative value of R is detected by the borrow out of the
trial subtraction, as a hardware divider does.
"""


def _trim(a: list[int]) -> list[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def _shift_in(r: list[int], bit: int, w: int) -> None:
    """r <- 2 r + bit, in place. The top bit shifted out is dropped."""
    mask = (1 << w) - 1
    carry = bit
    for i in range(len(r)):
        t = (r[i] << 1) | carry
        carry = t >> w
        r[i] = t & mask


def _sub_in_place(r: list[int], v: list[int], w: int) -> int:
    """r <- r - v modulo 2**(w len(r)); returns the borrow out (1 if r < v)."""
    mask = (1 << w) - 1
    borrow = 0
    for i in range(len(r)):
        t = r[i] - (v[i] if i < len(v) else 0) - borrow
        borrow = 1 if t < 0 else 0
        r[i] = t & mask
    return borrow


def _add_in_place(r: list[int], v: list[int], w: int) -> None:
    """r <- r + v modulo 2**(w len(r)); the carry out is dropped."""
    mask = (1 << w) - 1
    carry = 0
    for i in range(len(r)):
        t = r[i] + (v[i] if i < len(v) else 0) + carry
        carry = t >> w
        r[i] = t & mask


def bit_length(u: list[int], w: int) -> int:
    u = _trim(list(u))
    if not u:
        return 0
    return (len(u) - 1) * w + u[-1].bit_length()


def restoring_divide(u: list[int], v: list[int], w: int = 8, stats: dict | None = None) -> tuple[list[int], list[int]]:
    """Quotient and remainder of the limb arrays u and v (v nonzero) in radix 2**w.

    One quotient bit per step, from the top: shift the next bit of u into the
    partial remainder, subtract v, and add v back if the result is negative.
    If stats is given, it counts the steps and the restoring additions.
    """
    v = _trim(list(v))
    if not v:
        raise ZeroDivisionError("division by zero")
    n = len(v)
    m = bit_length(u, w)
    q = [0] * ((m + w - 1) // w)
    r = [0] * (n + 1)  # @line L1: R <- 0, Q <- 0
    restores = 0
    for i in range(m - 1, -1, -1):  # @line L2
        bit = (u[i // w] >> (i % w)) & 1
        _shift_in(r, bit, w)  # @line L3: R <- 2R + u_i
        negative = _sub_in_place(r, v, w)  # @line L4: trial subtraction
        if negative:  # @line L5
            _add_in_place(r, v, w)  # @line L6: restore, q_i = 0
            restores += 1
        else:
            q[i // w] |= 1 << (i % w)  # @line L7: q_i = 1
    if stats is not None:
        stats["steps"] = stats.get("steps", 0) + m
        stats["restores"] = stats.get("restores", 0) + restores
    return _trim(q), _trim(r)  # @line L8


def nonperforming_divide(u: list[int], v: list[int], w: int = 8) -> tuple[list[int], list[int]]:
    """The non-performing variant: subtract into a copy and keep it only if it is nonnegative."""
    v = _trim(list(v))
    if not v:
        raise ZeroDivisionError("division by zero")
    m = bit_length(u, w)
    q = [0] * ((m + w - 1) // w)
    r = [0] * (len(v) + 1)
    for i in range(m - 1, -1, -1):
        _shift_in(r, (u[i // w] >> (i % w)) & 1, w)
        t = list(r)
        if not _sub_in_place(t, v, w):
            r = t
            q[i // w] |= 1 << (i % w)
    return _trim(q), _trim(r)


def to_limbs(x: int, w: int) -> list[int]:
    out = []
    mask = (1 << w) - 1
    while x:
        out.append(x & mask)
        x >>= w
    return out


def from_limbs(a: list[int], w: int) -> int:
    x = 0
    for t in reversed(a):
        x = (x << w) | t
    return x


def divide_signed(a: int, b: int, w: int = 8) -> tuple[int, int]:
    """Truncating signed division, as in C: the quotient rounds toward zero and
    the remainder has the sign of the dividend."""
    q, r = restoring_divide(to_limbs(abs(a), w), to_limbs(abs(b), w), w)
    qi, ri = from_limbs(q, w), from_limbs(r, w)
    if (a < 0) != (b < 0):
        qi = -qi
    if a < 0:
        ri = -ri
    return qi, ri
