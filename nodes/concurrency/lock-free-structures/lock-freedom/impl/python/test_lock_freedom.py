# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-freedom/. The authors are listed in prov/NXBV97.jsonl.

from explorer import World, explore, solo
from lock_freedom import completions, max_steps_without_completion, setup_for, starving_schedule


def test_a_fair_schedule_starves_one_process() -> None:
    w = starving_schedule(1000)
    assert w.steps == [2000, 2000]          # both take steps all the time
    assert completions(w) == [0, 1000]      # only p1 completes


def test_system_progress_bound() -> None:
    # In every run, at most 2n - 1 steps in a row pass with no completed push.
    for n, count in ((2, 2), (2, 3), (3, 1), (3, 2)):
        assert max_steps_without_completion(n, count) <= 2 * n - 1
    assert max_steps_without_completion(2, 3) == 3
    assert max_steps_without_completion(3, 2) == 5


def test_every_run_of_a_finite_workload_ends() -> None:
    # explore raises Found if some run is longer than the depth bound.
    assert explore(setup_for(2, 2), max_depth=60)[1] > 0
    assert explore(setup_for(3, 2), max_depth=60)[1] > 0


def test_a_stopped_lock_holder_blocks_the_others() -> None:
    w = World(setup_for(2, 1, locked=True))
    w.step(0)                                # p0 takes the lock, then stops
    outcome, _ = solo(w, 1, 50)
    assert outcome == "loop"                 # p1 spins for ever
