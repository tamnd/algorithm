# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plan-recognition/. The authors are listed in prov/Y0RPP5.jsonl.

"""Plan recognition as planning, after Ramirez and Geffner (2009, 2010).

A domain maps each state to a dict from actions to next states; every action costs 1.
The observations are a sequence of actions that must appear in the plan in that order,
not always next to each other. A plan complies with the observations if they embed in it.
"""

import heapq
from fractions import Fraction
from math import inf
from typing import Dict, Hashable, List, Sequence

State = Hashable


def cost_with(dom, s0: State, goal: State, obs: Sequence, comply: bool):
    """Least cost of a plan from s0 to goal that does (comply=True) or does not embed obs.

    Search in the product of the domain with the index j of the observations matched so far.
    Greedy matching is enough to decide if a sequence embeds in a plan."""
    m = len(obs)
    start = (s0, 0)
    dist = {start: 0}
    heap = [(0, 0, start)]
    order = 1
    while heap:
        d, _, (s, j) = heapq.heappop(heap)
        if d > dist[(s, j)]:
            continue
        if s == goal and (j == m) == comply:
            return d
        for a, t in dom[s].items():
            k = j + 1 if j < m and a == obs[j] else j
            if dist.get((t, k), inf) > d + 1:
                dist[t, k] = d + 1
                heapq.heappush(heap, (d + 1, order, (t, k)))
                order += 1
    return inf


def optimal_cost(dom, s0: State, goal: State):
    return cost_with(dom, s0, goal, [], True)


def compatible_goals(dom, s0: State, goals: Sequence[State], obs: Sequence) -> List[State]:
    """Ramirez and Geffner 2009: the goals with an optimal plan that embeds the observations."""
    return [g for g in goals if cost_with(dom, s0, g, obs, True) == optimal_cost(dom, s0, g) < inf]


def likelihood(c_obs, c_not, base: Fraction = Fraction(1, 2)) -> Fraction:
    """P(O | G) = 1 / (1 + exp(-beta * (c_not - c_obs))), with exp(-beta) = base, so the result is exact."""
    if c_obs == inf:
        return Fraction(0)
    if c_not == inf:
        return Fraction(1)
    w_obs, w_not = base ** c_obs, base ** c_not
    return w_obs / (w_obs + w_not)


def posterior(dom, s0: State, goals: Sequence[State], obs: Sequence, prior=None, base=Fraction(1, 2)) -> Dict:
    """Ramirez and Geffner 2010: P(G | O) proportional to P(O | G) P(G), with the cost difference likelihood."""
    prior = prior or {g: Fraction(1, len(goals)) for g in goals}
    lik = {g: likelihood(cost_with(dom, s0, g, obs, True), cost_with(dom, s0, g, obs, False), base) for g in goals}
    z = sum(lik[g] * prior[g] for g in goals)
    if z == 0:
        return {g: Fraction(0) for g in goals}
    return {g: lik[g] * prior[g] / z for g in goals}


def boltzmann_posterior(dom, s0: State, goals: Sequence[State], obs: Sequence, horizon: int,
                        prior=None, base=Fraction(1, 2)) -> Dict:
    """P(G | O) when the agent picks a plan for G of at most horizon steps with weight base^cost.

    Sums over all plans by dynamic programming over (state, observations matched)."""
    prior = prior or {g: Fraction(1, len(goals)) for g in goals}
    m = len(obs)
    layer = {(s0, 0): Fraction(1)}
    total = {g: Fraction(0) for g in goals}
    match = {g: Fraction(0) for g in goals}
    for step in range(horizon + 1):
        for (s, j), w in layer.items():
            if s in total:
                total[s] += w
                if j == m:
                    match[s] += w
        if step == horizon:
            break
        nxt: Dict = {}
        for (s, j), w in layer.items():
            for a, t in dom[s].items():
                k = j + 1 if j < m and a == obs[j] else j
                nxt[t, k] = nxt.get((t, k), Fraction(0)) + w * base
        layer = nxt
    lik = {g: (match[g] / total[g] if total[g] else Fraction(0)) for g in goals}
    z = sum(lik[g] * prior[g] for g in goals)
    return {g: (lik[g] * prior[g] / z if z else Fraction(0)) for g in goals}


def grid(w: int, h: int, walls=()):
    """Moves between cells of a grid; an action is the pair (from cell, to cell)."""
    dom = {}
    for x in range(w):
        for y in range(h):
            if (x, y) in walls:
                continue
            dom[x, y] = {}
            for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                t = (x + dx, y + dy)
                if 0 <= t[0] < w and 0 <= t[1] < h and t not in walls:
                    dom[x, y][(x, y), t] = t
    return dom
