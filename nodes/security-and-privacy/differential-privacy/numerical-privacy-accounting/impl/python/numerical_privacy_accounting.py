# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/numerical-privacy-accounting/. The authors are listed in prov/XTW2ZE.jsonl.
"""Numerical privacy loss distribution (PLD) accounting with the FFT.

A PLD on a grid of step h is a list of masses: mass[j] sits at the loss
(lo + j) * h, and inf_mass sits at +infinity. Composing k mechanisms with
independent noise convolves their PLDs, which the FFT does in
O(N log N) for N about k times the grid size. The tight delta at epsilon is

    delta(epsilon) = inf_mass + sum_j mass[j] * max(0, 1 - e^(epsilon - loss_j)),

and epsilon for a target delta comes from bisection. Rounding each loss up
to the grid (pessimistic) gives an upper bound on delta; rounding down
(optimistic) gives a lower bound, so the two bracket the exact value.

The code is accounting only, in floats, in the real RAM model. The mechanisms
that it accounts for need a cryptographic source of randomness and exact
sampling of their noise in a deployment (Mironov 2012; Canonne, Kamath and
Steinke 2020).
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from statistics import NormalDist
from typing import List, Sequence, Tuple


@dataclass(frozen=True)
class Pld:
    """A privacy loss distribution on the grid (lo + j) * step."""

    lo: int
    masses: Tuple[float, ...]
    step: float
    inf_mass: float = 0.0

    def loss(self, j: int) -> float:
        return (self.lo + j) * self.step


def fft(a: Sequence[complex], invert: bool = False) -> List[complex]:
    """Iterative radix-2 FFT. Precondition: len(a) is a power of 2.

    With invert=True it computes the inverse transform, including the 1/N.
    Cost: O(N log N) arithmetic operations, O(N) space.
    """
    n = len(a)
    if n & (n - 1):
        raise ValueError("the length must be a power of 2")
    out = list(a)
    j = 0
    for i in range(1, n):  # bit-reversal permutation
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            out[i], out[j] = out[j], out[i]
    length = 2
    sign = 1.0 if invert else -1.0
    while length <= n:
        w_len = cmath.exp(sign * 2j * math.pi / length)
        half = length // 2
        for start in range(0, n, length):
            w = 1.0 + 0j
            for k in range(half):
                u = out[start + k]
                v = out[start + k + half] * w
                out[start + k] = u + v
                out[start + k + half] = u - v
                w *= w_len
        length <<= 1
    if invert:
        out = [x / n for x in out]
    return out


def compose(pld: Pld, k: int) -> Pld:
    """The PLD of k independent copies of the mechanism with PLD pld.

    Precondition: k >= 1. Cost: O(N log N) with N < 2 k n for n grid points.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    n = len(pld.masses)
    size = 1
    while size < k * (n - 1) + 1:  # @line L1
        size <<= 1
    spectrum = fft([complex(m) for m in pld.masses] + [0j] * (size - n))  # @line L2
    powered = [z**k for z in spectrum]  # @line L3
    values = fft(powered, invert=True)  # @line L4
    masses = tuple(max(0.0, z.real) for z in values[: k * (n - 1) + 1])
    inf_k = 1.0 - (1.0 - pld.inf_mass) ** k  # @line L5
    return Pld(k * pld.lo, masses, pld.step, inf_k)


def delta_for_epsilon(pld: Pld, epsilon: float) -> float:
    """The delta of the PLD at epsilon. Cost: O(n) for n grid points."""
    total = pld.inf_mass  # @line L6
    for j, m in enumerate(pld.masses):
        loss = pld.loss(j)
        if m > 0.0 and loss > epsilon:
            total += m * -math.expm1(epsilon - loss)
    return min(1.0, total)


def numerical_accountant(pld: Pld, k: int, epsilon: float) -> float:
    """delta(epsilon) for the k-fold composition of pld (lines L1 to L7).

    Precondition: k >= 1, epsilon >= 0. Cost: O(k n log(k n)) for n grid points.
    """
    composed = compose(pld, k)  # lines L1 to L5
    return delta_for_epsilon(composed, epsilon)  # @line L7


def epsilon_for_delta(pld: Pld, delta: float, tol: float = 1e-9) -> float:
    """The least epsilon >= 0 with delta_for_epsilon(pld, epsilon) <= delta, up to tol.

    It returns an epsilon with delta(epsilon) <= delta, found by bisection.
    Precondition: delta > pld.inf_mass. Cost: O(n log(L / tol)) for loss range L.
    """
    if delta <= pld.inf_mass:
        raise ValueError("delta must exceed the mass at infinity")
    lo = 0.0
    if delta_for_epsilon(pld, lo) <= delta:
        return lo
    hi = max(pld.loss(len(pld.masses) - 1), 0.0) + 1.0  # delta(hi) = inf_mass < delta
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if delta_for_epsilon(pld, mid) <= delta:
            hi = mid
        else:
            lo = mid
    return hi


def gaussian_pld(mu: float, step: float, pessimistic: bool = True, width: float = 10.0) -> Pld:
    """The discretized PLD of the Gaussian mechanism with mu = sensitivity / sigma.

    The exact PLD is N(mu^2 / 2, mu^2). Each grid cell ((i-1) h, i h] goes to
    i h (pessimistic) or to (i-1) h (optimistic). Pessimistic: the mass below
    the grid goes to the lowest grid point and the mass above it goes to
    +infinity. Optimistic: both tails are dropped. So the pessimistic PLD
    gives an upper bound on delta and the optimistic PLD a lower bound.
    Precondition: mu > 0, step > 0. Cost: O(n) with n = 2 width mu / step.
    """
    if mu <= 0 or step <= 0:
        raise ValueError("mu and step must be positive")
    law = NormalDist(mu * mu / 2, mu)
    i_lo = math.floor((law.mean - width * mu) / step)
    i_hi = math.ceil((law.mean + width * mu) / step)
    cdf = [law.cdf(i * step) for i in range(i_lo - 1, i_hi + 1)]
    cells = [max(0.0, cdf[j + 1] - cdf[j]) for j in range(len(cdf) - 1)]
    if pessimistic:
        cells[0] += cdf[0]  # the mass below (i_lo - 1) h, rounded up to i_lo h
        return Pld(i_lo, tuple(cells), step, 1.0 - cdf[-1])
    return Pld(i_lo - 1, tuple(cells), step, 0.0)


def randomized_response_pld(m: int, step: float) -> Pld:
    """The PLD of randomized response with epsilon_0 = m * step, on the grid of step.

    The loss is +epsilon_0 with probability e^eps0 / (1 + e^eps0) and
    -epsilon_0 otherwise; both are grid points, so there is no rounding.
    Precondition: m >= 1, step > 0. Cost: O(m).
    """
    if m < 1 or step <= 0:
        raise ValueError("need m >= 1 and step > 0")
    p = 1.0 / (1.0 + math.exp(-m * step))
    masses = [0.0] * (2 * m + 1)
    masses[0] = 1.0 - p
    masses[-1] = p
    return Pld(-m, tuple(masses), step, 0.0)
