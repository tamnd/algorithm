# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-tree-search/. The authors are listed in prov/C1KCSN.jsonl.
import random

from interval_tree_search import (
    IntervalTreeSearch,
    interval_tree_search,
    overlap_tests,
    stab_tests,
)

KINDS = ("closed", "half-open", "open")


def members(x, l, r, kind):
    if kind == "closed":
        return l <= x <= r
    if kind == "half-open":
        return l <= x < r
    return l < x < r


def meets(iv, q, kind):
    """Brute force on a fine grid: integer end points, so quarter steps suffice."""
    lo = min(iv[0], q[0]) - 1
    hi = max(iv[1], q[1]) + 1
    x = lo
    while x <= hi:
        if members(x, *iv, kind) and members(x, *q, kind):
            return True
        x += 0.25
    return False


EXAMPLE = [(1, 3), (2, 5), (3, 4), (5, 8), (6, 7), (8, 9), (7, 10)]


def names(t, idx):
    return sorted(t.iv[j] for j in idx)


def test_example_overlap():
    t = IntervalTreeSearch(EXAMPLE)
    assert names(t, t.overlap(4, 6, "closed")) == [(2, 5), (3, 4), (5, 8), (6, 7)]
    assert names(t, t.overlap(4, 6, "half-open")) == [(2, 5), (5, 8)]
    assert names(t, t.overlap(4, 6, "open")) == [(2, 5), (5, 8)]
    # in tree order, the order of the left ends
    assert t.overlap(4, 6, "closed") == [1, 2, 3, 4]


def test_example_stab():
    t = IntervalTreeSearch(EXAMPLE)
    assert names(t, t.stab(5, "closed")) == [(2, 5), (5, 8)]
    assert names(t, t.stab(5, "half-open")) == [(5, 8)]
    assert names(t, t.stab(5, "open")) == []
    assert names(t, t.stab(7, "closed")) == [(5, 8), (6, 7), (7, 10)]
    assert names(t, t.stab(7, "half-open")) == [(5, 8), (7, 10)]
    assert names(t, t.stab(7, "open")) == [(5, 8)]


def test_example_search():
    t = IntervalTreeSearch(EXAMPLE)
    assert t.iv[t.search(*overlap_tests(4, 6))] == (5, 8)
    assert t.iv[t.search(*overlap_tests(9, 9))] == (7, 10)
    assert t.search(*overlap_tests(11, 12)) is None
    assert t.search(*overlap_tests(10, 12, "half-open")) is None
    assert t.iv[t.search(*overlap_tests(10, 12, "closed"))] == (7, 10)


def test_touching():
    for kind, want in (("closed", [0, 1]), ("half-open", []), ("open", [])):
        assert interval_tree_search([(1, 3), (5, 6)], 3, 5, kind) == want
    t = IntervalTreeSearch([(1, 3), (3, 5)])
    assert t.stab(3, "closed") == [0, 1]
    assert t.stab(3, "half-open") == [1]
    assert t.stab(3, "open") == []


def test_edge_cases():
    t = IntervalTreeSearch([])
    assert t.overlap(0, 1) == [] and t.stab(0) == [] and t.search(*stab_tests(0)) is None
    t = IntervalTreeSearch([(2, 2)])
    assert t.stab(2) == [0] and t.stab(1) == [] and t.overlap(2, 2) == [0]
    # duplicates and a query inside one interval
    t = IntervalTreeSearch([(0, 10), (0, 10), (4, 5)])
    assert sorted(t.overlap(6, 7)) == [0, 1]
    assert sorted(t.stab(4, "half-open")) == [0, 1, 2]


def brute_overlap(ivs, a, b, kind):
    return sorted(j for j, iv in enumerate(ivs) if meets(iv, (a, b), kind))


def brute_stab(ivs, p, kind):
    return sorted(j for j, (l, r) in enumerate(ivs) if members(p, l, r, kind))


def random_family(rng, kind):
    n = rng.randint(0, 25)
    out = []
    for _ in range(n):
        l = rng.randint(0, 20)
        r = l + rng.randint(0 if kind == "closed" else 1, 8)
        out.append((l, r))
    return out


def test_random_against_brute_force():
    rng = random.Random(20261105)
    for _ in range(600):
        kind = rng.choice(KINDS)
        ivs = random_family(rng, kind)
        t = IntervalTreeSearch(ivs)
        a = rng.randint(-1, 29)
        b = a + rng.randint(0 if kind == "closed" else 1, 6)
        want = brute_overlap(ivs, a, b, kind)
        got = t.overlap(a, b, kind)
        assert sorted(got) == want and len(set(got)) == len(got)
        one = t.search(*overlap_tests(a, b, kind))
        assert (one is None) == (not want) and (one is None or one in want)
        p = rng.randint(-1, 29) + rng.choice((0, 0, 0.5))
        assert sorted(t.stab(p, kind)) == brute_stab(ivs, p, kind)
        one = t.search(*stab_tests(p, kind))
        assert (one is None) == (not brute_stab(ivs, p, kind))


def test_output_sensitive_visits():
    """REPORT never expands more than (k + 1) * (h + 1) nodes."""
    rng = random.Random(7)
    for _ in range(100):
        ivs = random_family(rng, "closed")
        t = IntervalTreeSearch(ivs)
        n = len(ivs)
        h = n.bit_length()
        a = rng.randint(0, 28)
        b = a + rng.randint(0, 4)
        reach, start = overlap_tests(a, b)
        expanded = 0

        # count nodes that pass L1 by replaying the recursion
        def walk(lo, hi):
            nonlocal expanded
            if lo >= hi:
                return
            mid = (lo + hi) // 2
            if not reach(t.max[mid]):
                return
            expanded += 1
            walk(lo, mid)
            if start(t.iv[t.order[mid]][0]):
                walk(mid + 1, hi)

        walk(0, n)
        k = len(t.overlap(a, b))
        assert expanded <= (k + 1) * max(h, 1)
