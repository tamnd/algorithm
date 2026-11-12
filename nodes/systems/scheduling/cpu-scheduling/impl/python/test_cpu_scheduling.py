# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cpu-scheduling/. The authors are listed in prov/DMSXXK.jsonl.

import random
from fractions import Fraction

from cpu_scheduling import Process, burst_key, fcfs_key, priority_key, simulate


def example() -> list:
    return [Process("A", 0, [4, 6, 2]), Process("B", 1, [3, 2, 3]), Process("C", 2, [5])]


def check_valid(procs: list, tr) -> None:
    """The trace is a legal schedule of one CPU."""
    segs = sorted(tr.segments)
    for (s1, e1, _), (s2, e2, _) in zip(segs, segs[1:]):
        assert s1 < e1 and e1 <= s2  # one thing at a time on the CPU
    for p in procs:
        mine = [(s, e) for s, e, n in segs if n == p.name]
        assert sum(e - s for s, e in mine) == sum(p.bursts[0::2])
        assert mine[0][0] >= p.arrival
        assert tr.completion[p.name] == mine[-1][1]
        # the CPU bursts are separated by at least the I/O bursts
        done, t, b = 0, p.arrival, 0
        need = p.bursts[0]
        for s, e in mine:
            assert s >= t
            done += e - s
            while done >= need and b + 1 < len(p.bursts):
                done -= need
                t = e + p.bursts[b + 1]
                b += 2
                need = p.bursts[b]
                assert done == 0
    assert tr.decisions[4] == len(procs)


def test_example_fcfs() -> None:
    tr = simulate(example())
    assert tr.segments == [(0, 4, "A"), (4, 7, "B"), (7, 12, "C"), (12, 15, "B"), (15, 17, "A")]
    assert tr.completion == {"C": 12, "B": 15, "A": 17}
    assert tr.ready_time == {"A": 5, "B": 6, "C": 5}
    assert tr.decisions == {1: 2, 2: 0, 3: 2, 4: 3}
    assert tr.dispatches == 5
    check_valid(example(), tr)


def test_example_shortest_burst() -> None:
    tr = simulate(example(), key=burst_key)
    assert tr.segments[-2:] == [(12, 14, "A"), (14, 17, "B")]
    assert tr.completion == {"C": 12, "A": 14, "B": 17}


def test_dispatch_latency() -> None:
    tr = simulate(example(), quantum=2, dispatch=Fraction(1, 2))
    busy = sum(e - s for s, e, n in tr.segments if n != "*")
    switch = sum(e - s for s, e, n in tr.segments if n == "*")
    assert busy == 17 and switch == Fraction(tr.dispatches, 2)
    assert tr.completion == {"C": 18, "A": Fraction(41, 2), "B": 22}
    check_valid(example(), tr)


def test_silberschatz_bursts() -> None:
    procs = [Process("P1", 0, [24]), Process("P2", 0, [3]), Process("P3", 0, [3])]
    assert simulate(procs).ready_time == {"P1": 0, "P2": 24, "P3": 27}
    assert simulate(procs, quantum=4).ready_time == {"P1": 6, "P2": 4, "P3": 7}
    procs = [Process("P1", 0, [8]), Process("P2", 1, [4]), Process("P3", 2, [9]), Process("P4", 3, [5])]
    tr = simulate(procs, key=burst_key, preemptive=True)
    assert sum(tr.ready_time.values()) == 26  # average 6.5


def test_fcfs_closed_form() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randrange(1, 8)
        procs = [Process(f"p{i}", rng.randrange(12), [rng.randrange(1, 6)]) for i in range(n)]
        tr = simulate(procs)
        t = 0
        for p in sorted(procs, key=lambda q: q.arrival):  # sorted() is stable
            t = max(t, p.arrival) + p.bursts[0]
            assert tr.completion[p.name] == t


def reference_nonpreemptive(procs: list, key) -> dict:
    """Plain list scheduler: at each free moment run the released job of least key."""
    left = list(enumerate(procs))
    t, done = 0, {}
    while left:
        t = max(t, min(p.arrival for _, p in left))
        cand = [(key(p, 0, p.bursts[0]), p.arrival, i, p) for i, p in left if p.arrival <= t]
        _, _, i, p = min(cand, key=lambda c: c[:3])
        t += p.bursts[0]
        done[p.name] = t
        left = [(j, q) for j, q in left if j != i]
    return done


def test_nonpreemptive_against_reference() -> None:
    rng = random.Random(11)
    for _ in range(500):
        n = rng.randrange(1, 7)
        procs = [Process(f"p{i}", rng.randrange(10), [rng.randrange(1, 6)], rng.randrange(3))
                 for i in range(n)]
        for key in (fcfs_key, burst_key, priority_key):
            assert simulate(procs, key=key).completion == reference_nonpreemptive(procs, key)


def test_random_traces_are_valid() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randrange(1, 6)
        procs = []
        for i in range(n):
            k = rng.randrange(0, 3)
            bursts = [rng.randrange(1, 5) for _ in range(2 * k + 1)]
            procs.append(Process(f"p{i}", rng.randrange(8), bursts, rng.randrange(3)))
        for kw in ({}, {"key": burst_key, "preemptive": True}, {"quantum": 2},
                   {"key": priority_key, "preemptive": True, "dispatch": Fraction(1, 3)}):
            check_valid(procs, simulate(procs, **kw))
