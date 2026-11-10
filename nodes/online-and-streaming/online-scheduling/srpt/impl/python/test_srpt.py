# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/srpt/. The authors are listed in prov/1YRN1P.jsonl.

import random
from fractions import Fraction
from functools import lru_cache

from srpt import srpt, total_flow_time


def brute_force_flow(jobs: list[tuple[int, int]]) -> int:
    """Optimal total flow time over all schedules that change jobs only at integer times.

    Each unit slot runs one released, unfinished job, or idles.
    """
    n = len(jobs)
    horizon = max(r for r, _ in jobs) + sum(p for _, p in jobs)

    @lru_cache(maxsize=None)
    def best(t: int, rem: tuple[int, ...]) -> int:
        if all(q == 0 for q in rem):
            return 0
        if t >= horizon:
            return 10**9
        out = best(t + 1, rem)  # idle in [t, t + 1)
        for j in range(n):
            if rem[j] > 0 and jobs[j][0] <= t:
                nxt = list(rem)
                nxt[j] -= 1
                extra = (t + 1 - jobs[j][0]) if nxt[j] == 0 else 0
                out = min(out, extra + best(t + 1, tuple(nxt)))
        return out

    return best(0, tuple(p for _, p in jobs))


def check_schedule(jobs, completion, pieces) -> None:
    work = [0] * len(jobs)
    last_end = 0
    for a, b, j in pieces:
        assert a >= last_end and b > a
        assert a >= jobs[j][0]
        work[j] += b - a
        last_end = b
    assert work == [p for _, p in jobs]
    for j in range(len(jobs)):
        assert completion[j] == max(b for a, b, k in pieces if k == j)


def test_example() -> None:
    jobs = [(0, 5), (1, 2), (2, 4), (3, 1)]
    completion, pieces = srpt(jobs)
    assert pieces == [(0, 1, 0), (1, 3, 1), (3, 4, 3), (4, 8, 0), (8, 12, 2)]
    assert completion == [8, 3, 12, 4]
    assert total_flow_time(jobs, completion) == 21


def test_edges() -> None:
    assert srpt([]) == ([], [])
    assert srpt([(3, 2)]) == ([5], [(3, 5, 0)])
    completion, pieces = srpt([(0, 1), (5, 1)])
    assert completion == [1, 6] and pieces == [(0, 1, 0), (5, 6, 1)]
    completion, _ = srpt([(0, 2), (0, 2), (0, 2)])
    assert sorted(completion) == [2, 4, 6]


def test_optimal_against_brute_force() -> None:
    rng = random.Random(1968)
    for _ in range(300):
        n = rng.randint(1, 4)
        jobs = [(rng.randint(0, 4), rng.randint(1, 3)) for _ in range(n)]
        completion, pieces = srpt(jobs)
        check_schedule(jobs, completion, pieces)
        assert total_flow_time(jobs, completion) == brute_force_flow(jobs)


def test_preemptions_and_integral() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(1, 8)
        jobs = [(Fraction(rng.randint(0, 20), 2), Fraction(rng.randint(1, 12), 3)) for _ in range(n)]
        completion, pieces = srpt(jobs)
        check_schedule(jobs, completion, pieces)
        assert len(pieces) - n <= max(0, n - 1)
        events = sorted({r for r, _ in jobs} | set(completion))
        integral = 0
        for a, b in zip(events, events[1:]):
            alive = sum(1 for j in range(n) if jobs[j][0] <= a < completion[j])
            integral += alive * (b - a)
        assert integral == total_flow_time(jobs, completion)


def test_starvation_of_long_job() -> None:
    k = 20
    jobs = [(0, 3)] + [(i, 1) for i in range(1, k + 1)]
    completion, _ = srpt(jobs)
    assert completion[0] - jobs[0][0] == k + 3
    fifo_end, fifo_max = 0, 0
    for r, p in jobs:
        fifo_end = max(fifo_end, r) + p
        fifo_max = max(fifo_max, fifo_end - r)
    assert fifo_max == 3
