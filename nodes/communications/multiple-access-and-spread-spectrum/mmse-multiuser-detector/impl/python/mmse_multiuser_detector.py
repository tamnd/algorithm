# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mmse-multiuser-detector/. The authors are listed in prov/1NBA15.jsonl.

"""The linear MMSE multiuser detector for synchronous CDMA.

Model (real, coherent BPSK, one symbol interval): y = S A b + w, where the
column s_k of S is the unit-energy signature of user k (N chips), A is the
diagonal matrix of the amplitudes A_k > 0, b is in {-1, +1}^K and w has
independent N(0, sigma^2) chips (sigma^2 = N0 / 2 in the complex model).

The matched filter bank gives z = S^T y = R A b + n with R = S^T S. The MMSE
detector computes x = (R + sigma^2 A^-2)^-1 z and decides b_k = sgn(x_k).
Row k of (R + sigma^2 A^-2)^-1, scaled by 1 / A_k, is the linear filter on z
that minimizes E[(b_k - w^T z)^2].
"""

import itertools
import math

import cbb


def matched_filter(y: list[float], sigs: list[list[float]]) -> list[float]:
    """z_k = s_k^T y for each user k."""
    return [math.fsum(a * b for a, b in zip(s, y)) for s in sigs]


def crosscorrelation(sigs: list[list[float]]) -> list[list[float]]:
    """R[i][j] = s_i^T s_j."""
    return [[math.fsum(a * b for a, b in zip(si, sj)) for sj in sigs] for si in sigs]


def regularized(r: list[list[float]], amps: list[float], sigma: float) -> list[list[float]]:
    """R + sigma^2 A^-2."""
    k = len(r)
    return [[r[i][j] + (sigma * sigma / (amps[i] * amps[i]) if i == j else 0.0) for j in range(k)] for i in range(k)]


def mmse_detector(y: list[float], sigs: list[list[float]], amps: list[float], sigma: float) -> list[int]:
    """The decisions sgn((R + sigma^2 A^-2)^-1 S^T y), with +1 for a zero output."""
    if any(a <= 0.0 for a in amps) or sigma < 0.0:
        raise ValueError("amplitudes must be positive and sigma must not be negative")
    z = matched_filter(y, sigs)  # @line L1
    r = crosscorrelation(sigs)  # @line L2
    m = regularized(r, amps, sigma)  # @line L3
    x = [v.real for v in cbb.solve(m, z)]  # @line L4
    return [1 if v >= 0.0 else -1 for v in x]  # @line L5


def mmse_rows(r: list[list[float]], amps: list[float], sigma: float) -> list[list[float]]:
    """The rows of (R + sigma^2 A^-2)^-1; row k is the filter on z for user k."""
    return [[v.real for v in row] for row in cbb.inv(regularized(r, amps, sigma))]


def output_sinr(w: list[float], k: int, r: list[list[float]], amps: list[float], sigma: float) -> float:
    """The SINR of user k at the output w^T z of any linear filter w on z."""
    kk = len(r)
    wr = [math.fsum(w[i] * r[i][j] for i in range(kk)) for j in range(kk)]
    sig = (wr[k] * amps[k]) ** 2
    mai = math.fsum((wr[j] * amps[j]) ** 2 for j in range(kk) if j != k)
    noise = sigma * sigma * math.fsum(wr[j] * w[j] for j in range(kk))
    return sig / (mai + noise)


def mmse_sinr(k: int, sigs: list[list[float]], amps: list[float], sigma: float) -> float:
    """A_k^2 s_k^T (sigma^2 I + sum over j != k of A_j^2 s_j s_j^T)^-1 s_k."""
    n = len(sigs[0])
    cov = [[(sigma * sigma if a == c else 0.0) + math.fsum(amps[j] ** 2 * sigs[j][a] * sigs[j][c] for j in range(len(sigs)) if j != k) for c in range(n)] for a in range(n)]
    u = [v.real for v in cbb.solve(cov, sigs[k])]
    return amps[k] ** 2 * math.fsum(p * q for p, q in zip(sigs[k], u))


def linear_ber(w: list[float], k: int, r: list[list[float]], amps: list[float], sigma: float) -> float:
    """The exact bit error rate of user k when the receiver decides sgn(w^T z).

    The other bits are equally likely and independent, so the rate is the
    average over them of Q(w^T R A b / (sigma sqrt(w^T R w))) with b_k = +1.
    """
    kk = len(r)
    wr = [math.fsum(w[i] * r[i][j] for i in range(kk)) for j in range(kk)]
    sd = sigma * math.sqrt(math.fsum(wr[j] * w[j] for j in range(kk)))
    others = [j for j in range(kk) if j != k]
    total = 0.0
    for signs in itertools.product((1, -1), repeat=len(others)):
        b = [0] * kk
        b[k] = 1
        for j, s in zip(others, signs):
            b[j] = s
        mean = math.fsum(wr[j] * amps[j] * b[j] for j in range(kk))
        total += cbb.qfunc(mean / sd)
    return total / (2 ** len(others))
