# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-degree-anonymization/. The authors are listed in prov/X8DF57.jsonl.

from collections.abc import Sequence

Edge = tuple[int, int]


def anonymize_degrees(d: Sequence[int], k: int) -> tuple[list[int], int]:
    """Return the k-anonymous sequence closest to d in L1 distance with no entry lowered, and that distance.

    Precondition: d is sorted in non-increasing order, k >= 1, and len(d) is 0
    or at least k. Ties go to the smallest cut. Cost: O(n k) time, O(n) space.
    """
    n = len(d)
    if 0 < n < k or k < 1:
        raise ValueError("need k >= 1 and n = 0 or n >= k")
    prefix = [0] * (n + 1)
    for j in range(n):
        prefix[j + 1] = prefix[j] + d[j]

    def cost(a: int, b: int) -> int:
        # I(a, b) for the 1-based positions a..b: raise them all to d(a)
        return (b - a + 1) * d[a - 1] - (prefix[b] - prefix[a - 1])

    da = [0] * (n + 1)
    cut = [0] * (n + 1)
    for i in range(1, n + 1):  # @line L2
        if i < 2 * k:  # @line L3
            da[i], cut[i] = cost(1, i), 0
        else:  # @line L4
            best_t = max(k, i - 2 * k + 1)
            best = da[best_t] + cost(best_t + 1, i)
            for t in range(best_t + 1, i - k + 1):
                c = da[t] + cost(t + 1, i)
                if c < best:
                    best, best_t = c, t
            da[i], cut[i] = best, best_t
    out = list(d)
    i = n
    while i > 0:  # @line L5
        t = cut[i]
        for j in range(t, i):
            out[j] = d[t]
        i = t
    return out, da[n]


def k_degree_anonymize(n: int, edges: Sequence[Edge], k: int) -> list[Edge] | None:
    """Return edges to add to the simple graph so that it becomes k-degree anonymous, or None for UNKNOWN.

    The vertices are 0..n-1. When a list comes back, its length is the least
    possible number of added edges. None means that Supergraph got stuck, not
    that no answer exists. Precondition: the edges form a simple graph and
    n = 0 or n >= k >= 1. Cost: O(n log n + n k) for the degree step and
    O(n^2 log n) for the construction step as coded.
    """
    adj: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    order = sorted(range(n), key=lambda v: (-len(adj[v]), v))  # @line L1
    target, _ = anonymize_degrees([len(adj[v]) for v in order], k)
    rank = {v: r for r, v in enumerate(order)}
    a = [0] * n
    for r, v in enumerate(order):  # @line L6
        a[v] = target[r] - len(adj[v])
    if sum(a) % 2:  # @line L7
        return None
    added: list[Edge] = []
    while any(x > 0 for x in a):  # @line L8
        v = max(range(n), key=lambda u: (a[u], -rank[u]))  # @line L9
        cand = sorted((w for w in range(n) if w != v and w not in adj[v] and a[w] > 0), key=lambda w: (-a[w], rank[w]))
        chosen = cand[: a[v]]  # @line L10
        if len(chosen) < a[v]:  # @line L11
            return None
        for w in chosen:  # @line L12
            adj[v].add(w)
            adj[w].add(v)
            a[w] -= 1
            added.append((min(v, w), max(v, w)))
        a[v] = 0  # @line L13
    return added  # @line L14
