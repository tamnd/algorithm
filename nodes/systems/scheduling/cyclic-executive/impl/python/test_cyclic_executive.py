# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclic-executive/. The authors are listed in prov/WJY423.jsonl.

import itertools
import random
from fractions import Fraction
from math import gcd, lcm

from cyclic_executive import admissible_frames, assign, cyclic_executive_plan, jobs_of, run_table

EXAMPLE = [(4, 1, 4), (5, Fraction(9, 5), 5), (20, 1, 20), (20, 2, 20)]


def check_plan(tasks, f, table, jobs) -> None:
    h = lcm(*(t for t, _, _ in tasks))
    assert f * len(table) == h
    assert sorted(j for fr in table for j in fr) == list(range(len(jobs)))
    for k, fr in enumerate(table):
        assert sum(jobs[j][2] for j in fr) <= f
    runs = run_table(f, table, jobs, cycles=2)
    for (s1, e1, _), (s2, _, _) in zip(runs, runs[1:]):
        assert e1 <= s2
    for s, e, j in runs:
        r, d, c, _ = jobs[j]
        m = s // h
        assert m * h + r <= s and e <= m * h + d and e - s == c


def test_example() -> None:
    assert lcm(4, 5, 20) == 20
    assert admissible_frames(EXAMPLE) == [2]
    f, table, jobs = cyclic_executive_plan(EXAMPLE)
    assert f == 2 and len(jobs) == 11
    check_plan(EXAMPLE, f, table, jobs)
    names = [[f"T{jobs[j][3] + 1}" for j in fr] for fr in table]
    assert names == [["T1", "T3"], ["T2"], ["T1"], ["T2"], ["T1"], ["T2"], ["T1"], ["T4"], ["T2"], ["T1"]]
    assert [sum(jobs[j][2] for j in fr) for fr in table] == [2, Fraction(9, 5), 1, Fraction(9, 5), 1,
                                                             Fraction(9, 5), 1, 2, Fraction(9, 5), 1]


def test_no_frame_without_splitting() -> None:
    tasks = [(4, 1, 4), (5, 2, 7), (20, 5, 20)]
    assert admissible_frames(tasks) == []
    assert cyclic_executive_plan(tasks) is None
    split = [(4, 1, 4), (5, 2, 7), (20, 1, 20), (20, 3, 20), (20, 1, 20)]
    assert admissible_frames(split) == [4]
    f, table, jobs = cyclic_executive_plan(split)
    check_plan(split, f, table, jobs)
    where = {jobs[j][3]: k for k, fr in enumerate(table) for j in fr if jobs[j][3] >= 2}
    assert where == {2: 0, 3: 1, 4: 2}


def test_third_constraint_is_exact() -> None:
    for t in range(1, 25):
        for f in range(1, 25):
            for d in range(1, t + 1):
                ok = all(
                    any(m * f >= k * t and (m + 1) * f <= k * t + d for m in range(k * t // f, k * t // f + 3))
                    for k in range(f + 1)
                )
                assert ok == (2 * f - gcd(t, f) <= d)


def brute(jobs, f, frames) -> bool:
    choices = []
    for r, d, _, _ in jobs:
        choices.append([k for k in range(frames) if k * f >= r and (k + 1) * f <= d])
    for pick in itertools.product(*choices):
        load = [0] * frames
        for (_, _, c, _), k in zip(jobs, pick):
            load[k] += c
        if max(load, default=0) <= f:
            return True
    return False


def test_random_against_brute_force() -> None:
    rng = random.Random(5)
    found = missed = 0
    for _ in range(500):
        tasks = []
        for _ in range(rng.randint(1, 3)):
            t = rng.choice([2, 3, 4, 6, 8, 12])
            tasks.append((t, rng.randint(1, max(1, t // 2)), rng.randint(max(1, t // 2), t)))
        h = lcm(*(t for t, _, _ in tasks))
        jobs = jobs_of(tasks)
        if len(jobs) > 9:
            continue
        for f in range(1, h + 1):
            if h % f == 0:
                want = (f >= max(c for _, c, _ in tasks) and any(t % f == 0 for t, _, _ in tasks)
                        and all(2 * f - gcd(t, f) <= d for t, _, d in tasks))
                assert (f in admissible_frames(tasks)) == want
        plan = cyclic_executive_plan(tasks)
        exists = any(brute(jobs, f, h // f) for f in admissible_frames(tasks))
        assert (plan is not None) == exists
        if plan:
            found += 1
            check_plan(tasks, *plan)
            assert assign(jobs, plan[0], h // plan[0]) is not None
        else:
            missed += 1
    assert found > 50 and missed > 20
