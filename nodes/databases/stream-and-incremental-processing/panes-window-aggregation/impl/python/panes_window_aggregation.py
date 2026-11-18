# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/panes-window-aggregation/. The authors are listed in prov/0B550K.jsonl.

"""Pane-based sliding-window aggregation (Li, Maier, Tufte, Papadimos and
Tucker 2005).

The windows are [j*S, j*S + R) for j = 0, 1, 2, ... in event time. The stream
is cut into panes of length g = gcd(R, S); each tuple is added to the partial
aggregate of its pane (the pane-level query), and each window is the
combination of its k = R / g pane partials (the window-level query).

Tuples may arrive out of order. The caller gives a watermark with advance(w):
no tuple with a timestamp below w is expected. A pane closes when the
watermark reaches its end. A tuple whose pane is closed is late; it is dropped
and counted.
"""

from collections import deque
from dataclasses import dataclass
from math import gcd
from typing import Any, Callable


@dataclass(frozen=True)
class Aggregate:
    """A bounded aggregate: lift a value, combine partials, lower the result."""

    name: str
    identity: Any
    lift: Callable[[Any], Any]
    combine: Callable[[Any, Any], Any]
    lower: Callable[[Any], Any]


def _max2(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return a if a >= b else b


SUM = Aggregate("sum", 0, lambda v: v, lambda a, b: a + b, lambda a: a)
COUNT = Aggregate("count", 0, lambda v: 1, lambda a, b: a + b, lambda a: a)
MAX = Aggregate("max", None, lambda v: v, _max2, lambda a: a)
AVG = Aggregate(
    "avg",
    (0, 0),
    lambda v: (v, 1),
    lambda a, b: (a[0] + b[0], a[1] + b[1]),
    lambda a: None if a[1] == 0 else (a[0], a[1]),  # exact (sum, count)
)


class PanedAggregator:
    def __init__(self, R: int, S: int, agg: Aggregate):
        if R <= 0 or S <= 0:
            raise ValueError("R and S must be positive")
        self.R, self.S, self.agg = R, S, agg
        self.g = gcd(R, S)  # @line L1
        self.k = R // self.g
        self.next = 0  # the id of the first pane that is not closed
        self.open: dict[int, Any] = {}  # @line L2
        self.last: deque = deque()
        self.late = 0
        self.combines = 0  # calls of agg.combine, for the cost tests

    def _combine(self, a, b):
        self.combines += 1
        return self.agg.combine(a, b)

    def insert(self, t: int, v) -> bool:
        """Add one tuple. Return False if it is late and dropped."""
        i = t // self.g  # @line L3
        if i < self.next:  # @line L4
            self.late += 1
            return False
        self.open[i] = self._combine(self.open.get(i, self.agg.identity), self.agg.lift(v))  # @line L5
        return True

    def advance(self, w: int) -> list[tuple[int, int, Any]]:
        """Close the panes that end at or before w; return the finished windows."""
        out = []
        while (self.next + 1) * self.g <= w:  # @line L6
            self.last.append(self.open.pop(self.next, self.agg.identity))  # @line L7
            if len(self.last) > self.k:
                self.last.popleft()
            e = (self.next + 1) * self.g  # @line L8
            self.next += 1
            if e >= self.R and (e - self.R) % self.S == 0:  # @line L9
                acc = self.agg.identity
                for p in self.last:
                    acc = self._combine(acc, p)
                out.append((e - self.R, e, self.agg.lower(acc)))  # @line L10
        return out

    def state_size(self) -> int:
        """The number of partials held: open panes plus the last k closed ones."""
        return len(self.open) + len(self.last)


def run(arrivals, R: int, S: int, agg: Aggregate, delay: int = 0):
    """Feed (t, v) pairs in arrival order with the watermark max_t_seen - delay.

    At the end, flush every window whose start is at most the largest
    timestamp. Return (windows, the aggregator)."""
    pa = PanedAggregator(R, S, agg)
    out = []
    top = None
    for t, v in arrivals:
        pa.insert(t, v)
        top = t if top is None else max(top, t)
        out.extend(pa.advance(top - delay))
    if top is not None:
        out.extend(pa.advance((top // S) * S + R))
    return out, pa
