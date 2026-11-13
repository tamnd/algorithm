# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-shortest-path/. The authors are listed in prov/4D16F2.jsonl.

"""Reference code for small stochastic shortest path (SSP) problems.

A model maps each non-goal state to a dict of actions. An action maps to a
pair (cost, outcomes), where outcomes is a list of (probability, next state).
Goal states are absorbing, cost nothing and do not appear as keys.
"""

from fractions import Fraction
from itertools import product
from typing import Dict, Hashable, List, Optional, Set, Tuple

State = Hashable
Action = Hashable
Model = Dict[State, Dict[Action, Tuple[Fraction, List[Tuple[Fraction, State]]]]]
Values = Dict[State, Fraction]
Policy = Dict[State, Action]


def q_value(model: Model, goals: Set[State], v, s: State, a: Action):
    cost, outcomes = model[s][a]
    return cost + sum(p * (0 if t in goals else v[t]) for p, t in outcomes)


def bellman_operator(model: Model, goals: Set[State], v):
    return {s: min(q_value(model, goals, v, s, a) for a in model[s]) for s in model}


def greedy_policy(model: Model, goals: Set[State], v) -> Policy:
    return {s: min(model[s], key=lambda a: q_value(model, goals, v, s, a)) for s in model}


def value_iteration(model: Model, goals: Set[State], start, eps: float, max_sweeps: int):
    """Jacobi value iteration. Stops when the largest change in a sweep is at most eps.

    Returns (values, sweeps). Raises RuntimeError if it does not stop within max_sweeps,
    which is what happens when a state is a dead end.
    """
    v = dict(start)
    for sweep in range(1, max_sweeps + 1):
        w = bellman_operator(model, goals, v)
        change = max(abs(w[s] - v[s]) for s in model)
        v = w
        if change <= eps:
            return v, sweep
    raise RuntimeError("value iteration did not converge")


def is_proper(model: Model, goals: Set[State], policy: Policy) -> bool:
    """A stationary policy is proper when a goal is reachable from every state in its chain."""
    good = set(goals)
    changed = True
    while changed:
        changed = False
        for s in model:
            if s not in good and any(p > 0 and t in good for p, t in model[s][policy[s]][1]):
                good.add(s)
                changed = True
    return all(s in good for s in model)


def proper_states(model: Model, goals: Set[State]) -> Set[State]:
    """States from which some policy reaches a goal with probability 1.

    The greatest set W such that from each state of W a goal can be reached using
    only actions whose outcomes all stay in W (or are goals). States outside W are
    dead ends in the sense used here: no proper policy exists from them.
    """
    w = set(model)
    while True:
        def safe(s, a):
            return all(p == 0 or t in goals or t in w for p, t in model[s][a][1])

        reach = set(goals)
        changed = True
        while changed:
            changed = False
            for s in w:
                if s not in reach and any(
                    safe(s, a) and any(p > 0 and t in reach for p, t in model[s][a][1]) for a in model[s]
                ):
                    reach.add(s)
                    changed = True
        new_w = {s for s in w if s in reach}
        if new_w == w:
            return w
        w = new_w


def all_policies_proper(model: Model, goals: Set[State]) -> bool:
    """True when every policy (stationary or not) reaches a goal with probability 1.

    Builds layers L_0 = goals and L_(k+1) = L_k plus the states all of whose actions
    can move into L_k; every policy is proper exactly when the layers cover all states.
    """
    layer = set(goals)
    changed = True
    while changed:
        changed = False
        for s in model:
            if s not in layer and all(any(p > 0 and t in layer for p, t in model[s][a][1]) for a in model[s]):
                layer.add(s)
                changed = True
    return all(s in layer for s in model)


def solve_linear(a: List[List[Fraction]], b: List[Fraction]) -> List[Fraction]:
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        inv = 1 / m[col][col]
        m[col] = [x * inv for x in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [m[i][n] for i in range(n)]


def policy_cost(model: Model, goals: Set[State], policy: Policy) -> Values:
    """Exact cost of a proper policy, by solving (I - P_mu) V = c_mu with Fraction."""
    if not is_proper(model, goals, policy):
        raise ValueError("the policy is improper")
    states = list(model)
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    a = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    b = [Fraction(0)] * n
    for s in states:
        cost, outcomes = model[s][policy[s]]
        b[idx[s]] = Fraction(cost)
        for p, t in outcomes:
            if t not in goals:
                a[idx[s]][idx[t]] -= p
    x = solve_linear(a, b)
    return {s: x[idx[s]] for s in states}


def optimal_by_enumeration(model: Model, goals: Set[State]) -> Tuple[Values, Policy]:
    """Try every deterministic stationary policy and return the best proper one.

    Under the assumptions of Bertsekas and Tsitsiklis one proper policy is best at
    every state; ValueError is raised if no proper policy exists or none is best everywhere.
    """
    states = list(model)
    found = []
    for choice in product(*(list(model[s]) for s in states)):
        pi = dict(zip(states, choice))
        if is_proper(model, goals, pi):
            found.append((policy_cost(model, goals, pi), pi))
    if not found:
        raise ValueError("no proper policy")
    low = {s: min(v[s] for v, _ in found) for s in states}
    for v, pi in found:
        if v == low:
            return v, pi
    raise ValueError("no proper policy is optimal at every state")


def with_give_up(model: Model, goal: State, penalty: Fraction) -> Model:
    """Add an action that pays the penalty and moves to the goal (the finite penalty model)."""
    out = {}
    for s, acts in model.items():
        acts = dict(acts)
        acts["give up"] = (Fraction(penalty), [(Fraction(1), goal)])
        out[s] = acts
    return out
