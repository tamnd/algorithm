# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/km-anonymity/. The authors are listed in prov/YFDA8G.jsonl.

import random
from collections import Counter
from itertools import combinations

from km_anonymity import generalize, is_km_anonymous

D = [{"a1", "b1", "b2"}, {"a2", "b1"}, {"a2", "b1", "b2"}, {"a1", "a2", "b2"}]
TO_A = {"a1": "A", "a2": "A"}
TO_B = {"b1": "B", "b2": "B"}


def test_example() -> None:
    assert is_km_anonymous(D, 2, 1)
    assert not is_km_anonymous(D, 2, 2)
    da = generalize(D, TO_A)
    assert da == [frozenset("A b1 b2".split()), frozenset({"A", "b1"}), frozenset("A b1 b2".split()), frozenset({"A", "b2"})]
    assert is_km_anonymous(da, 2, 2)
    assert is_km_anonymous(da, 2, 3)
    # not 2-anonymous as whole transactions
    assert min(Counter(da).values()) == 1
    assert not is_km_anonymous(generalize(D, TO_B), 2, 2)
    everything = {x: "ALL" for x in ["a1", "a2", "b1", "b2"]}
    assert generalize(D, everything) == [frozenset({"ALL"})] * 4
    assert is_km_anonymous(generalize(D, everything), 2, 4)


def test_edges() -> None:
    assert is_km_anonymous([], 5, 3)
    assert is_km_anonymous([{"x"}], 1, 2)
    assert not is_km_anonymous([{"x"}], 2, 1)
    assert is_km_anonymous([{"x"}], 2, 0)
    assert is_km_anonymous([["x", "x"], ["x"]], 2, 2)


def oracle(db: list[set[str]], k: int, m: int) -> bool:
    universe = sorted(set().union(*db)) if db else []
    for size in range(1, m + 1):
        for subset in combinations(universe, size):
            s = set(subset)
            support = sum(1 for t in db if s <= t)
            if 0 < support < k:
                return False
    return True


def random_db(rng: random.Random) -> list[set[str]]:
    items = "abcdef"[: rng.randint(1, 6)]
    return [set(rng.sample(items, rng.randint(1, len(items)))) for _ in range(rng.randint(0, 10))]


def test_against_oracle() -> None:
    rng = random.Random(31)
    for _ in range(600):
        db = random_db(rng)
        k = rng.randint(1, 4)
        m = rng.randint(1, 4)
        assert is_km_anonymous(db, k, m) == oracle(db, k, m)


def test_theorems() -> None:
    rng = random.Random(32)
    parent = {"a": "X", "b": "X", "c": "Y", "d": "Y", "e": "Z", "f": "Z"}
    top = {"X": "ALL", "Y": "ALL", "Z": "ALL"}
    for _ in range(500):
        db = random_db(rng)
        k = rng.randint(1, 4)
        m = rng.randint(1, 4)
        ok = is_km_anonymous(db, k, m)
        # anti-monotone in m and in k
        if ok:
            assert is_km_anonymous(db, k, m - 1)
            assert is_km_anonymous(db, k - 1 or 1, m)
        # coarser cuts stay anonymous
        coarse = generalize(db, parent)
        if ok:
            assert is_km_anonymous(coarse, k, m)
        if is_km_anonymous(coarse, k, m):
            assert is_km_anonymous(generalize(coarse, top), k, m)
        # whole-transaction k-anonymity implies km-anonymity for every m
        copies = [t for t in db for _ in range(k)]
        assert is_km_anonymous(copies, k, 6)
