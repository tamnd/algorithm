# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blocks-world/. The authors are listed in prov/KD4S9R.jsonl.

"""Blocks world: the two STRIPS encodings, state counts, and the "everything to the table,
then build" plan, which is within a factor 2 of optimal for fully specified goals.

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

def arrangements(n: int) -> int:
    """Ways to put n labeled blocks into unordered stacks (OEIS A000262): sum over k of L(n, k),
    by the recurrence a(n) = (2n - 1) a(n - 1) - (n - 1)(n - 2) a(n - 2)."""
    a = [1, 1]
    for k in range(2, n + 1):
        a.append((2 * k - 1) * a[k - 1] - (k - 1) * (k - 2) * a[k - 2])
    return a[n]


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


def support(stacks: Sequence[Sequence[str]]) -> Dict[str, str]:
    """Map each block to the block it is on, or to "table"."""
    below = {}
    for st in stacks:
        for i, b in enumerate(st):
            below[b] = "table" if i == 0 else st[i - 1]
    return below


def in_position(stacks: Sequence[Sequence[str]], goal_stacks: Sequence[Sequence[str]]) -> set:
    """Blocks that sit on their goal support, with every block below them also in position."""
    now, want = support(stacks), support(goal_stacks)
    good = set()
    for st in stacks:
        for b in st:
            if now[b] == want[b] and (now[b] == "table" or now[b] in good):
                good.add(b)
            else:
                break
    return good


def table_then_build(stacks: Sequence[Sequence[str]], goal_stacks: Sequence[Sequence[str]], blocks: Sequence[str]) -> List[Action]:
    """Move every block that is not in position to the table (top first), then build the goal
    stacks bottom up. Each block moves at most twice; blocks in position never move."""
    acts = {a.name: a for a in move_actions(blocks)}
    good = in_position(stacks, goal_stacks)
    now, want = support(stacks), support(goal_stacks)
    plan = []
    for st in stacks:
        for b in reversed(st):
            if b in good:
                break
            if now[b] != "table":
                plan.append(acts[f"move({b},{now[b]},table)"])
    for st in goal_stacks:
        for b in st:
            if b not in good and want[b] != "table":
                plan.append(acts[f"move({b},table,{want[b]})"])
    return plan
