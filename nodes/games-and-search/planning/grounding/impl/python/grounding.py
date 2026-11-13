# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grounding/. The authors are listed in prov/E2ANZJ.jsonl.

"""Grounding of typed action schemas into STRIPS actions.

ground_brute tries every typed parameter tuple. ground_join binds the parameters that occur in
static preconditions by matching those atoms against the initial state first, and so never builds
a tuple that a static precondition rules out. ground_reachable then keeps only the actions that
relaxed (delete-free) reachability can reach.

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


# Page specific code: lifted schemas.

Atom = Tuple[str, ...]  # ("at", "?t", "?l"); arguments that start with "?" are variables


class Schema(NamedTuple):
    name: str
    params: Tuple[Tuple[str, str], ...]  # (variable, type)
    pre: Tuple[Atom, ...]
    add: Tuple[Atom, ...]
    delete: Tuple[Atom, ...]
    distinct: Tuple[Tuple[str, str], ...] = ()  # pairs of variables that must differ, as (not (= ?x ?y))


def schema(name, params, pre=(), add=(), delete=(), distinct=()) -> Schema:
    return Schema(name, tuple(params), tuple(pre), tuple(add), tuple(delete), tuple(distinct))


def static_predicates(schemas: Sequence[Schema]) -> set:
    """Predicates that no schema adds or deletes. Their truth never changes after the initial state."""
    used = {atom[0] for s in schemas for atom in s.pre}
    changed = {atom[0] for s in schemas for atom in s.add + s.delete}
    return used - changed


def _ground_atom(atom: Atom, binding: Dict[str, str]) -> Atom:
    return (atom[0],) + tuple(binding.get(x, x) for x in atom[1:])


def _instantiate(s: Schema, binding: Dict[str, str]) -> Action:
    args = ",".join(binding[v] for v, _ in s.params)
    return make_action(
        f"{s.name}({args})",
        (_ground_atom(a, binding) for a in s.pre),
        (_ground_atom(a, binding) for a in s.add),
        (_ground_atom(a, binding) for a in s.delete),
    )


def ground_brute(schemas: Sequence[Schema], objects: Dict[str, Sequence[str]], init: Iterable[Fact]) -> List[Action]:
    """Every typed parameter tuple, minus those with a false static precondition or a failed inequality."""
    init = frozenset(init)
    static = static_predicates(schemas)
    out = []
    for s in schemas:
        names = [v for v, _ in s.params]
        for values in product(*(objects[t] for _, t in s.params)):
            b = dict(zip(names, values))
            if any(b[x] == b[y] for x, y in s.distinct):
                continue
            if all(_ground_atom(a, b) in init for a in s.pre if a[0] in static):
                out.append(_instantiate(s, b))
    return out


def ground_join(schemas: Sequence[Schema], objects: Dict[str, Sequence[str]], init: Iterable[Fact]) -> List[Action]:
    """Bind variables by joining the static precondition atoms with the initial state, then
    enumerate the variables that are still free. Builds no tuple that a static atom rules out."""
    init = frozenset(init)
    static = static_predicates(schemas)  # @line L1
    by_pred: Dict[str, List[Atom]] = {}
    for f in init:
        by_pred.setdefault(f[0], []).append(f)
    out = []  # @line L2
    for s in schemas:  # @line L3
        types = dict(s.params)
        domain = {v: set(objects[t]) for v, t in s.params}
        bindings: List[Dict[str, str]] = [{}]  # @line L4
        for atom in (a for a in s.pre if a[0] in static):  # @line L5
            extended = []
            for b in bindings:
                for fact in by_pred.get(atom[0], ()):
                    if len(fact) != len(atom):
                        continue
                    nb = dict(b)
                    ok = True
                    for term, value in zip(atom[1:], fact[1:]):
                        if term.startswith("?"):
                            if term in nb:
                                ok = nb[term] == value
                            elif value in domain[term]:
                                nb[term] = value
                            else:
                                ok = False
                        else:
                            ok = term == value
                        if not ok:
                            break
                    if ok:
                        extended.append(nb)
            bindings = extended  # @line L6
        for b in bindings:  # @line L7
            free = [v for v, _ in s.params if v not in b]
            for values in product(*(objects[types[v]] for v in free)):  # @line L8
                full = dict(b)
                full.update(zip(free, values))  # @line L9
                if any(full[x] == full[y] for x, y in s.distinct):  # @line L10
                    continue
                out.append(_instantiate(s, full))  # @line L11
    return out  # @line L12


def ground_reachable(schemas: Sequence[Schema], objects: Dict[str, Sequence[str]], init: Iterable[Fact]) -> List[Action]:
    """Keep the ground actions whose preconditions become true under delete-free reachability.
    Every action that is applicable in some reachable state is kept."""
    candidates = ground_join(schemas, objects, init)  # @line L13
    facts = set(init)
    kept = [False] * len(candidates)
    changed = True
    while changed:  # @line L14
        changed = False
        for i, a in enumerate(candidates):
            if not kept[i] and a.pre <= facts:  # @line L15
                kept[i] = True
                facts |= a.add  # @line L16
                changed = True  # @line L17
    return [a for i, a in enumerate(candidates) if kept[i]]  # @line L18
