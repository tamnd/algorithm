# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contingent-planning/. The authors are listed in prov/JA1FVX.jsonl.

import random
from collections import deque
from math import inf

from contingent_planning import contingent_plan, depth, is_valid, successors


# ---- references ----

def solvable(b, k, goal, actions, succ, obs):
    """Is there a plan of depth at most k from b? Plain depth-limited AND-OR recursion."""
    if all(goal(s) for s in b):
        return True
    if k == 0:
        return False
    for a in actions:
        br = successors(b, a, succ, obs)
        if br is not None and all(solvable(c, k - 1, goal, actions, succ, obs) for c in br.values()):
            return True
    return False


def least_depth(init, goal, actions, succ, obs, limit):
    b = frozenset(init)
    for k in range(limit + 1):
        if solvable(b, k, goal, actions, succ, obs):
            return k
    return inf


def conformant_length(init, goal, actions, succ):
    b0 = frozenset(init)
    dist = {b0: 0}
    q = deque([b0])
    while q:
        b = q.popleft()
        if all(goal(s) for s in b):
            return dist[b]
        for a in actions:
            nxt = [succ(s, a) for s in b]
            if all(nxt):
                nb = frozenset(t for n in nxt for t in n)
                if nb not in dist:
                    dist[nb] = dist[b] + 1
                    q.append(nb)
    return inf


# ---- examples of the page ----

def coin():
    succ = lambda s, a: {s} if a == "look" else {"T" if s == "H" else "H"}
    obs = lambda t, a: t if a == "look" else "nothing"
    return ["H", "T"], (lambda s: s == "H"), ["look", "turn"], succ, obs


def key_in_boxes():
    # state: (box with the key, held); take(i) takes the key if it is in box i; the hand feels the key
    init = [(i, False) for i in (1, 2, 3)]
    succ = lambda s, a: {(s[0], s[1] or s[0] == a)}
    obs = lambda t, a: "key" if t[1] else "empty"
    return init, (lambda s: s[1]), [1, 2, 3], succ, obs


def test_coin_needs_sensing():
    init, goal, actions, succ, obs = coin()
    plan, d, n = contingent_plan(init, goal, actions, succ, obs)
    assert plan == ("look", {"H": "done", "T": ("turn", {"nothing": "done"})})
    assert d == 2 and n == 2
    assert is_valid(plan, init, goal, succ, obs)
    assert conformant_length(init, goal, actions, succ) == inf


def test_key_in_boxes():
    init, goal, actions, succ, obs = key_in_boxes()
    plan, d, _ = contingent_plan(init, goal, actions, succ, obs)
    assert d == 3 and depth(plan) == 3
    assert plan == (1, {"key": "done", "empty": (2, {"key": "done", "empty": (3, {"key": "done"})})})
    assert is_valid(plan, init, goal, succ, obs)
    assert conformant_length(init, goal, actions, succ) == 3


def test_no_plan_when_a_trap_cannot_be_told_apart():
    # door 1 or 2 hides a trap; opening a door with the trap is not allowed; no sensor
    succ = lambda s, a: set() if a == s else {"out"}
    obs = lambda t, a: "nothing"
    plan, d, _ = contingent_plan([1, 2], lambda s: s == "out", [1, 2], succ, obs)
    assert plan is None and d == inf
    # with a sensor, look first
    succ2 = lambda s, a: {s} if a == "look" else (set() if a == s else {"out"})
    obs2 = lambda t, a: t if a == "look" else "nothing"
    plan, d, _ = contingent_plan([1, 2], lambda s: s == "out", ["look", 1, 2], succ2, obs2)
    assert d == 2 and plan == ("look", {1: (2, {"nothing": "done"}), 2: (1, {"nothing": "done"})})


def random_problem(rng, n, k, m):
    states = list(range(n))
    table = {}
    for s in states:
        for a in range(k):
            if rng.random() < 0.15:
                table[s, a] = set()
            else:
                table[s, a] = {t for t in states if rng.random() < 0.35} or {rng.choice(states)}
    sense = {(t, a): rng.randrange(m) for t in states for a in range(k)}
    init = [s for s in states if rng.random() < 0.6] or [0]
    goals = {s for s in states if rng.random() < 0.3} or {n - 1}
    return init, (lambda s: s in goals), list(range(k)), (lambda s, a: table[s, a]), (lambda t, a: sense[t, a])


def test_against_depth_limited_search():
    rng = random.Random(14)
    solved = 0
    for _ in range(200):
        n = rng.randint(1, 4)
        init, goal, actions, succ, obs = random_problem(rng, n, rng.randint(1, 3), rng.randint(1, 3))
        plan, d, nb = contingent_plan(init, goal, actions, succ, obs)
        exact = least_depth(init, goal, actions, succ, obs, min(nb, 6))
        if d <= 6:
            assert d == exact
        else:
            assert exact == inf
        if plan is not None:
            solved += 1
            assert depth(plan) == d
            assert is_valid(plan, init, goal, succ, obs)
    assert solved > 50


def test_one_observation_is_conformant_planning():
    rng = random.Random(15)
    for _ in range(100):
        init, goal, actions, succ, _ = random_problem(rng, rng.randint(1, 4), rng.randint(1, 3), 1)
        _, d, _ = contingent_plan(init, goal, actions, succ, lambda t, a: 0)
        assert d == conformant_length(init, goal, actions, succ)


def test_sensing_never_hurts():
    rng = random.Random(16)
    for _ in range(100):
        init, goal, actions, succ, obs = random_problem(rng, rng.randint(1, 4), 2, 2)
        _, d, _ = contingent_plan(init, goal, actions, succ, obs)
        assert d <= conformant_length(init, goal, actions, succ)
