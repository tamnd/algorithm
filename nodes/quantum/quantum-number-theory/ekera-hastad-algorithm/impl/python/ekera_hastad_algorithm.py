# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ekera-hastad-algorithm/. The authors are listed in prov/86HVR8.jsonl.
"""The Ekera-Hastad quantum algorithm for short discrete logarithms, and its use for factoring RSA integers.

The group is Z_N^* (N prime or composite), x = g^d with 0 <= d < 2^m, and the order of g is not
needed. One run uses an exponent register a of l + m qubits, an exponent register b of l qubits
and a target register, in this order from qubit 0 (qubit 0 is the least significant bit of a).
It prepares the uniform superposition with Hadamard gates, computes g^a x^(-b), applies the
quantum Fourier transforms of sizes 2^(l+m) and 2^l, and measures (j, k).

Small circuits are simulated state by state. For larger ones the exact distribution of (j, k)
comes from the closed form of the proof, which needs the order of g to be at least
2^(l+m) + 2^l d. The classical part builds a lattice from s pairs, reduces it with LLL
(exact rational arithmetic) and enumerates the lattice vectors near a target vector.
"""

import cmath
import math
import random
from fractions import Fraction

from qsim import apply_oracle, apply_register_unitary, basis_state, fourier_matrix, marginal, probabilities, registers, sample


def centered(z: int, M: int) -> int:
    """{z}_M: the residue of z mod M in [-M/2, M/2)."""
    z %= M
    return z - M if z >= M // 2 else z


# ---------------------------------------------------------------- the quantum part


def circuit_distribution(N: int, g: int, x: int, m: int, l: int) -> dict:
    """The exact distribution of (j, k) from a state-vector simulation of one run."""
    ra, rb, rt = registers(l + m, l, N.bit_length())
    n = 2 * l + m + len(rt)
    if n > 14:
        raise ValueError("too many qubits for this simulator")
    xinv = pow(x, -1, N)
    s = basis_state(n, 0)
    Fa, Fb = fourier_matrix(1 << (l + m)), fourier_matrix(1 << l)
    s = apply_register_unitary(s, Fa, ra)  # @line L4 (the transform of |0> is the uniform state, as with Hadamard gates)
    s = apply_register_unitary(s, Fb, rb)
    s = apply_oracle(s, [ra, rb], rt, lambda a, b: pow(g, a, N) * pow(xinv, b, N) % N)  # @line L5
    s = apply_register_unitary(s, Fa, ra)  # @line L6
    s = apply_register_unitary(s, Fb, rb)
    return marginal(probabilities(s), [ra, rb])  # @line L7 (the distribution of the measurement)


def closed_form_probability(d: int, m: int, l: int, j: int, k: int) -> float:
    """P(j, k) = 2^(-2(2l+m)) sum_e |sum_{b in B_e} w^(bT)|^2 with T = dj + 2^m k and w = e^(2 pi i/2^(l+m))."""
    A, B = 1 << (l + m), 1 << l
    T = (d * j + (1 << m) * k) % A
    tot = 0.0
    for e in range(-(B - 1) * d, A):
        amp = 0j
        for b in range(B):
            if 0 <= e + b * d < A:
                amp += cmath.exp(2j * math.pi * (b * T % A) / A)
        tot += abs(amp) ** 2
    return tot / (A * B) ** 2


def closed_form_distribution(d: int, m: int, l: int) -> dict:
    """The exact distribution of (j, k), valid when the order of g is at least 2^(l+m) + 2^l d."""
    A, B = 1 << (l + m), 1 << l
    cache: dict = {}
    out = {}
    for j in range(A):
        for k in range(B):
            T = (d * j + (1 << m) * k) % A
            if T not in cache:
                cache[T] = closed_form_probability(d, m, l, j, k)
            out[(j, k)] = cache[T]
    return out


def is_good(d: int, m: int, l: int, j: int, k: int) -> bool:
    """A good pair has |{dj + 2^m k}| <= 2^(m-2) modulo 2^(l+m)."""
    return 4 * abs(centered(d * j + (1 << m) * k, 1 << (l + m))) <= 1 << m


# ---------------------------------------------------------------- lattice tools


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def gram_schmidt(B):
    """The Gram-Schmidt vectors and coefficients mu of the rows of B, in exact rationals."""
    Bs, mu = [], [[Fraction(0)] * len(B) for _ in B]
    for i, b in enumerate(B):
        v = [Fraction(c) for c in b]
        for k in range(i):
            mu[i][k] = dot(b, Bs[k]) / dot(Bs[k], Bs[k])
            v = [vi - mu[i][k] * wk for vi, wk in zip(v, Bs[k])]
        Bs.append(v)
    return Bs, mu


def lll(B, delta=Fraction(3, 4)):
    """LLL reduction of the rows of an integer basis B (exact, recomputes Gram-Schmidt after each change)."""
    B = [list(b) for b in B]
    k = 1
    Bs, mu = gram_schmidt(B)
    while k < len(B):
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                B[k] = [a - q * c for a, c in zip(B[k], B[j])]
                Bs, mu = gram_schmidt(B)
        if dot(Bs[k], Bs[k]) >= (delta - mu[k][k - 1] ** 2) * dot(Bs[k - 1], Bs[k - 1]):
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            Bs, mu = gram_schmidt(B)
            k = max(k - 1, 1)
    return B


def close_vectors(B, v, R2):
    """All lattice vectors w (integer combinations of the rows of the full-rank basis B) with |w - v|^2 <= R2."""
    Bs, mu = gram_schmidt(B)
    n = len(B)
    norms = [dot(b, b) for b in Bs]
    nu = [dot(v, Bs[i]) / norms[i] for i in range(n)]  # v in Gram-Schmidt coordinates
    out = []
    y = [0] * n

    def rec(i, partial):
        if i < 0:
            out.append([sum(y[t] * B[t][c] for t in range(n)) for c in range(len(v))])
            return
        c = nu[i] - sum(mu[t][i] * y[t] for t in range(i + 1, n))
        rad2 = (R2 - partial) / norms[i]
        if rad2 < 0:
            return
        half = math.isqrt(math.floor(rad2)) + 1  # an integer above sqrt(rad2); the exact test below decides
        for yi in range(math.floor(c) - half, math.ceil(c) + half + 1):
            dlt = (yi - c) ** 2 * norms[i]
            if partial + dlt <= R2:
                y[i] = yi
                rec(i - 1, partial + dlt)
        y[i] = 0

    rec(n - 1, Fraction(0))
    return out


# ---------------------------------------------------------------- the classical part


def lattice_and_target(pairs, m: int, l: int):
    A = 1 << (l + m)
    s = len(pairs)
    B = [[j for j, _ in pairs] + [1]] + [[A if c == i else 0 for c in range(s + 1)] for i in range(s)]
    v = [centered(-(1 << m) * k, A) for _, k in pairs] + [0]
    return B, v


def radius2(s: int, m: int) -> Fraction:
    """(s/4 + 1) 4^m, the square of the search radius."""
    return Fraction(s + 4, 4) * 4**m


def candidates(pairs, m: int, l: int) -> list[int]:
    """The last coordinates d' in [0, 2^m) of the lattice vectors within the radius of the target."""
    B, v = lattice_and_target(pairs, m, l)  # @line L8, L9
    R = lll(B)  # @line L10
    ws = close_vectors(R, v, radius2(len(pairs), m))
    return sorted({w[-1] for w in ws if 0 <= w[-1] < 1 << m})  # @line L11


def brute_candidates(pairs, m: int, l: int) -> list[int]:
    """The reference: every d' in [0, 2^m) whose closest lattice vector is within the radius."""
    A = 1 << (l + m)
    R2 = radius2(len(pairs), m)
    return [e for e in range(1 << m) if sum(centered(e * j + (1 << m) * k, A) ** 2 for j, k in pairs) + e * e <= R2]


def ekera_hastad(N: int, g: int, x: int, m: int, s: int, rng: random.Random, dist=None, max_batches: int = 30):
    """Return (d, runs) with g^d = x (mod N) and 0 <= d < 2^m, or (None, runs) if every batch fails."""
    l = -(-m // s)  # @line L1
    if dist is None:
        dist = circuit_distribution(N, g, x, m, l)
    runs = 0
    for _ in range(max_batches):  # @line L2
        pairs = []
        for _ in range(s):  # @line L3
            pairs.append(sample(dist, rng))
            runs += 1
        for e in candidates(pairs, m, l):
            if pow(g, e, N) == x % N:  # @line L12
                return e, runs
    return None, runs


def exact_distribution(N: int, g: int, x: int, m: int, l: int) -> dict:
    """The exact distribution of (j, k) for any order of g, without a state vector.

    The target register holds y = g^a x^(-b), so the terms with equal y interfere and the others do not:
    P(j, k) = (2^(2l+m))^(-2) sum_y |sum_{(a, b) -> y} w^(aj + 2^m bk)|^2 with w = e^(2 pi i/2^(l+m)).
    """
    A, B = 1 << (l + m), 1 << l
    xinv = pow(x, -1, N)
    classes: dict = {}
    for a in range(A):
        ga = pow(g, a, N)
        for b in range(B):
            classes.setdefault(ga * pow(xinv, b, N) % N, []).append((a, b))
    w = [cmath.exp(2j * math.pi * t / A) for t in range(A)]
    out = {}
    for j in range(A):
        for k in range(B):
            tot = 0.0
            for members in classes.values():
                amp = sum(w[(a * j + (b * k << m)) % A] for a, b in members)
                tot += abs(amp) ** 2
            out[(j, k)] = tot / (A * B) ** 2
    return out


def factor_rsa(N: int, n: int, s: int, rng: random.Random, max_bases: int = 10):
    """Factor N = pq with 2^(n-1) < p, q < 2^n through the short logarithm d = (p + q - 2)/2."""
    m = n  # 2^(n-1) <= d < 2^n
    l = -(-m // s)
    for _ in range(max_bases):
        g = rng.randrange(2, N - 1)  # @line L13
        if math.gcd(g, N) > 1:
            return tuple(sorted((math.gcd(g, N), N // math.gcd(g, N))))
        x = pow(g, (N - 1) // 2, N)  # @line L14
        d, _ = ekera_hastad(N, g, x, m, s, rng, dist=exact_distribution(N, g, x, m, l), max_batches=10)  # @line L15
        if d is None:
            continue
        c = d + 1  # @line L16
        disc = c * c - N
        if disc >= 0 and math.isqrt(disc) ** 2 == disc:
            p, q = c - math.isqrt(disc), c + math.isqrt(disc)  # @line L17
            if p * q == N and 1 < p:
                return p, q
    return None
