# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-tardy-jobs/. The authors are listed in prov/44W58E.jsonl.

"""1||sum w_j U_j: the Lawler-Moore dynamic program and an FPTAS by rounding the weights."""

from fractions import Fraction
from typing import Sequence


def is_feasible(p: Sequence[int], d: Sequence[int], jobs) -> bool:
    """True if all the given jobs are on time in EDD order from time 0."""
    t = 0
    for j in sorted(jobs, key=lambda j: d[j]):
        t += p[j]
        if t > d[j]:
            return False
    return True


def _check(p, d, w):
    n = len(p)
    if not (len(d) == len(w) == n):
        raise ValueError("p, d and w must have the same length")
    if any(x < 0 for x in p) or any(x < 0 for x in w):
        raise ValueError("p and w must be nonnegative")


def lawler_moore(p: Sequence[int], d: Sequence[int], w: Sequence[int]) -> tuple[list[int], list[int], int]:
    """Exact: return (on-time jobs in EDD order, late jobs, least late weight).

    F[t] is the least late weight among the jobs seen so far when the on-time
    ones take exactly t units. Time O(n * sum(p)), space O(n * sum(p)) bits.
    """
    _check(p, d, w)
    n = len(p)
    edd = sorted(range(n), key=lambda j: (d[j], j))
    total = sum(p)
    inf = None
    f: list = [0] + [inf] * total
    keep: list[bytearray] = []  # keep[i][t] = 1 if job edd[i] is on time in the best state t
    for k in edd:
        g = [None if v is None else v + w[k] for v in f]
        choice = bytearray(total + 1)
        hi = min(total, d[k])
        for t in range(p[k], hi + 1):
            v = f[t - p[k]]
            if v is not None and (g[t] is None or v < g[t]):
                g[t] = v
                choice[t] = 1
        f = g
        keep.append(choice)
    best_t = min((t for t in range(total + 1) if f[t] is not None), key=lambda t: f[t])
    value = f[best_t]
    on_time: list[int] = []
    t = best_t
    for i in range(n - 1, -1, -1):
        if keep[i][t]:
            on_time.append(edd[i])
            t -= p[edd[i]]
    on_time.reverse()
    on_set = set(on_time)
    late = [j for j in edd if j not in on_set]
    return on_time, late, value


def fptas(p: Sequence[int], d: Sequence[int], w: Sequence[int], eps) -> tuple[list[int], list[int], int]:
    """Return (on-time jobs in EDD order, late jobs, late weight) with late weight <= (1 + eps) OPT.

    Time O(n^3 / eps) after sorting.
    """
    _check(p, d, w)
    eps = Fraction(eps)
    if eps <= 0:
        raise ValueError("eps must be positive")
    n = len(p)
    edd = sorted(range(n), key=lambda j: (d[j], j))
    if is_feasible(p, d, range(n)):  # @line L1
        return edd, [], 0
    levels = sorted(set(w), reverse=True)  # @line L2
    tstar = next(x for x in levels if not is_feasible(p, d, [j for j in range(n) if w[j] >= x]))
    scale = eps * tstar / n  # @line L3
    wr = [int(Fraction(x) / scale) for x in w]
    cap = int(n * tstar / scale)  # @line L4
    # g[W] = least on-time processing time with rounded late weight exactly W
    g: list = [0] + [None] * cap
    late_choice: list[bytearray] = []
    for k in edd:  # @line L5
        h: list = [None] * (cap + 1)
        choice = bytearray(cap + 1)
        for W in range(cap + 1):
            v = g[W]
            if v is not None and v + p[k] <= d[k]:
                h[W] = v + p[k]
            if W >= wr[k]:
                u = g[W - wr[k]]
                if u is not None and (h[W] is None or u < h[W]):
                    h[W] = u
                    choice[W] = 1
        g = h
        late_choice.append(choice)
    best = next(W for W in range(cap + 1) if g[W] is not None)  # @line L6
    late: list[int] = []
    W = best
    for i in range(n - 1, -1, -1):
        if late_choice[i][W]:
            late.append(edd[i])
            W -= wr[edd[i]]
    late_set = set(late)
    on_time = [j for j in edd if j not in late_set]
    return on_time, sorted(late), sum(w[j] for j in late)  # @line L7


def late_weight(p: Sequence[int], d: Sequence[int], w: Sequence[int], order: Sequence[int]) -> int:
    """Weight of the late jobs when the order runs back to back from time 0."""
    t, s = 0, 0
    for j in order:
        t += p[j]
        if t > d[j]:
            s += w[j]
    return s
