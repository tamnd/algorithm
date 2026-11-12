# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-scheduling/. The authors are listed in prov/RDGF8V.jsonl.

import random
from fractions import Fraction

from priority_scheduling import priority_schedule, waiting_times


def test_textbook_example() -> None:
    b, p = [10, 1, 2, 1, 5], [3, 1, 4, 5, 2]
    c, slices = priority_schedule([0] * 5, b, p)
    assert [i for i, _, _ in slices] == [1, 4, 0, 2, 3]  # P2, P5, P1, P3, P4
    w = waiting_times([0] * 5, b, p)
    assert w == [6, 0, 16, 18, 1]
    assert Fraction(sum(w), 5) == Fraction(41, 5)  # 8.2


def test_preemptive_and_nonpreemptive() -> None:
    a, b, p = [0, 1, 2, 4], [6, 2, 3, 1], [3, 1, 4, 2]
    c, slices = priority_schedule(a, b, p)
    assert slices == [(0, 0, 6), (1, 6, 8), (3, 8, 9), (2, 9, 12)]
    assert waiting_times(a, b, p) == [0, 5, 7, 4]
    c, slices = priority_schedule(a, b, p, preemptive=True)
    assert slices == [(0, 0, 1), (1, 1, 3), (0, 3, 4), (3, 4, 5), (0, 5, 9), (2, 9, 12)]
    assert waiting_times(a, b, p, preemptive=True) == [3, 0, 7, 0]


def test_starvation() -> None:
    # A low-priority process at time 0 and a stream of K high-priority ones.
    for k in (1, 5, 50):
        a = [0] + [2 * j for j in range(k)]
        b = [3] + [2] * k
        p = [9] + [1] * k
        for pre in (False, True):
            _, slices = priority_schedule(a, b, p, pre)
            first_low = min(s for i, s, _ in slices if i == 0)
            if pre:
                assert first_low == 2 * k  # waits for the whole stream
            else:
                assert first_low in (0, 2 * k)
    # Nonpreemptive: the low process starts first only because it is alone at 0.
    a, b, p = [1] + [2 * j for j in range(50)], [3] + [2] * 50, [9] + [1] * 50
    for pre in (False, True):
        _, slices = priority_schedule(a, b, p, pre)
        assert min(s for i, s, _ in slices if i == 0) == 100


def test_equal_priority_does_not_preempt() -> None:
    _, slices = priority_schedule([0, 1], [5, 1], [2, 2], preemptive=True)
    assert slices == [(0, 0, 5), (1, 5, 6)]


def test_burst_as_priority_is_sjf() -> None:
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randrange(1, 9)
        b = [rng.randrange(1, 10) for _ in range(n)]
        _, slices = priority_schedule([0] * n, b, b)
        assert [i for i, _, _ in slices] == sorted(range(n), key=lambda i: (b[i], i))


def unit_step(arrival: list, burst: list, priority: list, preemptive: bool) -> list:
    """Reference simulator in unit time steps, integer data only."""
    n = len(arrival)
    left = list(burst)
    done = [None] * n
    t, cur = 0, None
    while any(left):
        ready = [j for j in range(n) if arrival[j] <= t and left[j] > 0]
        if cur is None or preemptive:
            cur = min(ready, key=lambda j: (priority[j], arrival[j], j)) if ready else None
        if cur is not None:
            left[cur] -= 1
            if left[cur] == 0:
                done[cur] = t + 1
                cur = None
        t += 1
    return done


def test_against_unit_step_reference() -> None:
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randrange(1, 9)
        a = [rng.randrange(0, 15) for _ in range(n)]
        b = [rng.randrange(1, 8) for _ in range(n)]
        p = [rng.randrange(0, 4) for _ in range(n)]
        for pre in (False, True):
            c, slices = priority_schedule(a, b, p, pre)
            assert c == unit_step(a, b, p, pre)
            assert len(slices) <= 2 * n - 1
            prev = 0
            for i, s, e in slices:
                assert s >= prev and s >= a[i] and e > s
                prev = e


def test_fraction_times() -> None:
    a = [Fraction(0), Fraction(1, 2), Fraction(3, 4)]
    b = [Fraction(2), Fraction(1, 3), Fraction(1, 4)]
    c, _ = priority_schedule(a, b, [2, 0, 1], preemptive=True)
    assert c == [Fraction(31, 12), Fraction(5, 6), Fraction(13, 12)]
