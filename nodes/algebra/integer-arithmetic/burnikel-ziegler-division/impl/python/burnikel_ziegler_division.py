# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burnikel-ziegler-division/. The authors are listed in prov/V436BS.jsonl.

"""Burnikel-Ziegler recursive division on numbers of limbs in base 2^w.

Numbers are Python ints read as limb arrays in base beta = 2^w; limbs are
taken out with shifts and masks. Products of big numbers are delegated to
Python multiplication, which plays the role of M(n), and every such product
is recorded in Stats so that the cost recurrence can be checked.
"""

from dataclasses import dataclass, field


@dataclass
class Stats:
    """Counters: products by size (in limbs) and correction steps."""

    products: dict[int, int] = field(default_factory=dict)
    corrections: int = 0
    max_corrections: int = 0
    basecase_calls: int = 0


def limbs(x: int, w: int) -> int:
    """The number of base-2^w limbs of x (0 has 0 limbs)."""
    return (x.bit_length() + w - 1) // w


def _record(st: Stats, size: int) -> None:
    st.products[size] = st.products.get(size, 0) + 1


def schoolbook_divrem(a: int, b: int, n: int, m: int, w: int, st: Stats) -> tuple[int, int]:
    """Long division of a < beta^m * b by a normalized n-limb b (Knuth's D)."""
    st.basecase_calls += 1
    beta = 1 << w
    top = b >> (w * (n - 1))
    q = 0
    for j in range(m - 1, -1, -1):
        hi = (a >> (w * (n + j - 1))) & ((1 << (2 * w)) - 1)
        qj = min(hi // top, beta - 1)
        a -= (qj * b) << (w * j)
        while a < 0:
            qj -= 1
            a += b << (w * j)
        q = (q << w) | qj
    return q, a


def div_2n_1n(a: int, b: int, n: int, w: int, st: Stats, n0: int = 2) -> tuple[int, int]:
    """Divide 0 <= a < beta^n * b by a normalized n-limb b."""
    if n % 2 == 1 or n <= n0:  # @line L1
        return schoolbook_divrem(a, b, n, n, w, st)
    h = n // 2  # @line L2
    mask = (1 << (w * h)) - 1
    a4 = a & mask
    a123 = a >> (w * h)
    q1, r = div_3n_2n(a123, b, h, w, st, n0)  # @line L3
    q2, s = div_3n_2n((r << (w * h)) | a4, b, h, w, st, n0)  # @line L4
    return (q1 << (w * h)) | q2, s  # @line L5


def div_3n_2n(a: int, b: int, h: int, w: int, st: Stats, n0: int = 2) -> tuple[int, int]:
    """Divide 0 <= a < beta^h * b by a normalized 2h-limb b = b1 beta^h + b2."""
    mask = (1 << (w * h)) - 1
    b1, b2 = b >> (w * h), b & mask
    a12, a3 = a >> (w * h), a & mask
    a1 = a12 >> (w * h)
    if a1 < b1:  # @line L6
        q, r1 = div_2n_1n(a12, b1, h, w, st, n0)
    else:  # @line L7
        q = mask
        r1 = a12 - q * b1
    _record(st, h)
    r = (r1 << (w * h)) + a3 - q * b2  # @line L8
    k = 0
    while r < 0:  # @line L9
        q -= 1
        r += b
        k += 1
    st.corrections += k
    st.max_corrections = max(st.max_corrections, k)
    return q, r  # @line L10


def bz_divmod(a: int, b: int, w: int = 4, n0: int = 2, st: Stats | None = None) -> tuple[int, int]:
    """Return divmod(a, b) for a >= 0 and b > 0 by Burnikel-Ziegler.

    Normalizes b so that its top limb has its high bit set, pads it to n
    limbs, and divides a block of n limbs at a time from the top.
    """
    if b <= 0 or a < 0:
        raise ValueError("need a >= 0 and b > 0")
    st = st if st is not None else Stats()
    n = max(limbs(b, w), 1)
    shift = n * w - b.bit_length()
    bn, an = b << shift, a << shift
    blocks = max((limbs(an, w) + n - 1) // n, 1)
    if (an >> (w * n * (blocks - 1))) >= bn:
        blocks += 1
    mask = (1 << (w * n)) - 1
    q, r = 0, 0
    for i in range(blocks - 1, -1, -1):
        chunk = (an >> (w * n * i)) & mask
        qi, r = div_2n_1n((r << (w * n)) | chunk, bn, n, w, st, n0)
        q = (q << (w * n)) | qi
    return q, r >> shift
