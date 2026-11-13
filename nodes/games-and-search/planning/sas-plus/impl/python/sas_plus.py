# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sas-plus/. The authors are listed in prov/8Z7BSB.jsonl.

"""Translation of a STRIPS task into SAS+ (finite-domain variables) from mutex groups.

is_mutex_group checks, by an inductive argument over the ground actions, that at most one fact
of a group is true in every reachable state. translate covers the facts greedily with groups,
as Helmert's translator does, and gives every fact left over a binary variable.

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


# Page specific code.

NONE = "<none>"  # the value "no fact of this group is true"


def is_mutex_group(group: Iterable[Fact], init: State, actions: Sequence[Action]) -> bool:
    """A sufficient inductive test that at most one fact of group holds in every reachable state:
    at most one holds in init, and every action that adds a group fact adds exactly one, and either
    needs that fact already or needs and deletes another group fact."""
    g = frozenset(group)
    if len(g & init) > 1:
        return False
    for a in actions:
        added = a.add & g
        if len(added) > 1:
            return False
        if added and not (added <= a.pre or (a.pre & a.delete & g)):
            return False
    return True


def is_exactly_one_group(group: Iterable[Fact], init: State, actions: Sequence[Action]) -> bool:
    """is_mutex_group, plus exactly one fact in init, plus every action that deletes a group fact adds one."""
    g = frozenset(group)
    if not is_mutex_group(g, init, actions) or len(g & init) != 1:
        return False
    return all(not (a.delete & g) or (a.add & g) for a in actions)


class SasTask(NamedTuple):
    variables: Tuple[Tuple[Fact, ...], ...]  # the values of each variable (facts, maybe NONE)
    init: Tuple[Fact, ...]
    actions: Tuple[Tuple[str, Tuple[Tuple[int, Fact], ...], Tuple[Tuple[int, Fact], ...]], ...]  # name, pre, eff


def translate(facts: Iterable[Fact], init: State, actions: Sequence[Action], groups: Sequence[Iterable[Fact]]) -> Tuple[SasTask, Dict[Fact, int]]:
    """Build a SAS+ task. groups must pass is_mutex_group. Returns the task and the map fact -> variable."""
    facts = sorted(set(facts), key=repr)
    groups = [frozenset(g) for g in groups]
    covered: set = set()
    variables: List[Tuple[Fact, ...]] = []
    while True:
        best = max(groups, key=lambda g: len(g - covered), default=frozenset())
        rest = best - covered
        if len(rest) < 2:
            break
        values = tuple(sorted(rest, key=repr))
        if not (rest == best and is_exactly_one_group(best, init, actions)):
            values += (NONE,)
        variables.append(values)
        covered |= rest
    for f in facts:
        if f not in covered:
            variables.append((f, NONE))
            covered.add(f)
    var_of = {f: i for i, vals in enumerate(variables) for f in vals if f != NONE}
    sas_actions = []
    for a in actions:
        pre: Dict[int, Fact] = {}
        ok = True
        for f in a.pre:
            v = var_of[f]
            if v in pre and pre[v] != f:
                ok = False  # two values of one variable: never applicable
            pre[v] = f
        if not ok:
            continue
        eff: Dict[int, Fact] = {var_of[f]: f for f in a.add}
        for f in a.delete:
            v = var_of[f]
            if v in eff:
                continue
            if f not in a.pre:
                raise ValueError(f"{a.name} deletes {f!r} without requiring it")
            eff[v] = NONE
        sas_actions.append((a.name, tuple(sorted(pre.items())), tuple(sorted(eff.items(), key=repr))))
    return SasTask(tuple(variables), encode(init, variables, var_of), tuple(sas_actions)), var_of


def encode(state: State, variables: Sequence[Tuple[Fact, ...]], var_of: Dict[Fact, int]) -> Tuple[Fact, ...]:
    """The SAS+ state of a STRIPS state that satisfies the mutex groups."""
    values = [NONE] * len(variables)
    for f in state:
        v = var_of[f]
        if values[v] != NONE:
            raise ValueError(f"two true facts in variable {v}")
        values[v] = f
    return tuple(values)


def sas_successors(task: SasTask, state: Tuple[Fact, ...]):
    for name, pre, eff in task.actions:
        if all(state[v] == val for v, val in pre):
            new = list(state)
            for v, val in eff:
                new[v] = val
            yield name, tuple(new)


def sas_reachable(task: SasTask) -> Dict[Tuple[Fact, ...], int]:
    dist = {task.init: 0}
    queue = deque([task.init])
    while queue:
        s = queue.popleft()
        for _, t in sas_successors(task, s):
            if t not in dist:
                dist[t] = dist[s] + 1
                queue.append(t)
    return dist


def sas_plan_length(task: SasTask, goal: Dict[int, Fact]) -> Optional[int]:
    for s, d in sorted(sas_reachable(task).items(), key=lambda kv: kv[1]):
        if all(s[v] == val for v, val in goal.items()):
            return d
    return None


def blocks_world_groups(blocks: Sequence[str]) -> List[FrozenSet[Fact]]:
    """Where each block is; what is on each block; what the hand holds."""
    groups = []
    for x in blocks:
        groups.append(frozenset({("on", x, y) for y in blocks if y != x} | {("ontable", x), ("holding", x)}))
    for y in blocks:
        groups.append(frozenset({("on", x, y) for x in blocks if x != y} | {("clear", y), ("holding", y)}))
    groups.append(frozenset({("holding", x) for x in blocks} | {("handempty",)}))
    return groups


def blocks_world_facts(blocks: Sequence[str]) -> List[Fact]:
    facts = [("handempty",)]
    for x in blocks:
        facts += [("ontable", x), ("clear", x), ("holding", x)]
        facts += [("on", x, y) for y in blocks if y != x]
    return facts
