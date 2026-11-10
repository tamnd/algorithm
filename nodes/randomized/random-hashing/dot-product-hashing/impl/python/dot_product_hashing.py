# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dot-product-hashing/. The authors are listed in prov/2WYWCR.jsonl.

import random
from typing import Sequence


def key_digits(x: int, p: int, r: int) -> list[int]:
    """The r base-p digits of the key x, least significant first."""
    if not 0 <= x < p**r:
        raise ValueError("the key must lie in {0, ..., p^r - 1}")
    out = []
    for _ in range(r):
        out.append(x % p)
        x //= p
    return out


def draw_dot_product_hash(p: int, r: int, rng: random.Random) -> list[int]:
    """Draw a function of the family: a vector a uniform in {0, ..., p - 1}^r.

    p must be a prime. Keys are vectors of r digits in {0, ..., p - 1}, and
    the table has the p slots 0, ..., p - 1.
    """
    return [rng.randrange(p) for _ in range(r)]  # @line L1


def dot_product_hash(a: Sequence[int], x: Sequence[int], p: int) -> int:
    """h_a(x) = (a_0 x_0 + ... + a_{r-1} x_{r-1}) mod p."""
    if len(a) != len(x):
        raise ValueError("the key and the hash vector must have the same length")
    s = 0  # @line L2
    for ai, xi in zip(a, x):  # @line L3
        s = (s + ai * xi) % p  # @line L4
    return s  # @line L5


def draw_affine_dot_product_hash(p: int, r: int, rng: random.Random) -> tuple[list[int], int]:
    """The strongly universal variant: a vector a and an offset b, both uniform."""
    return [rng.randrange(p) for _ in range(r)], rng.randrange(p)


def affine_dot_product_hash(a: Sequence[int], b: int, x: Sequence[int], p: int) -> int:
    """h_{a,b}(x) = (a . x + b) mod p."""
    return (dot_product_hash(a, x, p) + b) % p


class DotProductHashTable:
    """A chained hash table on integer keys in {0, ..., p^r - 1} with a random dot-product hash."""

    def __init__(self, p: int, r: int, rng: random.Random) -> None:
        self.p = p
        self.r = r
        self.a = draw_dot_product_hash(p, r, rng)
        self.slots: list[list[int]] = [[] for _ in range(p)]

    def slot(self, key: int) -> int:
        return dot_product_hash(self.a, key_digits(key, self.p, self.r), self.p)

    def insert(self, key: int) -> None:
        chain = self.slots[self.slot(key)]
        if key not in chain:
            chain.append(key)

    def contains(self, key: int) -> bool:
        return key in self.slots[self.slot(key)]
