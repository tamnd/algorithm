# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/watkins-q-lambda/. The authors are listed in prov/EMENRX.jsonl.

import random
from fractions import Fraction as F

from watkins_q_lambda import eps_greedy, greedy, watkins_q_lambda

MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left


class Chain:
    """States 0, ..., n-1 in a row; both actions g and x move right; the last step ends the episode."""

    def __init__(self, n, rewards):
        self.n, self.rewards = n, rewards

    def start(self, rng):
        return 0

    def actions(self, s):
        return ["g", "x"]

    def step(self, s, a, rng):
        return self.rewards[s], (None if s == self.n - 1 else s + 1)


def script(actions):
    """A behavior that plays a fixed list of actions."""
    it = iter(actions)
    return lambda Q, s, acts, rng: next(it)


def replay(steps, Q, alpha, gamma, lam, cut):
    """Q(lambda) over a recorded episode [(s, a, r, s2, a2)], with all pairs listed; cut=False never cuts."""
    pairs = sorted({(s, a) for s, a, *_ in steps} | set(Q))
    z = {p: F(0) for p in pairs}
    for s, a, r, s2, a2 in steps:
        if s2 is None:
            delta, greedy_next = r - Q.get((s, a), 0), False
        else:
            m = max(Q.get((s2, b), 0) for b in ("g", "x"))
            greedy_next = Q.get((s2, a2), 0) == m
            delta = r + gamma * m - Q.get((s, a), 0)
        z[(s, a)] += 1
        for p in pairs:
            Q[p] = Q.get(p, 0) + alpha * delta * z[p]
            z[p] = gamma * lam * z[p] if (greedy_next or not cut) else F(0)
    return Q


def test_fixed_episode_trace_cut():
    env = Chain(4, [F(1)] * 4)
    Q0 = {(2, "g"): F(1)}  # g is greedy in state 2; every other value is 0
    acts = ["g", "g", "x", "g"]  # the third action is not greedy
    Q, rets = watkins_q_lambda(env, 1, F(1, 2), 1, F(1, 2), 0, None, Q=dict(Q0), choose=script(acts))
    assert rets == [4]
    assert {k: v for k, v in Q.items() if v != 0} == {
        (0, "g"): 1, (1, "g"): 1, (2, "g"): 1, (2, "x"): F(3, 4), (3, "g"): F(1, 2)}
    steps = [(0, "g", 1, 1, "g"), (1, "g", 1, 2, "x"), (2, "x", 1, 3, "g"), (3, "g", 1, None, None)]
    with_cut = replay(steps, dict(Q0), F(1, 2), 1, F(1, 2), cut=True)
    assert {k: v for k, v in with_cut.items() if v != 0} == {k: v for k, v in Q.items() if v != 0}
    no_cut = replay(steps, dict(Q0), F(1, 2), 1, F(1, 2), cut=False)
    assert no_cut[(0, "g")] == F(19, 16) and no_cut[(1, "g")] == F(11, 8)  # without the cut


def test_greedy_episode_propagates():
    env = Chain(5, [F(0)] * 4 + [F(1)])
    for lam, expect in ((1, [F(1, 2)] * 5), (F(1, 2), [F(1, 2) ** (5 - i) for i in range(5)])):
        Q, _ = watkins_q_lambda(env, 1, F(1, 2), 1, lam, 0, None, Q={}, choose=script(["g"] * 5))
        assert [Q.get((i, "g"), 0) for i in range(5)] == expect
    Q, _ = watkins_q_lambda(env, 1, F(1, 2), 1, 0, 0, None, Q={}, choose=script(["g"] * 5))
    assert [Q.get((i, "g"), 0) for i in range(5)] == [0, 0, 0, 0, F(1, 2)]  # lambda = 0: one step only


class Cliff:
    def start(self, rng):
        return (3, 0)

    def actions(self, s):
        return [0, 1, 2, 3]

    def step(self, s, a, rng):
        r, c = s
        dr, dc = MOVES[a]
        r2, c2 = min(max(r + dr, 0), 3), min(max(c + dc, 0), 11)
        if r2 == 3 and 1 <= c2 <= 10:
            return -100, (3, 0)
        if (r2, c2) == (3, 11):
            return -1, None
        return -1, (r2, c2)


def q_learning_choose_first(env, n, alpha, gamma, eps, rng):
    """One-step Q-learning that draws the next action before the update, as Q(lambda) does."""
    Q = {}
    for _ in range(n):
        s = env.start(rng)
        a = eps_greedy(Q, s, env.actions(s), eps, rng)
        while True:
            r, s2 = env.step(s, a, rng)
            if s2 is None:
                Q[(s, a)] = Q.get((s, a), 0) + alpha * (r - Q.get((s, a), 0))
                break
            a2 = eps_greedy(Q, s2, env.actions(s2), eps, rng)
            y = r + gamma * Q.get((s2, greedy(Q, s2, env.actions(s2))), 0)
            Q[(s, a)] = Q.get((s, a), 0) + alpha * (y - Q.get((s, a), 0))
            s, a = s2, a2
    return Q


def test_lambda_zero_is_one_step_q_learning():
    for seed in range(3):
        Qw, _ = watkins_q_lambda(Cliff(), 100, 0.5, 1, 0, 0.1, random.Random(seed))
        Qq = q_learning_choose_first(Cliff(), 100, 0.5, 1, 0.1, random.Random(seed))
        assert Qw.keys() == Qq.keys() and all(abs(Qw[k] - Qq[k]) < 1e-9 for k in Qq)


class Toy:
    def start(self, rng):
        return "a"

    def actions(self, s):
        return [0, 1]

    def step(self, s, a, rng):
        if s == "a":
            return (0, "b" if rng.random() < 0.5 else "c") if a == 0 else (1, "c")
        if s == "b":
            return (4 * (rng.random() < 0.5), None) if a == 0 else (1, None)
        return (-1, None) if a == 0 else (1 * (rng.random() < 0.5), None)


def test_learns_optimal_values_off_policy():
    QS = {("a", 0): 1.25, ("a", 1): 1.5, ("b", 0): 2, ("b", 1): 1, ("c", 0): -1, ("c", 1): 0.5}
    for lam, seed in ((0.5, 0), (0.9, 1)):
        Q, _ = watkins_q_lambda(Toy(), 100_000, lambda k: 20 / (200 + k), 1, lam, 0.5, random.Random(seed))
        assert max(abs(Q[k] - v) for k, v in QS.items()) < 0.05
