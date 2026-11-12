# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-q-learning/. The authors are listed in prov/K9FDTT.jsonl.

import itertools
import random
from fractions import Fraction as F

from double_q_learning import argmax, double_q_learning, double_target


class MaxBias:
    """Sutton and Barto, Example 6.7 and Figure 6.5: A has left (to B) and right (to the end), B has nb actions."""

    def __init__(self, nb=10):
        self.nb = nb

    def start(self, rng):
        return "A"

    def actions(self, s):
        return [0, 1] if s == "A" else list(range(self.nb))

    def step(self, s, a, rng):
        if s == "A":
            return (0.0, "B") if a == 0 else (0.0, None)
        return rng.gauss(-0.1, 1.0), None


def q_learning(env, n, alpha, eps, rng):
    """Plain Q-learning with gamma = 1 and random tie-breaking, the same draws for the behavior."""
    Q, firsts = {}, []
    for _ in range(n):
        s, k = env.start(rng), 0
        while True:
            acts = env.actions(s)
            if rng.random() < eps:
                a = acts[rng.randrange(len(acts))]
            else:
                a = acts[argmax([Q.get((s, b), 0.0) for b in acts], rng)]
            if k == 0:
                firsts.append(a)
            k += 1
            r, s2 = env.step(s, a, rng)
            y = r if s2 is None else r + max(Q.get((s2, b), 0.0) for b in env.actions(s2))
            Q[(s, a)] = Q.get((s, a), 0.0) + alpha * (y - Q.get((s, a), 0.0))
            if s2 is None:
                break
            s = s2
    return Q, firsts


def test_one_update_targets():
    QA = {("t", 0): F(1), ("t", 1): F(3)}
    QB = {("t", 0): F(2), ("t", 1): F(0)}
    rng = random.Random(0)
    assert double_target(QA, QB, F(0), "t", [0, 1], 1, rng) == 0  # QA picks 1, QB says 0
    assert double_target(QB, QA, F(0), "t", [0, 1], 1, rng) == 1  # QB picks 0, QA says 1
    assert max(QA.values()) == 3  # the Q-learning target on QA
    assert double_target(QA, QB, F(-5), None, None, 1, rng) == -5


def exact_estimators(mu, noise):
    """Exact E[max_i X_i] and E[Y_{argmax X}] for X_i, Y_i = mu_i + an independent uniform draw from noise."""
    m = len(mu)
    outcomes = list(itertools.product(noise, repeat=m))
    p = F(1, len(outcomes))
    single = double = F(0)
    for dx in outcomes:
        x = [mu[i] + dx[i] for i in range(m)]
        best = [i for i in range(m) if x[i] == max(x)]
        single += p * max(x)
        # Y is independent of X with E[Y_i] = mu_i; a tie is broken uniformly
        double += p * sum(mu[i] for i in best) / len(best)
    return single, double


def test_exact_bias_discrete():
    noise = [F(-1), F(1)]
    assert exact_estimators([F(0), F(0)], noise) == (F(1, 2), F(0))
    assert exact_estimators([F(0), F(0), F(0)], noise) == (F(3, 4), F(0))
    for m in range(1, 6):  # E[max] = 1 - 2^(1 - m) for m equal means
        assert exact_estimators([F(0)] * m, noise)[0] == 1 - F(2) ** (1 - m)
    rng = random.Random(3)
    for _ in range(100):
        mu = [F(rng.randint(-4, 4), 2) for _ in range(rng.randint(1, 4))]
        noise = [F(rng.randint(-3, 3)) for _ in range(2)]
        noise = [x - sum(noise) / 2 for x in noise]  # mean 0
        single, double = exact_estimators(mu, noise)
        assert single >= max(mu) >= double  # E[max] >= max E >= the double estimate
    # a case where the double estimator is strictly below the true max
    assert exact_estimators([F(0), F(1, 2)], [F(-1), F(1)]) == (F(7, 8), F(3, 8))


def left_rates(runs, k):
    return [sum(1 for r in runs if r[i] == 0) / len(runs) for i in range(k)]


def test_maximization_bias_figure_6_5():
    env, seeds, k = MaxBias(10), 1000, 100
    rq = left_rates([q_learning(env, k, 0.1, 0.1, random.Random(s))[1] for s in range(seeds)], k)
    rd = left_rates([double_q_learning(env, k, 0.1, 1, 0.1, random.Random(s))[2] for s in range(seeds)], k)
    assert sum(rq) / k > 0.7 and sum(rd) / k < 0.25  # mean left rate over the first 100 episodes
    assert min(rq[9:30]) > 0.85 and max(rd[9:30]) < 0.5  # episodes 10 to 30
    assert rd[99] < 0.15  # near the optimal eps / 2 = 0.05


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


def test_converges_on_small_mdp():
    QS = {("a", 0): 1.25, ("a", 1): 1.5, ("b", 0): 2, ("b", 1): 1, ("c", 0): -1, ("c", 1): 0.5}
    for seed in range(3):
        QA, QB, _ = double_q_learning(Toy(), 100_000, lambda k: 1 / k, 1, 0.5, random.Random(seed))
        for key, v in QS.items():
            assert abs(QA[key] - v) < 0.15 and abs(QB[key] - v) < 0.15  # B's reward 0 or 4 has variance 4
