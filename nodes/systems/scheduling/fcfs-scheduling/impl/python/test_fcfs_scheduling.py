# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fcfs-scheduling/. The authors are listed in prov/TCCY97.jsonl.

import random
from fractions import Fraction

from fcfs_scheduling import average_waiting, fcfs


def test_convoy_silberschatz() -> None:
    # bursts 24, 3, 3 all at time 0: waits 0, 24, 27, mean 17
    assert fcfs([0, 0, 0], [24, 3, 3]) == ([0, 24, 27], [24, 27, 30])
    assert average_waiting([0, 0, 0], [24, 3, 3]) == 17
    # the order 3, 3, 24: waits 0, 3, 6, mean 3
    assert average_waiting([0, 0, 0], [3, 3, 24]) == 3


def test_page_example() -> None:
    arrival = [0, 1, 2, 3, 20, 21]
    burst = [5, 3, 8, 2, 3, 1]
    start, completion = fcfs(arrival, burst)
    assert start == [0, 5, 8, 16, 20, 23]
    assert completion == [5, 8, 16, 18, 23, 24]
    assert average_waiting(arrival, burst) == Fraction(4 + 6 + 13 + 0 + 2, 6)


def test_edges() -> None:
    assert fcfs([], []) == ([], [])
    assert fcfs([7], [2]) == ([7], [9])
    assert fcfs([0, 0, 0], [1, 1, 1]) == ([0, 1, 2], [1, 2, 3])
    assert fcfs([5, 0], [1, 1]) == ([5, 0], [6, 1])  # input order is not arrival order
    assert fcfs([Fraction(1, 2)], [Fraction(1, 3)]) == ([Fraction(1, 2)], [Fraction(5, 6)])


def test_convoy_formula() -> None:
    # one long job of length L before k short jobs of length s, all at time 0
    for L in range(1, 30):
        for s in range(1, 5):
            for k in range(0, 6):
                bursts = [L] + [s] * k
                want = Fraction(k * L + s * k * (k - 1) // 2, k + 1)
                assert average_waiting([0] * (k + 1), bursts) == want
                short_first = Fraction(s * k * (k + 1) // 2, k + 1)
                assert average_waiting([0] * (k + 1), [s] * k + [L]) == short_first


def oracle(arrival: list, burst: list) -> list:
    """Unit-step simulation with an explicit FIFO ready queue (integer times)."""
    n, t, done = len(arrival), 0, [None] * len(arrival)
    queue, running, left, admitted = [], None, 0, set()
    while any(c is None for c in done):
        for i in sorted(range(n), key=lambda i: (arrival[i], i)):
            if arrival[i] <= t and i not in admitted:
                admitted.add(i)
                queue.append(i)
        if running is None and queue:
            running, left = queue.pop(0), None
            left = burst[running]
        if running is not None:
            left -= 1
            if left == 0:
                done[running] = t + 1
                running = None
        t += 1
    return done


def test_against_oracle() -> None:
    rng = random.Random(42)
    for _ in range(600):
        n = rng.randrange(1, 8)
        arrival = [rng.randrange(15) for _ in range(n)]
        burst = [rng.randrange(1, 6) for _ in range(n)]
        _, completion = fcfs(arrival, burst)
        assert completion == oracle(arrival, burst)


def test_work_conserving_and_order() -> None:
    rng = random.Random(9)
    for _ in range(500):
        n = rng.randrange(1, 8)
        arrival = [rng.randrange(20) for _ in range(n)]
        burst = [rng.randrange(1, 6) for _ in range(n)]
        start, completion = fcfs(arrival, burst)
        order = sorted(range(n), key=lambda i: start[i])
        assert order == sorted(range(n), key=lambda i: (arrival[i], i))
        for x, y in zip(order, order[1:]):
            assert start[y] == max(completion[x], arrival[y])  # idle only if nobody waits
