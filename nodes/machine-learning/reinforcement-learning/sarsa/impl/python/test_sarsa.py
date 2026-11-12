# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sarsa/. The authors are listed in prov/568W6N.jsonl.

import random
from fractions import Fraction as F

from sarsa import eps_greedy, greedy, greedy_path, sarsa

MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left


class Cliff:
    """Cliff walking (Sutton and Barto, Example 6.6): 4 x 12 grid, start (3, 0), goal (3, 11).
    Each step gives -1; stepping into row 3, columns 1 to 10, gives -100 and returns to the start."""

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


def q_learning(env, n, alpha, gamma, eps, rng):
    """A plain Q-learning loop, for the comparison of the cliff test."""
    Q, rets = {}, []
    for _ in range(n):
        s, tot = env.start(rng), 0
        while True:
            a = eps_greedy(Q, s, env.actions(s), eps, rng)
            r, s2 = env.step(s, a, rng)
            tot += r
            t = r if s2 is None else r + gamma * max(Q.get((s2, b), 0.0) for b in env.actions(s2))
            Q[(s, a)] = Q.get((s, a), 0.0) + alpha * (t - Q.get((s, a), 0.0))
            if s2 is None:
                break
            s = s2
        rets.append(tot)
    return Q, rets


class NoExplore:
    def random(self):
        return 0.5


def test_worked_example_first_updates():
    Q, _ = sarsa(Cliff(), 1, F(1, 2), 1, F(1, 10), NoExplore(), max_steps=5)
    assert Q == {((3, 0), 0): F(-1, 2), ((2, 0), 0): F(-1, 2), ((1, 0), 0): F(-1, 2), ((0, 0), 0): F(-3, 4)}


def test_cliff_sarsa_safe_q_learning_optimal():
    env = Cliff()
    Qs, rs = sarsa(env, 500, 0.5, 1, 0.1, random.Random(0))
    Qq, rq = q_learning(env, 500, 0.5, 1, 0.1, random.Random(0))
    ps = greedy_path(env, Qs, (3, 0), random.Random(0), 100)
    pq = greedy_path(env, Qq, (3, 0), random.Random(0), 100)
    assert len(ps) == 17 and min(r for r, _ in ps) == 0  # the safe path along the top row
    assert len(pq) == 13 and min(r for r, _ in pq) == 2  # the optimal path along the edge of the cliff
    assert sum(rs[-100:]) / 100 > sum(rq[-100:]) / 100 + 10  # SARSA earns more while it explores


def test_cliff_online_return_over_seeds():
    env = Cliff()
    for seed in range(1, 5):
        _, rs = sarsa(env, 500, 0.5, 1, 0.1, random.Random(seed))
        _, rq = q_learning(env, 500, 0.5, 1, 0.1, random.Random(seed))
        assert sum(rs[-100:]) > sum(rq[-100:])


class Toy:
    """Episodic MDP with a random start: q*(a,0) = 5/4, q*(a,1) = 3/2, q*(b,0) = 2, q*(b,1) = 1,
    q*(c,0) = -1, q*(c,1) = 1/2."""

    def start(self, rng):
        return "abc"[rng.randrange(3)]

    def actions(self, s):
        return [0, 1]

    def step(self, s, a, rng):
        if s == "a":
            return (1, "c") if a == 1 else (0, "b" if rng.random() < 0.5 else "c")
        if s == "b":
            return (4 if rng.random() < 0.5 else 0, None) if a == 0 else (1, None)
        return (-1, None) if a == 0 else (1 if rng.random() < 0.5 else 0, None)


Q_STAR = {("a", 0): 1.25, ("a", 1): 1.5, ("b", 0): 2, ("b", 1): 1, ("c", 0): -1, ("c", 1): 0.5}


def test_glie_converges_to_q_star():
    for seed in range(3):
        Q, _ = sarsa(Toy(), 30000, lambda n: 1 / n, 1, lambda k: k**-0.5, random.Random(seed))
        assert {s: greedy(Q, s, [0, 1]) for s in "abc"} == {"a": 1, "b": 0, "c": 1}
        for key in [("a", 1), ("b", 0), ("c", 1)]:  # the greedy pairs, visited most often
            assert abs(Q[key] - Q_STAR[key]) < 0.1
        for key, v in Q_STAR.items():  # the other pairs are tried less and less often
            assert abs(Q[key] - v) < 0.4


def test_fixed_eps_learns_eps_greedy_values():
    # with eps = 0.2 fixed, SARSA estimates the values of the eps-greedy policy, not q*:
    # V(c) = 0.9 * 0.5 + 0.1 * (-1) = 0.35, so q(a, 1) = 1.35 < q*(a, 1) = 1.5
    Q, _ = sarsa(Toy(), 30000, lambda n: 1 / n**0.7, 1, 0.2, random.Random(7))
    assert abs(Q[("a", 1)] - 1.35) < 0.05


def test_terminal_target_is_reward():
    class One:
        def start(self, rng):
            return "s"

        def actions(self, s):
            return ["x"]

        def step(self, s, a, rng):
            return 3, None

    Q, rets = sarsa(One(), 2, F(1, 2), 1, 0, random.Random(0))
    assert Q == {("s", "x"): F(9, 4)} and rets == [3, 3]
