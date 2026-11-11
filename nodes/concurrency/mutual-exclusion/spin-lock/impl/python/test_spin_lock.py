# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spin-lock/. The authors are listed in prov/S4E1T8.jsonl.

from fractions import Fraction

from interleave import explore, max_passage_rmr, no_progress, run, starvation
from spin_lock import client, spin_lock_acquire, spin_then_block, tas_acquire, ttas_acquire

INIT = {"L": False}


def ttas_bo(max_delay):
    return lambda: spin_lock_acquire("L", 1, max_delay)


def test_mutual_exclusion_two_processes_two_rounds() -> None:
    g = explore([client(ttas_bo(4), rounds=2)] * 2, INIT)
    assert g.violation is None and not g.stuck


def test_mutual_exclusion_three_processes() -> None:
    g = explore([client(ttas_bo(2), rounds=1)] * 3, INIT)
    assert g.violation is None and not g.stuck


def test_deadlock_free_but_not_starvation_free() -> None:
    g = explore([client(ttas_bo(2), rounds=None)] * 2, INIT)
    assert g.violation is None
    assert no_progress(g) == []
    assert starvation(g, 0) != []


def test_waiting_cost_while_the_lock_is_held() -> None:
    # process 1 takes the lock and stops in its critical section; process 0 then spins 200 steps
    for acquire, first, want in ((tas_acquire, 2, 199), (ttas_acquire, 3, 1)):
        def policy(t, enabled, rng, first=first):
            return 1 if t < first else 0
        m = run([client(acquire, rounds=1)] * 2, INIT, policy=policy, max_steps=first + 200)
        assert m.section[1] == "cs"
        assert m.rmr["cc"][0] == want


def test_passage_cost_is_unbounded_for_all_three() -> None:
    for acquire in (tas_acquire, ttas_acquire, ttas_bo(2)):
        g = explore([client(acquire, rounds=None)] * 2, INIT, cache=True)
        assert max_passage_rmr(g, 0, "cc") == float("inf")


def test_random_runs_keep_mutual_exclusion() -> None:
    for seed in range(40):
        n = 2 + seed % 5
        m = run([client(ttas_bo(8), rounds=3)] * n, INIT, seed=seed)
        assert m.violations == []
        assert sorted(m.entries) == sorted(p for p in range(n) for _ in range(3))


def test_spin_then_block_with_threshold_c_is_two_competitive() -> None:
    for switch in range(1, 30):
        worst = Fraction(0)
        for wait in range(1, 4 * switch + 2):
            cost = spin_then_block(wait, switch, switch)
            opt = min(wait, switch)
            assert cost <= 2 * opt
            worst = max(worst, Fraction(cost, opt))
        assert worst == 2
        assert spin_then_block(0, switch, switch) == 0


def test_no_deterministic_threshold_is_better_than_two() -> None:
    switch = 10
    eps = Fraction(1, 1000)
    for threshold in range(0, 60):
        wait = threshold + eps
        ratio = spin_then_block(wait, switch, threshold) / min(wait, switch)
        assert ratio >= 2
