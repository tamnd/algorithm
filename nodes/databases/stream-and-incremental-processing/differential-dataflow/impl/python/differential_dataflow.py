# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-dataflow/. The authors are listed in prov/Q08Q0Y.jsonl.

"""Differential computation of graph reachability, with times (epoch, iteration).

A collection that varies with time t is stored as differences: a map from
times to signed Counters, with the collection at t equal to the sum of the
differences at all times s <= t in the product order

    (e1, i1) <= (e2, i2)  iff  e1 <= e2 and i1 <= i2.

The program is the iterative dataflow

    R_{e,0}   = distinct(roots_e)
    R_{e,i+1} = distinct(roots_e + dst(R_{e,i} join edges_e))

where roots_e and edges_e are the inputs after epoch e. The inputs change only
at times (e, 0). The feedback edge moves each difference of R from (e, i) to
(e, i + 1). The join puts the product of differences at s and u at the least
upper bound of s and u, and distinct is evaluated only at the times in the
closure, under least upper bounds, of the times at which its input changes.

The code finds the matching differences by scanning, which is simple and slow;
a real system keeps them in indexed traces.
"""

from collections import Counter
from collections.abc import Iterable, Mapping


def leq(s: tuple, t: tuple) -> bool:
    return s[0] <= t[0] and s[1] <= t[1]


def lub(s: tuple, t: tuple) -> tuple:
    return (max(s[0], t[0]), max(s[1], t[1]))


def _clean(c: Mapping) -> Counter:
    return Counter({k: w for k, w in c.items() if w != 0})


class Trace:
    """Differences of one collection, indexed by time."""

    def __init__(self) -> None:
        self.diffs: dict = {}

    def add(self, t: tuple, d: Mapping) -> None:
        d = _clean(d)
        if d:
            cur = self.diffs.get(t, Counter())
            cur.update(d)
            cur = _clean(cur)
            if cur:
                self.diffs[t] = cur
            else:
                self.diffs.pop(t, None)

    def at(self, t: tuple, strict: bool = False) -> Counter:
        """The collection at t: the sum of the differences at times s <= t (s < t if strict)."""
        out: Counter = Counter()
        for s, d in self.diffs.items():
            if leq(s, t) and not (strict and s == t):
                out.update(d)
        return _clean(out)

    def get(self, t: tuple) -> Counter:
        return self.diffs.get(t, Counter())


class Reachability:
    """Maintain the nodes reachable from roots as edges and roots change, epoch by epoch."""

    def __init__(self) -> None:
        self.roots = Trace()
        self.edges = Trace()
        self.fed = Trace()        # R delayed by one iteration
        self.join = Trace()       # dst(fed join edges)
        self.union = Trace()      # roots + join, the input of distinct
        self.out = Trace()        # R
        self.closure: set = set()
        self.epoch = -1
        self.imax = -1            # the largest iteration of any stored time
        self.distinct_evals = 0

    def _note(self, t: tuple) -> None:
        self.imax = max(self.imax, t[1])

    def advance(self, d_roots: Mapping = (), d_edges: Mapping = ()) -> None:
        """Apply the changes of the next epoch and run its iterations to the fixed point."""
        e = self.epoch + 1
        self.epoch = e
        self.roots.add((e, 0), Counter(d_roots))  # @line L1
        self.edges.add((e, 0), Counter(d_edges))
        i = 0
        while True:
            t = (e, i)
            if i > 0 and i > self.imax and not self.out.get((e, i - 1)):
                break  # @line L2
            if i > 0:
                self.fed.add(t, self.out.get((e, i - 1)))  # @line L3
            dj: Counter = Counter()
            for s, df in self.fed.diffs.items():  # @line L4
                for u, de in self.edges.diffs.items():
                    if lub(s, u) != t:
                        continue
                    for node, w in df.items():
                        for (a, b), x in de.items():
                            if a == node:
                                dj[b] += w * x
            self.join.add(t, dj)
            du = Counter(self.roots.get(t))  # @line L5
            du.update(self.join.get(t))
            du = _clean(du)
            if du:
                self.union.add(t, du)
                if t not in self.closure:  # @line L6
                    self.closure |= {lub(t, c) for c in self.closure} | {t}
            if t in self.closure:  # @line L7
                self.distinct_evals += 1
                u_t = self.union.at(t)
                want = Counter({x: 1 for x, w in u_t.items() if w > 0})
                have = self.out.at(t, strict=True)
                diff = Counter(want)
                diff.subtract(have)
                self.out.add(t, diff)  # @line L8
            for tr in (self.fed, self.join, self.union, self.out):
                if t in tr.diffs:
                    self._note(t)
            i += 1

    def reachable(self, e: int, i: int | None = None) -> set:
        """R at (e, i), or at the end of the iterations of epoch e if i is None."""
        if i is None:
            i = max([s[1] for s in self.out.diffs] + [0]) + 1
        return {x for x, w in self.out.at((e, i)).items() if w > 0}


def recompute(roots: Iterable, edges: Iterable, i: int) -> set:
    """R_{e,i} from scratch, by the definition of the iteration."""
    roots = set(roots)
    edges = set(edges)
    r = set(roots)
    for _ in range(i):
        r = roots | {b for a, b in edges if a in r}
    return r


def bfs(roots: Iterable, edges: Iterable) -> set:
    adj: dict = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
    seen = set(roots)
    frontier = list(seen)
    while frontier:
        nxt = []
        for a in frontier:
            for b in adj.get(a, []):
                if b not in seen:
                    seen.add(b)
                    nxt.append(b)
        frontier = nxt
    return seen
