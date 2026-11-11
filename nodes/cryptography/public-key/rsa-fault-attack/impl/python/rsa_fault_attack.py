# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-fault-attack/. The authors are listed in prov/YCAWG0.jsonl.
"""The Bellcore fault attack on RSA with the Chinese remainder theorem.

Boneh, DeMillo and Lipton (Eurocrypt 1997) showed that one wrong bit in one
half of a CRT signature gives the factors of the modulus. With the
improvement of Lenstra (1996), the attacker needs the message, the faulty
signature and the public key, and nothing else:

    gcd(s'^e - m mod N, N) = the prime whose half was computed correctly.

The file holds a toy signer that can be told to inject a fault, the attack,
and the two standard countermeasures: verify the signature before it leaves
the device, and Shamir's trick.

For study only. The signatures here are raw RSA with no padding, the key is
a toy, the code is not constant time, and the "fault" is a local function
argument, not an attack on any device.
"""

import math
from dataclasses import dataclass


@dataclass
class CrtKey:
    """A toy RSA key with the CRT values. All of it stays in this process."""

    p: int
    q: int
    e: int

    def __post_init__(self) -> None:
        if self.p == self.q:
            raise ValueError("the two primes must differ")
        self.n = self.p * self.q
        lam = math.lcm(self.p - 1, self.q - 1)
        if math.gcd(self.e, lam) != 1:
            raise ValueError("e must be a unit modulo lcm(p-1, q-1)")
        self.d = pow(self.e, -1, lam)
        self.d_p = self.d % (self.p - 1)
        self.d_q = self.d % (self.q - 1)
        self.q_inverse = pow(self.q, -1, self.p)

    @property
    def public(self) -> tuple:
        return self.n, self.e


def sign_plain(key: CrtKey, message: int) -> int:
    """Raw RSA signing with the full private exponent. The slow reference."""
    return pow(message, key.d, key.n)


def sign_crt(key: CrtKey, message: int, fault_in: str = "none",
             fault_mask: int = 1) -> int:
    """Raw RSA-CRT signing, about four times faster than sign_plain.

    fault_in selects where a single fault lands: "none", "p" for the half
    modulo p, "q" for the half modulo q, or "both". fault_mask is the value
    the half is XORed with, which models a flipped bit in a register or in
    a memory word.
    """
    s_p = pow(message, key.d_p, key.p)
    s_q = pow(message, key.d_q, key.q)
    if fault_in in ("p", "both"):
        s_p ^= fault_mask
    if fault_in in ("q", "both"):
        s_q ^= fault_mask
    return garner(key, s_p, s_q)


def garner(key: CrtKey, s_p: int, s_q: int) -> int:
    """Recombine the two halves: the value that is s_p mod p and s_q mod q."""
    return (s_q + key.q * ((s_p - s_q) * key.q_inverse % key.p)) % key.n


def sign_crt_verified(key: CrtKey, message: int, fault_in: str = "none",
                      fault_mask: int = 1):
    """The first countermeasure: check the signature with the public key.

    Returns None when the check fails, so the faulty value never leaves the
    device and the attacker gets no equation. The cost is one exponentiation
    with the small public exponent.
    """
    signature = sign_crt(key, message, fault_in, fault_mask)
    if pow(signature, key.e, key.n) != message % key.n:
        return None
    return signature


def sign_crt_shamir(key: CrtKey, message: int, small_prime: int,
                    fault_in: str = "none", fault_mask: int = 1):
    """Shamir's trick: compute each half modulo p*r and q*r and compare mod r.

    Both halves equal m^d mod r when no fault happened, so a mismatch
    reports a fault without any public-key operation. A fault inside r
    itself, or a fault after the check, is not caught; this is the known
    limit of the trick.
    """
    s_p = pow(message, key.d, key.p * small_prime)
    s_q = pow(message, key.d, key.q * small_prime)
    if fault_in in ("p", "both"):
        s_p ^= fault_mask
    if fault_in in ("q", "both"):
        s_q ^= fault_mask
    if s_p % small_prime != s_q % small_prime:
        return None
    return garner(key, s_p % key.p, s_q % key.q)


def bellcore_attack(n: int, e: int, message: int, faulty: int):
    """Factor n from one faulty CRT signature of a known message.

    Returns (p, q, d) or None. The attacker uses the public key only.
    """
    # @line L1
    if pow(faulty, e, n) == message % n:
        return None  # no fault, so there is nothing to learn
    # @line L2
    g = math.gcd((pow(faulty, e, n) - message) % n, n)
    # @line L3
    if g in (1, n):
        return None
    # @line L4
    other = n // g
    # @line L5
    d = pow(e, -1, math.lcm(g - 1, other - 1))
    # @line L6
    return g, other, d


def lenstra_difference_attack(n: int, correct: int, faulty: int):
    """The older form: with the correct signature too, one gcd is enough.

    The two signatures agree modulo the prime whose half was right, so
    gcd(correct - faulty, n) is that prime. This needs no exponentiation,
    but it needs a second signature of the same message.
    """
    g = math.gcd((correct - faulty) % n, n)
    if g in (1, n):
        return None
    return g, n // g
