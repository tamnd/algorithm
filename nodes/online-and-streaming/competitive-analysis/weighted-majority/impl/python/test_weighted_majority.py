# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-majority/. The authors are listed in prov/PJZVZH.jsonl.

import math
import random
from fractions import Fraction as F

from weighted_majority import (
    against_adversary,
    expert_mistakes,
    mistakes,
    randomized_weighted_majority,
    sample_choices,
    weighted_majority,
)

PRED = [[1, 0, 1], [0, 1, 1], [1, 1, 0], [1, 0, 1], [0, 1, 0]]
OUT = [0, 1, 0, 1, 1]


def oracle_wm(predictions, outcomes, beta):
    """Independent version: weight of expert i is beta ** (mistakes of i so far)."""
    n = len(predictions[0])
    count = [0] * n
    said = []
    for f, y in zip(predictions, outcomes):
        vote = {0: F(0), 1: F(0)}
        for i in range(n):
            vote[f[i]] += beta ** count[i]
        said.append(1 if vote[1] >= vote[0] else 0)
        for i in range(n):
            count[i] += f[i] != y
    return said


def test_example():
    said, w = weighted_majority(PRED, OUT)
    assert said == [1, 1, 1, 1, 0]
    assert mistakes(said, OUT) == 3
    assert expert_mistakes(PRED, OUT) == [4, 2, 2]
    assert w == [F(1, 16), F(1, 4), F(1, 4)]
    losses = [[F(int(f[i] != y)) for i in range(3)] for f, y in zip(PRED, OUT)]
    expected, probs = randomized_weighted_majority(losses)
    assert probs[0] == [F(1, 3)] * 3
    assert expected == F(2, 3) + F(1, 4) + F(5, 7) + F(4, 9) + F(5, 7)


def check_bound(predictions, outcomes, beta):
    said, _ = weighted_majority(predictions, outcomes, beta)
    m = mistakes(said, outcomes)
    m_star = min(expert_mistakes(predictions, outcomes))
    n = len(predictions[0])
    # beta**m* <= W_final <= n ((1 + beta)/2)**m, in exact arithmetic
    assert beta ** m_star <= n * ((1 + beta) / 2) ** m
    if beta == F(1, 2):
        assert m <= 2.41 * (m_star + math.log2(n)) + 1e-9
    return said, m, m_star


def test_random_against_oracle_and_bound():
    rng = random.Random(1989)
    for _ in range(600):
        n = rng.randrange(1, 7)
        t = rng.randrange(0, 25)
        beta = F(rng.randrange(1, 10), 10)
        pred = [[rng.randrange(2) for _ in range(n)] for _ in range(t)]
        out = [rng.randrange(2) for _ in range(t)]
        if t == 0:
            assert weighted_majority([], []) == ([], [])
            continue
        said, _, _ = check_bound(pred, out, beta)
        assert said == oracle_wm(pred, out, beta)


def test_adaptive_adversary_forces_a_mistake_each_round():
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randrange(2, 6)
        t = rng.randrange(1, 40)
        table = [[rng.randrange(2) for _ in range(n)] for _ in range(t)]
        pred, out = against_adversary(n, t, lambda r: table[r])
        _, m, m_star = check_bound(pred, out, F(1, 2))
        assert m == t
    # two opposite experts: the learner errs T times and the best expert at most T/2 times
    pred, out = against_adversary(2, 50, lambda r: [0, 1])
    assert mistakes(weighted_majority(pred, out)[0], out) == 50
    assert min(expert_mistakes(pred, out)) <= 25


def test_halving_with_a_perfect_expert():
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randrange(1, 33)
        t = rng.randrange(1, 30)
        good = rng.randrange(n)
        out = [rng.randrange(2) for _ in range(t)]
        pred = [[rng.randrange(2) for _ in range(n)] for _ in range(t)]
        for r in range(t):
            pred[r][good] = out[r]
        said, _ = weighted_majority(pred, out, F(0))
        assert mistakes(said, out) <= int(math.log2(n))


def rwm_bound(losses, beta):
    n = len(losses[0])
    best = min(sum(row[i] for row in losses) for i in range(n))
    return (math.log(n) + float(best) * math.log(1 / float(beta))) / (1 - float(beta))


def test_randomized_bound_seeded_and_adversarial():
    rng = random.Random(1994)
    for _ in range(300):
        n = rng.randrange(1, 6)
        t = rng.randrange(1, 30)
        beta = F(rng.randrange(1, 10), 10)
        losses = [[F(rng.randrange(0, 5), 4) for _ in range(n)] for _ in range(t)]
        expected, probs = randomized_weighted_majority(losses, beta)
        assert all(sum(p) == 1 for p in probs)
        assert float(expected) <= rwm_bound(losses, beta) + 1e-9
    for _ in range(300):
        # adaptive adversary: loss 1 on each expert with at least the average probability
        n = rng.randrange(2, 6)
        t = rng.randrange(1, 30)
        beta = F(rng.randrange(1, 10), 10)
        losses: list[list[F]] = []
        for _r in range(t):
            _, probs = randomized_weighted_majority(losses + [[F(0)] * n], beta)
            p = probs[-1]
            losses.append([F(1) if x * n >= 1 else F(0) for x in p])
        expected, _ = randomized_weighted_majority(losses, beta)
        assert float(expected) <= rwm_bound(losses, beta) + 1e-9


def test_sampling_matches_expectation():
    rng = random.Random(8)
    losses = [[F(int(f[i] != y)) for i in range(3)] for f, y in zip(PRED, OUT)]
    expected, probs = randomized_weighted_majority(losses)
    runs, total = 20000, 0
    for _ in range(runs):
        picks = sample_choices(probs, rng)
        total += sum(int(losses[t][i]) for t, i in enumerate(picks))
    assert abs(total / runs - float(expected)) < 0.05
