# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/classical-planning/. The authors are listed in prov/M1BM1K.jsonl.

"""Classical planning over a small STRIPS core, with a shortest plan by breadth first search
and a brute force reference over all action sequences.

The STRIPS core below is a copy of the one on the strips page (not an import).
"""

import random
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


# Page specific code.

def random_stacks(blocks: Sequence[str], rng: random.Random) -> List[List[str]]:
    """A random arrangement of the blocks into stacks (bottom first). Not uniform over arrangements."""
    order = list(blocks)
    rng.shuffle(order)
    stacks: List[List[str]] = []
    for b in order:
        if stacks and rng.random() < 0.5:
            stacks[-1].append(b)
        else:
            stacks.append([b])
    return stacks


def brute_force_shortest(init: State, goal: FrozenSet[Fact], actions: Sequence[Action], max_len: int) -> Optional[int]:
    """The length of a shortest plan of length at most max_len, by listing every action sequence.

    No duplicate detection: every sequence of applicable actions up to max_len is generated,
    one length at a time, with an explicit stack.
    """
    init = frozenset(init)
    goal = frozenset(goal)
    for length in range(max_len + 1):
        stack = [(init, 0)]
        while stack:
            s, depth = stack.pop()
            if depth == length:
                if goal <= s:
                    return length
                continue
            for a in actions:
                if a.pre <= s:
                    stack.append(((s - a.delete) | a.add, depth + 1))
    return None
