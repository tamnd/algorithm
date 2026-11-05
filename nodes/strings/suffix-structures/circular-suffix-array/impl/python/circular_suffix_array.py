# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-suffix-array/. The authors are listed in prov/DE34MK.jsonl.

from collections.abc import Sequence


def _counting_sort(items: list[int], key: list[int], buckets: int) -> list[int]:
    """Stable sort of items by key[item], with 0 <= key[item] < buckets."""
    count = [0] * (buckets + 1)
    for x in items:
        count[key[x] + 1] += 1
    for b in range(buckets):
        count[b + 1] += count[b]
    out = [0] * len(items)
    for x in items:
        out[count[key[x]]] = x
        count[key[x]] += 1
    return out


def cyclic_sort(text: Sequence) -> tuple[list[int], list[int]]:
    """Return (ca, cls): the circular suffix array of text and the final classes.

    ca lists the start positions 0 .. n-1 of the n rotations of text in
    increasing lexicographic order; equal rotations are ordered by position.
    cls[i] is the rank of rotation i among the distinct rotations. No sentinel
    is added and positions are 0-based. Symbols need a total order; they are
    mapped to 0 .. sigma - 1 first. Time O(n log n) after that mapping.
    """
    n = len(text)
    if n == 0:  # @line L1
        return [], []
    code = {c: r for r, c in enumerate(sorted(set(text)))}
    cls = [code[c] for c in text]
    p = _counting_sort(list(range(n)), cls, len(code))  # @line L2
    length = 1  # @line L3
    while length < n:  # @line L4
        pn = [(x - length) % n for x in p]  # @line L5
        p = _counting_sort(pn, cls, n)  # @line L6
        new = [0] * n  # @line L7
        for r in range(1, n):
            a, b = p[r - 1], p[r]
            same = cls[a] == cls[b] and cls[(a + length) % n] == cls[(b + length) % n]
            new[b] = new[a] + (0 if same else 1)
        cls = new
        length *= 2  # @line L8
    ca = _counting_sort(list(range(n)), cls, n)  # @line L9
    return ca, cls


class CircularSuffixArray:
    """The sorted array of the rotations of a text, with its BWT and rotation search."""

    def __init__(self, text: Sequence) -> None:
        self.text = text
        self.n = len(text)
        self.ca, self.cls = cyclic_sort(text)

    def rotation(self, r: int) -> list:
        """Return the rotation of rank r as a list of symbols."""
        i = self.ca[r]
        return list(self.text[i:]) + list(self.text[:i])

    def bwt(self) -> tuple[list, int]:
        """Return the last column L and the rank of rotation 0 (the primary index)."""
        last = [self.text[(i - 1) % self.n] for i in self.ca]
        primary = self.ca.index(0) if self.n else -1
        return last, primary

    def least_rotation(self) -> int:
        """Return the smallest position whose rotation is lexicographically least."""
        return self.ca[0] if self.n else -1

    def _compare(self, i: int, pattern: Sequence) -> int:
        """Compare the first len(pattern) symbols of rotation i with pattern: -1, 0 or 1."""
        for k, c in enumerate(pattern):
            d = self.text[(i + k) % self.n]
            if d != c:
                return -1 if d < c else 1
        return 0

    def find(self, pattern: Sequence) -> list[int]:
        """Return the sorted positions i whose rotation starts with pattern (len(pattern) <= n)."""
        if self.n == 0 or len(pattern) > self.n:
            return []
        lo, hi = 0, self.n
        while lo < hi:
            mid = (lo + hi) // 2
            if self._compare(self.ca[mid], pattern) < 0:
                lo = mid + 1
            else:
                hi = mid
        start, hi = lo, self.n
        while lo < hi:
            mid = (lo + hi) // 2
            if self._compare(self.ca[mid], pattern) <= 0:
                lo = mid + 1
            else:
                hi = mid
        return sorted(self.ca[start:lo])

    def check_invariant(self) -> None:
        for r in range(1, self.n):
            a, b = self.rotation(r - 1), self.rotation(r)
            assert a < b or (a == b and self.ca[r - 1] < self.ca[r])
