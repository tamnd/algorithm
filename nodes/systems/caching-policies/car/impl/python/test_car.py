# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/car/. The authors are listed in prov/BEKWFB.jsonl.

import random
from fractions import Fraction

from car import CAR, car_hits


def naive_car(trace, c):
    """A second CAR with plain lists. A clock is a list of [page, bit], head first."""
    t1, t2, b1, b2 = [], [], [], []
    p = Fraction(0)
    hits = []

    def find(clock, x):
        return next((e for e in clock if e[0] == x), None)

    def replace():
        while True:
            if len(t1) >= max(1, p):
                e = t1.pop(0)
                if not e[1]:
                    b1.append(e[0])
                    return
                e[1] = False
                t2.append(e)
            else:
                e = t2.pop(0)
                if not e[1]:
                    b2.append(e[0])
                    return
                e[1] = False
                t2.append(e)

    for x in trace:
        e = find(t1, x) or find(t2, x)
        if e:
            e[1] = True
            hits.append(True)
            continue
        hits.append(False)
        if len(t1) + len(t2) == c:
            replace()
            ghost = x in b1 or x in b2
            if not ghost and len(t1) + len(b1) == c:
                b1.pop(0)
            elif not ghost and len(t1) + len(t2) + len(b1) + len(b2) == 2 * c:
                b2.pop(0)
        if x in b1:
            p = min(p + max(Fraction(1), Fraction(len(b2), len(b1))), Fraction(c))
            b1.remove(x)
            t2.append([x, False])
        elif x in b2:
            p = max(p - max(Fraction(1), Fraction(len(b1), len(b2))), Fraction(0))
            b2.remove(x)
            t2.append([x, False])
        else:
            t1.append([x, False])
    return hits


def check_invariants(a, full_before):
    c = a.c
    n1, n2, m1, m2 = len(a.t1), len(a.t2), len(a.b1), len(a.b2)
    assert n1 + n2 <= c  # I1
    assert n1 + m1 <= c  # I2
    assert n2 + m2 <= 2 * c  # I3
    assert n1 + n2 + m1 + m2 <= 2 * c  # I4
    if n1 + n2 < c:
        assert m1 == 0 and m2 == 0  # I5
    if n1 + n2 + m1 + m2 >= c:
        assert n1 + n2 == c  # I6
    if full_before:
        assert n1 + n2 == c  # I7
    assert 0 <= a.p <= c
    keys = list(a.t1) + list(a.t2) + list(a.b1) + list(a.b2)
    assert len(keys) == len(set(keys))
    assert set(a.where) == set(a.t1) | set(a.t2) == set(a.ref)


def traces():
    rng = random.Random(2004)
    for _ in range(60):
        u = rng.randint(2, 14)
        yield [rng.randrange(u) for _ in range(rng.randint(1, 200))], rng.randint(1, 6)


def test_worked_example():
    a = CAR(3)
    trace = [1, 2, 1, 3, 4, 2, 5, 4, 1, 6, 1, 2]
    got = [a.access(x) for x in trace]
    assert got == [False, False, True, False, False, False, False, False, True, False, True, False]
    assert list(a.t1) == [6] and list(a.t2) == [1, 2]
    assert a.ref[1] and not a.ref[2] and not a.ref[6]
    assert list(a.b1) == [3, 5] and list(a.b2) == [4]
    assert a.p == 1


def test_p_moves_in_both_directions():
    a = CAR(3)
    ps = []
    for x in [1, 2, 1, 3, 4, 2, 5, 4, 1, 6, 1, 2]:
        a.access(x)
        ps.append(a.p)
    assert ps == [0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 1]


def test_invariants_i1_to_i7():
    for trace, c in traces():
        a = CAR(c)
        for x in trace:
            full = len(a) == c
            before = x in a
            assert a.access(x) == before
            check_invariants(a, full)


def test_same_hits_as_naive_reference():
    for trace, c in traces():
        assert car_hits(trace, c) == naive_car(trace, c)


def test_hit_only_sets_the_bit():
    a = CAR(4)
    for x in [1, 2, 3]:
        a.access(x)
    order = (list(a.t1), list(a.t2))
    assert a.access(2)
    assert (list(a.t1), list(a.t2)) == order and a.ref[2]


def test_scan_keeps_pages_with_set_bits():
    c = 8
    a = CAR(c)
    hot = list(range(4))
    for x in hot + hot:
        a.access(x)
    for x in range(100, 400):
        a.access(x)
        for h in hot:
            a.access(h)
    assert all(h in a for h in hot)


def test_size_one():
    assert car_hits([1, 1, 2, 2, 1], 1) == [False, True, False, True, False]
