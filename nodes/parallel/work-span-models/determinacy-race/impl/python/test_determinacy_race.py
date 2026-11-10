# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/determinacy-race/. The authors are listed in prov/NHXTYV.jsonl.

import random

from determinacy_race import (DisjointSets, brute_force_data_races, brute_force_races, logically_parallel,
                              random_program, sp_bags)

X, Y = "x", "y"
INCREMENT = [("read", X), ("write", X)]  # x = x + 1


def test_parallel_increments_race():
    prog = [("spawn", INCREMENT), ("spawn", INCREMENT), ("sync",)]
    assert sp_bags(prog) == {X} == brute_force_races(prog)


def test_child_and_continuation_race():
    prog = [("spawn", [("write", X)]), ("read", X), ("sync",)]
    assert sp_bags(prog) == {X} == brute_force_races(prog)


def test_sync_removes_the_race():
    prog = [("spawn", INCREMENT), ("sync",), ("spawn", INCREMENT), ("sync",)]
    assert sp_bags(prog) == set() == brute_force_races(prog)
    prog = [("spawn", [("write", X)]), ("sync",), ("read", X)]
    assert sp_bags(prog) == set() == brute_force_races(prog)


def test_reads_do_not_race():
    prog = [("spawn", [("read", X)]), ("spawn", [("read", X)]), ("read", X), ("sync",)]
    assert sp_bags(prog) == set() == brute_force_races(prog)


def test_different_locations_do_not_race():
    prog = [("spawn", [("write", X)]), ("write", Y), ("sync",)]
    assert sp_bags(prog) == set() == brute_force_races(prog)


def test_nested_procedures():
    # the grandchild writes x; the parent reads x after the child returns but before its sync
    prog = [("spawn", [("spawn", [("write", X)])]), ("read", X)]
    assert sp_bags(prog) == {X} == brute_force_races(prog)
    # the child syncs its own child, but the parent has not synced the child
    prog = [("spawn", [("spawn", [("write", X)]), ("sync",)]), ("read", X), ("sync",), ("write", X)]
    assert sp_bags(prog) == {X} == brute_force_races(prog)
    # the implicit sync at the end of the child orders the grandchild before the parent's sync
    prog = [("spawn", [("spawn", [("write", X)])]), ("sync",), ("read", X)]
    assert sp_bags(prog) == set() == brute_force_races(prog)


def test_locks_remove_data_races_but_not_determinacy_races():
    # two parallel updates, each under lock L: x = x + 1 and x = 2 * x
    lock = frozenset({"L"})
    update = [("read", X, lock), ("write", X, lock)]
    prog = [("spawn", update), ("spawn", update), ("sync",)]
    assert brute_force_data_races(prog) == set()
    assert brute_force_races(prog) == {X} == sp_bags(prog)
    plain = [("read", X), ("write", X)]
    assert brute_force_data_races([("spawn", plain), ("spawn", update), ("sync",)]) == {X}


def test_sp_bags_equals_brute_force_on_random_programs():
    rng = random.Random(2024)
    seen_race = seen_free = 0
    for trial in range(3000):
        prog = random_program(rng, depth=rng.randint(0, 3), locs=rng.randint(1, 3), max_len=rng.randint(1, 5))
        expected = brute_force_races(prog)
        assert sp_bags(prog) == expected, prog
        seen_race += bool(expected)
        seen_free += not expected
    assert seen_race > 150 and seen_free > 150  # both outcomes are common


def test_bags_give_the_series_parallel_relation():
    # Corollary 9 of Feng and Leiserson: for u executed before v, u and v are parallel
    # exactly when the procedure of u is in a P-bag while v executes.
    rng = random.Random(7)
    for _ in range(1500):
        prog = random_program(rng, depth=3, locs=2, max_len=4)
        _, bags = sp_bags(prog, record_relation=True)
        assert bags == logically_parallel(prog), prog


def test_disjoint_sets():
    rng = random.Random(3)
    ds = DisjointSets()
    n = 200
    naive = list(range(n))  # naive[i] is a label of the set of i
    for i in range(n):
        ds.make_set(i, ("S", i))
    for _ in range(400):
        a, b = rng.randrange(n), rng.randrange(n)
        r = ds.union(a, b, ("P", a))
        old = naive[b]
        naive = [naive[a] if lab == old else lab for lab in naive]
        assert ds.tag[r] == ("P", a)
        assert ds.find(a) == ds.find(b) == r
    for i in range(n):
        for j in range(0, n, 17):
            assert (ds.find(i) == ds.find(j)) == (naive[i] == naive[j])
    assert max(ds.rank.values()) <= n.bit_length()  # union by rank keeps the rank at most lg n
