# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relaxed-planning-graph/. The authors are listed in prov/ZT81NP.jsonl.

"""The relaxed planning graph of the FF planner, and relaxed plan extraction.

A STRIPS action is Action(name, pre, add, dele) with frozensets of facts. The
graph ignores the delete lists. Layer i holds the actions that first become
applicable at fact level i, so level(a) and level(f) are first appearances.
extract returns a relaxed plan: a sequence of actions that reaches the goal
from the state when the delete lists are ignored.
"""

import math
from collections import namedtuple

Action = namedtuple("Action", "name pre add dele")


class RelaxedPlanningGraph:
    def __init__(self, actions, state, goal):
        self.actions = list(actions)
        self.goal = frozenset(goal)
        self.level = {f: 0 for f in state}  # @line L1
        self.F = [frozenset(state)]
        self.layers = []
        self.act_level = {}
        self.reached = self._build()

    def _build(self):
        used = set()
        while not self.goal <= self.F[-1]:  # @line L2
            i, F = len(self.F) - 1, self.F[-1]
            layer = [j for j, a in enumerate(self.actions) if j not in used and a.pre <= F]  # @line L3
            new = frozenset(f for j in layer for f in self.actions[j].add) - F  # @line L4
            if not new:  # @line L5
                return False
            for j in layer:  # @line L6
                used.add(j)
                self.act_level[j] = i
            for f in new:
                self.level[f] = i + 1
            self.layers.append(layer)
            self.F.append(F | new)
        return True  # @line L7

    def difficulty(self, j):
        return sum(self.level[p] for p in self.actions[j].pre)

    def extract(self):
        """Return (plan, goal sets per level) or (None, None) if the goal is not relaxed reachable."""
        if not self.reached:
            return None, None
        m = len(self.F) - 1
        goals = [set() for _ in range(m + 1)]
        need = {}
        for g in self.goal:  # @line L8
            goals[self.level[g]].add(g)
            need[g] = (m, 0)
        pos = {}
        count = [0] * (m + 1)
        for i in range(m, 0, -1):  # @line L9
            for g in sorted(goals[i], key=repr):  # @line L10
                if any(p < need[g] and g in self.actions[j].add for j, p in pos.items()):  # @line L11
                    continue
                cands = [j for j in self.layers[i - 1] if g in self.actions[j].add]
                o = min(cands, key=lambda j: (self.difficulty(j), j))  # @line L12
                pos[o] = (i - 1, count[i - 1])  # @line L13
                count[i - 1] += 1
                for p in self.actions[o].pre:  # @line L14
                    if self.level[p] >= 1:
                        goals[self.level[p]].add(p)  # @line L15
                        need[p] = min(need.get(p, (m + 1, 0)), pos[o])
        plan = [self.actions[j] for j in sorted(pos, key=pos.get)]  # @line L16
        return plan, goals


def relaxed_plan(actions, state, goal):
    plan, _ = RelaxedPlanningGraph(actions, state, goal).extract()
    return plan


def h_ff(actions, state, goal):
    """The number of actions of the extracted relaxed plan, or infinity."""
    plan = relaxed_plan(actions, state, goal)
    return math.inf if plan is None else len(plan)


def helpful_actions(actions, state, goal):
    """Applicable actions that add a goal of level 1 of the extraction."""
    _, goals = RelaxedPlanningGraph(actions, state, goal).extract()
    if goals is None or len(goals) < 2:
        return []
    return [a for a in actions if a.pre <= state and a.add & goals[1]]
