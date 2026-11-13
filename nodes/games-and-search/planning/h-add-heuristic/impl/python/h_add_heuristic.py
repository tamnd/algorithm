# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/h-add-heuristic/. The authors are listed in prov/FN069M.jsonl.

"""The additive heuristic h_add for propositional STRIPS with nonnegative costs.

h_add(s) is the sum over goal facts p of g(p), where g is the least fixed point of
    g(p) = 0                                            if p is in s
    g(p) = min over actions a that add p of cost(a) + sum over q in pre(a) of g(q)

The fixed point is computed by a generalized Dijkstra (Knuth 1977) or by a
Bellman-Ford loop. The Dijkstra version also records a best supporter for each
fact, and the supporters of the goal facts, followed back through their
preconditions, form a relaxed plan whose cost is at most h_add(s).
"""

import heapq
from typing import Dict, FrozenSet, Hashable, Iterable, List, NamedTuple, Optional, Sequence, Tuple

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


def fact_costs_dijkstra(state: Iterable[Fact], actions: Sequence[Action]) -> Tuple[Dict[Fact, float], Dict[Fact, Optional[Action]], List[Fact]]:
    """Returns g, a best supporter for each fact (None for facts of the state),
    and the facts in the order they were fixed."""
    g: Dict[Fact, float] = {}  # @line L1 (a missing key means the value infinity)
    support: Dict[Fact, Optional[Action]] = {}
    order: List[Fact] = []
    heap = []
    tie = 0
    for p in state:  # @line L2
        heap.append((0, tie, p, None))
        tie += 1
    waiting = [len(a.pre) for a in actions]  # @line L3
    users: Dict[Fact, list] = {}
    for i, a in enumerate(actions):
        for q in a.pre:
            users.setdefault(q, []).append(i)
    for i, a in enumerate(actions):
        if waiting[i] == 0:  # @line L4
            for p in a.add:
                heap.append((a.cost, tie, p, i))
                tie += 1
    heapq.heapify(heap)
    while heap:  # @line L5
        c, _, p, i = heapq.heappop(heap)  # @line L6
        if p in g:  # @line L7
            continue
        g[p] = c  # @line L8
        support[p] = None if i is None else actions[i]
        order.append(p)
        for j in users.get(p, ()):  # @line L9
            waiting[j] -= 1  # @line L10
            if waiting[j] == 0:  # @line L11 (every precondition is fixed now)
                a = actions[j]
                v = a.cost + sum(g[q] for q in a.pre)  # @line L12
                for r in a.add:  # @line L13
                    if r not in g:
                        tie += 1
                        heapq.heappush(heap, (v, tie, r, j))
    return g, support, order


def fact_costs_bellman_ford(state: Iterable[Fact], actions: Sequence[Action]) -> Dict[Fact, float]:
    g: Dict[Fact, float] = {p: 0 for p in state}
    changed = True
    while changed:
        changed = False
        for a in actions:
            if all(q in g for q in a.pre):
                v = a.cost + sum(g[q] for q in a.pre)
                for p in a.add:
                    if v < g.get(p, INF):
                        g[p] = v
                        changed = True
    return g


def h_add(state: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action], method: str = "dijkstra") -> float:
    if method == "dijkstra":
        g = fact_costs_dijkstra(state, actions)[0]
    elif method == "bellman-ford":
        g = fact_costs_bellman_ford(state, actions)
    else:
        raise ValueError(method)
    return sum(g.get(p, INF) for p in goal)  # @line L14


def best_supporter_plan(state: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action]) -> Optional[List[Action]]:
    """A relaxed plan built from best supporters, in an order that is executable
    in the delete relaxation. None if some goal fact is unreachable."""
    g, support, order = fact_costs_dijkstra(state, actions)  # @line L15
    goal = frozenset(goal)
    if any(p not in g for p in goal):
        return None
    needed = set()
    stack = list(goal)
    seen = set()
    while stack:  # @line L16
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        a = support[p]
        if a is not None:
            needed.add(a)
            stack.extend(a.pre)
    # a supporter is pushed only after all its preconditions are fixed, so the
    # order in which the supported facts were fixed is a valid order of actions
    plan: List[Action] = []
    for p in order:  # @line L17
        a = support[p]
        if a in needed and a not in plan:
            plan.append(a)
    return plan
