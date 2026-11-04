# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/real-time-queue/. The authors are listed in prov/X9W66J.jsonl.

"""Okasaki's real-time queue: a persistent FIFO queue with O(1) worst case.

The queue is a lazy front stream f, a rear list r and a schedule s, which
is a suffix of f that has not been evaluated yet. Invariant: |s| = |f| - |r|.
Each push and pop forces one cell of s, so the rotation f ++ reverse(r) is
evaluated one step at a time, and no operation does more than O(1) work.
Memoized suspensions make this hold even when an old version is reused.
"""

from typing import Callable, Generic, Iterator, Optional, Tuple, TypeVar

T = TypeVar("T")

# Number of suspended steps evaluated so far, for tests of the O(1) bound.
STEPS = 0


class _Stream(Generic[T]):
    """A memoized lazy list: forcing gives None (empty) or (head, tail)."""

    __slots__ = ("_thunk", "_cell", "_done")

    def __init__(self, thunk: "Optional[Callable[[], Optional[Tuple[T, _Stream[T]]]]]" = None) -> None:
        self._thunk = thunk
        self._cell: "Optional[Tuple[T, _Stream[T]]]" = None
        self._done = thunk is None

    def force(self) -> "Optional[Tuple[T, _Stream[T]]]":
        if not self._done:
            global STEPS
            STEPS += 1
            assert self._thunk is not None
            self._cell = self._thunk()
            self._thunk = None
            self._done = True
        return self._cell

    def is_forced(self) -> bool:
        return self._done


_EMPTY: "_Stream[object]" = _Stream()


class _Cons(Generic[T]):
    """An immutable cell of the rear list."""

    __slots__ = ("head", "next")

    def __init__(self, head: T, next: "Optional[_Cons[T]]") -> None:
        self.head = head
        self.next = next


def _evaluated(head: T, tail: "_Stream[T]") -> "_Stream[T]":
    s: _Stream[T] = _Stream()
    s._cell = (head, tail)
    return s


def _rotate(f: "_Stream[T]", r: "_Cons[T]", a: "_Stream[T]") -> "_Stream[T]":
    """The stream f ++ reverse(r) ++ a, built lazily; needs |r| = |f| + 1."""

    def step() -> "Optional[Tuple[T, _Stream[T]]]":
        cell = f.force()  # @line L1
        if cell is None:
            return (r.head, a)
        assert r.next is not None
        return (cell[0], _rotate(cell[1], r.next, _evaluated(r.head, a)))

    return _Stream(step)


class RealTimeQueue(Generic[T]):
    """An immutable FIFO queue. Every operation is O(1) in the worst case."""

    __slots__ = ("_f", "_r", "_s", "_lenf", "_lenr", "_lens")

    def __init__(self) -> None:
        """The empty queue. Cost: O(1)."""
        self._f: _Stream[T] = _EMPTY  # type: ignore[assignment]
        self._r: Optional[_Cons[T]] = None
        self._s: _Stream[T] = _EMPTY  # type: ignore[assignment]
        self._lenf = 0
        self._lenr = 0
        self._lens = 0

    @staticmethod
    def _exec(
        f: "_Stream[T]", lenf: int, r: "Optional[_Cons[T]]", lenr: int, s: "_Stream[T]", lens: int
    ) -> "RealTimeQueue[T]":
        q: RealTimeQueue[T] = RealTimeQueue.__new__(RealTimeQueue)
        cell = s.force()
        if cell is not None:  # @line L2
            q._f, q._r, q._s = f, r, cell[1]
            q._lenf, q._lenr, q._lens = lenf, lenr, lens - 1
            return q
        assert r is not None
        f2 = _rotate(f, r, _EMPTY)  # type: ignore[arg-type]  # @line L3
        q._f, q._r, q._s = f2, None, f2
        q._lenf, q._lenr, q._lens = lenf + lenr, 0, lenf + lenr
        return q

    def __len__(self) -> int:
        """Number of items. Cost: O(1)."""
        return self._lenf + self._lenr

    def is_empty(self) -> bool:
        """Whether the queue is empty. Cost: O(1)."""
        return self._lenf == 0

    def push(self, x: T) -> "RealTimeQueue[T]":
        """The queue with x added at the back. Cost: O(1) worst case."""
        return RealTimeQueue._exec(  # @line L4
            self._f, self._lenf, _Cons(x, self._r), self._lenr + 1, self._s, self._lens
        )

    def front(self) -> T:
        """The item at the front. Cost: O(1) worst case."""
        cell = self._f.force()
        if cell is None:  # @line L5
            raise IndexError("front of empty queue")
        return cell[0]

    def pop(self) -> "Tuple[T, RealTimeQueue[T]]":
        """The front item and the queue without it. Cost: O(1) worst case."""
        cell = self._f.force()
        if cell is None:  # @line L6
            raise IndexError("pop from empty queue")
        rest = RealTimeQueue._exec(  # @line L7
            cell[1], self._lenf - 1, self._r, self._lenr, self._s, self._lens
        )
        return cell[0], rest

    def __iter__(self) -> Iterator[T]:
        """Items from front to back, by repeated pop. Cost: Θ(n)."""
        q = self
        while not q.is_empty():
            x, q = q.pop()
            yield x

    def check_invariant(self) -> None:
        """Check |s| = |f| - |r|, that s is the unevaluated suffix of f, and |r|.

        The first |f| - |s| cells of f must be evaluated, and the stream after
        them must be s itself. Walks only evaluated cells. Cost: Θ(n).
        """
        assert self._lens == self._lenf - self._lenr >= 0
        n = 0
        c = self._r
        while c is not None:
            n += 1
            c = c.next
        assert n == self._lenr
        st = self._f
        for _ in range(self._lenf - self._lens):
            assert st.is_forced()
            cell = st.force()
            assert cell is not None
            st = cell[1]
        assert st is self._s
