# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/round-robin/. The authors are listed in prov/EHJG6W.jsonl.

import random
from fractions import Fraction

from round_robin import (mean_turnaround, processor_sharing, response_times, round_robin,
                         waiting_times)


def merged(slices: list) -> list:
    """Join consecutive slices of the same process."""
    out = []
    for i, s, e in slices:
        if out and out[-1][0] == i and out[-1][2] == s:
            out[-1] = (i, out[-1][1], e)
        else:
            out.append((i, s, e))
    return out


def test_textbook_example() -> None:
    c, slices = round_robin([0, 0, 0], [24, 3, 3], 4)
    assert merged(slices) == [(0, 0, 4), (1, 4, 7), (2, 7, 10), (0, 10, 30)]
    assert waiting_times([0, 0, 0], [24, 3, 3], 4) == [6, 4, 7]  # mean 17/3


def test_hand_worked_gantt() -> None:
    a = [0, 1, 2, 3, 6]  # A B C D E
    b = [5, 3, 1, 2, 4]
    c, slices = round_robin(a, b, 2)
    assert merged(slices) == [(0, 0, 2), (1, 2, 4), (2, 4, 5), (0, 5, 7), (3, 7, 9),
                              (1, 9, 10), (4, 10, 12), (0, 12, 13), (4, 13, 15)]
    assert c == [13, 10, 5, 9, 15]
    assert waiting_times(a, b, 2) == [8, 6, 2, 4, 5]
    assert response_times(a, b, 2) == [0, 1, 2, 4, 4]
    # FCFS on the same input
    assert round_robin(a, b, 5)[0] == [5, 8, 9, 11, 15]
    assert sum(response_times(a, b, 5)) == 21


def test_turnaround_depends_on_q() -> None:
    got = [mean_turnaround([0] * 4, [6, 3, 1, 7], q) for q in range(1, 8)]
    assert got == [11, Fraction(23, 2), Fraction(43, 4), Fraction(23, 2), Fraction(49, 4),
                   Fraction(21, 2), Fraction(21, 2)]


def fcfs(arrival: list, burst: list) -> list:
    t, out = 0, [None] * len(arrival)
    for i in sorted(range(len(arrival)), key=lambda i: (arrival[i], i)):
        t = max(t, arrival[i]) + burst[i]
        out[i] = t
    return out


def test_large_quantum_is_fcfs() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randrange(1, 9)
        a = [rng.randrange(0, 15) for _ in range(n)]
        b = [rng.randrange(1, 10) for _ in range(n)]
        assert round_robin(a, b, max(b))[0] == fcfs(a, b)


def test_wait_bound_between_slices() -> None:
    # A process that joins the queue with m - 1 processes ahead starts
    # its next slice within (m - 1)(q + s) + s.
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randrange(1, 9)
        a = [rng.randrange(0, 20) for _ in range(n)]
        b = [rng.randrange(1, 12) for _ in range(n)]
        q = rng.randrange(1, 5)
        s = rng.choice([0, 0, 1])
        _, slices = round_robin(a, b, q, s)
        # rebuild the queue to know how many were ahead at each join
        ends = {}
        for idx, (i, st, e) in enumerate(slices):
            ends.setdefault(i, []).append((st, e))
        for i in range(n):
            runs = ends[i]
            for (s1, e1), (s2, _) in zip(runs, runs[1:]):
                ahead = len({j for j, st, e in slices if j != i and e1 <= st < s2})
                assert ahead <= n - 1
                assert s2 - e1 <= ahead * (q + s) + s
        if s == 0 and all(x == 0 for x in a):
            for i in range(n):
                runs = ends[i]
                for (s1, e1), (s2, _) in zip(runs, runs[1:]):
                    assert s2 - e1 <= (n - 1) * q


def test_all_present_bound_n_minus_1_q() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randrange(1, 9)
        b = [rng.randrange(1, 20) for _ in range(n)]
        q = rng.randrange(1, 6)
        _, slices = round_robin([0] * n, b, q)
        last_end = {}
        for i, s, e in slices:
            assert s - last_end.get(i, 0) <= (n - 1) * q
            last_end[i] = e


def test_switch_overhead_fraction() -> None:
    n, q, s = 4, 3, 1
    c, slices = round_robin([0] * n, [30] * n, q, s)
    assert c[-1] == n * 30 + len(slices) * s  # every slice is a switch
    assert Fraction(len(slices) * s, c[-1]) == Fraction(s, q + s)


def test_processor_sharing_limit() -> None:
    b = [6, 3, 1, 7]
    assert processor_sharing(b) == [16, 10, 4, 17]
    for m in (1, 2, 4, 8, 16, 64):
        q = Fraction(1, m)
        c, _ = round_robin([0] * 4, b, q)
        assert c == [16 - q, 10 - q, 4 - q, 17]
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randrange(1, 6)
        b = [Fraction(rng.randrange(1, 40), rng.randrange(1, 5)) for _ in range(n)]
        ps = processor_sharing(b)
        for m in (1, 3, 10):
            q = Fraction(1, m)
            c, _ = round_robin([0] * n, b, q)
            assert all(abs(x - y) <= (n - 1) * q for x, y in zip(c, ps))


def test_schedule_is_valid() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randrange(1, 9)
        a = [rng.randrange(0, 20) for _ in range(n)]
        b = [rng.randrange(1, 10) for _ in range(n)]
        q = rng.randrange(1, 5)
        c, slices = round_robin(a, b, q)
        got = [0] * n
        prev_end = 0
        for i, s, e in slices:
            assert s >= prev_end and s >= a[i] and 0 < e - s <= q
            got[i] += e - s
            prev_end = e
        assert got == b
        assert all(c[i] == max(e for j, _, e in slices if j == i) for i in range(n))
