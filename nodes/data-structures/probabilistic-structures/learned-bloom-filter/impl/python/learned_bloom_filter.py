# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learned-bloom-filter/. The authors are listed in prov/MC3EJT.jsonl.

"""Learned Bloom filter (Kraska et al. 2018) with the sandwich of Mitzenmacher (2018)."""

import hashlib
from collections.abc import Callable, Iterable

Key = str | bytes | int


class LearnedBloomFilter:
    """A classifier score(x) with threshold tau, a backup Bloom filter for the keys
    that the classifier rejects, and an optional initial Bloom filter of all keys.

    query(x) is True for each stored key. For non-keys drawn from a query
    distribution D, it is True with probability eps0 * (Fp + (1 - Fp) * eps_b),
    where Fp is the fraction of D that the classifier accepts and eps0 = 1 if
    there is no initial filter.
    """

    def __init__(
        self,
        keys: Iterable[Key],
        score: Callable[[Key], float],
        tau: float,
        m_b: int,
        k_b: int,
        m_0: int = 0,
        k_0: int = 0,
        seed: int = 0,
    ) -> None:
        if m_b < 1 or k_b < 1 or m_0 < 0 or (m_0 > 0 and k_0 < 1):
            raise ValueError("need m_b, k_b >= 1, and k_0 >= 1 when m_0 > 0")
        self.score, self.tau, self.seed = score, tau, seed
        self.sizes = {0: (m_0, k_0), 1: (m_b, k_b)}
        ks = list(keys)
        self.pre = bytearray(m_0)
        for x in ks if m_0 else []:  # @line L1: the initial filter holds every key
            for p in self._positions(x, 0):
                self.pre[p] = 1
        self.negatives = [x for x in ks if score(x) < tau]  # @line L2
        self.backup = bytearray(m_b)
        for x in self.negatives:  # @line L3: the backup filter holds the false negatives
            for p in self._positions(x, 1):
                self.backup[p] = 1

    def _positions(self, key: Key, which: int) -> list[int]:
        """The k positions of key in filter which (0 initial, 1 backup)."""
        m, k = self.sizes[which]
        out: list[int] = []
        t = 0
        while len(out) < k:
            d = hashlib.blake2b(
                repr(key).encode(),
                key=self.seed.to_bytes(8, "little"),
                salt=(which << 32 | t).to_bytes(16, "little"),
            ).digest()
            out.extend(int.from_bytes(d[w : w + 8], "little") % m for w in range(0, 64, 8))
            t += 1
        return out[:k]

    def query(self, key: Key) -> bool:
        """False if key is surely not stored; True if it may be."""
        if self.sizes[0][0] and not all(self.pre[p] for p in self._positions(key, 0)):  # @line L4
            return False
        if self.score(key) >= self.tau:  # @line L5
            return True
        return all(self.backup[p] for p in self._positions(key, 1))  # @line L6
