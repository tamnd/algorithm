# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/q-learning/. The authors are listed in prov/CHAYP3.jsonl.

import random
from fractions import Fraction as F

from q_learning import greedy, greedy_path, q_learning, q_learning_from_log

MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left


class Cliff:
    """Cliff walking (Sutton and Barto, Example 6.6)."""

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


# A continuing MDP with 3 states and 2 actions: P[s][a] is a list of (probability, next state).
P = [
    [[(F(1, 2), 0), (F(1, 2), 1)], [(F(1), 2)]],
    [[(F(1), 0)], [(F(1, 4), 1), (F(3, 4), 2)]],
    [[(F(1, 3), 0), (F(2, 3), 2)], [(F(1), 1)]],
]
R = [[1, 0], [2, -1], [0, 3]]
GAMMA = F(1, 2)
Q_STAR = [[F(12, 5), F(23, 10)], [F(16, 5), F(9, 8)], [F(29, 15), F(23, 5)]]


class Small:
    def start(self, rng):
        return 0

    def actions(self, s):
        return [0, 1]

    def step(self, s, a, rng):
        u, acc = rng.random(), 0
        for p, s2 in P[s][a]:
            acc += p
            if u < acc:
                return R[s][a], s2
        return R[s][a], P[s][a][-1][1]


def test_q_star_solves_bellman_optimality_exactly():
    for s in range(3):
        for a in range(2):
            assert Q_STAR[s][a] == R[s][a] + GAMMA * sum(p * max(Q_STAR[s2]) for p, s2 in P[s][a])


def test_worked_example_from_log():
    log = [("x", "R", 0, "y"), ("y", "R", 2, None), ("x", "R", 0, "y"),
           ("y", "L", -1, "x"), ("x", "L", 1, None), ("y", "L", -1, "x")]
    Q = q_learning_from_log(log, lambda s: ["L", "R"], F(1, 2), F(1, 2))
    assert Q == {("x", "R"): F(1, 4), ("y", "R"): 1, ("y", "L"): F(-19, 32), ("x", "L"): F(1, 2)}


def test_one_over_n_steps_reach_q_star():
    for seed in range(2):
        Q, _ = q_learning(Small(), 1, lambda n: 1 / n, 0.5, 1.0, random.Random(seed), max_steps=100_000)
        err = max(abs(Q[(s, a)] - float(Q_STAR[s][a])) for s in range(3) for a in range(2))
        assert err < 0.03
        assert [greedy(Q, s, [0, 1]) for s in range(3)] == [0, 0, 1]


def test_cliff_greedy_path_is_optimal():
    env = Cliff()
    for seed in range(5):
        Q, _ = q_learning(env, 500, 0.5, 1, 0.1, random.Random(seed))
        path = greedy_path(env, Q, (3, 0), random.Random(0), 100)
        assert len(path) == 13  # 13 steps: up, 11 times right, down
        assert path[1:] == [(2, c) for c in range(12)]


def test_greedy_behavior_with_zero_eps_can_miss_the_optimum():
    # with eps = 0 and Q = 0, the first action is always tried first; Q-learning still learns from what it sees
    class Two:
        def start(self, rng):
            return "s"

        def actions(self, s):
            return ["a", "b"]

        def step(self, s, a, rng):
            return (1 if a == "a" else 5), None

    Q, _ = q_learning(Two(), 50, 0.5, 1, 0.0, random.Random(0))
    assert ("s", "b") not in Q and greedy(Q, "s", ["a", "b"]) == "a"
    Q, _ = q_learning(Two(), 50, 0.5, 1, 0.5, random.Random(0))
    assert greedy(Q, "s", ["a", "b"]) == "b"
