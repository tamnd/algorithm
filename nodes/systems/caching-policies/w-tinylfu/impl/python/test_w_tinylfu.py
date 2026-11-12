# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/w-tinylfu/. The authors are listed in prov/MSGGRD.jsonl.

import random

from w_tinylfu import FrequencyFilter, WTinyLFU, w_tinylfu_hits


def naive_w_tinylfu(trace, c, window, seed):
    """The same policy with plain lists (index 0 is the LRU end) and the same filter."""
    f = FrequencyFilter(c, seed=seed)
    main = c - window
    pcap = main * 4 // 5
    W, P, R, hits = [], [], [], []
    for x in trace:
        f.add(x)
        if x in W:
            W.remove(x)
            W.append(x)
            hits.append(True)
        elif x in R:
            R.remove(x)
            R.append(x)
            hits.append(True)
        elif x in P:
            P.remove(x)
            R.append(x)
            if len(R) > pcap:
                P.append(R.pop(0))
            hits.append(True)
        else:
            hits.append(False)
            W.append(x)
            if len(W) > window:
                w = W.pop(0)
                if len(P) + len(R) < main:
                    P.append(w)
                elif f.estimate(w) > f.estimate(P[0]):
                    P.pop(0)
                    P.append(w)
    return hits


def traces():
    rng = random.Random(2016)
    for _ in range(30):
        u = rng.randint(2, 60)
        c = rng.randint(2, 12)
        yield [rng.randrange(u) for _ in range(rng.randint(1, 400))], c, rng.randint(1, c - 1), rng.randrange(1000)


def test_worked_example():
    a = WTinyLFU(4, window=1)
    rows = []
    for x in "ABACADAEBFBFG":
        hit = a.access(x)
        rows.append((hit, a.duel, list(a.window), list(a.probation), list(a.protected)))
    assert [r[0] for r in rows] == [False, False, True, False, True, False, True, False, True, False, True, True, False]
    assert rows[2][2:] == (["B"], [], ["A"])
    assert rows[7] == (False, ("D", "B", False), ["E"], ["B", "C"], ["A"])
    assert rows[8][2:] == (["E"], ["C"], ["A", "B"])
    assert rows[9][1] == ("E", "C", False)
    assert rows[12] == (False, ("F", "C", True), ["G"], ["F"], ["A", "B"])


def test_same_hits_as_naive_reference():
    for trace, c, window, seed in traces():
        assert w_tinylfu_hits(trace, c, window, seed) == naive_w_tinylfu(trace, c, window, seed)


def test_segments_after_every_request():
    for trace, c, window, seed in traces():
        a = WTinyLFU(c, window, seed)
        for x in trace:
            before = x in a
            assert a.access(x) == before and x in a or (not before and a.evicted == x)
            assert len(a.window) <= a.window_cap
            assert len(a.protected) <= a.protected_cap
            assert len(a.probation) + len(a.protected) <= a.main_cap
            parts = [set(a.window), set(a.probation), set(a.protected)]
            assert sum(map(len, parts)) == len(set().union(*parts)), "segments are disjoint"


def test_default_sizes():
    a = WTinyLFU(1000)
    assert (a.window_cap, a.main_cap, a.protected_cap) == (10, 990, 792)
    assert WTinyLFU(50).window_cap == 1


def test_bursts_hit_in_the_window():
    # A new object asked three times in a row gets two hits from the window,
    # while the hot objects in the main cache stay.
    c = 100
    a = WTinyLFU(c)
    hot = list(range(c - a.window_cap))
    for _ in range(3):
        for h in hot:
            a.access(h)
    burst_hits = 0
    for i in range(200):
        for _ in range(3):
            burst_hits += a.access(("burst", i))
    assert burst_hits == 400
    assert a.filter.additions == 3 * len(hot) + 600 < a.filter.window, "no reset yet"
    # Only probation objects can lose a duel. Sketch collisions let a few
    # bursts win against probation objects, but the protected segment stays.
    assert len(a.protected) == a.protected_cap and set(a.protected) <= set(hot)
