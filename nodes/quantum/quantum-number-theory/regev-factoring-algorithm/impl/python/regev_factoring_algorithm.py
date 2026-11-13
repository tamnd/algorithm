# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regev-factoring-algorithm/. The authors are listed in prov/GJ2PQ0.jsonl.
"""Regev's quantum factoring algorithm, with an exact simulation of the quantum step.

The quantum step (lines L5 to L7) is simulated exactly. The register |e> holds
prod a_i^(z_i + D/2) mod N and is never used again, so it acts as a measured
register: for each value e the z register holds a Gaussian restricted to one coset
of the relation lattice L. The QFT over Z_D^d is applied to each part as a
d-dimensional discrete Fourier transform, and the outcome distribution is the sum
of the squared magnitudes. This is exact up to floating-point rounding.

The classical post-processing (lines L8 to L13) uses exact integers and fractions.
"""

import bisect
import cmath
import math
import random
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

Vector = Tuple[int, ...]


# ---------------------------------------------------------------- classical checks


def first_primes(d: int) -> List[int]:
    """The first d primes."""
    out: List[int] = []
    k = 2
    while len(out) < d:
        if all(k % p for p in out if p * p <= k):
            out.append(k)
        k += 1
    return out


def integer_root(N: int, k: int) -> int:
    """The largest integer r with r^k <= N."""
    lo, hi = 0, 1 << (N.bit_length() // k + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** k <= N:
            lo = mid
        else:
            hi = mid - 1
    return lo


def classical_checks(N: int, d: int) -> Optional[int]:
    """Return a nontrivial factor found without the quantum step, or None."""
    if N < 4:
        raise ValueError("N must be a composite number of at least 4")
    if N % 2 == 0:  # @line L1
        return 2
    for k in range(2, N.bit_length() + 1):  # @line L1
        r = integer_root(N, k)
        if r > 1 and r ** k == N:
            return r
    for b in first_primes(d):  # @line L2
        if N % b == 0 and b < N:
            return b
    return None


# ---------------------------------------------------------------- the quantum step


def tree_product(xs: Sequence[int]) -> int:
    """The product of small integers, multiplied pairwise in a binary tree."""
    xs = list(xs)
    if not xs:
        return 1
    while len(xs) > 1:
        xs = [xs[i] * xs[i + 1] if i + 1 < len(xs) else xs[i] for i in range(0, len(xs), 2)]
    return xs[0]


def exponent_product(z: Sequence[int], a: Sequence[int], N: int, D: int) -> Tuple[int, int]:
    """prod a_i^(z_i + D/2) mod N by repeated squaring over the bits of all exponents at once.

    Returns the value and the number of multiplications of n-bit numbers it used.
    """
    bits = D.bit_length() - 1
    shifted = [zi + D // 2 for zi in z]
    e, big = 1, 0
    for j in reversed(range(bits)):  # @line L6: most significant bit first
        e = e * e % N  # one squaring of an n-bit number
        small = tree_product([ai for ai, s in zip(a, shifted) if (s >> j) & 1])
        e = e * small % N  # one product of an n-bit number with a small one
        big += 2
    return e, big


def gaussian(z: Sequence[int], R: float) -> float:
    """The Gaussian function rho_R(z) = exp(-pi |z|^2 / R^2)."""
    return math.exp(-math.pi * sum(x * x for x in z) / (R * R))


def fft(xs: List[complex]) -> List[complex]:
    """The DFT y_w = sum_z x_z e^(2 pi i z w / D) for D a power of 2 (radix 2)."""
    D = len(xs)
    if D == 1:
        return list(xs)
    even, odd = fft(xs[0::2]), fft(xs[1::2])
    out = [0j] * D
    for k in range(D // 2):
        t = cmath.exp(2j * math.pi * k / D) * odd[k]
        out[k], out[k + D // 2] = even[k] + t, even[k] - t
    return out


def dft_nd(arr: List[complex], D: int, d: int) -> List[complex]:
    """The DFT over Z_D^d of an array indexed by sum_i z_i D^i (the QFT on d registers)."""
    arr = list(arr)
    for axis in range(d):
        stride = D ** axis
        for start in range(len(arr)):
            if (start // stride) % D:
                continue
            idx = [start + k * stride for k in range(D)]
            line = fft([arr[i] for i in idx])
            for i, v in zip(idx, line):
                arr[i] = v
    return arr


def unflatten(idx: int, D: int, d: int) -> Vector:
    return tuple((idx // D ** i) % D for i in range(d))


def outcome_distribution(N: int, a: Sequence[int], D: int, R: float) -> Dict[Vector, float]:
    """The exact distribution of the measured w in Z_D^d after lines L5 to L7."""
    d = len(a)
    if D < 2 or D & (D - 1):
        raise ValueError("D must be a power of 2")
    size = D ** d
    parts: Dict[int, List[complex]] = {}
    norm = 0.0
    for idx in range(size):
        z = [x - D if x >= D // 2 else x for x in unflatten(idx, D, d)]  # z in [-D/2, D/2)^d
        amp = gaussian(z, R)  # @line L5
        e, _ = exponent_product(z, a, N, D)  # @line L6
        parts.setdefault(e, [0j] * size)[idx] = amp
        norm += amp * amp
    prob = [0.0] * size
    for arr in parts.values():
        for w, c in enumerate(dft_nd(arr, D, d)):  # @line L7
            prob[w] += abs(c) ** 2
    scale = size * norm
    return {unflatten(w, D, d): p / scale for w, p in enumerate(prob) if p > 0}


class Sampler:
    """Draws outcomes w from an outcome distribution (the measurement of line L7)."""

    def __init__(self, dist: Dict[Vector, float]) -> None:
        self.keys = sorted(dist)
        acc, self.cum = 0.0, []
        for k in self.keys:
            acc += dist[k]
            self.cum.append(acc)

    def draw(self, rng: random.Random) -> Vector:
        i = bisect.bisect_right(self.cum, rng.random() * self.cum[-1])
        return self.keys[min(i, len(self.keys) - 1)]


# ---------------------------------------------------------------- classical post-processing


def postprocessing_basis(ws: Sequence[Vector], D: int) -> List[List[int]]:
    """Basis vectors of the lattice L' of line L8 (Regev's matrix B with S = D, so all entries are integers)."""
    d, m = len(ws[0]), len(ws)
    basis = []
    for j in range(d):  # @line L8
        basis.append([int(r == j) for r in range(d)] + [w[j] for w in ws])
    for i in range(m):  # @line L8
        basis.append([0] * d + [D * int(r == i) for r in range(m)])
    return basis


def lll(basis: Sequence[Sequence[int]], delta: Fraction = Fraction(3, 4)) -> List[List[int]]:
    """The LLL algorithm in exact rational arithmetic. The input vectors must be independent."""
    b = [list(v) for v in basis]
    n = len(b)

    def dot(u: Sequence, v: Sequence) -> Fraction:
        return sum((x * y for x, y in zip(u, v)), Fraction(0))

    def gram_schmidt() -> Tuple[List[List[Fraction]], List[Fraction]]:
        star: List[List[Fraction]] = []
        mu = [[Fraction(0)] * n for _ in range(n)]
        sq: List[Fraction] = []
        for i in range(n):
            v = [Fraction(x) for x in b[i]]
            for j in range(i):
                mu[i][j] = dot(b[i], star[j]) / sq[j]
                v = [x - mu[i][j] * y for x, y in zip(v, star[j])]
            star.append(v)
            sq.append(dot(v, v))
        return mu, sq

    mu, sq = gram_schmidt()
    k = 1
    while k < n:
        for j in reversed(range(k)):  # size reduction
            q = round(mu[k][j])
            if q:
                b[k] = [x - q * y for x, y in zip(b[k], b[j])]
                for i in range(j):
                    mu[k][i] -= q * mu[j][i]
                mu[k][j] -= q
        if sq[k] >= (delta - mu[k][k - 1] ** 2) * sq[k - 1]:  # Lovasz condition
            k += 1
        else:
            b[k], b[k - 1] = b[k - 1], b[k]
            mu, sq = gram_schmidt()
            k = max(k - 1, 1)
    return b


def product_mod(bases: Sequence[int], u: Sequence[int], N: int) -> int:
    """prod bases_i^(u_i) mod N; negative exponents use inverses."""
    x = 1
    for base, ui in zip(bases, u):
        x = x * pow(base, ui, N) % N
    return x


def recover_factor(reduced: Sequence[Sequence[int]], b: Sequence[int], N: int) -> Optional[int]:
    """Lines L10 to L13: look for u in L \\ L0 among the reduced vectors."""
    a = [x * x for x in b]
    d = len(b)
    for v in reduced:
        u = v[:d]  # @line L10
        if any(u) and product_mod(a, u, N) == 1:  # @line L11
            x = product_mod(b, u, N)  # @line L12
            if x not in (1, N - 1):  # @line L13
                return math.gcd(x - 1, N)  # @line L13
    return None  # @line L14


# ---------------------------------------------------------------- the algorithm


def regev_factor(N: int, d: int, D: int, R: float, rng: random.Random,
                 sampler: Optional[Sampler] = None) -> Optional[int]:
    """One attempt of Regev's algorithm. Returns a nontrivial factor of N, or None if this attempt fails."""
    f = classical_checks(N, d)
    if f is not None:
        return f
    b = first_primes(d)  # @line L2
    a = [x * x for x in b]  # @line L3
    if sampler is None:
        sampler = Sampler(outcome_distribution(N, a, D, R))
    ws = [sampler.draw(rng) for _ in range(d + 4)]  # @line L4, L5, L6, L7
    reduced = lll(postprocessing_basis(ws, D))  # @line L8, L9
    return recover_factor(reduced, b, N)  # @line L10, L11, L12, L13


def relation_lattice_contains(a: Sequence[int], u: Sequence[int], N: int) -> bool:
    """Whether u is in L = {z : prod a_i^(z_i) = 1 mod N}."""
    return product_mod(a, u, N) == 1
