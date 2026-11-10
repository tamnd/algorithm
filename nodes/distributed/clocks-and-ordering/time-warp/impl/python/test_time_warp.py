# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/time-warp/. The authors are listed in prov/GQ6HAV.jsonl.

from time_warp import TimeWarp, initial_events, sequential


def test_matches_sequential_simulation() -> None:
    total_rollbacks = total_anti = 0
    for seed in range(30):
        n = 2 + seed % 5
        events = initial_events(n, per_lp=3, seed=seed)
        end = 60
        want_state, want_done = sequential(n, events, end)
        tw = TimeWarp(n, events, end, seed=seed)
        tw.run(fossil_every=5)
        got_state, got_done = tw.result()
        assert got_state == want_state
        assert got_done == want_done
        total_rollbacks += tw.stats.rollbacks
        total_anti += tw.stats.antimessages
    assert total_rollbacks > 0 and total_anti > 0  # the runs did roll back


def test_gvt_never_decreases_and_bounds_rollbacks() -> None:
    for seed in range(10):
        n = 4
        events = initial_events(n, per_lp=4, seed=seed)
        tw = TimeWarp(n, events, 80, seed=seed, max_delay=9)
        tw.run(fossil_every=3)
        g = [x for x in tw.stats.gvt_values if x != float("inf")]
        assert g == sorted(g)
