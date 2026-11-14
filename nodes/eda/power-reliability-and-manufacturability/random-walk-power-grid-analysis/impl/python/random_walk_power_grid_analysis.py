# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-walk-power-grid-analysis/. The authors are listed in prov/4F39NW.jsonl.
"""Random walk power grid analysis after Qian, Nassif and Sapatnekar (2003, 2005).

The grid is in drop form: G x = cur, with G = L + diag(gpad). At node m let
D_m = sum of the wire conductances at m plus gpad[m]. A walk at m pays the
reward cur[m] / D_m, then stops at the pad with probability gpad[m] / D_m, or
moves to the neighbor j with probability g_mj / D_m. The expected total reward
of a walk that starts at k is the drop x_k. The estimate is the mean of
independent walks.
"""

from __future__ import annotations

import bisect
import math
import random
from typing import List, Tuple

from pgrid import Grid


class WalkTables:
    """For each node: the reward, the cumulative step table and its targets."""

    def __init__(self, grid: Grid):
        if not grid.every_part_has_a_pad():
            raise ValueError("a part of the grid has no pad: the drop is not defined")
        self.reward: List[float] = []
        self.cum: List[List[float]] = []
        self.target: List[List[int]] = []
        for m in range(grid.n):
            d = float(grid.degree(m))
            self.reward.append(float(grid.cur[m]) / d)
            acc, cum, tgt = 0.0, [], []
            for j, g in sorted(grid.adj[m].items()):
                acc += float(g) / d
                cum.append(acc)
                tgt.append(j)
            self.cum.append(cum)
            self.target.append(tgt)
        # The rest of each table, 1 - cum[-1], is the probability gpad / D of stopping.


def one_walk(t: WalkTables, k: int, rng: random.Random) -> Tuple[float, int]:
    """One walk from k: its total reward and its number of steps."""
    m, total, steps = k, 0.0, 0  # @line L3
    while True:  # @line L4
        total += t.reward[m]  # @line L5: pay cur[m] / D_m at each visit
        u = rng.random()  # @line L6
        cum = t.cum[m]
        i = bisect.bisect_right(cum, u)
        if i == len(cum):  # @line L6: u fell in the pad part, the walk stops
            return total, steps
        m = t.target[m][i]  # @line L7: move to neighbor j with probability g_mj / D_m
        steps += 1


def estimate_drop(grid: Grid, k: int, walks: int, rng: random.Random):
    """Mean drop at k over the walks, its standard error, and the mean walk length."""
    t = WalkTables(grid)
    s = s2 = 0.0  # @line L1
    steps = 0
    for _ in range(walks):  # @line L2
        r, n = one_walk(t, k, rng)
        s += r  # @line L8
        s2 += r * r
        steps += n
    mean = s / walks  # @line L9
    var = max(s2 / walks - mean * mean, 0.0) * walks / max(walks - 1, 1)
    return mean, math.sqrt(var / walks), steps / walks


def first_step_identity(grid: Grid, x) -> List[object]:
    """x_m - (cur[m] + sum_j g_mj x_j) / D_m for every node m.

    It is zero for every m exactly when G x = cur (the discrete harmonic property
    with sources).
    """
    out = []
    for m in range(grid.n):
        d = grid.degree(m)
        s = grid.cur[m]
        for j, g in grid.adj[m].items():
            s = s + g * x[j]
        out.append(x[m] - s / d)
    return out
