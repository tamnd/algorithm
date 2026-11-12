# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wireless-link-scheduling/. The authors are listed in prov/R3ET6W.jsonl.

"""Wireless link scheduling: choose a set of links that may transmit
together in one slot.

Interference is given as a conflict graph on the links, held as bitmasks:
conflict[l] has bit k set when links l and k cannot be active together.
A feasible schedule is an independent set of the conflict graph. The
max-weight schedule is a maximum weight independent set (MWIS), which is
NP-hard in general, so the exact solver here is exponential and meant for
small instances. The greedy maximal schedule is the usual fast rule.
The SINR model, in which a set is feasible only if every link in it has a
signal to interference and noise ratio of at least beta, is also given.
"""

from functools import lru_cache


def node_exclusive_conflicts(links: list) -> list:
    """Conflict graph under node-exclusive (primary) interference: two links
    conflict when they share an end node. This is the line graph of the
    network, so a feasible schedule is a matching."""
    m = len(links)
    conflict = [0] * m
    for a in range(m):
        for b in range(a + 1, m):
            if set(links[a]) & set(links[b]):
                conflict[a] |= 1 << b
                conflict[b] |= 1 << a
    return conflict


def is_independent(conflict: list, mask: int) -> bool:
    k = mask
    while k:
        low = k & -k
        if conflict[low.bit_length() - 1] & mask:
            return False
        k ^= low
    return True


def weight_of(w: list, mask: int) -> float:
    return sum(w[i] for i in range(len(w)) if mask >> i & 1)


def max_weight_schedule(conflict: list, w: list):
    """Exact MWIS by branching: take the lowest link of the candidate set,
    and either leave it out or put it in and drop its conflicts.
    Returns (weight, mask). Time O(2^m) in the worst case."""

    @lru_cache(maxsize=None)
    def best(cand: int):
        if cand == 0:
            return 0, 0
        low = cand & -cand
        v = low.bit_length() - 1
        rest = cand ^ low
        out_w, out_m = best(rest)
        if w[v] <= 0:
            return out_w, out_m
        in_w, in_m = best(rest & ~conflict[v])
        in_w += w[v]
        if in_w > out_w:
            return in_w, in_m | low
        return out_w, out_m

    return best((1 << len(w)) - 1)


def greedy_maximal_schedule(conflict: list, w: list) -> int:
    """Greedy maximal scheduling (longest queue first when w is the queue
    lengths): scan the links by weight, largest first, and add a link when
    it has positive weight and no conflict with the links already added."""
    chosen = 0
    for v in sorted(range(len(w)), key=lambda i: (-w[i], i)):
        if w[v] > 0 and not conflict[v] & chosen:
            chosen |= 1 << v
    return chosen


def sinr_feasible(mask: int, gain: list, power: list, noise: float, beta: float) -> bool:
    """SINR model: gain[k][l] is the gain from the sender of link k to the
    receiver of link l. Every active link l needs
    power[l] gain[l][l] >= beta (noise + sum of power[k] gain[k][l])."""
    active = [i for i in range(len(power)) if mask >> i & 1]
    for l in active:
        interference = sum(power[k] * gain[k][l] for k in active if k != l)
        if power[l] * gain[l][l] < beta * (noise + interference):
            return False
    return True
