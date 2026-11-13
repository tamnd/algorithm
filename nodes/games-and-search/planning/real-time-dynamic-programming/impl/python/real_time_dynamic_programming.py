# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/real-time-dynamic-programming/. The authors are listed in prov/X8DWC2.jsonl.

"""Trial-based real-time dynamic programming (RTDP) for stochastic shortest path problems.

A model maps each non-goal state to a dict of actions. An action maps to a pair
(cost, outcomes), where outcomes is a list of (probability, next state). Goal
states are absorbing, cost nothing and do not appear as keys. Costs should be
positive and the start values admissible (no larger than the optimal costs).
"""

import heapq
import random
from typing import Callable, Dict, Hashable, List, Optional, Set, Tuple

State = Hashable
Action = Hashable
Model = Dict[State, Dict[Action, Tuple[float, List[Tuple[float, State]]]]]


def q_value(model: Model, goals: Set[State], v: Dict[State, float], h, s: State, a: Action) -> float:
    cost, outcomes = model[s][a]
    total = cost
    for p, t in outcomes:
        if t not in goals:
            if t not in v:
                v[t] = h(t)  # a state gets its start value the first time it is seen
            total += p * v[t]
    return total


def greedy_action(model: Model, goals: Set[State], v, h, s: State) -> Tuple[Action, float]:
    """The action of least Q-value; ties go to the first action in the model's order."""
    best_a, best_q = None, None
    for a in model[s]:
        q = q_value(model, goals, v, h, s, a)
        if best_q is None or q < best_q:
            best_a, best_q = a, q
    return best_a, best_q


def sample(outcomes: List[Tuple[float, State]], rng: random.Random) -> State:
    x = rng.random()
    acc = 0.0
    for p, t in outcomes:
        acc += p
        if x < acc:
            return t
    return outcomes[-1][1]


def rtdp(
    model: Model,
    goals: Set[State],
    s0: State,
    h: Callable[[State], float],
    trials: int,
    rng: random.Random,
    max_steps: int = 10_000,
    v: Optional[Dict[State, float]] = None,
    backups: Optional[Dict[State, int]] = None,
) -> Tuple[Dict[State, float], List[int]]:
    """Run the given number of trials from s0. Returns the value table and the trial lengths.

    Only states that the trials visit, or see as outcomes, get an entry in the table.
    If backups is given, it counts the backups made at each state.
    """
    v = {} if v is None else v
    lengths = []
    for _ in range(trials):  # @line L2
        s = s0  # @line L3
        steps = 0
        while s not in goals and steps < max_steps:  # @line L4
            if s not in v:
                v[s] = h(s)  # @line L1
            a, q = greedy_action(model, goals, v, h, s)  # @line L5
            v[s] = q  # @line L6
            if backups is not None:
                backups[s] = backups.get(s, 0) + 1
            s = sample(model[s][a][1], rng)  # @line L7
            steps += 1
        lengths.append(steps)
    return v, lengths  # @line L8


def greedy_policy(model: Model, goals: Set[State], v, h, s0: State) -> Dict[State, Action]:
    """The greedy policy on the states it reaches from s0."""
    pi, stack = {}, [s0]
    while stack:
        s = stack.pop()
        if s in goals or s in pi:
            continue
        a, _ = greedy_action(model, goals, v, h, s)
        pi[s] = a
        for p, t in model[s][a][1]:
            if p > 0:
                stack.append(t)
    return pi


def h_min(model: Model, goals: Set[State]) -> Dict[State, float]:
    """h(s) = min over a of c(s, a) + min over outcomes s' of h(s'), with h = 0 on goals.

    It is the cost to the goal when each action may pick its best outcome, so it is a
    lower bound on the optimal cost, and h <= T h. Computed by Dijkstra's algorithm on
    the reversed all-outcome determinization.
    """
    rev: Dict[State, List[Tuple[State, float]]] = {}
    for s, acts in model.items():
        for a, (c, outs) in acts.items():
            for p, t in outs:
                if p > 0:
                    rev.setdefault(t, []).append((s, c))
    dist = {g: 0.0 for g in goals}
    heap = [(0.0, i, g) for i, g in enumerate(goals)]
    heapq.heapify(heap)
    count = len(heap)
    while heap:
        d, _, u = heapq.heappop(heap)
        if d > dist.get(u, float("inf")):
            continue
        for s, c in rev.get(u, []):
            if d + c < dist.get(s, float("inf")):
                dist[s] = d + c
                count += 1
                heapq.heappush(heap, (d + c, count, s))
    return {s: dist.get(s, float("inf")) for s in model}
