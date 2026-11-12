# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aging/. The authors are listed in prov/1CN15A.jsonl.

import random
from fractions import Fraction

from aging import effective_priority, schedule_with_aging, wait_bound


def stream(k: int) -> tuple:
    """A low process L (priority 5, burst 3) at time 1, and k processes of
    priority 0 and burst 2 at times 0, 2, ..., 2(k - 1), which keep the CPU busy."""
    arrival = [1] + [2 * j for j in range(k)]
    burst = [3] + [2] * k
    priority = [5] + [0] * k
    return arrival, burst, priority


def test_rule() -> None:
    assert [effective_priority(5, w, 4) for w in (0, 3, 4, 8, 19, 20, 100)] == [5, 5, 4, 3, 1, 0, 0]
    assert effective_priority(5, 100, None) == 5
    assert effective_priority(3, Fraction(7, 2), Fraction(1, 2)) == 0


def test_low_job_starves_without_aging() -> None:
    k = 1000
    a, b, p = stream(k)
    start = schedule_with_aging(a, b, p, period=None)
    assert start[0] == 2 * k  # L runs only after the whole stream
    assert all(start[j] == 2 * (j - 1) for j in range(1, k + 1))


def test_low_job_finishes_with_aging() -> None:
    k = 1000
    a, b, p = stream(k)
    start = schedule_with_aging(a, b, p, period=4)
    # L waits 21 >= 5 * 4, so at time 22 its priority is 0 and it arrived first.
    assert start[0] == 22
    assert start[0] - a[0] <= wait_bound(0, a, b, p, 4)
    # the same with a longer stream: the start of L does not move
    a2, b2, p2 = stream(5000)
    assert schedule_with_aging(a2, b2, p2, period=4)[0] == 22


def test_wait_bound_holds() -> None:
    rng = random.Random(1)
    for _ in range(400):
        n = rng.randrange(1, 15)
        a = sorted(rng.randrange(0, 30) for _ in range(n))
        b = [rng.randrange(1, 6) for _ in range(n)]
        p = [rng.randrange(0, 6) for _ in range(n)]
        period = rng.randrange(1, 5)
        start = schedule_with_aging(a, b, p, period)
        for i in range(n):
            assert start[i] - a[i] <= wait_bound(i, a, b, p, period)


def test_valid_schedule_and_no_aging_is_priority_order() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randrange(1, 10)
        a = [rng.randrange(0, 20) for _ in range(n)]
        b = [rng.randrange(1, 6) for _ in range(n)]
        p = [rng.randrange(0, 4) for _ in range(n)]
        for period in (None, 1, 3):
            start = schedule_with_aging(a, b, p, period)
            runs = sorted((start[i], start[i] + b[i], i) for i in range(n))
            for (s1, e1, _), (s2, _, _) in zip(runs, runs[1:]):
                assert e1 <= s2
            assert all(start[i] >= a[i] for i in range(n))
        # all at time 0 and no aging: plain priority order
        start = schedule_with_aging([0] * n, b, p, None)
        assert sorted(range(n), key=lambda i: start[i]) == sorted(range(n), key=lambda i: (p[i], i))
