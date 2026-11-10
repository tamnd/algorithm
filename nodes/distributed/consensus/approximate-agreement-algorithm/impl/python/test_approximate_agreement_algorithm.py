# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-agreement-algorithm/. The authors are listed in prov/11RC2B.jsonl.

import math
import random
from fractions import Fraction as F

from approximate_agreement_algorithm import (random_attack, rounds_needed, run, split_attack,
                                             spread, trimmed_midpoint)


def check(inputs, n, t, rounds, byz):
    hist = run(inputs, n, t, rounds, byz)
    lo, hi = min(inputs.values()), max(inputs.values())
    for before, after in zip(hist, hist[1:]):
        assert spread(after) <= spread(before) / 2  # the proved factor, exactly
        assert all(lo <= v <= hi for v in after.values())  # validity
    return hist


def test_halving_against_attacks() -> None:
    rng = random.Random(1)
    for seed in range(300):
        t = rng.randint(1, 3)
        n = 3 * t + 1 + rng.randint(0, 2)
        correct = rng.sample(range(n), n - rng.randint(0, t))
        inputs = {p: F(rng.randint(-40, 40), rng.randint(1, 4)) for p in correct}
        byz = split_attack if seed % 2 else random_attack(seed)
        check(inputs, n, t, 6, byz)


def test_reaches_epsilon_in_the_proved_rounds() -> None:
    inputs = {0: F(0), 1: F(100), 2: F(37), 3: F(64), 4: F(5)}
    n, t, eps = 7, 2, F(1, 10)
    delta = F(100)
    r = rounds_needed(delta, eps)
    assert r == math.ceil(math.log2(1000)) == 10
    hist = check(inputs, n, t, r, split_attack)
    assert spread(hist[-1]) <= eps


def test_factor_one_half_is_tight() -> None:
    # n = 4, t = 1: correct values 0, 1, 1; the Byzantine process sends low to 0 and high to the others
    hist = run({0: F(0), 1: F(1), 2: F(1)}, 4, 1, 1, split_attack)
    assert hist[1] == {0: F(1, 2), 1: F(1), 2: F(1)}
    assert spread(hist[1]) == spread(hist[0]) / 2


def test_no_byzantine_process() -> None:
    hist = check({p: F(p * p) for p in range(4)}, 4, 1, 5, None)
    assert spread(hist[-1]) <= F(9, 32)


def test_n_equal_3t_does_not_converge() -> None:
    # n = 3, t = 1: correct 0 and 1; the Byzantine process sends -10 to 0 and 10 to 1
    def attack(r, q, p, x):
        return F(-10) if p == 0 else F(10)

    hist = run({0: F(0), 1: F(1)}, 3, 1, 20, attack)
    assert all(spread(h) == 1 for h in hist)


def test_trim_keeps_the_correct_range() -> None:
    assert trimmed_midpoint([F(-99), F(2), F(4), F(99)], 1) == 3
    assert trimmed_midpoint([F(1)] * 5, 2) == 1
