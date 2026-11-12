# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/streaming-k-median/. The authors are listed in prov/NTSNHM.jsonl.

"""One-pass k-median over a stream by the divide and conquer method of
Guha, Mishra, Motwani and O'Callaghan: cluster each full buffer of m
weighted points into k weighted medians, pass the medians one level up,
and cluster what is left at the end.

The local solver is weighted k-median local search with single swaps (a
b = 5 approximation in a metric), or an exact solver for small inputs.
With L levels and a final step, the cost is at most
((1 + 2c)(1 + 2b)^L - 1) times the optimum; with b = c = 5 this is
11^(L + 1) - 1.
"""

from itertools import combinations


def weighted_cost(items, centers, dist):
    """Sum of weight times distance to the nearest center."""
    return sum(w * min(dist(p, c) for c in centers) for p, w in items)


def local_search_solver(items, k, dist):
    """Weighted k-median by greedy start and best single swaps.

    items is a list of (point, weight). Returns the indices of at most k
    medians among the items. The result is a single-swap local optimum.
    """
    n = len(items)
    if n <= k:
        return list(range(n))
    w = [wt for _, wt in items]
    D = [[dist(p, q) for q, _ in items] for p, _ in items]

    def cost(meds):
        return sum(w[j] * min(D[j][m] for m in meds) for j in range(n))

    meds = [min(range(n), key=lambda i: (sum(w[j] * D[j][i] for j in range(n)), i))]
    while len(meds) < k:
        meds.append(min((i for i in range(n) if i not in meds), key=lambda i: (cost(meds + [i]), i)))
    current = cost(meds)
    while True:
        best = None
        for a in range(k):
            for h in range(n):
                if h in meds:
                    continue
                trial = meds[:a] + [h] + meds[a + 1:]
                c = cost(trial)
                if c < current and (best is None or c < best[0]):
                    best = (c, trial)
        if best is None:
            return meds
        current, meds = best


def exact_solver(items, k, dist):
    """Weighted discrete k-median by trying all sets of k items."""
    n = len(items)
    if n <= k:
        return list(range(n))
    return list(min(combinations(range(n), k),
                    key=lambda c: (weighted_cost(items, [items[i][0] for i in c], dist), c)))


def reduce_items(items, k, dist, solver):
    """Cluster weighted items into at most k weighted medians.

    Returns (medians as (point, total weight), cost of this step).
    """
    idx = solver(items, k, dist)
    centers = [items[i][0] for i in idx]
    weight = [0] * len(centers)
    step_cost = 0
    for p, w in items:
        a = min(range(len(centers)), key=lambda t: (dist(p, centers[t]), t))
        weight[a] += w
        step_cost += w * dist(p, centers[a])
    return [(centers[t], weight[t]) for t in range(len(centers)) if weight[t] > 0], step_cost


class StreamingKMedian:
    """Keep one buffer of fewer than m weighted points per level."""

    def __init__(self, k, m, dist, solver=local_search_solver):
        if not 1 <= k < m:
            raise ValueError("need 1 <= k < m")
        self.k, self.m, self.dist, self.solver = k, m, dist, solver
        self.levels = []       # levels[i]: buffer of (point, weight)
        self.level_cost = []   # level_cost[i]: total cost of the reductions at level i

    def insert(self, p, w=1):
        pending = [(0, (p, w))]
        while pending:
            i, item = pending.pop()
            if i == len(self.levels):
                self.levels.append([])
                self.level_cost.append(0)
            self.levels[i].append(item)  # @line L2
            if len(self.levels[i]) == self.m:  # @line L3
                full, self.levels[i] = self.levels[i], []
                medians, c = reduce_items(full, self.k, self.dist, self.solver)  # @line L4
                self.level_cost[i] += c
                pending.extend((i + 1, it) for it in reversed(medians))  # @line L5

    def finish(self):
        """Cluster all buffered weighted points. Returns the k medians."""
        pool = [it for buf in self.levels for it in buf]  # @line L6
        idx = self.solver(pool, self.k, self.dist)  # @line L7
        return [pool[i][0] for i in idx]

    def memory(self):
        return sum(len(buf) for buf in self.levels)


def stream_k_median(stream, k, m, dist, solver=local_search_solver):
    s = StreamingKMedian(k, m, dist, solver)
    for p in stream:  # @line L1
        s.insert(p)
    return s.finish()
