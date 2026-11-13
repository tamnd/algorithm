# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hsp-planner/. The authors are listed in prov/WZK9NT.jsonl.

"""HSP: forward state-space search guided by the additive heuristic.

hsp2 is the HSP2 configuration of Bonet and Geffner (2001): weighted A* with
f = g + W * h_add and W = 5 by default. States with h_add = infinity are dead
ends of the delete relaxation and are pruned, since no plan leaves them.

hsp1 is the original HSP: hill climbing on h_add. It moves to a best child
(ties broken at random), prefers children it has not visited in the current
climb, and restarts from the initial state after too many moves that do not
improve h.
"""

import heapq
import random
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


def successor(s: State, a: Action) -> State:
    return (s - a.delete) | a.add


def is_plan(init: Iterable[Fact], goal: Iterable[Fact], plan: Sequence[Action]) -> bool:
    s = frozenset(init)
    for a in plan:
        if not a.pre <= s:
            return False
        s = successor(s, a)
    return frozenset(goal) <= s


class HAdd:
    """h_add with a precomputed index from facts to the actions that need them.
    Each call runs the generalized Dijkstra in O(sum of action sizes * log)."""

    def __init__(self, goal: Iterable[Fact], actions: Sequence[Action]):
        self.goal = frozenset(goal)
        self.actions = list(actions)
        self.users: Dict[Fact, List[int]] = {}
        for i, a in enumerate(self.actions):
            for q in a.pre:
                self.users.setdefault(q, []).append(i)
        self.free = [i for i, a in enumerate(self.actions) if not a.pre]
        self.calls = 0

    def __call__(self, s: State) -> float:
        self.calls += 1
        g: Dict[Fact, float] = {}
        heap = [(0, k, p) for k, p in enumerate(s)]     # the counter keeps facts from being compared
        tie = len(heap)
        for i in self.free:
            a = self.actions[i]
            for p in a.add:
                heap.append((a.cost, tie, p))
                tie += 1
        heapq.heapify(heap)
        waiting = [len(a.pre) for a in self.actions]
        left = len(self.goal)
        total = 0
        while heap and left:
            c, _, p = heapq.heappop(heap)
            if p in g:
                continue
            g[p] = c
            if p in self.goal:
                left -= 1
                total += c
            for j in self.users.get(p, ()):
                waiting[j] -= 1
                if waiting[j] == 0:
                    a = self.actions[j]
                    v = a.cost + sum(g[q] for q in a.pre)
                    for r in a.add:
                        if r not in g:
                            tie += 1
                            heapq.heappush(heap, (v, tie, r))
        return INF if left else total


class Stats(NamedTuple):
    expanded: int
    evaluated: int


def hsp2(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action], weight: float = 5) -> Tuple[Optional[List[Action]], Stats]:
    """Weighted A* with h_add. Complete on every finite task: a state is put
    back on the open list whenever a cheaper path to it is found."""
    init = frozenset(init)
    goal = frozenset(goal)
    h = HAdd(goal, actions)  # @line L1
    h0 = h(init)
    if h0 == INF:  # @line L2
        return None, Stats(0, h.calls)
    hval: Dict[State, float] = {init: h0}
    best: Dict[State, float] = {init: 0}  # @line L3
    parent: Dict[State, Optional[Tuple[State, Action]]] = {init: None}
    heap = [(weight * h0, 0, 0, init)]
    tie = 0
    expanded = 0
    while heap:  # @line L4
        _, gs, _, s = heapq.heappop(heap)  # @line L5
        if gs > best[s]:
            continue                                # a stale entry: a cheaper path to s was found later
        if goal <= s:  # @line L6
            plan = []
            while parent[s] is not None:
                s, a = parent[s]
                plan.append(a)
            return plan[::-1], Stats(expanded, h.calls)
        expanded += 1
        for a in actions:
            if a.pre <= s:  # @line L7
                t = successor(s, a)  # @line L8
                gt = gs + a.cost
                if gt < best.get(t, INF):  # @line L9
                    if t not in hval:
                        hval[t] = h(t)
                    if hval[t] == INF:  # @line L10
                        continue                    # relaxed dead end
                    best[t] = gt  # @line L11
                    parent[t] = (s, a)
                    tie += 1
                    heapq.heappush(heap, (gt + weight * hval[t], gt, tie, t))  # @line L12
    return None, Stats(expanded, h.calls)  # @line L13


def hsp1(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action], seed: int = 0,
         max_plateau: int = 20, max_restarts: int = 50, max_steps: int = 10000) -> Optional[List[Action]]:
    """Hill climbing on h_add with random tie breaking and restarts.
    Incomplete: it can return None on a solvable task."""
    rng = random.Random(seed)
    init = frozenset(init)
    goal = frozenset(goal)
    h = HAdd(goal, actions)
    cache: Dict[State, float] = {}

    def hv(s):
        if s not in cache:
            cache[s] = h(s)
        return cache[s]

    if hv(init) == INF:
        return None
    for _ in range(max_restarts):
        s, plan, visited = init, [], {init}
        best_h, plateau = hv(init), 0
        for _ in range(max_steps):
            if goal <= s:
                return plan
            children = [(hv(successor(s, a)), successor(s, a) in visited, a) for a in actions if a.pre <= s]
            children = [c for c in children if c[0] < INF]
            fresh = [c for c in children if not c[1]]
            if fresh:
                children = fresh             # prefer states not seen in this climb
            if not children:
                break
            m = min(c[0] for c in children)
            hm, seen, a = rng.choice([c for c in children if c[0] == m])
            s = successor(s, a)
            plan.append(a)
            visited.add(s)
            if hm < best_h and not seen:
                best_h, plateau = hm, 0
            else:
                plateau += 1
                if plateau > max_plateau:
                    break
    return None
