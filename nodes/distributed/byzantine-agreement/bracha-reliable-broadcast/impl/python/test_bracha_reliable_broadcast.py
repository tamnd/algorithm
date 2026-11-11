# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bracha-reliable-broadcast/. The authors are listed in prov/9Y7P6X.jsonl.

import itertools
import random

from bracha_reliable_broadcast import STRATEGIES, check, run, silent, split

SCHEDULERS = ("fifo", "random", "adversarial")


def test_honest_sender_all_deliver() -> None:
    for n, t in ((4, 1), (7, 2)):
        for faulty in itertools.combinations(range(1, n), t):
            for name, strat in STRATEGIES.items():
                for sch in SCHEDULERS:
                    res = run(n, t, 0, "a", set(faulty), strat, sch, seed=len(faulty))
                    assert check(n, 0, "a", set(faulty), res) == [], (n, faulty, name, sch)


def test_equivocating_sender_keeps_consistency_and_totality() -> None:
    """The sender is faulty; every traitor set that contains it, every
    strategy and scheduler, and several seeds."""
    for n, t in ((4, 1), (7, 2)):
        for rest in itertools.combinations(range(1, n), t - 1):
            faulty = {0, *rest}
            for name, strat in STRATEGIES.items():
                for sch in SCHEDULERS:
                    for seed in range(4):
                        res = run(n, t, 0, "a", faulty, strat, sch, seed)
                        assert check(n, 0, "a", faulty, res) == [], (n, faulty, name, sch, seed)


def test_seeded_random_runs() -> None:
    rng = random.Random(1987)
    for _ in range(200):
        t = rng.randint(1, 3)
        n = 3 * t + 1 + rng.randint(0, 2)
        faulty = set(rng.sample(range(n), rng.randint(0, t)))
        sender = rng.randrange(n)
        strat = rng.choice(list(STRATEGIES.values()))
        res = run(n, t, sender, "a", faulty, strat, rng.choice(SCHEDULERS), rng.randrange(10**6))
        assert check(n, sender, "a", faulty, res) == []


def test_message_count() -> None:
    """Each honest process sends at most one echo and one ready to each
    process, and an honest sender sends n initial messages."""
    for n, t in ((4, 1), (10, 3)):
        res = run(n, t, 0, "a", set(), silent, "random", 3)
        assert res["messages"] == n + 2 * n * n
        res = run(n, t, 0, "a", {0}, split, "random", 3)
        assert res["messages"] <= 2 * n * (n - 1)


def test_example_trace() -> None:
    res = run(4, 1, 0, "a", {0}, split, "fifo")
    assert res["delivered"] == {1: ["a"], 2: ["a"], 3: ["a"]}
    assert res["messages"] == 24
    assert (3, "echo", "b") in res["log"] and (3, "ready", "a") in res["log"]


def test_n_equal_3t_loses_validity() -> None:
    """With n = 3t, the n - t = 2t honest echoes are not more than
    (n + t)/2 = 2t, so silent traitors block an honest sender."""
    for t in (1, 2):
        n = 3 * t
        faulty = set(range(n - t, n))
        res = run(n, t, 0, "a", faulty, silent, "random", 0)
        assert check(n, 0, "a", faulty, res) == ["validity"]
