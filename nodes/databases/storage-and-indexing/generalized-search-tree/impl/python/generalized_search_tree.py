# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-search-tree/. The authors are listed in prov/SE99CH.jsonl.

"""Generalized search tree (GiST) of Hellerstein, Naughton and Pfeffer (1995).

The tree code knows nothing about keys. An extension object supplies the six
key methods: consistent, union, compress, decompress, penalty and pick_split.
Two extensions are given: IntervalExt (it behaves like a B+ tree on integers)
and RectExt (it behaves like an R-tree with Guttman's quadratic split, and its
compress step rounds rectangles outward to a grid, so its keys are lossy).

A leaf entry is (compressed key, record id). The exact key of each record is
kept in self.records, so that a search on lossy keys can recheck its result.
"""

from typing import Dict, List, Optional, Sequence, Tuple


class Entry:
    __slots__ = ("key", "ptr")

    def __init__(self, key, ptr):
        self.key = key      # a compressed predicate
        self.ptr = ptr      # a Node, or a record id in a leaf


class Node:
    __slots__ = ("leaf", "entries", "parent")

    def __init__(self, leaf: bool):
        self.leaf = leaf
        self.entries: List[Entry] = []
        self.parent: Optional["Node"] = None


class IntervalExt:
    """Keys are closed integer intervals (lo, hi); a point x is (x, x).

    A query (a, b) asks for the keys that overlap [a, b].
    """

    lossy = False

    def consistent(self, p, q) -> bool:
        return p[0] <= q[1] and q[0] <= p[1]

    def union(self, ps: Sequence) -> Tuple[int, int]:
        return (min(p[0] for p in ps), max(p[1] for p in ps))

    def compress(self, p):
        return p

    def decompress(self, p):
        return p

    def penalty(self, p, new) -> int:
        """How much p must grow to cover new."""
        return (max(p[1], new[1]) - min(p[0], new[0])) - (p[1] - p[0])

    def pick_split(self, ps: Sequence, m: int) -> Tuple[List[int], List[int]]:
        order = sorted(range(len(ps)), key=lambda i: (ps[i][0], ps[i][1], i))
        half = len(ps) // 2
        return order[:half], order[half:]

    def contains(self, p, k) -> bool:
        return p[0] <= k[0] and k[1] <= p[1]


def _area(r) -> int:
    return (r[2] - r[0] + 1) * (r[3] - r[1] + 1)


def _bbox(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


class RectExt:
    """Keys are integer rectangles (x1, y1, x2, y2), corners included.

    A query rectangle asks for the keys that intersect it. With grid > 1,
    compress rounds a rectangle outward to multiples of grid, so a compressed
    key covers more than the record and the search must recheck.
    """

    def __init__(self, grid: int = 1):
        self.grid = grid
        self.lossy = grid > 1

    def consistent(self, p, q) -> bool:
        return p[0] <= q[2] and q[0] <= p[2] and p[1] <= q[3] and q[1] <= p[3]

    def union(self, ps: Sequence):
        r = ps[0]
        for p in ps[1:]:
            r = _bbox(r, p)
        return r

    def compress(self, p):
        g = self.grid
        return (p[0] - p[0] % g, p[1] - p[1] % g, p[2] + (g - 1 - p[2] % g), p[3] + (g - 1 - p[3] % g))

    def decompress(self, p):
        return p

    def penalty(self, p, new):
        """Guttman's rule: the growth in area, and then the area."""
        return (_area(_bbox(p, new)) - _area(p), _area(p))

    def pick_split(self, ps: Sequence, m: int) -> Tuple[List[int], List[int]]:
        """Guttman's quadratic split."""
        n = len(ps)
        best = None
        for i in range(n):
            for j in range(i + 1, n):
                waste = _area(_bbox(ps[i], ps[j])) - _area(ps[i]) - _area(ps[j])
                if best is None or waste > best[0]:
                    best = (waste, i, j)
        _, i, j = best
        g1, g2 = [i], [j]
        b1, b2 = ps[i], ps[j]
        rest = [t for t in range(n) if t != i and t != j]
        while rest:
            if len(g1) + len(rest) == m:
                g1.extend(rest)
                break
            if len(g2) + len(rest) == m:
                g2.extend(rest)
                break
            pick = max(rest, key=lambda t: (abs((_area(_bbox(b1, ps[t])) - _area(b1))
                                                - (_area(_bbox(b2, ps[t])) - _area(b2))), -t))
            rest.remove(pick)
            d1 = _area(_bbox(b1, ps[pick])) - _area(b1)
            d2 = _area(_bbox(b2, ps[pick])) - _area(b2)
            if (d1, _area(b1), len(g1)) <= (d2, _area(b2), len(g2)):
                g1.append(pick)
                b1 = _bbox(b1, ps[pick])
            else:
                g2.append(pick)
                b2 = _bbox(b2, ps[pick])
        return g1, g2

    def contains(self, p, k) -> bool:
        return p[0] <= k[0] and p[1] <= k[1] and k[2] <= p[2] and k[3] <= p[3]


class GiST:
    def __init__(self, ext, max_entries: int = 4, min_entries: int = 2):
        if not 2 <= min_entries <= (max_entries + 1) // 2:
            raise ValueError("need 2 <= min_entries <= (max_entries + 1) / 2")
        self.ext = ext
        self.M = max_entries
        self.m = min_entries
        self.root = Node(True)
        self.records: Dict[object, object] = {}
        self.visited = 0

    # ----- search -----

    def search(self, q) -> List:
        """SEARCH: the record ids whose keys are consistent with q, sorted."""
        out: List = []
        self.visited = 0
        self._search(self.root, q, out)
        if self.ext.lossy:
            out = [r for r in out if self.ext.consistent(self.records[r], q)]
        return sorted(out)

    def _search(self, node: Node, q, out: List) -> None:
        self.visited += 1
        if not node.leaf:                                            # @line L1
            for e in node.entries:                                   # @line L2
                if self.ext.consistent(self.ext.decompress(e.key), q):  # @line L3
                    self._search(e.ptr, q, out)                      # @line L3
        else:
            for e in node.entries:                                   # @line L4
                if self.ext.consistent(self.ext.decompress(e.key), q):  # @line L5
                    out.append(e.ptr)                                # @line L5

    # ----- insert -----

    def insert(self, key, rid) -> None:
        if rid in self.records:
            raise KeyError("record id already present")
        self.records[rid] = key
        leaf = self._choose_subtree(self.root, key)                  # @line L6
        leaf.entries.append(Entry(self.ext.compress(key), rid))      # @line L7
        self._fix_upward(leaf)                                       # @line L8

    def _choose_subtree(self, node: Node, key) -> Node:
        while not node.leaf:                                         # @line L10
            best = min(range(len(node.entries)),                     # @line L11
                       key=lambda i: (self.ext.penalty(self.ext.decompress(node.entries[i].key), key), i))
            node = node.entries[best].ptr                            # @line L12
        return node                                                  # @line L10

    def _node_key(self, node: Node):
        """COMPRESS(UNION(the keys of the entries of node))."""
        return self.ext.compress(self.ext.union([self.ext.decompress(e.key) for e in node.entries]))

    def _entry_of(self, node: Node) -> Entry:
        for e in node.parent.entries:
            if e.ptr is node:
                return e
        raise AssertionError("node not found in its parent")

    def _split(self, node: Node) -> Node:
        keys = [self.ext.decompress(e.key) for e in node.entries]
        g1, g2 = self.ext.pick_split(keys, self.m)                   # @line L13
        assert len(g1) >= self.m and len(g2) >= self.m
        old = node.entries
        node.entries = [old[i] for i in sorted(g1)]                  # @line L14
        other = Node(node.leaf)                                      # @line L14
        other.entries = [old[i] for i in sorted(g2)]                 # @line L14
        if not other.leaf:
            for e in other.entries:
                e.ptr.parent = other
        return other

    def _fix_upward(self, node: Node) -> None:
        """Split nodes that overflow and ADJUST-KEYS up to the root."""
        while True:
            new = self._split(node) if len(node.entries) > self.M else None   # @line L8
            if node.parent is None:
                if new is not None:
                    root = Node(False)
                    for c in (node, new):
                        c.parent = root
                        root.entries.append(Entry(self._node_key(c), c))
                    self.root = root
                return
            parent = node.parent
            self._entry_of(node).key = self._node_key(node)          # @line L16
            if new is not None:
                new.parent = parent
                parent.entries.append(Entry(self._node_key(new), new))  # @line L15
            node = parent                                            # @line L9

    # ----- delete -----

    def delete(self, rid) -> bool:
        """DELETE: remove a record; condense underfull nodes by reinsertion."""
        if rid not in self.records:
            return False
        key = self.records.pop(rid)
        leaf = self._find_leaf(self.root, key, rid)                  # @line L17
        assert leaf is not None
        leaf.entries = [e for e in leaf.entries if e.ptr != rid]     # @line L17
        orphans: List = []
        node = leaf
        while node.parent is not None:
            parent = node.parent
            if len(node.entries) < self.m:                           # @line L18
                parent.entries = [e for e in parent.entries if e.ptr is not node]
                self._collect(node, orphans)
            elif node.entries:
                self._entry_of(node).key = self._node_key(node)      # @line L19
            node = parent
        while not self.root.leaf and len(self.root.entries) == 1:
            self.root = self.root.entries[0].ptr
            self.root.parent = None
        if not self.root.leaf and not self.root.entries:
            self.root = Node(True)
        for r in orphans:                                            # @line L18
            k = self.records.pop(r)
            self.insert(k, r)
        return True

    def _find_leaf(self, node: Node, key, rid) -> Optional[Node]:
        for e in node.entries:
            if node.leaf:
                if e.ptr == rid:
                    return node
            elif self.ext.consistent(self.ext.decompress(e.key), key):
                found = self._find_leaf(e.ptr, key, rid)
                if found is not None:
                    return found
        return None

    def _collect(self, node: Node, out: List) -> None:
        for e in node.entries:
            if node.leaf:
                out.append(e.ptr)
            else:
                self._collect(e.ptr, out)

    # ----- checks -----

    def height(self) -> int:
        h, v = 1, self.root
        while not v.leaf:
            h, v = h + 1, v.entries[0].ptr
        return h

    def check(self) -> None:
        """Raise AssertionError if a tree property of the paper fails."""
        depths = set()
        rids: List = []
        self._check(self.root, 1, depths, rids)
        assert len(depths) <= 1, "leaves at different depths"
        assert sorted(rids, key=repr) == sorted(self.records, key=repr)

    def _check(self, node: Node, depth: int, depths, rids) -> List:
        if node is not self.root:
            assert self.m <= len(node.entries) <= self.M, "fill out of range"
        else:
            assert len(node.entries) <= self.M
            if not node.leaf:
                assert len(node.entries) >= 2
        if node.leaf:
            depths.add(depth)
            keys = []
            for e in node.entries:
                rids.append(e.ptr)
                exact = self.records[e.ptr]
                assert self.ext.contains(self.ext.decompress(e.key), exact)
                keys.append(exact)
            return keys
        below_all = []
        for e in node.entries:
            assert e.ptr.parent is node
            assert e.key == self._node_key(e.ptr), "key is not the union of its child"
            below = self._check(e.ptr, depth + 1, depths, rids)
            for k in below:
                assert self.ext.contains(self.ext.decompress(e.key), k)
            below_all.extend(below)
        return below_all
