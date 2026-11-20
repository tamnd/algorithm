# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-interference-cancellation/. The authors are listed in prov/9G0E22.jsonl.

"""Parallel (multistage) interference cancellation for synchronous CDMA.

Model (real, coherent BPSK, one symbol interval): y = S A b + w, where the
column s_k of S is the unit-energy signature of user k (N chips), A is the
diagonal matrix of the known amplitudes A_k > 0, b is in {-1, +1}^K and w
has independent N(0, sigma^2) chips (sigma^2 = N0 / 2 in the complex model).

The matched filter bank gives z = S^T y = R A b + n with R = S^T S. Stage 0
makes tentative decisions (the signs of z, or the decorrelator decisions).
Every later stage subtracts, for each user at the same time, the interference
that the decisions of the previous stage predict, and takes the sign again.
"""

import math

import cbb


def matched_filter(y: list[float], sigs: list[list[float]]) -> list[float]:
    """z_k = s_k^T y for each user k."""
    return [math.fsum(a * b for a, b in zip(s, y)) for s in sigs]


def crosscorrelation(sigs: list[list[float]]) -> list[list[float]]:
    """R[i][j] = s_i^T s_j."""
    return [[math.fsum(a * b for a, b in zip(si, sj)) for sj in sigs] for si in sigs]


def _sgn(v: float) -> int:
    return 1 if v >= 0.0 else -1


def pic(z: list[float], r: list[list[float]], amps: list[float], stages: int, start: list[int] | None = None) -> list[list[int]]:
    """The decisions of stages 0, 1, ..., J on the matched filter outputs z.

    start gives the stage 0 decisions; None means the signs of z.
    """
    k_users = len(z)
    if len(amps) != k_users or any(a <= 0.0 for a in amps):
        raise ValueError("need one positive amplitude per user")
    if stages < 0:
        raise ValueError("the number of stages must not be negative")
    b = list(start) if start is not None else [_sgn(v) for v in z]  # @line L1
    history = [b]
    for _ in range(stages):  # @line L2
        new = []
        for k in range(k_users):  # @line L3
            x = z[k] - math.fsum(r[k][j] * amps[j] * b[j] for j in range(k_users) if j != k)  # @line L4
            new.append(_sgn(x))  # @line L5
        b = new  # @line L6
        history.append(b)
    return history  # @line L7


def pic_detector(y: list[float], sigs: list[list[float]], amps: list[float], stages: int, start: str = "mf") -> list[int]:
    """The decisions of the last stage. start is "mf" (signs of z) or "decorrelator"."""
    z = matched_filter(y, sigs)
    r = crosscorrelation(sigs)
    if start == "mf":
        b0 = None
    elif start == "decorrelator":
        b0 = [_sgn(v.real) for v in cbb.solve(r, z)]
    else:
        raise ValueError("start must be 'mf' or 'decorrelator'")
    return pic(z, r, amps, stages, b0)[-1]


def linear_pic(z: list[float], r: list[list[float]], stages: int) -> list[float]:
    """PIC without the sign: x <- z - (R - I) x from x = z, which is Jacobi iteration on R x = z."""
    k_users = len(z)
    x = list(z)
    for _ in range(stages):
        x = [z[k] - math.fsum(r[k][j] * x[j] for j in range(k_users) if j != k) for k in range(k_users)]
    return x
