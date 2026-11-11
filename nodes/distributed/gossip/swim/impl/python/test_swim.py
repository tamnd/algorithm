# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swim/. The authors are listed in prov/7NBZ21.jsonl.

import math
import statistics

from swim import Swim, expected_first_detection


def first_detection_times(n: int, order: str, trials: int) -> list[int]:
    out = []
    for seed in range(trials):
        s = Swim(n, seed, order=order)
        s.run(seed % 5 + 1)
        s.crash(0)
        t0 = s.t
        while 0 not in s.first_failed_probe:
            s.period()
        out.append(s.first_failed_probe[0] - t0)
    return out


def test_formula_tends_to_e_over_e_minus_one():
    assert abs(expected_first_detection(10 ** 6) - math.e / (math.e - 1)) < 1e-5
    assert abs(expected_first_detection(30) - 1.5660) < 1e-3


def test_first_detection_time_matches_e_over_e_minus_one():
    n = 30
    for order in ("random", "round-robin"):
        mean = statistics.mean(first_detection_times(n, order, 800))
        assert abs(mean / expected_first_detection(n) - 1) < 0.06


def test_round_robin_bounds_the_time_until_every_member_probes():
    n = 20
    for seed in range(15):
        # a huge suspicion timeout keeps the crashed member on every list
        s = Swim(n, seed, susp_mult=1000)
        s.run(seed % 7 + 1)
        s.crash(0)
        t0 = s.t
        first = {}
        while len(first) < n - 1:
            s.period()
            for i in s.alive:
                if s.last_target.get(i) == 0:
                    first.setdefault(i, s.t - t0)
            assert s.t - t0 <= 2 * n - 1


def test_suspicion_removes_false_positives_under_bounded_loss():
    suspected = confirmed = basic = 0
    for seed in range(8):
        s = Swim(40, seed, loss=0.05)
        s.run(200)
        suspected += s.false_suspicions
        confirmed += s.false_confirms
        b = Swim(40, seed, loss=0.05, suspicion=False)
        b.run(200)
        basic += b.false_confirms
    assert basic > 0          # basic SWIM declares live members faulty
    assert suspected > 0      # live members do get suspected
    assert confirmed == 0     # but they always refute in time


def test_crash_is_known_to_everyone_after_the_timeout():
    for seed in range(10):
        s = Swim(50, seed)
        s.run(3)
        s.crash(0)
        t0 = s.t
        while not s.everyone_knows(0):
            s.period()
            assert s.t - t0 <= s.timeout + 12
        assert s.first_confirm[0] - t0 >= s.timeout
        assert s.false_confirms == 0
