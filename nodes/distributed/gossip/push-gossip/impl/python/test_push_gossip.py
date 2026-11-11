# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/push-gossip/. The authors are listed in prov/7Q1FNH.jsonl.

import math
import random

from push_gossip import infect_and_die, push_gossip


def test_small_cases() -> None:
    assert push_gossip(1, random.Random(0)) == (0, 0, [1])
    assert push_gossip(2, random.Random(0)) == (1, 1, [1, 2])


def test_same_seed_same_run() -> None:
    assert push_gossip(300, random.Random(5)) == push_gossip(300, random.Random(5))


def test_doubling_bound_and_message_count() -> None:
    for seed in range(30):
        n = 50 + 37 * seed
        rounds, messages, hist = push_gossip(n, random.Random(seed))
        assert hist[-1] == n and len(hist) == rounds + 1
        # The informed set at most doubles in a round, so rounds >= log2 n.
        assert all(hist[t] <= 2 * hist[t - 1] for t in range(1, len(hist)))
        assert rounds >= math.ceil(math.log2(n))
        # Every informed process pushes once per round.
        assert messages == sum(hist[:-1])


def test_rounds_match_log2_plus_ln() -> None:
    # Frieze and Grimmett 1985, Pittel 1987: log2 n + ln n + O(1).
    for n, trials in ((256, 40), (1024, 30)):
        rounds = [push_gossip(n, random.Random(n + s))[0] for s in range(trials)]
        mean = sum(rounds) / trials
        target = math.log2(n) + math.log(n)
        assert target - 0.5 <= mean <= target + 2.5, (n, mean, target)
        assert max(rounds) <= target + 6


def test_messages_are_about_n_ln_n() -> None:
    n, trials = 1024, 20
    msgs = [push_gossip(n, random.Random(77 + s))[1] for s in range(trials)]
    ratio = sum(msgs) / trials / (n * math.log(n))
    assert 1.0 <= ratio <= 1.4, ratio


def star(n: int) -> list[list[int]]:
    return [list(range(1, n))] + [[0] for _ in range(1, n)]


def test_push_is_slow_on_a_star() -> None:
    # Only the center can inform a leaf, one leaf per round.
    n = 60
    for seed in range(10):
        for source in (0, 7):
            rounds, _, _ = push_gossip(n, random.Random(seed), adj=star(n), source=source)
            assert rounds >= n - 1


def test_fanout_success_probability() -> None:
    # Kermarrec, Massoulie and Ganesh 2003: fanout ln n + c gives exp(-exp(-c)).
    n, k, trials = 1000, 8, 300
    hits = sum(infect_and_die(n, k, random.Random(s)) == n for s in range(trials))
    c = k - math.log(n)
    predicted = math.exp(-math.exp(-c))
    assert abs(hits / trials - predicted) < 0.08, (hits / trials, predicted)


def test_fanout_reaches_almost_all_when_it_takes_off() -> None:
    n = 1000
    for seed in range(40):
        reached = infect_and_die(n, 8, random.Random(seed))
        assert reached >= n - 5 or reached < 20
