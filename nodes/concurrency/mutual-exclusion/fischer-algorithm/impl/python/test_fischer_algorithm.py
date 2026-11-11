# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fischer-algorithm/. The authors are listed in prov/DRQ896.jsonl.
import pytest

from fischer_algorithm import CS, replay, search


def test_safe_exactly_when_delay_exceeds_step():
    # All timed runs: two processes in the CS are possible if and only if delay <= step_max.
    for n in (2, 3):
        for step_max in (1, 2, 3):
            for delay in range(0, step_max + 1):
                assert search(n, step_max, delay)[1] is not None, (n, step_max, delay)
            for delay in (step_max + 1, step_max + 2):
                assert search(n, step_max, delay)[1] is None, (n, step_max, delay)


def test_state_counts():
    assert search(2, 2, 3) == (255, None)
    assert search(3, 2, 3) == (6108, None)


def test_found_run_is_a_legal_timed_run():
    # With delay = step_max, the search finds a run that ends with both processes inside.
    _, bad = search(2, 2, 2)
    _, pcs, _ = replay(2, 2, 2, [(t, p) for t, p, _ in bad])
    assert pcs == (CS, CS)


def test_worked_example():
    # The example of the page: step_max = 2 and delay = 3; process indexes 0 and 1 are the names 1 and 2.
    run = [(0, 0), (0, 0), (0, 1), (0, 1),  # both read x = 0 at time 0
           (1, 0),  # 0 writes x = 1
           (2, 1),  # 1 writes x = 2
           (4, 0),  # 0 checks x = 2: not its name, back to the wait
           (5, 1),  # 1 checks x = 2 and enters
           (5, 0)]  # 0 reads x = 2 and waits
    x, pcs, _ = replay(2, 2, 3, run)
    assert x == 2 and pcs == ("await", CS)


def test_broken_delay_run():
    # step_max = 2 and delay = 1: process 1 writes x after process 0 has checked it.
    run = [(0, 0), (0, 0), (0, 1), (0, 1), (0, 0),  # both read x = 0; 0 writes x = 1
           (1, 0),  # 0 checks x = 1 after the delay of 1 and enters
           (2, 1),  # 1 writes x = 2, 2 time units after its read
           (3, 1)]  # 1 checks x = 2 and enters
    x, pcs, _ = replay(2, 2, 1, run)
    assert pcs == (CS, CS) and x == 2
    # With delay = 3 > step_max the same run is not allowed: the check of 0 comes too early.
    with pytest.raises(AssertionError):
        replay(2, 2, 3, run)


def test_solo():
    # Alone: leave the remainder, read x = 0, write x, wait the delay, check x and enter.
    for delay in (1, 2, 5):
        x, pcs, _ = replay(3, 1, delay, [(0, 0), (0, 0), (0, 0), (delay, 0)])
        assert pcs[0] == CS and x == 1


def test_starvation_cycle():
    # step_max = 1, delay = 2. Process 1 reads x = 0 each time, but process 0 writes x last.
    prefix = [(0, 0), (0, 0), (0, 0), (0, 1), (1, 1), (2, 0), (2, 1)]
    s = replay(2, 1, 2, prefix)
    assert s[1] == (CS, "await") and s[0] == 1
    events = list(prefix)
    for k in range(5):
        t = 2 + 3 * k
        events += [(t, 0), (t, 0), (t, 0), (t, 0),  # 0 leaves, comes back, reads x = 0
                   (t + 1, 1), (t + 1, 1),  # 1 reads x = 0 and writes x = 2
                   (t + 1, 0),  # 0 writes x = 1 at the same time, after 1
                   (t + 3, 1),  # 1 checks x = 1: not its name, back to the wait
                   (t + 3, 0)]  # 0 checks x = 1 and enters
        assert replay(2, 1, 2, events) == s  # the same state again
