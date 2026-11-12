# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preemption/. The authors are listed in prov/D0YFHB.jsonl.

import random

from preemption import response_times, schedule

A, B, P = [0, 2, 3], [6, 2, 3], [2, 1, 3]


def test_example_three_models() -> None:
    r = schedule(A, B, P, "none")
    assert r["slices"] == [(0, 0, 6), (1, 6, 8), (2, 8, 11)]
    assert response_times(A, r) == [0, 4, 5]
    r = schedule(A, B, P, "resume")
    assert r["slices"] == [(0, 0, 2), (1, 2, 4), (0, 4, 8), (2, 8, 11)]
    assert response_times(A, r) == [0, 0, 5]
    r = schedule(A, B, P, "repeat")
    assert r["slices"] == [(0, 0, 2), (1, 2, 4), (0, 4, 10), (2, 10, 13)]
    assert r["completion"] == [10, 4, 13]


def test_example_with_switch_cost() -> None:
    r = schedule(A, B, P, "none", 1)
    assert r["switches"] == 3 and max(r["completion"]) == 14
    r = schedule(A, B, P, "resume", 1)
    assert r["switches"] == 4 and max(r["completion"]) == 15
    assert response_times(A, r)[1] == 1


def random_input(rng: random.Random) -> tuple:
    n = rng.randrange(1, 9)
    a = [rng.randrange(0, 20) for _ in range(n)]
    b = [rng.randrange(1, 8) for _ in range(n)]
    p = [rng.randrange(0, 4) for _ in range(n)]
    return a, b, p


def check_valid(a: list, b: list, r: dict, exact: bool) -> None:
    prev = 0
    got = [0] * len(a)
    for i, s, e in r["slices"]:
        assert s >= prev and s >= a[i] and e > s
        prev = e
        got[i] += e - s
    for i in range(len(a)):
        assert got[i] == b[i] if exact else got[i] >= b[i]


def test_resume_without_cost_keeps_the_busy_periods() -> None:
    rng = random.Random(1)
    for _ in range(400):
        a, b, p = random_input(rng)
        none = schedule(a, b, p, "none")
        res = schedule(a, b, p, "resume")
        rep = schedule(a, b, p, "repeat")
        check_valid(a, b, none, True)
        check_valid(a, b, res, True)
        check_valid(a, b, rep, False)
        # preempt-resume at zero cost does not change when the CPU is busy
        assert max(none["completion"]) == max(res["completion"])
        assert max(rep["completion"]) >= max(res["completion"])


def unit_step(a: list, b: list, p: list) -> list:
    left, done, t = list(b), [None] * len(a), 0
    while any(left):
        ready = [j for j in range(len(a)) if a[j] <= t and left[j] > 0]
        if ready:
            j = min(ready, key=lambda j: (p[j], a[j], j))
            left[j] -= 1
            if left[j] == 0:
                done[j] = t + 1
        t += 1
    return done


def test_resume_matches_unit_step_reference() -> None:
    rng = random.Random(2)
    for _ in range(400):
        a, b, p = random_input(rng)
        assert schedule(a, b, p, "resume")["completion"] == unit_step(a, b, p)


def test_top_priority_response() -> None:
    rng = random.Random(3)
    for _ in range(400):
        a, b, p = random_input(rng)
        top = rng.randrange(len(a))
        p[top] = -1  # strictly the highest priority
        for s in (0, 1, 2):
            r = schedule(a, b, p, "resume", s)
            assert response_times(a, r)[top] <= 2 * s
            r = schedule(a, b, p, "none", s)
            assert response_times(a, r)[top] <= max(b) + 2 * s
