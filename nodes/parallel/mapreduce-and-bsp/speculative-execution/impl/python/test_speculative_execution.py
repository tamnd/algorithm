# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/speculative-execution/. The authors are listed in prov/SZRQN3.jsonl.

import random

import pytest

from speculative_execution import (expected_no_backup, expected_with_backup, hadoop_candidates,
                                   late_choice, late_estimates, simulate)

CASES = [(1, 0.3, 2), (10, 0.1, 4), (50, 0.02, 5), (200, 0.01, 5), (30, 0.5, 3)]


@pytest.mark.parametrize("n,pi,s", CASES)
def test_simulation_matches_formulas(n, pi, s):
    rng = random.Random(n * 1000 + s)
    trials = 3000
    for backups, formula in ((False, expected_no_backup), (True, expected_with_backup)):
        runs = [simulate(n, pi, s, rng, backups) for _ in range(trials)]
        mean = sum(t for t, _ in runs) / trials
        assert abs(mean - formula(n, pi, s)) < 0.04 * (s - 1)
        if backups:
            copies = sum(c for _, c in runs) / trials
            assert abs(copies - n * pi) < 0.1 * n * pi + 0.1


def test_backups_never_hurt_in_the_model():
    for n, pi, s in CASES:
        assert expected_with_backup(n, pi, s) <= expected_no_backup(n, pi, s) + 1e-12
    assert expected_with_backup(5, 0.0, 9) == expected_no_backup(5, 0.0, 9) == 1


def test_late_estimate_is_exact_for_constant_rates():
    rng = random.Random(2)
    now = 100.0
    tasks, truth = [], {}
    for k in range(30):
        start = rng.uniform(0, 90)
        rate = rng.uniform(0.001, 0.0109)
        ps = min(1.0, rate * (now - start))
        if ps < 1.0:
            tasks.append((k, start, ps))
            truth[k] = (1 - ps) / rate
    est = late_estimates(tasks, now)
    for k, left in truth.items():
        assert est[k][1] == pytest.approx(left)


def test_hadoop_flags_a_late_starter_but_late_does_not():
    now = 100.0
    tasks = [("t%d" % i, 0.0, r * now) for i, r in
             enumerate([0.006, 0.0065, 0.007, 0.0075, 0.008, 0.0085])]
    tasks.append(("slow", 0.0, 0.3))          # rate 0.003: a real straggler
    tasks.append(("late start", 40.0, 0.42))  # rate 0.007: normal speed, started late
    assert sorted(hadoop_candidates(tasks, now)) == ["late start", "slow"]
    assert late_choice(tasks, now) == "slow"
    est = late_estimates(tasks, now)
    assert est["slow"][1] == pytest.approx(0.7 / 0.003)
    assert est["late start"][1] == pytest.approx(0.58 / 0.007)
