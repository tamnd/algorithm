# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fischer-heun-rmq/. The authors are listed in prov/6H7AGY.jsonl.

from typing import Sequence

W = 64  # bits per word


class FischerHeunRMQ:
    """Range minimum queries from the DFUDS of the 2d-Min-heap, without A.

    The array is encoded as 2n + 2 bits: the DFUDS sequence of its
    2d-Min-heap, in which the parent of position i is the nearest earlier
    position j with A[j] <= A[i], or a virtual root. Queries use rank,
    select, a leftmost range minimum on the excess, and findopen on these
    bits only. The directories here are simple: rank samples per word, a
    binary search for select, and a sparse table over word minima, so a
    query costs O(log n); the constant-time o(n)-bit directories of the
    paper are replaced by these for brevity.
    """

    def __init__(self, a: Sequence[int]) -> None:
        """Encode a; the array itself is not kept."""
        n = len(a)
        self.n = n
        # L1: parents in the 2d-Min-heap; 1-based positions, 0 is the root.
        deg = [0] * (n + 1)
        stack = [0]
        for i in range(1, n + 1):  # @line L1
            while stack[-1] != 0 and a[stack[-1] - 1] > a[i - 1]:
                stack.pop()
            deg[stack[-1]] += 1
            stack.append(i)
        # L2: DFUDS, a leading "(" and then "("^deg(v) ")" for v in preorder.
        bits = [1]
        for v in range(n + 1):  # @line L2
            bits.extend([1] * deg[v])
            bits.append(0)
        self.length = len(bits)
        self.words = [0] * ((self.length + W - 1) // W)
        for k, bit in enumerate(bits):
            if bit:
                self.words[k // W] |= 1 << (k % W)
        # L3: directories: ones before each word, and the minimum excess per word.
        self.ones_before = [0] * (len(self.words) + 1)
        for w, word in enumerate(self.words):  # @line L3
            self.ones_before[w + 1] = self.ones_before[w] + word.bit_count()
        self.block_min: list[tuple[int, int]] = []
        d = 0
        for w in range(len(self.words)):
            best = (1 << 62, 0)
            for p in range(w * W + 1, min(self.length, (w + 1) * W) + 1):
                d += 1 if self._bit(p) else -1
                if d < best[0]:
                    best = (d, p)
            self.block_min.append(best)
        self.sparse = [list(self.block_min)]
        h = 1
        while 2 * h <= len(self.block_min):
            prev = self.sparse[-1]
            self.sparse.append([min(prev[j], prev[j + h]) for j in range(len(prev) - h)])
            h *= 2

    def _bit(self, p: int) -> int:
        """Bit at 1-based position p: 1 for "(" and 0 for ")"."""
        return (self.words[(p - 1) // W] >> ((p - 1) % W)) & 1

    def _rank1(self, p: int) -> int:
        """Number of "(" among the first p bits."""
        w, r = divmod(p, W)
        if r == 0:
            return self.ones_before[w]
        return self.ones_before[w] + (self.words[w] & ((1 << r) - 1)).bit_count()

    def _rank0(self, p: int) -> int:
        return p - self._rank1(p)

    def _excess(self, p: int) -> int:
        """D[p], the number of "(" minus the number of ")" among the first p bits."""
        return 2 * self._rank1(p) - p

    def _select0(self, t: int) -> int:
        """1-based position of the t-th ")"."""
        lo, hi = 0, len(self.words) - 1
        while lo < hi:  # the last word with fewer than t zeros before it
            mid = (lo + hi + 1) // 2
            if mid * W - self.ones_before[mid] < t:
                lo = mid
            else:
                hi = mid - 1
        p = lo * W
        zeros = p - self.ones_before[lo]
        while zeros < t:
            p += 1
            if not self._bit(p):
                zeros += 1
        return p

    def _range_min(self, i: int, j: int) -> tuple[int, int]:
        """(value, position) of the leftmost minimum excess on words i..j."""
        k = (j - i + 1).bit_length() - 1
        return min(self.sparse[k][i], self.sparse[k][j - (1 << k) + 1])

    def _scan(self, x: int, y: int) -> tuple[int, int]:
        d = self._excess(x - 1)
        best = (1 << 62, 0)
        for p in range(x, y + 1):
            d += 1 if self._bit(p) else -1
            if d < best[0]:
                best = (d, p)
        return best

    def _rmq_excess(self, x: int, y: int) -> int:
        """Position of the leftmost minimum of D[x..y]."""
        bx, by = (x - 1) // W, (y - 1) // W
        if bx == by:
            return self._scan(x, y)[1]
        best = min(self._scan(x, (bx + 1) * W), self._scan(by * W + 1, y))
        if bx + 1 <= by - 1:
            best = min(best, self._range_min(bx + 1, by - 1))
        return best[1]

    def _open(self, w: int) -> int:
        """Position of the "(" that matches the ")" at w."""
        t = self._excess(w)
        d = t
        k = w - 1
        start = ((w - 1) // W) * W  # scan the bits of the word of w back to its start
        while k >= max(start, 1):
            d -= 1 if self._bit(k + 1) else -1
            if d == t:
                return k + 1
            k -= 1
        j = (w - 1) // W - 1  # the nearest earlier word whose minimum is at most t
        for h in range(len(self.sparse) - 1, -1, -1):
            if j - (1 << h) + 1 >= 0 and self.sparse[h][j - (1 << h) + 1][0] > t:
                j -= 1 << h
        d = self._excess((j + 1) * W)
        for k in range((j + 1) * W, j * W - 1, -1):
            if d == t and k < w:
                return k + 1
            d -= 1 if self._bit(k) else -1
        raise AssertionError("unbalanced sequence")

    def query(self, l: int, r: int) -> int:
        """Position of the leftmost minimum of a[l..r], 0 <= l <= r < n."""
        if not 0 <= l <= r < self.n:
            raise IndexError(f"bad range [{l}, {r}] for length {self.n}")
        i, j = l + 1, r + 1
        if i == j:  # @line L4
            return l
        x, y = self._select0(i + 1), self._select0(j)  # @line L5
        w = self._rmq_excess(x, y)  # @line L6
        if self._rank0(self._open(w)) == i:  # @line L7
            return l
        return self._rank0(w) - 1  # @line L8

    def bits(self) -> str:
        """The DFUDS sequence as a string of parentheses."""
        return "".join("(" if self._bit(p) else ")" for p in range(1, self.length + 1))

    def check_invariant(self) -> None:
        """The sequence is balanced, has 2n + 2 bits, and the directories agree."""
        assert self.length == 2 * self.n + 2
        d = 0
        for p in range(1, self.length + 1):
            d += 1 if self._bit(p) else -1
            assert d == self._excess(p)
            assert d > 0 or p == self.length
        assert d == 0
        for t in range(1, self.n + 2):
            p = self._select0(t)
            assert self._bit(p) == 0 and self._rank0(p) == t
