# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/catenable-deque/. The authors are listed in prov/776W85.jsonl.

"""A persistent catenable deque in the style of Okasaki's simple c-deque.

A c-deque is Shallow(d) with 0 to 4 elements, or Deep(f, m, r) where the
front f and the rear r hold 2 to 4 elements and the middle m is a c-deque
whose elements are tuples of 2 or 3 elements of the level above.  This
version is strict: the middle is built at once, not suspended.  Each
operation returns a new deque and never changes an old one.
"""

from collections.abc import Iterable, Iterator
from typing import Any, Generic, TypeVar, Union

T = TypeVar("T")


class _Shallow:
    __slots__ = ("d",)

    def __init__(self, d: tuple[Any, ...]) -> None:
        self.d = d


class _Deep:
    __slots__ = ("f", "m", "r")

    def __init__(self, f: tuple[Any, ...], m: "_CD", r: tuple[Any, ...]) -> None:
        self.f = f
        self.m = m
        self.r = r


_CD = Union[_Shallow, _Deep]
_EMPTY = _Shallow(())


def _is_empty(q: _CD) -> bool:
    return isinstance(q, _Shallow) and not q.d


def _from_seq(s: tuple[Any, ...]) -> _CD:
    """A c-deque of at most 8 elements."""
    if len(s) <= 4:
        return _Shallow(s)
    h = len(s) // 2
    return _Deep(s[:h], _EMPTY, s[h:])


def _cons(x: Any, q: _CD) -> _CD:
    if isinstance(q, _Shallow) and len(q.d) < 4:  # @line L1
        return _Shallow((x,) + q.d)
    if isinstance(q, _Shallow):  # @line L2
        a, b, c, d = q.d
        return _Deep((x, a), _EMPTY, (b, c, d))
    f, m, r = q.f, q.m, q.r  # @line L3
    if len(f) < 4:  # @line L4
        return _Deep((x,) + f, m, r)
    a, b, c, d = f  # @line L5
    return _Deep((x, a), _cons((b, c, d), m), r)  # @line L6


def _snoc(q: _CD, x: Any) -> _CD:
    if isinstance(q, _Shallow) and len(q.d) < 4:
        return _Shallow(q.d + (x,))
    if isinstance(q, _Shallow):
        a, b, c, d = q.d
        return _Deep((a, b, c), _EMPTY, (d, x))
    f, m, r = q.f, q.m, q.r
    if len(r) < 4:
        return _Deep(f, m, r + (x,))
    a, b, c, d = r
    return _Deep(f, _snoc(m, (a, b, c)), (d, x))


def _head(q: _CD) -> Any:
    return q.d[0] if isinstance(q, _Shallow) else q.f[0]


def _last(q: _CD) -> Any:
    return q.d[-1] if isinstance(q, _Shallow) else q.r[-1]


def _tail(q: _CD) -> _CD:
    if isinstance(q, _Shallow):  # @line L7
        return _Shallow(q.d[1:])
    f, m, r = q.f, q.m, q.r  # @line L8
    if len(f) > 2:  # @line L9
        return _Deep(f[1:], m, r)
    b = f[1]  # @line L10
    if not _is_empty(m):  # @line L11
        return _Deep((b,) + _head(m), _tail(m), r)
    s = (b,) + r  # @line L12
    if len(s) <= 4:  # @line L13
        return _Shallow(s)
    return _Deep(s[:2], _EMPTY, s[2:])  # @line L14


def _init(q: _CD) -> _CD:
    if isinstance(q, _Shallow):
        return _Shallow(q.d[:-1])
    f, m, r = q.f, q.m, q.r
    if len(r) > 2:
        return _Deep(f, m, r[:-1])
    b = r[0]
    if not _is_empty(m):
        return _Deep(f, _init(m), _last(m) + (b,))
    s = f + (b,)
    if len(s) <= 4:
        return _Shallow(s)
    return _Deep(s[:3], _EMPTY, s[3:])


def _push_front(d: tuple[Any, ...], m: _CD) -> _CD:
    if len(d) <= 3:  # @line L15
        return _cons(d, m)
    return _cons(d[:2], _cons(d[2:], m))  # @line L16


def _push_back(m: _CD, d: tuple[Any, ...]) -> _CD:
    if len(d) <= 3:
        return _snoc(m, d)
    return _snoc(_snoc(m, d[:2]), d[2:])


def _cat(q1: _CD, q2: _CD) -> _CD:
    if isinstance(q1, _Shallow) and isinstance(q2, _Shallow):  # @line L17
        return _from_seq(q1.d + q2.d)
    if isinstance(q1, _Shallow):  # @line L18
        assert isinstance(q2, _Deep)
        if len(q1.d) <= 1:  # @line L19
            return _cons(q1.d[0], q2) if q1.d else q2
        return _Deep(q1.d, _push_front(q2.f, q2.m), q2.r)  # @line L20
    if isinstance(q2, _Shallow):  # @line L21
        if len(q2.d) <= 1:  # @line L22
            return _snoc(q1, q2.d[0]) if q2.d else q1
        return _Deep(q1.f, _push_back(q1.m, q1.r), q2.d)  # @line L23
    m = _cat(_push_back(q1.m, q1.r), _push_front(q2.f, q2.m))  # @line L24
    return _Deep(q1.f, m, q2.r)


def _items(x: Any, level: int) -> Iterator[Any]:
    if level == 0:
        yield x
    else:
        for y in x:
            yield from _items(y, level - 1)


def _walk(q: _CD, level: int) -> Iterator[Any]:
    if isinstance(q, _Shallow):
        for x in q.d:
            yield from _items(x, level)
        return
    for x in q.f:
        yield from _items(x, level)
    yield from _walk(q.m, level + 1)
    for x in q.r:
        yield from _items(x, level)


def _check(q: _CD, level: int) -> int:
    """Check the invariant and return the number of items below q."""

    def elem(x: Any, lv: int) -> int:
        if lv == 0:
            return 1
        assert isinstance(x, tuple) and 2 <= len(x) <= 3
        return sum(elem(y, lv - 1) for y in x)

    if isinstance(q, _Shallow):
        assert len(q.d) <= 4
        return sum(elem(x, level) for x in q.d)
    assert isinstance(q, _Deep)
    assert 2 <= len(q.f) <= 4 and 2 <= len(q.r) <= 4
    return (
        sum(elem(x, level) for x in q.f)
        + _check(q.m, level + 1)
        + sum(elem(x, level) for x in q.r)
    )


def _depth(q: _CD) -> int:
    k = 0
    while isinstance(q, _Deep):
        q = q.m
        k += 1
    return k


class CatenableDeque(Generic[T]):
    """An immutable catenable deque. Every method returns a new deque."""

    __slots__ = ("_q", "_n")

    def __init__(self, _q: _CD = _EMPTY, _n: int = 0) -> None:
        self._q = _q
        self._n = _n

    @classmethod
    def from_iterable(cls, xs: Iterable[T]) -> "CatenableDeque[T]":
        q: CatenableDeque[T] = cls()
        for x in xs:
            q = q.snoc(x)
        return q

    def __len__(self) -> int:
        return self._n

    def is_empty(self) -> bool:
        return self._n == 0

    def cons(self, x: T) -> "CatenableDeque[T]":
        return CatenableDeque(_cons(x, self._q), self._n + 1)

    def snoc(self, x: T) -> "CatenableDeque[T]":
        return CatenableDeque(_snoc(self._q, x), self._n + 1)

    def head(self) -> T:
        if self._n == 0:
            raise IndexError("head of an empty deque")
        return _head(self._q)

    def last(self) -> T:
        if self._n == 0:
            raise IndexError("last of an empty deque")
        return _last(self._q)

    def tail(self) -> "CatenableDeque[T]":
        if self._n == 0:
            raise IndexError("tail of an empty deque")
        return CatenableDeque(_tail(self._q), self._n - 1)

    def init(self) -> "CatenableDeque[T]":
        if self._n == 0:
            raise IndexError("init of an empty deque")
        return CatenableDeque(_init(self._q), self._n - 1)

    def concat(self, other: "CatenableDeque[T]") -> "CatenableDeque[T]":
        return CatenableDeque(_cat(self._q, other._q), self._n + other._n)

    def __add__(self, other: "CatenableDeque[T]") -> "CatenableDeque[T]":
        return self.concat(other)

    def __iter__(self) -> Iterator[T]:
        return _walk(self._q, 0)

    def to_list(self) -> list[T]:
        return list(self)

    def depth(self) -> int:
        """The number of Deep levels on the spine."""
        return _depth(self._q)

    def check_invariant(self) -> None:
        assert _check(self._q, 0) == self._n
