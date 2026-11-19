# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-determinization/. The authors are listed in prov/40YQAC.jsonl.

"""Weighted determinization of an epsilon-free weighted acceptor (Mohri 1997).

Weights are costs -log p. The semiring is TROPICAL (min, +) or LOG_COST
(-log(exp(-a) + exp(-b)), +) from nlslog. In both, the division needed for
the residual weights is a subtraction of costs.

An acceptor has states 0..n-1, a start state with an initial weight, a final
cost per final state, and arcs (label, weight, next). A state of the result is
a weighted subset: a set of pairs (q, r), where r is the residual weight of
state q, the part of the weight that the result has not yet emitted.

The algorithm terminates when the input has the twins property over the
tropical semiring (Mohri 1997), and on every acyclic input. On other inputs
it can run forever, so max_states stops it with an error.

Residuals are floats. Two subsets are the same state when their residuals
agree after rounding to a multiple of delta; the first residuals seen are kept.
"""

from typing import Dict, FrozenSet, List, Tuple

from nlslog import TROPICAL, Semiring


class Acceptor:
    """A weighted acceptor with integer states and costs."""

    def __init__(self) -> None:
        self.start = 0
        self.initial = 0.0
        self.arcs: List[List[Tuple[str, float, int]]] = []
        self.final: Dict[int, float] = {}

    def add_state(self) -> int:
        self.arcs.append([])
        return len(self.arcs) - 1

    def add_arc(self, q: int, label: str, weight: float, nxt: int) -> None:
        self.arcs[q].append((label, weight, nxt))

    def set_final(self, q: int, weight: float = 0.0) -> None:
        self.final[q] = weight

    def num_states(self) -> int:
        return len(self.arcs)

    def num_arcs(self) -> int:
        return sum(len(a) for a in self.arcs)

    def is_deterministic(self) -> bool:
        return all(len({a[0] for a in arcs}) == len(arcs) for arcs in self.arcs)


class NotDeterminizable(Exception):
    """Raised when the result grows past max_states. The attribute subsets holds the subsets built so far."""


def determinize(a: Acceptor, sr: Semiring = TROPICAL, max_states: int = 10000, delta: float = 1e-9):
    """Return (d, subsets): a deterministic acceptor equivalent to a, and the weighted subset of each state.

    Raise NotDeterminizable if d would have more than max_states states.
    """
    d = Acceptor()
    index: Dict[FrozenSet[Tuple[int, int]], int] = {}
    subsets: List[List[Tuple[int, float]]] = []
    queue: List[int] = []

    def key(subset):
        return frozenset((q, round(r / delta)) for q, r in subset)

    def state_of(subset):
        k = key(subset)
        if k not in index:  # @line L10
            if len(subsets) >= max_states:
                err = NotDeterminizable("more than %d states" % max_states)
                err.subsets = subsets
                raise err
            index[k] = d.add_state()
            subsets.append(subset)
            queue.append(index[k])
        return index[k]

    d.initial = a.initial  # @line L1
    d.start = state_of([(a.start, sr.one)])
    head = 0
    while head < len(queue):  # @line L2
        p = queue[head]  # @line L3
        head += 1
        subset = subsets[p]
        rho = sr.zero
        for q, r in subset:  # @line L4
            if q in a.final:
                rho = sr.plus(rho, sr.times(r, a.final[q]))
        if rho != sr.zero:
            d.set_final(p, rho)
        # Group the arcs that leave the subset by label, in first-seen order.
        by_label: Dict[str, List[Tuple[float, int]]] = {}
        for q, r in subset:
            for label, w, n in a.arcs[q]:
                by_label.setdefault(label, []).append((sr.times(r, w), n))
        for label, moves in by_label.items():  # @line L5
            w_new = sr.zero
            for v, _ in moves:  # @line L6
                w_new = sr.plus(w_new, v)
            residual: Dict[int, float] = {}
            for v, n in moves:  # @line L7
                residual[n] = sr.plus(residual.get(n, sr.zero), v)
            nxt = sorted((n, v - w_new) for n, v in residual.items())  # @line L8
            d.add_arc(p, label, w_new, state_of(nxt))  # @line L9
    return d, subsets


def string_weight(a: Acceptor, x, sr: Semiring = TROPICAL) -> float:
    """Return the weight of the string x in a: the semiring sum over the paths that read x."""
    cur = {a.start: a.initial}
    for c in x:
        nxt: Dict[int, float] = {}
        for q, w in cur.items():
            for label, wa, n in a.arcs[q]:
                if label == c:
                    nxt[n] = sr.plus(nxt.get(n, sr.zero), sr.times(w, wa))
        cur = nxt
    total = sr.zero
    for q, w in cur.items():
        if q in a.final:
            total = sr.plus(total, sr.times(w, a.final[q]))
    return total
