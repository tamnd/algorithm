# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stream-slicing/. The authors are listed in prov/ZPAWWC.jsonl.

"""Stream slicing for several sliding-window queries that share one stream.

Each query q has a range R and a slide S; its windows are [j*S, j*S + R) for
j = 0, 1, 2, ... The stream is cut into slices, one partial aggregate per
slice, and each window result is combined from the slices it covers.

Two cutting rules are given:
- "edges": cut at every window start and every window end of every query
  (the general rule of Krishnamurthy et al. 2006 and Traub et al. 2021);
- "starts": cut only at window starts (the rule of Cutty, Carbone et al.
  2016). A window end then falls inside the open slice, and the result uses
  the running partial of that slice at the moment the end is reached.

The input must be in timestamp order (ties allowed). The aggregate needs only
an associative combine with an identity; it need not be commutative.
"""

from collections import deque
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Aggregate:
    name: str
    identity: Any
    lift: Callable[[Any], Any]
    combine: Callable[[Any, Any], Any]


SUM = Aggregate("sum", 0, lambda v: v, lambda a, b: a + b)
MAX = Aggregate("max", None, lambda v: v, lambda a, b: b if a is None else a if b is None else max(a, b))
CONCAT = Aggregate("concat", "", lambda v: str(v) + ",", lambda a, b: a + b)  # not commutative


def _next_multiple(x: int, S: int, offset: int = 0) -> int:
    """The smallest b > x with b = offset + j*S for an integer j >= 0."""
    if x < offset:
        return offset
    return offset + ((x - offset) // S + 1) * S


class Slicer:
    def __init__(self, queries: list[tuple[int, int]], agg: Aggregate, mode: str = "edges"):
        if mode not in ("edges", "starts"):
            raise ValueError("mode must be 'edges' or 'starts'")
        for R, S in queries:
            if R <= 0 or S <= 0:
                raise ValueError("R and S must be positive")
        self.queries, self.agg, self.mode = list(queries), agg, mode
        self.closed: deque = deque()  # (start, end, partial) of closed slices
        self.cur_start, self.cur = 0, agg.identity  # the open slice
        self.cur_end = self._next_boundary(0)
        self.next_end = [R for R, S in self.queries]  # the next window end of each query
        self.cuts = [0]  # the start of every slice made so far
        self.combines = 0

    def _next_boundary(self, x: int) -> int:
        """The first cut after time x."""
        best = None
        for R, S in self.queries:
            cands = [_next_multiple(x, S)]
            if self.mode == "edges":
                cands.append(_next_multiple(x, S, R))
            for b in cands:
                best = b if best is None else min(best, b)
        return best

    def _op(self, a, b):
        self.combines += 1
        return self.agg.combine(a, b)

    def _close_until(self, t: int) -> None:
        """Close the open slice while it ends at or before t."""
        while self.cur_end <= t:  # @line L8
            self.closed.append((self.cur_start, self.cur_end, self.cur))  # @line L9
            self.cur_start, self.cur = self.cur_end, self.agg.identity
            self.cur_end = self._next_boundary(self.cur_start)
            self.cuts.append(self.cur_start)

    def _emit_until(self, t: int, max_start=None) -> list[tuple[int, int, int, Any]]:
        """Emit, in time order, every window that ends at or before t.

        With max_start, a query stops at its first window that starts later."""
        out = []
        while True:
            q = min(range(len(self.queries)), key=lambda i: (self.next_end[i], i))
            e = self.next_end[q]
            if e > t:  # @line L4
                break
            R, S = self.queries[q]
            ws = e - R
            if max_start is not None and ws > max_start:
                self.next_end[q] = float("inf")
                continue
            self._close_until(e)  # @line L5
            acc = self.agg.identity
            for s0, s1, p in self.closed:  # @line L6
                if s0 >= ws:
                    acc = self._op(acc, p)
            if self.cur_start < e:  # only in mode "starts": the end is inside the open slice
                acc = self._op(acc, self.cur)
            out.append((q, ws, e, acc))  # @line L7
            self.next_end[q] = e + S
            # drop the slices that no window still open can use
            lo = min(ne - R2 for ne, (R2, _) in zip(self.next_end, self.queries))
            while self.closed and self.closed[0][1] <= lo:
                self.closed.popleft()
        return out

    def insert(self, t: int, v) -> list[tuple[int, int, int, Any]]:
        """Add a tuple with timestamp t (not below the previous one)."""
        out = self._emit_until(t)  # @line L1
        self._close_until(t)  # @line L2
        self.cur = self._op(self.cur, self.agg.lift(v))  # @line L3
        return out

    def flush(self, top: int) -> list[tuple[int, int, int, Any]]:
        """Emit every window that starts at or before top."""
        last = max((top // S) * S + R for R, S in self.queries)
        return self._emit_until(last, max_start=top)


def run(stream, queries, agg, mode="edges"):
    """Run the slicer on (t, v) pairs in timestamp order; return (windows, slicer)."""
    sl = Slicer(queries, agg, mode)
    out = []
    top = None
    for t, v in stream:
        if top is not None and t < top:
            raise ValueError("input must be in timestamp order")
        out.extend(sl.insert(t, v))
        top = t
    if top is not None:
        out.extend(sl.flush(top))
    return out, sl
