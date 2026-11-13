# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contingent-planning/. The authors are listed in prov/JA1FVX.jsonl.

"""Contingent planning by AND-OR search over set beliefs.

A problem has a set of initial states, a goal test on states, a list of actions,
succ(s, a), the set of possible next states (empty if a is not applicable in s),
and obs(s, a), the observation that the agent gets when the action a has led to
the state s. A plan is a tree: the string "done", or a pair (a, {o: subplan}).
"""

from collections import deque
from math import inf
from typing import Callable, Dict, FrozenSet, Hashable, Iterable, List, Optional, Tuple

State = Hashable
Belief = FrozenSet[State]


def successors(b: Belief, a, succ: Callable, obs: Callable) -> Optional[Dict[object, Belief]]:
    """The beliefs after a, one for each possible observation, or None if a is not applicable in b."""
    out: Dict[object, set] = {}
    for s in b:
        nxt = succ(s, a)
        if not nxt:
            return None
        for t in nxt:
            out.setdefault(obs(t, a), set()).add(t)
    return {o: frozenset(c) for o, c in out.items()}


def and_or_graph(b0: Belief, actions: List, succ: Callable, obs: Callable, goal: Callable):
    """All beliefs reachable from b0 that are not goal beliefs, with their AND branches."""
    edges: Dict[Belief, List[Tuple[object, Dict[object, Belief]]]] = {}
    queue, seen = deque([b0]), {b0}
    while queue:
        b = queue.popleft()
        if all(goal(s) for s in b):
            continue
        edges[b] = []
        for a in actions:
            br = successors(b, a, succ, obs)
            if br is None:
                continue
            edges[b].append((a, br))
            for c in br.values():
                if c not in seen:
                    seen.add(c)
                    queue.append(c)
    return edges


def contingent_plan(init: Iterable[State], goal: Callable, actions: List, succ: Callable, obs: Callable):
    """A plan tree of least worst-case depth, its depth, and the number of beliefs in the graph.

    d(b) = 0 if b is inside the goal, else the least over applicable a of 1 + max over o of d(b_a^o).
    The values are the least fixed point, found by rounds of updates from infinity.
    """
    b0 = frozenset(init)
    edges = and_or_graph(b0, actions, succ, obs, goal)
    d = {b: inf for b in edges}
    val = lambda c: 0 if c not in edges else d[c]
    changed = True
    while changed:
        changed = False
        for b, opts in edges.items():
            best = min((1 + max(val(c) for c in br.values()) for _, br in opts), default=inf)
            if best < d[b]:
                d[b] = best
                changed = True
    if val(b0) == inf:
        return None, inf, len(edges)

    def build(b):
        if b not in edges:
            return "done"
        for a, br in edges[b]:
            if 1 + max(val(c) for c in br.values()) == d[b]:
                return (a, {o: build(c) for o, c in br.items()})

    return build(b0), val(b0), len(edges)


def depth(plan) -> int:
    if plan == "done":
        return 0
    return 1 + max(depth(p) for p in plan[1].values())


def run_ok(plan, s: State, goal: Callable, succ: Callable, obs: Callable) -> bool:
    """Follow the plan from the true state s for every outcome."""
    if plan == "done":
        return goal(s)
    a, branches = plan
    nxt = succ(s, a)
    if not nxt:
        return False
    for t in nxt:
        o = obs(t, a)
        if o not in branches or not run_ok(branches[o], t, goal, succ, obs):
            return False
    return True


def is_valid(plan, init: Iterable[State], goal: Callable, succ: Callable, obs: Callable) -> bool:
    return all(run_ok(plan, s, goal, succ, obs) for s in init)
