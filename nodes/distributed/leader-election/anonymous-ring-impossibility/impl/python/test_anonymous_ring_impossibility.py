# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anonymous-ring-impossibility/. The authors are listed in prov/DFYQ3T.jsonl.

from anonymous_ring_impossibility import (
    leaders,
    lcr_without_ids,
    random_program,
    run_phases,
    run_sync,
)


def all_equal(row) -> bool:
    return all(s == row[0] for s in row)


def test_random_programs_stay_symmetric() -> None:
    for seed in range(60):
        prog = random_program(seed)
        for n in range(1, 9):
            for row in run_sync(prog, n, 12):
                assert all_equal(row)
                assert leaders(prog, row) in (0, n)


def test_phase_schedule_stays_symmetric() -> None:
    for seed in range(60):
        prog = random_program(seed)
        for n in range(1, 9):
            hist = run_phases(prog, n, 12)
            for row in hist:
                assert all_equal(row)
            # and it is the same run as the lock-step one, state by state
            assert hist == run_sync(prog, n, 12)


def test_lcr_without_ids_elects_everyone() -> None:
    prog = lcr_without_ids()
    for n in range(2, 9):
        hist = run_sync(prog, n, n + 2)
        counts = [leaders(prog, row) for row in hist]
        assert counts[n - 1] == 0 and counts[n] == n
        assert all(c in (0, n) for c in counts)
