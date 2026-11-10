# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eventually-perfect-failure-detector/. The authors are listed in prov/S0DYB3.jsonl.

import random
from collections import Counter

from eventually_perfect_failure_detector import exact_at_end, false_suspicions, run

ETA, DELTA = 4, 6


def random_case(seed: int, n: int = 5) -> tuple[int, dict[int, int]]:
    rng = random.Random(seed)
    gst = rng.randint(0, 400)
    who = rng.sample(range(n), rng.randint(0, (n - 1) // 2))
    return gst, {p: rng.randint(0, gst + 200) for p in who}


def test_no_false_suspicions_in_the_end_and_a_bound_per_pair() -> None:
    # After GST + eta + delta, process p can suspect a correct q at most
    # eta + delta - 2 - T0 times: each mistake raises T[q] by 1, and from
    # T[q] = eta + delta - 2 on a heartbeat always comes in time.
    for seed in range(40):
        gst, crash = random_case(seed)
        for mode in ("random", "adversary"):
            res = run(5, gst, ETA, DELTA, gst + 1500, seed, crash, True, 1, mode)
            assert exact_at_end(res)
            ok = set(res["correct"])
            late = Counter((p, q) for t, p, q, k in res["events"] if k == "suspect" and t >= gst + ETA + DELTA and p in ok and q in ok)
            assert all(c <= ETA + DELTA - 2 - 1 for c in late.values()), late


def test_mistakes_happen_before_gst() -> None:
    total = 0
    for seed in range(10):
        res = run(4, 300, ETA, DELTA, 600, seed)
        total += false_suspicions(res) - false_suspicions(res, 300)
    assert total > 0


def test_a_crashed_process_is_suspected_for_ever() -> None:
    for seed in range(40):
        gst, crash = random_case(seed)
        res = run(5, gst, ETA, DELTA, gst + 800, seed, crash)
        for q, c in crash.items():
            # Heartbeats sent before the crash arrive by max(c, GST) + delta.
            quiet = max(c, gst) + DELTA
            assert not any(k == "trust" and src == q and t > quiet for t, p, src, k in res["events"])
            for p in res["correct"]:
                assert q in res["suspects"][p]


def test_a_fixed_timeout_below_eta_plus_delta_keeps_making_mistakes() -> None:
    # Non-example: T = eta + delta - 3 is fixed. With the delays 1, delta,
    # eta + 1, 1, delta, eta + 1, ... the gap between two arrivals is
    # eta + delta - 1 in every third period, so a correct process is
    # suspected again and again, for ever. The growing timeout makes at
    # most one mistake per pair (4 * 3 pairs) after GST + eta + delta.
    t0 = ETA + DELTA - 3
    for seed in range(10):
        gst = 100 + seed
        horizon = gst + 2000
        fixed = run(4, gst, ETA, DELTA, horizon, seed, None, False, t0, "adversary")
        grow = run(4, gst, ETA, DELTA, horizon, seed, None, True, t0, "adversary")
        assert false_suspicions(fixed, horizon - 500) > 0
        assert false_suspicions(grow, gst + ETA + DELTA) <= 4 * 3
        assert false_suspicions(grow, horizon - 500) == 0 and exact_at_end(grow)


def test_a_fixed_timeout_of_eta_plus_delta_minus_2_is_enough_after_gst() -> None:
    # If the bounds were known, a fixed timeout would do. The point of the
    # growing timeout is that eta + delta is not known.
    for seed in range(10):
        gst, crash = random_case(seed, 4)
        for mode in ("random", "adversary"):
            res = run(4, gst, ETA, DELTA, gst + 600, seed, crash, False, ETA + DELTA - 2, mode)
            assert false_suspicions(res, gst + ETA + DELTA) == 0
            assert exact_at_end(res)
