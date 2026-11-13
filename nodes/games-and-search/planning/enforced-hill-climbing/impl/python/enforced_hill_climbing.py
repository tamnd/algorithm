# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/enforced-hill-climbing/. The authors are listed in prov/K6E90E.jsonl.

"""Enforced hill climbing (Hoffmann and Nebel 2001, Figure 3).

The search starts in the initial state. From the current state s it runs a
breadth-first search for the nearest state that is a goal or has a strictly
smaller heuristic value than s, appends the path to that state to the plan,
and continues from there. It never takes a step back, so it fails when a
breadth-first search runs out of states.

The caller gives successors(s), which yields pairs (action, next state),
h(s), a number or math.inf, and is_goal(s). States must be hashable. States
with h = math.inf are dead ends for an exact dead-end test such as the FF
heuristic, so they are not expanded. The result is a list of actions, or
None on failure.
"""

import math
from collections import deque
from typing import Callable, Hashable, Iterable, List, Optional, Tuple


def enforced_hill_climbing(init: Hashable,
                           successors: Callable[[Hashable], Iterable[Tuple[object, Hashable]]],
                           h: Callable[[Hashable], float],
                           is_goal: Callable[[Hashable], bool],
                           stats: Optional[dict] = None) -> Optional[List[object]]:
    """Return a plan from init to a goal state, or None when a breadth-first search fails."""
    s, plan = init, []  # @line L1
    hs = h(s)
    depths = []
    if stats is not None:
        stats["depths"] = depths
    if hs == math.inf:  # @line L2
        return None
    while not is_goal(s):  # @line L3
        found = _better(s, hs, successors, h, is_goal)  # @line L4
        if found is None:  # @line L5
            return None
        path, s, hs = found
        plan.extend(path)  # @line L6
        depths.append(len(path))
    return plan  # @line L7


def _better(s, hs, successors, h, is_goal):
    """Breadth-first search from s for the nearest goal state or state with h below hs."""
    parent = {s: None}  # @line L8
    queue = deque([s])
    while queue:  # @line L9
        u = queue.popleft()  # @line L10
        for a, t in successors(u):  # @line L11
            if t in parent:
                continue
            parent[t] = (u, a)  # @line L12
            ht = h(t)
            if is_goal(t) or ht < hs:  # @line L13
                path, x = [], t
                while parent[x] is not None:
                    x, b = parent[x]
                    path.append(b)
                return path[::-1], t, ht
            if ht < math.inf:  # @line L14
                queue.append(t)
    return None  # @line L15
