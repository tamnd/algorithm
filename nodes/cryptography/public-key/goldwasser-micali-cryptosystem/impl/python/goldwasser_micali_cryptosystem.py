# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldwasser-micali-cryptosystem/. The authors are listed in prov/5FBQTT.jsonl.
"""Goldwasser-Micali probabilistic encryption (1984), one bit at a time.

Key: N = p q and a pseudosquare y (a non-square modulo p and modulo q).
A bit b is sent as y^b r^2 mod N for a fresh random unit r. The holder of p
reads the bit from the Legendre symbol of the ciphertext modulo p.

For study only. This code is not constant time, the primes are supplied by
the caller, and the scheme expands each bit to a full element of Z_N.
"""

import random
import secrets
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class PublicKey:
    n: int
    y: int


@dataclass(frozen=True)
class PrivateKey:
    p: int
    q: int


def jacobi(a: int, n: int) -> int:
    """The Jacobi symbol (a/n) for odd n > 0, by quadratic reciprocity.

    Cost: O(log n) steps on numbers below n, so O((log n)^2) bit operations.
    """
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be odd and positive")
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def _unit(n: int, rng: random.Random | None) -> int:
    """A uniform element of Z_n^*."""
    while True:
        r = rng.randrange(1, n) if rng is not None else secrets.randbelow(n - 1) + 1
        if gcd(r, n) == 1:
            return r


def is_square_mod_prime(a: int, p: int) -> bool:
    """Euler's criterion: a^((p-1)/2) = 1 (mod p) for a unit a. Cost: one exponentiation."""
    return pow(a, (p - 1) // 2, p) == 1


def keygen(p: int, q: int, rng: random.Random | None = None) -> tuple[PublicKey, PrivateKey]:
    """Make a key from two distinct odd primes. Cost: O(1) expected exponentiations.

    y is drawn uniformly from the pseudosquares by rejection: a random unit
    is a non-square modulo both primes with probability 1/4.
    """
    if p == q or p % 2 == 0 or q % 2 == 0:
        raise ValueError("p and q must be distinct odd primes")
    n = p * q  # @line L1
    while True:
        y = _unit(n, rng)  # @line L2
        if not is_square_mod_prime(y, p) and not is_square_mod_prime(y, q):
            break
    return PublicKey(n, y), PrivateKey(p, q)  # @line L3


def encrypt(pk: PublicKey, bits: list[int], rng: random.Random | None = None) -> list[int]:
    """Encrypt a list of bits. Cost: one squaring and at most two multiplications per bit."""
    out = []
    for b in bits:  # @line L4
        if b not in (0, 1):
            raise ValueError("each message entry must be 0 or 1")
        r = _unit(pk.n, rng)  # @line L5
        out.append((pk.y if b else 1) * r * r % pk.n)  # @line L6
    return out  # @line L7


def decrypt(sk: PrivateKey, cs: list[int]) -> list[int]:
    """Decrypt a list of ciphertexts. Cost: one exponentiation modulo p per bit."""
    bits = []
    for c in cs:  # @line L8
        bits.append(0 if is_square_mod_prime(c % sk.p, sk.p) else 1)  # @line L9
    return bits  # @line L10


def xor(pk: PublicKey, c1: int, c2: int) -> int:
    """The product of two ciphertexts encrypts the XOR of their bits."""
    return c1 * c2 % pk.n


def bits_of(data: bytes) -> list[int]:
    """The bits of a byte string, most significant bit first."""
    return [(byte >> (7 - i)) & 1 for byte in data for i in range(8)]


def bytes_of(bits: list[int]) -> bytes:
    """The inverse of bits_of."""
    return bytes(sum(bits[k + i] << (7 - i) for i in range(8)) for k in range(0, len(bits), 8))
