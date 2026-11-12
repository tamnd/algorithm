# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sporadic-server/. The authors are listed in prov/NBTSC8.jsonl.

import random
from math import lcm

from sporadic_server import sporadic_server


def rta(c: int, higher: list[tuple[int, int]], limit: int) -> int | None:
    r = c
    while r <= limit:
        nxt = c + sum(-(-r // t) * ch for ch, t in higher)
        if nxt == r:
            return r
        r = nxt
    return None


def test_replenishment_rules_trace() -> None:
    r = sporadic_server([], (9, 2, 5), [(1, 1), (3, 3)], 14)
    assert r.timeline[:10] == [None, "S", None, "S", None, None, "S", None, "S", None]
    assert r.replenishments == [(6, 1), (8, 1), (11, 1), (13, 1)]
    assert r.aperiodic == [2, 9]


def test_no_double_hit() -> None:
    # Same case that makes a deferrable server miss: Cs=2, Ts=5, task released at 3 with C=2, D=5.
    tasks = [(1, 2, 20, 5, 3)]
    r = sporadic_server(tasks, (9, 2, 5), [(3, 4)], 12)
    assert r.timeline[3:11] == ["S", "S", 0, 0, None, "S", "S", None]
    assert r.jobs[0] == [(3, 7)] and r.misses(tasks) == 0
    assert r.replenishments[0] == (8, 2)


def test_top_priority_window_bound() -> None:
    rng = random.Random(8)
    for _ in range(300):
        cs = rng.randint(1, 3)
        ts = rng.randint(2 * cs, 9)
        tasks = [(1, 1, rng.randint(4, 9), 50, rng.randint(0, 5))]
        reqs = sorted((rng.randint(0, 50), rng.randint(1, 5)) for _ in range(rng.randint(1, 12)))
        r = sporadic_server(tasks, (9, cs, ts), reqs, 70)
        run = [1 if x == "S" else 0 for x in r.timeline]
        assert max(sum(run[a:a + ts]) for a in range(len(run) - ts + 1)) <= cs


def test_lower_tasks_meet_rta_with_server_as_periodic_task() -> None:
    rng = random.Random(21)
    checked = 0
    for _ in range(400):
        n = rng.randint(1, 3)
        periods = [rng.choice([4, 5, 6, 8, 10, 12]) for _ in range(n)]
        cs, ts = rng.randint(1, 2), rng.choice([4, 5, 6])
        tasks = [(0, rng.randint(1, max(1, t // 3)), t, t, 0) for t in periods]
        prios = rng.sample(range(1, 10), n + 1)
        ps = prios[-1]
        tasks = [(prios[i], c, t, d, 0) for i, (_, c, t, d, _) in enumerate(tasks)]
        h = lcm(*periods, ts)
        if h > 120:
            continue
        reqs = sorted((rng.randint(0, 2 * h), rng.randint(1, 4)) for _ in range(rng.randint(0, 15)))
        bounds = []
        for p, c, t, d, _ in tasks:
            higher = [(c2, t2) for p2, c2, t2, _, _ in tasks if p2 > p]
            if ps > p:
                higher.append((cs, ts))
            bounds.append(rta(c, higher, d))
        if any(b is None for b in bounds):
            continue
        try:
            r = sporadic_server(tasks, (ps, cs, ts), reqs, 3 * h)
        except ValueError:
            raise AssertionError("overrun in a set that RTA accepts")
        for i, b in enumerate(bounds):
            assert r.worst_response(i) <= b
            assert all(f is not None for rr, f in r.jobs[i] if rr + tasks[i][3] <= 3 * h)
        checked += 1
    assert checked > 100


def test_errors() -> None:
    try:
        sporadic_server([(9, 1, 4, 4, 0)], (9, 1, 2), [], 4)
    except ValueError:
        pass
    else:
        raise AssertionError("equal priorities accepted")
