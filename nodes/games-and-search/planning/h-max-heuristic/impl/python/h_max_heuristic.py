# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/h-max-heuristic/. The authors are listed in prov/7HHW76.jsonl.

"""The h-max heuristic for propositional STRIPS with nonnegative action costs.

h_max(s) is the least fixed point of
    g(p) = 0                                            if p is in s
    g(p) = min over actions a that add p of cost(a) + max over q in pre(a) of g(q)
and h_max(s) = max over goal facts p of g(p). The max of an empty set is 0.

Two ways to compute it are given: a generalized Dijkstra (Knuth 1977), which
fixes facts in order of their value, and a plain Bellman-Ford loop, which
updates every action until nothing changes.
"""

import heapq
from typing import Dict, FrozenSet, Hashable, Iterable, NamedTuple, Sequence

Fact = Hashable
INF = float("inf")


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]
    cost: int = 1


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = (), cost: int = 1) -> Action:
    return Action(name, frozenset(pre), frozenset(add), frozenset(delete), cost)


def fact_costs_dijkstra(state: Iterable[Fact], actions: Sequence[Action]) -> Dict[Fact, float]:
    """g(p) for every reachable fact p. A fact that is missing has value INF.
    An action fires when its last precondition is fixed; its value is then
    cost + the value of that last precondition, which is the max over pre."""
    g: Dict[Fact, float] = {}  # @line L1 (a missing key means the value infinity)
    heap = []
    tie = 0
    for p in state:  # @line L2
        heap.append((0, tie, p))
        tie += 1
    waiting = [len(a.pre) for a in actions]  # @line L3
    users: Dict[Fact, list] = {}
    for i, a in enumerate(actions):
        for q in a.pre:
            users.setdefault(q, []).append(i)
    for i, a in enumerate(actions):
        if waiting[i] == 0:  # @line L4
            for p in a.add:
                heap.append((a.cost, tie, p))
                tie += 1
    heapq.heapify(heap)
    while heap:  # @line L5
        c, _, p = heapq.heappop(heap)  # @line L6
        if p in g:  # @line L7
            continue
        g[p] = c  # @line L8 (p is fixed: its value is final)
        for i in users.get(p, ()):  # @line L9
            waiting[i] -= 1  # @line L10
            if waiting[i] == 0:  # @line L11 (p is the last precondition, so g(p) is the max)
                a = actions[i]
                for r in a.add:  # @line L12
                    if r not in g:
                        tie += 1
                        heapq.heappush(heap, (c + a.cost, tie, r))
    return g


def fact_costs_bellman_ford(state: Iterable[Fact], actions: Sequence[Action]) -> Dict[Fact, float]:
    """The same values by repeated updates until a fixed point."""
    g: Dict[Fact, float] = {p: 0 for p in state}
    changed = True
    while changed:
        changed = False
        for a in actions:
            if all(q in g for q in a.pre):
                v = a.cost + max((g[q] for q in a.pre), default=0)
                for p in a.add:
                    if v < g.get(p, INF):
                        g[p] = v
                        changed = True
    return g


def h_max(state: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action], method: str = "dijkstra") -> float:
    if method == "dijkstra":
        g = fact_costs_dijkstra(state, actions)
    elif method == "bellman-ford":
        g = fact_costs_bellman_ford(state, actions)
    else:
        raise ValueError(method)
    return max((g.get(p, INF) for p in goal), default=0)  # @line L13
