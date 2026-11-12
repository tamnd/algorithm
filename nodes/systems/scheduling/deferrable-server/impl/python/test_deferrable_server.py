# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deferrable-server/. The authors are listed in prov/D4EFKC.jsonl.

import random

from deferrable_server import deferrable_server


def test_budget_is_kept_and_used_late() -> None:
    r = deferrable_server([], (9, 2, 5), [(3, 2)], 10)
    assert r.timeline[:5] == [None, None, None, "S", "S"]
    assert r.aperiodic == [5]


def test_double_hit() -> None:
    # Server (Cs=2, Ts=5) at top priority; a lower task released at 3 with C=2, D=5.
    tasks = [(1, 2, 20, 5, 3)]
    r = deferrable_server(tasks, (9, 2, 5), [(3, 4)], 12)
    assert r.timeline[3:9] == ["S", "S", "S", "S", 0, 0]
    assert r.jobs[0] == [(3, 9)]
    assert r.misses(tasks) == 1
    # Without the request, the same task meets its deadline.
    q = deferrable_server(tasks, (9, 2, 5), [], 12)
    assert q.jobs[0] == [(3, 5)] and q.misses(tasks) == 0


def test_window_bound_two_budgets() -> None:
    # In any window of length w, a top-priority DS runs at most Cs * (ceil((w - Cs) / Ts) + 1).
    rng = random.Random(4)
    for _ in range(200):
        cs, ts = rng.randint(1, 3), rng.randint(4, 8)
        reqs = sorted((rng.randint(0, 60), rng.randint(1, 5)) for _ in range(rng.randint(1, 10)))
        r = deferrable_server([], (9, cs, ts), reqs, 80)
        run = [1 if x == "S" else 0 for x in r.timeline]
        for w in range(1, 30):
            bound = cs * (-(-(w - cs) // ts) + 1) if w > cs else w
            assert max(sum(run[a:a + w]) for a in range(len(run) - w + 1)) <= bound
        for start in range(0, 80, ts):
            assert sum(run[start:start + ts]) <= cs


def rta(c: int, higher: list[tuple[int, int]], server: tuple[int, int] | None, limit: int) -> int | None:
    r = c
    while r <= limit:
        nxt = c + sum(-(-r // t) * ch for ch, t in higher)
        if server is not None:
            cs, ts = server
            nxt += cs + max(0, -(-(r - cs) // ts)) * cs
        if nxt == r:
            return r
        r = nxt
    return None


def test_lower_tasks_meet_rta_with_double_hit_term() -> None:
    rng = random.Random(9)
    checked = 0
    for _ in range(400):
        n = rng.randint(1, 3)
        periods = [rng.choice([4, 5, 6, 8, 10, 12]) for _ in range(n)]
        cs, ts = rng.randint(1, 2), rng.choice([4, 5, 6])
        prios = rng.sample(range(1, 10), n + 1)
        ps = prios[-1]
        tasks = [(prios[i], rng.randint(1, max(1, t // 3)), t, t, rng.randint(0, 3)) for i, t in enumerate(periods)]
        h = 120
        reqs = sorted((rng.randint(0, 2 * h), rng.randint(1, 4)) for _ in range(rng.randint(0, 20)))
        bounds = []
        for p, c, t, d, _ in tasks:
            higher = [(c2, t2) for p2, c2, t2, _, _ in tasks if p2 > p]
            bounds.append(rta(c, higher, (cs, ts) if ps > p else None, d))
        if any(b is None for b in bounds):
            continue
        r = deferrable_server(tasks, (ps, cs, ts), reqs, 3 * h)
        for i, b in enumerate(bounds):
            assert r.worst_response(i) <= b
        checked += 1
    assert checked > 100


def test_fcfs_and_service() -> None:
    r = deferrable_server([(1, 1, 4, 4, 0)], (9, 1, 2), [(0, 2), (1, 1)], 10)
    assert r.aperiodic == [3, 5]
    assert r.misses([(1, 1, 4, 4, 0)]) == 0


def test_errors() -> None:
    try:
        deferrable_server([(9, 1, 4, 4, 0)], (9, 1, 2), [], 4)
    except ValueError:
        pass
    else:
        raise AssertionError("equal priorities accepted")
