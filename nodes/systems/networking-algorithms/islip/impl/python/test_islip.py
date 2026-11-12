# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/islip/. The authors are listed in prov/QBWMZS.jsonl.

import itertools
import random

from islip import Scheduler, bernoulli_run, saturated_run


def is_matching(req: list[list[bool]], match: list[int]) -> bool:
    used = [j for j in match if j >= 0]
    return len(used) == len(set(used)) and all(req[i][j] for i, j in enumerate(match) if j >= 0)


def test_trace_from_equal_pointers() -> None:
    sched = Scheduler(4)
    full = [[True] * 4 for _ in range(4)]
    got = []
    for _ in range(5):
        got.append((sched.schedule(full), list(sched.g)))
    assert got == [
        ([0, -1, -1, -1], [1, 0, 0, 0]),
        ([1, 0, -1, -1], [2, 1, 0, 0]),
        ([2, 1, 0, -1], [3, 2, 1, 0]),
        ([3, 2, 1, 0], [0, 3, 2, 1]),
        ([0, 3, 2, 1], [1, 0, 3, 2]),
    ]


def test_returns_a_matching_and_is_maximal_with_n_iterations() -> None:
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randrange(1, 7)
        sched = Scheduler(n, iterations=n)
        sched.g = [rng.randrange(n) for _ in range(n)]
        sched.a = [rng.randrange(n) for _ in range(n)]
        req = [[rng.random() < 0.4 for _ in range(n)] for _ in range(n)]
        m = sched.schedule(req)
        assert is_matching(req, m)
        taken = set(j for j in m if j >= 0)
        assert not any(m[i] < 0 and req[i][j] and j not in taken for i in range(n) for j in range(n))


def test_pointers_desynchronize_within_n_minus_one_slots() -> None:
    n = 4
    full = [[True] * n for _ in range(n)]
    worst = 0
    for g in itertools.product(range(n), repeat=n):
        for a in ((0, 0, 0, 0), (1, 2, 3, 0), (3, 3, 1, 0)):
            sched = Scheduler(n)
            sched.g, sched.a = list(g), list(a)
            t = 0
            while len(set(sched.g)) < n:
                sched.schedule(full)
                t += 1
            worst = max(worst, t)
            # Once distinct, the pointers stay distinct and each slot is perfect.
            for _ in range(3):
                assert sum(1 for j in sched.schedule(full) if j >= 0) == n
                assert len(set(sched.g)) == n
    assert worst == n - 1


def test_saturated_throughput_islip_against_rrm() -> None:
    for n in (2, 16):
        islip = saturated_run(Scheduler(n), 1000)
        rrm = saturated_run(Scheduler(n, rrm=True), 1000)
        assert all(size == n for size in islip[n - 1:])
        assert all(size == 1 for size in rrm)  # RRM pointers stay in lock step


def test_uniform_full_load_throughput_tends_to_one() -> None:
    n = 16
    sched = Scheduler(n)
    q = [[0] * n for _ in range(n)]
    rng = random.Random(3)
    a1, d1, _ = bernoulli_run(sched, 1.0, 3000, rng, q)
    a2, d2, _ = bernoulli_run(sched, 1.0, 3000, rng, q)  # the same run goes on
    assert d1 / (n * 3000) < d2 / (n * 3000)
    assert d2 / (n * 3000) > 0.95
    assert len(set(sched.g)) == n


def test_rrm_is_unstable_where_islip_is_stable() -> None:
    n = 16
    a, d, left = bernoulli_run(Scheduler(n, rrm=True), 0.7, 3000, random.Random(3))
    assert d / a < 0.85 and left > 0.15 * a
    a, d, left = bernoulli_run(Scheduler(n), 0.7, 3000, random.Random(3))
    assert d / a > 0.99
