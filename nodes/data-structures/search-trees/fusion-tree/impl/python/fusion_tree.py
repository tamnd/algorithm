# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fusion-tree/. The authors are listed in prov/SD1PX6.jsonl.
"""A static fusion tree for predecessor search on w-bit integers.

Each node holds at most B keys. A node keeps the distinguishing bit positions
of its keys, the exact sketches of the keys, and one packed word with all the
sketches, so that the rank of a sketch among the node's sketches is found with
one subtraction, one AND and one population count. This version computes the
exact sketch with a loop over the positions; the structure of Fredman and
Willard computes an approximate sketch with one multiplication instead.
"""

from bisect import bisect_right
from typing import List, Optional


def msb(x: int) -> int:
    """Position of the highest set bit of x > 0."""
    return x.bit_length() - 1


class FusionNode:
    __slots__ = ("keys", "children", "pos", "r", "width", "packed", "mult", "high")

    def __init__(self, keys: List[int]) -> None:
        self.keys = keys
        self.children: List[Optional["FusionNode"]] = [None] * (len(keys) + 1)
        d = {msb(a ^ b) for a, b in zip(keys, keys[1:])}
        self.pos = sorted(d, reverse=True)  # distinguishing positions, high to low
        self.r = len(self.pos)
        self.width = self.r + 1  # one sketch plus a sentinel bit per field
        self.mult = 0
        self.high = 0
        self.packed = 0
        for j, x in enumerate(keys):
            shift = j * self.width
            self.mult |= 1 << shift
            self.high |= 1 << (shift + self.r)
            self.packed |= ((1 << self.r) | self.sketch(x)) << shift

    def sketch(self, z: int) -> int:
        s = 0
        for b in self.pos:
            s = (s << 1) | ((z >> b) & 1)
        return s

    def packed_rank(self, s: int) -> int:
        """The number of keys whose sketch is less than s, for 0 <= s <= 2^r."""
        q = s * self.mult  # @line L9
        t = (self.packed - q) & self.high  # @line L10
        return len(self.keys) - bin(t).count("1")  # @line L11

    def node_pred(self, q: int) -> int:
        """Index of the largest key <= q in this node, or -1."""
        keys = self.keys
        s = self.sketch(q)  # @line L1
        i = self.packed_rank(s)  # @line L2
        y = None  # @line L3
        for j in (i - 1, i):
            if 0 <= j < len(keys) and (y is None or (keys[j] ^ q) < (y ^ q)):
                y = keys[j]
        if y == q:  # @line L4
            return i  # keys[i - 1] has a smaller sketch, so q is keys[i]
        p = msb(q ^ y)  # @line L5
        if (q >> p) & 1:  # @line L6
            e = ((q >> (p + 1)) << (p + 1)) | ((1 << p) - 1)
            rank = self.packed_rank(self.sketch(e) + 1)
        else:  # @line L7
            e = ((q >> (p + 1)) << (p + 1)) | (1 << p)
            rank = self.packed_rank(self.sketch(e))
        return rank - 1  # @line L8


class FusionTree:
    def __init__(self, keys, w: int = 64, b: int = 8) -> None:
        if b < 1 or b * b > w:
            raise ValueError("need 1 <= b and b * b <= w so that a node fits in a word")
        self.w, self.b = w, b
        a = sorted(set(keys))
        for x in a:
            if not 0 <= x < (1 << w):
                raise ValueError("keys must be w-bit unsigned integers")
        self.n = len(a)
        self.root = self._build(a)

    def _build(self, a: List[int]) -> Optional[FusionNode]:
        if not a:
            return None
        root_holder: List[Optional[FusionNode]] = [None]
        stack = [(a, None, 0)]
        while stack:
            part, parent, slot = stack.pop()
            m = len(part)
            if m <= self.b:
                node = FusionNode(part)
                rest: List[List[int]] = []
            else:
                k = self.b
                idx = [(j + 1) * (m + 1) // (k + 1) - 1 for j in range(k)]
                node = FusionNode([part[t] for t in idx])
                bounds = [-1] + idx + [m]
                rest = [part[bounds[j] + 1:bounds[j + 1]] for j in range(k + 1)]
            if parent is None:
                root_holder[0] = node
            else:
                parent.children[slot] = node
            for j, sub in enumerate(rest):
                if sub:
                    stack.append((sub, node, j))
        return root_holder[0]

    def __len__(self) -> int:
        return self.n

    def predecessor(self, q: int) -> Optional[int]:
        """The largest key <= q, or None."""
        v = self.root  # @line L12
        best = None
        while v is not None:  # @line L13
            j = v.node_pred(q)  # @line L14
            if j >= 0 and v.keys[j] == q:  # @line L15
                return q
            if j >= 0:  # @line L16
                best = v.keys[j]
            v = v.children[j + 1]  # @line L17
        return best  # @line L18

    def successor(self, q: int) -> Optional[int]:
        """The smallest key >= q, or None, with the same node ranks."""
        v = self.root
        best = None
        while v is not None:
            j = v.node_pred(q)
            if j >= 0 and v.keys[j] == q:
                return q
            if j + 1 < len(v.keys):
                best = v.keys[j + 1]
            v = v.children[j + 1]
        return best

    def contains(self, q: int) -> bool:
        return self.predecessor(q) == q

    def keys(self) -> List[int]:
        """All keys in increasing order, by an in-order walk with an explicit stack."""
        out: List[int] = []
        stack: List[tuple] = [(False, self.root)]
        while stack:
            is_key, item = stack.pop()
            if is_key:
                out.append(item)
            elif item is not None:
                v = item
                for j in range(len(v.keys), 0, -1):
                    stack.append((False, v.children[j]))
                    stack.append((True, v.keys[j - 1]))
                stack.append((False, v.children[0]))
        return out

    def height(self) -> int:
        h, v = 0, self.root
        while v is not None:
            h, v = h + 1, v.children[0]
        return h

    def check_invariant(self) -> None:
        stack = [(self.root, -1, 1 << self.w)]
        count = 0
        while stack:
            v, lo, hi = stack.pop()
            if v is None:
                continue
            k = v.keys
            assert 1 <= len(k) <= self.b
            assert all(lo < x < hi for x in k)
            assert all(a < b for a, b in zip(k, k[1:]))
            sk = [v.sketch(x) for x in k]
            assert all(a < b for a, b in zip(sk, sk[1:])), "sketches keep the order"
            assert len(k) * v.width <= self.w, "the packed node fits in a word"
            for s in range((1 << v.r) + 1):
                assert v.packed_rank(s) == sum(1 for t in sk if t < s)
            assert len(v.children) == len(k) + 1
            count += len(k)
            bounds = [lo] + k + [hi]
            for j, c in enumerate(v.children):
                stack.append((c, bounds[j], bounds[j + 1]))
        assert count == self.n
