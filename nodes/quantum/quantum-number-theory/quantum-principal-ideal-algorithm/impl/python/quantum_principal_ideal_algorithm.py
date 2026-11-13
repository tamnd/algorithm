# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-principal-ideal-algorithm/. The authors are listed in prov/M8TEVB.jsonl.
"""The quantum principal ideal algorithm in a real quadratic field, simulated on a small state vector.

This is the smallest case of the S-unit method: the field is Q(sqrt(D)) with the order Z[sqrt(D)],
the unit rank is 1, and the set S is replaced by the single input ideal I. An ideal is a pair
(P, Q) that stands for the Z-module [Q, P + sqrt(D)], with Q > 0 and Q | D - P^2.

For a reduced ideal J and a real x, let J(x) be the reduced ideal mu J of its cycle with the largest
log|mu| <= x. The quantum part samples the Fourier transform of

    g(a, k) = (the ideal (I^a)(k/N), floor(k - N log|mu|)),

where (I^a)(k/N) = mu I^a. If I = (alpha), then g(a, k) = F(k + a N log|alpha|) for the same function
F of the principal cycle, so g hides the lattice of the pairs (a, -N log|beta|) with I^a = (beta).
Its rank-2 period lattice is the image of the group of I-units, and it holds a point with a = 1
exactly when I is principal.

The registers are a (4 qubits), k (5 qubits) and a 3-bit code of the value of g, 12 qubits in all.
When g takes more than 8 values, the tests use 3 qubits for a and 4 for the code, or the closed form.
This file computes I^a by repeated multiplication and reduction, and finds (I^a)(k/N) by walking the
cycle. That is fine for the small D of the tests. A real circuit uses repeated squaring and the
infrastructure to reach a distance in polynomial time.
"""

import cmath
import math
import random

from qsim import apply_oracle, apply_register_unitary, basis_state, fourier_matrix, marginal, probabilities, registers, sample


# ---------------------------------------------------------------- ideals of Z[sqrt(D)]


def is_square(n: int) -> bool:
    return n >= 0 and math.isqrt(n) ** 2 == n


def canon(D: int, P: int, Q: int) -> int:
    """The representative of P mod Q in (s - Q, s], with s = isqrt(D)."""
    s = math.isqrt(D)
    return s - ((s - P) % Q)


def is_ideal(D: int, P: int, Q: int) -> bool:
    return Q > 0 and (D - P * P) % Q == 0


def is_reduced(D: int, P: int, Q: int) -> bool:
    """[Q, P + sqrt(D)] is reduced if (P' + sqrt(D))/Q is a reduced quadratic irrational for some P' = P mod Q."""
    s = math.isqrt(D)
    P = canon(D, P, Q)
    return 0 < P and Q <= s + P


def step(D: int, P: int, Q: int):
    """One step forward on a cycle of reduced ideals: J' = ((P' + sqrt(D))/Q) J. Returns (P', Q', log of the factor)."""
    s = math.isqrt(D)
    P = canon(D, P, Q)
    a = (P + s) // Q
    P1 = a * Q - P
    Q1 = (D - P1 * P1) // Q
    return canon(D, P1, Q1), Q1, math.log((P1 + math.sqrt(D)) / Q)


def step_back(D: int, P: int, Q: int):
    """The inverse of step. Returns (P0, Q0, log of the factor of the forward step)."""
    P = canon(D, P, Q)
    Q0 = (D - P * P) // Q
    return canon(D, -P, Q0), Q0, math.log((P + math.sqrt(D)) / Q0)


def rho(D: int, P: int, Q: int):
    """One reduction step mu J with mu = (P' + sqrt(D))/Q and P' = -P mod Q. Returns (P', |Q'|, log|mu|)."""
    s = math.isqrt(D)
    if Q <= 2 * s:
        P1 = canon(D, -P, Q)
    else:
        P1 = (-P) % Q
        if 2 * P1 > Q:
            P1 -= Q
    Q1 = (D - P1 * P1) // Q
    return P1 % abs(Q1), abs(Q1), math.log(abs((P1 + math.sqrt(D)) / Q))


def reduce_ideal(D: int, P: int, Q: int):
    """A reduced ideal mu [Q, P + sqrt(D)]. Returns (P, Q, log|mu|)."""
    e = 0.0
    for _ in range(4 * Q.bit_length() + 8):
        if is_reduced(D, P, Q):
            return canon(D, P, Q), Q, e
        P, Q, d = rho(D, P, Q)
        e += d
    raise ArithmeticError("the reduction did not end")


def multiply(D: int, I1: tuple, I2: tuple):
    """The product of [Q1, P1 + sqrt(D)] and [Q2, P2 + sqrt(D)] as w [Q, P + sqrt(D)]. Returns (P, Q, w)."""
    (P1, Q1), (P2, Q2) = I1, I2
    vecs = [(Q1 * Q2, 0), (Q1 * P2, Q1), (Q2 * P1, Q2), (P1 * P2 + D, P1 + P2)]  # u + v sqrt(D) as (u, v)
    piv = None
    rest = []
    for u, v in vecs:
        if v == 0:
            rest.append(u)
            continue
        if piv is None:
            piv = (u, v)
            continue
        while v:  # Euclid on the second coordinates, keeping the first coordinates in the lattice
            t = piv[1] // v
            piv, (u, v) = (u, v), (piv[0] - t * u, piv[1] - t * v)
        rest.append(u)
    u0 = 0
    for u in rest:
        u0 = math.gcd(u0, u)
    v0, w = piv
    if w < 0:
        v0, w = -v0, -w
    if u0 % w or v0 % w:
        raise ArithmeticError("the product is not an ideal of Z[sqrt(D)]")
    Q = u0 // w
    return v0 // w % Q, Q, w


def reduced_power(D: int, I: tuple, a: int):
    """A reduced ideal J_a = mu I^a with its distance e_a = log|mu|, from I^(a-1) times I. Returns (P, Q, e_a)."""
    P, Q, e = math.isqrt(D), 1, 0.0  # I^0 = (1)
    for _ in range(a):
        P, Q, w = multiply(D, (P, Q), I)
        P, Q, d = reduce_ideal(D, P, Q)
        e += d - math.log(w)
    return P, Q, e


def cycle_around(D: int, P: int, Q: int, e: float, lo: float, hi: float) -> list:
    """The ideals (Q, P mod Q, distance) of the cycle of a reduced ideal at distance e, from the last one <= lo to the first one > hi."""
    P = canon(D, P, Q)
    while e > lo:
        P, Q, d = step_back(D, P, Q)
        e -= d
    out = [(Q, P % Q, e)]
    while e <= hi:
        P, Q, d = step(D, P, Q)
        e += d
        out.append((Q, P % Q, e))
    return out


def regulator(D: int) -> float:
    """The reference: R = log(eps), the distance from (1) back to (1) on the principal cycle."""
    P, Q, R = step(D, math.isqrt(D), 1)
    while Q != 1:
        P, Q, d = step(D, P, Q)
        R += d
    return R


def principal_cycle(D: int) -> list:
    """The reduced principal ideals (Q, P mod Q, x, y, delta) with generator theta = x + y sqrt(D), 0 <= delta < R."""
    s = math.isqrt(D)
    P, Q = 0, 1
    x, y, xp, yp = 1, 0, 0, 1
    out = []
    while True:
        out.append((Q, P % Q, x, y, math.log(x + y * math.sqrt(D))))
        a = (P + s) // Q
        x, y, xp, yp = a * x + xp, a * y + yp, x, y
        P = a * Q - P
        Q = (D - P * P) // Q
        if Q == 1:
            return out


# ---------------------------------------------------------------- the quantum part


def g_values(D: int, I: tuple, N: float, A: int, q: int) -> list:
    """g(a, k) for a < A and k < q, as a list of rows of tuples (Q, P mod Q, offset)."""
    rows = []
    for a in range(A):
        P, Q, e = reduced_power(D, I, a)
        walk = cycle_around(D, P, Q, e, 0.0, (q - 1) / N)
        row, j = [], 0
        for k in range(q):
            while j + 1 < len(walk) and N * walk[j + 1][2] <= k:
                j += 1
            Qj, Pj, d = walk[j]
            row.append((Qj, Pj, math.floor(k - N * d)))
        rows.append(row)
    return rows


def circuit_distribution(D: int, I: tuple, N: float, na: int = 4, nk: int = 5, t: int = 3) -> dict:
    """The exact distribution of the measured (b, c), from a state-vector simulation on na + nk + t qubits."""
    A, q = 1 << na, 1 << nk
    vals = g_values(D, I, N, A, q)
    codes: dict = {}
    for row in vals:
        for v in row:
            codes.setdefault(v, len(codes))
    if len(codes) > 1 << t:
        raise ValueError("the target register is too small for the values of g")
    ra, rk, rt = registers(na, nk, t)
    s = basis_state(na + nk + t, 0)
    s = apply_register_unitary(s, fourier_matrix(A), ra)  # @line L4
    s = apply_register_unitary(s, fourier_matrix(q), rk)  # @line L4
    s = apply_oracle(s, [ra, rk], rt, lambda a, k: codes[vals[a][k]])  # @line L5
    s = apply_register_unitary(s, fourier_matrix(A), ra)  # @line L6
    s = apply_register_unitary(s, fourier_matrix(q), rk)  # @line L6
    return marginal(probabilities(s), [ra, rk])  # @line L7 (the distribution of the measurement)


def closed_form_distribution(D: int, I: tuple, N: float, A: int = 16, q: int = 32) -> dict:
    """P(b, c) = (A q)^(-2) sum over values v of |sum_{g(a, k) = v} e^(2 pi i (ab/A + kc/q))|^2."""
    vals = g_values(D, I, N, A, q)
    level: dict = {}
    for a, row in enumerate(vals):
        for k, v in enumerate(row):
            level.setdefault(v, {}).setdefault(a, []).append(k)
    wa = [cmath.exp(2j * math.pi * x / A) for x in range(A)]
    wq = [cmath.exp(2j * math.pi * x / q) for x in range(q)]
    tot = [[0.0] * q for _ in range(A)]
    for rows in level.values():
        inner = {a: [sum(wq[k * c % q] for k in ks) for c in range(q)] for a, ks in rows.items()}
        for b in range(A):
            for c in range(q):
                tot[b][c] += abs(sum(wa[a * b % A] * s[c] for a, s in inner.items())) ** 2
    return {(b, c): tot[b][c] / (A * q) ** 2 for b in range(A) for c in range(q) if tot[b][c] > 1e-12}


# ---------------------------------------------------------------- the classical part


def distance_candidates(b: int, c: int, A: int, q: int, N: float, R: float) -> list:
    """The estimates (t, w) of log|alpha| in [0, R) from one sample (b, c), each with the window w.

    The peaks lie near c = j q/(N R) for an integer j, with b/A = c N log|alpha|/q mod 1. So the
    candidates are the t = (b/A + m) q/(c N) for integers m with t in [-w, R + w), and w = q/(|c| N A).
    Here c is taken in (-q/2, q/2], and the samples with j = 0 give no candidate.
    """
    cs = c if 2 * c < q else c - q
    if round(cs * N * R / q) == 0:
        return []
    u = q / (cs * N)
    w = abs(u) / A
    lo, hi = sorted((-w / u - b / A, (R + w) / u - b / A))
    ts = [(b / A + m) * u for m in range(math.floor(lo), math.ceil(hi) + 1)]
    return [(t, w) for t in sorted(ts) if -w <= t < R + w]


def principal_near(D: int, t: float, w: float, cycle: list, R: float) -> list:
    """The reduced principal ideals with distance within w of t mod R (classically, by the infrastructure)."""
    return [J for J in cycle if abs((J[4] - t + R / 2) % R - R / 2) <= w]


def quantum_principal_ideal(D: int, I: tuple, N: float, rng: random.Random, dist=None, na: int = 4, nk: int = 5, max_rounds: int = 30):
    """Decide whether the reduced ideal I = (P, Q) of Z[sqrt(D)] is principal.

    Returns ((x, y), delta, rounds) with I = (x + y sqrt(D)) and delta = log(x + y sqrt(D)), or (None, None, max_rounds).
    R is the regulator, which Hallgren's algorithm for Pell's equation computes first.
    """
    A, q = 1 << na, 1 << nk
    R = regulator(D)  # @line L1
    cycle = principal_cycle(D)  # the walk stands for the infrastructure of the classical check
    P, Q = canon(D, I[0], I[1]) % I[1], I[1]
    if dist is None:
        dist = circuit_distribution(D, I, N, na, nk)
    for rounds in range(1, max_rounds + 1):  # @line L2
        b, c = sample(dist, rng)  # @line L3
        for t, w in distance_candidates(b, c, A, q, N, R):  # @line L8
            for Qj, Pj, x, y, d in principal_near(D, t, w, cycle, R):  # @line L9
                if (Qj, Pj) == (Q, P):  # @line L10
                    return (x, y), d, rounds  # @line L11
    return None, None, max_rounds  # @line L12
