# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tinylfu/. The authors are listed in prov/F0NQ2Y.jsonl.

import random

from tinylfu import FrequencyFilter, TinyLFU, tinylfu_hits


class ExactFilter:
    """The same counting rules with no hashing: an exact doorkeeper set and
    exact counters, capped and halved in the same way."""

    def __init__(self, window, cap):
        self.window, self.cap = window, cap
        self.door, self.count, self.additions = set(), {}, 0

    def add(self, x):
        if x not in self.door:
            self.door.add(x)
        elif self.count.get(x, 0) < self.cap:
            self.count[x] = self.count.get(x, 0) + 1
        self.additions += 1
        if self.additions == self.window:
            self.count = {k: v // 2 for k, v in self.count.items()}
            self.door.clear()
            self.additions //= 2

    def estimate(self, x):
        return self.count.get(x, 0) + (x in self.door)


def traces():
    rng = random.Random(2017)
    for _ in range(25):
        u = rng.randint(2, 60)
        c = rng.randint(1, 8)
        yield [rng.randrange(u) for _ in range(rng.randint(1, 400))], c, rng.randrange(1000)


def test_worked_example():
    a = TinyLFU(2)
    rows = []
    for x in "AABBCCCADAC":
        hit = a.access(x)
        rows.append((hit, a.last, list(a.cache)))
    assert [r[0] for r in rows] == [False, True, False, True, False, False, False, False, False, True, True]
    assert rows[4] == (False, ("A", False), ["A", "B"])
    assert rows[6] == (False, ("A", True), ["B", "C"])
    assert rows[7] == (False, ("B", True), ["C", "A"])
    assert rows[8] == (False, ("C", False), ["C", "A"])


def test_estimate_never_below_the_exact_count():
    # Hash collisions and doorkeeper false positives only raise estimates.
    for trace, c, seed in traces():
        f = FrequencyFilter(c, seed=seed, width=8, door_bits=64)
        e = ExactFilter(f.window, f.cap)
        for x in trace:
            f.add(x)
            e.add(x)
            assert f.additions == e.additions
            for y in set(trace):
                assert f.estimate(y) >= e.estimate(y)


def test_counters_are_capped():
    f = FrequencyFilter(4, sample_factor=50)
    for _ in range(150):
        f.add("hot")
    assert f.cap == 50 and f.sketch("hot") == 50 and f.estimate("hot") == 51


def test_reset_halves_counters_and_clears_the_doorkeeper():
    f = FrequencyFilter(3)  # W = 30
    for i in range(f.window - 1):
        f.add(i % 4)
    before = [row[:] for row in f.rows]
    assert not f.in_door("last")  # so the last add only touches the doorkeeper
    f.add("last")
    assert f.resets == 1 and f.additions == f.window // 2
    assert not any(f.door)
    for r, row in enumerate(f.rows):
        assert row == [v // 2 for v in before[r]]


def test_admission_rule_on_every_full_miss():
    for trace, c, seed in traces():
        a = TinyLFU(c, seed=seed)
        for x in trace:
            hit_before = x in a
            v = next(iter(a.cache)) if len(a) == a.c else None
            hit = a.access(x)
            assert hit == hit_before and len(a) <= c
            if hit or v is None:
                assert x in a and a.last is None
                continue
            victim, admitted = a.last
            assert victim == v
            assert admitted == (a.filter.estimate(x) > a.filter.estimate(v))
            assert (x in a, v in a) == ((True, False) if admitted else (False, True))


def test_one_hit_wonders_do_not_flush_hot_objects():
    c = 20
    a = TinyLFU(c)
    hot = [("hot", i) for i in range(c)]
    for _ in range(4):
        for h in hot:
            a.access(h)
    for i in range(10 * c):
        a.access(("once", i))
    assert all(h in a for h in hot)


def test_hits_are_reproducible_for_a_seed():
    trace = [random.Random(5).randrange(50) for _ in range(500)]
    assert tinylfu_hits(trace, 10, seed=3) == tinylfu_hits(trace, 10, seed=3)
