# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/small-subgroup-attack/. The authors are listed in prov/MG2E7C.jsonl.
"""A small subgroup key recovery attack (Lim and Lee, Crypto 1997) on toy groups.

The victim has a static Diffie-Hellman secret x in a subgroup of prime order
q of Z_p^*. Here p - 1 = 2 q l_1 ... l_r with small primes l_i (a DSA-style
prime, not a safe prime). The attacker sends elements h of small order l in
place of a public key. If the victim does not check that h lies in the
subgroup of order q, its answer depends on h^x, which has only l possible
values, so the attacker learns x mod l by trying them all. The Chinese
remainder theorem then gives x mod l_1 ... l_r, which is x itself when that
product is larger than q.

For study only. The code is not constant time, and the attack runs only on
toy parameters against a local simulated victim. To defend real systems,
use X25519 from libsodium or the Python package cryptography, or check
each received group element as SP 800-56A Rev. 3 Section 5.6.2.3 says.

Cost: the attack makes one query per small prime l and tries at most l
exponents for each, so about l_1 + ... + l_r exponentiations in total.
"""

import hashlib
import random

# A toy DSA-style group: p - 1 = 2 * Q * (3 * 5 * 7 * 11 * 13 * 17 * 19 * 23).
SMALL_PRIMES = [3, 5, 7, 11, 13, 17, 19, 23]
Q = 16777289  # prime, about 2^24
P = 3742893553829431  # 2 * Q * 111546435 + 1, prime
G = 2367483421172228  # 2^((p - 1) / q) mod p, of order Q

# A toy safe-prime group: p = 2q + 1, generator 2 of order q (p = 7 mod 8).
SAFE_P = 140737488356903
SAFE_Q = (SAFE_P - 1) // 2
SAFE_G = 2


class ValidationError(ValueError):
    """A received element is not in the subgroup of order q."""


def _tag(z: int) -> bytes:
    """What the victim sends back: anything that depends on Z, here SHA-256 of Z."""
    return hashlib.sha256(z.to_bytes(8, "big")).digest()


class Victim:
    """A server with a static secret x. It answers each element h with a tag of h^x mod p."""

    def __init__(self, p: int, q: int, x: int, validate: bool) -> None:
        self.p, self.q, self.x, self.validate = p, q, x, validate

    def respond(self, h: int) -> bytes:
        if self.validate:
            if not 2 <= h <= self.p - 2 or pow(h, self.q, self.p) != 1:
                raise ValidationError("the element is not in the subgroup of order q")
        return _tag(pow(h, self.x, self.p))


def element_of_order(p: int, ell: int, rng: random.Random) -> int:
    """An element of order ell in Z_p^*, for a prime ell that divides p - 1."""
    while True:
        h = pow(rng.randrange(2, p - 1), (p - 1) // ell, p)
        if h != 1:
            return h


def crt(residues: list[tuple[int, int]]) -> tuple[int, int]:
    """Combine x = r_i mod m_i (pairwise coprime m_i) into x mod (m_1 ... m_k)."""
    x, m = 0, 1
    for r, mi in residues:
        t = (r - x) * pow(m, -1, mi) % mi
        x, m = x + m * t, m * mi
    return x % m, m


def small_subgroup_attack(victim: Victim, p: int, small_primes: list[int], rng: random.Random) -> tuple[int, int]:
    """Learn x mod each small prime and combine. Return (x mod M, M)."""
    residues = []
    for ell in small_primes:  # @line L1
        h = element_of_order(p, ell, rng)  # @line L2
        answer = victim.respond(h)  # @line L3
        t = next(t for t in range(ell) if _tag(pow(h, t, p)) == answer)  # @line L4
        residues.append((t, ell))
    return crt(residues)  # @line L5
