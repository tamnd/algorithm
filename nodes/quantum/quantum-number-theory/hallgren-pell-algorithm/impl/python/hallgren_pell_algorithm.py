# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hallgren-pell-algorithm/. The authors are listed in prov/6ZS7YE.jsonl.
"""Hallgren's quantum algorithm for Pell's equation x^2 - D y^2 = 1, simulated on a small state vector.

The order is Z[sqrt(D)] for a non-square D > 1. Its reduced principal ideals come in a cycle,
given by the continued fraction of sqrt(D): the k-th one is [Q_k, P_k + sqrt(D)] with the
generator theta_k = p_{k-1} + q_{k-1} sqrt(D), where p/q are the convergents, and its distance
is delta_k = ln(theta_k). One period of the cycle ends at the fundamental unit eps, and
delta_{k + period} = delta_k + R with the regulator R = ln(eps).

The quantum part samples the Fourier transform of the function
    f_N(k) = (the ideal I with the largest distance delta(I) <= k/N, floor(k - N delta(I))),
which repeats with the irrational period S = N R in the sense of Hallgren: f_N(k) = f_N(k')
only if |k' - k - uS| < 1 for an integer u. The input register has 8 qubits (qubit 0 is the least
significant bit), and the target register holds a 4-bit code of the value of f_N.

This file evaluates f_N by walking the cycle from the start. That is fine for the small D of the
tests. A real circuit reaches distance k/N in polynomial time by multiplying and reducing ideals,
and it does not need to walk.
"""

import cmath
import math
import random
from fractions import Fraction

from qsim import apply_oracle, apply_register_unitary, basis_state, fourier_matrix, marginal, probabilities, registers, sample


# ---------------------------------------------------------------- the cycle of reduced principal ideals


def is_square(n: int) -> bool:
    return n >= 0 and math.isqrt(n) ** 2 == n


def ideal_walk(D: int):
    """Yield (Q_k, P_k mod Q_k, x_k, y_k, delta_k) for k = 0, 1, 2, ... with theta_k = x_k + y_k sqrt(D)."""
    if D < 2 or is_square(D):
        raise ValueError("D must be a non-square integer above 1")
    s = math.isqrt(D)
    P, Q = 0, 1
    x, y, xp, yp = 1, 0, 0, 1  # theta_0 = 1 = p_{-1} + q_{-1} sqrt(D); (p_{-2}, q_{-2}) = (0, 1)
    rt = math.sqrt(D)
    while True:
        yield Q, P % Q, x, y, math.log(x + y * rt)
        a = (P + s) // Q
        x, y, xp, yp = a * x + xp, a * y + yp, x, y
        P = a * Q - P
        Q = (D - P * P) // Q


def ideals_up_to(D: int, t: float) -> list:
    """The ideals of the walk with distance at most t, and the first one beyond t."""
    out = []
    for item in ideal_walk(D):
        out.append(item)
        if item[4] > t:
            return out


def fundamental_unit(D: int):
    """The reference: the first theta_k with k > 0 and Q_k = 1. Returns (x, y, R)."""
    walk = ideal_walk(D)
    next(walk)
    for Q, _, x, y, d in walk:
        if Q == 1:
            return x, y, d


def brute_force_pell(D: int) -> tuple[int, int]:
    """The reference: the least y > 0 with D y^2 + 1 a square."""
    y = 1
    while not is_square(D * y * y + 1):
        y += 1
    return math.isqrt(D * y * y + 1), y


# ---------------------------------------------------------------- the quantum part


def f_values(D: int, N: float, q: int) -> list:
    """f_N(k) for k = 0, ..., q-1, as tuples (Q, P mod Q, offset)."""
    walk = ideals_up_to(D, (q - 1) / N)
    out, j = [], 0
    for k in range(q):
        while j + 1 < len(walk) and N * walk[j + 1][4] <= k:
            j += 1
        Q, P, _, _, d = walk[j]
        out.append((Q, P, math.floor(k - N * d)))
    return out


def label_codes(values: list) -> dict:
    """A fixed injective code of the values of f_N, in order of first appearance."""
    codes: dict = {}
    for v in values:
        codes.setdefault(v, len(codes))
    return codes


def circuit_distribution(D: int, N: float, n: int = 8, t: int = 4) -> dict:
    """The exact distribution of the measured c, from a state-vector simulation on n + t qubits."""
    q = 1 << n
    vals = f_values(D, N, q)
    codes = label_codes(vals)
    if len(codes) > 1 << t:
        raise ValueError("the target register is too small for the values of f_N")
    rk, rt = registers(n, t)
    s = basis_state(n + t, 0)
    F = fourier_matrix(q)
    s = apply_register_unitary(s, F, rk)  # @line L3
    s = apply_oracle(s, [rk], rt, lambda k: codes[vals[k]])  # @line L4
    s = apply_register_unitary(s, F, rk)  # @line L5
    return {c: p for (c,), p in marginal(probabilities(s), [rk]).items()}  # @line L6 (the distribution of the measurement)


def closed_form_distribution(D: int, N: float, q: int) -> dict:
    """P(c) = q^(-2) sum over values v of |sum_{k : f_N(k) = v} e^(2 pi i kc/q)|^2."""
    vals = f_values(D, N, q)
    level: dict = {}
    for k, v in enumerate(vals):
        level.setdefault(v, []).append(k)
    w = [cmath.exp(2j * math.pi * t / q) for t in range(q)]
    out = {}
    for c in range(q):
        tot = sum(abs(sum(w[k * c % q] for k in ks)) ** 2 for ks in level.values())
        out[c] = tot / (q * q)
    return out


# ---------------------------------------------------------------- the classical part


def convergents(num: int, den: int) -> list[Fraction]:
    out, h0, h1, k0, k1 = [], 0, 1, 1, 0
    while den:
        a = num // den
        num, den = den, num - a * den
        h0, h1 = h1, a * h1 + h0
        k0, k1 = k1, a * k1 + k0
        out.append(Fraction(h1, k1))
    return out


def unit_near(D: int, t: float, w: float):
    """The generator (x, y, delta) of the ideal (1) at a distance in [t - w, t + w] with delta > 0, if any."""
    if t + w <= 0:
        return None
    for Q, _, x, y, d in ideals_up_to(D, t + w):
        if Q == 1 and d > 0 and abs(d - t) <= w:
            return x, y, d
    return None


def regulator_candidates(c1: int, c2: int, q: int, N: float, B: float) -> list[float]:
    """The estimates t = a q/(N c1) of R with t <= B, one for each convergent a/b of c1/c2 with a > 0."""
    if c1 <= 0 or c2 <= 0:
        return []
    ts = [fr.numerator * q / (N * c1) for fr in convergents(c1, c2) if fr.numerator > 0]
    return [t for t in ts if t <= B]


def hallgren_pell(D: int, N: float, rng: random.Random, n: int = 8, dist=None, max_rounds: int = 60):
    """Return ((x, y), R, rounds): the fundamental solution of x^2 - D y^2 = 1, the regulator, and the rounds used.

    The register size q = 2^n must satisfy q >= 3 (N B)^2 for a known bound B >= R; here B = sqrt(q/3)/N.
    """
    q = 1 << n
    w = 1 / N
    B = math.sqrt(q / 3) / N
    if dist is None:
        dist = circuit_distribution(D, N, n)
    for rounds in range(1, max_rounds + 1):  # @line L1
        c1, c2 = sample(dist, rng), sample(dist, rng)  # @line L2
        found = []
        for t in regulator_candidates(c1, c2, q, N, B + w):  # @line L7
            u = unit_near(D, t, w)  # @line L8
            if u is not None:
                found.append(u)
        if not found:  # @line L9
            continue
        top = min(u[2] for u in found)  # @line L10
        K = math.ceil((B + 2 * w) / math.log(1 + math.sqrt(D)))
        hits = [u for k in range(1, K + 1) if (u := unit_near(D, top / k, w)) is not None]  # @line L11
        x, y, R = min(hits, key=lambda u: u[2])  # @line L12
        if x * x - D * y * y == -1:  # @line L13
            x, y = x * x + D * y * y, 2 * x * y
        return (x, y), R, rounds  # @line L14
    return None, None, max_rounds
