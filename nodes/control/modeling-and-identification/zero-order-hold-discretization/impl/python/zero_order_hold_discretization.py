# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-order-hold-discretization/. The authors are listed in prov/TDAR9X.jsonl.

"""Zero-order hold discretization of x' = A x + B u, y = C x + D u.

With the input held constant on each interval [k h, (k + 1) h), the samples
x_k = x(k h) satisfy x_(k+1) = A_d x_k + B_d u_k exactly, where

    A_d = e^(A h),    B_d = (integral from 0 to h of e^(A s) ds) B.

Van Loan (1978): the exponential of the block matrix [[A, B], [0, 0]] h is
[[A_d, B_d], [0, I]], so one matrix exponential of size n + m gives both.
C and D do not change. The cost is that of one dense matrix exponential of
size n + m, O((n + m)^3) flops times the number of products in expm.
"""

from ctlmat import block, expm, scale, zeros

__all__ = ["zoh", "zoh_ss"]


def zoh(A, B, h):
    """Return (A_d, B_d) for sampling period h > 0, in floating point."""
    if h <= 0:
        raise ValueError("the sampling period h must be positive")
    n = len(A)
    m = len(B[0]) if B else 0
    if any(len(row) != n for row in A) or len(B) != n:
        raise ValueError("A must be n by n and B must be n by m")
    big = block([[scale(h, A), scale(h, B)], [zeros(m, n), zeros(m, m)]])  # @line L1
    e = expm(big)  # @line L2
    ad = [row[:n] for row in e[:n]]  # @line L3
    bd = [row[n:] for row in e[:n]]  # @line L4
    return ad, bd


def zoh_ss(A, B, C, D, h):
    """Return (A_d, B_d, C, D): the full discrete model of (A, B, C, D)."""
    ad, bd = zoh(A, B, h)
    return ad, bd, [list(r) for r in C], [list(r) for r in D]
