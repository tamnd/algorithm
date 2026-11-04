# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-tree/. The authors are listed in prov/4A6SZN.jsonl.

from typing import Generic, TypeVar

V = TypeVar("V")


class _Node(Generic[V]):
    __slots__ = ("val", "edges")

    def __init__(self, val: "V | None" = None) -> None:
        self.val: V | None = val
        # first symbol of the label -> (label, child)
        self.edges: dict[str, tuple[str, "_Node[V]"]] = {}


def _lcp(a: str, b: str) -> int:
    j = 0
    while j < len(a) and j < len(b) and a[j] == b[j]:
        j += 1
    return j


class RadixTree(Generic[V]):
    """A radix tree (compressed trie) with string-labelled edges.

    get, put and delete take O(m) expected time for a key of length m: the
    walk compares each symbol of the key once, and child lookup is a dict
    lookup. The tree has at most 2n nodes for n keys. Values must not be None.
    """

    def __init__(self) -> None:
        self.root: _Node[V] = _Node()
        self.n = 0

    def size(self) -> int:
        return self.n

    def _walk(self, s: str) -> list[tuple[_Node[V], str]]:
        """Return the path [(node, label of the edge into it)] to the node of s, or [] if none."""
        x = self.root
        path = [(x, "")]
        i = 0
        while i < len(s):
            e = x.edges.get(s[i])
            if e is None or not s.startswith(e[0], i):
                return []
            i += len(e[0])
            x = e[1]
            path.append((x, e[0]))
        return path

    def get(self, s: str) -> V | None:
        """Return the value of key s, or None."""
        x = self.root  # @line L1
        i = 0
        while i < len(s):  # @line L2
            e = x.edges.get(s[i])  # @line L3
            if e is None or not s.startswith(e[0], i):  # @line L4
                return None
            i += len(e[0])  # @line L5
            x = e[1]
        return x.val  # @line L6

    def put(self, s: str, v: V) -> None:
        """Set the value of key s to v (v must not be None)."""
        if v is None:
            raise ValueError("a value must not be None")
        x = self.root  # @line L7
        i = 0
        while i < len(s):  # @line L8
            e = x.edges.get(s[i])  # @line L9
            if e is None:  # @line L10
                x.edges[s[i]] = (s[i:], _Node(v))
                self.n += 1
                return
            label, child = e
            j = _lcp(label, s[i:])  # @line L11
            if j < len(label):  # @line L12
                z: _Node[V] = _Node()  # @line L13
                z.edges[label[j]] = (label[j:], child)
                x.edges[s[i]] = (label[:j], z)
                child = z  # @line L14
            i += j  # @line L15
            x = child
        if x.val is None:  # @line L16
            self.n += 1
        x.val = v  # @line L17

    def delete(self, s: str) -> None:
        """Remove key s if present, and merge the nodes that no longer branch."""
        path = self._walk(s)  # @line L18
        if not path or path[-1][0].val is None:  # @line L19
            return
        x = path[-1][0]
        x.val = None  # @line L20
        self.n -= 1
        k = len(path) - 1
        if k > 0 and not x.edges:  # @line L21
            parent, label = path[k - 1][0], path[k][1]
            del parent.edges[label[0]]
            k -= 1
        x, into = path[k]
        if k > 0 and x.val is None and len(x.edges) == 1:  # @line L22
            parent = path[k - 1][0]
            (flabel, fchild), = x.edges.values()
            parent.edges[into[0]] = (into + flabel, fchild)

    def keys_with_prefix(self, p: str) -> list[str]:
        """Return the keys that start with p, in lexicographic order."""
        x = self.root  # @line L23
        i = 0
        t = ""
        while i < len(p):
            e = x.edges.get(p[i])
            if e is None:
                return []
            label, child = e
            rest = p[i:]
            if not (label.startswith(rest) or rest.startswith(label)):
                return []
            i += len(label)
            t += label
            x = child
        out: list[str] = []  # @line L24
        stack: list[tuple[_Node[V], str]] = [(x, t)]
        while stack:  # @line L25
            y, u = stack.pop()  # @line L26
            if y.val is not None:  # @line L27
                out.append(u)
            for c in sorted(y.edges, reverse=True):  # @line L28
                label, child = y.edges[c]
                stack.append((child, u + label))
        return out  # @line L29

    def keys(self) -> list[str]:
        return self.keys_with_prefix("")

    def longest_prefix_of(self, s: str) -> str | None:
        """Return the longest key that is a prefix of s, or None."""
        x = self.root
        i, best = 0, (0 if self.root.val is not None else -1)
        while i < len(s):
            e = x.edges.get(s[i])
            if e is None or not s.startswith(e[0], i):
                break
            i += len(e[0])
            x = e[1]
            if x.val is not None:
                best = i
        return None if best < 0 else s[:best]

    def node_count(self) -> int:
        count, stack = 0, [self.root]
        while stack:
            y = stack.pop()
            count += 1
            stack.extend(c for _, c in y.edges.values())
        return count

    def check_invariant(self) -> None:
        """Check (R1) to (R4)."""
        valued, stack = 0, [(self.root, True)]
        while stack:
            y, is_root = stack.pop()
            if y.val is not None:
                valued += 1
            elif not is_root:
                assert len(y.edges) >= 2, "a node without a value must branch"
            for c, (label, child) in y.edges.items():
                assert label and label[0] == c
                stack.append((child, False))
        assert valued == self.n
