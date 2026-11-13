# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sussman-anomaly/. The authors are listed in prov/0Z947C.jsonl.

"""The Sussman anomaly by enumeration: C on A, A and B on the table, goals on(A, B) and on(B, C).

A serial plan reaches one goal by a shortest plan for that goal alone, and then reaches both goals
by a shortest plan from there. Enumeration over all action sequences shows that every serial plan,
in either goal order, is longer than the optimal plan, and that a planner that also keeps the
first goal true afterwards finds no plan at all.

The STRIPS core below is a copy of the one on the strips page (not an import).
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

ON_A_B = frozenset({("on", "a", "b")})
ON_B_C = frozenset({("on", "b", "c")})
GOAL = ON_A_B | ON_B_C


def sussman_task(hand: bool) -> Tuple[State, List[Action]]:
    """The initial state (C on A; A and B on the table) and the actions of one encoding."""
    if hand:
        return blocks_world_state([["a", "c"], ["b"]]), blocks_world_actions("abc")
    return move_state([["a", "c"], ["b"]]), move_actions("abc")


def plans_up_to(init: State, goal: FrozenSet[Fact], actions: Sequence[Action], max_len: int) -> List[Tuple[Action, ...]]:
    """Every action sequence of length at most max_len that reaches the goal (explicit stack)."""
    out = []
    stack: List[Tuple[State, Tuple[Action, ...]]] = [(frozenset(init), ())]
    while stack:
        s, seq = stack.pop()
        if goal <= s:
            out.append(seq)
        if len(seq) == max_len:
            continue
        for a in actions:
            if a.pre <= s:
                stack.append(((s - a.delete) | a.add, seq + (a,)))
    return out


def shortest_length(init: State, goal: FrozenSet[Fact], actions: Sequence[Action]) -> Optional[int]:
    plan = bfs_plan(init, goal, actions)
    return None if plan is None else len(plan)


def serial_plans(init: State, first: FrozenSet[Fact], goal: FrozenSet[Fact], actions: Sequence[Action], max_len: int) -> List[Tuple[Action, ...]]:
    """Plans p1 p2 of length at most max_len where p1 is a shortest plan for first and p2 is a
    shortest plan for goal from the end of p1, found by enumerating every sequence."""
    d1 = shortest_length(init, first, actions)
    out = []
    for seq in plans_up_to(init, goal, actions, max_len):
        prefix = seq[:d1]
        mid = run_plan(init, prefix)
        if mid is None or not first <= mid:
            continue
        if len(seq) - d1 == shortest_length(mid, goal, actions):
            out.append(seq)
    return out


def protected_plan(init: State, first: FrozenSet[Fact], goal: FrozenSet[Fact], actions: Sequence[Action]) -> Optional[List[Action]]:
    """Reach first by a shortest plan, then search for goal only through states where first stays true."""
    p1 = bfs_plan(init, first, actions)
    mid = run_plan(init, p1)
    parent = {mid: None}
    queue = deque([mid])
    while queue:
        s = queue.popleft()
        if goal <= s:
            plan = []
            while parent[s] is not None:
                s, a = parent[s]
                plan.append(a)
            return p1 + plan[::-1]
        for a in actions:
            if a.pre <= s:
                t = (s - a.delete) | a.add
                if first <= t and t not in parent:
                    parent[t] = (s, a)
                    queue.append(t)
    return None
