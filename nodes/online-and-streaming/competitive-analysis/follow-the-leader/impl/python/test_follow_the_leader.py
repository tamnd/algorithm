# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/follow-the-leader/. The authors are listed in prov/DKX8AG.jsonl.

import math
import random
from fractions import Fraction as F

from follow_the_leader import (
    alternating_losses,
    best_fixed,
    follow_the_leader,
    follow_the_perturbed_leader,
    ftl_squared_loss,
)


def oracle_ftl(losses):
    n = len(losses[0])
    picks = []
    for t in range(len(losses)):
        sums = [sum((losses[s][i] for s in range(t)), F(0)) for i in range(n)]
        picks.append(min(range(n), key=lambda i: (sums[i], i)))
    return picks


def test_alternating_sequence_gives_linear_regret():
    for t in (1, 2, 3, 10, 101, 400):
        losses = alternating_losses(t)
        picks, paid = follow_the_leader(losses)
        assert paid == t - F(1, 2)
        assert picks == [0] + [1 if r % 2 == 1 else 0 for r in range(1, t)]
        best = best_fixed(losses)
        assert best == min(F(1, 2) + (t - 1) // 2, F(t // 2))
        assert paid - best >= F(t, 2) - 1


def test_example_table():
    picks, paid = follow_the_leader(alternating_losses(4))
    assert picks == [0, 1, 0, 1]
    assert paid == F(7, 2)
    assert best_fixed(alternating_losses(4)) == F(3, 2)


def test_random_against_oracle_and_be_the_leader():
    rng = random.Random(2005)
    for _ in range(600):
        n = rng.randrange(1, 6)
        t = rng.randrange(1, 30)
        losses = [[F(rng.randrange(0, 5), 4) for _ in range(n)] for _ in range(t)]
        picks, paid = follow_the_leader(losses)
        assert picks == oracle_ftl(losses)
        assert paid == sum(losses[r][picks[r]] for r in range(t))
        # be the leader: playing the leader after the round beats the best fixed expert
        nxt = oracle_ftl(losses + [[F(0)] * n])[1:]
        btl = sum(losses[r][nxt[r]] for r in range(t))
        assert btl <= best_fixed(losses)
        # so the regret is at most the sum of the one-step changes
        assert paid - best_fixed(losses) <= sum(losses[r][picks[r]] - losses[r][nxt[r]] for r in range(t))


def test_ftl_is_fine_for_squared_loss():
    rng = random.Random(9)
    for _ in range(600):
        t = rng.randrange(1, 60)
        zs = [F(rng.randrange(0, 11), 10) for _ in range(t)]
        xs, reg = ftl_squared_loss(zs)
        assert xs[0] == F(1, 2)
        assert all(0 <= x <= 1 for x in xs)
        assert 0 <= reg <= 2 * (1 + math.log(t))


def test_ftpl_fixes_the_alternating_sequence():
    rng = random.Random(1)
    n, t = 2, 200
    eps = math.sqrt(2 / (n * t))
    losses = [[float(x) for x in row] for row in alternating_losses(t)]
    best = float(best_fixed(alternating_losses(t)))
    runs = 200
    avg = sum(follow_the_perturbed_leader(losses, eps, rng)[1] - best for _ in range(runs)) / runs
    assert avg <= 2 * math.sqrt(2 * n * t)
    assert avg < t / 4


def test_ftpl_bound_on_seeded_losses():
    rng = random.Random(77)
    for _ in range(40):
        n = rng.randrange(2, 5)
        t = rng.randrange(20, 80)
        losses = [[rng.randrange(0, 5) / 4 for _ in range(n)] for _ in range(t)]
        best = min(sum(row[i] for row in losses) for i in range(n))
        eps = math.sqrt(2 / (n * t))
        runs = 100
        avg = sum(follow_the_perturbed_leader(losses, eps, rng)[1] - best for _ in range(runs)) / runs
        assert avg <= 2 * math.sqrt(2 * n * t)
