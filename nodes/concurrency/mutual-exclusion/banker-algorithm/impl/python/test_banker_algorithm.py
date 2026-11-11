# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/banker-algorithm/. The authors are listed in prov/47TX1V.jsonl.
import itertools
import random

from banker_algorithm import Banker, build, is_safe
from procsim import explore


def brute_safe(avail, alloc, need):
    """Try every order of the processes."""
    n, m = len(alloc), len(avail)
    for perm in itertools.permutations(range(n)):
        work = list(avail)
        for i in perm:
            if any(need[i][r] > work[r] for r in range(m)):
                break
            work = [work[r] + alloc[i][r] for r in range(m)]
        else:
            return True
    return False


def random_state(rng, n, m):
    total = [rng.randint(1, 4) for _ in range(m)]
    maximum = [[rng.randint(0, t) for t in total] for _ in range(n)]
    alloc = [[0] * m for _ in range(n)]
    for r in range(m):
        for _ in range(rng.randint(0, total[r])):
            i = rng.randrange(n)
            if alloc[i][r] < maximum[i][r]:
                alloc[i][r] += 1
    avail = [total[r] - sum(row[r] for row in alloc) for r in range(m)]
    need = [[maximum[i][r] - alloc[i][r] for r in range(m)] for i in range(n)]
    return avail, alloc, need


def test_page_example():
    b = Banker([3, 3], [[2, 2], [2, 1], [1, 3]])
    for i, x in enumerate([[1, 0], [1, 1], [0, 1]]):
        b.alloc[i], b.need[i] = list(x), [b.maximum[i][r] - x[r] for r in range(2)]
    b.avail = [1, 1]
    assert is_safe(b.avail, b.alloc, b.need) == [1, 2, 0]
    assert b.request(0, [0, 1]) is True
    assert is_safe(b.avail, b.alloc, b.need) == [1, 0, 2]
    assert b.avail == [1, 0]
    assert b.request(2, [1, 0]) is False  # the unit is free, but the result is unsafe
    assert b.avail == [1, 0] and b.alloc[2] == [0, 1]


def test_safety_check_matches_brute_force_over_orders():
    rng = random.Random(21)
    unsafe = 0
    for _ in range(1500):
        n, m = rng.randint(1, 5), rng.randint(1, 3)
        avail, alloc, need = random_state(rng, n, m)
        seq = is_safe(avail, alloc, need)
        assert (seq is not None) == brute_safe(avail, alloc, need)
        unsafe += seq is None
        if seq is not None:
            assert sorted(seq) == list(range(n))
            assert brute_safe(avail, [alloc[i] for i in seq], [need[i] for i in seq])
    assert unsafe > 50


def test_request_keeps_the_state_safe():
    rng = random.Random(22)
    for _ in range(300):
        n, m = rng.randint(2, 4), rng.randint(1, 3)
        total = [rng.randint(1, 4) for _ in range(m)]
        b = Banker(total, [[rng.randint(0, t) for t in total] for _ in range(n)])
        for _ in range(20):
            i = rng.randrange(n)
            if rng.random() < 0.3:
                b.release(i, [rng.randint(0, a) for a in b.alloc[i]])
                continue
            req = [rng.randint(0, k) for k in b.need[i]]
            before = (list(b.avail), [r[:] for r in b.alloc])
            ok = b.request(i, req)
            if not ok:
                assert (b.avail, b.alloc) == before
                fits = all(req[r] <= b.avail[r] for r in range(m))
                if fits:  # refused only because the result would be unsafe
                    alloc = [r[:] for r in b.alloc]
                    alloc[i] = [alloc[i][r] + req[r] for r in range(m)]
                    need = [[b.maximum[j][r] - alloc[j][r] for r in range(m)] for j in range(n)]
                    assert not brute_safe([b.avail[r] - req[r] for r in range(m)], alloc, need)
            assert brute_safe(b.avail, b.alloc, b.need)
            assert all(b.avail[r] + sum(row[r] for row in b.alloc) == total[r] for r in range(m))


def test_banker_never_deadlocks_in_any_interleaving():
    # one type of three units; three clients that each claim two
    plans = {p: [("get", 0), ("get", 0)] for p in "pqs"}
    maximum = {p: [2] for p in "pqs"}
    free = explore(lambda: build([3], maximum, plans, banker=False))
    assert free.deadlocks and not free.truncated
    safe = explore(lambda: build([3], maximum, plans, banker=True))
    assert safe.deadlocks == [] and safe.finals >= 1 and not safe.truncated
    # two single unit types taken in opposite orders
    plans2 = {"p": [("get", 0), ("get", 1)], "q": [("get", 1), ("get", 0)]}
    maximum2 = {"p": [1, 1], "q": [1, 1]}
    assert explore(lambda: build([1, 1], maximum2, plans2, banker=False)).deadlocks
    res = explore(lambda: build([1, 1], maximum2, plans2, banker=True))
    assert res.deadlocks == [] and not res.truncated


def test_unsafe_state_that_is_not_a_deadlock():
    # one type of three units; p and q claim three each and hold one each
    assert is_safe([1], [[1], [1]], [[2], [2]]) is None
    maximum, start = {"p": [3], "q": [3]}, {"p": [1], "q": [1]}
    # p gives its unit back without asking for more: every run finishes
    light = {"p": [], "q": [("get", 0), ("get", 0)]}
    res = explore(lambda: build([3], maximum, light, start, banker=False))
    assert res.deadlocks == [] and res.finals == 1
    # if both use their full claims, some runs deadlock
    full = {"p": [("get", 0), ("get", 0)], "q": [("get", 0), ("get", 0)]}
    assert explore(lambda: build([3], maximum, full, start, banker=False)).deadlocks
