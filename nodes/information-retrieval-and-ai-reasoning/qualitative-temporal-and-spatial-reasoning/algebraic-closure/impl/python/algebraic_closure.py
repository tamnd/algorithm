# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algebraic-closure/. The authors are listed in prov/DTG755.jsonl.

"""Algebraic closure of a qualitative constraint network.

The network is closed when R[i][j] is a subset of R[i][k] composed with
R[k][j] for all nodes i, j, k, with composition read from the composition
table of the calculus. The algorithm keeps a queue of pairs whose label
changed and revises the two triangles of each pair with every third node.
"""

from collections import deque
from itertools import combinations

from qcn import Calculus, Network, label


def algebraic_closure(calc: Calculus, n: int, net: Network,
                      stats: dict[str, int] | None = None) -> Network | None:
    """Return the largest algebraically closed subnetwork of net, or None if
    it has an empty label (then net is inconsistent).

    net maps pairs (i, j), i < j, of the nodes 0 .. n-1 to relation masks; a
    missing pair has the universal relation. The input is not changed.
    Cost: at most n(n-1)/2 * (1 + |B|) pairs leave the queue, and each costs
    O(n) compositions, so O(|B| n^3) table operations.
    """
    if stats is None:
        stats = {}
    stats["pops"] = 0
    r = [[label(calc, net, i, j) for j in range(n)] for i in range(n)]
    if any(r[i][j] == 0 for i, j in combinations(range(n), 2)):  # @line L1
        return None
    queue = deque(combinations(range(n), 2))  # @line L2
    queued = set(queue)

    def push(a: int, b: int) -> None:
        key = (a, b) if a < b else (b, a)
        if key not in queued:
            queued.add(key)
            queue.append(key)

    while queue:  # @line L3
        i, j = queue.popleft()  # @line L4
        queued.discard((i, j))
        stats["pops"] += 1
        for k in range(n):  # @line L5
            if k == i or k == j:
                continue
            t = r[i][k] & calc.compose(r[i][j], r[j][k])  # @line L6
            if t != r[i][k]:  # @line L7
                if t == 0:  # @line L8
                    return None
                r[i][k], r[k][i] = t, calc.converse(t)  # @line L9
                push(i, k)
            t = r[k][j] & calc.compose(r[k][i], r[i][j])  # @line L10
            if t != r[k][j]:  # @line L11
                if t == 0:  # @line L12
                    return None
                r[k][j], r[j][k] = t, calc.converse(t)  # @line L13
                push(k, j)
    return {(i, j): r[i][j] for i, j in combinations(range(n), 2)}  # @line L14
