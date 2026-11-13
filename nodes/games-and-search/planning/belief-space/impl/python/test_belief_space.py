# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belief-space/. The authors are listed in prov/N0RMN6.jsonl.

import random
from fractions import Fraction as F
from itertools import product

import pytest

from belief_space import (
    as_vector,
    obs_prob,
    progress,
    reachable_set_beliefs,
    support,
    track,
    update,
    update_set,
)

# ---- the corridor of the page: cells 1..4, doors at 1 and 3 ----

CELLS = [1, 2, 3, 4]
DOORS = {1, 3}


def move(s, a):
    if a == "right":
        return {min(s + 1, 4): F(1)}
    return {max(s - 1, 1): F(1)}


def sensor(o, s):
    hit = (o == "door") == (s in DOORS)
    return F(4, 5) if hit else F(1, 5)


def succ(s, a):
    return set(move(s, a))


def exact_sensor(s):
    return {"door"} if s in DOORS else {"wall"}


# ---- reference: Bayes rule over whole state paths ----

def path_posterior(b0, steps, P, O, states):
    """Pr(final state | observations) by summing the joint weight of every state path."""
    post = {s: F(0) for s in states}
    moves = sum(1 for a, _ in steps if a is not None)
    for path in product(states, repeat=moves + 1):
        w = F(b0.get(path[0], 0))
        if w == 0:
            continue
        cur = path[0]
        k = 0
        for (a, o) in steps:
            if a is None:
                w *= O(o, cur)
            else:
                k += 1
                nxt = path[k]
                w *= P(cur, a).get(nxt, 0) * O(o, nxt)
                cur = nxt
            if w == 0:
                break
        if w:
            post[cur] += w
    z = sum(post.values())
    return {s: p / z for s, p in post.items() if p}


def test_page_example():
    b0 = {s: F(1, 4) for s in CELLS}
    bs = track(b0, [(None, "door"), ("right", "wall")], move, sensor)
    assert as_vector(bs[1], CELLS) == (F(2, 5), F(1, 10), F(2, 5), F(1, 10))
    assert as_vector(bs[2], CELLS) == (0, F(16, 37), F(1, 37), F(20, 37))
    assert obs_prob(bs[1], "right", "wall", move, sensor) == F(37, 50)
    # the set belief with an exact sensor
    b = frozenset(s for s in CELLS if "door" in exact_sensor(s))
    assert b == {1, 3}
    assert progress(b, "right", succ) == {2, 4}
    assert update_set(b, "right", "wall", succ, exact_sensor) == {2, 4}
    assert update_set(frozenset(CELLS), "left", "door", succ, exact_sensor) == {1, 3}


def test_moving_left_localizes_without_sensing():
    b = frozenset(CELLS)
    sizes = []
    for _ in range(3):
        b = progress(b, "left", succ)
        sizes.append(len(b))
    assert sizes == [3, 2, 1] and b == {1}


def random_pomdp(rng, n, k, m):
    states = list(range(n))
    acts = list(range(k))
    obs = list(range(m))
    T = {}
    for s in states:
        for a in acts:
            w = [rng.randint(0, 3) for _ in states]
            w[rng.randrange(n)] += 1
            T[s, a] = {t: F(x, sum(w)) for t, x in zip(states, w) if x}
    Z = {}
    for s in states:
        w = [rng.randint(0, 3) for _ in obs]
        w[rng.randrange(m)] += 1
        for o, x in zip(obs, w):
            Z[o, s] = F(x, sum(w))
    return states, acts, obs, (lambda s, a: T[s, a]), (lambda o, s: Z[o, s])


def test_updates_match_bayes_over_paths():
    rng = random.Random(5)
    for _ in range(60):
        states, acts, obs, P, O = random_pomdp(rng, rng.randint(2, 3), 2, rng.randint(2, 3))
        w = [rng.randint(0, 3) for _ in states]
        w[0] += 1
        b0 = {s: F(x, sum(w)) for s, x in zip(states, w) if x}
        steps, b = [], b0
        for _ in range(rng.randint(1, 4)):
            a = rng.choice(acts)
            # draw an observation that has positive probability
            o = next(o for o in rng.sample(obs, len(obs)) if obs_prob(b, a, o, P, O) > 0)
            steps.append((a, o))
            b = update(b, a, o, P, O)
        assert b == path_posterior(b0, steps, P, O, states)
        assert sum(b.values()) == 1


def test_support_follows_the_set_update():
    rng = random.Random(6)
    for _ in range(60):
        states, acts, obs, P, O = random_pomdp(rng, rng.randint(2, 4), 2, 2)
        nsucc = lambda s, a: {t for t, p in P(s, a).items() if p > 0}
        nobs = lambda s: {o for o in obs if O(o, s) > 0}
        b = {s: F(1, len(states)) for s in states}
        for _ in range(4):
            a = rng.choice(acts)
            good = [o for o in obs if obs_prob(b, a, o, P, O) > 0]
            o = rng.choice(good)
            nb = update(b, a, o, P, O)
            assert support(nb) == update_set(support(b), a, o, nsucc, nobs)
            b = nb


def test_number_of_set_beliefs():
    rng = random.Random(7)
    for _ in range(40):
        n = rng.randint(1, 5)
        states, acts, obs, P, O = random_pomdp(rng, n, 2, 2)
        nsucc = lambda s, a: {t for t, p in P(s, a).items() if p > 0}
        nobs = lambda s: {o for o in obs if O(o, s) > 0}
        found = reachable_set_beliefs(frozenset(states), acts, nsucc, nobs, obs)
        assert all(b and b <= set(states) for b in found)
        assert len(found) <= 2 ** n - 1


def test_zero_probability_observation():
    b = {1: F(1)}
    with pytest.raises(ValueError):
        update(b, "right", "door", move, lambda o, s: F(int(o == "wall")))
