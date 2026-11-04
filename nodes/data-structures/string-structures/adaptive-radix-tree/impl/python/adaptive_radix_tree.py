# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-radix-tree/. The authors are listed in prov/1RJXRZ.jsonl.

"""Adaptive radix tree (ART) over byte strings.

Inner nodes branch on one byte and come in four layouts, chosen by the number
of children: Node4 and Node16 keep sorted parallel arrays of key bytes and
children, Node48 keeps a 256-entry index into 48 child slots, and Node256 keeps
256 child slots. Each inner node stores the bytes of its compressed path in
full (pessimistic path compression), and leaves store their whole key (lazy
expansion). A 0 byte is appended to every key as a terminator, so no stored
key is a prefix of another; keys must not contain the byte 0.
"""

from typing import Generic, TypeVar

V = TypeVar("V")

# Shrink thresholds give hysteresis: a node shrinks only well below the size
# at which the smaller layout would have grown into it.
SHRINK = {16: 3, 48: 12, 256: 36}
SMALLER = {16: 4, 48: 16, 256: 48}
CAPACITY = {4: 4, 16: 16, 48: 48, 256: 256}
LARGER = {4: 16, 16: 48, 48: 256}


class _Leaf(Generic[V]):
    __slots__ = ("key", "val")

    def __init__(self, key: bytes, val: V) -> None:
        self.key = key
        self.val = val


class _Inner:
    """An inner node of layout kind 4, 16, 48 or 256."""

    __slots__ = ("kind", "prefix", "count", "keys", "kids", "index")

    def __init__(self, kind: int, prefix: bytes) -> None:
        self.kind = kind
        self.prefix = prefix
        self.count = 0
        self.keys: list[int] = []  # Node4 and Node16: sorted key bytes
        self.kids: list[object] = []  # children: parallel to keys, 48 slots, or 256 slots
        self.index: list[int] = []  # Node48: byte -> slot, or -1
        if kind == 48:
            self.index = [-1] * 256
        elif kind == 256:
            self.kids = [None] * 256

    def find(self, b: int) -> object:
        if self.kind <= 16:
            for k, kb in enumerate(self.keys):  # a SIMD compare of 16 bytes in a real ART
                if kb == b:
                    return self.kids[k]
            return None
        if self.kind == 48:
            s = self.index[b]
            return None if s < 0 else self.kids[s]
        return self.kids[b]

    def items(self) -> list[tuple[int, object]]:
        """The children with their bytes, in increasing byte order."""
        if self.kind <= 16:
            return list(zip(self.keys, self.kids))
        if self.kind == 48:
            return [(b, self.kids[s]) for b, s in enumerate(self.index) if s >= 0]
        return [(b, c) for b, c in enumerate(self.kids) if c is not None]

    def set(self, b: int, child: object) -> None:
        """Replace the child of an existing byte b."""
        if self.kind <= 16:
            self.kids[self.keys.index(b)] = child
        elif self.kind == 48:
            self.kids[self.index[b]] = child
        else:
            self.kids[b] = child

    def add(self, b: int, child: object) -> None:
        """Add a child for a new byte b; the node must not be full."""
        if self.kind <= 16:
            k = 0
            while k < len(self.keys) and self.keys[k] < b:
                k += 1
            self.keys.insert(k, b)
            self.kids.insert(k, child)
        elif self.kind == 48:
            slot = self.kids.index(None) if None in self.kids else len(self.kids)
            if slot == len(self.kids):
                self.kids.append(child)
            else:
                self.kids[slot] = child
            self.index[b] = slot
        else:
            self.kids[b] = child
        self.count += 1

    def remove(self, b: int) -> None:
        if self.kind <= 16:
            k = self.keys.index(b)
            del self.keys[k]
            del self.kids[k]
        elif self.kind == 48:
            self.kids[self.index[b]] = None
            self.index[b] = -1
        else:
            self.kids[b] = None
        self.count -= 1


def _relayout(node: _Inner, kind: int) -> _Inner:
    new = _Inner(kind, node.prefix)
    for b, c in node.items():
        new.add(b, c)
    return new


class AdaptiveRadixTree(Generic[V]):
    """Ordered map from byte strings (without the byte 0) to values."""

    def __init__(self) -> None:
        self.root: object = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    @staticmethod
    def _key(key: bytes) -> bytes:
        if 0 in key:
            raise ValueError("keys must not contain the byte 0")
        return bytes(key) + b"\x00"

    def get(self, key: bytes) -> V | None:
        """Return the value of key, or None."""
        k = self._key(key)
        node, depth = self.root, 0
        while isinstance(node, _Inner):  # @line L1
            p = node.prefix
            if k[depth : depth + len(p)] != p:  # @line L2
                return None
            depth += len(p)  # @line L3
            node = node.find(k[depth])  # @line L4
            depth += 1
        if node is not None and node.key == k:  # @line L5
            return node.val
        return None  # @line L6

    def _replace(self, parent: _Inner | None, b: int, new: object) -> None:
        if parent is None:
            self.root = new
        else:
            parent.set(b, new)

    def put(self, key: bytes, val: V) -> None:
        """Set the value of key to val."""
        k = self._key(key)
        node, depth = self.root, 0
        parent: _Inner | None = None
        pb = -1
        if node is None:  # @line L7
            self.root = _Leaf(k, val)
            self.n += 1
            return
        while True:
            if isinstance(node, _Leaf):  # @line L8
                if node.key == k:
                    node.val = val
                    return
                lk = node.key  # @line L9
                p = 0
                while lk[depth + p] == k[depth + p]:
                    p += 1
                split = _Inner(4, k[depth : depth + p])  # @line L10
                split.add(lk[depth + p], node)
                split.add(k[depth + p], _Leaf(k, val))
                self._replace(parent, pb, split)
                self.n += 1
                return
            assert isinstance(node, _Inner)
            pre = node.prefix
            m = 0
            while m < len(pre) and pre[m] == k[depth + m]:  # @line L11
                m += 1
            if m < len(pre):  # @line L12
                split = _Inner(4, pre[:m])
                old_byte = pre[m]
                node.prefix = pre[m + 1 :]
                split.add(old_byte, node)
                split.add(k[depth + m], _Leaf(k, val))
                self._replace(parent, pb, split)
                self.n += 1
                return
            depth += len(pre)  # @line L13
            b = k[depth]
            child = node.find(b)
            if child is None:  # @line L14
                if node.count == CAPACITY[node.kind]:  # @line L15
                    node2 = _relayout(node, LARGER[node.kind])
                    self._replace(parent, pb, node2)
                    node = node2
                node.add(b, _Leaf(k, val))  # @line L16
                self.n += 1
                return
            parent, pb, node, depth = node, b, child, depth + 1  # @line L17

    def delete(self, key: bytes) -> None:
        """Remove key if present, shrinking or merging nodes as needed."""
        k = self._key(key)
        path: list[tuple[_Inner, int]] = []
        node, depth = self.root, 0
        while isinstance(node, _Inner):  # @line L18
            p = node.prefix
            if k[depth : depth + len(p)] != p:
                return
            depth += len(p)
            path.append((node, k[depth]))
            node = node.find(k[depth])
            depth += 1
        if node is None or node.key != k:  # @line L19
            return
        self.n -= 1
        if not path:
            self.root = None
            return
        parent, b = path[-1]  # @line L20
        parent.remove(b)
        grand, gb = path[-2] if len(path) >= 2 else (None, -1)
        if parent.count == 1:  # @line L21
            (cb, only), = parent.items()
            if isinstance(only, _Inner):
                only.prefix = parent.prefix + bytes([cb]) + only.prefix
            self._replace(grand, gb, only)
        elif parent.kind in SHRINK and parent.count <= SHRINK[parent.kind]:  # @line L22
            self._replace(grand, gb, _relayout(parent, SMALLER[parent.kind]))

    def items(self) -> list[tuple[bytes, V]]:
        """All (key, value) pairs in increasing byte order of the keys."""
        out: list[tuple[bytes, V]] = []
        stack: list[object] = [self.root]
        while stack:
            node = stack.pop()
            if node is None:
                continue
            if isinstance(node, _Leaf):
                out.append((node.key[:-1], node.val))
            else:
                assert isinstance(node, _Inner)
                stack.extend(c for _, c in reversed(node.items()))
        return out

    def keys(self) -> list[bytes]:
        return [k for k, _ in self.items()]

    def node_kinds(self) -> dict[int, int]:
        """The number of inner nodes of each layout."""
        out = {4: 0, 16: 0, 48: 0, 256: 0}
        stack = [self.root]
        while stack:
            node = stack.pop()
            if isinstance(node, _Inner):
                out[node.kind] += 1
                stack.extend(c for _, c in node.items())
        return out

    def check_invariant(self) -> None:
        low = {4: 2, 16: SHRINK[16] + 1, 48: SHRINK[48] + 1, 256: SHRINK[256] + 1}
        leaves = 0
        stack: list[tuple[object, bytes]] = [(self.root, b"")]
        while stack:
            node, path = stack.pop()
            if node is None:
                assert path == b"" and self.n == 0
                continue
            if isinstance(node, _Leaf):
                assert node.key.startswith(path), "leaf key does not match its path"
                assert node.key.endswith(b"\x00") and node.key.count(0) == 1
                leaves += 1
                continue
            assert isinstance(node, _Inner)
            kids = node.items()
            assert node.count == len(kids) and low[node.kind] <= node.count <= CAPACITY[node.kind]
            if node.kind <= 16:
                assert node.keys == sorted(set(node.keys))
            if node.kind == 48:
                assert sum(c is not None for c in node.kids) == node.count
            for b, c in kids:
                stack.append((c, path + node.prefix + bytes([b])))
        assert leaves == self.n
