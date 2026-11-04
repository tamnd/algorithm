# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roaring-bitmap/. The authors are listed in prov/SA2AHY.jsonl.

from bisect import bisect_left, insort

ARRAY_MAX = 4096  # an array container holds at most this many values
WORDS = 1024  # a bitmap container is 1024 words of 64 bits = 2**16 bits
MASK64 = (1 << 64) - 1


class ArrayContainer:
    """A sorted list of distinct 16-bit values, at most ARRAY_MAX of them."""

    def __init__(self, values: list[int] | None = None) -> None:
        self.values = values if values is not None else []

    def cardinality(self) -> int:
        return len(self.values)

    def contains(self, low: int) -> bool:
        i = bisect_left(self.values, low)
        return i < len(self.values) and self.values[i] == low

    def members(self) -> list[int]:
        return list(self.values)


class BitmapContainer:
    """2**16 bits in 1024 words of 64 bits, with a cached count of ones."""

    def __init__(self) -> None:
        self.words = [0] * WORDS
        self.card = 0

    def cardinality(self) -> int:
        return self.card

    def contains(self, low: int) -> bool:
        return (self.words[low >> 6] >> (low & 63)) & 1 == 1

    def members(self) -> list[int]:
        out = []
        for j, word in enumerate(self.words):
            while word:
                t = word & -word
                out.append((j << 6) | (t.bit_length() - 1))
                word ^= t
        return out


Container = ArrayContainer | BitmapContainer


def to_bitmap(values: list[int]) -> BitmapContainer:
    b = BitmapContainer()
    for v in values:
        b.words[v >> 6] |= 1 << (v & 63)
    b.card = len(values)
    return b


def from_words(words: list[int]) -> Container | None:
    """Build the right container from 1024 words; None if all are zero."""
    card = sum(word.bit_count() for word in words)
    if card == 0:
        return None
    if card <= ARRAY_MAX:
        b = BitmapContainer()
        b.words = words
        return ArrayContainer(b.members())
    b = BitmapContainer()
    b.words = words
    b.card = card
    return b


class RoaringBitmap:
    """A set of 32-bit unsigned integers in the Roaring layout.

    Each value x is split into a key x >> 16 and a low part x & 0xFFFF. The
    keys are kept in a sorted list; each key has a container for its low
    parts: an array container when it holds at most 4096 values, otherwise
    a bitmap container. Empty containers are removed.
    """

    def __init__(self) -> None:
        self.keys: list[int] = []
        self.containers: list[Container] = []

    def _find(self, high: int) -> int:
        i = bisect_left(self.keys, high)
        if i < len(self.keys) and self.keys[i] == high:
            return i
        return -1

    def add(self, x: int) -> None:
        """Insert x, 0 <= x < 2**32. Cost O(log k + 4096) for k containers."""
        if not 0 <= x < (1 << 32):
            raise ValueError("x must be a 32-bit unsigned integer")
        high, low = x >> 16, x & 0xFFFF  # @line L1
        i = bisect_left(self.keys, high)  # @line L2
        if i == len(self.keys) or self.keys[i] != high:
            self.keys.insert(i, high)
            self.containers.insert(i, ArrayContainer())
        c = self.containers[i]  # @line L3
        if isinstance(c, ArrayContainer):  # @line L4
            if not c.contains(low):  # @line L5
                insort(c.values, low)
            if len(c.values) > ARRAY_MAX:  # @line L6
                self.containers[i] = to_bitmap(c.values)
        else:
            bit = 1 << (low & 63)  # @line L7
            if not c.words[low >> 6] & bit:
                c.words[low >> 6] |= bit
                c.card += 1

    def contains(self, x: int) -> bool:
        """Return True if x is a member. Cost O(log k + log 4096)."""
        if not 0 <= x < (1 << 32):
            return False
        i = self._find(x >> 16)  # @line L8
        if i < 0:
            return False
        return self.containers[i].contains(x & 0xFFFF)  # @line L9

    def remove(self, x: int) -> None:
        """Delete x if present. Cost O(log k + 4096)."""
        if not 0 <= x < (1 << 32):
            return
        high, low = x >> 16, x & 0xFFFF
        i = self._find(high)  # @line L10
        if i < 0:
            return
        c = self.containers[i]
        if isinstance(c, ArrayContainer):  # @line L11
            j = bisect_left(c.values, low)
            if j < len(c.values) and c.values[j] == low:
                c.values.pop(j)
        else:
            bit = 1 << (low & 63)
            if c.words[low >> 6] & bit:
                c.words[low >> 6] ^= bit
                c.card -= 1
            if c.card <= ARRAY_MAX:  # @line L12
                self.containers[i] = ArrayContainer(c.members())
        if self.containers[i].cardinality() == 0:  # @line L13
            self.keys.pop(i)
            self.containers.pop(i)

    def cardinality(self) -> int:
        """Return the number of members. Cost O(k)."""
        return sum(c.cardinality() for c in self.containers)

    def __iter__(self):
        for high, c in zip(self.keys, self.containers):
            for low in c.members():
                yield (high << 16) | low

    def to_list(self) -> list[int]:
        return list(self)

    @staticmethod
    def _combine(a: Container, b: Container, op: str) -> Container | None:
        if isinstance(a, ArrayContainer) and isinstance(b, ArrayContainer):
            if op == "and":
                out, i, j = [], 0, 0
                av, bv = a.values, b.values
                while i < len(av) and j < len(bv):
                    if av[i] < bv[j]:
                        i += 1
                    elif av[i] > bv[j]:
                        j += 1
                    else:
                        out.append(av[i])
                        i += 1
                        j += 1
                return ArrayContainer(out) if out else None
            out, i, j = [], 0, 0
            av, bv = a.values, b.values
            while i < len(av) or j < len(bv):
                if j == len(bv) or (i < len(av) and av[i] < bv[j]):
                    out.append(av[i])
                    i += 1
                elif i == len(av) or bv[j] < av[i]:
                    out.append(bv[j])
                    j += 1
                else:
                    out.append(av[i])
                    i += 1
                    j += 1
            if len(out) > ARRAY_MAX:
                return to_bitmap(out)
            return ArrayContainer(out)
        if op == "and" and isinstance(a, ArrayContainer) != isinstance(b, ArrayContainer):
            arr, bm = (a, b) if isinstance(a, ArrayContainer) else (b, a)
            out = [v for v in arr.values if bm.contains(v)]
            return ArrayContainer(out) if out else None
        wa = a.words if isinstance(a, BitmapContainer) else to_bitmap(a.values).words
        wb = b.words if isinstance(b, BitmapContainer) else to_bitmap(b.values).words
        if op == "and":
            words = [p & q for p, q in zip(wa, wb)]
        else:
            words = [p | q for p, q in zip(wa, wb)]
        return from_words(words)

    def _merge(self, other: "RoaringBitmap", op: str) -> "RoaringBitmap":
        res = RoaringBitmap()
        i = j = 0
        while i < len(self.keys) and j < len(other.keys):
            ki, kj = self.keys[i], other.keys[j]
            if ki < kj:
                if op == "or":
                    res.keys.append(ki)
                    res.containers.append(_copy(self.containers[i]))
                i += 1
            elif kj < ki:
                if op == "or":
                    res.keys.append(kj)
                    res.containers.append(_copy(other.containers[j]))
                j += 1
            else:
                c = self._combine(self.containers[i], other.containers[j], op)
                if c is not None:
                    res.keys.append(ki)
                    res.containers.append(c)
                i += 1
                j += 1
        if op == "or":
            for k in range(i, len(self.keys)):
                res.keys.append(self.keys[k])
                res.containers.append(_copy(self.containers[k]))
            for k in range(j, len(other.keys)):
                res.keys.append(other.keys[k])
                res.containers.append(_copy(other.containers[k]))
        return res

    def union(self, other: "RoaringBitmap") -> "RoaringBitmap":
        """Return a new bitmap with the members of either. Cost O(k + k') container merges."""
        return self._merge(other, "or")

    def intersection(self, other: "RoaringBitmap") -> "RoaringBitmap":
        """Return a new bitmap with the members of both."""
        return self._merge(other, "and")

    def check_invariant(self) -> None:
        """Raise AssertionError if the representation is not valid."""
        assert len(self.keys) == len(self.containers)
        assert all(0 <= k < (1 << 16) for k in self.keys)
        assert all(a < b for a, b in zip(self.keys, self.keys[1:]))
        for c in self.containers:
            if isinstance(c, ArrayContainer):
                assert 1 <= len(c.values) <= ARRAY_MAX
                assert all(0 <= v < (1 << 16) for v in c.values)
                assert all(a < b for a, b in zip(c.values, c.values[1:]))
            else:
                assert isinstance(c, BitmapContainer)
                assert len(c.words) == WORDS
                assert all(0 <= word <= MASK64 for word in c.words)
                assert c.card == sum(word.bit_count() for word in c.words)
                assert c.card > ARRAY_MAX


def _copy(c: Container) -> Container:
    if isinstance(c, ArrayContainer):
        return ArrayContainer(list(c.values))
    b = BitmapContainer()
    b.words = list(c.words)
    b.card = c.card
    return b
