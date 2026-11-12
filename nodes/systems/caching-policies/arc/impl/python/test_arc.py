# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc/. The authors are listed in prov/Z520JB.jsonl.

import random
from fractions import Fraction

from arc import ARC, arc_hits


def naive_arc(trace, c):
    """A second ARC, written with plain Python lists (index 0 is the LRU end)."""
    t1, t2, b1, b2 = [], [], [], []
    p = Fraction(0)
    hits = []

    def replace(x):
        if t1 and (len(t1) > p or (x in b2 and len(t1) == p)):
            b1.append(t1.pop(0))
        else:
            b2.append(t2.pop(0))

    for x in trace:
        if x in t1 or x in t2:
            (t1 if x in t1 else t2).remove(x)
            t2.append(x)
            hits.append(True)
            continue
        hits.append(False)
        if x in b1:
            p = min(Fraction(c), p + max(Fraction(len(b2), len(b1)), 1))
            replace(x)
            b1.remove(x)
            t2.append(x)
        elif x in b2:
            p = max(Fraction(0), p - max(Fraction(len(b1), len(b2)), 1))
            replace(x)
            b2.remove(x)
            t2.append(x)
        else:
            if len(t1) + len(b1) == c:
                if len(t1) < c:
                    b1.pop(0)
                    replace(x)
                else:
                    t1.pop(0)
            else:
                total = len(t1) + len(t2) + len(b1) + len(b2)
                if total >= c:
                    if total == 2 * c:
                        b2.pop(0)
                    replace(x)
            t1.append(x)
    return hits


def dbl_step(l1, l2, x, c):
    """One request to DBL(2c): L1 holds pages seen once, L2 pages seen at least twice."""
    if x in l1 or x in l2:
        (l1 if x in l1 else l2).remove(x)
        l2.append(x)
        return
    if len(l1) == c:
        l1.pop(0)
    elif len(l1) + len(l2) == 2 * c:
        l2.pop(0)
    l1.append(x)


def check_invariants(a):
    c = a.c
    n1, n2, m1, m2 = len(a.t1), len(a.t2), len(a.b1), len(a.b2)
    assert n1 + n2 <= c
    assert n1 + m1 <= c
    assert n2 + m2 <= 2 * c
    assert n1 + n2 + m1 + m2 <= 2 * c
    assert 0 <= a.p <= c
    keys = list(a.t1) + list(a.t2) + list(a.b1) + list(a.b2)
    assert len(keys) == len(set(keys)), "the four lists are disjoint"
    if n1 + n2 + m1 + m2 < c:
        assert m1 == 0 and m2 == 0
    else:
        assert n1 + n2 == c


def traces():
    rng = random.Random(2003)
    for _ in range(60):
        u = rng.randint(2, 14)
        yield [rng.randrange(u) for _ in range(rng.randint(1, 200))], rng.randint(1, 6)


def test_worked_example():
    a = ARC(3)
    trace = [1, 2, 1, 3, 4, 2, 5, 4, 1, 6, 1, 2]
    got = [a.access(x) for x in trace]
    assert got == [False, False, True, False, False, False, False, True, False, False, True, False]
    assert list(a.t1) == [] and list(a.t2) == [4, 1, 2]
    assert list(a.b1) == [3, 5, 6] and list(a.b2) == []
    assert a.p == 0


def test_p_moves_in_both_directions():
    a = ARC(3)
    ps = []
    for x in [1, 2, 1, 3, 4, 2, 5, 4, 1]:
        a.access(x)
        ps.append(a.p)
    assert ps == [0, 0, 0, 0, 0, 1, 1, 1, 0]


def test_invariants_after_every_request():
    for trace, c in traces():
        a = ARC(c)
        for x in trace:
            before = x in a
            assert a.access(x) == before
            check_invariants(a)


def test_same_hits_as_naive_reference():
    for trace, c in traces():
        assert arc_hits(trace, c) == naive_arc(trace, c)


def test_directory_is_dbl_2c():
    for trace, c in traces():
        a = ARC(c)
        l1, l2 = [], []
        for x in trace:
            a.access(x)
            dbl_step(l1, l2, x, c)
            assert list(a.b1) + list(a.t1) == l1
            assert list(a.b2) + list(a.t2) == l2


def test_directory_holds_the_c_most_recent_pages():
    for trace, c in traces():
        a = ARC(c)
        for t, x in enumerate(trace):
            a.access(x)
            recent = []
            for y in reversed(trace[: t + 1]):
                if y not in recent:
                    recent.append(y)
                if len(recent) == c:
                    break
            directory = set(a.t1) | set(a.t2) | set(a.b1) | set(a.b2)
            assert set(recent) <= directory


def test_scan_does_not_flush_t2_while_p_is_zero():
    c = 8
    a = ARC(c)
    hot = list(range(4))
    for x in hot + hot:
        a.access(x)
    assert set(a.t2) == set(hot) and a.p == 0
    for x in range(100, 400):
        a.access(x)
    assert set(hot) <= set(a.t2)
    assert all(a.access(x) for x in hot)


def test_loop_larger_than_cache_has_no_hits():
    # All four lists are in LRU order, so on a pure loop ARC, like LRU, always
    # drops the page that the loop needs next.
    c = 10
    for length in (11, 12, 15, 20, 30):
        trace = list(range(length)) * 50
        assert sum(arc_hits(trace, c)) == 0


def test_size_one():
    assert arc_hits([1, 1, 2, 2, 1], 1) == [False, True, False, True, False]
