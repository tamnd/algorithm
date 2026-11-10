# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bully-algorithm/. The authors are listed in prov/HSXH10.jsonl.

import random

from bully_algorithm import bully, worst_case_messages


def agreed(sim) -> bool:
    top = max(sim.up)
    return all(c == top for c in sim.coordinators().values())


def test_page_example() -> None:
    # five processes, 5 has crashed, 2 notices first
    sim = bully(5, [(0, "crash", 5), (1, "detect", 2)])
    assert agreed(sim) and max(sim.up) == 4
    assert sim.counts == {"ELECTION": 6, "OK": 3, "COORDINATOR": 3}
    assert sim.total() == 12


def test_lowest_starts_all_up() -> None:
    for n in range(1, 30):
        sim = bully(n, [(0, "detect", 1)])
        assert agreed(sim)
        assert sim.total() == worst_case_messages(n, False) == n * n - 1
        assert sim.counts["ELECTION"] == n * (n - 1) // 2


def test_lowest_starts_after_coordinator_crash() -> None:
    for n in range(2, 30):
        sim = bully(n, [(0, "crash", n), (1, "detect", 1)])
        assert agreed(sim) and max(sim.up) == n - 1
        assert sim.total() == worst_case_messages(n, True) == n * n - n - 1


def test_best_case() -> None:
    # the second highest process notices: n - 1 messages
    for n in range(2, 30):
        sim = bully(n, [(0, "crash", n), (1, "detect", n - 1)])
        assert agreed(sim) and sim.total() == n - 1


def test_upper_bound_simultaneous_starters() -> None:
    # without crashes during the election, any set of starters that notice at the
    # same step gives at most n^2 - n - 1, and each process starts once
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randrange(2, 12)
        starters = rng.sample(range(1, n), rng.randrange(1, n))
        events = [(0, "crash", n)] + [(1, "detect", s) for s in starters]
        sim = bully(n, events)
        assert agreed(sim)
        assert sim.starts == n - min(starters)
        assert sim.total() <= worst_case_messages(n, True)


def test_late_starter_causes_second_announcement() -> None:
    sim = bully(7, [(0, "crash", 7), (1, "detect", 6), (2, "detect", 1)])
    assert agreed(sim)
    assert sim.starts > 6
    assert sim.total() > worst_case_messages(7, True)


def test_seeded_crash_patterns() -> None:
    rng = random.Random(2024)
    for trial in range(150):
        n = rng.randrange(2, 10)
        events = []
        t = 0
        for _ in range(rng.randrange(1, 6)):
            t += rng.randrange(0, 6)
            events.append((t, rng.choice(["crash", "crash", "recover"]), rng.randrange(1, n + 1)))
        # never let every process stay down
        events.append((t + 1, "recover", 1))
        sim = bully(n, events, poll=4, seed=trial)
        assert sim.up and agreed(sim), (n, events, sim.coordinators())


def test_recovered_high_process_bullies() -> None:
    sim = bully(6, [(0, "crash", 6), (1, "detect", 3), (20, "recover", 6)])
    assert agreed(sim) and max(sim.up) == 6
