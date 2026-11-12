# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gcra/. The authors are listed in prov/5WH9D0.jsonl.

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]


class GCRA:
    """The generic cell rate algorithm GCRA(T, tau), virtual scheduling form.

    T is the emission interval (1 / rate) and tau the tolerance, both in units
    of time. The only state is the theoretical arrival time `tat`. Time is an
    explicit number that the caller passes in; it must not go back.
    """

    def __init__(self, T: Number, tau: Number, start: Number = 0) -> None:
        if T <= 0 or tau < 0:
            raise ValueError("need T > 0 and tau >= 0")
        self.T = T
        self.tau = tau
        self.tat: Number = start
        self.last: Number = start

    def allow(self, t: Number) -> bool:
        """Return True if a cell that arrives at time t conforms, and update the state."""
        if t < self.last:
            raise ValueError("time went back")
        self.last = t
        if t < self.tat - self.tau:  # @line L1
            return False
        self.tat = max(t, self.tat) + self.T  # @line L2
        return True  # @line L3

    def allow_n(self, t: Number, n: int = 1) -> bool:
        """Rate limiter form: n units at once, with emission interval T per unit.

        The request passes if its new theoretical arrival time is at most
        tau + T after t. For n = 1 this is the test of allow().
        """
        if t < self.last:
            raise ValueError("time went back")
        self.last = t
        new_tat = max(t, self.tat) + n * self.T
        if new_tat - t > self.tau + self.T:
            return False
        self.tat = new_tat
        return True

    def retry_at(self, n: int = 1) -> Number:
        """The earliest time at which n units would pass if nothing else arrives."""
        return self.tat + n * self.T - self.T - self.tau


class GCRALeakyBucket:
    """GCRA(T, tau), continuous-state leaky bucket form: level X and last conformance time."""

    def __init__(self, T: Number, tau: Number, start: Number = 0) -> None:
        if T <= 0 or tau < 0:
            raise ValueError("need T > 0 and tau >= 0")
        self.T = T
        self.tau = tau
        self.X: Number = 0
        self.lct: Number = start

    def allow(self, t: Number) -> bool:
        x = max(0, self.X - (t - self.lct))  # @line L4
        if x > self.tau:  # @line L5
            return False
        self.X = x + self.T  # @line L6
        self.lct = t
        return True  # @line L7


def gcra(times: list[Number], T: Number, tau: Number, start: Optional[Number] = None) -> list[bool]:
    """Decisions of GCRA(T, tau) for cells at the given times (in order)."""
    if not times:
        return []
    g = GCRA(T, tau, times[0] if start is None else start)
    return [g.allow(t) for t in times]
