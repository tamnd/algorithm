# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bellman-equation/. The authors are listed in prov/Y80W1T.jsonl.

"""The Bellman equation in its total cost and finite horizon forms.

A model maps each non-goal state to a dict of actions. An action maps to a
pair (cost, outcomes), where outcomes is a list of (probability, next state).
Goal states are absorbing and cost nothing, so they do not appear as keys.
Use Fraction for probabilities and costs to get exact answers.
"""

from fractions import Fraction
from itertools import product
from typing import Dict, Hashable, List, Optional, Sequence, Set, Tuple

State = Hashable
Action = Hashable
Outcomes = List[Tuple[Fraction, State]]
Model = Dict[State, Dict[Action, Tuple[Fraction, Outcomes]]]
Values = Dict[State, Fraction]
Policy = Dict[State, Action]


def value_of(values: Values, goals: Set[State], s: State) -> Fraction:
    """V(s), with V = 0 on goal states."""
    return Fraction(0) if s in goals else values[s]


def q_value(model: Model, goals: Set[State], values: Values, s: State, a: Action) -> Fraction:
    """c(s, a) + sum over s' of P(s' | s, a) V(s')."""
    cost, outcomes = model[s][a]
    return cost + sum((p * value_of(values, goals, t) for p, t in outcomes), Fraction(0))


def backup(model: Model, goals: Set[State], values: Values, s: State) -> Tuple[Fraction, Action]:
    """The right side of the Bellman equation at s, and the first action that attains it."""
    best_a = None
    best_q: Optional[Fraction] = None
    for a in model[s]:
        q = q_value(model, goals, values, s, a)
        if best_q is None or q < best_q:
            best_q, best_a = q, a
    if best_q is None:
        raise ValueError(f"state {s!r} has no action")
    return best_q, best_a


def bellman_operator(model: Model, goals: Set[State], values: Values) -> Values:
    """(T V)(s) for every non-goal state s."""
    return {s: backup(model, goals, values, s)[0] for s in model}


def is_fixed_point(model: Model, goals: Set[State], values: Values) -> bool:
    return bellman_operator(model, goals, values) == values


def greedy_policy(model: Model, goals: Set[State], values: Values) -> Policy:
    return {s: backup(model, goals, values, s)[1] for s in model}


def backward_induction(
    model: Model, goals: Set[State], horizon: int, terminal: Optional[Values] = None
) -> Tuple[List[Values], List[Policy]]:
    """V_0 = terminal, V_k = T V_{k-1}. Returns [V_0 .. V_H] and [pi_1 .. pi_H].

    pi_k is the action to take when k steps remain.
    """
    v = dict(terminal) if terminal is not None else {s: Fraction(0) for s in model}
    values = [v]
    policies: List[Policy] = []
    for _ in range(horizon):
        policies.append(greedy_policy(model, goals, v))
        v = bellman_operator(model, goals, v)
        values.append(v)
    return values, policies


def reaches_goal(model: Model, goals: Set[State], policy: Policy) -> bool:
    """True when the policy is proper: every state reaches a goal with probability 1.

    In a finite Markov chain this holds exactly when a goal is reachable along
    positive probability edges from every state.
    """
    good = set(goals)
    changed = True
    while changed:
        changed = False
        for s in model:
            if s not in good and any(p > 0 and t in good for p, t in model[s][policy[s]][1]):
                good.add(s)
                changed = True
    return all(s in good for s in model)


def solve_linear(a: List[List[Fraction]], b: List[Fraction]) -> List[Fraction]:
    """Solve a x = b exactly by Gauss-Jordan elimination. a must be nonsingular."""
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
    """Exact cost of a proper policy: solve V = c_pi + P_pi V on the non-goal states."""
    if not reaches_goal(model, goals, policy):
        raise ValueError("the policy is improper")
    states = list(model)
    index = {s: i for i, s in enumerate(states)}
    n = len(states)
    a = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    b = [Fraction(0)] * n
    for s in states:
        cost, outcomes = model[s][policy[s]]
        b[index[s]] = Fraction(cost)
        for p, t in outcomes:
            if t not in goals:
                a[index[s]][index[t]] -= p
    x = solve_linear(a, b)
    return {s: x[index[s]] for s in states}


def best_proper_policy(model: Model, goals: Set[State]) -> Tuple[Values, Policy]:
    """Enumerate every deterministic stationary policy, keep the proper ones, and
    return the one whose cost is smallest at every state.

    Under the assumptions of Bertsekas and Tsitsiklis such a policy exists.
    Raises ValueError if no proper policy exists or no policy is best everywhere.
    """
    states = list(model)
    best: Optional[Values] = None
    best_pi: Optional[Policy] = None
    candidates = []
    for choice in product(*(list(model[s]) for s in states)):
        pi = dict(zip(states, choice))
        if reaches_goal(model, goals, pi):
            candidates.append((policy_cost(model, goals, pi), pi))
    if not candidates:
        raise ValueError("no proper policy")
    low = {s: min(v[s] for v, _ in candidates) for s in states}
    for v, pi in candidates:
        if v == low:
            best, best_pi = v, pi
            break
    if best is None or best_pi is None:
        raise ValueError("no proper policy is optimal at every state")
    return best, best_pi


def trajectory_values(values: Sequence[Values], s: State) -> List[Fraction]:
    """The sequence V_0(s), V_1(s), ... from a list of value functions."""
    return [v[s] for v in values]
