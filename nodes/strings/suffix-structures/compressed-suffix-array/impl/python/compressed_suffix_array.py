# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compressed-suffix-array/. The authors are listed in prov/M2B1RW.jsonl.

from collections.abc import Hashable, Sequence


def _suffix_array(t: list[int]) -> list[int]:
    """Suffix array by prefix doubling with library sorts; t ends with a unique smallest code."""
    n = len(t)
    sa, rank, h = list(range(n)), t[:], 1
    while n > 1:
        key = [(rank[i], rank[i + h] if i + h < n else -1) for i in range(n)]
        sa.sort(key=key.__getitem__)
        new = [0] * n
        for r in range(1, n):
            new[sa[r]] = new[sa[r - 1]] + (key[sa[r]] != key[sa[r - 1]])
        rank = new
        if rank[sa[-1]] == n - 1:
            break
        h *= 2
    return sa


class _GammaStream:
    """Positive integers written with the Elias gamma code into one growing integer."""

    def __init__(self) -> None:
        self.bits, self.length = 0, 0

    def write(self, x: int) -> None:
        """Write k - 1 zeros, then the k binary digits of x from the highest one, which is 1."""
        k = x.bit_length()
        self.length += k - 1
        rev = int(format(x, "b")[::-1], 2)  # the stream is read from the low end
        self.bits |= rev << self.length
        self.length += k

    def read(self, pos: int) -> tuple[int, int]:
        """The value that starts at pos and the position after it."""
        zeros = 0
        while not self.bits >> (pos + zeros) & 1:
            zeros += 1
        pos += zeros
        chunk = (self.bits >> pos) & ((1 << (zeros + 1)) - 1)
        return int(format(chunk, "0%db" % (zeros + 1))[::-1], 2), pos + zeros + 1


class CompressedSuffixArray:
    """Sadakane-style compressed suffix array of a text with a sentinel appended.

    The symbols need a total order and are coded 1 .. sigma, and the sentinel is
    the code 0, unique and smallest; rows are 0 .. n and positions 0-based. The
    index keeps Psi(i) = ISA[SA[i] + 1] (cyclic) as the increasing sequence
    F(i) * (n + 1) + Psi(i), with a sample every `block` rows and gamma-coded gaps,
    plus SA at the positions that are multiples of `step` (and n), and ISA there.
    It does not keep the text.
    """

    def __init__(self, text: Sequence[Hashable], step: int = 4, block: int = 8) -> None:
        self.n = n = len(text)
        self.step, self.block = step, block
        self.symbols = sorted(set(text))
        code = {c: r + 1 for r, c in enumerate(self.symbols)}
        t = [code[c] for c in text] + [0]
        sa = _suffix_array(t)
        isa = [0] * (n + 1)
        for i, p in enumerate(sa):
            isa[p] = i
        self.samples: list[tuple[int, int]] = []  # (value, offset in the stream) at every block-th row
        self.stream = _GammaStream()
        prev = 0
        for i, p in enumerate(sa):
            value = t[p] * (n + 1) + isa[(p + 1) % (n + 1)]
            if i % block == 0:
                self.samples.append((value, self.stream.length))
            else:
                self.stream.write(value - prev)
            prev = value
        self.sa_sample = {i: p for i, p in enumerate(sa) if p % step == 0 or p == n}
        self.isa_sample = [isa[p] for p in range(0, n + 1, step)]

    def _value(self, i: int) -> int:
        value, pos = self.samples[i // self.block]
        for _ in range(i % self.block):
            gap, pos = self.stream.read(pos)
            value += gap
        return value

    def psi(self, i: int) -> int:
        """Row of the suffix that starts one position after the suffix of row i."""
        return self._value(i) % (self.n + 1)

    def first(self, i: int) -> int:
        """Code of the first symbol of the suffix of row i (0 for the sentinel)."""
        return self._value(i) // (self.n + 1)

    def lookup(self, i: int) -> int:
        """SA[i], by walking Psi to a sampled row."""
        t = 0  # @line L1
        while i not in self.sa_sample:  # @line L2
            i = self.psi(i)  # @line L3
            t += 1
        return self.sa_sample[i] - t  # @line L4

    def inverse(self, p: int) -> int:
        """ISA[p], from the sample at or before p."""
        i = self.isa_sample[p // self.step]
        for _ in range(p % self.step):
            i = self.psi(i)
        return i

    def extract(self, left: int, right: int) -> list[Hashable]:
        """The text symbols at positions left .. right - 1."""
        if not 0 <= left <= right <= self.n:
            raise ValueError("bad range")
        i, out = self.inverse(left), []
        for _ in range(right - left):
            out.append(self.symbols[self.first(i) - 1])
            i = self.psi(i)
        return out

    def _compare(self, i: int, pattern: list[int]) -> int:
        """Sign of (prefix of the suffix of row i) minus pattern, over len(pattern) symbols."""
        for x in pattern:  # @line L5
            y = self.first(i)
            if y != x:
                return -1 if y < x else 1  # @line L6
            i = self.psi(i)  # @line L7
        return 0

    def find(self, pattern: Sequence[Hashable]) -> tuple[int, int]:
        """Rows [lo, hi) of the suffixes that start with pattern, by binary search."""
        code = {c: r + 1 for r, c in enumerate(self.symbols)}
        if any(c not in code for c in pattern):
            return (0, 0)
        p = [code[c] for c in pattern]
        lo, hi = 0, self.n + 1
        while lo < hi:  # @line L8
            mid = (lo + hi) // 2
            if self._compare(mid, p) < 0:
                lo = mid + 1
            else:
                hi = mid
        start, hi = lo, self.n + 1
        while lo < hi:  # @line L9
            mid = (lo + hi) // 2
            if self._compare(mid, p) <= 0:
                lo = mid + 1
            else:
                hi = mid
        return (start, lo)  # @line L10

    def locate(self, pattern: Sequence[Hashable]) -> list[int]:
        """Sorted start positions of a nonempty pattern."""
        if len(pattern) == 0:
            raise ValueError("the pattern must be nonempty")
        lo, hi = self.find(pattern)
        return sorted(self.lookup(i) for i in range(lo, hi))

    def psi_stream_length(self) -> int:
        """Number of binary digits used by the gamma-coded gaps of Psi."""
        return self.stream.length
