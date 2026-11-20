# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decorrelating-detector/. The authors are listed in prov/X81J9E.jsonl.

"""The decorrelating detector of Lupas and Verdu for synchronous CDMA.

Model (real, coherent BPSK, one symbol interval): y = S A b + w, where the
column s_k of S is the unit-energy signature of user k (N chips), A is the
diagonal matrix of the amplitudes A_k > 0, b is in {-1, +1}^K and w has
independent N(0, sigma^2) chips (sigma^2 = N0 / 2 in the complex model).

The matched filter bank gives z = S^T y = R A b + n with R = S^T S and
n ~ N(0, sigma^2 R). The decorrelator solves R x = z, so x = A b + R^-1 n has
no multiple access interference, and decides b_k = sgn(x_k).
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


def decorrelate(z: list[float], r: list[list[float]]) -> list[float]:
    """The solution x of R x = z (raises ValueError if R is singular)."""
    return [v.real for v in cbb.solve(r, z)]


def decorrelating_detector(y: list[float], sigs: list[list[float]]) -> list[int]:
    """The decisions sgn(R^-1 S^T y), with +1 for a zero output."""
    z = matched_filter(y, sigs)  # @line L1
    r = crosscorrelation(sigs)  # @line L2
    x = decorrelate(z, r)  # @line L3
    return [1 if v >= 0.0 else -1 for v in x]  # @line L4


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


def decorrelator_ber(k: int, r: list[list[float]], amps: list[float], sigma: float) -> float:
    """The closed form Q(A_k / (sigma sqrt((R^-1)_kk)))."""
    rinv_kk = cbb.inv(r)[k][k].real
    return cbb.qfunc(amps[k] / (sigma * math.sqrt(rinv_kk)))


def near_far_resistance(r: list[list[float]], k: int) -> float:
    """1 / (R^-1)_kk, the near-far resistance of the decorrelator (and of the optimum detector)."""
    return 1.0 / cbb.inv(r)[k][k].real
