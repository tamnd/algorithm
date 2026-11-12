# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wiener-attack/. The authors are listed in prov/TNJ165.jsonl.
"""Wiener's attack: recover a small RSA private exponent from the public key.

Wiener (1990) observed that ed = 1 + k*phi(N) makes k/d a very good rational
approximation of e/N, so good that Legendre's theorem forces k/d to be one
of the continued fraction convergents of e/N. There are only about
log(N) convergents, so the private exponent falls out of a short loop
whenever d < N^(1/4)/3 and q < p < 2q.

The module holds the continued fraction machinery, the attack, and a toy
key generator that builds a weak key on purpose.

For study only. The code is not constant time, and it runs on toy keys made
inside this process. A real key with e = 65537 has a private exponent of
the full size, and this attack says nothing about it.
"""

import math
from dataclasses import dataclass


def continued_fraction(numerator: int, denominator: int) -> list:
    """The partial quotients of numerator / denominator, by Euclid's division."""
    quotients = []
    while denominator:
        quotient, remainder = divmod(numerator, denominator)
        quotients.append(quotient)
        numerator, denominator = denominator, remainder
    return quotients


def convergents(quotients: list):
    """The convergents h_i / k_i of a continued fraction, in order.

    The standard recurrences are h_i = a_i h_{i-1} + h_{i-2} and
    k_i = a_i k_{i-1} + k_{i-2}, with h_{-1} = 1, h_{-2} = 0, k_{-1} = 0 and
    k_{-2} = 1. Each pair is in lowest terms.
    """
    h_previous, h_current = 0, 1
    k_previous, k_current = 1, 0
    for quotient in quotients:
        h_previous, h_current = h_current, quotient * h_current + h_previous
        k_previous, k_current = k_current, quotient * k_current + k_previous
        yield h_current, k_current


def is_square(value: int) -> bool:
    """True when value is a perfect square. Uses an exact integer square root."""
    if value < 0:
        return False
    root = math.isqrt(value)
    return root * root == value


def wiener_attack(n: int, e: int):
    """Recover (p, q, d) from the public key when d is small. None on failure.

    Each convergent k/d of e/N is a guess. The guess names phi(N), then the
    sum p + q, then a quadratic whose roots are the two primes. The final
    test p*q = N accepts only the right guess, so the attack never returns
    a wrong answer.
    """
    # @line L1
    quotients = continued_fraction(e, n)
    # @line L2
    for k, d in convergents(quotients):
        # @line L3
        if k == 0 or d % 2 == 0:
            continue
        # @line L4
        if (e * d - 1) % k != 0:
            continue
        # @line L5
        phi = (e * d - 1) // k
        # @line L6
        total = n - phi + 1  # the guess for p + q
        # @line L7
        if total < 0 or total % 2 != 0:
            continue
        # @line L8
        discriminant = total * total - 4 * n  # the guess for (p - q)^2
        # @line L9
        if not is_square(discriminant):
            continue
        # @line L10
        root = math.isqrt(discriminant)
        p, q = (total + root) // 2, (total - root) // 2
        # @line L11
        if p * q == n:
            return p, q, d
    # @line L12
    return None


def wiener_bound(n: int) -> int:
    """The largest integer below N^(1/4)/3, the exponent bound of the theorem."""
    quarter = math.isqrt(math.isqrt(n))
    return quarter // 3


@dataclass
class ToyWeakKey:
    """A toy RSA key built with a small private exponent on purpose."""

    p: int
    q: int
    d: int

    def __post_init__(self) -> None:
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        if math.gcd(self.d, self.phi) != 1:
            raise ValueError("d must be a unit modulo phi(N)")
        self.e = pow(self.d, -1, self.phi)

    @property
    def public(self) -> tuple:
        return self.n, self.e

    def is_in_the_wiener_range(self) -> bool:
        """The two hypotheses of the theorem: the ratio of the primes and d."""
        small, large = min(self.p, self.q), max(self.p, self.q)
        return large < 2 * small and self.d <= wiener_bound(self.n)


def weak_key(p: int, q: int, rnd, bound: int = 0) -> ToyWeakKey:
    """Draw a small odd d coprime to phi(N) and invert it to get e.

    bound is the exclusive upper limit for d; it defaults to the bound of
    the theorem, N^(1/4)/3.
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    limit = bound or wiener_bound(n)
    if limit < 3:
        raise ValueError("the modulus is too small for a weak exponent")
    while True:
        d = rnd.randrange(limit // 2, limit) | 1
        if math.gcd(d, phi) == 1 and pow(d, -1, phi) > 1:
            return ToyWeakKey(p=p, q=q, d=d)
