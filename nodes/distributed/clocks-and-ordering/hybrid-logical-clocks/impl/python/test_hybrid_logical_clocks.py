# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-logical-clocks/. The authors are listed in prov/F6ZVRW.jsonl.

import random
from collections import deque

from hybrid_logical_clocks import random_execution, skewed_readings, timestamp_execution


def happened_before(execution: list[tuple]) -> list[set[int]]:
    """Oracle: hb[e] is the set of events f with e -> f, by BFS on the event graph."""
    succ: list[list[int]] = [[] for _ in execution]
    last: dict[int, int] = {}
    send_of: dict[int, int] = {}
    for e, (p, kind, x) in enumerate(execution):
        if p in last:
            succ[last[p]].append(e)
        last[p] = e
        if kind == "send":
            send_of[x[1]] = e
        elif kind == "recv":
            succ[send_of[x]].append(e)
    out = []
    for e in range(len(execution)):
        seen: set[int] = set()
        todo = deque(succ[e])
        while todo:
            f = todo.popleft()
            if f not in seen:
                seen.add(f)
                todo.extend(succ[f])
        out.append(seen)
    return out


def test_example() -> None:
    # P1 = 0 runs slow, P2 = 1 runs fast, P3 = 2.
    ex = [
        (1, "send", (0, 0)),  # pt 10
        (0, "local", None),  # pt 7
        (0, "recv", 0),  # pt 8
        (0, "send", (2, 1)),  # pt 9
        (2, "recv", 1),  # pt 9
        (0, "local", None),  # pt 11
    ]
    pts = [10, 7, 8, 9, 9, 11]
    assert timestamp_execution(3, ex, pts) == [(10, 0), (7, 0), (10, 1), (10, 2), (10, 3), (11, 0)]


def check(n: int, ex: list[tuple], eps: int, rng: random.Random, strict: bool) -> None:
    _, pts = skewed_readings(n, ex, eps, rng, strict)
    st = timestamp_execution(n, ex, pts)
    hb = happened_before(ex)
    for f in range(len(ex)):
        lf, cf = st[f]
        # l stays within eps of the physical clock
        assert 0 <= lf - pts[f] <= eps
        # Theorem 1: happened-before implies a smaller timestamp
        for g in hb[f]:
            assert st[f] < st[g]
        # c counts at most the causal predecessors with the same l
        same_l = sum(1 for g in range(f) if f in hb[g] and st[g][0] == lf)
        assert cf <= same_l
        if strict:
            assert cf <= n * (eps + 1)


def test_bounds_under_seeded_skew() -> None:
    rng = random.Random(2014)
    for _ in range(500):
        n = rng.randint(1, 5)
        ex = random_execution(n, rng.randint(0, 50), rng)
        eps = rng.randint(0, 20)
        check(n, ex, eps, rng, strict=rng.random() < 0.5)


def test_large_skew_drives_c_up_but_bounded() -> None:
    # One fast process sends to slow processes; their c values rise while their pt catches up.
    rng = random.Random(5)
    for _ in range(100):
        n = 4
        eps = 10
        ex = random_execution(n, 60, rng, p_send=0.5, p_recv=0.4)
        times = list(range(1, len(ex) + 1))
        pts = [t + (eps if p == 0 else 0) for t, (p, _, _) in zip(times, ex)]
        st = timestamp_execution(n, ex, pts)
        for f, (lf, cf) in enumerate(st):
            assert 0 <= lf - pts[f] <= eps
            assert cf <= n * (eps + 1)


def test_c_resets_when_physical_time_moves_ahead() -> None:
    ex = [(0, "local", None)] * 4
    assert timestamp_execution(1, ex, [5, 5, 5, 6]) == [(5, 0), (5, 1), (5, 2), (6, 0)]
