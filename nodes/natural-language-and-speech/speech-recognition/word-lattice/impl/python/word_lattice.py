# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-lattice/. The authors are listed in prov/5BPGS0.jsonl.

"""A word lattice: a directed acyclic graph of word hypotheses with times and scores.

Nodes carry a time (a frame index). An arc (src, dst, word, ac, lm) says that
word spans the frames time[src] .. time[dst] - 1, with the log acoustic score
ac and the log language model score lm. There is one start node and a set of
final nodes. A path from the start to a final node is one transcription.

The combined log score of an arc, as in the decoder, is

    s(a) = ac + lm_weight * lm + ip,

where lm_weight and the log insertion penalty ip are tuned heuristics. All
the queries are one pass over the nodes in topological order with a semiring
(nlslog): VITERBI (max, +) for the best path, LOG (log-add, +) for total
scores and posteriors, COUNTING for the number of paths.

Arc posteriors use an acoustic scale kappa on the combined score,
exp(kappa * s(a)); kappa = 1 / lm_weight is the usual choice, so that the
language model keeps its own scale and the acoustic scores are flattened.
"""

import math
from typing import Callable, Dict, Iterator, List, Optional, Sequence, Set, Tuple

from nlslog import COUNTING, LOG, NEG_INF, VITERBI, Semiring

Arc = Tuple[int, int, str, float, float]


class Lattice:
    def __init__(self) -> None:
        self.times: List[int] = []
        self.arcs: List[Arc] = []
        self.out_arcs: List[List[int]] = []
        self.in_arcs: List[List[int]] = []
        self.start = 0
        self.final: Set[int] = set()

    def add_node(self, time: int) -> int:
        self.times.append(time)
        self.out_arcs.append([])
        self.in_arcs.append([])
        return len(self.times) - 1

    def add_arc(self, src: int, dst: int, word: str, ac: float, lm: float) -> int:
        if self.times[dst] < self.times[src]:
            raise ValueError("an arc must not go back in time")
        self.arcs.append((src, dst, word, ac, lm))
        k = len(self.arcs) - 1
        self.out_arcs[src].append(k)
        self.in_arcs[dst].append(k)
        return k

    def num_nodes(self) -> int:
        return len(self.times)

    def topo_order(self) -> List[int]:
        """Return the nodes in an order where every arc goes forward. Raise ValueError on a cycle."""
        indeg = [len(a) for a in self.in_arcs]
        ready = [v for v in range(self.num_nodes()) if indeg[v] == 0]
        order: List[int] = []
        while ready:
            u = ready.pop()
            order.append(u)
            for k in self.out_arcs[u]:
                v = self.arcs[k][1]
                indeg[v] -= 1
                if indeg[v] == 0:
                    ready.append(v)
        if len(order) != self.num_nodes():
            raise ValueError("the lattice has a cycle")
        return order

    def score(self, k: int, lm_weight: float = 1.0, ip: float = 0.0) -> float:
        _, _, _, ac, lm = self.arcs[k]
        return ac + lm_weight * lm + ip

    def forward(self, sr: Semiring, weight: Callable[[int], object]) -> list:
        """Return alpha[v]: the semiring sum over the paths from the start to v of their weights."""
        order = self.topo_order()  # @line L1
        alpha = [sr.zero] * self.num_nodes()
        alpha[self.start] = sr.one  # @line L2
        for u in order:  # @line L3
            for k in self.out_arcs[u]:
                v = self.arcs[k][1]
                alpha[v] = sr.plus(alpha[v], sr.times(alpha[u], weight(k)))  # @line L4
        return alpha

    def backward(self, sr: Semiring, weight: Callable[[int], object]) -> list:
        """Return beta[v]: the semiring sum over the paths from v to a final node of their weights."""
        order = self.topo_order()
        beta = [sr.zero] * self.num_nodes()
        for q in self.final:  # @line L5
            beta[q] = sr.one
        for u in reversed(order):  # @line L6
            for k in self.out_arcs[u]:
                v = self.arcs[k][1]
                beta[u] = sr.plus(beta[u], sr.times(weight(k), beta[v]))  # @line L7
        return beta

    def total(self, sr: Semiring, weight: Callable[[int], object]):
        alpha = self.forward(sr, weight)
        out = sr.zero
        for q in self.final:
            out = sr.plus(out, alpha[q])
        return out

    def num_paths(self) -> int:
        return self.total(COUNTING, lambda k: 1)

    def best_path(self, lm_weight: float = 1.0, ip: float = 0.0):
        """Return (words, score) of the path with the best combined score, or ([], -inf)."""
        order = self.topo_order()
        best = [NEG_INF] * self.num_nodes()
        back: List[Optional[int]] = [None] * self.num_nodes()
        best[self.start] = 0.0
        for u in order:
            if best[u] == NEG_INF:
                continue
            for k in self.out_arcs[u]:
                v = self.arcs[k][1]
                s = best[u] + self.score(k, lm_weight, ip)
                if s > best[v]:
                    best[v], back[v] = s, k
        end = max(sorted(self.final), key=lambda q: best[q], default=None)
        if end is None or best[end] == NEG_INF:
            return [], NEG_INF
        words: List[str] = []
        v = end
        while back[v] is not None:
            k = back[v]
            words.append(self.arcs[k][2])
            v = self.arcs[k][0]
        return words[::-1], best[end]

    def arc_posteriors(self, lm_weight: float = 1.0, ip: float = 0.0, kappa: Optional[float] = None) -> List[float]:
        """Return gamma[k]: the posterior probability that a path uses arc k, with acoustic scale kappa."""
        if kappa is None:
            kappa = 1.0 / lm_weight
        w = lambda k: kappa * self.score(k, lm_weight, ip)
        alpha = self.forward(LOG, w)
        beta = self.backward(LOG, w)
        z = NEG_INF
        for q in self.final:
            z = LOG.plus(z, alpha[q])
        if z == NEG_INF:
            raise ValueError("no path from the start to a final node")
        gamma = []
        for k, (u, v, _, _, _) in enumerate(self.arcs):
            g = alpha[u] + w(k) + beta[v] - z  # @line L8
            gamma.append(math.exp(g) if g > NEG_INF else 0.0)
        return gamma

    def prune(self, beam: float, lm_weight: float = 1.0, ip: float = 0.0) -> "Lattice":
        """Return a lattice with the arcs whose best path through them is within beam of the best path."""
        w = lambda k: self.score(k, lm_weight, ip)
        alpha = self.forward(VITERBI, w)
        beta = self.backward(VITERBI, w)
        best = max((alpha[q] for q in self.final), default=NEG_INF)
        tol = 1e-9 * (1.0 + abs(best)) if best > NEG_INF else 0.0  # sums in another order round apart
        keep = [k for k, (u, v, _, _, _) in enumerate(self.arcs)
                if best > NEG_INF and alpha[u] + w(k) + beta[v] >= best - beam - tol]  # @line L9
        used = {self.start} | {q for q in self.final}
        for k in keep:
            used.add(self.arcs[k][0])
            used.add(self.arcs[k][1])
        out = Lattice()
        new_id: Dict[int, int] = {}
        for v in sorted(used):  # @line L10
            new_id[v] = out.add_node(self.times[v])
        out.start = new_id[self.start]
        out.final = {new_id[q] for q in self.final if alpha[q] >= best - beam - tol}
        for k in keep:
            u, v, word, ac, lm = self.arcs[k]
            out.add_arc(new_id[u], new_id[v], word, ac, lm)
        return out

    def paths(self) -> Iterator[List[int]]:
        """Yield every path from the start to a final node as a list of arc ids (exponential; for tests)."""
        stack: List[Tuple[int, List[int]]] = [(self.start, [])]
        while stack:
            u, path = stack.pop()
            if u in self.final:
                yield path
            for k in self.out_arcs[u]:
                stack.append((self.arcs[k][1], path + [k]))

    def words(self, path: Sequence[int]) -> List[str]:
        return [self.arcs[k][2] for k in path]
