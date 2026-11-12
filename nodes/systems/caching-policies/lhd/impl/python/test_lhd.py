# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lhd/. The authors are listed in prov/VC0D27.jsonl.

import random
from collections import OrderedDict
from fractions import Fraction

from lhd import LHD, lhd_hits


def brute_rank(H, L):
    A = len(H)
    out = []
    for a in range(A):
        num = sum(H[e] for e in range(a, A))
        den = sum((e - a + 1) * L[e] for e in range(a, A))
        out.append(Fraction(num) / den if den else Fraction(0))
    return out


def traces():
    rng = random.Random(2018)
    for _ in range(25):
        u = rng.randint(2, 40)
        cap = rng.randint(1, 30)
        trace = [(x, 1 + x % 5) for x in (rng.randrange(u) for _ in range(rng.randint(1, 400)))]
        yield trace, cap, rng.randint(1, 4), rng.randint(5, 50)


def test_worked_example_rank_table():
    a = LHD(10, classes=1, ages=4)
    a.new_hits[0] = [0, 3, 0, 1]
    a.new_lives[0] = [1, 3, 1, 3]
    a.reconfigure()
    assert a.rank[0] == [Fraction(2, 11), Fraction(2, 7), Fraction(1, 7), Fraction(1, 3)]


def test_rank_matches_the_formula_after_decay():
    rng = random.Random(1)
    a = LHD(10, classes=3, ages=6)
    for _ in range(4):
        for k in range(3):
            for e in range(6):
                h = rng.randrange(4)
                a.new_hits[k][e] = h
                a.new_lives[k][e] = h + rng.randrange(4)
        a.reconfigure()
        for k in range(3):
            assert a.rank[k] == brute_rank(a.hits[k], a.lives[k])


def test_full_sample_evicts_the_global_minimum():
    for trace, cap, classes, interval in traces():
        a = LHD(cap, samples=10 ** 6, classes=classes, ages=8, coarseness=2, interval=interval)
        for x, s in trace:
            if x not in a and s <= cap and a.used + s > cap:
                a.t += 1  # ages as the access will see them
                best = min(a.keys, key=lambda y: (a.density(y), a.last[y]))
                a.t -= 1
                a.access(x, s)
                assert a.evicted[0] == best
            else:
                a.access(x, s)


def test_sizes_and_histograms_stay_consistent():
    for trace, cap, classes, interval in traces():
        a = LHD(cap, samples=3, classes=classes, ages=8, coarseness=2, interval=interval, seed=cap)
        hits = evictions = 0
        for x, s in trace:
            before = x in a
            hit = a.access(x, s)
            assert hit == before
            hits += hit
            evictions += len(a.evicted)
            assert a.used == sum(a.size.values()) <= cap
            assert (x in a) == (s <= cap)
            assert all(1 <= r for r in a.refs.values())
            if a.t % interval == 0:
                hits = evictions = 0
            assert sum(map(sum, a.new_hits)) == hits
            assert sum(map(sum, a.new_lives)) == hits + evictions


def test_learns_a_loop_that_lru_misses():
    # A loop of 40 objects mixed one to one with objects used once. The
    # reuse distance is 80, so LRU with room for 50 never hits. With small
    # samples some loop objects survive by chance, LHD sees their hits at
    # ages near 80, and then keeps loop objects. With a full sample and no
    # hits to learn from, it acts like LRU: this is why the paper keeps
    # a few explorer objects.
    trace = []
    for r in range(100):
        for i in range(40):
            trace += [(("loop", i), 1), (("once", r * 40 + i), 1)]
    lru, lru_hits = OrderedDict(), 0
    for x, _ in trace:
        if x in lru:
            lru_hits += 1
            lru.move_to_end(x)
        else:
            lru[x] = None
            if len(lru) > 50:
                lru.popitem(last=False)
    opts = dict(coarseness=4, ages=64, interval=500)
    sampled = lhd_hits(trace, 50, samples=4, **opts)
    full = lhd_hits(trace, 50, samples=64, **opts)
    assert lru_hits == 0 and sum(full) == 0
    assert sum(sampled[-2000:]) > 500


def test_too_large_objects_are_not_cached():
    a = LHD(5)
    assert a.access("big", 6) is False and "big" not in a and a.used == 0
