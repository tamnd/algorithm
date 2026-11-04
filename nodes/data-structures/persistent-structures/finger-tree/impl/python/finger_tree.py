# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finger-tree/. The authors are listed in prov/BJ50ZK.jsonl.

"""A 2-3 finger tree (Hinze and Paterson) measured by size.

This version is strict: the middle tree is built at once, not suspended.
Each operation returns a new tree and never changes an old one.
"""

from collections.abc import Iterator
from typing import Any, Generic, Optional, TypeVar, Union

T = TypeVar("T")


class _Node:
    """A 2-3 node whose children are items (level 0) or nodes of one level less."""

    __slots__ = ("size", "items")

    def __init__(self, items: tuple[Any, ...]) -> None:
        self.items = items
        self.size = sum(_sz(x) for x in items)


def _sz(x: Any) -> int:
    return x.size if isinstance(x, _Node) else 1


def _dsz(xs: tuple[Any, ...]) -> int:
    return sum(_sz(x) for x in xs)


class _Empty:
    __slots__ = ()
    size = 0


class _Single:
    __slots__ = ("x", "size")

    def __init__(self, x: Any) -> None:
        self.x = x
        self.size = _sz(x)


class _Deep:
    __slots__ = ("size", "pr", "m", "sf")

    def __init__(self, pr: tuple[Any, ...], m: "_Tree", sf: tuple[Any, ...]) -> None:
        self.pr, self.m, self.sf = pr, m, sf
        self.size = _dsz(pr) + m.size + _dsz(sf)


_Tree = Union[_Empty, _Single, _Deep]
EMPTY = _Empty()


def _cons(a: Any, t: _Tree) -> _Tree:
    if isinstance(t, _Empty):  # @line L1
        return _Single(a)
    if isinstance(t, _Single):  # @line L2
        return _Deep((a,), EMPTY, (t.x,))
    pr, m, sf = t.pr, t.m, t.sf  # @line L3
    if len(pr) == 4:  # @line L4
        b, c, d, e = pr
        return _Deep((a, b), _cons(_Node((c, d, e)), m), sf)
    return _Deep((a,) + pr, m, sf)  # @line L5


def _snoc(t: _Tree, a: Any) -> _Tree:
    if isinstance(t, _Empty):
        return _Single(a)
    if isinstance(t, _Single):
        return _Deep((t.x,), EMPTY, (a,))
    pr, m, sf = t.pr, t.m, t.sf
    if len(sf) == 4:
        e, d, c, b = sf
        return _Deep(pr, _snoc(m, _Node((e, d, c))), (b, a))
    return _Deep(pr, m, sf + (a,))


def _cons_all(xs: tuple[Any, ...], t: _Tree) -> _Tree:
    for x in reversed(xs):  # @line L6
        t = _cons(x, t)
    return t


def _snoc_all(t: _Tree, xs: tuple[Any, ...]) -> _Tree:
    for x in xs:  # @line L7
        t = _snoc(t, x)
    return t


def _tree_of(xs: tuple[Any, ...]) -> _Tree:
    return _cons_all(xs, EMPTY)  # @line L8


def _viewl(t: _Tree) -> Optional[tuple[Any, _Tree]]:
    if isinstance(t, _Empty):  # @line L9
        return None
    if isinstance(t, _Single):  # @line L10
        return (t.x, EMPTY)
    a = t.pr[0]  # @line L11
    return (a, _deepl(t.pr[1:], t.m, t.sf))  # @line L12


def _viewr(t: _Tree) -> Optional[tuple[_Tree, Any]]:
    if isinstance(t, _Empty):
        return None
    if isinstance(t, _Single):
        return (EMPTY, t.x)
    a = t.sf[-1]
    return (_deepr(t.pr, t.m, t.sf[:-1]), a)


def _deepl(pr: tuple[Any, ...], m: _Tree, sf: tuple[Any, ...]) -> _Tree:
    if pr:  # @line L13
        return _Deep(pr, m, sf)
    v = _viewl(m)  # @line L14
    if v is None:
        return _tree_of(sf)
    node, m2 = v  # @line L15
    return _Deep(node.items, m2, sf)


def _deepr(pr: tuple[Any, ...], m: _Tree, sf: tuple[Any, ...]) -> _Tree:
    if sf:
        return _Deep(pr, m, sf)
    v = _viewr(m)
    if v is None:
        return _tree_of(pr)
    m2, node = v
    return _Deep(pr, m2, node.items)


def _nodes(xs: tuple[Any, ...]) -> tuple[_Node, ...]:
    n = len(xs)
    if n == 2:  # @line L16
        return (_Node(xs),)
    if n == 3:  # @line L17
        return (_Node(xs),)
    if n == 4:  # @line L18
        return (_Node(xs[:2]), _Node(xs[2:]))
    return (_Node(xs[:3]),) + _nodes(xs[3:])  # @line L19


def _app3(t1: _Tree, ts: tuple[Any, ...], t2: _Tree) -> _Tree:
    if isinstance(t1, _Empty):  # @line L20
        return _cons_all(ts, t2)
    if isinstance(t2, _Empty):  # @line L21
        return _snoc_all(t1, ts)
    if isinstance(t1, _Single):  # @line L22
        return _cons(t1.x, _cons_all(ts, t2))
    if isinstance(t2, _Single):  # @line L23
        return _snoc(_snoc_all(t1, ts), t2.x)
    mid = _app3(t1.m, _nodes(t1.sf + ts + t2.pr), t2.m)  # @line L24
    return _Deep(t1.pr, mid, t2.sf)


def _locate(i: int, xs: tuple[Any, ...]) -> tuple[int, int]:
    """For 0 <= i < size(xs): (k, j) with position i at offset j inside xs[k]."""
    for k, x in enumerate(xs):  # @line L25
        s = _sz(x)
        if i < s:
            return (k, i)
        i -= s
    raise IndexError("index outside the digit")


def _split_digit(i: int, xs: tuple[Any, ...]) -> tuple[tuple[Any, ...], Any, tuple[Any, ...]]:
    k, _ = _locate(i, xs)
    return (xs[:k], xs[k], xs[k + 1 :])


def _split_tree(i: int, t: _Tree) -> tuple[_Tree, Any, _Tree]:
    """For 0 <= i < size(t): (l, x, r) with x the element that holds position i."""
    if isinstance(t, _Single):  # @line L26
        return (EMPTY, t.x, EMPTY)
    assert isinstance(t, _Deep)
    spr = _dsz(t.pr)
    if i < spr:  # @line L27
        l, x, r = _split_digit(i, t.pr)
        return (_tree_of(l), x, _deepl(r, t.m, t.sf))
    i -= spr  # @line L28
    if i < t.m.size:
        ml, xs, mr = _split_tree(i, t.m)
        l, x, r = _split_digit(i - ml.size, xs.items)
        return (_deepr(t.pr, ml, l), x, _deepl(r, mr, t.sf))
    l, x, r = _split_digit(i - t.m.size, t.sf)  # @line L29
    return (_deepr(t.pr, t.m, l), x, _tree_of(r))


def _lookup(i: int, t: _Tree) -> Any:
    """For 0 <= i < size(t): the item at position i."""
    while isinstance(t, _Deep) and _dsz(t.pr) <= i < _dsz(t.pr) + t.m.size:  # @line L30
        i, t = i - _dsz(t.pr), t.m  # @line L31
    if isinstance(t, _Single):  # @line L32
        xs: tuple[Any, ...] = (t.x,)
    else:
        assert isinstance(t, _Deep)
        xs = t.pr + t.sf  # @line L33
        if i >= _dsz(t.pr):
            i -= t.m.size
    while True:
        k, i = _locate(i, xs)  # @line L34
        if not isinstance(xs[k], _Node):
            return xs[k]
        xs = xs[k].items


def _iter(t: _Tree) -> Iterator[Any]:
    def elem(x: Any) -> Iterator[Any]:
        if isinstance(x, _Node):
            for c in x.items:
                yield from elem(c)
        else:
            yield x

    if isinstance(t, _Single):
        yield from elem(t.x)
    elif isinstance(t, _Deep):
        for x in t.pr:
            yield from elem(x)
        for x in _iter(t.m):
            yield from elem(x)
        for x in t.sf:
            yield from elem(x)


def _check_elem(x: Any, level: int) -> int:
    if level == 0:
        assert not isinstance(x, _Node), "an item expected at level 0"
        return 1
    assert isinstance(x, _Node), "a node expected above level 0"
    assert len(x.items) in (2, 3), "a node has 2 or 3 children"
    s = sum(_check_elem(c, level - 1) for c in x.items)
    assert s == x.size, "cached node size"
    return s


def _check_tree(t: _Tree, level: int) -> int:
    if isinstance(t, _Empty):
        return 0
    if isinstance(t, _Single):
        s = _check_elem(t.x, level)
    else:
        assert 1 <= len(t.pr) <= 4 and 1 <= len(t.sf) <= 4, "digits have 1 to 4 elements"
        s = sum(_check_elem(x, level) for x in t.pr)
        s += _check_tree(t.m, level + 1)
        s += sum(_check_elem(x, level) for x in t.sf)
    assert s == t.size, "cached tree size"
    return s


class FingerTree(Generic[T]):
    """A persistent sequence. Every method returns new trees; self never changes."""

    __slots__ = ("_t",)

    def __init__(self, _t: _Tree = EMPTY) -> None:
        self._t = _t

    def __len__(self) -> int:
        return self._t.size

    def __iter__(self) -> Iterator[T]:
        return _iter(self._t)

    def to_list(self) -> list[T]:
        return list(_iter(self._t))

    @classmethod
    def from_iterable(cls, xs: "list[T]") -> "FingerTree[T]":
        t: _Tree = EMPTY
        for x in xs:
            t = _snoc(t, x)
        return cls(t)

    def cons(self, x: T) -> "FingerTree[T]":
        return FingerTree(_cons(x, self._t))

    def snoc(self, x: T) -> "FingerTree[T]":
        return FingerTree(_snoc(self._t, x))

    def viewl(self) -> "Optional[tuple[T, FingerTree[T]]]":
        v = _viewl(self._t)
        return None if v is None else (v[0], FingerTree(v[1]))

    def viewr(self) -> "Optional[tuple[FingerTree[T], T]]":
        v = _viewr(self._t)
        return None if v is None else (FingerTree(v[0]), v[1])

    def head(self) -> T:
        v = _viewl(self._t)
        if v is None:
            raise IndexError("head of an empty finger tree")
        return v[0]

    def last(self) -> T:
        v = _viewr(self._t)
        if v is None:
            raise IndexError("last of an empty finger tree")
        return v[1]

    def append(self, other: "FingerTree[T]") -> "FingerTree[T]":
        return FingerTree(_app3(self._t, (), other._t))

    def split_at(self, i: int) -> "tuple[FingerTree[T], FingerTree[T]]":
        """The first i items and the rest."""
        if i <= 0:
            return (FingerTree(EMPTY), self)
        if i >= self._t.size:
            return (self, FingerTree(EMPTY))
        l, x, r = _split_tree(i, self._t)
        return (FingerTree(l), FingerTree(_cons(x, r)))

    def lookup(self, i: int) -> T:
        if not 0 <= i < self._t.size:
            raise IndexError("finger tree index out of range")
        return _lookup(i, self._t)

    def depth(self) -> int:
        d, t = 0, self._t
        while isinstance(t, _Deep):
            d, t = d + 1, t.m
        return d

    def check_invariant(self) -> None:
        _check_tree(self._t, 0)
