# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/srt-division/. The authors are listed in prov/732WBN.jsonl.

"""Radix-4 SRT division with digit set {-2, ..., 2} and a derived selection table.

Fixed-point convention: x and d lie in [1/2, 1) and are given as integers
X = x * 2^F and D = d * 2^F. The partial remainder w satisfies |w| <= (2/3) d.
The quotient digit is chosen from 4 bits of d (0.1xxx) and 4w truncated to
3 fractional bits, exactly as a hardware table lookup would.
"""

import math
from fractions import Fraction

RHO = Fraction(2, 3)  # redundancy factor a/(r-1) = 2/3
D_BITS = 4  # divisor estimate 0.1xxx: 4 bits after the binary point
Y_BITS = 3  # fractional bits of the remainder estimate


def build_table(d_bits: int = D_BITS, y_bits: int = Y_BITS) -> dict[tuple[int, int], int]:
    """For each (divisor cell, remainder cell) pick a digit k that keeps |4w - k d| <= rho d.

    A cell is the set of exact (y, d) with d in [i/2^d_bits, (i+1)/2^d_bits) and
    y in [j/2^y_bits, (j+1)/2^y_bits) and |y| <= (8/3) d. Raises if some cell has no digit.
    """
    table = {}
    for i in range(2 ** (d_bits - 1), 2**d_bits):
        dlo, dhi = Fraction(i, 2**d_bits), Fraction(i + 1, 2**d_bits)
        lim = math.ceil(4 * RHO * dhi * 2**y_bits) + 1
        for j in range(-lim - 1, lim + 1):
            ylo, yhi = Fraction(j, 2**y_bits), Fraction(j + 1, 2**y_bits)
            if ylo > 4 * RHO * dhi or yhi <= -4 * RHO * dhi:
                continue  # unreachable cell
            feasible = []
            for k in range(-2, 3):
                low_ok = k == -2 or ylo >= max((k - RHO) * dlo, (k - RHO) * dhi)
                high_ok = k == 2 or yhi <= min((k + RHO) * dlo, (k + RHO) * dhi)
                if low_ok and high_ok:
                    feasible.append(k)
            if not feasible:
                raise ValueError(f"no digit for cell {(i, j)}")
            table[(i, j)] = min(feasible, key=lambda k: (abs(k), -k))
    return table


TABLE = build_table()


def srt_divide_fixed(X: int, D: int, F: int, n: int, table=None) -> tuple[int, int]:
    """n radix-4 SRT steps on x = X/2^F and d = D/2^F, both in [1/2, 1).

    The remainder is held as W = w * 2^(F+2), so w0 = x/4 is exact.
    Returns (Q, W) with x/(4d) = Q/4^n + w/(4^n d) and 0 <= w < d.
    """
    table = TABLE if table is None else table
    d_index = D >> (F - D_BITS)  # 0.1xxx, the 4 leading bits of d
    D4 = 4 * D  # d in the units of W
    W, Q = X, 0  # @line L1
    for _ in range(n):  # @line L2
        y_index = (4 * W) >> (F + 2 - Y_BITS)  # @line L3
        q = table[(d_index, y_index)]  # @line L4
        W = 4 * W - q * D4  # @line L5
        Q = 4 * Q + q  # @line L6
    if W < 0:  # @line L7
        Q, W = Q - 1, W + D4
    return Q, W  # @line L8


def srt_float_divide(a: float, b: float) -> float:
    """a / b correctly rounded (ties to even) via radix-4 SRT, for positive normal results."""
    if not (a > 0 and b > 0 and math.isfinite(a) and math.isfinite(b)):
        raise ValueError("positive finite operands expected")
    ma, ea = math.frexp(a)  # ma in [1/2, 1)
    mb, eb = math.frexp(b)
    F = 53
    X, D = int(ma * 2**F), int(mb * 2**F)
    n = 28  # 56 quotient bits of x/(4d); x/d = 4 Q / 4^n + ...
    Q, W = srt_divide_fixed(X, D, F, n)  # W > 0 iff the division is inexact
    # x/d = Q * 2^(2 - 2n) + tail, with tail in [0, 2^(2 - 2n)); sticky = tail > 0
    shift = Q.bit_length() - 53
    keep, rest = Q >> shift, Q & ((1 << shift) - 1)
    half = 1 << (shift - 1)
    if rest > half or (rest == half and (W != 0 or keep % 2 == 1)):
        keep += 1
    return math.ldexp(keep, shift + 2 - 2 * n + ea - eb)


def trace(x: Fraction, d: Fraction, n: int) -> list[tuple[Fraction, Fraction, int]]:
    """Rows (4w, its truncated estimate, chosen digit) of the first n steps, in exact rationals."""
    rows, w = [], x / 4
    d_index = math.floor(d * 2**D_BITS)
    for _ in range(n):
        y = 4 * w
        j = math.floor(y * 2**Y_BITS)
        q = TABLE[(d_index, j)]
        rows.append((y, Fraction(j, 2**Y_BITS), q))
        w = y - q * d
    return rows
