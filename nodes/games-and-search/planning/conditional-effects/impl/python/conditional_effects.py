# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-effects/. The authors are listed in prov/DWVFYP.jsonl.

"""Conditional effects, their semantics, and the exponential compilation into plain STRIPS.

An action has a precondition and a list of effects (cond, add, del). All conditions are read in
the state before the action. With D and A the unions of the delete and add lists of the effects
that fire, the next state is (s minus D) union A.

compile_away makes one STRIPS action for each set of effects that fires. Each condition here is a
single fact (or empty), and a new fact ("not", c) stands for "c is false", so that "this effect
does not fire" is a plain precondition.

The STRIPS core below is a copy of the one on the strips page (not an import).
"""

from collections import deque
from itertools import product
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


# Page specific code.

class Effect(NamedTuple):
    cond: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


class CondAction(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    effects: Tuple[Effect, ...]


def effect(cond: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Effect:
    return Effect(frozenset(cond), frozenset(add), frozenset(delete))


def cond_action(name: str, pre: Iterable[Fact], effects: Iterable[Effect]) -> CondAction:
    return CondAction(name, frozenset(pre), tuple(effects))


def cond_successor(state: State, a: CondAction) -> State:
    fired = [e for e in a.effects if e.cond <= state]
    dels = frozenset().union(*(e.delete for e in fired))
    adds = frozenset().union(*(e.add for e in fired))
    return (state - dels) | adds


def cond_reachable(init: State, actions: Sequence[CondAction]) -> Dict[State, int]:
    init = frozenset(init)
    dist = {init: 0}
    queue = deque([init])
    while queue:
        s = queue.popleft()
        for a in actions:
            if a.pre <= s:
                t = cond_successor(s, a)
                if t not in dist:
                    dist[t] = dist[s] + 1
                    queue.append(t)
    return dist


def neg(f: Fact) -> Fact:
    return ("not", f)


def compile_away(init: State, actions: Sequence[CondAction]) -> Tuple[State, List[Action]]:
    """One STRIPS action per set of firing effects. Returns the new initial state and the actions."""
    conds = set()
    for a in actions:
        for e in a.effects:
            if len(e.cond) > 1:
                raise ValueError("this compilation takes conditions of at most one fact")
            conds |= e.cond
    new_init = frozenset(init) | {neg(c) for c in conds if c not in init}
    out = []
    for a in actions:
        always = [e for e in a.effects if not e.cond]
        maybe = [e for e in a.effects if e.cond]
        for choice in product((False, True), repeat=len(maybe)):
            fired = always + [e for e, on in zip(maybe, choice) if on]
            pre = set(a.pre)
            for e, on in zip(maybe, choice):
                (c,) = e.cond
                pre.add(c if on else neg(c))
            if any(c in pre and neg(c) in pre for c in conds):
                continue
            adds = frozenset().union(*(e.add for e in fired))
            dels = frozenset().union(*(e.delete for e in fired))
            # Keep ("not", c) equal to "c is false" after the action.
            adds_neg = {neg(c) for c in conds if c in dels and c not in adds}
            dels_neg = {neg(c) for c in conds if c in adds}
            tag = "".join("1" if on else "0" for on in choice)
            out.append(make_action(f"{a.name}[{tag}]", pre, adds | adds_neg, dels | dels_neg))
    return new_init, out


def briefcase(locations: Sequence[str], objects: Sequence[str]) -> List[CondAction]:
    """Pednault's briefcase domain: moving the briefcase moves every object inside it."""
    acts = []
    for l in locations:
        for m in locations:
            if l != m:
                effs = [effect((), [("at-b", m)], [("at-b", l)])]
                effs += [effect([("in", o)], [("at", o, m)], [("at", o, l)]) for o in objects]
                acts.append(cond_action(f"move({l},{m})", [("at-b", l)], effs))
    for o in objects:
        for l in locations:
            acts.append(cond_action(f"put-in({o},{l})", [("at", o, l), ("at-b", l), ("out", o)], [effect((), [("in", o)], [("out", o)])]))
        acts.append(cond_action(f"take-out({o})", [("in", o)], [effect((), [("out", o)], [("in", o)])]))
    return acts
