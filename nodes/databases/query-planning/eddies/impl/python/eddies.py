# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eddies/. The authors are listed in prov/CC4NGE.jsonl.
"""An eddy (Avnur and Hellerstein, SIGMOD 2000) with one SteM per relation.

The query is a natural join of relations with selection filters on single
relations. Base tuples arrive one at a time, in any interleaving of the
relations. Each arriving tuple gets a timestamp and is built into the SteM
(state module, an index of the tuples seen so far) of its relation. Then the
eddy routes the tuple, one operator at a time, through the filters of the
relations it covers and through probes into the SteMs of the other relations.
A routing policy chooses the next operator for each tuple separately, and
routing steps interleave with new arrivals, as in a pipelined system.

A probe returns only SteM entries with a smaller timestamp than the base
tuple that started the routing. So each result is built only from the base
tuple of the result that arrived last, and each result is output exactly
once, for every arrival order and every routing policy.
"""

from random import Random
from typing import Callable, Dict, List, Optional, Sequence, Tuple

Row = Dict[str, object]


class SteM:
    """A state module: the tuples of one relation seen so far, with hash indexes built on demand."""

    def __init__(self) -> None:
        self.rows: List[Tuple[int, Row]] = []
        self.idx: Dict[Tuple[str, ...], Dict[tuple, List[Tuple[int, Row]]]] = {}

    def build(self, ts: int, row: Row) -> None:
        self.rows.append((ts, row))
        for attrs, d in self.idx.items():
            d.setdefault(tuple(row[a] for a in attrs), []).append((ts, row))

    def probe(self, attrs: Tuple[str, ...], key: tuple, before: int) -> List[Row]:
        if attrs not in self.idx:
            d: Dict[tuple, List[Tuple[int, Row]]] = {}
            for ts, row in self.rows:
                d.setdefault(tuple(row[a] for a in attrs), []).append((ts, row))
            self.idx[attrs] = d
        return [row for ts, row in self.idx[attrs].get(key, []) if ts < before]


class FixedPolicy:
    """Always choose the first eligible operator in a fixed priority list."""

    def __init__(self, priority: Sequence[str]):
        self.rank = {op: i for i, op in enumerate(priority)}

    def choose(self, eligible: List[str], rng: Random) -> str:
        return min(eligible, key=lambda op: self.rank.get(op, len(self.rank)))

    def feedback(self, op: str, returned: int) -> None:
        pass


class RandomPolicy:
    """Choose an eligible operator uniformly at random."""

    def choose(self, eligible: List[str], rng: Random) -> str:
        return eligible[rng.randrange(len(eligible))]

    def feedback(self, op: str, returned: int) -> None:
        pass


class LotteryPolicy:
    """Lottery scheduling: an operator gets a ticket for each tuple it receives
    and loses one for each tuple it returns. The eddy draws an eligible operator
    with probability proportional to its tickets (at least 1)."""

    def __init__(self) -> None:
        self.tickets: Dict[str, int] = {}

    def choose(self, eligible: List[str], rng: Random) -> str:
        weights = [max(1, self.tickets.get(op, 1)) for op in eligible]
        x = rng.randrange(sum(weights))
        for op, w in zip(eligible, weights):
            if x < w:
                break
            x -= w
        self.tickets[op] = self.tickets.get(op, 1) + 1
        return op

    def feedback(self, op: str, returned: int) -> None:
        self.tickets[op] = max(1, self.tickets.get(op, 1) - returned)


class Eddy:
    """A natural join of `schemas` (relation name to attribute names) with
    `filters` (filter name to (relation name, predicate))."""

    def __init__(self, schemas: Dict[str, Sequence[str]],
                 filters: Optional[Dict[str, Tuple[str, Callable[[Row], bool]]]] = None,
                 costs: Optional[Dict[str, float]] = None):
        self.schemas = {r: set(a) for r, a in schemas.items()}
        self.filters = filters or {}
        self.costs = costs or {}
        names = list(self.schemas)
        reached = {names[0]} if names else set()
        grow = True
        while grow:
            grow = False
            for r in names:
                if r not in reached and any(self.schemas[r] & self.schemas[q] for q in reached):
                    reached.add(r)
                    grow = True
        if len(reached) != len(names):
            raise ValueError("the join graph is not connected")
        self.stems = {r: SteM() for r in names}
        self.work: Dict[str, float] = {}

    def _eligible(self, parts: Dict[str, Row], done: frozenset) -> List[str]:
        ops = [f for f, (rel, _) in self.filters.items() if rel in parts and f not in done]
        for r in self.schemas:
            if r not in parts and any(self.schemas[r] & self.schemas[q] for q in parts):
                ops.append("stem:" + r)
        return ops

    def run(self, arrivals: Sequence[Tuple[str, Row]], policy, rng: Random,
            p_route: float = 0.5, use_timestamps: bool = True) -> List[Dict[str, Row]]:
        """Process the arrivals in order. Returns the results, each a dict from relation to row.

        Arrivals and routing steps interleave: while tuples wait in the eddy,
        the next step routes one of them, chosen at random, with probability
        p_route, and otherwise takes the next arrival. With p_route = 1, each
        arrival is routed to the end before the next one. use_timestamps =
        False turns off the timestamp test of the probes, to show why it is
        needed."""
        out: List[Dict[str, Row]] = []
        waiting: List[Tuple[Dict[str, Row], frozenset, int]] = []
        nxt = 0
        while nxt < len(arrivals) or waiting:  # @line L1
            if nxt < len(arrivals) and (not waiting or rng.random() >= p_route):
                rel, row = arrivals[nxt]
                self.stems[rel].build(nxt, row)  # @line L2
                waiting.append(({rel: row}, frozenset(), nxt))  # @line L3
                nxt += 1
                continue
            i = rng.randrange(len(waiting))
            waiting[i], waiting[-1] = waiting[-1], waiting[i]
            parts, done, tau = waiting.pop()  # @line L4
            eligible = self._eligible(parts, done)  # @line L5
            if not eligible:  # @line L6
                out.append(parts)
                continue
            op = policy.choose(eligible, rng)  # @line L7
            self.work[op] = self.work.get(op, 0) + self.costs.get(op, 1)
            if not op.startswith("stem:"):  # @line L8
                frel, pred = self.filters[op]
                if pred(parts[frel]):
                    waiting.append((parts, done | {op}, tau))
                    policy.feedback(op, 1)
                else:
                    policy.feedback(op, 0)
                continue
            target = op[5:]
            attrs = tuple(sorted(set().union(*(self.schemas[target] & self.schemas[q] for q in parts))))
            key = []
            for a in attrs:
                key.append(next(parts[q][a] for q in parts if a in self.schemas[q]))
            before = tau if use_timestamps else len(arrivals)
            matches = self.stems[target].probe(attrs, tuple(key), before)  # @line L9
            for m in matches:
                p2 = dict(parts)
                p2[target] = m
                waiting.append((p2, done, tau))
            policy.feedback(op, len(matches))
        return out


def random_arrivals(relations: Dict[str, List[Row]], rng: Random) -> List[Tuple[str, Row]]:
    """All base tuples of all relations, in a uniform random order of arrival."""
    seq = [(r, row) for r, rows in relations.items() for row in rows]
    rng.shuffle(seq)
    return seq
