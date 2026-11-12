# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shortest-job-first/. The authors are listed in prov/GK26MR.jsonl.

import itertools
import random
from fractions import Fraction

from shortest_job_first import predict, sjf

A = [0, 2, 4, 5, 6, 20]
B = [7, 4, 1, 4, 2, 3]


def waits(arrival: list, start: list) -> int:
    return sum(s - a for s, a in zip(start, arrival))


def test_silberschatz_all_at_zero() -> None:
    start, completion = sjf([0, 0, 0, 0], [6, 8, 7, 3])
    assert start == [3, 16, 9, 0]
    assert Fraction(sum(start), 4) == 7


def test_page_example() -> None:
    start, completion = sjf(A, B)
    assert start == [0, 10, 7, 14, 8, 20]
    assert completion == [7, 14, 8, 18, 10, 23]
    assert waits(A, start) == 22  # mean 11/3; FCFS gives 29/6


def test_misprediction() -> None:
    start, _ = sjf(A, B, predicted=[7, 4, 6, 1, 2, 3])
    assert start == [0, 13, 17, 7, 11, 20]
    assert waits(A, start) == 31


def test_exponential_average_silberschatz() -> None:
    taus = predict([6, 4, 6, 4, 13, 13, 13], Fraction(1, 2), 10)
    assert taus == [10, 8, 6, 6, 5, 9, 11, 12]


def test_exponential_average_closed_form() -> None:
    rng = random.Random(4)
    for _ in range(300):
        alpha = Fraction(rng.randrange(0, 9), 8)
        ts = [rng.randrange(1, 30) for _ in range(rng.randrange(0, 8))]
        tau0 = rng.randrange(1, 30)
        taus = predict(ts, alpha, tau0)
        m = len(ts)
        closed = sum(alpha * (1 - alpha) ** j * ts[m - 1 - j] for j in range(m)) + (1 - alpha) ** m * tau0
        assert taus[-1] == closed
    assert predict([5, 9], Fraction(0), 3) == [3, 3, 3]  # alpha 0: history ignored
    assert predict([5, 9], Fraction(1), 3) == [3, 5, 9]  # alpha 1: last burst only


def test_edges() -> None:
    assert sjf([], []) == ([], [])
    assert sjf([3], [2]) == ([3], [5])
    assert sjf([0, 0, 0], [2, 2, 2]) == ([0, 2, 4], [2, 4, 6])  # ties by index


def test_not_optimal_with_arrivals() -> None:
    # a long job at 0 and a short one at 1: SJF cannot wait for the short one
    start, _ = sjf([0, 1], [10, 1])
    assert waits([0, 1], start) == 9
    assert waits([0, 1], [2, 1]) == 2  # idle on [0, 1), then the short job


def test_starvation() -> None:
    # short jobs of length 2 arrive at 0, 2, 4, ...; a job of length 5 arrives at 1
    m = 50
    arrival = [2 * k for k in range(m)] + [1]
    burst = [2] * m + [5]
    start, _ = sjf(arrival, burst)
    assert start[m] == 2 * m  # it runs only when the stream stops


def reference(arrival: list, burst: list) -> list:
    """Plain O(n^2) scan: at each free moment take the arrived job of least (burst, arrival, index)."""
    n, t, left, start = len(arrival), 0, set(range(len(arrival))), [None] * len(arrival)
    while left:
        t = max(t, min(arrival[i] for i in left))
        i = min((i for i in left if arrival[i] <= t), key=lambda i: (burst[i], arrival[i], i))
        start[i] = t
        t += burst[i]
        left.remove(i)
    return start


def test_against_reference() -> None:
    rng = random.Random(17)
    for _ in range(800):
        n = rng.randrange(1, 9)
        arrival = [rng.randrange(12) for _ in range(n)]
        burst = [rng.randrange(1, 7) for _ in range(n)]
        assert sjf(arrival, burst)[0] == reference(arrival, burst)


def test_optimal_at_time_zero() -> None:
    rng = random.Random(23)
    for _ in range(300):
        n = rng.randrange(1, 7)
        burst = [rng.randrange(1, 10) for _ in range(n)]
        best = min(sum(sum(burst[j] for j in p[:k]) for k in range(n))
                   for p in itertools.permutations(range(n)))
        assert sum(sjf([0] * n, burst)[0]) == best
