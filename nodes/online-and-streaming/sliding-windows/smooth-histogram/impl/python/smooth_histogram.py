# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smooth-histogram/. The authors are listed in prov/PBPEZG.jsonl.
"""The smooth histogram of Braverman and Ostrovsky over a count-based window.

The structure keeps start times x_1 < ... < x_s and, for each start time x, an
insertion-only instance that has read the items x, x + 1, ..., t. An instance
has update(item) and value(). This file uses exact instances. For an
(alpha, beta)-smooth function f, the answer for a window of the last w <= W
items is between (1 - alpha) f(window) and f(window).
"""

from fractions import Fraction
from typing import Any, Callable, List, Tuple


class SmoothHistogram:
    """Approximate f over the last w <= W items for a smooth function f."""

    def __init__(self, window: int, beta: Fraction, make_instance: Callable[[], Any]) -> None:
        beta = Fraction(beta)
        if window < 1 or not 0 < beta < 1:
            raise ValueError("need window >= 1 and 0 < beta < 1")
        self.window = window
        self.keep = 1 - beta
        self.make_instance = make_instance
        self.t = 0
        self.starts: List[int] = []
        self.instances: List[Any] = []

    def update(self, item: Any) -> None:
        """Read one item (lines L1 to L8)."""
        self.t += 1  # @line L1
        self.starts.append(self.t)  # @line L2
        self.instances.append(self.make_instance())
        for inst in self.instances:  # @line L3
            inst.update(item)
        self._prune()
        self._expire()

    def _prune(self) -> None:
        # The values do not increase along the list, because each later
        # instance reads a suffix of the items of an earlier one. So the
        # largest j with f(x_j) >= (1 - beta) f(x_i) is found by a scan.
        values = [inst.value() for inst in self.instances]
        s = len(values)
        kept = []
        i = 0  # @line L4
        while i < s:  # @line L5
            kept.append(i)
            limit = self.keep * values[i]
            j = i + 1  # @line L6
            while j + 1 < s and values[j + 1] >= limit:
                j += 1
            i = j  # @line L7
        self.starts = [self.starts[i] for i in kept]
        self.instances = [self.instances[i] for i in kept]

    def _expire(self) -> None:
        last = -1
        for i, x in enumerate(self.starts):
            if x <= self.t - self.window:
                last = i
        if last > 0:  # @line L8
            del self.starts[:last]
            del self.instances[:last]

    def query(self, w: int = 0) -> Any:
        """Approximate f over the last w items, 1 <= w <= W (default W); lines L9 to L11."""
        if w == 0:
            w = self.window
        if not 1 <= w <= self.window:
            raise ValueError("w must be in 1..W")
        if not self.starts:
            raise ValueError("the stream is empty")
        if self.starts[0] > self.t - w:  # @line L9
            return self.instances[0].value()
        i = max(i for i, x in enumerate(self.starts) if x <= self.t - w)  # @line L10
        return self.instances[i + 1].value()  # @line L11

    def state(self) -> List[Tuple[int, Any]]:
        """The list of pairs (start time, value of its instance)."""
        return [(x, inst.value()) for x, inst in zip(self.starts, self.instances)]


class ExactSum:
    """The sum of nonnegative numbers, an (alpha, alpha)-smooth function."""

    def __init__(self) -> None:
        self.total = 0

    def update(self, item: int) -> None:
        if item < 0:
            raise ValueError("the sum must have nonnegative items")
        self.total += item

    def value(self) -> int:
        return self.total


class ExactDistinct:
    """The number of distinct items, an (alpha, alpha)-smooth function."""

    def __init__(self) -> None:
        self.seen: set = set()

    def update(self, item: Any) -> None:
        self.seen.add(item)

    def value(self) -> int:
        return len(self.seen)


class ExactMax:
    """The maximum of nonnegative numbers (0 for no items), an (alpha, alpha)-smooth function."""

    def __init__(self) -> None:
        self.best = 0

    def update(self, item: int) -> None:
        self.best = max(self.best, item)

    def value(self) -> int:
        return self.best
