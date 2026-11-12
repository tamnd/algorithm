# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-bitmap/. The authors are listed in prov/FD46E0.jsonl.

"""Tree bitmap (Eatherton, Varghese and Dittia, 2004).

A multibit trie of stride s. Each node holds
  - an internal bitmap of 2**s - 1 bits, one for each prefix of length
    0 to s - 1 inside the node: the prefix of length j and value v has
    bit index 2**j - 1 + v;
  - an external bitmap of 2**s bits, one for each possible child;
  - one contiguous array of children, in the order of the external bits;
  - one contiguous array of results (next hops), in the order of the
    internal bits.
The position of an entry in an array is the number of 1 bits before its bit
(a popcount). A prefix (p, l) lives in the node at depth l // s, as the
in-node prefix of length l % s.
"""

from typing import Optional


def rank(bitmap: int, i: int) -> int:
    """The number of 1 bits of bitmap below position i (a popcount)."""
    return (bitmap & ((1 << i) - 1)).bit_count()


class Node:
    __slots__ = ("internal", "external", "children", "results")

    def __init__(self) -> None:
        self.internal = 0
        self.external = 0
        self.children: list["Node"] = []
        self.results: list[object] = []


class TreeBitmap:
    def __init__(self, w: int, stride: int = 4) -> None:
        if not 1 <= stride <= w:
            raise ValueError("need 1 <= stride <= w")
        self.w, self.s = w, stride
        self.root = Node()

    # The s bits of addr that start at depth k, padded with zeros at the end.
    def _chunk(self, addr: int, k: int) -> int:
        start = k * self.s
        take = min(self.s, self.w - start)
        bits = (addr >> (self.w - start - take)) & ((1 << take) - 1)
        return bits << (self.s - take)

    def _path(self, p: int, l: int) -> tuple[list[int], int, int]:
        """The child indices down to the node of (p, l), and the in-node prefix."""
        s = self.s
        k, j = divmod(l, s)
        steps = [(p >> (l - (i + 1) * s)) & ((1 << s) - 1) for i in range(k)]
        return steps, j, p & ((1 << j) - 1)

    def insert(self, p: int, l: int, hop: object) -> None:
        steps, j, v = self._path(p, l)
        node = self.root
        for c in steps:
            r = rank(node.external, c)
            if not (node.external >> c) & 1:
                node.external |= 1 << c
                node.children.insert(r, Node())
            node = node.children[r]
        i = (1 << j) - 1 + v
        r = rank(node.internal, i)
        if (node.internal >> i) & 1:
            node.results[r] = hop
        else:
            node.internal |= 1 << i
            node.results.insert(r, hop)

    def delete(self, p: int, l: int) -> bool:
        steps, j, v = self._path(p, l)
        path = [self.root]
        node = self.root
        for c in steps:
            if not (node.external >> c) & 1:
                return False
            node = node.children[rank(node.external, c)]
            path.append(node)
        i = (1 << j) - 1 + v
        if not (node.internal >> i) & 1:
            return False
        node.results.pop(rank(node.internal, i))
        node.internal &= ~(1 << i)
        # Free the nodes that became empty, from the bottom up.
        for depth in range(len(steps), 0, -1):
            node = path[depth]
            if node.internal or node.external:
                break
            parent, c = path[depth - 1], steps[depth - 1]
            parent.children.pop(rank(parent.external, c))
            parent.external &= ~(1 << c)
        return True

    def lookup(self, addr: int) -> tuple[Optional[object], int]:
        """Return the next hop of the longest match and the memory reads."""
        s, w = self.s, self.w
        node, k = self.root, 0  # @line L1
        best: Optional[tuple[Node, int]] = None  # @line L2
        reads = 0
        while True:  # @line L3
            reads += 1  # one read of the node: both bitmaps and both pointers
            c = self._chunk(addr, k)  # @line L4
            for j in range(min(s - 1, w - k * s), -1, -1):  # @line L5
                i = (1 << j) - 1 + (c >> (s - j))
                if (node.internal >> i) & 1:  # @line L6
                    best = (node, rank(node.internal, i))  # @line L7
                    break
            if (k + 1) * s > w or not (node.external >> c) & 1:  # @line L8
                break
            node = node.children[rank(node.external, c)]  # @line L9
            k += 1
        if best is None:  # @line L10
            return None, reads
        reads += 1  # one read of the result array
        return best[0].results[best[1]], reads  # @line L11

    def prefixes(self) -> dict[tuple[int, int], object]:
        """Rebuild the prefix table from the bitmaps alone."""
        out: dict[tuple[int, int], object] = {}
        s = self.s
        stack = [(self.root, 0, 0)]  # node, depth, the bits of the path
        while stack:
            node, k, bits = stack.pop()
            r = 0
            for i in range((1 << s) - 1):
                if (node.internal >> i) & 1:
                    j = (i + 1).bit_length() - 1
                    v = i - ((1 << j) - 1)
                    out[((bits << j) | v, k * s + j)] = node.results[r]
                    r += 1
            r = 0
            for c in range(1 << s):
                if (node.external >> c) & 1:
                    stack.append((node.children[r], k + 1, (bits << s) | c))
                    r += 1
        return out

    def check_layout(self) -> int:
        """Check the array sizes against the bitmaps; return the node count."""
        count = 0
        stack = [(self.root, True)]
        full = 1 << ((1 << self.s) - 1)
        while stack:
            node, is_root = stack.pop()
            count += 1
            assert 0 <= node.internal < full
            assert 0 <= node.external < (1 << (1 << self.s))
            assert len(node.children) == node.external.bit_count()
            assert len(node.results) == node.internal.bit_count()
            assert is_root or node.internal or node.external, "an empty node was kept"
            stack.extend((c, False) for c in node.children)
        return count


def brute_force_lpm(table: dict[tuple[int, int], object], addr: int, w: int) -> Optional[object]:
    best, best_len = None, -1
    for (p, l), hop in table.items():
        if addr >> (w - l) == p and l > best_len:
            best, best_len = hop, l
    return best
