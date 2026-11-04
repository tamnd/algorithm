# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/banker-queue/. The authors are listed in prov/WBJ0ZE.jsonl.

from collections.abc import Callable, Iterator
from typing import Generic, Optional, TypeVar

T = TypeVar("T")

# A stream cell is None (the empty stream) or a pair (item, rest), where rest is a Susp.
Cell = Optional[tuple[T, "Susp[T]"]]


class Susp(Generic[T]):
    """A suspension: a computation of a stream cell that runs at most once.

    The first force runs the computation and stores the cell; later forces
    return the stored cell in O(1) time. This memoization is what makes the
    amortized bounds of the queue hold when old versions are reused.
    """

    __slots__ = ("_thunk", "_cell", "_done")

    def __init__(self, thunk: Callable[[], Cell[T]]) -> None:
        self._thunk: Callable[[], Cell[T]] | None = thunk
        self._cell: Cell[T] = None
        self._done = False

    @staticmethod
    def value(cell: Cell[T]) -> "Susp[T]":
        """A suspension that is already evaluated."""
        s: Susp[T] = Susp(lambda: cell)
        s.force()
        return s

    def force(self) -> Cell[T]:
        if not self._done:
            assert self._thunk is not None
            self._cell = self._thunk()
            self._done = True
            self._thunk = None
        return self._cell

    @property
    def evaluated(self) -> bool:
        return self._done


EMPTY_STREAM: Susp = Susp.value(None)


def append(f: Susp[T], g: Susp[T]) -> Susp[T]:
    """The lazy concatenation f ++ g: each cell is computed only when forced."""

    def step() -> Cell[T]:
        cell = f.force()
        if cell is None:
            return g.force()
        x, rest = cell
        return (x, append(rest, g))

    return Susp(step)


# The rear list is an immutable linked list: None, or a pair (item, rest), newest item first.
RList = Optional[tuple[T, "RList[T]"]]


def reverse(r: "RList[T]") -> Susp[T]:
    """A suspension of the reverse of the rear list r (newest item first).

    The whole reversal runs at the first force, in O(len(r)) time: it is a
    monolithic suspension. The cells it builds are already evaluated.
    """

    def run() -> Cell[T]:
        s: Susp[T] = EMPTY_STREAM
        node = r
        while node is not None:  # newest first, so the oldest item ends up in front
            x, node = node
            s = Susp.value((x, s))
        return s.force()

    return Susp(run)


class BankerQueue(Generic[T]):
    """Okasaki's banker's queue: a persistent FIFO queue.

    The fields are (lf, F, lr, R): a lazy stream F of length lf (the front, in
    queue order) and a rear list R of length lr (newest item first), with the
    invariant lr <= lf. snoc, head and tail take O(1) amortized time, also when
    any old version is reused, because the rebuild F ++ reverse(R) is a shared
    memoized suspension. One operation can take Theta(n) time. Every method
    returns a new queue and leaves self unchanged.
    """

    __slots__ = ("_lf", "_f", "_lr", "_r")

    def __init__(self) -> None:
        self._lf = 0  # @line L1
        self._f: Susp[T] = EMPTY_STREAM
        self._lr = 0
        self._r: RList[T] = None

    @classmethod
    def _make(cls, lf: int, f: Susp[T], lr: int, r: RList[T]) -> "BankerQueue[T]":
        q: BankerQueue[T] = cls.__new__(cls)
        q._lf, q._f, q._lr, q._r = lf, f, lr, r
        return q

    @classmethod
    def _check(cls, lf: int, f: Susp[T], lr: int, r: RList[T]) -> "BankerQueue[T]":
        if lr <= lf:  # @line L8
            return cls._make(lf, f, lr, r)
        return cls._make(lf + lr, append(f, reverse(r)), 0, None)  # @line L9

    def is_empty(self) -> bool:
        return self._lf == 0

    def __len__(self) -> int:
        return self._lf + self._lr

    def snoc(self, x: T) -> "BankerQueue[T]":
        """Return the queue with x added at the rear."""
        lf, f, lr, r = self._lf, self._f, self._lr, self._r  # @line L2
        return self._check(lf, f, lr + 1, (x, r))  # @line L3

    def head(self) -> T:
        """Return the front item. Raises IndexError on an empty queue."""
        if self._lf == 0:  # @line L4
            raise IndexError("head of an empty queue")
        cell = self._f.force()  # @line L5
        assert cell is not None
        return cell[0]

    def tail(self) -> "BankerQueue[T]":
        """Return the queue without its front item. Raises IndexError on an empty queue."""
        if self._lf == 0:  # @line L6
            raise IndexError("tail of an empty queue")
        cell = self._f.force()
        assert cell is not None
        return self._check(self._lf - 1, cell[1], self._lr, self._r)  # @line L7

    def __iter__(self) -> Iterator[T]:
        q = self
        while not q.is_empty():
            yield q.head()
            q = q.tail()

    def to_list(self) -> list[T]:
        return list(self)

    def lengths(self) -> tuple[int, int]:
        """The pair (lf, lr), for tests and for the trace of the page."""
        return self._lf, self._lr

    def check_invariant(self) -> None:
        """Check lr <= lf, that F has lf cells and that R has lr items. Forces F."""
        assert 0 <= self._lr <= self._lf
        k, node = 0, self._r
        while node is not None:
            k, node = k + 1, node[1]
        assert k == self._lr
        n, s = 0, self._f
        while (cell := s.force()) is not None:
            n += 1
            s = cell[1]
        assert n == self._lf
