# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minhash/. The authors are listed in prov/4BV5E4.jsonl.

import hashlib
import math
from typing import Callable, Hashable, Iterable, Sequence

HashFn = Callable[[Hashable], int]


def minhash_signature(a: Iterable[Hashable], hashes: Sequence[HashFn]) -> list[float]:
    """Return the MinHash signature of the set a: for each hash function, the least value on a.

    The empty set gives [inf, ..., inf]. Cost: len(hashes) * |a| hash evaluations.
    """
    items = set(a)
    sig: list[float] = []
    for h in hashes:  # @line L1
        m = math.inf  # @line L2
        for x in items:  # @line L3
            m = min(m, h(x))  # @line L4
        sig.append(m)
    return sig  # @line L5


def estimate_jaccard(sa: Sequence[float], sb: Sequence[float]) -> float:
    """Return the fraction of positions where two signatures of equal length k >= 1 agree. Cost O(k)."""
    if len(sa) != len(sb) or not sa:
        raise ValueError("signatures must have the same positive length")
    m = 0  # @line L6
    for i in range(len(sa)):  # @line L7
        if sa[i] == sb[i]:  # @line L8
            m += 1
    return m / len(sa)  # @line L9


def make_hashes(k: int, seed: int = 0) -> list[HashFn]:
    """Return k independent-looking 64-bit hash functions, keyed BLAKE2b of repr(x)."""

    def make(i: int) -> HashFn:
        key = f"{seed}:{i}".encode()

        def h(x: Hashable) -> int:
            d = hashlib.blake2b(repr(x).encode(), digest_size=8, key=key[:64]).digest()
            return int.from_bytes(d, "big")

        return h

    return [make(i) for i in range(k)]


def jaccard(a: Iterable[Hashable], b: Iterable[Hashable]) -> float:
    """The exact Jaccard similarity, with J(empty, empty) = 1."""
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)
