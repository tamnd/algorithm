# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-real-time-a-star/. The authors are listed in prov/D7J46M.jsonl.

"""Learning real-time A* (Korf 1990) with a search horizon of one move.

The agent stands in a state x, gives each successor y the value
f(y) = c(x, y) + H(y), stores the least f as the new value H(x), and moves
to a successor with that least f. H starts as the heuristic h0 and is kept
from one trial to the next, so the agent learns. With an admissible h0 the
values stay lower bounds, and repeated trials from the same start reach a
trial that changes no value; that trial and all later ones are optimal.
"""

import math
from collections.abc import Callable, Hashable

INF = math.inf


class LRTAStar:
    def __init__(self, succ: dict, goal: Hashable, h0: Callable[[Hashable], float]):
        """succ maps each state to a dict {successor: cost} with positive finite costs."""
        for u, vs in succ.items():
            for v, c in vs.items():
                if not 0 < c < INF:
                    raise ValueError("arc costs must be positive and finite")
        self.succ, self.goal, self.h0 = succ, goal, h0
        self.H: dict = {}  # the learned values; a state not in H has the value h0

    def value(self, s) -> float:
        return self.H.get(s, self.h0(s))

    def trial(self, start: Hashable, max_moves: int = 10**7) -> tuple[list, bool]:
        """One trial from start to the goal. Return the walk and whether a value changed."""
        x = start  # @line L1
        walk = [x]
        changed = False
        while x != self.goal:  # @line L2
            if len(walk) > max_moves:
                raise RuntimeError("move limit reached")
            if not self.succ[x]:
                raise ValueError("a state without successors is not the goal")
            best, best_f = None, INF
            for y, c in self.succ[x].items():  # @line L3
                fy = c + self.value(y)
                if fy < best_f:  # @line L4
                    best, best_f = y, fy
            if best_f != self.value(x):
                changed = True
            self.H[x] = best_f  # @line L5
            x = best  # @line L6
            walk.append(x)
        return walk, changed  # @line L7

    def trials(self, start: Hashable, max_trials: int = 10**6) -> list:
        """Repeat trials until one changes no value. Return the cost of each trial."""
        costs = []
        while len(costs) < max_trials:  # @line L8
            walk, changed = self.trial(start)  # @line L9
            costs.append(sum(self.succ[a][b] for a, b in zip(walk, walk[1:])))
            if not changed:  # @line L10
                break
        return costs  # @line L11
