# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lirs/. The authors are listed in prov/ESWX79.jsonl.

import random

from lirs import LIRS, lirs_hits


def naive_lirs(trace, c, lhirs):
    """LIRS with no stack S. Membership in S is computed from the time of the
    last access: a block is in S if it is LIR or if its last access is more
    recent than the last access of the oldest LIR block."""
    llirs = c - lhirs
    last, lir, q, hits = {}, set(), [], []

    def oldest_lir():
        return min(lir, key=last.__getitem__) if lir else None

    def in_s(x):
        y = oldest_lir()
        return x in lir or (x in last and (y is None or last[x] > last[y]))

    for t, x in enumerate(trace):
        if x in lir:
            hits.append(True)
        elif x in q:
            hits.append(True)
            q.remove(x)
            if in_s(x):
                y = oldest_lir()
                lir.remove(y)
                lir.add(x)
                q.append(y)
            else:
                q.append(x)
        else:
            hits.append(False)
            if len(lir) < llirs:
                lir.add(x)
            else:
                if len(lir) + len(q) == c:
                    q.pop(0)
                if in_s(x):
                    y = oldest_lir()
                    lir.remove(y)
                    lir.add(x)
                    q.append(y)
                else:
                    q.append(x)
        last[x] = t
    return hits


def recency_and_irr(trace, t):
    """Recency and IRR of each block just before time t (0-based), by definition."""
    out = {}
    for x in set(trace[:t]):
        times = [i for i in range(t) if trace[i] == x]
        recency = len(set(trace[times[-1] + 1 : t]))
        irr = len(set(trace[times[-2] + 1 : times[-1]])) if len(times) > 1 else None
        out[x] = (recency, irr)
    return out


def check_invariants(a, last):
    if a.s:
        assert next(iter(a.s)) in a.lir, "the bottom of S is an LIR block"
    assert a.lir <= set(a.s)
    assert not (a.lir & set(a.q))
    assert len(a.lir) <= a.llirs and len(a.q) <= a.lhirs
    order = [last[x] for x in a.s]
    assert order == sorted(order), "S is in order of last access"
    if a.lir:
        m = min(last[y] for y in a.lir)
        assert set(a.s) == a.lir | {x for x in last if last[x] > m}


def traces():
    rng = random.Random(2002)
    for _ in range(60):
        u = rng.randint(2, 16)
        c = rng.randint(2, 7)
        yield [rng.randrange(u) for _ in range(rng.randint(1, 250))], c, rng.randint(1, c - 1)


def test_recency_and_irr_of_table_1():
    # Table 1 of the paper: the values at virtual time 10. None is an infinite IRR.
    info = recency_and_irr(list("ADBCBADAE"), 9)
    assert info == {"A": (1, 1), "B": (3, 1), "C": (4, None), "D": (2, 3), "E": (0, None)}


def test_worked_example_from_a_cold_cache():
    # The page example. A cold start gives A and D the LIR status first, so the
    # state differs from the snapshot {A, B} that Table 1 assumes.
    a = LIRS(3, lhirs=1)
    got = [a.access(x) for x in "ADBCBADAEDC"]
    assert got == [False] * 5 + [True] * 3 + [False, True, False]
    assert a.lir == {"A", "D"}
    assert list(a.s) == ["A", "E", "D", "C"] and list(a.q) == ["C"]
    a = LIRS(3, lhirs=1)
    states = []
    for x in "ADBCBADA":
        a.access(x)
        states.append((sorted(a.lir), list(a.s), list(a.q)))
    assert states[4] == (["B", "D"], ["D", "C", "B"], ["A"])
    assert states[5] == (["B", "D"], ["D", "C", "B", "A"], ["A"])
    assert states[6] == (["B", "D"], ["B", "A", "D"], ["A"])
    assert states[7] == (["A", "D"], ["D", "A"], ["B"])


def test_invariants_after_every_request():
    for trace, c, lhirs in traces():
        a = LIRS(c, lhirs)
        last = {}
        for t, x in enumerate(trace):
            a.access(x)
            last[x] = t
            check_invariants(a, last)


def test_hit_flag_is_membership():
    for trace, c, lhirs in traces():
        a = LIRS(c, lhirs)
        for x in trace:
            before = x in a
            assert a.access(x) == before
            assert len(a) <= c


def test_same_hits_as_reference_without_stack():
    for trace, c, lhirs in traces():
        assert lirs_hits(trace, c, lhirs) == naive_lirs(trace, c, lhirs)


def test_loop_larger_than_cache():
    # LRU gets no hit here. LIRS keeps its LIR blocks and hits on them.
    c, n = 10, 12
    trace = list(range(n)) * 100
    hits = lirs_hits(trace, c, lhirs=1)
    assert sum(hits[n * 2 :]) >= 8 * 98


def test_scan_does_not_touch_lir_blocks():
    a = LIRS(10, lhirs=2)
    for x in list(range(8)) * 2:
        a.access(x)
    lir = set(a.lir)
    for x in range(100, 1000):
        a.access(x)
    assert a.lir == lir == set(range(8))
