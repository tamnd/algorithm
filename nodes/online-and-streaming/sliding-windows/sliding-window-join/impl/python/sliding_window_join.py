# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-join/. The authors are listed in prov/1RHMXP.jsonl.
"""Symmetric hash join of two streams A and B over sliding windows."""

from collections import deque
from typing import Any, Deque, Dict, List, Tuple

Tup = Tuple[float, Any, Any]  # (timestamp, key, value)
Pair = Tuple[Tup, Tup]  # (tuple of A, tuple of B)


class _Side:
    """One window: a FIFO of all tuples and a map from key to a FIFO of tuples."""

    def __init__(self) -> None:
        self.queue: Deque[Tup] = deque()
        self.index: Dict[Any, Deque[Tup]] = {}

    def insert(self, u: Tup) -> None:
        self.queue.append(u)
        self.index.setdefault(u[1], deque()).append(u)

    def pop_oldest(self) -> None:
        u = self.queue.popleft()
        bucket = self.index[u[1]]
        bucket.popleft()  # the oldest tuple with this key is the oldest tuple overall with it
        if not bucket:
            del self.index[u[1]]

    def matches(self, key: Any) -> Deque[Tup]:
        return self.index.get(key, deque())

    def __len__(self) -> int:
        return len(self.queue)


class TimeWindowJoin:
    """A tuple at time t sees the tuples of the other stream with time > t - T of that stream."""

    def __init__(self, t_a: float, t_b: float) -> None:
        if t_a <= 0 or t_b <= 0:
            raise ValueError("window lengths must be positive")
        self.length = {"A": t_a, "B": t_b}
        self.side = {"A": _Side(), "B": _Side()}
        self.probed = 0  # tuples looked at during probes, equal to the output size

    def arrive(self, stream: str, t: float, key: Any, value: Any = None) -> List[Pair]:
        other = "B" if stream == "A" else "A"
        for x in ("A", "B"):  # @line L1
            s = self.side[x]
            while s.queue and s.queue[0][0] <= t - self.length[x]:
                s.pop_oldest()
        u = (t, key, value)
        found = list(self.side[other].matches(key))  # @line L2
        self.probed += len(found)
        out = [(u, w) if stream == "A" else (w, u) for w in found]
        self.side[stream].insert(u)  # @line L3
        return out

    def stored(self) -> int:
        return len(self.side["A"]) + len(self.side["B"])


class CountWindowJoin:
    """A tuple sees the last n tuples of the other stream that arrived before it."""

    def __init__(self, n_a: int, n_b: int) -> None:
        if n_a < 1 or n_b < 1:
            raise ValueError("window sizes must be at least 1")
        self.size = {"A": n_a, "B": n_b}
        self.side = {"A": _Side(), "B": _Side()}
        self.seq = 0

    def arrive(self, stream: str, key: Any, value: Any = None) -> List[Pair]:
        other = "B" if stream == "A" else "A"
        self.seq += 1
        u = (self.seq, key, value)  # the arrival number takes the place of a timestamp
        out = [(u, w) if stream == "A" else (w, u) for w in self.side[other].matches(key)]
        s = self.side[stream]
        s.insert(u)
        if len(s) > self.size[stream]:
            s.pop_oldest()
        return out

    def stored(self) -> int:
        return len(self.side["A"]) + len(self.side["B"])
