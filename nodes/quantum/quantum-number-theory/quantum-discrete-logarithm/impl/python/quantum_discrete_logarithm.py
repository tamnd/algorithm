# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-discrete-logarithm/. The authors are listed in prov/KD2HD3.jsonl.
"""Shor's quantum algorithm for discrete logarithms, run on a state-vector simulator.

The group is the subgroup <g> of Z_p^* of known order r, and h = g^x. The circuit has an
exponent register a, an exponent register b and a target register, in this order from qubit 0
(qubit 0 is the least significant bit of a). Two forms are given:

- the main form of the page: both exponent registers hold 0..r-1 and the Fourier transform
  is the exact one of Z_r, padded to the register;
- Shor's original form for a generator g of Z_p^* (r = p - 1): the exponent registers hold
  0..p-2, and the Fourier transform is the one of Z_q with q the least power of 2 above p.

The Fourier transforms are applied as dense matrices; the page on the quantum Fourier
transform gives the circuits. The oracle |a>|b>|y> -> |a>|b>|y xor g^a h^(-b) mod p> is applied
as a permutation of the basis states.
"""

import math
import random

from qsim import (
    apply_oracle,
    apply_register_unitary,
    basis_state,
    fourier_matrix,
    marginal,
    padded,
    probabilities,
    registers,
    sample,
)


def width(n: int) -> int:
    """The number of qubits that hold the values 0..n-1."""
    return max(1, (n - 1).bit_length())


def oracle_value(p: int, g: int, h: int, r: int, a: int, b: int) -> int:
    """f(a, b) = g^a h^(-b) mod p, with the exponent of h reduced mod r."""
    return pow(g, a, p) * pow(h, (-b) % r, p) % p


def circuit_state(p: int, g: int, h: int, r: int) -> tuple[list[complex], list[list[int]]]:
    """The state of the main circuit before the measurement, and its registers [a, b, target]."""
    k = width(r)
    regs = registers(k, k, p.bit_length())
    ra, rb, rt = regs
    n = 2 * k + len(rt)
    if n > 14:
        raise ValueError("too many qubits for this simulator")
    F = padded(fourier_matrix(r), 1 << k)
    s = basis_state(n, 0)
    s = apply_register_unitary(s, F, ra)  # @line L3 (F_r |0> is the uniform state on 0..r-1)
    s = apply_register_unitary(s, F, rb)
    s = apply_oracle(s, [ra, rb], rt, lambda a, b: oracle_value(p, g, h, r, a, b) if a < r and b < r else 0)  # @line L4
    s = apply_register_unitary(s, F, ra)  # @line L5
    s = apply_register_unitary(s, F, rb)
    return s, regs


def outcome_distribution(p: int, g: int, h: int, r: int) -> dict:
    """The exact distribution of the measured pair (c, d) of the main circuit."""
    s, (ra, rb, _) = circuit_state(p, g, h, r)
    return marginal(probabilities(s), [ra, rb])


def closed_form_distribution(r: int, x: int) -> dict:
    """The distribution that the proof gives: (c, -x c mod r) with probability 1/r each."""
    return {(c, (-x * c) % r): 1 / r for c in range(r)}


def solve_congruence(c: int, d: int, r: int):
    """All x mod r with c x = -d (mod r), as (x0, m): x = x0 (mod m). None if there is none."""
    g = math.gcd(c, r)
    if (-d) % g:
        return None
    m = r // g
    if m == 1:
        return 0, 1
    return (-d // g) * pow(c // g, -1, m) % m, m


def merge(x1: int, m1: int, x2: int, m2: int):
    """Combine x = x1 (mod m1) and x = x2 (mod m2). None if they disagree."""
    g = math.gcd(m1, m2)
    if (x2 - x1) % g:
        return None
    l = m1 // g * m2
    t = (x2 - x1) // g * pow(m1 // g, -1, m2 // g) % (m2 // g) if m2 // g > 1 else 0
    return (x1 + m1 * t) % l, l


def quantum_dlog(p: int, g: int, h: int, r: int, rng: random.Random, max_runs: int = 50):
    """Return (x, runs) with g^x = h (mod p) and 0 <= x < r, or (None, max_runs)."""
    dist = outcome_distribution(p, g, h, r)  # the exact distribution of lines L3 to L6, computed once
    x, m = 0, 1  # @line L1
    for run in range(1, max_runs + 1):  # @line L2
        c, d = sample(dist, rng)  # @line L6
        sol = solve_congruence(c, d, r)  # @line L7, L8
        if sol is None:
            continue  # cannot happen in an exact run; a noisy machine could give it
        merged = merge(x, m, sol[0], sol[1])  # @line L9
        if merged is None:
            x, m = sol
        else:
            x, m = merged
        if m == r and pow(g, x, p) == h % p:  # @line L10
            return x, run  # @line L11
    return None, max_runs


# ---------------------------------------------------------------- Shor's original form


def shor_q(p: int) -> int:
    """The least power of 2 above p, so that p < q < 2p."""
    q = 1
    while q <= p:
        q *= 2
    return q


def centered(z: int, q: int) -> int:
    """{z}_q: the residue of z mod q in (-q/2, q/2]."""
    z %= q
    return z - q if z > q // 2 else z


def shor_circuit_distribution(p: int, g: int, h: int) -> dict:
    """The exact distribution of (c, d, y) in Shor's form: g generates Z_p^*, registers over 0..p-2, QFT mod q."""
    r = p - 1
    q = shor_q(p)
    k = width(q)
    ra, rb, rt = registers(k, k, p.bit_length())
    n = 2 * k + len(rt)
    if n > 14:
        raise ValueError("too many qubits for this simulator")
    prep = padded(fourier_matrix(r), 1 << k)
    Fq = fourier_matrix(q)
    s = basis_state(n, 0)
    s = apply_register_unitary(s, prep, ra)
    s = apply_register_unitary(s, prep, rb)
    s = apply_oracle(s, [ra, rb], rt, lambda a, b: oracle_value(p, g, h, r, a, b) if a < r and b < r else 0)
    s = apply_register_unitary(s, Fq, ra)
    s = apply_register_unitary(s, Fq, rb)
    return marginal(probabilities(s), [ra, rb, rt])


def shor_amplitude_formula(p: int, x: int, c: int, d: int, k: int) -> complex:
    """Shor's closed form (6.6) for the amplitude of (c, d, g^k): x is the logarithm."""
    import cmath

    r, q = p - 1, shor_q(p)
    tot = 0j
    for b in range(r):
        e = b * x * c + k * c + b * d - c * r * ((b * x + k) // r)
        tot += cmath.exp(2j * math.pi * (e % q) / q)
    return tot / (r * q)


def shor_is_good(p: int, x: int, c: int, d: int) -> bool:
    """Shor's conditions (6.10) and (6.11) on the pair (c, d)."""
    r, q = p - 1, shor_q(p)
    cr = centered(c * r, q)
    T = x * c + d - x * cr / r
    return abs(T - q * round(T / q)) <= 0.5 and abs(cr) <= q / 12


def shor_candidate(p: int, c: int, d: int):
    """Shor's post-processing: x = -round(d (p-1)/q) / c' (mod p-1), or None if c' is not invertible."""
    r, q = p - 1, shor_q(p)
    cp = (c * r - centered(c * r, q)) // q
    if math.gcd(cp, r) != 1:
        return None
    t = (2 * d * r + q) // (2 * q)  # round(d r / q) with exact integers
    return (-t) * pow(cp, -1, r) % r
