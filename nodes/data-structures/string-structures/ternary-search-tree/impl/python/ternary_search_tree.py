# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ternary-search-tree/. The authors are listed in prov/BVWSE3.jsonl.

from typing import Generic, TypeVar

V = TypeVar("V")


class _Node(Generic[V]):
    __slots__ = ("c", "left", "mid", "right", "val")

    def __init__(self, c: str) -> None:
        self.c = c
        self.left: _Node[V] | None = None
        self.mid: _Node[V] | None = None
        self.right: _Node[V] | None = None
        self.val: V | None = None


class TernarySearchTree(Generic[V]):
    """A ternary search tree (TST) with string keys of length at least 1.

    Each node holds one symbol and three links. A search compares each symbol
    of the key with one node on the middle path and with the nodes of the
    left and right links that it passes, so get and put take O(m + d) symbol
    comparisons, where d is the number of left and right steps. Values must
    not be None. The empty string is not a key.
    """

    def __init__(self) -> None:
        self.root: _Node[V] | None = None
        self.n = 0

    def size(self) -> int:
        return self.n

    def _find(self, s: str) -> "_Node[V] | None":
        x = self.root
        d = 0
        while x is not None:
            if s[d] < x.c:
                x = x.left
            elif s[d] > x.c:
                x = x.right
            elif d < len(s) - 1:
                x = x.mid
                d += 1
            else:
                return x
        return None

    def get(self, s: str) -> V | None:
        """Return the value of key s, or None."""
        if not s:
            raise ValueError("keys must not be empty")
        x = self.root  # @line L1
        d = 0
        while x is not None:  # @line L2
            if s[d] < x.c:  # @line L3
                x = x.left
            elif s[d] > x.c:  # @line L4
                x = x.right
            elif d < len(s) - 1:  # @line L5
                x = x.mid
                d += 1
            else:
                return x.val  # @line L6
        return None  # @line L7

    def put(self, s: str, v: V) -> None:
        """Set the value of key s to v (s nonempty, v not None)."""
        if not s:
            raise ValueError("keys must not be empty")
        if v is None:
            raise ValueError("a value must not be None")
        if self.root is None:
            self.root = _Node(s[0])
        x = self.root  # @line L8
        d = 0
        while True:  # @line L9
            c = s[d]
            if c < x.c:  # @line L10
                if x.left is None:
                    x.left = _Node(c)
                x = x.left
            elif c > x.c:  # @line L11
                if x.right is None:
                    x.right = _Node(c)
                x = x.right
            elif d < len(s) - 1:  # @line L12
                d += 1
                if x.mid is None:
                    x.mid = _Node(s[d])
                x = x.mid
            else:
                if x.val is None:  # @line L13
                    self.n += 1
                x.val = v  # @line L14
                return

    def delete(self, s: str) -> None:
        """Remove key s if present, and prune the nodes that are no longer needed."""
        if not s:
            return
        # path of (node, parent, which link of the parent leads to node)
        path: list[tuple[_Node[V], _Node[V] | None, str]] = []
        x, parent, link, d = self.root, None, "root", 0  # @line L15
        while x is not None:
            path.append((x, parent, link))
            if s[d] < x.c:
                x, parent, link = x.left, x, "left"
            elif s[d] > x.c:
                x, parent, link = x.right, x, "right"
            elif d < len(s) - 1:
                x, parent, link, d = x.mid, x, "mid", d + 1
            else:
                break
        if x is None or x.val is None:  # @line L16
            return
        x.val = None  # @line L17
        self.n -= 1
        # walk back up: remove each node with no value and no middle child
        for node, par, lk in reversed(path):  # @line L18
            if node.val is not None or node.mid is not None:  # @line L19
                return
            repl = self._bst_remove_root(node)  # @line L20
            self._set_link(par, lk, repl)

    @staticmethod
    def _bst_remove_root(node: "_Node[V]") -> "_Node[V] | None":
        """Return the sibling BST rooted at node with node removed."""
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        # take the smallest node of the right subtree as the new root
        p, m = node, node.right
        while m.left is not None:
            p, m = m, m.left
        if p is not node:
            p.left = m.right
            m.right = node.right
        m.left = node.left
        return m

    def _set_link(self, par: "_Node[V] | None", link: str, child: "_Node[V] | None") -> None:
        if par is None:
            self.root = child
        else:
            setattr(par, link, child)

    def keys_with_prefix(self, p: str) -> list[str]:
        """Return the keys that start with p, in lexicographic order."""
        out: list[str] = []  # @line L21
        if p == "":
            start, prefix = self.root, ""
        else:
            x = self._find(p)
            if x is None:
                return out
            if x.val is not None:
                out.append(p)
            start, prefix = x.mid, p
        # explicit stack: ("node", x, prefix) visits a subtree; ("emit", ...) reports a key
        stack: list[tuple[_Node[V] | None, str, int]] = [(start, prefix, 0)]
        while stack:  # @line L22
            y, t, state = stack.pop()
            if y is None:
                continue
            if state == 0:  # in-order: left, node, mid, right
                stack.append((y.right, t, 0))
                stack.append((y, t, 1))
                stack.append((y.left, t, 0))
            else:
                if y.val is not None:  # @line L23
                    out.append(t + y.c)
                stack.append((y.mid, t + y.c, 0))  # @line L24
        return out  # @line L25

    def keys(self) -> list[str]:
        return self.keys_with_prefix("")

    def longest_prefix_of(self, s: str) -> str | None:
        """Return the longest key that is a prefix of s, or None."""
        x, d, best = self.root, 0, -1
        while x is not None and d < len(s):
            if s[d] < x.c:
                x = x.left
            elif s[d] > x.c:
                x = x.right
            else:
                d += 1
                if x.val is not None:
                    best = d
                x = x.mid
        return None if best < 0 else s[:best]

    def keys_that_match(self, q: str) -> list[str]:
        """Return the keys that match q, where '.' matches any one symbol, in order."""
        out: list[str] = []
        if not q:
            return out
        stack: list[tuple[_Node[V] | None, int, str, int]] = [(self.root, 0, "", 0)]
        while stack:
            y, d, t, state = stack.pop()
            if y is None:
                continue
            c = q[d]
            if state == 0:
                if c == "." or c > y.c:
                    stack.append((y.right, d, t, 0))
                stack.append((y, d, t, 1))
                if c == "." or c < y.c:
                    stack.append((y.left, d, t, 0))
            elif c == "." or c == y.c:
                if d == len(q) - 1:
                    if y.val is not None:
                        out.append(t + y.c)
                else:
                    stack.append((y.mid, d + 1, t + y.c, 0))
        return out

    def node_count(self) -> int:
        count, stack = 0, [self.root]
        while stack:
            y = stack.pop()
            if y is not None:
                count += 1
                stack.extend((y.left, y.mid, y.right))
        return count

    def check_invariant(self) -> None:
        """Check the BST order of each sibling tree, no dead nodes, and the count."""
        valued = 0
        stack: list[tuple[_Node[V] | None, str | None, str | None]] = [(self.root, None, None)]
        while stack:
            y, lo, hi = stack.pop()
            if y is None:
                continue
            assert (lo is None or lo < y.c) and (hi is None or y.c < hi)
            assert y.val is not None or y.mid is not None, "dead node"
            if y.val is not None:
                valued += 1
            stack.append((y.left, lo, y.c))
            stack.append((y.right, y.c, hi))
            stack.append((y.mid, None, None))
        assert valued == self.n
