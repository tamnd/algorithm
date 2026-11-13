# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shor-algorithm/. The authors are listed in prov/MH2W70.jsonl.
"""Shor's algorithm: quantum order finding, continued fractions and Miller's reduction.

The quantum part runs on the state-vector simulator qsim (qubit 0 is the least
significant bit). The exponent register is qubits 0 .. t-1 and the work register
is qubits t .. t+n-1. Modular exponentiation is applied as one permutation of the
basis states; the gate-level circuit for it is on the page quantum-modular-exponentiation.
"""

import functools
import math
import random
from typing import Callable, Dict, List, Optional, Tuple

from qsim import H, apply_1q, apply_controlled_phase, apply_permutation, basis_state, marginal, probabilities, sample, swap_qubits

Sampler = Callable[[int, int, int, random.Random], int]


def exponent_qubits(N: int) -> int:
    """The least t with 2^t >= N^2."""
    return (N * N - 1).bit_length()


def work_qubits(N: int) -> int:
    """The number of qubits that hold a residue mod N."""
    return N.bit_length()


# ---------------------------------------------------------------- the quantum part


def qft(state: List[complex], reg: List[int]) -> None:
    """The quantum Fourier transform |x> -> 2^(-t/2) sum_y e^(2 pi i x y / 2^t) |y> on reg, gate by gate."""
    t = len(reg)
    for k in reversed(range(t)):
        apply_1q(state, reg[k], H)
        for m in reversed(range(k)):
            apply_controlled_phase(state, reg[m], reg[k], 2 * math.pi / 2 ** (k - m + 1))
    for i in range(t // 2):
        swap_qubits(state, reg[i], reg[t - 1 - i])


def inverse_qft(state: List[complex], reg: List[int]) -> None:
    """The inverse of qft: the same gates in reverse order with negated angles."""
    t = len(reg)
    for i in range(t // 2):
        swap_qubits(state, reg[i], reg[t - 1 - i])
    for k in range(t):
        for m in range(k):
            apply_controlled_phase(state, reg[m], reg[k], -2 * math.pi / 2 ** (k - m + 1))
        apply_1q(state, reg[k], H)


def order_finding_state(N: int, a: int, t: int) -> List[complex]:
    """The state of the order-finding circuit just before the measurement."""
    n = work_qubits(N)
    xs = list(range(t))
    state = basis_state(t + n, 1 << t)  # exponent 0, work register 1
    for q in xs:
        apply_1q(state, q, H)
    powers = [pow(a, x, N) for x in range(1 << t)]
    mask = (1 << t) - 1

    def modexp(i: int) -> int:  # |x>|y> -> |x>|y a^x mod N> for y < N, identity for y >= N
        x, y = i & mask, i >> t
        return i if y >= N else x | ((y * powers[x]) % N) << t

    state = apply_permutation(state, modexp)
    inverse_qft(state, xs)
    return state


def order_finding_distribution(N: int, a: int, t: int) -> Dict[int, float]:
    """The exact distribution of the measured exponent register."""
    return marginal(probabilities(order_finding_state(N, a, t)), list(range(t)))


@functools.lru_cache(maxsize=64)
def _cached_distribution(N: int, a: int, t: int) -> Tuple[Tuple[int, float], ...]:
    return tuple(sorted(order_finding_distribution(N, a, t).items()))


def simulator_sampler(N: int, a: int, t: int, rng: random.Random) -> int:
    """Run the order-finding circuit on the simulator and measure the exponent register.

    The state before the measurement is the same on every run, so it is computed once
    per (N, a, t) and each run draws a fresh outcome from it.
    """
    if t + work_qubits(N) > 16:
        raise ValueError("too many qubits for the state-vector simulator")
    return sample(dict(_cached_distribution(N, a, t)), rng)


# ---------------------------------------------------------------- continued fractions


def continued_fraction(p: int, q: int) -> List[int]:
    """The partial quotients of p/q for p >= 0 and q > 0 (exact integer arithmetic)."""
    out = []
    while q:
        out.append(p // q)
        p, q = q, p % q
    return out


def convergents(p: int, q: int) -> List[Tuple[int, int]]:
    """The convergents h_k/k_k of p/q, as pairs (h_k, k_k) in lowest terms."""
    h0, h1, k0, k1 = 0, 1, 1, 0
    out = []
    for a in continued_fraction(p, q):
        h0, h1 = h1, a * h1 + h0
        k0, k1 = k1, a * k1 + k0
        out.append((h1, k1))
    return out


def order_candidates(c: int, t: int, N: int) -> List[int]:
    """The denominators below N of the convergents of c / 2^t."""
    return [k for _, k in convergents(c, 1 << t) if 0 < k < N]


def order_from_measurement(c: int, t: int, N: int, a: int) -> Optional[int]:
    """The least candidate denominator k with a^k = 1 mod N, or None."""
    for k in order_candidates(c, t, N):
        if pow(a, k, N) == 1:
            return k
    return None


def quantum_order(N: int, a: int, rng: random.Random, sampler: Sampler = simulator_sampler, max_passes: int = 200) -> Optional[int]:
    """ORDER(a, N) of the page: a positive multiple of the order of a (r itself in a good pass).

    Returns None if no pass succeeds within max_passes (the pseudocode loops forever).
    """
    if math.gcd(a, N) != 1:
        raise ValueError("a and N must be coprime")
    t = exponent_qubits(N)  # @line L12
    Q = 1 << t
    for _ in range(max_passes):  # @line L13
        c = sampler(N, a, t, rng)  # @line L14, L15, L16, L17
        for _, q in convergents(c, Q):  # @line L18
            if q < N and pow(a, q, N) == 1:  # @line L19
                return q
    return None


def find_order(N: int, a: int, rng: random.Random, runs: int = 8, sampler: Sampler = simulator_sampler) -> Optional[int]:
    """The refined order finding of the variants: run the circuit `runs` times and return the least verified candidate.

    Each verified candidate is a multiple of the order r, and a run whose measured
    fraction is s/r with gcd(s, r) = 1 gives r itself. The least common multiple of
    two candidate denominators is also tried, which recovers r when two runs give
    r/gcd(s1, r) and r/gcd(s2, r) with gcd(s1, s2, r) = 1.
    """
    if math.gcd(a, N) != 1:
        raise ValueError("a and N must be coprime")
    t = exponent_qubits(N)
    best = None
    seen: List[int] = []
    for _ in range(runs):
        c = sampler(N, a, t, rng)
        for k in order_candidates(c, t, N):
            for e in [k] + [k * j // math.gcd(k, j) for j in seen]:
                if e < N and pow(a, e, N) == 1 and (best is None or e < best):
                    best = e
            if k not in seen:
                seen.append(k)
    return best


# ---------------------------------------------------------------- factoring


def is_probable_prime(N: int) -> bool:
    """Miller-Rabin with the first 12 primes as bases; exact for N < 3.3 * 10^24."""
    if N < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if N % p == 0:
            return N == p
    d, s = N - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for b in small:
        x = pow(b, d, N)
        if x in (1, N - 1):
            continue
        for _ in range(s - 1):
            x = x * x % N
            if x == N - 1:
                break
        else:
            return False
    return True


def integer_root(N: int, k: int) -> int:
    """The integer k-th root floor(N^(1/k)) for N >= 0 and k >= 1, by binary search on integers."""
    lo, hi = 0, 1 << (N.bit_length() // k + 1)
    while lo < hi:  # invariant: lo^k <= N < (hi + 1)^k
        mid = (lo + hi + 1) // 2
        if mid ** k <= N:
            lo = mid
        else:
            hi = mid - 1
    return lo


def perfect_power_root(N: int) -> Optional[int]:
    """Return b if N = b^k for some b >= 2 and k >= 2 (the least such b), else None."""
    best = None
    for k in range(2, N.bit_length() + 1):
        b = integer_root(N, k)
        if b > 1 and b ** k == N:
            best = b
    return best


def factor_from_order(N: int, a: int, m: int) -> Optional[int]:
    """Miller's step for any multiple m of the order r of a (lines L8 to L11).

    Write m = 2^s d with d odd and square y = a^d until the next square is 1. The last
    y before 1 equals a^(r/2) when r is even, so the result is the same as with r itself:
    gcd(a^(r/2) - 1, N) when r is even and a^(r/2) != -1 mod N, and None otherwise.
    """
    if m <= 0 or pow(a, m, N) != 1:
        raise ValueError("m must be a positive multiple of the order of a")
    d = m  # @line L8
    while d % 2 == 0:
        d //= 2
    y = pow(a, d, N)
    if y == 1:  # @line L9
        return None  # the order is odd
    while y * y % N != 1:  # @line L10
        y = y * y % N
    if y == N - 1:  # @line L11
        return None
    return math.gcd(y - 1, N)


def shor_factor(N: int, rng: random.Random, sampler: Sampler = simulator_sampler, tries: int = 20) -> Optional[int]:
    """SHOR(N) of the page: a nontrivial factor of the composite N, or None after `tries` bases."""
    if N < 4 or is_probable_prime(N):
        raise ValueError("N must be composite")
    if N % 2 == 0:  # @line L1
        return 2
    b = perfect_power_root(N)  # @line L2
    if b is not None:
        return b
    for _ in range(tries):  # @line L3
        a = rng.randrange(2, N - 1)  # @line L4
        g = math.gcd(a, N)  # @line L5
        if g > 1:  # @line L6
            return g
        m = quantum_order(N, a, rng, sampler=sampler)  # @line L7
        if m is not None:
            f = factor_from_order(N, a, m)
            if f is not None:
                return f
    return None
