# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maglev-hashing/. The authors are listed in prov/DA1P19.jsonl.

"""Maglev hashing: the lookup table of Eisenbud et al. (NSDI 2016).

Each backend has a preference list, a permutation of the M table slots given
by offset + j * skip (mod M). The backends take turns; each one takes the
next slot of its list that is still empty, until the table is full. A key
goes to the backend in slot h(key) mod M.

The paper does not fix h1 and h2. Here they are BLAKE2b with two different
personalization strings, which keeps the results the same on every run.
"""

import hashlib
from collections.abc import Sequence


def _h(data: str, person: bytes) -> int:
    d = hashlib.blake2b(data.encode(), digest_size=8, person=person).digest()
    return int.from_bytes(d, "big")


def offset_skip(name: str, m: int) -> tuple[int, int]:
    """The pair (offset, skip) of a backend for a table of prime size m."""
    offset = _h(name, b"maglev-offset") % m
    skip = _h(name, b"maglev-skip") % (m - 1) + 1
    return offset, skip


def permutations(pairs: Sequence[tuple[int, int]], m: int) -> list[list[int]]:
    """The full preference lists, for small tables and for tests."""
    return [[(o + j * s) % m for j in range(m)] for o, s in pairs]


def populate(pairs: Sequence[tuple[int, int]], m: int) -> list[int]:
    """Fill a table of size m from the (offset, skip) pairs; Pseudocode 1 of the paper.

    Entry c of the result is the index of the backend that owns slot c. The
    slot j of the list of backend i is computed on the fly as
    (offset_i + j * skip_i) mod m, so the lists are never stored.
    """
    n = len(pairs)
    if n == 0:
        raise ValueError("at least one backend is needed")
    nxt = [0] * n  # @line L1
    entry = [-1] * m  # @line L2
    filled = 0  # @line L3
    while True:  # @line L4
        for i in range(n):  # @line L5
            o, s = pairs[i]
            c = (o + nxt[i] * s) % m  # @line L6
            while entry[c] >= 0:  # @line L7
                nxt[i] += 1  # @line L8
                c = (o + nxt[i] * s) % m
            entry[c] = i  # @line L9
            nxt[i] += 1  # @line L10
            filled += 1
            if filled == m:  # @line L11
                return entry


class Maglev:
    """A Maglev table over named backends."""

    def __init__(self, backends: Sequence[str], m: int = 65537) -> None:
        self.backends = list(backends)
        self.m = m
        self.table = populate([offset_skip(b, m) for b in self.backends], m)

    def lookup(self, key: str) -> str:
        return self.backends[self.table[_h(key, b"maglev-key") % self.m]]  # @line L12

    def owners(self) -> list[str]:
        """The table as backend names, one per slot."""
        return [self.backends[i] for i in self.table]


def changed_fraction(before: Sequence[str], after: Sequence[str]) -> float:
    """The fraction of slots whose backend differs between two tables."""
    return sum(a != b for a, b in zip(before, after)) / len(before)
