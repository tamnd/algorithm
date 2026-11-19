# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-movers-distance/. The authors are listed in prov/ZXZK9R.jsonl.
"""Word Mover's Distance (Kusner, Sun, Kolkin and Weinberger 2015) and its lower bounds.

A document is a list of tokens. The word vectors are given as a dict from a
word to a list of floats; the code does not train them. The normalized bag of
words (nBOW) of a document gives each distinct word the share c_i / sum c_j of
its count, after the stop words and the words without a vector are removed.
WMD is the least total cost of moving the nBOW of one document onto the nBOW
of the other, where moving one unit from word i to word j costs |x_i - x_j|.

The transportation problem is solved exactly by successive shortest paths
with Bellman-Ford on integer amounts: the shares are rationals, so they are
scaled by the least common multiple of their denominators.
"""

import math
from fractions import Fraction
from typing import Dict, Iterable, List, Sequence, Tuple

Vector = Sequence[float]
Vectors = Dict[str, Vector]


def euclidean(a: Vector, b: Vector) -> float:
    return math.sqrt(math.fsum((x - y) ** 2 for x, y in zip(a, b)))


def nbow(tokens: Iterable[str], vectors: Vectors, stop_words: Iterable[str] = ()) -> Tuple[List[str], List[Fraction]]:
    """Return the distinct words of the document, in order of first use, and their shares as Fractions."""
    stop = set(stop_words)
    counts: Dict[str, int] = {}
    for t in tokens:
        if t in stop or t not in vectors:
            continue
        counts[t] = counts.get(t, 0) + 1
    total = sum(counts.values())
    if total == 0:
        raise ValueError("the document has no word with a vector")
    words = list(counts)
    return words, [Fraction(counts[w], total) for w in words]


def transport(supply: Sequence[int], demand: Sequence[int], cost: Sequence[Sequence[float]]) -> Tuple[float, List[List[int]]]:
    """Solve min sum F_ij cost_ij subject to row sums supply and column sums demand, F >= 0.

    The amounts are integers with equal totals. Successive shortest paths:
    each round finds a cheapest path from the source to the sink in the
    residual network with Bellman-Ford and pushes the bottleneck amount along
    it. Returns (the least cost, the integer flow matrix).
    """
    m, n = len(supply), len(demand)
    if sum(supply) != sum(demand):
        raise ValueError("the supplies and the demands must have the same total")
    if any(a < 0 for a in supply) or any(b < 0 for b in demand):
        raise ValueError("the amounts must not be negative")
    flow = [[0] * n for _ in range(m)]  # @line L4
    left = list(supply)
    need = list(demand)
    # Nodes: 0 .. m-1 supply words, m .. m+n-1 demand words, s = m+n, t = m+n+1.
    s, t = m + n, m + n + 1
    eps = 1e-12
    while any(left):  # @line L5
        dist = [math.inf] * (m + n + 2)
        prev: List[Tuple[int, int]] = [(-1, -1)] * (m + n + 2)
        dist[s] = 0.0
        for _ in range(m + n + 1):  # @line L6
            changed = False
            for i in range(m):
                if left[i] > 0 and dist[s] + eps < dist[i]:
                    dist[i], prev[i] = dist[s], (s, 0)
                    changed = True
            for i in range(m):
                if dist[i] == math.inf:
                    continue
                for j in range(n):
                    if dist[i] + cost[i][j] + eps < dist[m + j]:
                        dist[m + j], prev[m + j] = dist[i] + cost[i][j], (i, 1)
                        changed = True
            for j in range(n):
                if dist[m + j] == math.inf:
                    continue
                for i in range(m):
                    if flow[i][j] > 0 and dist[m + j] - cost[i][j] + eps < dist[i]:
                        dist[i], prev[i] = dist[m + j] - cost[i][j], (m + j, -1)
                        changed = True
                if need[j] > 0 and dist[m + j] + eps < dist[t]:
                    dist[t], prev[t] = dist[m + j], (m + j, 0)
                    changed = True
            if not changed:
                break
        path = []
        v = t
        while v != s:
            u, kind = prev[v]
            path.append((u, v, kind))
            v = u
        path.reverse()
        delta = min(left[path[0][1]], need[path[-1][0] - m])  # @line L7
        for u, v, kind in path:
            if kind == -1:
                delta = min(delta, flow[v][u - m])
        for u, v, kind in path:  # @line L8
            if kind == 1:
                flow[u][v - m] += delta
            elif kind == -1:
                flow[v][u - m] -= delta
        left[path[0][1]] -= delta
        need[path[-1][0] - m] -= delta
    total = math.fsum(flow[i][j] * cost[i][j] for i in range(m) for j in range(n))
    return total, flow


def wmd_with_flow(
    doc1: Iterable[str], doc2: Iterable[str], vectors: Vectors, stop_words: Iterable[str] = ()
) -> Tuple[float, List[str], List[str], List[List[Fraction]]]:
    """Return (WMD, words of doc1, words of doc2, the optimal flow T as Fractions)."""
    w1, d1 = nbow(doc1, vectors, stop_words)  # @line L1
    w2, d2 = nbow(doc2, vectors, stop_words)
    cost = [[euclidean(vectors[a], vectors[b]) for b in w2] for a in w1]  # @line L2
    scale = math.lcm(*(f.denominator for f in d1 + d2))  # @line L3
    supply = [int(f * scale) for f in d1]
    demand = [int(f * scale) for f in d2]
    total, flow = transport(supply, demand, cost)
    T = [[Fraction(x, scale) for x in row] for row in flow]
    return total / scale, w1, w2, T  # @line L9


def wmd(doc1: Iterable[str], doc2: Iterable[str], vectors: Vectors, stop_words: Iterable[str] = ()) -> float:
    """The Word Mover's Distance between two documents."""
    return wmd_with_flow(doc1, doc2, vectors, stop_words)[0]


def wcd(doc1: Iterable[str], doc2: Iterable[str], vectors: Vectors, stop_words: Iterable[str] = ()) -> float:
    """The word centroid distance |X d - X' d'|, a lower bound of WMD. O(d p) time."""
    w1, d1 = nbow(doc1, vectors, stop_words)
    w2, d2 = nbow(doc2, vectors, stop_words)
    dim = len(vectors[w1[0]])
    c1 = [math.fsum(float(f) * vectors[w][k] for w, f in zip(w1, d1)) for k in range(dim)]
    c2 = [math.fsum(float(f) * vectors[w][k] for w, f in zip(w2, d2)) for k in range(dim)]
    return euclidean(c1, c2)


def rwmd(doc1: Iterable[str], doc2: Iterable[str], vectors: Vectors, stop_words: Iterable[str] = ()) -> float:
    """The relaxed WMD max(l1, l2), a lower bound of WMD. O(d p^2) time.

    l1 drops the column constraints, so each word of doc1 moves all its share
    to its nearest word of doc2; l2 drops the row constraints.
    """
    w1, d1 = nbow(doc1, vectors, stop_words)
    w2, d2 = nbow(doc2, vectors, stop_words)
    cost = [[euclidean(vectors[a], vectors[b]) for b in w2] for a in w1]
    l1 = math.fsum(float(d1[i]) * min(cost[i]) for i in range(len(w1)))
    l2 = math.fsum(float(d2[j]) * min(cost[i][j] for i in range(len(w1))) for j in range(len(w2)))
    return max(l1, l2)


def knn(
    query: Sequence[str], docs: Sequence[Sequence[str]], vectors: Vectors, k: int, stop_words: Iterable[str] = ()
) -> Tuple[List[Tuple[float, int]], int]:
    """Exact k nearest documents by WMD, with prefetch by WCD and pruning by RWMD.

    Returns (the k pairs (distance, index) in order, the number of exact WMD
    computations). A document whose RWMD is at least the current k-th
    distance cannot enter the k nearest, so its WMD is skipped.
    """
    stop = list(stop_words)
    order = sorted(range(len(docs)), key=lambda i: wcd(query, docs[i], vectors, stop))
    best: List[Tuple[float, int]] = []
    exact = 0
    for i in order:
        if len(best) == k and rwmd(query, docs[i], vectors, stop) >= best[-1][0]:
            continue
        dist = wmd(query, docs[i], vectors, stop)
        exact += 1
        best.append((dist, i))
        best.sort()
        del best[k:]
    return best, exact
