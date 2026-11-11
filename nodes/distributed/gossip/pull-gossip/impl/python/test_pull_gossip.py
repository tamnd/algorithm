# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pull-gossip/. The authors are listed in prov/1XHB8V.jsonl.

import math
import random

from pull_gossip import pull_gossip, uninformed_after_one_round


def test_small_cases_and_determinism() -> None:
    assert pull_gossip(1, random.Random(0)) == (0, 0, [1])
    rounds, tx, hist = pull_gossip(2, random.Random(0))
    assert rounds == 1 and tx == 1 and hist == [1, 2]
    assert pull_gossip(400, random.Random(5)) == pull_gossip(400, random.Random(5))


def test_history_is_monotone_and_complete() -> None:
    for seed in range(10):
        rounds, _, hist = pull_gossip(300, random.Random(seed))
        assert len(hist) == rounds + 1 and hist[-1] == 300
        assert all(hist[t] >= hist[t - 1] for t in range(1, len(hist)))
        # One informed process can answer many calls, but each caller learns at most once.
        assert all(hist[t] <= 300 for t in range(len(hist)))


def test_uninformed_fraction_squares() -> None:
    # If u processes are uninformed, each stays uninformed with probability (u - 1)/(n - 1).
    n = 1000
    for u, trials in ((500, 30), (300, 40), (100, 200)):
        mean = sum(uninformed_after_one_round(n, u, random.Random(u * 1000 + s)) for s in range(trials)) / trials
        expected = u * (u - 1) / (n - 1)
        assert abs(mean - expected) <= 0.06 * expected + 1.0, (u, mean, expected)


def test_slow_start() -> None:
    # With one informed process, nothing happens in a round with probability about 1/e.
    n = 1000
    stuck = sum(uninformed_after_one_round(n, n - 1, random.Random(s)) == n - 1 for s in range(400))
    assert abs(stuck / 400 - (1 - 1 / (n - 1)) ** (n - 1)) < 0.07


def test_rounds_close_to_log2_n_plus_log2_ln_n() -> None:
    # Karp et al.: pull needs log2 n + O(log log n) rounds; the late phase is doubly exponential.
    for n, trials in ((256, 30), (1024, 20)):
        rounds = [pull_gossip(n, random.Random(n + s))[0] for s in range(trials)]
        mean = sum(rounds) / trials
        target = math.log2(n) + math.log2(math.log(n))
        assert target - 1.0 <= mean <= target + 2.5, (n, mean, target)


def test_transmissions_are_linear_per_round() -> None:
    # Every informed process answers each call it gets, so the cost is about the sum of informed counts.
    n = 512
    for seed in range(5):
        rounds, tx, hist = pull_gossip(n, random.Random(seed))
        assert tx >= n - 1
        assert tx <= 2 * sum(hist[:-1]) + 50
        assert tx < 5 * n
