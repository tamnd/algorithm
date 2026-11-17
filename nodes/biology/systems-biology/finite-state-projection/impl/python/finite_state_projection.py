# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-state-projection/. The authors are listed in prov/62X0PG.jsonl.
"""The finite state projection (FSP) of Munsky and Khammash (2006).

A network with n species and m reactions is given by stoich (the m change
vectors) and propensity(x) (the m propensities of the state x). The
chemical master equation is dP/dt = A P for the generator A on all states.
The FSP keeps a finite set J of states and solves dp/dt = A_J p, where A_J
is A with the rows and columns outside J removed. Probability that flows
out of J is lost, so 1 - sum(p) is the mass that left J. That mass is a
bound on the L1 error of p against the exact solution.

exp(A_J t) p0 is computed by uniformization: with q >= max a0(x) on J,
P = I + A_J / q has entries >= 0 and exp(A_J t) = sum over k of
Poisson(k; q t) P^k. Every term is >= 0, so cutting the series only lowers
the result, and the computed mass that left J is still an upper bound on
the error.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, List, Sequence, Tuple

State = Tuple[int, ...]


def project_generator(states: Sequence[State], stoich: Sequence[Sequence[int]],
                      propensity: Callable[[State], Sequence[float]]):
    """The sparse generator A_J on the list `states`.

    Returns (out_rate, edges): out_rate[s] = a0 of states[s] (the negative
    of the diagonal of A_J), and edges is a list of (s, r, rate) for the
    flows from states[s] to states[r] inside J. Flows to states outside J
    are left out: that mass is lost.
    """
    index = {x: s for s, x in enumerate(states)}
    out_rate = []
    edges = []
    for s, x in enumerate(states):
        a = propensity(x)
        total = 0.0
        for j, aj in enumerate(a):
            if aj < 0:
                raise ValueError("propensities must be >= 0")
            if aj == 0:
                continue
            total += aj
            y = tuple(x[i] + stoich[j][i] for i in range(len(x)))
            r = index.get(y)
            if r is not None:
                edges.append((s, r, aj))
        out_rate.append(total)
    return out_rate, edges


def expm_action(out_rate: Sequence[float], edges, p0: Sequence[float], t: float,
                tol: float = 1e-15) -> List[float]:
    """exp(A_J t) p0 by uniformization, in pieces with q dt <= 10."""
    q = max(out_rate, default=0.0)
    p = [float(v) for v in p0]
    if q == 0.0 or t == 0.0:
        return p
    pieces = max(1, math.ceil(q * t / 10.0))
    lam = q * t / pieces
    keep = [1.0 - r / q for r in out_rate]
    k_max = int(lam + 10.0 * math.sqrt(lam) + 40)
    for _ in range(pieces):
        term = p
        weight = math.exp(-lam)
        acc = [weight * v for v in term]
        cum = weight
        for k in range(1, k_max + 1):
            nxt = [keep[s] * term[s] for s in range(len(term))]
            for s, r, rate in edges:
                nxt[r] += rate / q * term[s]
            term = nxt
            weight *= lam / k
            cum += weight
            for s in range(len(acc)):
                acc[s] += weight * term[s]
            if 1.0 - cum < tol:
                break
        p = acc
    return p


def neighbors(states: Sequence[State], stoich, propensity) -> List[State]:
    """The states outside `states` that one reaction with a positive
    propensity reaches from a state in `states`."""
    inside = set(states)
    new = []
    for x in states:
        for j, aj in enumerate(propensity(x)):
            if aj > 0:
                y = tuple(x[i] + stoich[j][i] for i in range(len(x)))
                if y not in inside:
                    inside.add(y)
                    new.append(y)
    return new


def finite_state_projection(x0: Sequence[int], stoich: Sequence[Sequence[int]],
                            propensity: Callable[[State], Sequence[float]], t: float,
                            eps: float, initial: Sequence[State] = (), max_states: int = 20000):
    """Grow J from {x0} (and `initial`) until the mass that left J by time t
    is at most eps.

    Returns (states, p, lost, rounds): p[s] is the FSP probability of
    states[s] at time t, lost = 1 - sum(p), and rounds is the number of
    solves. Then 0 <= P(x, t) - p(x) for every x in J, and the sum of
    |P(x, t) - p(x)| over all states (p = 0 outside J) is lost.
    """
    x0 = tuple(int(v) for v in x0)
    states = [x0] + [tuple(s) for s in initial if tuple(s) != x0]  # @line L1
    rounds = 0
    while True:  # @line L2
        out_rate, edges = project_generator(states, stoich, propensity)  # @line L3
        p0 = [1.0 if s == 0 else 0.0 for s in range(len(states))]
        p = expm_action(out_rate, edges, p0, t)  # @line L4
        rounds += 1
        lost = 1.0 - sum(p)
        if lost <= eps:  # @line L5
            return states, p, lost, rounds
        new = neighbors(states, stoich, propensity)  # @line L6
        if not new or len(states) + len(new) > max_states:
            raise RuntimeError("the projection cannot grow to reach the tolerance")
        states = states + new
