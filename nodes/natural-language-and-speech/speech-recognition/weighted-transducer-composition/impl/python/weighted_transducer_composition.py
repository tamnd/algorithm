# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-transducer-composition/. The authors are listed in prov/BWQJKE.jsonl.

"""Composition of weighted finite-state transducers, with the epsilon filter.

Weights are costs -log p, as in Mohri, Pereira and Riley 2002. The semiring is
TROPICAL (min, +) or LOG_COST (-log(exp(-a) + exp(-b)), +) from nlslog. A
transducer has states 0..n-1, one start state, a final cost per final state,
and arcs (ilabel, olabel, weight, next). EPS is the empty label.

compose(t1, t2) builds only the states (q1, q2, f) that are reachable from the
start. The filter state f in {0, 1, 2} picks one way to interleave the epsilon
moves of the two machines, so that no path is counted twice:
    f = 0  after a matched move, or a move where both machines read epsilon
    f = 1  after a move of t1 alone (t1 writes epsilon, t2 waits)
    f = 2  after a move of t2 alone (t2 reads epsilon, t1 waits)
A move of t1 alone is allowed in f = 0 or 1, a move of t2 alone in f = 0 or 2,
and a move where both read epsilon only in f = 0.

With filter=False the three epsilon moves are always allowed. That counts some
paths more than once: harmless in TROPICAL (min is idempotent) but wrong in
LOG_COST.
"""

from typing import Dict, List, Tuple

from nlslog import TROPICAL, Semiring

EPS = "<eps>"


class Wfst:
    """A weighted transducer with integer states, weights as costs."""

    def __init__(self) -> None:
        self.start = 0
        self.arcs: List[List[Tuple[str, str, float, int]]] = []
        self.final: Dict[int, float] = {}

    def add_state(self) -> int:
        self.arcs.append([])
        return len(self.arcs) - 1

    def add_arc(self, q: int, ilabel: str, olabel: str, weight: float, nxt: int) -> None:
        self.arcs[q].append((ilabel, olabel, weight, nxt))

    def set_final(self, q: int, weight: float = 0.0) -> None:
        self.final[q] = weight

    def num_states(self) -> int:
        return len(self.arcs)

    def num_arcs(self) -> int:
        return sum(len(a) for a in self.arcs)


def compose(t1: Wfst, t2: Wfst, sr: Semiring = TROPICAL, filter: bool = True):
    """Return (t, pairs): the composition t1 o t2 and the triple (q1, q2, f) of each state of t.

    The output labels of t1 meet the input labels of t2. Without epsilons the
    result has at most s1 s2 states and at most e1 e2 arcs.
    Cost: O(s1 s2 d1 d2) for out-degrees d1 and d2, which is O(e1 e2).
    """
    t = Wfst()
    index: Dict[Tuple[int, int, int], int] = {}
    pairs: List[Tuple[int, int, int]] = []
    stack: List[Tuple[int, int, int]] = []

    def state_of(key):
        if key not in index:  # @line L10
            index[key] = t.add_state()
            pairs.append(key)
            stack.append(key)
        return index[key]

    # Arcs of t2 by input label, built once.
    by_in: List[Dict[str, List[Tuple[str, str, float, int]]]] = []
    for q in range(t2.num_states()):
        d: Dict[str, List[Tuple[str, str, float, int]]] = {}
        for arc in t2.arcs[q]:
            d.setdefault(arc[0], []).append(arc)
        by_in.append(d)

    t.start = state_of((t1.start, t2.start, 0))  # @line L1
    while stack:  # @line L2
        q1, q2, f = stack.pop()  # @line L3
        p = index[(q1, q2, f)]
        if q1 in t1.final and q2 in t2.final:  # @line L4
            t.set_final(p, sr.times(t1.final[q1], t2.final[q2]))
        for a, b, w1, n1 in t1.arcs[q1]:
            if b != EPS:  # @line L5
                for _, c, w2, n2 in by_in[q2].get(b, ()):
                    t.add_arc(p, a, c, sr.times(w1, w2), state_of((n1, n2, 0)))  # @line L11
        eps1 = [arc for arc in t1.arcs[q1] if arc[1] == EPS]
        eps2 = by_in[q2].get(EPS, [])
        if f == 0 or not filter:  # @line L6
            for a, _, w1, n1 in eps1:
                for _, c, w2, n2 in eps2:
                    t.add_arc(p, a, c, sr.times(w1, w2), state_of((n1, n2, 0)))
        if f != 2 or not filter:  # @line L7
            for a, _, w1, n1 in eps1:
                t.add_arc(p, a, EPS, w1, state_of((n1, q2, 1 if filter else 0)))
        if f != 1 or not filter:  # @line L8
            for _, c, w2, n2 in eps2:
                t.add_arc(p, EPS, c, w2, state_of((q1, n2, 2 if filter else 0)))
    return t, pairs  # @line L9


def relation(t: Wfst, sr: Semiring = TROPICAL, max_arcs: int = 12) -> Dict[Tuple[Tuple[str, ...], Tuple[str, ...]], float]:
    """Return the weight of each (input, output) string pair, summed over all paths of at most max_arcs arcs.

    Epsilons are dropped from the strings. For an acyclic machine with fewer
    than max_arcs arcs on every path this is the exact weighted relation.
    The number of paths can be exponential, so use it only on small machines.
    """
    out: Dict[Tuple[Tuple[str, ...], Tuple[str, ...]], float] = {}
    stack = [(t.start, (), (), sr.one, 0)]
    while stack:
        q, x, y, w, k = stack.pop()
        if q in t.final:
            key = (x, y)
            out[key] = sr.plus(out.get(key, sr.zero), sr.times(w, t.final[q]))
        if k == max_arcs:
            continue
        for a, b, wa, n in t.arcs[q]:
            stack.append((n, x + ((a,) if a != EPS else ()), y + ((b,) if b != EPS else ()), sr.times(w, wa), k + 1))
    return out
