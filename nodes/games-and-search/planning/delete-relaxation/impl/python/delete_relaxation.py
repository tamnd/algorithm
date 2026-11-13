# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delete-relaxation/. The authors are listed in prov/JJ5Q8N.jsonl.

"""The delete relaxation of a propositional STRIPS task, and h+ computed exactly.

The relaxed task has the same facts, initial state and goal, and each action
keeps its preconditions and add list but loses its delete list. Relaxed plan
existence is decided by a fixed point in polynomial time. The optimal relaxed
plan cost h+ is NP-hard in general; here it is computed exactly by uniform-cost
search over relaxed states, which is fine for tasks with a few facts.
"""

import heapq
from collections import deque
from typing import Dict, FrozenSet, Hashable, Iterable, List, NamedTuple, Optional, Sequence, Tuple

Fact = Hashable
State = FrozenSet[Fact]
INF = float("inf")


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]
    cost: int = 1


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = (), cost: int = 1) -> Action:
    return Action(name, frozenset(pre), frozenset(add), frozenset(delete), cost)


def relax(actions: Sequence[Action]) -> List[Action]:
    """Drop every delete list."""
    return [a._replace(delete=frozenset()) for a in actions]  # @line L1


def relaxed_closure(state: Iterable[Fact], actions: Sequence[Action]) -> FrozenSet[Fact]:
    """All facts that some relaxed plan from state can make true.
    Each round adds at least one fact or stops, so there are at most |F| + 1 rounds."""
    reached = set(state)  # @line L2
    changed = True
    while changed:  # @line L3
        changed = False
        for a in actions:  # @line L4
            if a.pre <= reached and not a.add <= reached:  # @line L5
                reached |= a.add  # @line L6
                changed = True  # @line L7 (another pass follows only if this pass changed R)
    return frozenset(reached)  # @line L8


def relaxed_solvable(state: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action]) -> bool:
    return frozenset(goal) <= relaxed_closure(state, actions)  # @line L9


def h_plus(state: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action]) -> Tuple[float, Optional[List[Action]]]:
    """The cost of an optimal relaxed plan from state, and one such plan.
    Uniform-cost search over relaxed states (sets of facts that only grow).
    Exponential in the number of facts in the worst case."""
    start = frozenset(state)
    goal = frozenset(goal)
    best: Dict[State, int] = {start: 0}
    parent: Dict[State, Optional[Tuple[State, Action]]] = {start: None}
    heap = [(0, 0, start)]
    tie = 0
    while heap:
        c, _, s = heapq.heappop(heap)
        if c > best[s]:
            continue
        if goal <= s:
            plan = []
            while parent[s] is not None:
                s, a = parent[s]
                plan.append(a)
            return c, plan[::-1]
        for a in actions:
            if a.pre <= s and not a.add <= s:     # an action that adds nothing new is never useful
                t = s | a.add
                nc = c + a.cost
                if t not in best or nc < best[t]:
                    best[t] = nc
                    parent[t] = (s, a)
                    tie += 1
                    heapq.heappush(heap, (nc, tie, t))
    return INF, None


def set_cover_task(universe: Iterable[Fact], sets: Sequence[Iterable[Fact]]):
    """The reduction from set cover: one delete-free action per set, which adds its
    elements. h+ of the initial (empty) state is the size of a smallest cover."""
    acts = [make_action(f"take{i}", [], s, []) for i, s in enumerate(sets)]
    return frozenset(), frozenset(universe), acts


def optimal_cost(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action]) -> float:
    """Reference h*: Dijkstra over the real (not relaxed) states."""
    init = frozenset(init)
    goal = frozenset(goal)
    best = {init: 0}
    heap = [(0, 0, init)]
    tie = 0
    while heap:
        c, _, s = heapq.heappop(heap)
        if c > best[s]:
            continue
        if goal <= s:
            return c
        for a in actions:
            if a.pre <= s:
                t = (s - a.delete) | a.add
                if t not in best or c + a.cost < best[t]:
                    best[t] = c + a.cost
                    tie += 1
                    heapq.heappush(heap, (c + a.cost, tie, t))
    return INF


def reachable(init: Iterable[Fact], actions: Sequence[Action]) -> Dict[State, int]:
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


def two_package_task():
    """One truck at A, packages p1 and p2 at A, both must go to B."""
    acts = [
        make_action("drive(A,B)", ["tA"], ["tB"], ["tA"]),
        make_action("drive(B,A)", ["tB"], ["tA"], ["tB"]),
    ]
    for p in ("p1", "p2"):
        for x in ("A", "B"):
            acts.append(make_action(f"load({p},{x})", ["t" + x, f"{p}@{x}"], [f"{p}@T"], [f"{p}@{x}"]))
            acts.append(make_action(f"unload({p},{x})", ["t" + x, f"{p}@T"], [f"{p}@{x}"], [f"{p}@T"]))
    return frozenset(["tA", "p1@A", "p2@A"]), frozenset(["p1@B", "p2@B"]), acts
