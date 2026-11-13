# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/real-time-a-star/. The authors are listed in prov/YMQYKM.jsonl.

"""Real-time A* (Korf 1990) with a search horizon of one move.

The agent stands in a state x, looks at the successors y of x, and gives
each the value f(y) = c(x, y) + h(y), where h(y) is the stored value of y
if the agent has stored one and the heuristic h0(y) if not. It moves to a
successor with the least f and stores, for the state that it leaves, the
second least f: the estimated cost of solving the problem from x if the
agent ever comes back to x, which then means taking the best other move.
When x has only one successor, there is no second value, and this file
stores the least f.
"""

import math
from collections.abc import Callable, Hashable

INF = math.inf


def real_time_a_star(
    succ: dict,
    start: Hashable,
    goal: Hashable,
    h0: Callable[[Hashable], float],
    max_moves: int = 10**7,
    stored: dict | None = None,
) -> tuple[list, dict]:
    """Move from start to goal; return the walk and the table of stored values.

    succ maps each state to a dict {successor: cost} with positive finite
    costs. The goal must be reachable from every state. stored, if given,
    is the table of values from an earlier run and is updated in place.
    """
    for u, vs in succ.items():
        for v, c in vs.items():
            if not 0 < c < INF:
                raise ValueError("arc costs must be positive and finite")
    table: dict = {} if stored is None else stored  # @line L1
    x = start  # @line L2
    walk = [x]
    while x != goal:  # @line L3
        if len(walk) > max_moves:
            raise RuntimeError("move limit reached")
        if not succ[x]:
            raise ValueError("a state without successors is not the goal")
        f = sorted((c + table.get(y, h0(y)), i, y) for i, (y, c) in enumerate(succ[x].items()))  # @line L4
        best = f[0][2]  # @line L5
        if len(f) >= 2:  # @line L6
            table[x] = f[1][0]
        else:  # @line L7
            table[x] = f[0][0]
        x = best  # @line L8
        walk.append(x)
    return walk, table  # @line L9


def walk_cost(succ: dict, walk: list) -> float:
    return sum(succ[a][b] for a, b in zip(walk, walk[1:]))
