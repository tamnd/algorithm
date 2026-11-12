# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/completely-fair-scheduler/. The authors are listed in prov/BQCYGA.jsonl.

import random
from fractions import Fraction

import pytest

from completely_fair_scheduler import Task, cfs, cpu_until


def test_weights_1024_and_2048_share_1_to_2() -> None:
    a = Task("A", 1024, 0, (3000,))
    b = Task("B", 2048, 0, (6000,))
    tr = cfs([a, b], latency=48, min_gran=6)
    # period 48: slices 16 and 32, and both vruntimes grow by 16 per slice
    assert tr.runs[:4] == [(0, 16, "A"), (16, 48, "B"), (48, 64, "A"), (64, 96, "B")]
    for _, end, _ in tr.runs:
        ca, cb = cpu_until(tr.runs, "A", end), cpu_until(tr.runs, "B", end)
        assert abs(ca - end / 3) <= 16 and abs(cb - 2 * end / 3) <= 32  # within one slice
        if end % 48 == 0:
            assert cb == 2 * ca  # exact at the end of each period
    assert tr.done == {"A": 8984, "B": 9000}  # A's last slice is 8 of its 16


def test_min_granularity_stretches_the_period() -> None:
    tasks = [Task(f"t{i}", 1024, 0, (60,)) for i in range(10)]
    tr = cfs(tasks, latency=48, min_gran=6)
    assert [e - s for s, e, _ in tr.runs[:10]] == [6] * 10  # not 4.8
    assert [x for _, _, x in tr.runs[:10]] == [f"t{i}" for i in range(10)]
    tr = cfs(tasks[:4], latency=48, min_gran=6)
    assert [e - s for s, e, _ in tr.runs[:4]] == [12] * 4


def test_weighted_error_bound() -> None:
    # CPU-bound tasks that start together: at the end of every run, each task
    # is within one of its slices of its weighted fair share.
    rng = random.Random(4)
    weights = [15, 110, 335, 655, 820, 1024, 1277, 1586, 2048, 3121]
    for _ in range(40):
        ws = [rng.choice(weights) for _ in range(rng.randrange(1, 6))]
        tasks = [Task(f"t{i}", w, 0, (100000,)) for i, w in enumerate(ws)]
        lat, gran = rng.choice([(48, 6), (24, 3), (6, Fraction(3, 4))])
        tr = cfs(tasks, latency=lat, min_gran=gran, until=400)
        assert not tr.done
        total = sum(ws)
        period = max(Fraction(lat), len(ws) * Fraction(gran))
        cpu = [Fraction(0)] * len(ws)
        for s, e, x in tr.runs:
            cpu[int(x[1:])] += e - s
            for i, w in enumerate(ws):
                assert abs(cpu[i] - e * Fraction(w, total)) <= period * Fraction(w, total)


def reference(tasks, latency, min_gran):
    """A heap-free reference: a linear scan for the smallest (vruntime, index)."""
    vr = [Fraction(0)] * len(tasks)
    phase = [0] * len(tasks)
    left = [Fraction(k.bursts[0]) for k in tasks]
    ready_at = [Fraction(k.arrival) for k in tasks]
    runnable, done, runs = set(), {}, []
    t, min_vr = Fraction(0), Fraction(0)
    while len(done) < len(tasks):
        waiting = [i for i in range(len(tasks)) if ready_at[i] is not None]
        for i in sorted(waiting, key=lambda i: (ready_at[i], i)):
            if ready_at[i] <= t:
                vr[i] = max(vr[i], min_vr)
                runnable.add(i)
                ready_at[i] = None
        if not runnable:
            t = min(x for x in ready_at if x is not None)
            continue
        i = min(runnable, key=lambda i: (vr[i], i))
        big_w = sum(tasks[k].weight for k in runnable)
        sl = max(Fraction(latency), len(runnable) * Fraction(min_gran)) * tasks[i].weight / big_w
        d = min(sl, left[i])
        runs.append((t, t + d, tasks[i].name))
        t += d
        left[i] -= d
        vr[i] += d * 1024 / tasks[i].weight
        min_vr = max(min_vr, min(vr[k] for k in runnable))
        if left[i] == 0:
            runnable.discard(i)
            phase[i] += 1
            if phase[i] == len(tasks[i].bursts):
                done[tasks[i].name] = t
            else:
                ready_at[i] = t + tasks[i].bursts[phase[i]]
                phase[i] += 1
                left[i] = Fraction(tasks[i].bursts[phase[i]])
    return runs, done


def test_matches_linear_scan_reference() -> None:
    rng = random.Random(8)
    for _ in range(60):
        tasks = []
        for i in range(rng.randrange(1, 6)):
            m = rng.randrange(0, 3)
            bursts = tuple(rng.randrange(1, 40) for _ in range(2 * m + 1))
            tasks.append(Task(f"t{i}", rng.choice([512, 1024, 1277, 2048]), rng.randrange(0, 30), bursts))
        lat, gran = rng.choice([(12, 3), (20, 2), (8, 4)])
        tr = cfs(tasks, latency=lat, min_gran=gran)
        runs, done = reference(tasks, lat, gran)
        assert tr.runs == runs and tr.done == done


def longest_streak(runs, name, after):
    best = cur = Fraction(0)
    for s, e, x in runs:
        if s < after:
            continue
        cur = cur + (e - s) if x == name else Fraction(0)
        best = max(best, cur)
    return best


def test_waking_task_is_placed_at_min_vruntime() -> None:
    a = Task("A", 1024, 0, (3000,))
    b = Task("B", 1024, 0, (10, 1000, 500))  # B sleeps for 1000 time units
    placed = cfs([a, b], latency=48, min_gran=6, place=True)
    raw = cfs([a, b], latency=48, min_gran=6, place=False)
    assert longest_streak(placed.runs, "B", 1010) <= 24
    assert longest_streak(raw.runs, "B", 1010) >= 400  # B takes the CPU to catch up


def test_edges() -> None:
    assert cfs([]).done == {}
    tr = cfs([Task("X", 1024, 5, (7,))])
    assert tr.runs == [(5, 12, "X")] and tr.done == {"X": 12}
    with pytest.raises(ValueError):
        cfs([Task("X", 0, 0, (1,))])
    with pytest.raises(ValueError):
        cfs([Task("X", 1024, 0, (1, 2))])
