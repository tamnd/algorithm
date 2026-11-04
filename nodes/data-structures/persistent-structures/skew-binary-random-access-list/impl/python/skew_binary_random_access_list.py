# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skew-binary-random-access-list/. The authors are listed in prov/RA7KJS.jsonl.

"""Okasaki's skew binary random-access list.

A version is a linked list of cells (weight, tree, rest). Each tree is a
complete binary tree of weight 2^k - 1 that stores its items in preorder.
The weights grow along the list, except that the first two may be equal;
they are the digits of n in skew binary. Nodes are tuples (x, left, right),
with None children for a leaf. Nothing is mutated, so every version stays
valid, and an update copies only one path and one prefix of the list.
"""

from typing import Any, Iterable, Iterator, List, Optional, Tuple

Tree = Tuple[Any, Any, Any]
Cells = Optional[Tuple[int, Tree, Any]]


class SkewList:
    """An immutable random-access list."""

    __slots__ = ("_cells", "_n")

    def __init__(self, _cells: Cells = None, _n: int = 0) -> None:
        """The empty list (use the methods to build others). Cost: O(1)."""
        self._cells = _cells
        self._n = _n

    @staticmethod
    def from_iterable(items: Iterable[Any]) -> "SkewList":
        """A list with the given items in order. Cost: Θ(n)."""
        xs = list(items)
        s = SkewList()
        for x in reversed(xs):
            s = s.cons(x)
        return s

    def __len__(self) -> int:
        """Number of items. Cost: O(1)."""
        return self._n

    def is_empty(self) -> bool:
        """Whether the list is empty. Cost: O(1)."""
        return self._cells is None

    def cons(self, x: Any) -> "SkewList":
        """A new list with x in front. Cost: Θ(1) worst case."""
        c = self._cells
        if c is not None and c[2] is not None and c[0] == c[2][0]:  # @line L1
            w1, t1, (w2, t2, rest) = c
            return SkewList((1 + w1 + w2, (x, t1, t2), rest), self._n + 1)  # @line L2
        return SkewList((1, (x, None, None), c), self._n + 1)  # @line L3

    def head(self) -> Any:
        """The first item. Cost: Θ(1)."""
        if self._cells is None:
            raise IndexError("head of an empty list")
        return self._cells[1][0]  # @line L4

    def tail(self) -> "SkewList":
        """The list without its first item. Cost: Θ(1) worst case."""
        if self._cells is None:
            raise IndexError("tail of an empty list")
        w, t, rest = self._cells  # @line L5
        if w == 1:  # @line L6
            return SkewList(rest, self._n - 1)
        h = w // 2  # @line L7
        return SkewList((h, t[1], (h, t[2], rest)), self._n - 1)

    def _find(self, i: int) -> Tuple[List[Tuple[int, Tree]], int, Tree, int, Cells]:
        if not 0 <= i < self._n:
            raise IndexError("index out of range")
        before: List[Tuple[int, Tree]] = []
        c = self._cells
        assert c is not None
        while i >= c[0]:  # @line L8
            before.append((c[0], c[1]))
            i -= c[0]
            c = c[2]
            assert c is not None
        w, t, rest = c  # @line L9
        return before, w, t, i, rest

    def __getitem__(self, i: int) -> Any:
        """Item i. Cost: O(min(i, log n))."""
        _, w, t, i, _ = self._find(i)
        while i != 0:  # @line L10
            w //= 2  # @line L11
            if i <= w:  # @line L12
                t, i = t[1], i - 1
            else:
                t, i = t[2], i - 1 - w
        return t[0]  # @line L13

    def update(self, i: int, y: Any) -> "SkewList":
        """A new list with item i set to y. Cost: O(min(i, log n))."""
        before, w, t, i, rest = self._find(i)  # @line L14
        path: List[Tuple[Tree, bool]] = []
        h = w
        while i != 0:
            h //= 2
            if i <= h:
                path.append((t, True))
                t, i = t[1], i - 1
            else:
                path.append((t, False))
                t, i = t[2], i - 1 - h
        new: Tree = (y, t[1], t[2])  # @line L15
        for p, went_left in reversed(path):  # @line L16
            new = (p[0], new, p[2]) if went_left else (p[0], p[1], new)
        cells: Cells = (w, new, rest)
        for bw, bt in reversed(before):  # @line L17
            cells = (bw, bt, cells)
        return SkewList(cells, self._n)

    def __iter__(self) -> Iterator[Any]:
        """Items in order, iteratively. Cost: Θ(n)."""
        c = self._cells
        while c is not None:
            stack = [c[1]]
            while stack:
                t = stack.pop()
                yield t[0]
                if t[2] is not None:
                    stack.append(t[2])
                if t[1] is not None:
                    stack.append(t[1])
            c = c[2]

    def to_list(self) -> List[Any]:
        """All items in order. Cost: Θ(n)."""
        return list(self)

    def weights(self) -> List[int]:
        """The tree weights, front first: the skew binary digits of n."""
        out, c = [], self._cells
        while c is not None:
            out.append(c[0])
            c = c[2]
        return out

    def check_invariant(self) -> None:
        """Check that weights are 2^k - 1, grow strictly after the first
        pair, sum to n, and that each tree is complete of its weight.
        Cost: Θ(n)."""
        ws = self.weights()
        assert sum(ws) == self._n
        for k, w in enumerate(ws):
            assert w >= 1 and (w + 1) & w == 0
            if k >= 1:
                assert ws[k - 1] < w or (k == 1 and ws[0] == w)
        c = self._cells
        while c is not None:
            stack = [(c[1], c[0])]
            while stack:
                t, w = stack.pop()
                if w == 1:
                    assert t[1] is None and t[2] is None
                else:
                    assert t[1] is not None and t[2] is not None
                    stack.append((t[1], w // 2))
                    stack.append((t[2], w // 2))
            c = c[2]
