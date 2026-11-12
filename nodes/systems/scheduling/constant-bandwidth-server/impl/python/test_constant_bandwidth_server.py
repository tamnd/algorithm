# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constant-bandwidth-server/. The authors are listed in prov/P5NM45.jsonl.

import random
from fractions import Fraction
from math import lcm

from constant_bandwidth_server import cbs_schedule


def test_figure_one_trace() -> None:
    # Hard task (2, 3) and a CBS with Q = 2, T = 7; soft jobs at 2, 7 and 17.
    r = cbs_schedule([(2, 3)], [(2, 7)], [[(2, 3), (7, 2), (17, 1)]], 21)
    assert r.servers[0].log == [
        (2, "new", 9), (6, "recharge", 16), (12, "recharge", 23), (17, "keep", 23), (18, "recharge", 30),
    ]
    assert r.soft_finish == [[9, 15, 18]]
    assert r.hard_misses == [] and r.invariant_ok


def test_overrun_is_isolated() -> None:
    hard = [(2, 3)]
    reqs = [[(0, 12)]]
    plain = cbs_schedule(hard, [(2, 7)], reqs, 21, cbs=False)
    assert plain.hard_misses
    r = cbs_schedule(hard, [(2, 7)], reqs, 21)
    assert r.hard_misses == [] and r.invariant_ok
    assert r.soft_finish == [[None]] or r.soft_finish[0][0] > 7


def test_random_isolation_when_total_bandwidth_at_most_one() -> None:
    rng = random.Random(12)
    plain_missed = 0
    for _ in range(250):
        hard = [(rng.randint(1, 3), rng.choice([4, 5, 6, 8, 10])) for _ in range(rng.randint(1, 3))]
        servers = [(rng.randint(1, 3), rng.choice([5, 6, 7, 9])) for _ in range(rng.randint(1, 2))]
        total = sum(Fraction(c, t) for c, t in hard + servers)
        if total > 1:
            continue
        h = lcm(*(t for _, t in hard))
        reqs = [sorted((rng.randint(0, 2 * h), rng.randint(1, 15)) for _ in range(rng.randint(1, 6)))
                for _ in servers]
        r = cbs_schedule(hard, servers, reqs, 2 * h)
        assert r.hard_misses == [] and r.invariant_ok
        for sv in r.servers:
            ds = [d for _, _, d in sv.log]
            assert ds == sorted(ds)
        if cbs_schedule(hard, servers, reqs, 2 * h, cbs=False).hard_misses:
            plain_missed += 1
    assert plain_missed > 0


def test_lemma_hard_task_in_its_own_server() -> None:
    # A hard task (C, T) served by a CBS with Q = C and T_s = T behaves like the task itself.
    rng = random.Random(2)
    for _ in range(150):
        c, t = rng.randint(1, 3), rng.choice([4, 6, 8])
        other = [(rng.randint(1, 2), rng.choice([4, 5, 8]))]
        if Fraction(c, t) + sum(Fraction(a, b) for a, b in other) > 1:
            continue
        h = lcm(t, *(b for _, b in other))
        reqs = [[(k * t, c) for k in range(2 * h // t)]]
        r = cbs_schedule(other, [(c, t)], reqs, 2 * h)
        assert r.hard_misses == []
        for k, f in enumerate(r.soft_finish[0]):
            assert f is not None and f <= (k + 1) * t


def test_edges() -> None:
    r = cbs_schedule([], [(1, 2)], [[]], 5)
    assert r.timeline == [None] * 5 and r.invariant_ok
