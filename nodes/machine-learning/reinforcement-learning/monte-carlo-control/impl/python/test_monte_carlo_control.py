# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-control/. The authors are listed in prov/VZ2NZH.jsonl.

import random
from fractions import Fraction as F

import pytest

from monte_carlo_control import greedy, mc_es, off_policy_mc_control, on_policy_mc_control


class Toy:
    """The MDP of the page: from a, action 0 gives 0 and goes to b or c; action 1 gives 1 and goes to c.
    In b, action 0 gives 0 or 4, action 1 gives 1. In c, action 0 gives -1, action 1 gives 0 or 1."""

    states = ["a", "b", "c"]

    def actions(self, s):
        return [0, 1]

    def start(self, rng):
        return "a"

    def step(self, s, a, rng):
        if s == "a":
            if a == 1:
                return 1, "c"
            return 0, ("b" if rng.random() < 0.5 else "c")
        if s == "b":
            return (4 if rng.random() < 0.5 else 0, None) if a == 0 else (1, None)
        return (-1, None) if a == 0 else ((1 if rng.random() < 0.5 else 0), None)


Q_STAR = {("a", 0): 1.25, ("a", 1): 1.5, ("b", 0): 2, ("b", 1): 1, ("c", 0): -1, ("c", 1): 0.5}
PI_STAR = {"a": 1, "b": 0, "c": 1}


class ScriptRng:
    """A stand-in for random.Random that returns scripted values, for the worked example."""

    def __init__(self, ints, floats):
        self.ints, self.floats = list(ints), list(floats)

    def randrange(self, n):
        return self.ints.pop(0)

    def random(self):
        return self.floats.pop(0)


def test_worked_example():
    # starts (a,1), (b,0), (a,0), (a,1); the draws give b reward 4, a goes to c, c rewards 1 then 0
    rng = ScriptRng([1, 2, 0, 1], [0.3, 0.7, 0.2, 0.9])
    pi, Q, N = mc_es(Toy(), 4, 1, rng)
    assert Q == {("c", 0): -1, ("a", 1): 0.5, ("b", 0): 4, ("c", 1): 0.5, ("a", 0): 1}
    assert pi == {"a": 0, "b": 0, "c": 1}
    assert N[("a", 1)] == 2


def test_mc_es_finds_optimal_policy():
    for seed in range(3):
        pi, Q, _ = mc_es(Toy(), 20000, 1, random.Random(seed))
        assert pi == PI_STAR
        for k, v in Q_STAR.items():
            assert abs(Q[k] - v) < 0.1


def test_q_is_first_visit_sample_average():
    log = []

    class Rec(Toy):
        def step(self, s, a, rng):
            r, s2 = super().step(s, a, rng)
            log.append((s, a, r, s2))
            return r, s2

    g = F(1, 2)
    _, Q, N = mc_es(Rec(), 300, g, random.Random(5))
    eps, cur = [], []
    for s, a, r, s2 in log:
        cur.append((s, a, r))
        if s2 is None:
            eps.append(cur)
            cur = []
    sums, cnt = {}, {}
    for ep in eps:
        seen = set()
        for t, (s, a, _) in enumerate(ep):
            if (s, a) in seen:
                continue
            seen.add((s, a))
            G = sum(g**k * ep[t + k][2] for k in range(len(ep) - t))
            sums[(s, a)] = sums.get((s, a), 0) + G
            cnt[(s, a)] = cnt.get((s, a), 0) + 1
    assert cnt == N
    assert Q == {k: sums[k] / cnt[k] for k in sums}


def test_on_policy_eps_soft():
    Q, _ = on_policy_mc_control(Toy(), 60000, 1, 0.1, random.Random(3))
    assert {s: greedy(Q, s, [0, 1]) for s in "abc"} == PI_STAR
    # values of the eps-greedy policy (eps = 0.1): V(b) = 1.95, V(c) = 0.425
    assert abs(Q[("a", 1)] - 1.425) < 0.05
    assert abs(Q[("a", 0)] - 1.1875) < 0.1


def test_off_policy_weighted_is():
    pi, Q, _ = off_policy_mc_control(Toy(), 20000, 1, random.Random(4))
    assert pi == PI_STAR
    for k, v in Q_STAR.items():
        assert abs(Q[k] - v) < 0.1


def test_greedy_ties_take_first_action():
    assert greedy({}, "s", [3, 1, 2]) == 3
    assert greedy({("s", 2): 1}, "s", [3, 1, 2]) == 2


def test_episode_too_long():
    class Loop(Toy):
        def step(self, s, a, rng):
            return 0, "a"

    with pytest.raises(RuntimeError):
        mc_es(Loop(), 1, 1, random.Random(0), max_steps=50)
