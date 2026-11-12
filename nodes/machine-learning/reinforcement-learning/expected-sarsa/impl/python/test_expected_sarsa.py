# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expected-sarsa/. The authors are listed in prov/HAESKC.jsonl.

import random
from fractions import Fraction as F

from expected_sarsa import eps_greedy, eps_greedy_probs, expected_sarsa, expected_value, greedy

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


def q_learning(env, n, alpha, gamma, eps, rng):
    """A plain Q-learning loop with the same order of random draws."""
    Q = {}
    for _ in range(n):
        s = env.start(rng)
        while True:
            a = eps_greedy(Q, s, env.actions(s), eps, rng)
            r, s2 = env.step(s, a, rng)
            y = r if s2 is None else r + gamma * max(Q.get((s2, b), 0.0) for b in env.actions(s2))
            Q[(s, a)] = Q.get((s, a), 0.0) + alpha * (y - Q.get((s, a), 0.0))
            if s2 is None:
                break
            s = s2
    return Q


def sarsa(env, n, alpha, gamma, eps, rng):
    """A plain SARSA loop, for the step size comparison."""
    Q, rets = {}, []
    for _ in range(n):
        s = env.start(rng)
        a = eps_greedy(Q, s, env.actions(s), eps, rng)
        tot = 0
        while True:
            r, s2 = env.step(s, a, rng)
            tot += r
            if s2 is None:
                y, a2 = r, None
            else:
                a2 = eps_greedy(Q, s2, env.actions(s2), eps, rng)
                y = r + gamma * Q.get((s2, a2), 0.0)
            Q[(s, a)] = Q.get((s, a), 0.0) + alpha * (y - Q.get((s, a), 0.0))
            if s2 is None:
                break
            s, a = s2, a2
        rets.append(tot)
    return Q, rets


QN = {("n", 0): F(-3), ("n", 1): F(-1), ("n", 2): F(-10), ("n", 3): F(-2)}


def test_worked_example_targets():
    eps = F(1, 10)
    assert expected_value(QN, "n", [0, 1, 2, 3], eps) == F(-13, 10)
    p = eps_greedy_probs(QN, "n", [0, 1, 2, 3], eps)
    assert p == {0: F(1, 40), 1: F(37, 40), 2: F(1, 40), 3: F(1, 40)}
    mean = sum(p[a] * QN[("n", a)] for a in p)
    var = sum(p[a] * QN[("n", a)] ** 2 for a in p) - mean**2
    assert mean == F(-13, 10) and var == F(103, 50)  # the SARSA target varies, the expected one does not
    # one update from Q(S, A) = -2 with R = -1, gamma = 1, alpha = 1/2
    assert F(-2) + F(1, 2) * (-1 + expected_value(QN, "n", [0, 1, 2, 3], eps) - F(-2)) == F(-43, 20)


def test_total_variance_exact():
    rng = random.Random(21)
    for _ in range(200):
        acts = list(range(rng.randint(1, 4)))
        nexts = {s2: F(rng.randint(1, 4)) for s2 in range(rng.randint(1, 3))}
        tot = sum(nexts.values())
        P = {s2: w / tot for s2, w in nexts.items()}
        rew = {s2: F(rng.randint(-3, 3)) for s2 in P}
        Q = {(s2, a): F(rng.randint(-5, 5)) for s2 in P for a in acts}
        g, eps = F(rng.randint(0, 4), 4), F(rng.randint(0, 4), 4)
        # SARSA target R + g Q(S', A') with A' ~ pi(. | S'); Expected SARSA target R + g E_pi Q(S', .)
        sarsa_dist, exp_dist, cond_var = [], [], 0
        for s2, p2 in P.items():
            pi = eps_greedy_probs(Q, s2, acts, eps)
            m = expected_value(Q, s2, acts, eps)
            exp_dist.append((p2, rew[s2] + g * m))
            for a, pa in pi.items():
                sarsa_dist.append((p2 * pa, rew[s2] + g * Q[(s2, a)]))
            cond_var += p2 * sum(pa * (g * Q[(s2, a)] - g * m) ** 2 for a, pa in pi.items())
        E = lambda d: sum(p * x for p, x in d)
        V = lambda d: sum(p * x * x for p, x in d) - E(d) ** 2
        assert E(sarsa_dist) == E(exp_dist)
        assert V(sarsa_dist) == V(exp_dist) + cond_var  # law of total variance
        assert cond_var >= 0


def test_greedy_target_is_q_learning():
    for seed in range(3):
        Qe, _ = expected_sarsa(Cliff(), 200, 0.5, 1, 0.1, random.Random(seed), target_eps=0)
        Qq = q_learning(Cliff(), 200, 0.5, 1, 0.1, random.Random(seed))
        assert Qe == Qq


def test_cliff_large_step_size():
    env = Cliff()
    for seed in range(3):
        Qe, re_ = expected_sarsa(env, 500, 1.0, 1, 0.1, random.Random(seed))
        _, rs = sarsa(env, 500, 1.0, 1, 0.1, random.Random(seed))
        s, path = (3, 0), [(3, 0)]
        while True:
            _, s = env.step(s, greedy(Qe, s, [0, 1, 2, 3]), None)
            if s is None:
                break
            path.append(s)
        assert len(path) == 15 and min(r for r, _ in path) == 1  # a safe path one row above the cliff edge
        assert sum(re_[-100:]) / 100 > -25
        assert sum(rs[-100:]) / 100 < -50  # SARSA with alpha = 1 does much worse


def test_probs_sum_to_one():
    p = eps_greedy_probs({}, "s", ["a", "b", "c"], F(1, 3))
    assert sum(p.values()) == 1 and p == {"a": F(1, 9) + F(2, 3), "b": F(1, 9), "c": F(1, 9)}
