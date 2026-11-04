# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-set/. The authors are listed in prov/C0Q5CB.jsonl.


class BitSet:
    """A set of integers from {0, ..., n - 1} stored as an array of w-bit words.

    Element i is bit (i mod w) of word i // w. Bits at positions n and above
    in the last word are always 0. insert, delete and contains cost O(1);
    count, complement and union cost O(n / w) word operations; next_member
    costs O(n / w) in the worst case. Space: ceil(n / w) words.
    """

    def __init__(self, n: int = 0, w: int = 64) -> None:
        if n < 0 or w < 1:
            raise ValueError("need n >= 0 and w >= 1")
        self.n = n
        self.w = w
        self._mask = (1 << w) - 1
        self.words = [0] * ((n + w - 1) // w)  # @line L1

    def _check_index(self, i: int) -> None:
        if not 0 <= i < self.n:
            raise IndexError("element out of the universe")

    def insert(self, i: int) -> None:
        """Add i to the set. Precondition: 0 <= i < n. Cost O(1)."""
        self._check_index(i)
        self.words[i // self.w] |= 1 << (i % self.w)  # @line L2

    def delete(self, i: int) -> None:
        """Remove i from the set if present. Precondition: 0 <= i < n. Cost O(1)."""
        self._check_index(i)
        self.words[i // self.w] &= ~(1 << (i % self.w)) & self._mask  # @line L3

    def contains(self, i: int) -> bool:
        """Return True if i is in the set. Precondition: 0 <= i < n. Cost O(1)."""
        self._check_index(i)
        return (self.words[i // self.w] >> (i % self.w)) & 1 == 1  # @line L4

    def count(self) -> int:
        """Return the number of members. Cost O(n / w) popcounts."""
        c = 0
        for word in self.words:
            c += word.bit_count()
        return c

    def next_member(self, i: int) -> int | None:
        """Return the least member >= i, or None. Precondition: i >= 0. Cost O(n / w)."""
        j = i // self.w
        if j >= len(self.words):
            return None
        x = self.words[j] & ~((1 << (i % self.w)) - 1) & self._mask
        while x == 0:
            j += 1
            if j == len(self.words):
                return None
            x = self.words[j]
        return j * self.w + ((x & -x).bit_length() - 1)

    def complement(self) -> None:
        """Replace the set by its complement in {0, ..., n - 1}. Cost O(n / w)."""
        for j in range(len(self.words)):
            self.words[j] = ~self.words[j] & self._mask
        r = self.n % self.w
        if r != 0:
            self.words[-1] &= (1 << r) - 1

    def union(self, other: "BitSet") -> None:
        """Add every member of other, a set over the same n and w. Cost O(n / w)."""
        if other.n != self.n or other.w != self.w:
            raise ValueError("universes differ")
        for j in range(len(self.words)):
            self.words[j] |= other.words[j]

    def members(self) -> list[int]:
        """Return the members in increasing order. Cost O(n / w + size)."""
        out = []
        for j, word in enumerate(self.words):
            while word:
                b = word & -word
                out.append(j * self.w + b.bit_length() - 1)
                word ^= b
        return out

    def check_invariant(self) -> None:
        """Assert the representation invariant: the right number of words,
        each a w-bit word, and no bit at a position >= n."""
        assert len(self.words) == (self.n + self.w - 1) // self.w
        for word in self.words:
            assert 0 <= word <= self._mask
        r = self.n % self.w
        if r != 0 and self.words:
            assert self.words[-1] >> r == 0
