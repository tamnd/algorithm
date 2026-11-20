# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/successive-interference-cancellation/. The authors are listed in prov/TZZ989.jsonl.

"""Successive interference cancellation (SIC) for synchronous CDMA.

Model (real, coherent BPSK, one symbol interval): y = S A b + w, where the
column s_k of S is the unit-energy signature of user k (N chips), A is the
diagonal matrix of the amplitudes A_k > 0, b is in {-1, +1}^K and w has
independent N(0, sigma^2) chips (sigma^2 = N0 / 2 in the complex model).

The detector decides the users one at a time, strongest first. After each
decision it rebuilds that user's signal A_k b_k s_k and subtracts it from y,
so the next user sees less interference. Subtracting in the chip domain and
then correlating with s_k gives the same number as subtracting R_kj A_j b_j
from the matched filter output z_k, so the work is done on z and R.
"""

import math


def matched_filter(y: list[float], sigs: list[list[float]]) -> list[float]:
    """z_k = s_k^T y for each user k."""
    return [math.fsum(a * b for a, b in zip(s, y)) for s in sigs]


def crosscorrelation(sigs: list[list[float]]) -> list[list[float]]:
    """R[i][j] = s_i^T s_j."""
    return [[math.fsum(a * b for a, b in zip(si, sj)) for sj in sigs] for si in sigs]


def sic(z: list[float], r: list[list[float]], amps: list[float] | None = None, order: list[int] | None = None) -> tuple[list[int], list[int]]:
    """SIC on the matched filter outputs z with crosscorrelations r.

    With amps given, the users go in order of decreasing amplitude and the
    known amplitude is used to rebuild each signal. With amps None, the users
    go in order of decreasing |z_k| and the amplitude of each user is
    estimated as |x|, the magnitude of its output after cancellation (the
    estimate of Patel and Holtzman). An explicit order overrides both rules.
    Returns (decisions, order).
    """
    k_users = len(z)
    if amps is not None and (len(amps) != k_users or any(a <= 0.0 for a in amps)):
        raise ValueError("need one positive amplitude per user")
    if order is None:
        key = amps if amps is not None else [abs(v) for v in z]
        order = sorted(range(k_users), key=lambda u: -key[u])  # @line L1
    if sorted(order) != list(range(k_users)):
        raise ValueError("order must be a permutation of the users")
    b = [0] * k_users
    est = [0.0] * k_users
    done: list[int] = []
    for k in order:  # @line L2
        x = z[k] - math.fsum(r[k][j] * est[j] * b[j] for j in done)  # @line L3
        b[k] = 1 if x >= 0.0 else -1  # @line L4
        est[k] = amps[k] if amps is not None else abs(x)  # @line L5
        done.append(k)
    return b, order  # @line L6


def sic_detector(y: list[float], sigs: list[list[float]], amps: list[float] | None = None) -> list[int]:
    """The SIC decisions for the chip samples y."""
    z = matched_filter(y, sigs)
    r = crosscorrelation(sigs)
    return sic(z, r, amps)[0]


def sic_chip_domain(y: list[float], sigs: list[list[float]], amps: list[float]) -> list[int]:
    """The same detector with known amplitudes, written as subtraction of waveforms from y."""
    k_users = len(sigs)
    order = sorted(range(k_users), key=lambda u: -amps[u])
    res = list(y)
    b = [0] * k_users
    for k in order:
        x = math.fsum(a * c for a, c in zip(sigs[k], res))
        b[k] = 1 if x >= 0.0 else -1
        res = [v - amps[k] * b[k] * c for v, c in zip(res, sigs[k])]
    return b
