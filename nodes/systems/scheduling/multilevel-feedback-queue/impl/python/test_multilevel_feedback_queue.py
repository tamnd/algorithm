# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multilevel-feedback-queue/. The authors are listed in prov/1E6C07.jsonl.

import random

import pytest

from multilevel_feedback_queue import Job, mlfq


def show(tl):
    return "".join(x or "." for x in tl)


def test_example() -> None:
    jobs = [Job("A", 0, (12,)), Job("B", 1, (1, 3, 1, 3, 1)), Job("C", 5, (3,))]
    tr = mlfq(jobs, [2, 4], [4, 8])
    assert show(tr.timeline) == "AABAACCBCAABAAAAAA"
    assert tr.done == {"C": 9, "B": 12, "A": 18}
    assert tr.levels[3]["A"] == 0 and tr.levels[4]["A"] == 1  # A moves down after 4 ticks
    assert all(lv["B"] == 0 and lv["C"] == 0 for lv in tr.levels)


def test_edges() -> None:
    assert mlfq([], [1], [1]).done == {}
    tr = mlfq([Job("X", 2, (3,))], [1, 2], [1, 2])
    assert show(tr.timeline) == "..XXX" and tr.done == {"X": 5}
    with pytest.raises(ValueError):
        mlfq([Job("X", 0, (1, 2))], [1], [1])
    with pytest.raises(ValueError):
        mlfq([], [1, 2], [1])


GAMING = [Job("L", 0, (60,)), Job("G", 0, tuple([9, 1] * 12 + [9]))]


def test_gaming_job_wins_under_rules_4a_4b() -> None:
    # G runs 9 ticks of a 10-tick quantum, then does a 1-tick I/O. Under the
    # old rules its counter is reset at each I/O, so it never moves down.
    tr = mlfq(GAMING, [10, 10, 10], [10, 10, 10], accounting=False)
    tl = show(tr.timeline)
    assert tl[:30] == "LLLLLLLLLL" + "GGGGGGGGGL" * 2
    assert all(lv["G"] == 0 for lv in tr.levels)
    assert tl[:100].count("G") == 81


def test_gaming_job_is_caught_by_accounting() -> None:
    tr = mlfq(GAMING, [10, 10, 10], [10, 10, 10], accounting=True)
    tl = show(tr.timeline)
    # 9 ticks, the I/O, then 1 more tick uses up the allotment of 10
    assert tl[:22] == "LLLLLLLLLL" + "GGGGGGGGGL" + "GL"
    assert tr.levels[19]["G"] == 0 and tr.levels[20]["G"] == 1
    assert tr.levels[49]["G"] == 2
    assert tl[:100].count("G") == 40
    assert tr.done == {"L": 96, "G": 185}


def test_level_equals_cpu_used_over_allotment() -> None:
    # Rule 4 with equal allotments A and no boost: after each tick the level of
    # a job is min(k - 1, floor(CPU used so far / A)), whatever its I/O does.
    rng = random.Random(5)
    for _ in range(300):
        k, a = rng.randrange(1, 4), rng.randrange(1, 5)
        quantum = [rng.randrange(1, a + 1) for _ in range(k)]
        jobs = []
        for i in range(rng.randrange(1, 5)):
            m = rng.randrange(0, 4)
            bursts = [rng.randrange(1, 6) for _ in range(2 * m + 1)]
            jobs.append(Job(f"j{i}", rng.randrange(6), tuple(bursts)))
        tr = mlfq(jobs, quantum, [a] * k)
        used = {j.name: 0 for j in jobs}
        for t, name in enumerate(tr.timeline):
            if name is not None:
                used[name] += 1
            for j in jobs:
                assert tr.levels[t][j.name] == min(k - 1, used[j.name] // a)
        for j in jobs:
            assert used[j.name] == sum(j.bursts[0::2])


def test_rule_1_and_no_run_during_io() -> None:
    rng = random.Random(9)
    for _ in range(300):
        k = rng.randrange(1, 4)
        quantum = [rng.randrange(1, 4) for _ in range(k)]
        allot = [q * rng.randrange(1, 3) for q in quantum]
        jobs = []
        for i in range(rng.randrange(1, 5)):
            m = rng.randrange(0, 3)
            jobs.append(Job(f"j{i}", rng.randrange(6), tuple(rng.randrange(1, 5) for _ in range(2 * m + 1))))
        tr = mlfq(jobs, quantum, allot)
        # rebuild when each job is ready from the timeline alone
        cpu = {j.name: 0 for j in jobs}
        ready_from = {j.name: j.arrival for j in jobs}
        for t, name in enumerate(tr.timeline):
            before = tr.levels[t - 1] if t > 0 else {j.name: 0 for j in jobs}
            ready = [x.name for x in jobs if ready_from[x.name] <= t < tr.done[x.name]]
            if name is None:
                assert not ready
                continue
            assert name in ready
            assert before[name] == min(before[x] for x in ready)
            cpu[name] += 1
            j = next(j for j in jobs if j.name == name)
            ends, acc = [], 0
            for p in range(0, len(j.bursts), 2):
                acc += j.bursts[p]
                ends.append((acc, p))
            for acc_end, p in ends:
                if cpu[name] == acc_end and p + 1 < len(j.bursts):
                    ready_from[name] = t + 1 + j.bursts[p + 1]


def test_boost_stops_starvation() -> None:
    long_job = Job("L", 0, (40,))
    stream = [Job(f"s{i}", i, (1,)) for i in range(3, 120)]
    starved = mlfq([long_job] + stream, [1, 2], [1, 2], boost=0)
    runs = [t for t, x in enumerate(starved.timeline) if x == "L"]
    assert runs[:4] == [0, 1, 2, 120]  # no CPU at all from tick 3 to 119
    boosted = mlfq([long_job] + stream, [1, 2], [1, 2], boost=20)
    runs = [t for t, x in enumerate(boosted.timeline) if x == "L"]
    for m in range(1, 6):
        assert any(20 * m <= t < 20 * (m + 1) for t in runs)
    assert boosted.done["L"] == starved.done["L"] == 157
