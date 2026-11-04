# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extendible-hashing/. The authors are listed in prov/X591T6.jsonl.

from collections.abc import Callable, Hashable, Iterator
from typing import Any

W = 64  # default number of bits of a hash value


def hash64(k: Hashable) -> int:
    """The built-in hash, as a non-negative 64-bit value."""
    return hash(k) % (1 << W)


class Bucket:
    """A bucket: a list of [key, value] pairs and a local depth."""

    def __init__(self, depth: int) -> None:
        self.depth = depth
        self.pairs: list[list[Any]] = []


class ExtendibleHashing:
    """A dictionary stored by extendible hashing.

    A directory of 2**d pointers sends key k to the bucket dir[h(k) mod 2**d].
    Each bucket holds at most b pairs (more only when its local depth is W).
    A full bucket splits on one more bit; the directory doubles only when the
    bucket's local depth equals d. Search and delete cost O(b). An insert costs
    O(b + 2**d) in the worst case (W is a constant).
    """

    def __init__(self, b: int = 4, h: Callable[[Hashable], int] = hash64, w: int = W) -> None:
        if b < 1:
            raise ValueError("the bucket capacity must be at least 1")
        self.b = b
        self.w = w
        self.h = lambda k: h(k) % (1 << w)
        self.d = 0
        self.dir: list[Bucket] = [Bucket(0)]
        self.n = 0

    def _find(self, bucket: Bucket, k: Hashable) -> int:
        for p, pair in enumerate(bucket.pairs):
            if pair[0] == k:
                return p
        return -1

    def search(self, k: Hashable) -> Any:
        """Return the value of k, or None if k is not a key."""
        bucket = self.dir[self.h(k) % (1 << self.d)]  # @line L1
        p = self._find(bucket, k)
        if p >= 0:  # @line L2
            return bucket.pairs[p][1]
        return None  # @line L3

    def insert(self, k: Hashable, v: Any) -> None:
        """Set the value of k to v."""
        hk = self.h(k)
        bucket = self.dir[hk % (1 << self.d)]  # @line L4
        p = self._find(bucket, k)
        if p >= 0:  # @line L5
            bucket.pairs[p][1] = v
            return
        while len(bucket.pairs) >= self.b and bucket.depth < self.w:  # @line L6
            if bucket.depth == self.d:  # @line L7
                self.dir = self.dir + self.dir
                self.d += 1
            bucket.depth += 1  # @line L8
            new = Bucket(bucket.depth)
            bit = bucket.depth - 1
            keep = [q for q in bucket.pairs if not (self.h(q[0]) >> bit) & 1]  # @line L9
            new.pairs = [q for q in bucket.pairs if (self.h(q[0]) >> bit) & 1]
            bucket.pairs = keep
            for i in range(len(self.dir)):  # @line L10
                if self.dir[i] is bucket and (i >> bit) & 1:
                    self.dir[i] = new
            bucket = self.dir[hk % (1 << self.d)]  # @line L11
        bucket.pairs.append([k, v])  # @line L12
        self.n += 1

    def delete(self, k: Hashable) -> bool:
        """Remove k. Return True if k was a key. Buckets are not merged."""
        bucket = self.dir[self.h(k) % (1 << self.d)]  # @line L13
        p = self._find(bucket, k)
        if p >= 0:  # @line L14
            bucket.pairs.pop(p)
            self.n -= 1
            return True
        return False

    def __len__(self) -> int:
        return self.n

    def buckets(self) -> list[Bucket]:
        """The distinct buckets, in order of their first directory entry."""
        seen: dict[int, Bucket] = {}
        for bucket in self.dir:
            seen.setdefault(id(bucket), bucket)
        return list(seen.values())

    def items(self) -> Iterator[tuple[Any, Any]]:
        for bucket in self.buckets():
            for k, v in bucket.pairs:
                yield k, v

    def check_invariant(self) -> None:
        """Assert (E1) to (E5) of the page."""
        assert len(self.dir) == 1 << self.d
        keys = []
        where: dict[int, list[int]] = {}
        for i, x in enumerate(self.dir):
            where.setdefault(id(x), []).append(i)
        for bucket in self.buckets():
            ell = bucket.depth
            assert 0 <= ell <= self.d
            idx = where[id(bucket)]
            pat = idx[0] % (1 << ell)
            assert idx == list(range(pat, len(self.dir), 1 << ell))  # (E1)
            for k, _ in bucket.pairs:
                assert self.h(k) % (1 << ell) == pat  # (E2)
                keys.append(k)
            assert len(bucket.pairs) <= self.b or ell == self.w  # (E5)
        assert len(keys) == len(set(keys))  # (E3)
        assert self.n == len(keys)  # (E4)
