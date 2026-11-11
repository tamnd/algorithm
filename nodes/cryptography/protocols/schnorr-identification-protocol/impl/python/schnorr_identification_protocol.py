# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schnorr-identification-protocol/. The authors are listed in prov/99NZYX.jsonl.
"""The Schnorr identification protocol, in a toy group and in RFC 3526 group 14.

The prover holds x with public key y = g^x in a group of prime order q.

    prover:   k <- uniform in Z_q,  a = g^k          (commitment)
    verifier: c <- uniform in [0, 2^t)                (challenge of t bits)
    prover:   z = k + c x mod q                       (response)
    verifier: accept iff g^z = a y^c

Group 14 of RFC 3526 is the safe prime
    p = 2^2048 - 2^1984 - 1 + 2^64 (floor(2^1918 pi) + 124476),
computed here from that formula with pi from Machin's formula. Since p = 7
mod 8, the number 2 is a square mod p, so g = 2 generates the subgroup of
prime order q = (p - 1) / 2.

For study only. The code is not constant time and the parties are local
simulated objects. Use a reviewed library such as libsodium or a FIPS 140
validated module for real authentication.
"""

import secrets


# ------------------------------------------------------------ groups
def arctan_inv(n: int, one: int) -> int:
    """arctan(1/n) * one, by its Taylor series in fixed point."""
    total = term = one // n
    n2, k, sign = n * n, 1, -1
    while term:
        term //= n2
        total += sign * (term // (2 * k + 1))
        sign, k = -sign, k + 1
    return total


def floor_pi_times_2_pow(e: int) -> int:
    """floor(2^e * pi), with 64 guard bits; Machin: pi = 16 atan(1/5) - 4 atan(1/239)."""
    guard = 64
    one = 1 << (e + guard)
    pi = 16 * arctan_inv(5, one) - 4 * arctan_inv(239, one)
    # Each series loses at most a few units in the last place; 64 guard bits
    # leave the integer part exact unless 2^e pi is within 2^-50 of an integer.
    return pi >> guard


def rfc3526_group14_prime() -> int:
    return 2**2048 - 2**1984 - 1 + 2**64 * (floor_pi_times_2_pow(1918) + 124476)


class Group:
    """The subgroup of prime order q = (p - 1) / 2 of Z_p^*, for a safe prime p."""

    def __init__(self, p: int, g: int):
        self.p, self.q, self.g = p, (p - 1) // 2, g
        assert g not in (0, 1) and pow(g, self.q, p) == 1

    def contains(self, a: int) -> bool:
        return 0 < a < self.p and pow(a, self.q, self.p) == 1


TOY = Group(2039, 4)                  # q = 1019
GROUP14 = Group(rfc3526_group14_prime(), 2)


# ------------------------------------------------------------ the protocol
def keygen(G: Group, rand=secrets.randbelow):
    x = 1 + rand(G.q - 1)                                         # @line L1
    return x, pow(G.g, x, G.p)


class Prover:
    def __init__(self, G: Group, x: int, rand=secrets.randbelow):
        self.G, self.x, self.rand = G, x, rand

    def commit(self, k: int = None) -> int:
        self.k = self.rand(self.G.q) if k is None else k          # @line L2
        return pow(self.G.g, self.k, self.G.p)

    def respond(self, c: int) -> int:
        return (self.k + c * self.x) % self.G.q                    # @line L4


def challenge(t: int, rand=secrets.randbelow) -> int:
    return rand(2**t)                                              # @line L3


def verify(G: Group, y: int, a: int, c: int, z: int, t: int) -> bool:
    if not (G.contains(y) and G.contains(a)):                       # @line L5
        return False
    if not (0 <= z < G.q and 0 <= c < 2**t):
        return False
    return pow(G.g, z, G.p) == a * pow(y, c, G.p) % G.p             # @line L6


def identify(G: Group, prover: Prover, y: int, t: int, rand=secrets.randbelow) -> bool:
    """One full run between a prover and an honest verifier."""
    a = prover.commit()
    c = challenge(t, rand)
    return verify(G, y, a, c, prover.respond(c), t)


# ------------------------------------------------------------ attacks and tools
class GuessingImpersonator:
    """Does not know x. Guesses the challenge c* and prepares a = g^z y^-c*."""

    def __init__(self, G: Group, y: int, guess: int, z: int):
        self.G, self.y, self.guess, self.z = G, y, guess, z

    def commit(self) -> int:
        G = self.G
        return pow(G.g, self.z, G.p) * pow(self.y, (-self.guess) % G.q, G.p) % G.p

    def respond(self, c: int) -> int:
        return self.z            # correct only if c equals the guess


def simulate(G: Group, y: int, c: int, z: int):
    """Honest-verifier simulator: an accepting (a, c, z) without x."""
    return pow(G.g, z, G.p) * pow(y, (-c) % G.q, G.p) % G.p, c, z


def key_from_nonce_reuse(G: Group, c1: int, z1: int, c2: int, z2: int) -> int:
    """Two answers with the same k and c1 != c2 give x = (z1 - z2) / (c1 - c2) mod q."""
    return (z1 - z2) * pow(c1 - c2, -1, G.q) % G.q


def is_probable_prime(n: int, bases=(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)) -> bool:
    if n < 2:
        return False
    for b in bases:
        if n % b == 0:
            return n == b
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for b in bases:
        x = pow(b, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True
