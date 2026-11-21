# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/privacy-preserving-record-linkage/. The authors are listed in prov/KHENH3.jsonl.
"""Privacy-preserving record linkage with Bloom filters, after Schnell, Bachteler and Reiher (2009).

Each data owner normalizes an identifier, splits it into q-grams padded with q - 1
copies of a pad character on each side, and sets k bits for each q-gram in a bit
vector of length m. Bit i of a q-gram g is (h1(g) + i * h2(g)) mod m, where h1 is
HMAC-SHA1 and h2 is HMAC-MD5 under two secret keys. A Bloom filter is a Python int
used as a bit vector. The linkage unit compares filters by the Dice coefficient
2 |a and b| / (|a| + |b|) and keeps the pairs at or above a threshold.

The keys must come from a cryptographic source of randomness and must stay secret
from the linkage unit. This encoding is known to leak information through the
frequencies of q-grams; see the page for the defenses.
"""

import hashlib
import hmac
from fractions import Fraction
from typing import Sequence


def normalize(s: str) -> str:
    """Lower case, with runs of white space replaced by one space and the ends trimmed."""
    return " ".join(s.lower().split())


def qgrams(s: str, q: int = 2, pad: str = "_") -> list[str]:
    """The distinct q-grams of s padded with q - 1 pad characters on each side, in order of first use.

    Precondition: q >= 1 and pad is one character. Cost: O(q len(s)).
    """
    if q < 1 or len(pad) != 1:
        raise ValueError("need q >= 1 and a pad of one character")
    t = pad * (q - 1) + s + pad * (q - 1)
    seen: dict[str, None] = {}
    for i in range(len(t) - q + 1):
        seen.setdefault(t[i : i + q], None)
    return list(seen)


def _h(key: bytes, g: str, algo: str) -> int:
    return int.from_bytes(hmac.new(key, g.encode("utf-8"), algo).digest(), "big")


def positions(g: str, key1: bytes, key2: bytes, k: int, m: int) -> list[int]:
    """The k bit positions of the q-gram g by double hashing with HMAC-SHA1 and HMAC-MD5."""
    a = _h(key1, g, "sha1")
    b = _h(key2, g, "md5")
    return [(a + i * b) % m for i in range(k)]


def encode(s: str, key1: bytes, key2: bytes, k: int, m: int, q: int = 2) -> int:
    """The Bloom filter of the identifier s, as an int with m bits.

    Precondition: k >= 1, m >= 1, q >= 1. Cost: O(len(s) (q + k)) HMAC calls and bit operations.
    """
    if k < 1 or m < 1:
        raise ValueError("need k >= 1 and m >= 1")
    grams = qgrams(normalize(s), q)  # @line L2
    f = 0  # @line L3
    for g in grams:  # @line L4
        for p in positions(g, key1, key2, k, m):
            f |= 1 << p  # @line L5
    return f


def dice(a: int, b: int) -> Fraction:
    """The Dice coefficient of two bit vectors, 0 if both are empty. Cost: O(m / w) word operations."""
    total = a.bit_count() + b.bit_count()
    if total == 0:
        return Fraction(0)
    return Fraction(2 * (a & b).bit_count(), total)


def link(
    left: Sequence[str],
    right: Sequence[str],
    key1: bytes,
    key2: bytes,
    k: int,
    m: int,
    theta: Fraction,
    q: int = 2,
) -> list[tuple[int, int, Fraction]]:
    """All pairs (i, j, s) with s = dice(encode(left[i]), encode(right[j])) >= theta, in order of i and j.

    In a real linkage, each data owner encodes its own records with the shared keys,
    and only the filters go to the linkage unit, which runs the comparison loop.
    Precondition: 0 <= theta <= 1. Cost: O((n + r) l (q + k)) for encoding n + r
    identifiers of length at most l, and O(n r m / w) for the comparisons.
    """
    fl = [encode(s, key1, key2, k, m, q) for s in left]  # @line L1
    fr = [encode(s, key1, key2, k, m, q) for s in right]
    matches: list[tuple[int, int, Fraction]] = []  # @line L6
    for i, a in enumerate(fl):  # @line L7
        for j, b in enumerate(fr):
            s = dice(a, b)  # @line L8
            if s >= theta:  # @line L9
                matches.append((i, j, s))
    return matches  # @line L10
