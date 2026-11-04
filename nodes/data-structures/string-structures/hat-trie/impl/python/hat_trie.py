# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hat-trie/. The authors are listed in prov/HZ5P9K.jsonl.

from typing import Generic, TypeVar

V = TypeVar("V")


def _hash(s: str) -> int:
    """Shift-add-xor string hash, deterministic across runs."""
    h = 220373
    for c in s:
        h ^= ((h << 5) + (h >> 2) + ord(c)) & 0xFFFFFFFF
    return h


class Container(Generic[V]):
    """An array hash table: each slot is one array of (suffix, value) entries.

    A pure container hangs from one pointer and stores the suffixes without the
    symbol of that pointer. A hybrid container hangs from the pointers lo .. hi - 1
    of its parent and keeps the first symbol of each suffix.
    """

    def __init__(self, slots: int, pure: bool, lo: int, hi: int) -> None:
        self.slots: list[list[tuple[str, V]]] = [[] for _ in range(slots)]
        self.pure = pure
        self.lo, self.hi = lo, hi
        self.size = 0

    def find(self, t: str) -> V | None:
        for k, v in self.slots[_hash(t) % len(self.slots)]:  # @line L5
            if k == t:
                return v
        return None

    def put(self, t: str, v: V) -> bool:
        """Insert or update t; return True if t is new."""
        slot = self.slots[_hash(t) % len(self.slots)]
        for i, (k, _) in enumerate(slot):
            if k == t:
                slot[i] = (t, v)
                return False
        slot.append((t, v))  # @line L7
        self.size += 1
        return True

    def items(self) -> list[tuple[str, V]]:
        return [e for slot in self.slots for e in slot]


class Node(Generic[V]):
    __slots__ = ("child", "value")

    def __init__(self, r: int) -> None:
        self.child: list[Node[V] | Container[V]] = []
        self.value: V | None = None  # the value of the key that ends at this node


class HatTrie(Generic[V]):
    """A HAT-trie over the symbols with codes 0 .. r - 1.

    Trie nodes have an array of r pointers; leaves are array hash containers of at
    most `limit` entries. Values must not be None.
    """

    def __init__(self, r: int = 128, limit: int = 1024, slots: int = 64) -> None:
        if limit < 1 or slots < 1:
            raise ValueError("the limit and the number of slots must be positive")
        self.r, self.limit, self.nslots = r, limit, slots
        self.root: Node[V] = self._node()
        self.n = 0
        self.bursts = 0

    def _node(self) -> Node[V]:
        x: Node[V] = Node(self.r)
        h: Container[V] = Container(self.nslots, False, 0, self.r)
        x.child = [h] * self.r
        return x

    def _code(self, c: str) -> int:
        k = ord(c)
        if k >= self.r:
            raise ValueError(f"symbol {c!r} is outside the alphabet")
        return k

    def _descend(self, s: str) -> tuple[Node[V], int]:
        """The deepest trie node on the path of s and the number of symbols it consumed."""
        x, d = self.root, 0  # @line L1
        while d < len(s):  # @line L2
            y = x.child[self._code(s[d])]  # @line L3
            if not isinstance(y, Node):
                break
            x, d = y, d + 1
        return x, d

    def get(self, s: str) -> V | None:
        x, d = self._descend(s)
        if d == len(s):
            return x.value
        y = x.child[self._code(s[d])]
        assert isinstance(y, Container)
        return y.find(s[d + 1:] if y.pure else s[d:])  # @line L4

    def put(self, s: str, v: V) -> None:
        if v is None:
            raise ValueError("a value must not be None")
        x, d = self._descend(s)  # @line L6
        if d == len(s):
            if x.value is None:
                self.n += 1
            x.value = v
            return
        y = x.child[self._code(s[d])]
        assert isinstance(y, Container)
        if y.put(s[d + 1:] if y.pure else s[d:], v):
            self.n += 1
        if y.size > self.limit:  # @line L8
            self._burst(x, y)

    def _burst(self, x: Node[V], y: Container[V]) -> None:
        work = [(x, y)]
        while work:  # @line L12
            x, y = work.pop()
            if y.size <= self.limit:
                continue
            self.bursts += 1
            if y.pure:  # @line L9
                z = self._node()
                x.child[y.lo] = z
                h = z.child[0]
                assert isinstance(h, Container)
                for t, v in y.items():
                    if t == "":
                        z.value = v
                    else:
                        h.put(t, v)
                work.append((z, h))
                continue
            counts = [0] * (y.hi - y.lo)
            for t, _ in y.items():
                counts[ord(t[0]) - y.lo] += 1
            if y.hi - y.lo == 1:  # @line L11
                p: Container[V] = Container(self.nslots, True, y.lo, y.hi)
                for t, v in y.items():
                    p.put(t[1:], v)
                x.child[y.lo] = p
                work.append((x, p))
                continue
            used = [y.lo + i for i, k in enumerate(counts) if k]
            if len(used) == 1:  # @line L10
                c = used[0]  # one symbol only: cut out its range
                cuts = [y.lo, c, c + 1, y.hi]
            else:
                best, split, left = None, used[1], 0
                for s in range(used[0] + 1, used[-1] + 1):
                    left += counts[s - 1 - y.lo]
                    gap = abs(2 * left - y.size)
                    if best is None or gap < best:
                        best, split = gap, s
                cuts = [y.lo, split, y.hi]
            for lo, hi in zip(cuts, cuts[1:]):
                if lo == hi:
                    continue
                part: Container[V] = Container(self.nslots, False, lo, hi)
                for t, v in y.items():
                    if lo <= ord(t[0]) < hi:
                        part.put(t, v)
                for c in range(lo, hi):
                    x.child[c] = part
                work.append((x, part))

    def size(self) -> int:
        return self.n

    def keys(self) -> list[str]:
        """All keys in sorted order; each container is sorted when it is reached."""
        out: list[str] = []
        stack: list[tuple[Node[V] | None, str, Container[V] | None]] = [(self.root, "", None)]
        while stack:
            x, prefix, c = stack.pop()
            if c is not None:
                out.extend(sorted(prefix + t for t, _ in c.items()))
                continue
            assert x is not None
            if x.value is not None:
                out.append(prefix)
            entries: list[tuple[Node[V] | None, str, Container[V] | None]] = []
            k = 0
            while k < self.r:
                y = x.child[k]
                if isinstance(y, Node):
                    entries.append((y, prefix + chr(k), None))
                    k += 1
                elif y.pure:
                    entries.append((None, prefix + chr(k), y))
                    k += 1
                else:
                    entries.append((None, prefix, y))
                    k = y.hi
            stack.extend(reversed(entries))
        return out

    def check_invariant(self) -> None:
        count = 0
        stack = [self.root]
        while stack:
            x = stack.pop()
            assert len(x.child) == self.r
            count += x.value is not None
            k = 0
            while k < self.r:
                y = x.child[k]
                if isinstance(y, Node):
                    stack.append(y)
                    k += 1
                    continue
                assert y.lo == k and y.size <= self.limit
                assert all(x.child[c] is y for c in range(y.lo, y.hi))
                assert y.size == len(y.items())
                if y.pure:
                    assert y.hi == k + 1
                else:
                    assert all(t != "" and y.lo <= ord(t[0]) < y.hi for t, _ in y.items())
                for t, _ in y.items():
                    assert y.slots[_hash(t) % len(y.slots)].count((t, y.find(t))) == 1
                count += y.size
                k = y.hi
        assert count == self.n
