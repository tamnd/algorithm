# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ryu/. The authors are listed in prov/JH77DH.jsonl.

"""Ryu: shortest round-trip decimal for binary64 (Adams 2018).

ryu(x) returns (digits, exponent) with digits * 10^exponent the shortest
decimal that reads back to x under round to nearest, ties to even, and the
closest such decimal to x when several have the same length. The 125-bit
multipliers are computed on demand instead of being stored in a table.
"""

import math
import struct

MANTISSA_BITS = 52
BIAS = 1023
POW5_INV_BITCOUNT = 125
POW5_BITCOUNT = 125


def pow5bits(e: int) -> int:
    """ceil(log2(5^e)) for e >= 1, and 1 for e = 0."""
    return ((e * 1217359) >> 19) + 1


def log10_pow2(e: int) -> int:
    """floor(log10(2^e)) for 0 <= e <= 1650."""
    return (e * 78913) >> 18


def log10_pow5(e: int) -> int:
    """floor(log10(5^e)) for 0 <= e <= 2620."""
    return (e * 732923) >> 20


def pow5_inv_split(q: int) -> int:
    """The table entry ceil(2^(pow5bits(q) - 1 + 125) / 5^q), a 125-bit multiplier."""
    return ((1 << (pow5bits(q) - 1 + POW5_INV_BITCOUNT)) // 5**q) + 1


def pow5_split(i: int) -> int:
    """The table entry 5^i normalized to exactly 125 bits (truncated)."""
    shift = pow5bits(i) - POW5_BITCOUNT
    return 5**i >> shift if shift >= 0 else 5**i << -shift


def pow5_factor(v: int) -> int:
    count = 0
    while v % 5 == 0:
        v //= 5
        count += 1
    return count


def decode(x: float) -> tuple[int, int, int]:
    """Return (sign, ieee_mantissa, ieee_exponent) of a binary64 value."""
    bits = struct.unpack("<Q", struct.pack("<d", x))[0]
    return bits >> 63, bits & ((1 << MANTISSA_BITS) - 1), (bits >> MANTISSA_BITS) & 0x7FF


def ryu(x: float) -> tuple[int, int]:
    """Shortest decimal (digits, exponent) for a finite positive float x."""
    if not (math.isfinite(x) and x > 0):
        raise ValueError("ryu expects a finite positive float")
    _, ieee_m, ieee_e = decode(x)
    if ieee_e == 0:  # @line L1
        e2, m2 = 1 - BIAS - MANTISSA_BITS - 2, ieee_m
    else:
        e2, m2 = ieee_e - BIAS - MANTISSA_BITS - 2, (1 << MANTISSA_BITS) | ieee_m
    accept_bounds = m2 % 2 == 0  # ties go to even, so even m2 owns its boundaries
    mv = 4 * m2
    mm_shift = 1 if (ieee_m != 0 or ieee_e <= 1) else 0
    lo_n, hi_n = mv - 1 - mm_shift, mv + 2  # interval [lo_n, hi_n] * 2^e2
    vm_tz = vr_tz = False
    if e2 >= 0:  # @line L2
        q = max(0, log10_pow2(e2) - (1 if e2 > 3 else 0))
        e10 = q
        k = POW5_INV_BITCOUNT + pow5bits(q) - 1
        j = -e2 + q + k
        mul = pow5_inv_split(q)
        vr, vp, vm = (mv * mul) >> j, (hi_n * mul) >> j, (lo_n * mul) >> j  # @line L3
        if q <= 21:  # @line L4
            if mv % 5 == 0:
                vr_tz = pow5_factor(mv) >= q
            elif accept_bounds:
                vm_tz = pow5_factor(lo_n) >= q
            else:
                vp -= 1 if pow5_factor(hi_n) >= q else 0  # @line L5
    else:
        q = max(0, log10_pow5(-e2) - (1 if -e2 > 1 else 0))  # @line L2
        e10 = q + e2
        i = -e2 - q
        k = pow5bits(i) - POW5_BITCOUNT
        j = q - k
        mul = pow5_split(i)
        vr, vp, vm = (mv * mul) >> j, (hi_n * mul) >> j, (lo_n * mul) >> j  # @line L3
        if q <= 1:  # @line L4
            vr_tz = True
            if accept_bounds:
                vm_tz = mm_shift == 1
            else:
                vp -= 1  # @line L5
        elif q < 63:
            vr_tz = mv & ((1 << q) - 1) == 0
    removed, last = 0, 0
    while vp // 10 > vm // 10:  # @line L6
        vm_tz = vm_tz and vm % 10 == 0
        vr_tz = vr_tz and last == 0
        last = vr % 10
        vr, vp, vm = vr // 10, vp // 10, vm // 10
        removed += 1
    if vm_tz and accept_bounds:  # @line L7
        while vm % 10 == 0:
            vr_tz = vr_tz and last == 0
            last = vr % 10
            vr, vp, vm = vr // 10, vp // 10, vm // 10
            removed += 1
    if vr_tz and last == 5 and vr % 2 == 0:  # @line L8
        last = 4  # an exact tie: round half to even
    out = vr + (1 if (vr == vm and not (accept_bounds and vm_tz)) or last >= 5 else 0)  # @line L9
    return out, e10 + removed  # @line L10


def ryu_str(x: float) -> str:
    """Format like '1.5e-7', '-0.0', 'inf'; the digits come from ryu."""
    if math.isnan(x):
        return "nan"
    sign = "-" if math.copysign(1.0, x) < 0 else ""
    if math.isinf(x):
        return sign + "inf"
    if x == 0:
        return sign + "0.0"
    digits, exp = ryu(abs(x))
    s = str(digits)
    mantissa = s[0] + ("." + s[1:] if len(s) > 1 else "")
    return f"{sign}{mantissa}e{exp + len(s) - 1}"
