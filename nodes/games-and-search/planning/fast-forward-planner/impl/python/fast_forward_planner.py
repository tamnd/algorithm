# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-forward-planner/. The authors are listed in prov/RWBN9P.jsonl.

"""The Fast-Forward (FF) planner of Hoffmann and Nebel (2001) for STRIPS tasks.

A STRIPS action is Action(name, pre, add, dele) with frozensets of facts. The
call ff(actions, init, goal) returns a list of actions, or None when the task
has no plan. FF first runs enforced hill climbing on the FF heuristic, with
two pruning rules: only helpful actions are tried, and a state is dropped
when its relaxed plan deletes a goal that the last action has just added. If
that fails, FF forgets everything and runs a complete greedy best-first search
on the same heuristic, without pruning.
"""

import heapq
import math
from collections import deque, namedtuple
from typing import FrozenSet, Hashable, List, Optional, Sequence, Tuple

Action = namedtuple("Action", "name pre add dele")


def relaxed_plan(actions: Sequence[Action], state: FrozenSet[Hashable],
                 goal: FrozenSet[Hashable]) -> Tuple[Optional[List[Action]], Optional[List[set]]]:
    """A relaxed plan from the relaxed planning graph, and the goal sets per level, or (None, None)."""
    level, layers, facts, used = {f: 0 for f in state}, [], state, set()
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
    m = len(layers)
    goals = [set() for _ in range(m + 1)]
    need, pos, count = {}, {}, [0] * (m + 1)
    for g in goal:
        goals[level[g]].add(g)
        need[g] = (m, 0)
    for i in range(m, 0, -1):
        for g in sorted(goals[i], key=repr):
            if any(p < need[g] and g in actions[j].add for j, p in pos.items()):
                continue
            o = min((j for j in layers[i - 1] if g in actions[j].add),
                    key=lambda j: (sum(level[p] for p in actions[j].pre), j))
            pos[o] = (i - 1, count[i - 1])
            count[i - 1] += 1
            for p in actions[o].pre:
                if level[p] >= 1:
                    goals[level[p]].add(p)
                    need[p] = min(need.get(p, (m + 1, 0)), pos[o])
    return [actions[j] for j in sorted(pos, key=pos.get)], goals


class Task:
    """A STRIPS task with a cache of relaxed plans per state."""

    def __init__(self, actions, init, goal, added_goal_deletion=True):
        self.actions, self.init, self.goal = list(actions), frozenset(init), frozenset(goal)
        self.added_goal_deletion = added_goal_deletion
        self.cache = {}

    def evaluate(self, s):
        if s not in self.cache:
            self.cache[s] = relaxed_plan(self.actions, s, self.goal)
        return self.cache[s]

    def h(self, s):
        plan, _ = self.evaluate(s)
        return math.inf if plan is None else len(plan)

    def successors(self, s):
        for a in self.actions:
            if a.pre <= s:
                yield a, (s - a.dele) | a.add

    def helpful_actions(self, s):
        """Applicable actions that add a goal of level 1 of the relaxed plan (Equation 5 of the paper)."""
        plan, goals = self.evaluate(s)  # @line L4
        if plan is None or len(goals) < 2:
            return []
        return [a for a in self.actions if a.pre <= s and a.add & goals[1]]  # @line L5

    def pruned_successors(self, s):
        for a in self.helpful_actions(s):
            t = (s - a.dele) | a.add  # @line L6
            if self.added_goal_deletion:
                t_plan, _ = self.evaluate(t)
                new_goals = a.add & self.goal
                if t_plan is not None and any(b.dele & new_goals for b in t_plan):  # @line L7
                    continue
            yield a, t  # @line L8


def enforced_hill_climbing(task: Task, stats: Optional[dict] = None) -> Optional[List[Action]]:
    """Enforced hill climbing with helpful actions and added goal deletion."""
    s, plan = task.init, []
    hs = task.h(s)
    if hs == math.inf:
        return None
    while not task.goal <= s:
        parent, queue, found = {s: None}, deque([s]), None
        while queue and found is None:
            u = queue.popleft()
            for a, t in task.pruned_successors(u):
                if t in parent:
                    continue
                parent[t] = (u, a)
                ht = task.h(t)
                if task.goal <= t or ht < hs:
                    found = t
                    break
                if ht < math.inf:
                    queue.append(t)
        if found is None:
            return None
        path, x = [], found
        while parent[x] is not None:
            x, a = parent[x]
            path.append(a)
        plan.extend(reversed(path))
        s, hs = found, task.h(found)
        if stats is not None:
            stats.setdefault("depths", []).append(len(path))
    return plan


def greedy_best_first(task: Task) -> Optional[List[Action]]:
    """Complete greedy best-first search on the FF heuristic, without pruning."""
    tie = 0
    heap, parent = [(task.h(task.init), tie, task.init)], {task.init: None}  # @line L9
    if heap[0][0] == math.inf:
        return None
    while heap:  # @line L10
        _, _, s = heapq.heappop(heap)  # @line L11
        if task.goal <= s:  # @line L12
            plan = []
            while parent[s] is not None:
                s, a = parent[s]
                plan.append(a)
            return plan[::-1]
        for a, t in task.successors(s):  # @line L13
            if t not in parent:
                parent[t] = (s, a)
                ht = task.h(t)
                if ht < math.inf:
                    tie += 1
                    heapq.heappush(heap, (ht, tie, t))
    return None  # @line L14


def ff(actions: Sequence[Action], init, goal, stats: Optional[dict] = None) -> Optional[List[Action]]:
    """Return a plan for the STRIPS task, or None when it has no plan."""
    task = Task(actions, init, goal)
    if stats is not None:
        stats["phase"] = "enforced hill climbing"
    plan = enforced_hill_climbing(task, stats)  # @line L1
    if plan is not None:  # @line L2
        return plan
    if stats is not None:
        stats["phase"] = "best-first search"
    return greedy_best_first(task)  # @line L3
