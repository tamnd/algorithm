# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/confusion-network/. The authors are listed in prov/Q6R3VD.jsonl.

"""Confusion networks built from word lattices by lattice alignment.

This follows the clustering of Mangu, Brill and Stolcke (2000):

1. compute the posterior of every lattice arc by forward-backward, with an
   acoustic scale kappa (1 / lm_weight by default), and drop the arcs whose
   posterior is at most a threshold theta;
2. group the arcs with the same word, start time and end time into classes,
   ordered by the lattice: class A comes before class B if a path leads from
   the end of an arc of A to the start of an arc of B (transitive closure);
3. intra-word clustering: merge unordered classes of the same word, the pair
   with the largest max over arc pairs of overlap * p(e) * p(f) first, while
   that value is positive;
4. inter-word clustering: merge unordered classes, the pair with the largest
   average over word pairs of sim(w1, w2) * p(w1) * p(w2) first, until every
   pair is ordered;
5. the classes, in order, are the slots. The missing mass of a slot is the
   posterior of the empty word EPS.

The paper uses a phonetic similarity: 1 minus the edit distance of the phone
strings normalized by the sum of their lengths. This module has no
pronunciations, so word_similarity applies the same formula to letters. Pass
another function to build() to change it.

The consensus hypothesis takes the word of largest posterior in each slot. It
minimizes the expected number of errors counted along the slots, which is an
upper bound on the word error, so it approximately minimizes the expected word
error of the lattice.
"""

import math
from typing import Callable, Dict, Iterator, List, Optional, Set, Tuple

from nlslog import LOG, NEG_INF

EPS = "-"
Arc = Tuple[int, int, str, float, float]


class Lattice:
    """A word lattice whose arcs all move forward in time: time[src] < time[dst]."""

    def __init__(self) -> None:
        self.times: List[int] = []
        self.arcs: List[Arc] = []
        self.out_arcs: List[List[int]] = []
        self.start = 0
        self.final: Set[int] = set()

    def add_node(self, time: int) -> int:
        self.times.append(time)
        self.out_arcs.append([])
        return len(self.times) - 1

    def add_arc(self, src: int, dst: int, word: str, ac: float, lm: float) -> int:
        if self.times[dst] <= self.times[src]:
            raise ValueError("an arc must move forward in time")
        self.arcs.append((src, dst, word, ac, lm))
        self.out_arcs[src].append(len(self.arcs) - 1)
        return len(self.arcs) - 1

    def topo_order(self) -> List[int]:
        # Every arc moves forward in time, so sorting by time is a topological order.
        return sorted(range(len(self.times)), key=lambda v: (self.times[v], v))

    def score(self, k: int, lm_weight: float = 1.0, ip: float = 0.0) -> float:
        _, _, _, ac, lm = self.arcs[k]
        return ac + lm_weight * lm + ip

    def log_posteriors(self, lm_weight: float = 1.0, ip: float = 0.0, kappa: Optional[float] = None) -> List[float]:
        """Return the log posterior of each arc (NEG_INF if no complete path uses it)."""
        if kappa is None:
            kappa = 1.0 / lm_weight
        w = [kappa * self.score(k, lm_weight, ip) for k in range(len(self.arcs))]
        order = self.topo_order()
        alpha = [NEG_INF] * len(self.times)
        alpha[self.start] = 0.0
        for u in order:
            for k in self.out_arcs[u]:
                v = self.arcs[k][1]
                alpha[v] = LOG.plus(alpha[v], alpha[u] + w[k])
        beta = [NEG_INF] * len(self.times)
        for q in self.final:
            beta[q] = 0.0
        for u in reversed(order):
            for k in self.out_arcs[u]:
                beta[u] = LOG.plus(beta[u], w[k] + beta[self.arcs[k][1]])
        z = NEG_INF
        for q in self.final:
            z = LOG.plus(z, alpha[q])
        if z == NEG_INF:
            raise ValueError("no path from the start to a final node")
        out = []
        for k, (u, v, _, _, _) in enumerate(self.arcs):
            g = alpha[u] + w[k] + beta[v]
            out.append(g - z if g > NEG_INF else NEG_INF)
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


def edit_distance(a, b) -> int:
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return prev[-1]


def word_similarity(w1: str, w2: str) -> float:
    """1 minus the letter edit distance normalized by the sum of the lengths (a stand-in for phones)."""
    if not w1 and not w2:
        return 1.0
    return 1.0 - edit_distance(w1, w2) / (len(w1) + len(w2))


class ConfusionNetwork:
    def __init__(self, slots: List[Dict[str, float]], eps: List[float], slot_of: Dict[int, int]) -> None:
        self.slots = slots      # slots[i][w] = posterior of word w in slot i
        self.eps = eps          # eps[i] = posterior of the empty word in slot i
        self.slot_of = slot_of  # lattice arc id -> slot index, for the arcs that were kept

    def consensus_slots(self) -> List[str]:
        """The word of largest posterior in each slot, EPS included (ties go to the smaller word)."""
        out = []
        for words, e in zip(self.slots, self.eps):
            w, p = max(sorted(words.items()), key=lambda item: item[1])
            out.append(w if p >= e else EPS)  # @line L10
        return out

    def consensus(self) -> List[str]:
        return [w for w in self.consensus_slots() if w != EPS]

    def expected_errors(self, choice: List[str]) -> float:
        """Expected number of errors, counted slot by slot, of one choice per slot (EPS allowed)."""
        total = 0.0
        for words, e, w in zip(self.slots, self.eps, choice):
            total += 1.0 - (e if w == EPS else words.get(w, 0.0))
        return total

    def num_paths(self) -> int:
        n = 1
        for words, e in zip(self.slots, self.eps):
            n *= len(words) + (1 if e > 0.0 else 0)
        return n


def build(lat: Lattice, lm_weight: float = 1.0, ip: float = 0.0, kappa: Optional[float] = None,
          theta: float = 0.0, similarity: Callable[[str, str], float] = word_similarity) -> ConfusionNetwork:
    times, arcs = lat.times, lat.arcs
    logp = lat.log_posteriors(lm_weight, ip, kappa)  # @line L1
    post: Dict[int, float] = {}
    for k, g in enumerate(logp):
        if g > NEG_INF and (theta <= 0.0 or math.exp(g) > theta):
            post[k] = math.exp(g)

    # Reachability over the kept arcs, as bit masks, in reverse topological order.
    kept_out: List[List[int]] = [[] for _ in times]
    for k in post:
        kept_out[arcs[k][0]].append(k)
    reach = [0] * len(times)
    for v in reversed(lat.topo_order()):
        r = 1 << v
        for k in kept_out[v]:
            r |= reach[arcs[k][1]]
        reach[v] = r

    def before(e: int, f: int) -> bool:  # @line L2
        return (reach[arcs[e][1]] >> arcs[f][0]) & 1 == 1

    # Initial classes: the kept arcs with the same word, start time and end time.
    groups: Dict[Tuple[int, int, str], List[int]] = {}
    for k in sorted(post):
        u, v, word, _, _ = arcs[k]
        groups.setdefault((times[u], times[v], word), []).append(k)
    keys = sorted(groups)
    classes: Dict[int, List[int]] = {c: groups[key] for c, key in enumerate(keys)}
    start_of = {c: key[0] for c, key in enumerate(keys)}
    succ: Dict[int, Set[int]] = {}
    for c in sorted(classes, key=lambda c: -start_of[c]):  # @line L3
        s: Set[int] = set()
        for d in classes:
            if start_of[d] > start_of[c] and d not in s:
                if any(before(e, f) for e in classes[c] for f in classes[d]):
                    s.add(d)
                    s |= succ[d]
        succ[c] = s

    def ordered(a: int, b: int) -> bool:
        return b in succ[a] or a in succ[b]

    def merge(a: int, b: int) -> None:
        """Merge class b into class a and keep the order transitively closed."""
        preds = [p for p in classes if a in succ[p] or b in succ[p]]
        after = succ[a] | succ[b]
        for p in preds:
            succ[p] |= after
            succ[p].add(a)
            succ[p].discard(b)
        succ[a] = after
        classes[a] = classes[a] + classes[b]
        del classes[b]
        del succ[b]

    def overlap(e: int, f: int) -> float:
        s1, e1 = times[arcs[e][0]], times[arcs[e][1]]
        s2, e2 = times[arcs[f][0]], times[arcs[f][1]]
        return max(0, min(e1, e2) - max(s1, s2)) / ((e1 - s1) + (e2 - s2))

    def word_post(c: int) -> Dict[str, float]:
        out: Dict[str, float] = {}
        for k in classes[c]:
            out[arcs[k][2]] = out.get(arcs[k][2], 0.0) + post[k]
        return out

    def sim_intra(a: int, b: int) -> float:
        return max(overlap(e, f) * post[e] * post[f] for e in classes[a] for f in classes[b])

    def sim_inter(a: int, b: int) -> float:
        pa, pb = word_post(a), word_post(b)
        total = sum(similarity(w1, w2) * p1 * p2 for w1, p1 in pa.items() for w2, p2 in pb.items())
        return total / (len(pa) * len(pb))

    # Intra-word clustering. Every class still holds one word here.
    while True:  # @line L4
        best = None
        ids = sorted(classes)
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                if arcs[classes[a][0]][2] == arcs[classes[b][0]][2] and not ordered(a, b):
                    s = sim_intra(a, b)
                    if s > 0.0 and (best is None or s > best[0]):
                        best = (s, a, b)
        if best is None:
            break
        merge(best[1], best[2])  # @line L5

    # Inter-word clustering, until the order is total.
    while True:  # @line L6
        best = None
        ids = sorted(classes)
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                if not ordered(a, b):
                    s = sim_inter(a, b)
                    if best is None or s > best[0]:
                        best = (s, a, b)
        if best is None:
            break
        merge(best[1], best[2])  # @line L7

    # In a total order, the first class has the most successors.
    order = sorted(classes, key=lambda c: -len(succ[c]))
    slots: List[Dict[str, float]] = []
    eps: List[float] = []
    slot_of: Dict[int, int] = {}
    for i, c in enumerate(order):
        words = word_post(c)  # @line L8
        slots.append(words)
        e = 1.0 - sum(words.values())  # @line L9
        eps.append(e if e > 1e-12 else 0.0)  # rounding, or pruned arcs, can push the mass past 1
        for k in classes[c]:
            slot_of[k] = i
    return ConfusionNetwork(slots, eps, slot_of)
