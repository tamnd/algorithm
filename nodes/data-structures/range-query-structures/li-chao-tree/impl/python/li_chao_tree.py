# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/li-chao-tree/. The authors are listed in prov/E3PVVE.jsonl.

from typing import Optional

Line = tuple[int, int]  # (a, b) for y = a*x + b


def _val(f: Line, x: int) -> int:
    return f[0] * x + f[1]


class LiChaoTree:
    """Minimum of lines y = a*x + b at integer points of [lo, hi).

    Nodes are created only when a line is placed, so n insertions make at
    most n nodes. insert and query take O(log(hi - lo)) time.
    """

    def __init__(self, lo: int, hi: int) -> None:
        """The domain is the integers lo <= x < hi; requires lo < hi."""
        if lo >= hi:
            raise ValueError("need lo < hi")
        self.lo = lo
        self.hi = hi
        self.line: list[Optional[Line]] = [None]  # node 0 is the root
        self.left: list[int] = [-1]
        self.right: list[int] = [-1]

    def _child(self, v: int, go_left: bool) -> int:
        kids = self.left if go_left else self.right
        if kids[v] == -1:
            kids[v] = len(self.line)
            self.line.append(None)
            self.left.append(-1)
            self.right.append(-1)
        return kids[v]

    def insert(self, a: int, b: int) -> None:
        """Add the line y = a*x + b."""
        f: Line = (a, b)
        v, lo, hi = 0, self.lo, self.hi  # @line L1
        while True:  # @line L2
            g = self.line[v]
            if g is None:  # @line L3
                self.line[v] = f
                return
            mid = (lo + hi) // 2  # @line L4
            if _val(f, mid) < _val(g, mid):  # @line L5
                self.line[v], f = f, g
                g = self.line[v]
                assert g is not None
            if hi - lo == 1:  # @line L6
                return
            if _val(f, lo) < _val(g, lo):  # @line L7
                v, hi = self._child(v, True), mid
            elif _val(f, hi - 1) < _val(g, hi - 1):  # @line L8
                v, lo = self._child(v, False), mid
            else:  # @line L9
                return

    def query(self, x: int) -> Optional[int]:
        """The least value of the lines at x, or None if there are none."""
        if not self.lo <= x < self.hi:
            raise IndexError("x outside the domain")
        v, lo, hi = 0, self.lo, self.hi  # @line L10
        best: Optional[int] = None
        while v != -1 and self.line[v] is not None:  # @line L11
            y = _val(self.line[v], x)  # type: ignore[arg-type]
            best = y if best is None or y < best else best  # @line L12
            if hi - lo == 1:  # @line L13
                break
            mid = (lo + hi) // 2  # @line L14
            if x < mid:  # @line L15
                v, hi = self.left[v], mid
            else:
                v, lo = self.right[v], mid
        return best  # @line L16

    def stored(self) -> list[Optional[Line]]:
        """The line of each node, in order of creation."""
        return list(self.line)

    def check_invariant(self) -> None:
        """Check that no filled node has an empty parent and that every
        stored line is lowest at the middle among the lines of its subtree."""
        stack = [(0, self.lo, self.hi)]
        while stack:
            v, lo, hi = stack.pop()
            g = self.line[v]
            mid = (lo + hi) // 2
            for c, a, b in ((self.left[v], lo, mid), (self.right[v], mid, hi)):
                if c == -1:
                    continue
                h = self.line[c]
                if h is not None:
                    assert g is not None, "filled node below an empty one"
                    assert _val(g, mid) <= _val(h, mid), "node line not lowest at mid"
                if a < b:
                    stack.append((c, a, b))
