# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clock-pro/. The authors are listed in prov/P3XQXT.jsonl.

import random

from clock_pro import ClockPro, clock_pro_hits


def ring(a):
    """The entries of the clock, from HAND_hot around the circle."""
    out = []
    e = a.hand_hot
    if e is None:
        return out
    while True:
        out.append(e)
        assert e.next.prev is e and e.prev.next is e
        e = e.next
        if e is a.hand_hot:
            return out


def code(e):
    s = e.key + ("H" if e.hot else ("c" if e.resident else "n"))
    return s + ("*" if e.ref else "") + ("t" if e.test else "")


def check_invariants(a):
    entries = ring(a)
    assert {id(e) for e in entries} == {id(e) for e in a.table.values()}
    assert len(entries) == len(a.table)
    for hand in (a.hand_cold, a.hand_test):
        assert hand is None or any(hand is e for e in entries)
    assert a.n_hot == sum(e.hot for e in entries)
    assert a.n_cold == sum(not e.hot and e.resident for e in entries)
    assert a.n_nonres == sum(not e.resident for e in entries)
    assert a.n_hot + a.n_cold <= a.m, "at most m resident pages"
    assert a.n_nonres <= a.m, "at most m non-resident pages"
    assert 1 <= a.mc <= a.m - 1
    assert a.n_hot <= a.m - a.mc
    for e in entries:
        assert not (e.hot and e.test), "a hot page has no test period"
        assert not (e.hot and not e.resident), "hot pages are resident"
        if not e.resident:
            assert e.test, "a non-resident page is in its test period"


def traces():
    rng = random.Random(2005)
    for _ in range(60):
        u = rng.randint(2, 30)
        m = rng.randint(2, 8)
        yield [rng.randrange(u) for _ in range(rng.randint(1, 300))], m, rng.random() < 0.5


def test_worked_example():
    a = ClockPro(4, mc=1, adaptive=False)
    rows = []
    for x in "ABACDBEAFBCGD":
        hit = a.access(x)
        rows.append((hit, a.evicted, " ".join(code(e) for e in ring(a))))
    assert [r[0] for r in rows] == [False, False, True, False, False, True, False, True, False, True, False, False, False]
    assert [r[1] for r in rows] == [None] * 6 + ["C", None, "D", None, "E", "F", "G"]
    assert rows[6][2] == "Cnt Dct AH BH Ect"
    assert rows[10][2] == "Dnt AH* BH* Ent Fct CH"
    assert rows[12][2] == "Gnt DH AH BH Cc"


def test_invariants_after_every_request():
    for trace, m, adaptive in traces():
        a = ClockPro(m, adaptive=adaptive)
        for x in trace:
            before = x in a
            full = len(a) == a.m
            assert a.access(x) == before
            if not before and full:
                assert a.evicted is not None and a.evicted not in a
            else:
                assert a.evicted is None
            check_invariants(a)


def test_hot_pages_survive_a_scan():
    a = ClockPro(10, mc=2, adaptive=False)
    for x in list(range(6)) * 3:
        a.access(x)
    for x in range(100, 1100):
        a.access(x)
    assert all(x in a for x in range(6))


def test_loop_slightly_larger_than_memory():
    # LRU gets no hit on these loops; CLOCK-Pro keeps most hot pages.
    for n in (11, 12, 15):
        trace = list(range(n)) * 100
        assert sum(clock_pro_hits(trace, 10)[2 * n :]) > 700


def test_adaptation_moves_mc():
    a = ClockPro(20, mc=1)
    seen = {a.mc}
    rng = random.Random(7)
    for _ in range(3000):
        a.access(rng.randrange(60))
        seen.add(a.mc)
    assert min(seen) == 1 and max(seen) > 1
