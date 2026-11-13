# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pddl/. The authors are listed in prov/DM6GS3.jsonl.

"""A reader for the STRIPS fragment of PDDL (:strips, :typing, :equality), grounded into the
STRIPS core by trying every typed parameter tuple.

Supported: typed parameter and object lists, a type hierarchy, conjunctive preconditions and goals,
(= a b) and (not (= a b)) under :equality, add and delete effects. Other requirement flags raise
ValueError. The STRIPS core below is a copy of the one on the strips page (not an import).
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


# Page specific code: the reader.

SUPPORTED = {":strips", ":typing", ":equality"}


def parse_sexpr(text: str):
    """Parse one s-expression into nested lists of lower case strings, with an explicit stack."""
    lines = [line.split(";", 1)[0] for line in text.lower().splitlines()]
    tokens = " ".join(lines).replace("(", " ( ").replace(")", " ) ").split()
    stack: List[list] = [[]]
    for tok in tokens:
        if tok == "(":
            stack.append([])
        elif tok == ")":
            if len(stack) == 1:
                raise ValueError("unbalanced ')'")
            done = stack.pop()
            stack[-1].append(done)
        else:
            stack[-1].append(tok)
    if len(stack) != 1 or len(stack[0]) != 1:
        raise ValueError("expected exactly one expression")
    return stack[0][0]


def typed_list(items: Sequence[str]) -> List[Tuple[str, str]]:
    """'?x ?y - block ?l - loc ?z' -> [(?x, block), (?y, block), (?l, loc), (?z, object)]."""
    out, pending, i = [], [], 0
    while i < len(items):
        if items[i] == "-":
            if i + 1 >= len(items) or isinstance(items[i + 1], list):
                raise ValueError("a type name must follow '-' (either types are not supported)")
            out += [(x, items[i + 1]) for x in pending]
            pending, i = [], i + 2
        else:
            pending.append(items[i])
            i += 1
    return out + [(x, "object") for x in pending]


def conjuncts(expr) -> List[list]:
    if not expr:
        return []
    if expr[0] == "and":
        return [c for e in expr[1:] for c in conjuncts(e)]
    return [expr]


class Domain(NamedTuple):
    name: str
    requirements: FrozenSet[str]
    supertype: Dict[str, str]
    actions: List[dict]


class Problem(NamedTuple):
    name: str
    domain: str
    objects: List[Tuple[str, str]]
    init: FrozenSet[Fact]
    goal: FrozenSet[Fact]


def read_domain(text: str) -> Domain:
    expr = parse_sexpr(text)
    if expr[0] != "define" or expr[1][0] != "domain":
        raise ValueError("not a domain")
    reqs, supertype, actions = frozenset({":strips"}), {}, []
    for part in expr[2:]:
        key = part[0]
        if key == ":requirements":
            reqs = frozenset(part[1:])
            bad = reqs - SUPPORTED
            if bad:
                raise ValueError(f"unsupported requirements: {sorted(bad)}")
        elif key == ":types":
            for t, parent in typed_list(part[1:]):
                supertype[t] = parent
        elif key == ":action":
            fields = dict(zip(part[2::2], part[3::2]))
            pre = conjuncts(fields.get(":precondition", []))
            eff = conjuncts(fields.get(":effect", []))
            for lit in pre + eff:
                atom = lit[1] if lit[0] == "not" else lit
                if not isinstance(atom, list) or not all(isinstance(x, str) for x in atom) or atom[0] in ("or", "when", "forall", "exists", "imply"):
                    raise ValueError(f"unsupported formula in {part[1]}: {lit}")
            actions.append({"name": part[1], "params": typed_list(fields.get(":parameters", [])), "pre": pre, "eff": eff})
        elif key in (":predicates", ":constants"):
            pass
        else:
            raise ValueError(f"unsupported section {key}")
    return Domain(expr[1][1], reqs, supertype, actions)


def read_problem(text: str) -> Problem:
    expr = parse_sexpr(text)
    if expr[0] != "define" or expr[1][0] != "problem":
        raise ValueError("not a problem")
    name, domain, objects, init, goal = expr[1][1], None, [], frozenset(), frozenset()
    for part in expr[2:]:
        if part[0] == ":domain":
            domain = part[1]
        elif part[0] == ":objects":
            objects = typed_list(part[1:])
        elif part[0] == ":init":
            init = frozenset(tuple(f) for f in part[1:])
        elif part[0] == ":goal":
            goal = frozenset(tuple(f) for f in conjuncts(part[1]))
    return Problem(name, domain, objects, init, goal)


def objects_by_type(domain: Domain, problem: Problem) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {"object": []}
    for obj, t in problem.objects:
        seen = set()
        while t not in seen:
            seen.add(t)
            out.setdefault(t, []).append(obj)
            if t == "object":
                break
            t = domain.supertype.get(t, "object")
    return out


def ground(domain: Domain, problem: Problem) -> List[Action]:
    """Every typed parameter tuple, with (in)equalities decided at grounding time."""
    objs = objects_by_type(domain, problem)
    out = []
    for act in domain.actions:
        names = [v for v, _ in act["params"]]
        for values in product(*(objs.get(t, []) for _, t in act["params"])):
            b = dict(zip(names, values))
            sub = lambda atom: tuple([atom[0]] + [b.get(x, x) for x in atom[1:]])
            pre, ok = [], True
            for c in act["pre"]:
                if c[0] == "=":
                    ok = ok and sub(c)[1] == sub(c)[2]
                elif c[0] == "not" and c[1][0] == "=":
                    ok = ok and sub(c[1])[1] != sub(c[1])[2]
                elif c[0] == "not":
                    raise ValueError("negative preconditions are not supported")
                else:
                    pre.append(sub(c))
            if not ok:
                continue
            add = [sub(e) for e in act["eff"] if e[0] != "not"]
            dele = [sub(e[1]) for e in act["eff"] if e[0] == "not"]
            out.append(make_action(f"({act['name']} {' '.join(values)})".replace(" )", ")"), pre, add, dele))
    return out
