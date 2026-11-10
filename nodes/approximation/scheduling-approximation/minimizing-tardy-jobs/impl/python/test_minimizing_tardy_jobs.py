# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimizing-tardy-jobs/. The authors are listed in prov/192FEE.jsonl.

import itertools
import random

from minimizing_tardy_jobs import is_feasible, moore_hodgson, tardy_count


def best_by_orders(p, d):
    return min(tardy_count(p, d, o) for o in itertools.permutations(range(len(p))))


def best_by_subsets(p, d):
    n = len(p)
    best = 0
    for mask in range(1 << n):
        jobs = [j for j in range(n) if mask >> j & 1]
        if len(jobs) > best and is_feasible(p, d, jobs):
            best = len(jobs)
    return n - best


def check(p, d):
    on_time, late = moore_hodgson(p, d)
    assert sorted(on_time + late) == list(range(len(p)))
    assert is_feasible(p, d, on_time)
    assert tardy_count(p, d, on_time + late) == len(late)
    return len(late)


def test_page_example() -> None:
    p = [4, 3, 2, 6, 1, 5, 2]
    d = [5, 6, 7, 10, 12, 14, 15]
    on_time, late = moore_hodgson(p, d)
    assert on_time == [1, 2, 4, 5, 6] and late == [0, 3]
    assert best_by_orders(p, d) == 2


def test_dropping_the_current_job_fails() -> None:
    p, d = [6, 3, 4], [6, 7, 8]
    # keeping job 0 makes jobs 1 and 2 late
    assert tardy_count(p, d, [0, 1, 2]) == 2
    assert moore_hodgson(p, d) == ([1, 2], [0])


def test_against_orders() -> None:
    rng = random.Random(51)
    for _ in range(300):
        n = rng.randint(1, 6)
        p = [rng.randint(0, 7) for _ in range(n)]
        d = [rng.randint(-2, 20) for _ in range(n)]
        assert check(p, d) == best_by_orders(p, d)


def test_against_subsets() -> None:
    rng = random.Random(52)
    for _ in range(200):
        n = rng.randint(1, 10)
        p = [rng.randint(1, 9) for _ in range(n)]
        d = [rng.randint(0, 6 * n) for _ in range(n)]
        assert check(p, d) == best_by_subsets(p, d)


def test_edges() -> None:
    assert moore_hodgson([], []) == ([], [])
    assert moore_hodgson([3], [2]) == ([], [0])
    on_time, late = moore_hodgson([2, 2], [2, 2])
    assert len(on_time) == 1 and len(late) == 1
