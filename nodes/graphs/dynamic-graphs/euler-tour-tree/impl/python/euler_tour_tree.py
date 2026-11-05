# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-tour-tree/. The authors are listed in prov/TH5ZDM.jsonl.

"""Euler tour trees: a dynamic forest stored as Euler tours in treaps.

Each vertex v has a loop node (v, v), and each tree edge {u, v} has two arc
nodes (u, v) and (v, u). The nodes of one tree, in the order of an Euler tour
of that tree, form one treap ordered by position. Supports link, cut,
connected, reroot, component aggregates and subtree aggregates in O(log n)
expected time per operation. The structure is fully dynamic for forests and
deterministic except for the random treap priorities.
"""

import random


class _Node:
    __slots__ = ("pri", "left", "right", "parent", "size", "loops", "val", "agg", "u", "v")

    def __init__(self, u: int, v: int, pri: float, val: int = 0) -> None:
        self.u, self.v = u, v
        self.pri = pri
        self.left: "_Node | None" = None
        self.right: "_Node | None" = None
        self.parent: "_Node | None" = None
        self.val = val
        self.loops = 1 if u == v else 0
        self.size = 1
        self.agg = val


def _size(t: "_Node | None") -> int:
    return t.size if t else 0


def _update(t: _Node) -> None:
    t.size, t.loops, t.agg = 1, (1 if t.u == t.v else 0), t.val
    for c in (t.left, t.right):
        if c:
            t.size += c.size
            t.loops += c.loops
            t.agg += c.agg


def _join(a: "_Node | None", b: "_Node | None") -> "_Node | None":
    """Concatenate two treaps (all of a before all of b). Depth O(log n) expected."""
    if a is None:
        return b
    if b is None:
        return a
    if a.pri > b.pri:
        r = _join(a.right, b)
        a.right = r
        r.parent = a
        _update(a)
        a.parent = None
        return a
    l = _join(a, b.left)
    b.left = l
    l.parent = b
    _update(b)
    b.parent = None
    return b


def _split(t: "_Node | None", k: int) -> "tuple[_Node | None, _Node | None]":
    """Split t into its first k nodes and the rest."""
    if t is None:
        return None, None
    t.parent = None
    if _size(t.left) >= k:
        a, b = _split(t.left, k)
        t.left = b
        if b:
            b.parent = t
        _update(t)
        return a, t
    a, b = _split(t.right, k - _size(t.left) - 1)
    t.right = a
    if a:
        a.parent = t
    _update(t)
    return t, b


def _root(x: _Node) -> _Node:
    while x.parent:
        x = x.parent
    return x


def _pos(x: _Node) -> int:
    """Index of x in its sequence."""
    i = _size(x.left)
    while x.parent:
        p = x.parent
        if p.right is x:
            i += _size(p.left) + 1
        x = p
    return i


def _sum_prefix(t: "_Node | None", k: int) -> int:
    """Sum of the values of the first k nodes of t, without changing t."""
    s = 0
    while t and k > 0:
        if _size(t.left) >= k:
            t = t.left
            continue
        s += (t.left.agg if t.left else 0) + t.val
        k -= _size(t.left) + 1
        t = t.right
    return s


class EulerTourForest:
    """A forest on vertices 0 .. n-1, with an integer value on each vertex."""

    def __init__(self, n: int, values: "list[int] | None" = None, seed: int = 1) -> None:
        self._rng = random.Random(seed)
        vals = values if values is not None else [0] * n
        self._loop = [_Node(v, v, self._rng.random(), vals[v]) for v in range(n)]
        self._arc: dict[tuple[int, int], _Node] = {}

    def reroot(self, v: int) -> _Node:
        """Rotate the tour of v's tree so that it starts at the loop node of v."""
        x = self._loop[v]
        a, b = _split(_root(x), _pos(x))  # @line L1
        return _join(b, a)  # @line L2

    def connected(self, u: int, v: int) -> bool:
        return _root(self._loop[u]) is _root(self._loop[v])  # @line L3

    def link(self, u: int, v: int) -> None:
        """Add the edge {u, v}. Precondition: u and v are in different trees."""
        if self.connected(u, v):
            raise ValueError("u and v are already connected")
        tu = self.reroot(u)  # @line L4
        tv = self.reroot(v)
        a = _Node(u, v, self._rng.random())  # @line L5
        b = _Node(v, u, self._rng.random())
        self._arc[(u, v)], self._arc[(v, u)] = a, b
        _join(_join(_join(tu, a), tv), b)  # @line L6

    def cut(self, u: int, v: int) -> None:
        """Remove the tree edge {u, v}. Precondition: it is an edge of the forest."""
        a = self._arc.pop((u, v))  # @line L7
        b = self._arc.pop((v, u))
        if _pos(a) > _pos(b):  # @line L8
            a, b = b, a
        r = _root(a)
        i, j = _pos(a), _pos(b)
        x, rest = _split(r, i)  # @line L9
        _, rest = _split(rest, 1)
        y, rest = _split(rest, j - i - 1)
        _, z = _split(rest, 1)
        _join(x, z)  # @line L10

    def component_size(self, v: int) -> int:
        return _root(self._loop[v]).loops  # @line L11

    def component_sum(self, v: int) -> int:
        return _root(self._loop[v]).agg

    def set_value(self, v: int, x: int) -> None:
        t: "_Node | None" = self._loop[v]
        t.val = x
        while t:
            _update(t)
            t = t.parent

    def subtree_sum(self, v: int, p: int) -> int:
        """Sum of the values on v's side of the tree edge {p, v}."""
        a, b = self._arc[(p, v)], self._arc[(v, p)]  # @line L12
        r = _root(a)
        i, j = _pos(a), _pos(b)
        if i < j:  # @line L13
            return _sum_prefix(r, j) - _sum_prefix(r, i + 1)
        return r.agg - (_sum_prefix(r, i) - _sum_prefix(r, j + 1))  # @line L14

    def tour(self, v: int) -> list[tuple[int, int]]:
        """The nodes of v's tree in tour order, as (u, v) pairs. Iterative in-order walk."""
        out, stack, t = [], [], _root(self._loop[v])
        while stack or t:
            while t:
                stack.append(t)
                t = t.left
            t = stack.pop()
            out.append((t.u, t.v))
            t = t.right
        return out
