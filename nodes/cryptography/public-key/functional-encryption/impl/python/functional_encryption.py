# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/functional-encryption/. The authors are listed in prov/YYQV99.jsonl.
#
# Inner-product functional encryption from DDH: the scheme of Abdalla, Bourse, De Caro and
# Pointcheval (PKC 2015). A key for the vector y lets its holder compute <x, y> from an
# encryption of x, and nothing more. Decryption ends with a small discrete logarithm, solved
# here by baby-step giant-step, so the inner products must lie in a known small range.
# The group is the subgroup of squares modulo a safe prime p = 2q + 1.
# For study only. The 129-bit group is a toy and NOT secure, and the code is not constant time.
# Use a maintained FE library (for example CiFEr or GoFE of the FENTEC project) instead.

import math
import random


class Group:
    """The squares modulo a safe prime p = 2q + 1: a cyclic group of prime order q."""

    def __init__(self, p: int, g: int):
        self.p, self.q, self.g = p, (p - 1) // 2, g
        if pow(g, self.q, p) != 1 or g % p in (0, 1, p - 1):
            raise ValueError("g must generate the subgroup of order q")

    def exp(self, base: int, e: int) -> int:
        return pow(base, e % self.q, self.p)


# A 129-bit safe prime: q = 2^127 + 6225 is prime and so is 2q + 1. g = 4 is a square.
TOY = Group(340282366920938463463374607431768223907, 4)
TINY = Group(23, 4)  # q = 11, the group of the worked example


def baby_step_giant_step(G: Group, h: int, lo: int, hi: int):
    """The t in [lo, hi] with g^t = h, or None. O(sqrt(hi - lo)) time and space."""
    n = hi - lo + 1
    m = math.isqrt(n - 1) + 1
    target = h * G.exp(G.g, -lo) % G.p  # now find u in [0, n) with g^u = target
    baby = {}
    e = 1
    for j in range(m):
        baby.setdefault(e, j)
        e = e * G.g % G.p
    giant = G.exp(G.g, -m)
    gamma = target
    for i in range(m + 1):
        if gamma in baby:
            u = i * m + baby[gamma]
            if u < n:
                return lo + u
        gamma = gamma * giant % G.p
    return None


def setup(G: Group, length: int, rng: random.Random):
    s = [rng.randrange(G.q) for _ in range(length)]
    return [G.exp(G.g, si) for si in s], s


def keygen(G: Group, msk, y):
    if len(y) != len(msk):
        raise ValueError("length mismatch")
    return sum(si * yi for si, yi in zip(msk, y)) % G.q


def encrypt(G: Group, mpk, x, rng: random.Random, r=None):
    if r is None:
        r = rng.randrange(1, G.q)
    return G.exp(G.g, r), [G.exp(h, r) * G.exp(G.g, xi) % G.p for h, xi in zip(mpk, x)]


def decrypt_to_group(G: Group, sk_y: int, y, ct) -> int:
    """Return g^<x, y> = prod ct_i^(y_i) / ct_0^(sk_y)."""
    ct0, cts = ct
    num = 1
    for c, yi in zip(cts, y):
        num = num * G.exp(c, yi) % G.p
    return num * G.exp(ct0, -sk_y) % G.p


def decrypt(G: Group, sk_y: int, y, ct, bound: int):
    """Return <x, y> if |<x, y>| <= bound, else None."""
    return baby_step_giant_step(G, decrypt_to_group(G, sk_y, y, ct), -bound, bound)
