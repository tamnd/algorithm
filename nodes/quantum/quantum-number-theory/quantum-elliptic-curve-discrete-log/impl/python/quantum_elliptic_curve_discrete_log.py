# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-elliptic-curve-discrete-log/. The authors are listed in prov/RB6N46.jsonl.
"""Shor's discrete logarithm algorithm on an elliptic curve, run on a state-vector simulator.

The curve is y^2 = x^3 + A x + B over F_p, P is a point of order r and Q = xP. The circuit has an
exponent register a, an exponent register b and an accumulator register, in this order from
qubit 0 (qubit 0 is the least significant bit of a). The accumulator holds a curve point in
compressed form: the x coordinate (or p for the point at infinity O) and the parity of y.

As in the Proos-Zalka circuit, the group operation is a sequence of controlled additions of the
classical constants 2^j P and 2^j Q to the accumulator. Adding a constant point C is a
permutation of the points, R -> R + C, so each step is a permutation of the basis states.
The Fourier transforms are applied as dense matrices; the page on the quantum Fourier transform
gives the circuits.
"""

import math
import random

from qsim import apply_permutation, apply_register_unitary, basis_state, fourier_matrix, get_reg, marginal, padded, probabilities, registers, sample, set_reg

O = None  # the point at infinity


class Curve:
    """The curve y^2 = x^3 + A x + B over F_p, for a prime p > 3."""

    def __init__(self, p: int, A: int, B: int):
        if (4 * A**3 + 27 * B * B) % p == 0:
            raise ValueError("the curve is singular")
        self.p, self.A, self.B = p, A % p, B % p

    def points(self) -> list:
        p = self.p
        return [O] + [(x, y) for x in range(p) for y in range(p) if (y * y - x**3 - self.A * x - self.B) % p == 0]

    def neg(self, P):
        return O if P is O else (P[0], (-P[1]) % self.p)

    def add(self, P, Q):
        """The chord-and-tangent group law in affine coordinates."""
        p = self.p
        if P is O:
            return Q
        if Q is O:
            return P
        if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
            return O
        if P == Q:
            lam = (3 * P[0] * P[0] + self.A) * pow(2 * P[1], -1, p) % p
        else:
            lam = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, p) % p
        x3 = (lam * lam - P[0] - Q[0]) % p
        return x3, (lam * (P[0] - x3) - P[1]) % p

    def mul(self, k: int, P):
        """kP by double-and-add."""
        R, S = O, P
        if k < 0:
            k, S = -k, self.neg(P)
        while k:
            if k & 1:
                R = self.add(R, S)
            S = self.add(S, S)
            k >>= 1
        return R

    def order(self, P) -> int:
        k, R = 1, P
        while R is not O:
            R, k = self.add(R, P), k + 1
        return k

    # compressed encoding: x (or p for O) in the low bits, the parity of y in the top bit
    def code_bits(self) -> int:
        return self.p.bit_length() + 1

    def encode(self, P) -> int:
        xb = self.p.bit_length()
        if P is O:
            return self.p
        return P[0] | ((P[1] & 1) << xb)

    def decode(self, code: int):
        """The point with this code, or the string 'invalid' if no point has it."""
        xb = self.p.bit_length()
        x, par = code & ((1 << xb) - 1), code >> xb
        if x == self.p and par == 0:
            return O
        if x >= self.p:
            return "invalid"
        for y in range(self.p):
            if y & 1 == par and (y * y - x**3 - self.A * x - self.B) % self.p == 0:
                return x, y
        return "invalid"


def width(n: int) -> int:
    """The number of qubits that hold the values 0..n-1."""
    return max(1, (n - 1).bit_length())


def controlled_add(state: list, E: Curve, control: int, acc: list[int], C) -> list:
    """If qubit control is 1, map the accumulator |R> to |R + C>. Codes of no point are left alone."""
    table = {}
    for code in range(1 << len(acc)):
        R = E.decode(code)
        table[code] = code if R == "invalid" else E.encode(E.add(R, C))
    perm = []
    for x in range(len(state)):
        if (x >> control) & 1:
            perm.append(set_reg(x, acc, table[get_reg(x, acc)]))
        else:
            perm.append(x)
    return apply_permutation(state, perm)


def group_operation(state: list, E: Curve, P, Q, ra: list[int], rb: list[int], acc: list[int]) -> list:
    """|a>|b>|R> -> |a>|b>|R + aP + bQ> as 2n controlled additions of constant points."""
    for j, q in enumerate(ra):  # @line L4
        state = controlled_add(state, E, q, acc, E.mul(1 << j, P))
    for j, q in enumerate(rb):  # @line L5
        state = controlled_add(state, E, q, acc, E.mul(1 << j, Q))
    return state


def circuit_distribution(E: Curve, P, Q, r: int, fourier_size: int | None = None) -> dict:
    """The exact distribution of the measured pair (c, d).

    With fourier_size None the exponent registers hold 0..r-1 and the transform is the exact one of Z_r.
    With fourier_size = 2^m the registers hold 0..2^m - 1 and the transform is the one of Z_(2^m).
    """
    N = r if fourier_size is None else fourier_size
    k = width(N)
    ra, rb, acc = registers(k, k, E.code_bits())
    n = 2 * k + len(acc)
    if n > 14:
        raise ValueError("too many qubits for this simulator")
    F = padded(fourier_matrix(N), 1 << k)
    s = basis_state(n, set_reg(0, acc, E.encode(O)))
    s = apply_register_unitary(s, F, ra)  # @line L3 (F_N |0> is the uniform state on 0..N-1)
    s = apply_register_unitary(s, F, rb)
    s = group_operation(s, E, P, Q, ra, rb, acc)
    s = apply_register_unitary(s, F, ra)  # @line L6
    s = apply_register_unitary(s, F, rb)
    return marginal(probabilities(s), [ra, rb])


def closed_form_distribution(r: int, x: int) -> dict:
    """The distribution that the proof gives: (c, x c mod r) with probability 1/r each."""
    return {(c, x * c % r): 1 / r for c in range(r)}


def solve_congruence(c: int, d: int, r: int):
    """All x mod r with c x = d (mod r), as (x0, m): x = x0 (mod m). None if there is none."""
    g = math.gcd(c, r)
    if d % g:
        return None
    m = r // g
    if m == 1:
        return 0, 1
    return (d // g) * pow(c // g, -1, m) % m, m


def merge(x1: int, m1: int, x2: int, m2: int):
    """Combine x = x1 (mod m1) and x = x2 (mod m2). None if they disagree."""
    g = math.gcd(m1, m2)
    if (x2 - x1) % g:
        return None
    l = m1 // g * m2
    t = (x2 - x1) // g * pow(m1 // g, -1, m2 // g) % (m2 // g) if m2 // g > 1 else 0
    return (x1 + m1 * t) % l, l


def quantum_ecdlp(E: Curve, P, Q, r: int, rng: random.Random, max_runs: int = 50):
    """Return (x, runs) with xP = Q and 0 <= x < r, or (None, max_runs)."""
    dist = circuit_distribution(E, P, Q, r)  # the exact distribution of lines L3 to L7, computed once
    x, m = 0, 1  # @line L1
    for run in range(1, max_runs + 1):  # @line L2
        c, d = sample(dist, rng)  # @line L7
        sol = solve_congruence(c, d, r)  # @line L8
        if sol is None:
            continue
        merged = merge(x, m, sol[0], sol[1])  # @line L9
        x, m = sol if merged is None else merged
        if m == r and E.mul(x, P) == Q:  # @line L10
            return x, run  # @line L11
    return None, max_runs


def rounding_candidate(c: int, d: int, r: int, N: int):
    """Post-processing for the power-of-2 form: c/N is near k/r and d/N near xk/r (mod 1)."""
    k = (2 * r * c + N) // (2 * N) % r  # round(r c / N) mod r
    if math.gcd(k, r) != 1:
        return None
    t = (2 * r * d + N) // (2 * N) % r  # round(r d / N) mod r
    return t * pow(k, -1, r) % r


def power_of_two_success(E: Curve, P, Q, r: int, x: int, m: int) -> float:
    """The exact probability that one run of the power-of-2 form gives x by rounding."""
    N = 1 << m
    dist = circuit_distribution(E, P, Q, r, fourier_size=N)
    return sum(pr for (c, d), pr in dist.items() if rounding_candidate(c, d, r, N) == x)
