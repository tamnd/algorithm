# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/force-directed-scheduling/. The authors are listed in prov/CDK7W8.jsonl.

import itertools
import random
from fractions import Fraction as F

from force_directed_scheduling import (distribution_graphs, force, force_directed_schedule, resource_usage,
                                       time_frames)

# The differential equation example (Paulin and Knight): v1 .. v11 are 0 .. 10.
KIND = ["mul", "mul", "mul", "alu", "alu", "mul", "mul", "mul", "alu", "alu", "alu"]
EDGES = [(0, 2), (1, 2), (2, 3), (3, 4), (5, 6), (6, 4), (7, 8), (9, 10)]
N = 11


def feasible(n, delay, edges, latency, start):
    return (all(start[v] >= start[u] + delay[u] for (u, v) in edges)
            and all(1 <= start[v] and start[v] + delay[v] - 1 <= latency for v in range(n)))


def all_schedules(n, delay, edges, latency):
    frames = time_frames(n, delay, edges, latency, {})
    for t in itertools.product(*[range(a, b + 1) for a, b in frames]):
        if feasible(n, delay, edges, latency, t):
            yield list(t)


def units(n, kind, delay, start):
    return sum(resource_usage(n, kind, delay, start).values())


def random_dfg(rng, n):
    kind = [rng.choice("ma") for _ in range(n)]
    delay = [rng.choice([1, 1, 2]) for _ in range(n)]
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.35]
    return kind, delay, edges


def test_diffeq_first_forces():
    d = [1] * N
    frames = time_frames(N, d, EDGES, 4, {})
    dg = distribution_graphs(N, KIND, d, frames)
    assert dg["mul"] == {1: F(17, 6), 2: F(7, 3), 3: F(5, 6)}
    assert dg["alu"] == {1: F(1, 3), 2: F(1), 3: F(2), 4: F(5, 3)}
    want = {5: [F(1, 4), F(-1)], 7: [F(5, 6), F(11, 18), F(-19, 18)], 10: [F(-4, 3), F(0), F(1, 9)]}
    for v, forces in want.items():
        lo, hi = frames[v]
        assert [force(N, KIND, d, EDGES, 4, {}, frames, dg, v, s) for s in range(lo, hi + 1)] == forces


def test_diffeq_schedules():
    d = [1] * N
    trace = []
    s = force_directed_schedule(N, KIND, d, EDGES, 4, trace)
    assert s == [1, 1, 2, 3, 4, 2, 3, 3, 4, 1, 2]
    assert trace == [(10, 2, F(-4, 3)), (7, 3, F(-7, 6)), (5, 2, F(-1, 2))]
    assert resource_usage(N, KIND, d, s) == {"mul": 2, "alu": 2}
    assert min(units(N, KIND, d, t) for t in all_schedules(N, d, EDGES, 4)) == 4
    for latency, want in ((5, {"mul": 2, "alu": 1}), (6, {"mul": 2, "alu": 1})):
        s = force_directed_schedule(N, KIND, d, EDGES, latency)
        assert feasible(N, d, EDGES, latency, s)
        assert resource_usage(N, KIND, d, s) == want
    assert force_directed_schedule(N, KIND, d, EDGES, 3) is None


def test_not_optimal():
    # one unit type; FDS first starts v3 at step 2, which puts v1 and v2 both at step 1
    kind = ["a"] * 5
    d = [1] * 5
    edges = [(0, 2), (1, 2), (1, 3), (2, 4), (3, 4)]
    trace = []
    s = force_directed_schedule(5, kind, d, edges, 5, trace)
    assert s == [1, 1, 2, 4, 5]
    assert trace == [(2, 2, F(-10, 9)), (3, 4, F(-4, 9))]
    assert units(5, kind, d, s) == 2
    assert units(5, kind, d, [1, 2, 3, 4, 5]) == 1


def test_frames_are_exact():
    # every start in a frame belongs to some schedule that also meets the fixed starts
    rng = random.Random(5401)
    for _ in range(80):
        n = rng.randint(1, 5)
        kind, delay, edges = random_dfg(rng, n)
        cp = max(a + delay[v] - 1 for v, (a, _) in enumerate(time_frames(n, delay, edges, 99, {})))
        latency = cp + rng.randint(0, 2)
        sched = list(all_schedules(n, delay, edges, latency))
        fixed = {}
        for v in rng.sample(range(n), rng.randint(0, n)):
            fixed[v] = rng.randint(1, latency)
        frames = time_frames(n, delay, edges, latency, fixed)
        ok = [t for t in sched if all(t[v] == s for v, s in fixed.items())]
        if frames is None:
            assert not ok
            continue
        for v in range(n):
            assert {t[v] for t in ok} == set(range(frames[v][0], frames[v][1] + 1))


def test_against_exhaustive():
    rng = random.Random(5402)
    worse = 0
    for _ in range(250):
        n = rng.randint(1, 6)
        kind, delay, edges = random_dfg(rng, n)
        cp = max(a + delay[v] - 1 for v, (a, _) in enumerate(time_frames(n, delay, edges, 99, {})))
        assert force_directed_schedule(n, kind, delay, edges, cp - 1) is None
        for latency in (cp, cp + 1, cp + 2):
            s = force_directed_schedule(n, kind, delay, edges, latency)
            assert feasible(n, delay, edges, latency, s)
            best = min(units(n, kind, delay, t) for t in all_schedules(n, delay, edges, latency))
            got = units(n, kind, delay, s)
            assert got >= best
            worse += got > best
            assert s == force_directed_schedule(n, kind, delay, edges, latency)  # deterministic
    # a heuristic: it misses the optimum on some instances, but not on most
    assert 0 < worse < 75
