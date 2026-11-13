# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backward-state-space-search/. The authors are listed in prov/3Y3JQ2.jsonl.

"""Backward state-space search (regression) for propositional STRIPS tasks.

The search nodes are subgoals: sets of facts that stand for every state that
contains them. The root is the goal G. An action a is relevant for a subgoal g
when it adds a fact of g and deletes no fact of g, and the regressed subgoal is
(g minus add(a)) union pre(a). The search stops at a subgoal that the initial
state contains. Actions must have disjoint add and delete lists.
"""

from collections import deque
from typing import Dict, FrozenSet, Hashable, Iterable, List, NamedTuple, Optional, Sequence, Tuple

Fact = Hashable
State = FrozenSet[Fact]


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Action:
    a = Action(name, frozenset(pre), frozenset(add), frozenset(delete))
    if a.add & a.delete:
        raise ValueError("add and delete lists must be disjoint")
    return a


def run_plan(state: State, plan: Sequence[Action]) -> Optional[State]:
    for a in plan:
        if not a.pre <= state:
            return None
        state = (state - a.delete) | a.add
    return state


def is_plan(init: Iterable[Fact], goal: Iterable[Fact], plan: Sequence[Action]) -> bool:
    final = run_plan(frozenset(init), plan)
    return final is not None and frozenset(goal) <= final


def relevant(g: FrozenSet[Fact], a: Action) -> bool:
    return bool(a.add & g) and not (a.delete & g)


def regress(g: FrozenSet[Fact], a: Action) -> FrozenSet[Fact]:
    return (g - a.add) | a.pre


class Stats(NamedTuple):
    expanded: int
    generated: int
    reached: int


def backward_search(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action],
                    strategy: str = "bfs", trace: Optional[list] = None) -> Tuple[Optional[List[Action]], Stats]:
    """Regression search from the goal. "bfs" gives a plan with the fewest actions,
    "dfs" some plan. Returns (plan in execution order, or None; Stats).
    If trace is a list, each expanded subgoal is appended to it."""
    init = frozenset(init)
    goal = frozenset(goal)
    parent: Dict[FrozenSet[Fact], Optional[Tuple[FrozenSet[Fact], Action]]] = {goal: None}  # @line L1
    frontier = deque([goal])  # @line L2
    pop = frontier.popleft if strategy == "bfs" else frontier.pop
    expanded = generated = 0
    while frontier:  # @line L3
        g = pop()  # @line L4
        if g <= init:  # @line L5
            plan = []  # @line L13
            while parent[g] is not None:  # @line L14
                g, a = parent[g]  # @line L15
                plan.append(a)  # @line L16 (the first action found is the first to execute)
            return plan, Stats(expanded, generated, len(parent))  # @line L17
        expanded += 1
        if trace is not None:
            trace.append(g)
        for a in actions:  # @line L6
            if relevant(g, a):  # @line L7
                h = regress(g, a)  # @line L8
                generated += 1
                if h not in parent:  # @line L9
                    parent[h] = (g, a)  # @line L10
                    frontier.append(h)  # @line L11
    return None, Stats(expanded, generated, len(parent))  # @line L12


def all_subgoals(goal: Iterable[Fact], actions: Sequence[Action]) -> List[FrozenSet[Fact]]:
    """Every subgoal that regression can reach from the goal (no stop test)."""
    goal = frozenset(goal)
    seen = {goal}
    queue = deque([goal])
    while queue:
        g = queue.popleft()
        for a in actions:
            if relevant(g, a):
                h = regress(g, a)
                if h not in seen:
                    seen.add(h)
                    queue.append(h)
    return list(seen)
