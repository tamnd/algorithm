# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-plan-existence-np-complete/. The authors are listed in prov/T3WXP4.jsonl.

"""Executable parts of the proof that bounded plan existence is NP-complete.

sat_to_bounded_planning is the hardness reduction (Bylander 1994, Theorem 4.2):
a CNF formula with m variables and n clauses becomes a delete-free STRIPS task
that has a plan of at most k = 2m + n actions exactly when the formula is
satisfiable. verify_plan is the polynomial check that puts the problem in NP
when k is written in unary. unbounded_to_bounded shows why a bound written in
binary gives a PSPACE-complete problem instead.
"""

from collections import deque
from itertools import product
from typing import FrozenSet, Hashable, Iterable, List, NamedTuple, Optional, Sequence, Tuple

Fact = Hashable
State = FrozenSet[Fact]


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Action:
    return Action(name, frozenset(pre), frozenset(add), frozenset(delete))


def successor(s: State, a: Action) -> State:
    return (s - a.delete) | a.add


def verify_plan(init: Iterable[Fact], goal: Iterable[Fact], plan: Sequence[Action], k: int) -> bool:
    """The certificate check: at most k actions, each applicable, goal reached."""
    if len(plan) > k:
        return False
    s = frozenset(init)
    for a in plan:
        if not a.pre <= s:
            return False
        s = successor(s, a)
    return frozenset(goal) <= s


def shortest_plan_length(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action], k: Optional[int] = None) -> Optional[int]:
    """Breadth-first search, cut at depth k when k is given. An action that
    changes nothing is skipped."""
    init = frozenset(init)
    goal = frozenset(goal)
    dist = {init: 0}
    queue = deque([init])
    while queue:
        s = queue.popleft()
        if goal <= s:
            return dist[s]
        if k is not None and dist[s] >= k:
            continue
        for a in actions:
            if a.pre <= s:
                t = successor(s, a)
                if t != s and t not in dist:
                    dist[t] = dist[s] + 1
                    queue.append(t)
    return None


def bounded_plan_exists(init, goal, actions, k: int) -> bool:
    return shortest_plan_length(init, goal, actions, k) is not None


# A clause is a list of nonzero integers: +i is the variable x_i, -i is its negation.

def sat_to_bounded_planning(m: int, clauses: Sequence[Sequence[int]]):
    """Facts T(i), F(i), V(i) for each variable and C(j) for each clause.
    The task is delete-free, every action has at most one precondition and one
    add effect, and the initial state is empty."""
    acts: List[Action] = []
    for i in range(1, m + 1):
        acts.append(make_action(f"setT({i})", [], [("T", i)]))
        acts.append(make_action(f"setF({i})", [], [("F", i)]))
        acts.append(make_action(f"doneT({i})", [("T", i)], [("V", i)]))
        acts.append(make_action(f"doneF({i})", [("F", i)], [("V", i)]))
    for j, clause in enumerate(clauses):
        for lit in clause:
            fact = ("T", lit) if lit > 0 else ("F", -lit)
            acts.append(make_action(f"sat({j},{lit})", [fact], [("C", j)]))
    goal = {("V", i) for i in range(1, m + 1)} | {("C", j) for j in range(len(clauses))}
    return frozenset(), frozenset(goal), acts, 2 * m + len(clauses)


def satisfiable(m: int, clauses: Sequence[Sequence[int]]) -> Optional[Tuple[bool, ...]]:
    for bits in product((False, True), repeat=m):
        if all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clauses):
            return bits
    return None


def plan_from_assignment(m: int, clauses: Sequence[Sequence[int]], bits: Sequence[bool]) -> List[Action]:
    """The plan of length 2m + n that the proof builds from a satisfying assignment."""
    plan: List[Action] = []
    for i in range(1, m + 1):
        v = "T" if bits[i - 1] else "F"
        plan.append(make_action(f"set{v}({i})", [], [(v, i)]))
        plan.append(make_action(f"done{v}({i})", [(v, i)], [("V", i)]))
    for j, clause in enumerate(clauses):
        lit = next(l for l in clause if bits[abs(l) - 1] == (l > 0))
        fact = ("T", lit) if lit > 0 else ("F", -lit)
        plan.append(make_action(f"sat({j},{lit})", [fact], [("C", j)]))
    return plan


def assignment_from_plan(m: int, plan: Sequence[Action]) -> Tuple[bool, ...]:
    """Read the assignment back: x_i is true when the plan makes T(i) true."""
    made = {f for a in plan for f in a.add}
    return tuple(("T", i) in made for i in range(1, m + 1))


def unbounded_to_bounded(facts: Sequence[Fact], init, goal, actions):
    """Plan existence as bounded plan existence: a task with |F| facts has at most
    2^|F| states, so a plan exists iff one of at most 2^|F| - 1 actions exists.
    The bound has |F| binary digits, so the reduction is polynomial only when
    k is written in binary."""
    return init, goal, actions, 2 ** len(facts) - 1
