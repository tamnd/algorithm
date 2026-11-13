# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relaxed-plan-heuristic/. The authors are listed in prov/KSWASX.jsonl.

"""The FF heuristic: the length of a relaxed plan extracted from the relaxed planning graph.

A STRIPS action is Action(name, pre, add, dele) with frozensets of facts. The
call h_ff(actions, state, goal) builds the relaxed planning graph from the
state, extracts a relaxed plan backward from the goal, and returns its length,
or math.inf when the goal is not reachable even with the deletes ignored. The
cost is O(k m n) for k layers, m actions and n facts. The value is at least
h+, the optimal relaxed plan length, and it is not admissible.
"""

import math
from collections import namedtuple
from typing import FrozenSet, Hashable, List, Optional, Sequence, Tuple

Action = namedtuple("Action", "name pre add dele")


def _levels(actions: Sequence[Action], state: FrozenSet[Hashable], goal: FrozenSet[Hashable]):
    level = {f: 0 for f in state}
    layers: List[List[int]] = []
    facts, used = frozenset(state), set()
    while not goal <= facts:
        layer = [j for j, a in enumerate(actions) if j not in used and a.pre <= facts]
        new = frozenset(f for j in layer for f in actions[j].add) - facts
        if not new:
            return None, None
        used.update(layer)
        for f in new:
            level[f] = len(layers) + 1
        layers.append(layer)
        facts = facts | new
    return level, layers


def relaxed_plan(actions: Sequence[Action], state, goal) -> Tuple[Optional[List[Action]], Optional[List[set]]]:
    """Return (relaxed plan, goal sets per level), or (None, None) if the goal is not relaxed reachable."""
    actions, state, goal = list(actions), frozenset(state), frozenset(goal)
    level, layers = _levels(actions, state, goal)  # @line L1
    if level is None:  # @line L2
        return None, None
    m = len(layers)
    goals = [set() for _ in range(m + 1)]
    need = {}
    for g in goal:
        goals[level[g]].add(g)
        need[g] = (m, 0)
    pos, count = {}, [0] * (m + 1)
    for i in range(m, 0, -1):
        for g in sorted(goals[i], key=repr):
            if any(p < need[g] and g in actions[j].add for j, p in pos.items()):
                continue
            o = min((j for j in layers[i - 1] if g in actions[j].add),
                    key=lambda j: (sum(level[p] for p in actions[j].pre), j))  # @line L3
            pos[o] = (i - 1, count[i - 1])
            count[i - 1] += 1
            for p in actions[o].pre:
                if level[p] >= 1:
                    goals[level[p]].add(p)
                    need[p] = min(need.get(p, (m + 1, 0)), pos[o])
    return [actions[j] for j in sorted(pos, key=pos.get)], goals


def h_ff(actions: Sequence[Action], state, goal) -> float:
    """The FF heuristic value of the state."""
    plan, _ = relaxed_plan(actions, state, goal)
    if plan is None:
        return math.inf
    return len(plan)  # @line L5


def helpful_actions(actions: Sequence[Action], state, goal) -> List[Action]:
    """Applicable actions that add a goal of level 1 of the extraction (FF's helpful actions)."""
    state = frozenset(state)
    _, goals = relaxed_plan(actions, state, goal)
    if goals is None or len(goals) < 2:
        return []
    return [a for a in actions if a.pre <= state and a.add & goals[1]]  # @line L4
