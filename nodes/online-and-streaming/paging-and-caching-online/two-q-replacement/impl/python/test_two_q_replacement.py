# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-q-replacement/. The authors are listed in prov/VWYKNJ.jsonl.

import random

from two_q_replacement import TwoQ, two_q_replacement


class ListTwoQ:
    """An independent model of full 2Q with plain lists; index 0 is the head."""

    def __init__(self, c, kin, kout):
        self.c, self.kin, self.kout = c, kin, kout
        self.a1in, self.a1out, self.am = [], [], []

    def reclaim(self):
        if len(self.a1in) + len(self.am) < self.c:
            return None
        if len(self.a1in) > self.kin:
            y = self.a1in.pop()
            self.a1out.insert(0, y)
            if len(self.a1out) > self.kout:
                self.a1out.pop()
            return y
        return self.am.pop()

    def access(self, x):
        if x in self.am:
            self.am.remove(x)
            self.am.insert(0, x)
            return True, None
        if x in self.a1in:
            return True, None
        if x in self.a1out:
            self.a1out.remove(x)
            out = self.reclaim()
            self.am.insert(0, x)
            return False, out
        out = self.reclaim()
        self.a1in.insert(0, x)
        return False, out


def belady_misses(requests, c):
    cache, misses = set(), 0
    for t, x in enumerate(requests):
        if x in cache:
            continue
        misses += 1
        if len(cache) == c:
            def next_use(y):
                for u in range(t + 1, len(requests)):
                    if requests[u] == y:
                        return u
                return len(requests)
            cache.remove(max(sorted(cache), key=next_use))
        cache.add(x)
    return misses


def lru_misses(requests, c):
    cache, misses = [], 0
    for x in requests:
        if x in cache:
            cache.remove(x)
        else:
            misses += 1
            if len(cache) == c:
                cache.pop(0)
        cache.append(x)
    return misses


def test_example() -> None:
    seq = "abcdeabaxyzwab"
    misses, log = two_q_replacement(list(seq), 4, 1, 2)
    assert misses == 11
    q = TwoQ(4, 1, 2)
    for x in seq:
        q.access(x)
    # Each list is printed from the tail to the head.
    assert (list(q.a1in), list(q.a1out), list(q.am)) == (["z", "w"], ["x", "y"], ["a", "b"])
    outs = [None, None, None, None, "a", "b", "c", None, "d", "e", "x", "y", None, None]
    assert [out for _, _, out in log] == outs
    assert lru_misses(list(seq), 4) == 13


def test_matches_list_model() -> None:
    rng = random.Random(1994)
    for _ in range(300):
        c = rng.randint(1, 8)
        kin = rng.randint(0, c - 1)
        kout = rng.randint(0, 6)
        u = rng.randint(1, 3 * c + 2)
        a, b = TwoQ(c, kin, kout), ListTwoQ(c, kin, kout)
        for _ in range(rng.randint(0, 80)):
            x = rng.randrange(u)
            assert a.access(x) == b.access(x)
            assert list(reversed(a.a1in)) == b.a1in
            assert list(reversed(a.a1out)) == b.a1out
            assert list(reversed(a.am)) == b.am


def test_invariants() -> None:
    rng = random.Random(7)
    for _ in range(200):
        c = rng.randint(1, 8)
        kin, kout = rng.randint(0, c - 1), rng.randint(0, 6)
        q = TwoQ(c, kin, kout)
        for _ in range(100):
            x = rng.randrange(2 * c + 3)
            hit, _ = q.access(x)
            res = q.resident()
            assert len(res) <= c and len(set(res)) == len(res)
            assert len(q.a1out) <= kout
            assert not set(q.a1out) & set(res)
            assert x in res


def test_scan_resistance() -> None:
    # A hot set reaches Am; a long scan of new pages then passes through A1in only.
    c, kin, kout = 8, 2, 4
    hot = ["h%d" % i for i in range(4)]
    warm = hot + ["p%d" % i for i in range(8)] + hot
    scan = ["s%d" % i for i in range(100)]
    requests = warm + scan + hot
    q = TwoQ(c, kin, kout)
    for x in warm:
        q.access(x)
    assert set(hot) <= set(q.am)
    for x in scan:
        q.access(x)
    assert all(q.access(x)[0] for x in hot)
    tail = len(requests) - len(hot)
    assert lru_misses(requests, c) - lru_misses(requests[:tail], c) == len(hot)


def bad_sequence(c, kin, kout, stale, cycle, reps):
    """Put stale pages in Am, then cycle over c new pages. Built with the list model."""
    q, reqs, n = ListTwoQ(c, kin, kout), [], 0

    def acc(x):
        reqs.append(x)
        q.access(x)

    for _ in range(c):
        acc(("f", n))
        n += 1
    for i in range(stale):
        acc(("s", i))
        while ("s", i) not in q.a1out:
            acc(("f", n))
            n += 1
        acc(("s", i))
    prefix = len(reqs)
    reqs += [("w", j) for j in range(cycle)] * reps
    return reqs, prefix


def test_not_competitive_with_usual_parameters() -> None:
    # c = 8, Kin = c / 4, Kout = c / 2: stale pages in Am are never evicted, and a cycle
    # over c pages misses each time, while the offline optimum stops missing.
    c, kin, kout = 8, 2, 4
    for reps in (5, 50):
        reqs, prefix = bad_sequence(c, kin, kout, 6, c, reps)
        misses, log = two_q_replacement(reqs, c, kin, kout)
        assert all(not hit for x, hit, _ in log[prefix:])
        assert sum(1 for _, hit, _ in log[prefix:] if not hit) == c * reps
        opt = belady_misses(reqs, c)
        assert opt <= belady_misses(reqs[:prefix], c) + c


def test_edges() -> None:
    assert two_q_replacement([], 3, 1, 1) == (0, [])
    assert two_q_replacement([5, 5, 5], 1, 0, 0)[0] == 1
    for args in ((0, 0, 0), (3, 3, 1), (3, -1, 1)):
        try:
            TwoQ(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("bad parameters must be rejected")
