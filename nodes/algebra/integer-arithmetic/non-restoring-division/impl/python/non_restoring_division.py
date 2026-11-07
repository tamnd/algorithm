# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-restoring-division/. The authors are listed in prov/HPV12R.jsonl.

"""Non-restoring binary division on limb arrays.

Numbers are lists of limbs in radix 2**w (w >= 2), least significant limb
first. The partial remainder R lies in [-V, V) and is held in two's complement
in n + 1 limbs, where n is the number of limbs of the divisor V; its sign is
the top binary digit of the top limb.
"""


def _trim(a: list[int]) -> list[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def _shift_in(r: list[int], bit: int, w: int) -> None:
    """r <- 2 r + bit modulo 2**(w len(r)), in place."""
    mask = (1 << w) - 1
    carry = bit
    for i in range(len(r)):
        t = (r[i] << 1) | carry
        carry = t >> w
        r[i] = t & mask


def _add_in_place(r: list[int], v: list[int], w: int) -> None:
    """r <- r + v modulo 2**(w len(r))."""
    mask = (1 << w) - 1
    carry = 0
    for i in range(len(r)):
        t = r[i] + (v[i] if i < len(v) else 0) + carry
        carry = t >> w
        r[i] = t & mask


def _sub_in_place(r: list[int], v: list[int], w: int) -> None:
    """r <- r - v modulo 2**(w len(r))."""
    mask = (1 << w) - 1
    borrow = 0
    for i in range(len(r)):
        t = r[i] - (v[i] if i < len(v) else 0) - borrow
        borrow = 1 if t < 0 else 0
        r[i] = t & mask


def _negative(r: list[int], w: int) -> bool:
    return (r[-1] >> (w - 1)) & 1 == 1


def bit_length(u: list[int], w: int) -> int:
    u = _trim(list(u))
    if not u:
        return 0
    return (len(u) - 1) * w + u[-1].bit_length()


def non_restoring_divide(u: list[int], v: list[int], w: int = 8, stats: dict | None = None) -> tuple[list[int], list[int]]:
    """Quotient and remainder of the limb arrays u and v (v nonzero) in radix 2**w.

    Each step shifts in the next binary digit of u and then subtracts v if the
    partial remainder is nonnegative, or adds v if it is negative. The quotient
    digit is 1 when the new remainder is nonnegative. One final addition makes
    the remainder nonnegative. If stats is given, it counts the steps and the
    final corrections.
    """
    if w < 2:
        raise ValueError("w must be at least 2, so that 2V fits in n + 1 limbs with a sign")
    v = _trim(list(v))
    if not v:
        raise ZeroDivisionError("division by zero")
    m = bit_length(u, w)
    q = [0] * ((m + w - 1) // w)
    r = [0] * (len(v) + 1)  # @line L1: R <- 0
    for i in range(m - 1, -1, -1):  # @line L2
        was_negative = _negative(r, w)
        _shift_in(r, (u[i // w] >> (i % w)) & 1, w)
        if not was_negative:  # @line L3: R >= 0, so R <- 2R + u_i - V
            _sub_in_place(r, v, w)
        else:  # @line L4: R < 0, so R <- 2R + u_i + V
            _add_in_place(r, v, w)
        if not _negative(r, w):  # @line L5: q_i <- [R >= 0]
            q[i // w] |= 1 << (i % w)
    corrected = 0
    if _negative(r, w):  # @line L6: final correction
        _add_in_place(r, v, w)
        corrected = 1
    if stats is not None:
        stats["steps"] = stats.get("steps", 0) + m
        stats["corrections"] = stats.get("corrections", 0) + corrected
    return _trim(q), _trim(r)  # @line L7


def signed_digit_quotient(u: int, v: int) -> tuple[list[int], int]:
    """The quotient digits d_i in {-1, +1} of the textbook form, from the top,
    and the uncorrected remainder R_0, with u = (sum d_i 2**i) v + R_0."""
    m = u.bit_length()
    r = 0
    digits = []
    for i in range(m - 1, -1, -1):
        d = 1 if r >= 0 else -1
        r = 2 * r + ((u >> i) & 1) - d * v
        digits.append(d)
    return digits, r


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
