# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/holm-de-lichtenberg-thorup/. The authors are listed in prov/4DN5PG.jsonl.

"""Holm-de Lichtenberg-Thorup fully dynamic connectivity.

Every edge has a level between 0 and floor(lg n). F_i is a spanning forest of
the edges of level at least i, kept as an Euler tour forest in treaps; F_0 is
a spanning forest of the whole graph. A tree of F_i has at most n / 2^i
vertices. When a tree edge of level l is deleted, the algorithm looks for a
replacement edge at levels l, l - 1, ..., 0, and raises the level of every
edge it checks and rejects, which pays for the search. Insertions and
deletions (fully dynamic); O(log^2 n) amortized time per update; O(log n)
time per query. Deterministic, apart from the treap priorities, which only
affect the running time.
"""

import random


class _Node:
    __slots__ = ("pri", "left", "right", "parent", "size", "loops", "nt", "tr",
                 "snt", "str_", "u", "v")

    def __init__(self, u: int, v: int, pri: float) -> None:
        self.u, self.v, self.pri = u, v, pri
        self.left = self.right = self.parent = None
        self.size = 1
        self.loops = 1 if u == v else 0
        self.nt = 0  # loop node: number of non-tree edges of this level at u
        self.tr = 0  # arc node: 1 if this tree edge has exactly this level
        self.snt = 0
        self.str_ = 0


def _upd(t: _Node) -> None:
    t.size, t.loops, t.snt, t.str_ = 1, (1 if t.u == t.v else 0), t.nt, t.tr
    for c in (t.left, t.right):
        if c:
            t.size += c.size
            t.loops += c.loops
            t.snt += c.snt
            t.str_ += c.str_


def _size(t) -> int:
    return t.size if t else 0


def _join(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if a.pri > b.pri:
        r = _join(a.right, b)
        a.right, r.parent = r, a
        _upd(a)
        a.parent = None
        return a
    l = _join(a, b.left)
    b.left, l.parent = l, b
    _upd(b)
    b.parent = None
    return b


def _split(t, k):
    if t is None:
        return None, None
    t.parent = None
    if _size(t.left) >= k:
        a, b = _split(t.left, k)
        t.left = b
        if b:
            b.parent = t
        _upd(t)
        return a, t
    a, b = _split(t.right, k - _size(t.left) - 1)
    t.right = a
    if a:
        a.parent = t
    _upd(t)
    return t, b


def _root(x: _Node) -> _Node:
    while x.parent:
        x = x.parent
    return x


def _pos(x: _Node) -> int:
    i = _size(x.left)
    while x.parent:
        p = x.parent
        if p.right is x:
            i += _size(p.left) + 1
        x = p
    return i


def _refresh(x: _Node) -> None:
    while x:
        _upd(x)
        x = x.parent


def _find(t, attr: str, agg: str):
    """A node of the treap t whose field attr is positive, or None."""
    if t is None or getattr(t, agg) == 0:
        return None
    while True:
        if t.left and getattr(t.left, agg) > 0:
            t = t.left
        elif getattr(t, attr) > 0:
            return t
        else:
            t = t.right


class _EulerForest:
    """Euler tour forest for one level, with counters for the search."""

    def __init__(self, n: int, rng: random.Random) -> None:
        self.rng = rng
        self.loop = [_Node(v, v, rng.random()) for v in range(n)]
        self.arc: dict[tuple[int, int], _Node] = {}

    def _reroot(self, v: int):
        x = self.loop[v]
        a, b = _split(_root(x), _pos(x))
        return _join(b, a)

    def connected(self, u: int, v: int) -> bool:
        return _root(self.loop[u]) is _root(self.loop[v])

    def size(self, v: int) -> int:
        return _root(self.loop[v]).loops

    def link(self, u: int, v: int, exact_level: bool) -> None:
        tu, tv = self._reroot(u), self._reroot(v)
        a, b = _Node(u, v, self.rng.random()), _Node(v, u, self.rng.random())
        a.tr = 1 if exact_level else 0
        _upd(a)
        self.arc[(u, v)], self.arc[(v, u)] = a, b
        _join(_join(_join(tu, a), tv), b)

    def cut(self, u: int, v: int) -> None:
        a, b = self.arc.pop((u, v)), self.arc.pop((v, u))
        if _pos(a) > _pos(b):
            a, b = b, a
        i, j = _pos(a), _pos(b)
        x, rest = _split(_root(a), i)
        _, rest = _split(rest, 1)
        _, rest = _split(rest, j - i - 1)
        _, z = _split(rest, 1)
        _join(x, z)

    def set_exact(self, u: int, v: int, flag: bool) -> None:
        a = self.arc[(u, v)] if (u, v) in self.arc else None
        if a is None:
            return
        b = self.arc[(v, u)]
        a.tr, b.tr = (1 if flag else 0), 0
        _refresh(a)
        _refresh(b)

    def add_nontree(self, v: int, d: int) -> None:
        self.loop[v].nt += d
        _refresh(self.loop[v])

    def find_tree_edge(self, v: int):
        x = _find(_root(self.loop[v]), "tr", "str_")
        return None if x is None else (x.u, x.v)

    def find_nontree_vertex(self, v: int):
        x = _find(_root(self.loop[v]), "nt", "snt")
        return None if x is None else x.u


class DynamicConnectivity:
    def __init__(self, n: int, seed: int = 1) -> None:
        self.n = n
        self.top = max(0, n.bit_length() - 1)  # floor(lg n)
        rng = random.Random(seed)
        self.F = [_EulerForest(n, rng) for _ in range(self.top + 1)]
        self.level: dict[tuple[int, int], int] = {}
        self.is_tree: dict[tuple[int, int], bool] = {}
        self.count: dict[tuple[int, int], int] = {}  # parallel copies
        # nontree[i][v]: set of other ends of non-tree edges of level i at v
        self.nontree = [[set() for _ in range(n)] for _ in range(self.top + 1)]

    @staticmethod
    def _key(u: int, v: int) -> tuple[int, int]:
        return (u, v) if u < v else (v, u)

    def connected(self, u: int, v: int) -> bool:
        return u == v or self.F[0].connected(u, v)  # @line L12

    def _add_nontree(self, e: tuple[int, int], i: int) -> None:
        u, v = e
        self.level[e] = i
        self.is_tree[e] = False
        self.nontree[i][u].add(v)
        self.nontree[i][v].add(u)
        self.F[i].add_nontree(u, 1)
        self.F[i].add_nontree(v, 1)

    def _remove_nontree(self, e: tuple[int, int]) -> None:
        u, v = e
        i = self.level[e]
        self.nontree[i][u].discard(v)
        self.nontree[i][v].discard(u)
        self.F[i].add_nontree(u, -1)
        self.F[i].add_nontree(v, -1)

    def _add_tree(self, e: tuple[int, int], i: int) -> None:
        u, v = e
        self.level[e] = i
        self.is_tree[e] = True
        for j in range(i + 1):
            self.F[j].link(u, v, j == i)

    def insert(self, u: int, v: int) -> None:
        if u == v:
            return
        e = self._key(u, v)
        self.count[e] = self.count.get(e, 0) + 1
        if self.count[e] > 1:
            return  # a parallel copy changes no connectivity
        if not self.F[0].connected(u, v):  # @line L1
            self._add_tree(e, 0)  # @line L2
        else:
            self._add_nontree(e, 0)

    def delete(self, u: int, v: int) -> None:
        if u == v:
            return
        e = self._key(u, v)
        self.count[e] -= 1
        if self.count[e] > 0:
            return
        del self.count[e]
        if not self.is_tree[e]:
            self._remove_nontree(e)  # @line L3
            del self.level[e], self.is_tree[e]
            return
        lev = self.level.pop(e)
        del self.is_tree[e]
        for j in range(lev + 1):
            self.F[j].cut(u, v)  # @line L4
        for i in range(lev, -1, -1):  # @line L5
            Fi = self.F[i]
            a, b = (u, v) if Fi.size(u) <= Fi.size(v) else (v, u)  # @line L6
            # Raise every level-i tree edge of the smaller tree to level i + 1.
            while True:
                t = Fi.find_tree_edge(a)
                if t is None:
                    break
                x, y = t
                f = self._key(x, y)
                Fi.set_exact(x, y, False)
                self.level[f] = i + 1  # @line L7
                self.F[i + 1].link(x, y, True)
            # Scan the level-i non-tree edges at the smaller tree.
            while True:
                x = Fi.find_nontree_vertex(a)
                if x is None:
                    break
                y = next(iter(self.nontree[i][x]))  # @line L8
                f = self._key(x, y)
                self._remove_nontree(f)
                if Fi.connected(y, b):  # @line L9
                    self._add_tree(f, i)
                    return
                self._add_nontree(f, i + 1)  # @line L10
        # @line L11: no replacement edge; the tree stays split.

    def check_invariants(self) -> None:
        """For tests: tree sizes at level i are at most n / 2^i."""
        for i, Fi in enumerate(self.F):
            for v in range(self.n):
                assert Fi.size(v) <= self.n >> i
