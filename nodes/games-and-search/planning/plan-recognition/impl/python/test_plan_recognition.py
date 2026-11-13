# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plan-recognition/. The authors are listed in prov/Y0RPP5.jsonl.

import random
from fractions import Fraction as F
from math import inf

from plan_recognition import (boltzmann_posterior, compatible_goals, cost_with, grid, likelihood, optimal_cost,
                              posterior)


# ---- reference: enumerate every plan up to a length ----

def embeds(obs, plan):
    it = iter(plan)
    return all(any(a == o for a in it) for o in obs)


def all_plans(dom, s0, length):
    """Every action sequence of at most the given length, with its end state."""
    out, stack = [], [(s0, ())]
    while stack:
        s, p = stack.pop()
        out.append((s, p))
        if len(p) < length:
            for a, t in dom[s].items():
                stack.append((t, p + (a,)))
    return out


def enum_costs(plans, g, obs):
    yes = min((len(p) for s, p in plans if s == g and embeds(obs, p)), default=inf)
    no = min((len(p) for s, p in plans if s == g and not embeds(obs, p)), default=inf)
    return yes, no


def enum_boltzmann(plans, goals, obs):
    lik = {}
    for g in goals:
        tot = sum((F(1, 2) ** len(p) for s, p in plans if s == g), F(0))
        hit = sum((F(1, 2) ** len(p) for s, p in plans if s == g and embeds(obs, p)), F(0))
        lik[g] = hit / tot if tot else F(0)
    z = sum(lik.values())
    return {g: lik[g] / z if z else F(0) for g in goals}


# ---- the example of the page ----

DOM = grid(3, 3)
START = (0, 1)
A, B, C = (2, 2), (2, 0), (0, 2)


def test_one_move_east():
    obs = [((0, 1), (1, 1))]
    assert [(cost_with(DOM, START, g, obs, True), cost_with(DOM, START, g, obs, False)) for g in (A, B, C)] == \
        [(3, 3), (3, 3), (3, 1)]
    assert compatible_goals(DOM, START, [A, B, C], obs) == [A, B]
    assert posterior(DOM, START, [A, B, C], obs) == {A: F(5, 12), B: F(5, 12), C: F(1, 6)}


def test_then_north():
    obs = [((0, 1), (1, 1)), ((1, 1), (1, 2))]
    assert posterior(DOM, START, [A, B, C], obs) == {A: F(5, 9), B: F(2, 9), C: F(2, 9)}
    assert compatible_goals(DOM, START, [A, B, C], obs) == [A]


def test_no_observation_gives_the_prior():
    prior = {A: F(1, 2), B: F(1, 3), C: F(1, 6)}
    assert posterior(DOM, START, [A, B, C], [], prior) == prior
    assert likelihood(2, inf) == 1 and likelihood(inf, 2) == 0 and likelihood(4, 2) == F(1, 5)


# ---- random checks against enumeration ----

def random_grid(rng):
    walls = {(rng.randrange(3), rng.randrange(3)) for _ in range(rng.randint(0, 2))}
    dom = grid(3, 3, walls)
    cells = sorted(dom)
    return dom, cells


def random_obs(rng, dom, s0, k):
    """Observations taken from a random walk, so that some plan embeds them."""
    s, walk = s0, []
    for _ in range(rng.randint(k, k + 3)):
        if not dom[s]:
            break
        a = rng.choice(sorted(dom[s]))
        walk.append(a)
        s = dom[s][a]
    idx = sorted(rng.sample(range(len(walk)), min(k, len(walk))))
    return [walk[i] for i in idx]


def test_costs_against_enumeration():
    rng = random.Random(23)
    for _ in range(40):
        dom, cells = random_grid(rng)
        s0 = rng.choice(cells)
        obs = random_obs(rng, dom, s0, rng.randint(0, 2))
        plans = all_plans(dom, s0, 9)
        for g in cells:
            yes, no = enum_costs(plans, g, obs)
            got_yes, got_no = cost_with(dom, s0, g, obs, True), cost_with(dom, s0, g, obs, False)
            if yes < inf:
                assert got_yes == yes
            else:
                assert got_yes > 9
            if no < inf:
                assert got_no == no
            else:
                assert got_no > 9
            assert optimal_cost(dom, s0, g) == min(got_yes, got_no)


def test_posterior_is_the_cost_difference_formula():
    rng = random.Random(24)
    for _ in range(30):
        dom, cells = random_grid(rng)
        s0 = rng.choice(cells)
        goals = rng.sample(cells, min(3, len(cells)))
        obs = random_obs(rng, dom, s0, rng.randint(1, 2))
        plans = all_plans(dom, s0, 10)
        lik = {}
        for g in goals:
            yes, no = enum_costs(plans, g, obs)
            if yes == inf and cost_with(dom, s0, g, obs, True) < inf:
                break
            if no == inf and cost_with(dom, s0, g, obs, False) < inf:
                break
            lik[g] = likelihood(yes, no)
        else:
            z = sum(lik.values())
            if z:
                assert posterior(dom, s0, goals, obs) == {g: lik[g] / z for g in goals}


def test_boltzmann_posterior_against_enumeration():
    rng = random.Random(25)
    for _ in range(30):
        dom, cells = random_grid(rng)
        s0 = rng.choice(cells)
        goals = rng.sample(cells, min(3, len(cells)))
        obs = random_obs(rng, dom, s0, rng.randint(0, 2))
        plans = all_plans(dom, s0, 6)
        assert boltzmann_posterior(dom, s0, goals, obs, 6) == enum_boltzmann(plans, goals, obs)


def test_boltzmann_example():
    obs = [((0, 1), (1, 1))]
    post = boltzmann_posterior(DOM, START, [A, B, C], obs, 6)
    assert post[A] == post[B] > post[C]
