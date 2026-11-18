# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sase-event-matching/. The authors are listed in prov/482Z67.jsonl.

"""Sequence pattern matching in the style of SASE (Wu, Diao and Rizvi, SIGMOD 2006).

The pattern is SEQ(E_1, ..., E_k) WITHIN W, with the "skip till any match"
selection: every choice of events e_1, ..., e_k in stream order with
e_i of type E_i and e_k.ts - e_1.ts <= W is a match. Options:

- partition: an equivalence test [key]; all events of a match have the same
  key, and each key gets its own set of stacks (partitioned stacks);
- negated: {i: type}, which forbids an event of that type (with the same key)
  strictly between e_{i-1} and e_i, for 1 <= i < k (0-based positions);
- predicate: a function of the tuple of events, checked after construction.

Each position i has a stack of instances (an active instance stack). An entry
holds the event and RIP, the index of the newest entry in stack i - 1 when
the event arrived. Every entry at or below RIP came earlier, so the paths that
follow the RIP pointers from an entry of the last stack are exactly the
sequences that end with it. Entries older than now - W are pruned.

The matcher needs its input in stream order: timestamps that never decrease.
Reorder puts a stream with bounded disorder back into order first.
"""

import heapq
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Optional


@dataclass(frozen=True)
class Event:
    type: str
    ts: int
    key: Any = None
    value: Any = None
    eid: int = 0


@dataclass
class _Stack:
    base: int = 0  # the absolute index of entries[0]
    entries: list = field(default_factory=list)  # (event, rip, stream position)

    def top(self) -> int:
        return self.base + len(self.entries) - 1

    def get(self, idx: int):
        return self.entries[idx - self.base]


class SaseMatcher:
    def __init__(
        self,
        types: list[str],
        window: int,
        partition: bool = False,
        negated: Optional[dict[int, str]] = None,
        predicate: Optional[Callable[[tuple], bool]] = None,
    ):
        if not types:
            raise ValueError("the pattern needs at least one positive component")
        negated = dict(negated or {})
        for i in negated:
            if not 1 <= i < len(types):
                raise ValueError("a negation must lie between two positive components")
        self.types, self.window, self.partition = list(types), window, partition
        self.negated, self.predicate = negated, predicate
        self.k = len(types)
        self.parts: dict[Any, list[_Stack]] = {}
        self.neg_events: dict[Any, list[tuple[int, Event]]] = {}  # (position, event)
        self.pos = 0  # the position of the next event in the stream
        self.last_ts = None
        self.visits = 0  # stack entries visited by construction

    def _prune(self, stacks: list[_Stack], negs: list, now: int) -> None:
        lo = now - self.window
        for st in stacks:
            drop = 0
            while drop < len(st.entries) and st.entries[drop][0].ts < lo:
                drop += 1
            if drop:
                del st.entries[:drop]
                st.base += drop
        while negs and negs[0][1].ts < lo:
            negs.pop(0)

    def push(self, e: Event) -> list[tuple[Event, ...]]:
        """Add the next event; return the matches that end with it."""
        if self.last_ts is not None and e.ts < self.last_ts:
            raise ValueError("events must come in timestamp order; use Reorder")
        self.last_ts = e.ts
        p = self.pos
        self.pos += 1
        key = e.key if self.partition else None
        stacks = self.parts.setdefault(key, [_Stack() for _ in range(self.k)])  # @line L1
        negs = self.neg_events.setdefault(key, [])
        self._prune(stacks, negs, e.ts)  # @line L2
        if e.type in self.negated.values():
            negs.append((p, e))
        out = []
        for i in range(self.k - 1, -1, -1):  # @line L3
            if self.types[i] != e.type:
                continue
            if i == 0 or stacks[i - 1].entries:  # @line L4
                rip = stacks[i - 1].top() if i > 0 else -1
                stacks[i].entries.append((e, rip, p))  # @line L5
                if i == self.k - 1:
                    out.extend(self._construct(stacks, negs, e))  # @line L6
        return out

    def _construct(self, stacks, negs, e) -> list[tuple[Event, ...]]:
        found = []
        last = stacks[self.k - 1]
        start = last.get(last.top())

        def dfs(i: int, entry, path: list) -> bool:
            """Extend path (positions k-1 down to i) through the RIP of entry."""
            self.visits += 1
            if i == 0:
                found.append(tuple(reversed(path)))  # @line L7
                return True
            st = stacks[i - 1]
            any_match = False
            idx = entry[1]
            # newest first; an entry lower in the stack has fewer predecessors,
            # so after the first entry without a path, all lower ones fail too
            while idx >= st.base:
                cand = st.get(idx)
                if not dfs(i - 1, cand, path + [cand]):
                    break
                any_match = True
                idx -= 1
            return any_match

        dfs(self.k - 1, start, [start])
        out = []
        for path in found:
            events = tuple(x[0] for x in path)
            if events[-1].ts - events[0].ts > self.window:  # @line L8
                continue
            if any(self._blocked(negs, path[i - 1][2], path[i][2], t) for i, t in self.negated.items()):
                continue
            if self.predicate is not None and not self.predicate(events):
                continue
            out.append(events)  # @line L9
        return out

    @staticmethod
    def _blocked(negs, a: int, b: int, t: str) -> bool:
        return any(a < p < b and n.type == t for p, n in negs)


class Reorder:
    """A K-slack buffer: it holds events until no earlier event can still come.

    It assumes that an event with timestamp t arrives before every event with
    a timestamp of t + D or more. It releases events in (ts, eid) order."""

    def __init__(self, delay: int):
        self.delay, self.heap, self.top = delay, [], None

    def push(self, e: Event) -> list[Event]:
        heapq.heappush(self.heap, (e.ts, e.eid, e))
        self.top = e.ts if self.top is None else max(self.top, e.ts)
        out = []
        while self.heap and self.heap[0][0] <= self.top - self.delay:
            out.append(heapq.heappop(self.heap)[2])
        return out

    def flush(self) -> list[Event]:
        out = [heapq.heappop(self.heap)[2] for _ in range(len(self.heap))]
        return out


def run(matcher: SaseMatcher, events: Iterable[Event], delay: Optional[int] = None):
    """Feed events (through a Reorder buffer when delay is given); return the matches."""
    out = []
    if delay is None:
        for e in events:
            out.extend(matcher.push(e))
        return out
    buf = Reorder(delay)
    for e in events:
        for x in buf.push(e):
            out.extend(matcher.push(x))
    for x in buf.flush():
        out.extend(matcher.push(x))
    return out
