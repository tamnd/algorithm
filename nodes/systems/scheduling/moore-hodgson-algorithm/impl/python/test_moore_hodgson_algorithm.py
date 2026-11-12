# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moore-hodgson-algorithm/. The authors are listed in prov/KEY8Q5.jsonl.

import itertools
import random

from moore_hodgson_algorithm import all_on_time, moore_hodgson_algorithm, moore_original


def late_count(p, d, order):
    t = 0
    late = 0
    for j in order:
        t += p[j]
        late += t > d[j]
    return late


def best_by_subsets(p, d):
    """The largest set of jobs that can all be on time, by a search over all 2^n subsets."""
    n = len(p)
    best = 0
    for mask in range(1 << n):
        jobs = [j for j in range(n) if mask >> j & 1]
        if len(jobs) > best and all_on_time(p, d, jobs):
            best = len(jobs)
    return best


def test_example() -> None:
    p = [3, 2, 4, 1, 6, 2, 3]
    d = [4, 5, 8, 9, 12, 13, 14]
    on_time, late = moore_hodgson_algorithm(p, d)
    assert on_time == [0, 1, 3, 5, 6] and late == [2, 4]
    assert late_count(p, d, on_time + late) == 2
    assert best_by_subsets(p, d) == 5
    assert late_count(p, d, range(7)) == 5  # EDD alone


def test_edges() -> None:
    assert moore_hodgson_algorithm([], []) == ([], [])
    assert moore_hodgson_algorithm([3], [2]) == ([], [0])
    assert moore_hodgson_algorithm([3], [3]) == ([0], [])
    assert moore_hodgson_algorithm([0, 0], [0, 0]) == ([0, 1], [])
    # a common due date: keep the shortest jobs
    on_time, late = moore_hodgson_algorithm([4, 1, 3, 2], [5, 5, 5, 5])
    assert sorted(on_time) == [1, 3] and sorted(late) == [0, 2]


def test_against_subsets() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randrange(0, 11)
        p = [rng.randrange(0, 8) for _ in range(n)]
        d = [rng.randrange(0, 25) for _ in range(n)]
        on_time, late = moore_hodgson_algorithm(p, d)
        assert sorted(on_time + late) == list(range(n))
        assert all_on_time(p, d, on_time)
        assert len(on_time) == best_by_subsets(p, d)


def test_against_all_orders() -> None:
    rng = random.Random(5)
    for _ in range(150):
        n = rng.randrange(1, 7)
        p = [rng.randrange(1, 7) for _ in range(n)]
        d = [rng.randrange(1, 20) for _ in range(n)]
        on_time, late = moore_hodgson_algorithm(p, d)
        best = min(late_count(p, d, o) for o in itertools.permutations(range(n)))
        assert late_count(p, d, on_time + late) == best == len(late)


def test_same_count_as_moore_original() -> None:
    rng = random.Random(9)
    for _ in range(300):
        n = rng.randrange(0, 30)
        p = [rng.randrange(1, 10) for _ in range(n)]
        d = [rng.randrange(1, 60) for _ in range(n)]
        on_time, _ = moore_hodgson_algorithm(p, d)
        assert len(on_time) == len(moore_original(p, d))


def test_kept_set_has_least_total_time() -> None:
    # among the largest on-time sets, the algorithm keeps one of least total processing time
    rng = random.Random(13)
    for _ in range(200):
        n = rng.randrange(1, 10)
        p = [rng.randrange(1, 8) for _ in range(n)]
        d = [rng.randrange(1, 25) for _ in range(n)]
        on_time, _ = moore_hodgson_algorithm(p, d)
        best = None
        for mask in range(1 << n):
            jobs = [j for j in range(n) if mask >> j & 1]
            if len(jobs) == len(on_time) and all_on_time(p, d, jobs):
                s = sum(p[j] for j in jobs)
                best = s if best is None else min(best, s)
        assert sum(p[j] for j in on_time) == best


def test_dropping_the_new_job_is_wrong() -> None:
    # the rule "reject each job that would be late" keeps only 4 jobs of the example
    p = [3, 2, 4, 1, 6, 2, 3]
    d = [4, 5, 8, 9, 12, 13, 14]
    t, kept = 0, []
    for j in range(7):
        if t + p[j] <= d[j]:
            t += p[j]
            kept.append(j)
    assert kept == [0, 1, 3, 4]
    assert len(moore_hodgson_algorithm(p, d)[0]) == 5
