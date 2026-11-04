# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-bloom-filter/. The authors are listed in prov/MMBG5S.jsonl.

"""Spectral Bloom filter (Cohen and Matias 2003): minimum selection and minimal increase."""

import hashlib

Key = str | bytes | int


class SpectralBloomFilter:
    """m counters and k hash functions that estimate the multiplicity of a key.

    estimate(x) is never below the true multiplicity of x. With
    minimal_increase=False (minimum selection) the filter supports delete;
    with minimal_increase=True (minimal increase) the estimates are never
    larger, but delete is not allowed.
    """

    def __init__(self, m: int, k: int, minimal_increase: bool = False, seed: int = 0) -> None:
        if m < 1 or k < 1:
            raise ValueError("m and k must be positive")
        self.m = m
        self.k = k
        self.mi = minimal_increase
        self.seed = seed
        self.counters = [0] * m  # @line L1

    def _positions(self, key: Key) -> list[int]:
        """h_1(key), ..., h_k(key), from independent 64-bit words of BLAKE2b."""
        out: list[int] = []
        t = 0
        while len(out) < self.k:
            d = hashlib.blake2b(
                repr(key).encode(),
                key=self.seed.to_bytes(8, "little"),
                salt=t.to_bytes(16, "little"),
            ).digest()
            out.extend(int.from_bytes(d[w : w + 8], "little") % self.m for w in range(0, 64, 8))
            t += 1
        return out[: self.k]  # @line L2

    def _set(self, key: Key) -> list[int]:
        """The distinct positions of key, in a fixed order."""
        return sorted(set(self._positions(key)))

    def insert(self, key: Key, w: int = 1) -> None:
        """Add w copies of key."""
        if w < 0:
            raise ValueError("w must be nonnegative")
        ps = self._set(key)
        if not self.mi:
            for p in ps:  # @line L3
                self.counters[p] += w
            return
        v = min(self.counters[p] for p in ps)  # @line L4
        for p in ps:  # @line L5: raise only the counters below v + w
            self.counters[p] = max(self.counters[p], v + w)

    def delete(self, key: Key, w: int = 1) -> None:
        """Remove w copies of key. Precondition: at least w copies are present."""
        if self.mi:
            raise ValueError("minimal increase does not support delete")
        for p in self._set(key):  # @line L6
            self.counters[p] -= w

    def estimate(self, key: Key) -> int:
        """An upper bound on the multiplicity of key, exact with high probability."""
        return min(self.counters[p] for p in self._set(key))  # @line L7

    def query(self, key: Key, threshold: int = 1) -> bool:
        """True if key may have at least threshold copies; False means surely fewer."""
        return self.estimate(key) >= threshold
