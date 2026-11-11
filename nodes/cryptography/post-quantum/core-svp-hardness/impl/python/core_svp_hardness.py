# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/core-svp-hardness/. The authors are listed in prov/AEJ0J4.jsonl.
"""A core-SVP calculator for LWE in the model of Alkim, Ducas, Poppelmann
and Schwabe (USENIX Security 2016).

Primal attack: embed m LWE samples in a lattice of dimension d = m + n + 1
and volume q^m. BKZ with block size b succeeds, under the geometric series
assumption (GSA), when

    sigma * sqrt(b) <= delta(b)^(2 b - d - 1) * q^(m / d),
    delta(b) = ((pi b)^(1/b) * b / (2 pi e))^(1 / (2 (b - 1))).

Dual attack: BKZ-b finds a dual vector of length l = delta^(d - 1) q^(n / d)
in dimension d = m + n; it tells LWE from uniform with advantage about
eps = 4 exp(-2 pi^2 tau^2), tau = l sigma / q.

Core-SVP cost of one SVP call in dimension b: 2^(0.292 b) classical
(Becker, Ducas, Gama and Laarhoven, SODA 2016) and 2^(0.265 b) quantum
(Laarhoven 2015). The model counts one call and ignores the number of
calls, memory and lower-order terms, so it is a conservative estimate.

For study only. This is a rough model, not the lattice estimator of
Albrecht, Player and Scott; use that estimator to set real parameters.
The code does no cryptography and has no timing concerns.
"""

import math
from typing import Dict, Optional, Tuple

CLASSICAL = 0.292
QUANTUM = 0.265


def delta_bkz(b: int) -> float:
    """Root Hermite factor reached by BKZ-b (the usual asymptotic formula, for b >= 50)."""
    return ((math.pi * b) ** (1.0 / b) * b / (2 * math.pi * math.e)) ** (1.0 / (2 * (b - 1)))


def primal_succeeds(n: int, q: int, sigma: float, m: int, b: int) -> bool:
    """The GSA success condition with m samples and block size b (in logs)."""
    d = m + n + 1
    if b > d:
        return False
    lhs = math.log(sigma) + 0.5 * math.log(b)
    rhs = (2 * b - d - 1) * math.log(delta_bkz(b)) + (m / d) * math.log(q)
    return lhs <= rhs


def primal_block_size(n: int, q: int, sigma: float, m_max: int, b_min: int = 50) -> Tuple[int, int]:
    """The smallest b for which some m <= m_max satisfies the condition. Returns (b, m)."""
    for b in range(b_min, n + m_max + 2):
        for m in range(max(1, b - n - 1), m_max + 1):
            if primal_succeeds(n, q, sigma, m, b):
                return b, m
    raise ValueError("no block size found")


def dual_advantage(n: int, q: int, sigma: float, m: int, b: int) -> float:
    d = m + n
    length = delta_bkz(b) ** (d - 1) * q ** (n / d)
    tau = length * sigma / q
    return 4 * math.exp(-2 * math.pi ** 2 * tau ** 2)


def dual_cost_bits(n: int, q: int, sigma: float, m_max: int, c: float = CLASSICAL, b_min: int = 50) -> Tuple[float, int, int]:
    """The best (log2 cost, b, m) of the dual attack in the ADPS style.

    One BKZ-b run is assumed to give 2^(0.2075 b) short dual vectors, and
    about 1 / eps^2 vectors are needed, so the cost is
    c b + max(0, log2(1 / eps^2) - 0.2075 b).
    """
    best: Optional[Tuple[float, int, int]] = None
    for b in range(b_min, n + m_max + 1):
        for m in range(max(1, b - n), m_max + 1):
            eps = dual_advantage(n, q, sigma, m, b)
            if eps <= 0:
                continue
            need = -2 * math.log2(eps) if eps < 1 else 0.0
            bits = c * b + max(0.0, need - 0.2075 * b)
            if best is None or bits < best[0]:
                best = (bits, b, m)
    assert best is not None
    return best


def core_svp_bits(b: int) -> Dict[str, float]:
    """log2 of the cost of one SVP call in dimension b: 0.292 b and 0.265 b."""
    return {"classical": CLASSICAL * b, "quantum": QUANTUM * b}


def cbd_sigma(eta: int) -> float:
    """Standard deviation of the centered binomial distribution B_eta."""
    return math.sqrt(eta / 2)


def kyber_primal(k: int, eta1: int, n: int = 256, q: int = 3329) -> Tuple[int, int]:
    """Primal block size for Kyber's Module-LWE as plain LWE in dimension k n.

    Secret and error both follow B_eta1. At most (k + 1) n samples are used,
    as in the Kyber round 3 scripts' search range (an assumption here).
    """
    return primal_block_size(k * n, q, cbd_sigma(eta1), (k + 1) * n)
