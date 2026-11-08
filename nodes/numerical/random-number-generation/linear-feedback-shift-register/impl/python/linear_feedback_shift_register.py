# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-feedback-shift-register/. The authors are listed in prov/C3FG9T.jsonl.

"""Linear feedback shift registers over GF(2), in Fibonacci and Galois form.

A polynomial over GF(2) is an int: bit i is the coefficient of x^i. The
characteristic polynomial of degree k is P(x) = x^k + c_1 x^(k-1) + ... + c_k,
and the output bits satisfy s_(i+k) = c_1 s_(i+k-1) xor ... xor c_k s_i.
"""


def taps_word(poly: int, k: int) -> int:
    """The tap word T of the Fibonacci form: bit k-j of T is c_j, so T = P - x^k."""
    if poly >> k != 1:
        raise ValueError("poly must have degree exactly k")
    return poly ^ (1 << k)


class FibonacciLFSR:
    """State word: bit j holds s_(i+j) for j = 0 .. k-1; the oldest bit s_i is bit 0."""

    def __init__(self, poly: int, k: int, state: int) -> None:
        self.k, self.t = k, taps_word(poly, k)
        self.mask = (1 << k) - 1
        self.s = state & self.mask
        if self.s == 0:
            raise ValueError("the zero state is a fixed point")

    def step(self) -> int:
        b = bin(self.s & self.t).count("1") & 1  # @line L1
        out = self.s & 1  # @line L2
        self.s = (self.s >> 1) | (b << (self.k - 1))  # @line L3
        return out  # @line L4


class GaloisLFSR:
    """State t is a polynomial of degree < k; one step computes t <- x t mod P."""

    def __init__(self, poly: int, k: int, state: int) -> None:
        if poly >> k != 1:
            raise ValueError("poly must have degree exactly k")
        self.k, self.p = k, poly
        self.s = state & ((1 << k) - 1)
        if self.s == 0:
            raise ValueError("the zero state is a fixed point")

    def step(self) -> int:
        out = (self.s >> (self.k - 1)) & 1  # @line L5
        self.s <<= 1  # @line L6
        if out:  # @line L7
            self.s ^= self.p  # clears bit k  # @line L8
        return out  # @line L9


def gf2_mulmod(a: int, b: int, p: int, k: int) -> int:
    """a * b mod p over GF(2), for a, b of degree < k = deg p."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if (a >> k) & 1:
            a ^= p
    return r


def gf2_powmod(a: int, e: int, p: int, k: int) -> int:
    r = 1 if k > 0 else 0
    while e:
        if e & 1:
            r = gf2_mulmod(r, a, p, k)
        a = gf2_mulmod(a, a, p, k)
        e >>= 1
    return r


def _prime_factors(n: int) -> list[int]:
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def is_primitive(poly: int, k: int) -> bool:
    """True when x has order exactly 2^k - 1 modulo poly, i.e. poly is primitive."""
    if k < 1 or poly >> k != 1:
        return False
    if k == 1:
        return poly == 0b11
    n = (1 << k) - 1
    x = 0b10
    if gf2_powmod(x, n, poly, k) != 1:
        return False
    return all(gf2_powmod(x, n // q, poly, k) != 1 for q in _prime_factors(n))


def state_period(step_state, s0: int) -> int:
    """Brute-force period of a bijective state map from s0."""
    s, n = step_state(s0), 1
    while s != s0:
        s, n = step_state(s), n + 1
    return n
