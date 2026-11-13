# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strips/. The authors are listed in prov/MGC5NA.jsonl.

"""A small STRIPS core: states are frozensets of facts, actions have pre, add and del lists.

The same core is copied (not imported) into the other planning pages of this group.
A fact is any hashable value, usually a tuple such as ("on", "a", "b").
"""

from collections import deque
from typing import Dict, FrozenSet, Hashable, Iterable, List, NamedTuple, Optional, Sequence

Fact = Hashable
State = FrozenSet[Fact]


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Action:
    return Action(name, frozenset(pre), frozenset(add), frozenset(delete))


def applicable(state: State, action: Action) -> bool:
    return action.pre <= state


def successor(state: State, action: Action) -> State:
    """The STRIPS successor (s minus del) union add. The caller checks applicability."""
    return (state - action.delete) | action.add


def run_plan(state: State, plan: Sequence[Action]) -> Optional[State]:
    """Apply the plan from state. Return the final state, or None if an action is not applicable."""
    for a in plan:
        if not a.pre <= state:
            return None
        state = (state - a.delete) | a.add
    return state


def is_plan(init: State, goal: FrozenSet[Fact], plan: Sequence[Action]) -> bool:
    final = run_plan(frozenset(init), plan)
    return final is not None and frozenset(goal) <= final


def reachable(init: State, actions: Sequence[Action]) -> Dict[State, int]:
    """Breadth first search over ground states: map each reachable state to its distance from init."""
    init = frozenset(init)
    dist = {init: 0}
    queue = deque([init])
    while queue:
        s = queue.popleft()
        for a in actions:
            if a.pre <= s:
                t = (s - a.delete) | a.add
                if t not in dist:
                    dist[t] = dist[s] + 1
                    queue.append(t)
    return dist


def bfs_plan(init: State, goal: FrozenSet[Fact], actions: Sequence[Action]) -> Optional[List[Action]]:
    """A shortest plan (fewest actions) by breadth first search, or None if the goal is unreachable."""
    init = frozenset(init)
    goal = frozenset(goal)
    parent: Dict[State, Optional[tuple]] = {init: None}
    queue = deque([init])
    while queue:
        s = queue.popleft()
        if goal <= s:
            plan = []
            while parent[s] is not None:
                s, a = parent[s]
                plan.append(a)
            plan.reverse()
            return plan
        for a in actions:
            if a.pre <= s:
                t = (s - a.delete) | a.add
                if t not in parent:
                    parent[t] = (s, a)
                    queue.append(t)
    return None


# Blocks world with four operators: pickup, putdown, stack, unstack.

def blocks_world_actions(blocks: Sequence[str]) -> List[Action]:
    acts = []
    for x in blocks:
        acts.append(make_action(f"pickup({x})", [("clear", x), ("ontable", x), ("handempty",)], [("holding", x)], [("clear", x), ("ontable", x), ("handempty",)]))
        acts.append(make_action(f"putdown({x})", [("holding", x)], [("ontable", x), ("clear", x), ("handempty",)], [("holding", x)]))
        for y in blocks:
            if x != y:
                acts.append(make_action(f"stack({x},{y})", [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), ("handempty",)], [("holding", x), ("clear", y)]))
                acts.append(make_action(f"unstack({x},{y})", [("on", x, y), ("clear", x), ("handempty",)], [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), ("handempty",)]))
    return acts


def blocks_world_state(stacks: Sequence[Sequence[str]], hand: bool = True) -> State:
    """Facts of an arrangement; each stack is listed from the bottom up. hand adds handempty."""
    facts = set()
    for st in stacks:
        if not st:
            continue
        facts.add(("ontable", st[0]))
        for below, above in zip(st, st[1:]):
            facts.add(("on", above, below))
        facts.add(("clear", st[-1]))
    if hand:
        facts.add(("handempty",))
    return frozenset(facts)


# Blocks world with one move operator in three forms (no hand).

def move_actions(blocks: Sequence[str]) -> List[Action]:
    acts = []
    for b in blocks:
        for x in blocks:
            if x == b:
                continue
            acts.append(make_action(f"move({b},{x},table)", [("on", b, x), ("clear", b)], [("ontable", b), ("clear", x)], [("on", b, x)]))
            acts.append(make_action(f"move({b},table,{x})", [("ontable", b), ("clear", b), ("clear", x)], [("on", b, x)], [("ontable", b), ("clear", x)]))
            for y in blocks:
                if y != b and y != x:
                    acts.append(make_action(f"move({b},{x},{y})", [("on", b, x), ("clear", b), ("clear", y)], [("on", b, y), ("clear", x)], [("on", b, x), ("clear", y)]))
    return acts


def move_state(stacks: Sequence[Sequence[str]]) -> State:
    return blocks_world_state(stacks, hand=False)
