# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ben-or-consensus/. The authors are listed in prov/G8VCBD.jsonl.

import random

from ben_or_consensus import run, violations


def random_crashes(rng: random.Random, n: int, f: int) -> dict[int, int]:
    """Up to f crashes, each after a random number of sends, often mid-broadcast."""
    who = rng.sample(range(n), rng.randint(0, f))
    return {p: rng.randint(0, 3 * n) for p in who}


def test_safety_and_termination_on_many_seeds() -> None:
    rng = random.Random(1983)
    runs = 0
    for n in (3, 4, 5, 6, 7):
        f = (n - 1) // 2
        for mode in ("random", "fifo", "lifo"):
            for _ in range(60):
                inputs = [rng.randrange(2) for _ in range(n)]
                crashes = random_crashes(rng, n, f)
                res = run(inputs, f, rng.randrange(10**9), crashes, mode)
                assert violations(inputs, res) == [], (inputs, crashes, mode, res)
                runs += 1
    assert runs == 900


def test_safety_against_the_split_adversary() -> None:
    rng = random.Random(27)
    for n in (3, 4, 5):
        f = (n - 1) // 2
        for _ in range(25):
            inputs = [i % 2 for i in range(n)]
            crashes = random_crashes(rng, n, f)
            res = run(inputs, f, rng.randrange(10**9), crashes, "split")
            assert violations(inputs, res) == []


def test_unanimous_inputs_decide_in_round_1() -> None:
    rng = random.Random(5)
    for n in (3, 5, 7):
        f = (n - 1) // 2
        for v in (0, 1):
            for _ in range(20):
                res = run([v] * n, f, rng.randrange(10**9), random_crashes(rng, n, f))
                assert all(res["decided_round"][i] == 1 for i in res["correct"])
                assert set(res["decisions"].values()) == {v}


def test_lemma_b_everyone_adopts_a_decided_value() -> None:
    # If some process decides v in round r, every process that finishes
    # round r ends it with x = v.
    rng = random.Random(83)
    for _ in range(200):
        n = rng.choice([3, 4, 5, 7])
        f = (n - 1) // 2
        inputs = [rng.randrange(2) for _ in range(n)]
        res = run(inputs, f, rng.randrange(10**9), random_crashes(rng, n, f))
        for i, r in res["decided_round"].items():
            v = res["decisions"][i]
            for h in res["history"]:
                if len(h) >= r:
                    assert h[r - 1] == v


def test_crash_in_the_middle_of_a_broadcast() -> None:
    # p0 crashes after it has sent its first report to p0 and p1 only.
    n, f = 5, 2
    res = run([0, 1, 1, 0, 1], f, 11, {0: 2})
    assert res["sent"][0] == 2 and res["crashed"] == [0]
    assert violations([0, 1, 1, 0, 1], res) == []


def test_mean_rounds_small_n() -> None:
    means = {}
    for n in (3, 5):
        f = (n - 1) // 2
        rounds = [run([i % 2 for i in range(n)], f, s)["rounds"] for s in range(200)]
        means[n] = sum(rounds) / len(rounds)
    assert means == {3: 2.6, 5: 4.135}
