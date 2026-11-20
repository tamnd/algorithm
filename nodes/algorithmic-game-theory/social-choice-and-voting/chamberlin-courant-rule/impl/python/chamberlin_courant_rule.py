# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chamberlin-courant-rule/. The authors are listed in prov/EKGPRX.jsonl.
"""The Chamberlin-Courant rule with Borda misrepresentation.

A profile is a sequence of n rankings of the candidates 0, ..., m - 1, best first. A voter is
represented by the member of the committee W that it ranks highest. Its misrepresentation is
the position of that member in its ranking (0 for the top), and its satisfaction is m - 1 minus
this position, the Borda score. The rule elects a committee of k candidates with the least
total misrepresentation, which is the same as the largest total satisfaction.

Three algorithms:
- chamberlin_courant: exact search over all committees, ties to the lexicographically first;
- cc_single_peaked: exact dynamic program for profiles single-peaked on a given axis;
- greedy_cc: the greedy algorithm, a 1 - 1/e approximation of the satisfaction.
"""

from itertools import combinations
from typing import Sequence, Tuple


def _positions(profile, m):
    pos = []
    for r in profile:
        p = [0] * m
        for i, a in enumerate(r):
            p[a] = i
        pos.append(p)
    return pos


def misrepresentation(profile, m: int, committee) -> int:
    """Total Borda misrepresentation: the sum over voters of the best position of a member."""
    pos = _positions(profile, m)
    return sum(min(p[c] for c in committee) for p in pos)


def satisfaction(profile, m: int, committee) -> int:
    """Total Borda satisfaction: n (m - 1) minus the misrepresentation; 0 for the empty committee."""
    if not committee:
        return 0
    return len(profile) * (m - 1) - misrepresentation(profile, m, committee)


def chamberlin_courant(profile, m: int, k: int) -> Tuple[int, ...]:
    """Return the lexicographically first committee of size k with the least misrepresentation.

    Exact search over all C(m, k) committees: O(C(m, k) n k) time after O(m n) setup.
    """
    if not 1 <= k <= m:
        raise ValueError("need 1 <= k <= m")
    pos = _positions(profile, m)
    best, best_cost = None, None
    for W in combinations(range(m), k):
        cost = sum(min(p[c] for c in W) for p in pos)
        if best_cost is None or cost < best_cost:
            best, best_cost = W, cost
    return best


def cc_single_peaked(profile, m: int, k: int, axis: Sequence[int]) -> Tuple[Tuple[int, ...], int]:
    """Return (committee, misrepresentation) of an optimal committee of size k.

    The profile must be single-peaked on the axis, a tuple of all candidates from left to right.
    Then every voter is best represented by the nearest chosen candidate on the left of its
    peak or the nearest one on the right, and a dynamic program over the axis finds the optimum
    in O(m^2 (n + k)) time and O(m^2 + m n) space.
    """
    if not 1 <= k <= m:
        raise ValueError("need 1 <= k <= m")
    pos = _positions(profile, m)
    where = {a: t for t, a in enumerate(axis)}
    peak = [where[r[0]] for r in profile]
    # cost[i][t]: misrepresentation of voter i by the candidate at axis place t
    cost = [[p[axis[t]] for t in range(m)] for p in pos]
    head = [0] * m  # @line L1
    tail = [0] * m
    for i in range(len(profile)):
        for t in range(m):
            if peak[i] < t:
                head[t] += cost[i][t]
            else:
                tail[t] += cost[i][t]
    seg = [[0] * m for _ in range(m)]  # @line L2
    for i in range(len(profile)):
        ci, q = cost[i], peak[i]
        for s in range(q + 1):
            for t in range(q + 1, m):
                seg[s][t] += min(ci[s], ci[t])
    INF = None
    F = [[INF] * m for _ in range(k + 1)]
    back = [[-1] * m for _ in range(k + 1)]
    for t in range(m):  # @line L3
        F[1][t] = head[t]
    for j in range(2, k + 1):  # @line L4
        for t in range(j - 1, m):  # @line L5
            best, arg = None, -1
            for s in range(j - 2, t):  # @line L6
                v = F[j - 1][s] + seg[s][t]
                if best is None or v < best:
                    best, arg = v, s
            F[j][t], back[j][t] = best, arg
    t_best, total = -1, None
    for t in range(k - 1, m):  # @line L7
        v = F[k][t] + tail[t]
        if total is None or v < total:
            t_best, total = t, v
    chosen, t = [], t_best  # @line L8
    for j in range(k, 0, -1):
        chosen.append(axis[t])
        t = back[j][t]
    return tuple(sorted(chosen)), total  # @line L9


def greedy_cc(profile, m: int, k: int) -> Tuple[int, ...]:
    """Add k candidates one at a time, each with the largest gain in satisfaction.

    Ties go to the smallest index. O(k m n) time. The satisfaction of the result is at least
    1 - (1 - 1/k)^k > 1 - 1/e of the optimum.
    """
    if not 1 <= k <= m:
        raise ValueError("need 1 <= k <= m")
    pos = _positions(profile, m)
    best_sat = [0] * len(profile)  # satisfaction of each voter with the committee so far
    W = []
    for _ in range(k):
        pick, pick_gain = None, None
        for c in range(m):
            if c in W:
                continue
            gain = sum(max(0, m - 1 - p[c] - b) for p, b in zip(pos, best_sat))
            if pick_gain is None or gain > pick_gain:
                pick, pick_gain = c, gain
        W.append(pick)
        best_sat = [max(b, m - 1 - p[pick]) for p, b in zip(pos, best_sat)]
    return tuple(sorted(W))
