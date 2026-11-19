# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weight-pushing/. The authors are listed in prov/GPP9K3.jsonl.

"""Weight pushing of a weighted automaton or transducer (Mohri 1997, 2002).

Weights are costs -log p. The semiring is TROPICAL (min, +) or LOG_COST
(-log(exp(-a) + exp(-b)), +) from nlslog. Dividing by a finite cost is
subtracting it.

A machine has states 0..n-1, a start state with an initial weight, a final
cost per final state, and arcs (ilabel, olabel, weight, next). Labels play no
part in pushing.

shortest_distance_to_final computes d[q], the semiring sum over all paths from
q to a final state of the path weight times the final weight. It is the
generic single-source shortest-distance algorithm of Mohri 2002, run on the
reversed machine from the final states, with a FIFO queue. It is exact in the
tropical semiring when no cycle has a negative cost. In the log semiring it
stops when no distance changes by more than delta.

push(m) then sets, for every state q with d[q] finite,
    w(e)    <- d[p]^-1 (x) w(e) (x) d[n]   = w(e) + d[n] - d[p]  on costs
    lambda  <- lambda (x) d[i]             = lambda + d[i]
    rho(q)  <- d[q]^-1 (x) rho(q)          = rho(q) - d[q]
States that reach no final state (d = +inf) are dropped first.
"""

from collections import deque
from typing import Dict, List, Tuple

from nlslog import TROPICAL, Semiring


class Machine:
    """A weighted transducer with integer states and costs. An acceptor has ilabel == olabel."""

    def __init__(self) -> None:
        self.start = 0
        self.initial = 0.0
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


def _changed(sr: Semiring, old: float, new: float, delta: float) -> bool:
    if sr.idempotent:
        return new != old
    if old == sr.zero:
        return new != old
    return abs(new - old) > delta


def shortest_distance_to_final(m: Machine, sr: Semiring = TROPICAL, delta: float = 1e-12, max_pops: int = 10 ** 6) -> List[float]:
    """Return d[q] for every state q: the semiring sum over the paths from q to a final state."""
    n = m.num_states()
    incoming: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
    for p in range(n):
        for _, _, w, q in m.arcs[p]:
            incoming[q].append((p, w))
    d = [sr.zero] * n
    r = [sr.zero] * n
    queue: deque = deque()
    queued = [False] * n
    for q, rho in m.final.items():  # @line L1
        d[q] = sr.plus(d[q], rho)
        r[q] = sr.plus(r[q], rho)
        queue.append(q)
        queued[q] = True
    pops = 0
    while queue:  # @line L2
        q = queue.popleft()  # @line L3
        queued[q] = False
        pops += 1
        if pops > max_pops:
            raise RuntimeError("the shortest distance does not converge")
        rq, r[q] = r[q], sr.zero  # @line L4
        for p, w in incoming[q]:  # @line L5
            extra = sr.times(w, rq)
            new = sr.plus(d[p], extra)
            if _changed(sr, d[p], new, delta):  # @line L6
                d[p] = new
                r[p] = sr.plus(r[p], extra)
                if not queued[p]:  # @line L7
                    queue.append(p)
                    queued[p] = True
    return d


def push(m: Machine, sr: Semiring = TROPICAL, delta: float = 1e-12) -> Machine:
    """Return a new machine with the weights pushed toward the start state.

    Every string pair keeps its weight. Raise ValueError if no final state can
    be reached from the start.
    """
    d = shortest_distance_to_final(m, sr, delta)
    if d[m.start] == sr.zero:  # @line L8
        raise ValueError("no successful path")
    out = Machine()
    keep = [q for q in range(m.num_states()) if d[q] != sr.zero]  # @line L9
    new_id = {q: k for k, q in enumerate(keep)}
    for _ in keep:
        out.add_state()
    out.start = new_id[m.start]
    out.initial = sr.times(m.initial, d[m.start])  # @line L10
    for p in keep:
        for a, b, w, n in m.arcs[p]:  # @line L11
            if n in new_id:
                out.add_arc(new_id[p], a, b, sr.times(w, d[n]) - d[p], new_id[n])
        if p in m.final:  # @line L12
            out.set_final(new_id[p], m.final[p] - d[p])
    return out


def string_weight(m: Machine, x, sr: Semiring = TROPICAL) -> float:
    """Return the weight of the input string x in an epsilon-free acceptor m."""
    cur = {m.start: m.initial}
    for c in x:
        nxt: Dict[int, float] = {}
        for q, w in cur.items():
            for a, _, wa, n in m.arcs[q]:
                if a == c:
                    nxt[n] = sr.plus(nxt.get(n, sr.zero), sr.times(w, wa))
        cur = nxt
    total = sr.zero
    for q, w in cur.items():
        if q in m.final:
            total = sr.plus(total, sr.times(w, m.final[q]))
    return total
