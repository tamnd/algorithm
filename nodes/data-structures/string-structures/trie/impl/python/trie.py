# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trie/. The authors are listed in prov/SJRBA7.jsonl.

from typing import Generic, TypeVar

V = TypeVar("V")


class _Node(Generic[V]):
    __slots__ = ("val", "next")

    def __init__(self) -> None:
        self.val: V | None = None
        self.next: dict[str, "_Node[V]"] = {}


class Trie(Generic[V]):
    """A trie with a dictionary of children in each node.

    get, put and delete take O(m) expected time for a key of length m.
    keys_with_prefix takes O(|p| + t) expected time, where t is the number
    of nodes below the node of p. Values must not be None.
    """

    def __init__(self) -> None:
        self.root: _Node[V] = _Node()
        self.n = 0

    def size(self) -> int:
        return self.n

    def get(self, s: str) -> V | None:
        """Return the value of key s, or None if s is not a key."""
        x: _Node[V] | None = self.root  # @line L1
        for c in s:  # @line L2
            x = x.next.get(c)  # @line L3
            if x is None:  # @line L4
                return None
        return x.val  # @line L5

    def contains(self, s: str) -> bool:
        return self.get(s) is not None

    def put(self, s: str, v: V) -> None:
        """Set the value of key s to v (v must not be None)."""
        if v is None:
            raise ValueError("a value must not be None")
        x = self.root  # @line L6
        for c in s:  # @line L7
            if c not in x.next:  # @line L8
                x.next[c] = _Node()
            x = x.next[c]  # @line L9
        if x.val is None:  # @line L10
            self.n += 1
        x.val = v  # @line L11

    def delete(self, s: str) -> None:
        """Remove key s if it is a key, and cut the nodes that are no longer needed."""
        path = [self.root]  # @line L12
        x: _Node[V] | None = self.root
        for c in s:  # @line L13
            x = x.next.get(c)  # @line L14
            if x is None:  # @line L15
                return
            path.append(x)  # @line L16
        assert x is not None
        if x.val is None:  # @line L17
            return
        x.val = None  # @line L18
        self.n -= 1
        for i in range(len(s), 0, -1):  # @line L19
            if path[i].val is not None or path[i].next:  # @line L20
                return
            del path[i - 1].next[s[i - 1]]  # @line L21

    def keys_with_prefix(self, p: str) -> list[str]:
        """Return the keys that start with p, in lexicographic order."""
        x: _Node[V] | None = self.root  # @line L22
        for c in p:
            x = x.next.get(c)
            if x is None:
                break
        if x is None:  # @line L23
            return []
        out: list[str] = []  # @line L24
        stack: list[tuple[_Node[V], str]] = [(x, p)]
        while stack:  # @line L25
            y, t = stack.pop()  # @line L26
            if y.val is not None:  # @line L27
                out.append(t)
            for c in sorted(y.next, reverse=True):  # @line L28
                stack.append((y.next[c], t + c))
        return out  # @line L29

    def keys(self) -> list[str]:
        return self.keys_with_prefix("")

    def longest_prefix_of(self, s: str) -> str | None:
        """Return the longest key that is a prefix of s, or None."""
        x: _Node[V] | None = self.root  # @line L30
        best = -1
        for i in range(len(s) + 1):  # @line L31
            assert x is not None
            if x.val is not None:  # @line L32
                best = i
            if i == len(s):  # @line L33
                break
            x = x.next.get(s[i])  # @line L34
            if x is None:  # @line L35
                break
        return None if best < 0 else s[:best]  # @line L36

    def keys_that_match(self, q: str) -> list[str]:
        """Return the keys of length |q| that match q, where '.' matches any one symbol."""
        out: list[str] = []
        stack: list[tuple[_Node[V], str]] = [(self.root, "")]
        while stack:
            y, t = stack.pop()
            d = len(t)
            if d == len(q):
                if y.val is not None:
                    out.append(t)
                continue
            if q[d] == ".":
                for c in sorted(y.next, reverse=True):
                    stack.append((y.next[c], t + c))
            elif q[d] in y.next:
                stack.append((y.next[q[d]], t + q[d]))
        return out

    def node_count(self) -> int:
        count, stack = 0, [self.root]
        while stack:
            y = stack.pop()
            count += 1
            stack.extend(y.next.values())
        return count

    def check_invariant(self) -> None:
        """Check (T2) and (T3)."""
        valued, stack = 0, [self.root]
        while stack:
            y = stack.pop()
            if y.val is not None:
                valued += 1
            elif y is not self.root:
                assert y.next, "a node without a value must have a child"
            stack.extend(y.next.values())
        assert valued == self.n
