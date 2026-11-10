# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiplicative-weights-update/. The authors are listed in prov/F0X9Y9.jsonl.

import math
import random
from fractions import Fraction as F

from multiplicative_weights_update import hedge, multiplicative_weights_update, solve_zero_sum, tuned_eta


def ahk_bound(costs, eta, i):
    s = sum(row[i] for row in costs)
    a = sum(abs(row[i]) for row in costs)
    return float(s + eta * a) + math.log(len(costs[0])) / float(eta)


def test_example():
    costs = [[F(1), F(0)], [F(0), F(1)], [F(1), F(0)]]
    total, probs = multiplicative_weights_update(costs, F(1, 2))
    assert probs == [[F(1, 2), F(1, 2)], [F(1, 3), F(2, 3)], [F(1, 2), F(1, 2)]]
    assert total == F(5, 3)
    assert total <= ahk_bound(costs, F(1, 2), 1)


def test_mwu_against_product_formula_and_bound():
    rng = random.Random(2012)
    for _ in range(600):
        n = rng.randrange(1, 6)
        t = rng.randrange(1, 25)
        eta = F(rng.randrange(1, 11), 20)
        costs = [[F(rng.randrange(-4, 5), 4) for _ in range(n)] for _ in range(t)]
        total, probs = multiplicative_weights_update(costs, eta)
        # oracle: w_i(t) is the product of (1 - eta m_i(s)) over s < t
        want = F(0)
        for r in range(t):
            w = [math.prod((1 - eta * costs[s][i] for s in range(r)), start=F(1)) for i in range(n)]
            p = [x / sum(w) for x in w]
            assert p == probs[r]
            want += sum(pi * mi for pi, mi in zip(p, costs[r]))
        assert total == want
        for i in range(n):
            assert float(total) <= ahk_bound(costs, eta, i) + 1e-9


def test_mwu_adaptive_costs():
    rng = random.Random(5)
    for _ in range(100):
        n = rng.randrange(2, 6)
        t = rng.randrange(1, 30)
        eta = F(rng.randrange(1, 11), 20)
        costs: list[list[F]] = []
        for _r in range(t):
            _, probs = multiplicative_weights_update(costs + [[F(0)] * n], eta)
            p = probs[-1]
            costs.append([F(1) if x * n >= 1 else F(-1, 2) for x in p])
        total, _ = multiplicative_weights_update(costs, eta)
        for i in range(n):
            assert float(total) <= ahk_bound(costs, eta, i) + 1e-9


def hedge_oracle(losses, eta):
    n = len(losses[0])
    total = 0.0
    for r, row in enumerate(losses):
        cum = [sum(losses[s][i] for s in range(r)) for i in range(n)]
        z = [math.exp(-eta * c) for c in cum]
        total += sum(zi * li for zi, li in zip(z, row)) / sum(z)
    return total


def regret(losses, total):
    n = len(losses[0])
    return total - min(sum(row[i] for row in losses) for i in range(n))


def test_hedge_seeded_rational_losses():
    rng = random.Random(1997)
    for _ in range(600):
        n = rng.randrange(1, 7)
        t = rng.randrange(1, 40)
        losses = [[float(F(rng.randrange(0, 9), 8)) for _ in range(n)] for _ in range(t)]
        eta = rng.choice([0.1, 0.5, 1.0, 2.0])
        total, _ = hedge(losses, eta)
        assert abs(total - hedge_oracle(losses, eta)) < 1e-9
        assert regret(losses, total) <= math.log(n) / eta + eta * t / 8 + 1e-9
        if n >= 2:
            eta = tuned_eta(n, t)
            total, _ = hedge(losses, eta)
            assert regret(losses, total) <= math.sqrt(t * math.log(n) / 2) + 1e-9


def test_hedge_adversarial_losses():
    rng = random.Random(6)
    for _ in range(200):
        n = rng.randrange(2, 8)
        t = rng.randrange(1, 60)
        eta = tuned_eta(n, t)
        losses: list[list[float]] = []
        for _r in range(t):
            _, probs = hedge(losses + [[0.0] * n], eta)
            p = probs[-1]
            top = max(range(n), key=lambda i: p[i])
            losses.append([1.0 if i == top else 0.0 for i in range(n)])
        total, _ = hedge(losses, eta)
        assert regret(losses, total) <= math.sqrt(t * math.log(n) / 2) + 1e-9
    # all losses 1/2 except a perfect expert: Hedge's loss is bounded by ln n / eta + eta T / 8
    n, t = 16, 400
    losses = [[0.0] + [0.5] * (n - 1) for _ in range(t)]
    total, probs = hedge(losses, tuned_eta(n, t))
    assert probs[-1][0] > 0.99
    assert regret(losses, total) <= math.sqrt(t * math.log(n) / 2)


def test_zero_sum_game():
    rps = [[0.5, 0.0, 1.0], [1.0, 0.5, 0.0], [0.0, 1.0, 0.5]]
    rounds = 4000
    row, col, avg = solve_zero_sum(rps, rounds)
    gap = math.sqrt(math.log(3) / (2 * rounds))
    assert 0.5 - gap - 1e-9 <= avg <= 0.5 + 1e-9
    guarantee = min(sum(row[i] * rps[i][j] for i in range(3)) for j in range(3))
    assert guarantee >= 0.5 - gap - 1e-9
    assert abs(sum(col) - 1) < 1e-9
