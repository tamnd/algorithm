# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-load-consistent-hashing/. The authors are listed in prov/5BJKG5.jsonl.

import random
from fractions import Fraction

from bounded_load_consistent_hashing import BoundedLoadRing


def check(r: BoundedLoadRing) -> None:
    """Capacity (C) and the walk invariant (I)."""
    cap = r.capacity()
    assert sum(r.loads().values()) == len(r.where)
    for b in r.order:
        assert r.load(b) <= cap
    for x in r.where:
        for i in range(len(r.order)):
            if r.passes(x, i):
                assert r.load(r.order[i]) >= cap


def test_example_of_the_page():
    pos = {"A": 20, "B": 50, "C": 80}
    balls = {"p": 10, "q": 12, "r": 15, "s": 17, "t": 19}
    r = BoundedLoadRing(list(pos), Fraction(1, 2), pos.get, balls.get)
    got = [r.insert(x) for x in "pqrst"]
    assert got == ["A", "B", "A", "B", "A"]
    assert r.capacity() == 3 and r.moves == 0
    r.delete("s")  # the capacity drops to 2, so A sheds p to B
    assert r.capacity() == 2 and r.moves == 1
    assert r.lookup("p") == "B"
    r.delete("r")  # A is no longer full, and p comes back
    assert r.moves == 2 and r.lookup("p") == "A" and r.lookup("q") == "B"
    check(r)


def test_large_eps_is_the_plain_ring():
    r = BoundedLoadRing(["b%d" % i for i in range(10)], 1000)
    for i in range(300):
        r.insert("x%d" % i)
    for x in r.where:
        assert r.walk_length(x) == 0
    assert r.moves == 0


def test_invariants_under_random_updates():
    for eps in [Fraction(1, 10), Fraction(1, 2), Fraction(1)]:
        rng = random.Random(7)
        r = BoundedLoadRing(["b%d" % i for i in range(12)], eps)
        live, nxt = [], 0
        for step in range(400):
            u = rng.random()
            if u < 0.55 or len(live) < 5:
                x = "x%d" % nxt
                nxt += 1
                r.insert(x)
                live.append(x)
            elif u < 0.95:
                r.delete(live.pop(rng.randrange(len(live))))
            elif u < 0.975:
                r.add_bin("extra%d" % step)
            elif len(r.order) > 2:
                r.remove_bin(r.order[rng.randrange(len(r.order))])
            check(r)


def test_loads_do_not_depend_on_the_order():
    rng = random.Random(8)
    bins = ["b%d" % i for i in range(15)]
    r = BoundedLoadRing(bins, Fraction(1, 4))
    live, nxt = [], 0
    for _ in range(500):
        if rng.random() < 0.6 or not live:
            live.append("x%d" % nxt)
            r.insert(live[-1])
            nxt += 1
        else:
            r.delete(live.pop(rng.randrange(len(live))))
    fresh = BoundedLoadRing(bins, Fraction(1, 4))
    shuffled = live[:]
    rng.shuffle(shuffled)
    for x in shuffled:
        fresh.insert(x)
    assert fresh.loads() == r.loads()


def test_moves_are_few_and_grow_as_eps_shrinks():
    per_update = {}
    for eps in [Fraction(1, 10), Fraction(1)]:
        rng = random.Random(9)
        r = BoundedLoadRing(["b%d" % i for i in range(20)], eps)
        for i in range(400):
            r.insert("x%d" % i)
        r.moves = 0
        live, nxt = list(r.where), 400
        for _ in range(200):
            if rng.random() < 0.5:
                r.delete(live.pop(rng.randrange(len(live))))
            else:
                live.append("x%d" % nxt)
                r.insert(live[-1])
                nxt += 1
        per_update[eps] = r.moves / 200
        check(r)
    assert per_update[Fraction(1)] < 3
    assert per_update[Fraction(1, 10)] > per_update[Fraction(1)]


def test_bin_changes_move_few_balls():
    r = BoundedLoadRing(["b%d" % i for i in range(20)], Fraction(1, 2))
    for i in range(600):
        r.insert("x%d" % i)
    before = dict(r.where)
    r.moves = 0
    r.add_bin("new")
    check(r)
    changed = sum(1 for x in before if r.where[x] != before[x])
    assert changed <= r.moves < 600 // 2
    assert r.load("new") > 0
