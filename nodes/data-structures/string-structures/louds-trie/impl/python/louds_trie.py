# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/louds-trie/. The authors are listed in prov/C20ZQR.jsonl.

from bisect import bisect_left

BLOCK = 64


class BitVector:
    """A static bit vector with rank and select over block counts.

    rank1(i) is the number of 1 bits in B[0 .. i-1]; select1(j) and select0(j)
    are the positions of the j-th 1 and 0 bit, counting from 1.
    """

    def __init__(self, bits: list[int]) -> None:
        self.bits = bits
        self.cum = [0]
        for s in range(0, len(bits), BLOCK):
            self.cum.append(self.cum[-1] + sum(bits[s: s + BLOCK]))

    def __len__(self) -> int:
        return len(self.bits)

    def rank1(self, i: int) -> int:
        b = i // BLOCK
        return self.cum[b] + sum(self.bits[b * BLOCK: i])

    def rank0(self, i: int) -> int:
        return i - self.rank1(i)

    def _select(self, j: int, one: bool) -> int:
        def count(b: int) -> int:
            return self.cum[b] if one else b * BLOCK - self.cum[b]

        lo, hi = 0, len(self.cum) - 1  # the last block whose count before it is < j
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if count(mid) < j:
                lo = mid
            else:
                hi = mid - 1
        seen, want = count(lo), 1 if one else 0
        for p in range(lo * BLOCK, len(self.bits)):
            if self.bits[p] == want:
                seen += 1
                if seen == j:
                    return p
        raise IndexError("select out of range")

    def select1(self, j: int) -> int:
        return self._select(j, True)

    def select0(self, j: int) -> int:
        return self._select(j, False)


class LoudsTrie:
    """A static trie in LOUDS form: nodes are numbered 0, 1, ... in breadth-first order.

    B = 10 followed by 1^d 0 for each node of degree d, in breadth-first order.
    label[y] is the symbol on the edge into node y (label[0] is unused) and
    terminal[y] tells whether node y ends a key.
    """

    def __init__(self, keys: list[str]) -> None:
        children: list[dict[str, int]] = [{}]  # a pointer trie, used only to build
        ends = [False]
        for k in keys:
            x = 0
            for c in k:
                if c not in children[x]:
                    children[x][c] = len(children)
                    children.append({})
                    ends.append(False)
                x = children[x][c]
            ends[x] = True
        bits = [1, 0]
        self.label: list[str] = [""]
        self.terminal: list[bool] = []
        queue, head = [0], 0
        while head < len(queue):  # @line L7
            x = queue[head]
            head += 1
            self.terminal.append(ends[x])
            for c in sorted(children[x]):
                bits.append(1)
                self.label.append(c)
                queue.append(children[x][c])
            bits.append(0)
        self.b = BitVector(bits)
        self.n = len(queue)

    def children_range(self, x: int) -> tuple[int, int]:
        """The children of x are the nodes first .. last - 1."""
        a = self.b.select0(x + 1) + 1  # @line L1
        e = self.b.select0(x + 2)
        first = self.b.rank1(a)  # @line L2
        return first, first + (e - a)

    def child(self, x: int, c: str) -> int:
        """The child of x by symbol c, or -1."""
        first, last = self.children_range(x)
        y = bisect_left(self.label, c, first, last)  # @line L3
        return y if y < last and self.label[y] == c else -1

    def parent(self, x: int) -> int:
        p = self.b.select1(x + 1)  # @line L4
        return self.b.rank0(p) - 1

    def _walk(self, s: str) -> int:
        x = 0
        for c in s:  # @line L5
            x = self.child(x, c)
            if x < 0:
                return -1
        return x

    def contains(self, s: str) -> bool:
        x = self._walk(s)
        return x >= 0 and self.terminal[x]  # @line L6

    def string_of(self, x: int) -> str:
        out = []
        while x != 0:
            out.append(self.label[x])
            x = self.parent(x)
        return "".join(reversed(out))

    def keys_with_prefix(self, p: str) -> list[str]:
        x = self._walk(p)
        if x < 0:
            return []
        out: list[str] = []
        stack = [(x, p)]
        while stack:
            y, s = stack.pop()
            if self.terminal[y]:
                out.append(s)
            first, last = self.children_range(y)
            for z in range(last - 1, first - 1, -1):
                stack.append((z, s + self.label[z]))
        return out

    def check_invariant(self) -> None:
        bits = self.b.bits
        assert len(bits) == 2 * self.n + 1 and bits[:2] == [1, 0]
        assert sum(bits) == self.n and len(self.label) == self.n == len(self.terminal)
        for x in range(self.n):
            first, last = self.children_range(x)
            labels = self.label[first:last]
            assert labels == sorted(set(labels)), "distinct sorted labels"
            for y in range(first, last):
                assert self.parent(y) == x and y > x
        for x in range(1, self.n):
            first, last = self.children_range(x)
            assert self.terminal[x] or last > first, "every leaf ends a key"
