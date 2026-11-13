# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conformant-planning/. The authors are listed in prov/9DV4RS.jsonl.

"""Conformant planning by breadth-first search in the space of set beliefs.

A problem has a set of initial states, a goal test on states, a list of
actions, and succ(s, a), the set of possible next states of the action a in
the state s. An empty set means that a is not applicable in s. A conformant
plan is a sequence of actions that is applicable in every state it can meet
and ends in a goal state for every initial state and every outcome.
"""

from collections import deque
from typing import Callable, FrozenSet, Hashable, Iterable, List, Optional, Tuple

State = Hashable
Belief = FrozenSet[State]


def progress(b: Belief, a, succ: Callable) -> Optional[Belief]:
    """The belief after a, or None if a is not applicable in some state of b."""
    out = set()
    for s in b:
        nxt = succ(s, a)
        if not nxt:
            return None
        out.update(nxt)
    return frozenset(out)


def conformant_bfs(init: Iterable[State], goal: Callable, actions: List, succ: Callable) -> Tuple[Optional[List], int]:
    """A shortest conformant plan, or None if there is none, and the number of beliefs expanded."""
    b0 = frozenset(init)
    parent = {b0: None}
    queue = deque([b0])
    expanded = 0
    while queue:
        b = queue.popleft()
        if all(goal(s) for s in b):
            plan = []
            while parent[b] is not None:
                b, a = parent[b]
                plan.append(a)
            return plan[::-1], expanded
        expanded += 1
        for a in actions:
            nb = progress(b, a, succ)
            if nb is not None and nb not in parent:
                parent[nb] = (b, a)
                queue.append(nb)
    return None, expanded


def is_conformant(plan: List, init: Iterable[State], goal: Callable, succ: Callable) -> bool:
    """Check a plan by following every initial state and every outcome, one state at a time."""
    def run(s, i):
        if i == len(plan):
            return goal(s)
        nxt = succ(s, plan[i])
        return bool(nxt) and all(run(t, i + 1) for t in nxt)
    return all(run(s, 0) for s in init)


# ---- the bomb in the toilet with clogging ----

def bomb_in_toilet(n: int):
    """States are (package with the bomb, armed, clogged). dunk(i) needs an unclogged toilet,
    disarms the bomb if it is in package i, and clogs the toilet. flush unclogs it."""
    init = [(i, True, False) for i in range(n)]
    actions = [("dunk", i) for i in range(n)] + [("flush",)]

    def succ(s, a):
        bomb, armed, clogged = s
        if a[0] == "flush":
            return {(bomb, armed, False)}
        if clogged:
            return set()
        return {(bomb, armed and bomb != a[1], True)}

    goal = lambda s: not s[1]
    return init, goal, actions, succ
