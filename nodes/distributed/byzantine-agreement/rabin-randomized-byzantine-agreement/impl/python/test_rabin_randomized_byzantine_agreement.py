# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-randomized-byzantine-agreement/. The authors are listed in prov/93SCFK.jsonl.

import random

from rabin_randomized_byzantine_agreement import Dealer, check, mean_rounds, run, thresholds

STRATEGIES = ("silent", "random", "wrong", "straddle")


def test_thresholds():
    assert thresholds(17, 2) == (11, 13, 15)
    for t in range(1, 6):
        n = 8 * t + 1
        low, high, good = thresholds(n, t)
        assert good <= n - t  # a unanimous round decides
        assert 2 * low > n + t  # two processes never pass with different values


def test_validity_decides_in_round_one():
    n, t = 17, 2
    for b in (0, 1):
        for strat in STRATEGIES:
            res = run(n, t, {0, 5}, strat, [b] * n, seed=3)
            honest = [i for i in range(n) if i not in (0, 5)]
            assert check(res, honest, [b] * n) == []
            assert set(res["decisions"].values()) == {b}
            assert max(res["when"].values()) == 1 and res["rounds"] == 1


def test_agreement_and_termination_seeded():
    for n, t in ((9, 1), (17, 2), (25, 3)):
        for strat in STRATEGIES:
            for seed in range(40):
                rng = random.Random(seed)
                faulty = set(rng.sample(range(n), t))
                inputs = [rng.randrange(2) for _ in range(n)]
                res = run(n, t, faulty, strat, inputs, seed=seed)
                assert check(res, [i for i in range(n) if i not in faulty], inputs) == []


def test_constant_expected_rounds_measured():
    # The coin defeats the straddle attack with probability at least 1/2 per
    # round, so the expected last decision round is at most 3.
    n, t = 17, 2
    inputs = [1] * 10 + [0] * 7  # honest count of 1 is L - 1: the attack starts at once
    rounds = []
    for seed in range(300):
        res = run(n, t, {15, 16}, "straddle", inputs, seed=seed)
        assert check(res, list(range(15)), inputs) == []
        rounds.append(max(res["when"].values()))
    mean = sum(rounds) / len(rounds)
    assert 2 <= mean <= 3.2, mean
    for strat in STRATEGIES:
        assert mean_rounds(25, 3, strat, 100) <= 3.2


def test_without_the_coin_the_adversary_blocks():
    inputs = [1] * 10 + [0] * 7
    res = run(17, 2, {15, 16}, "straddle", inputs, coin=False, max_rounds=60)
    assert res["rounds"] is None and res["decisions"] == {}


def test_fails_below_the_bound():
    # n = 8t: even unanimous honest processes with t silent ones never reach G.
    n, t = 16, 2
    res = run(n, t, {14, 15}, "silent", [1] * n, max_rounds=30)
    assert res["rounds"] is None


def test_forged_coin_shares_are_ignored():
    d = Dealer(4, 1, seed=5)
    real = [d.share(1, i) for i in (0, 1)]
    coin = real[0][3]
    forged = [("share", 1, 2, 1 - coin), ("share", 1, 3, 1 - coin)]
    assert d.reconstruct(1, forged) is None
    assert d.reconstruct(1, forged + real) == coin
    assert d.reconstruct(1, real[:1] + forged) is None  # t + 1 valid shares are needed
