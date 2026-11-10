# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandra-toueg-consensus/. The authors are listed in prov/AKDA5X.jsonl.

import random

from chandra_toueg_consensus import run, violations


def crashes(rng: random.Random, n: int, f: int) -> dict[int, int]:
    who = rng.sample(range(n), rng.randint(0, f))
    return {p: rng.randint(0, 4 * n) for p in who}


def test_safety_and_termination_on_many_seeds() -> None:
    rng = random.Random(1996)
    count = 0
    for n in (3, 4, 5, 7):
        f = (n - 1) // 2
        for mode in ("random", "lifo"):
            for _ in range(50):
                inputs = [rng.randrange(3) for _ in range(n)]
                plan = crashes(rng, n, f)
                res = run(inputs, f, rng.randrange(10**9), rng.randint(0, 400), plan, mode)
                assert violations(inputs, res) == [], (inputs, plan, mode)
                count += 1
    assert count == 400


def test_the_detector_makes_mistakes_before_gst() -> None:
    rng = random.Random(7)
    total = 0
    for _ in range(30):
        res = run([0, 1, 0, 1, 1], 2, rng.randrange(10**9), 300)
        total += res["mistakes"]
        assert violations([0, 1, 0, 1, 1], res) == []
    assert total > 0


def test_no_mistakes_no_crash_decides_in_round_1() -> None:
    # GST = 0 and the trusted process is the coordinator of round 1 (p1).
    seen = 0
    for seed in range(40):
        res = run([3, 1, 2], 1, seed, 0)
        if res["trusted"] == 1:
            seen += 1
            assert res["log"]["rbcast"][0][0] == 1
            assert set(res["decisions"].values()) == {res["log"]["proposals"][0][1]}
    assert seen > 0


def test_locking_every_later_proposal_is_the_decided_value() -> None:
    rng = random.Random(43)
    for _ in range(300):
        n = rng.choice([3, 4, 5])
        f = (n - 1) // 2
        inputs = [rng.randrange(3) for _ in range(n)]
        res = run(inputs, f, rng.randrange(10**9), rng.randint(0, 300), crashes(rng, n, f))
        log = res["log"]
        if not log["rbcast"]:
            continue
        r0, v = min(log["rbcast"])
        assert all(w == v for r, w in log["proposals"] if r >= r0)
        assert all(w == v for _, w in log["rbcast"])


def test_crash_of_the_first_coordinator_in_the_middle_of_its_proposal() -> None:
    # p1 coordinates round 1. Its sends: EST to itself (1), PROP to p0 (2),
    # then it crashes before the PROP to p1 and p2.
    res = run([0, 1, 0], 1, 5, 50, {1: 2})
    assert res["crashed"] == [1] and res["sent"][1] == 2
    assert violations([0, 1, 0], res) == []
