# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/higher-order-ivm/. The authors are listed in prov/0ABZ30.jsonl.

import random
from collections import Counter

import pytest

from higher_order_ivm import HigherOrderIVM, brute_force, map_definition

CHAIN = {"R": ("A", "B"), "S": ("B", "C"), "T": ("C", "D")}

QUERIES = [
    (CHAIN, ("A", "D"), ()),
    (CHAIN, (), ()),
    (CHAIN, ("C",), ("B",)),
    (CHAIN, ("A",), ("A", "D")),
    ({"R": ("A", "B"), "S": ("B", "C")}, ("A", "C"), ()),
    ({"R": ("A", "B"), "S": ("B", "C"), "T": ("C", "A")}, ("B",), ()),
    ({"R": ("A",), "S": ("B",)}, ("A", "B"), ()),
    ({"R": ("A", "B"), "S": ("A", "C"), "T": ("A", "D"), "U": ("D", "E")}, ("B", "E"), ("A",)),
    ({"R": ("A", "B")}, ("B",), ("A",)),
]


def check_all(ivm, rels, vals, group, atoms):
    assert ivm.result() == brute_force(atoms, rels, vals, group)
    for s in ivm.maps:
        if s != ivm.full:
            assert dict(ivm.maps[s]) == map_definition(ivm, rels, s)


def test_page_example() -> None:
    h = HigherOrderIVM(CHAIN, ("A", "D"))
    ups = [("R", (1, 10)), ("S", (10, 20)), ("T", (20, 5)), ("R", (2, 10)), ("T", (20, 7))]
    got = []
    for n, t in ups:
        h.update(n, t)
        got.append(h.result().get((), 0))
    assert got == [0, 0, 5, 15, 36]
    assert dict(h.maps[frozenset({"R"})]) == {(10,): 12}
    assert dict(h.maps[frozenset({"T"})]) == {(20,): 3}
    assert dict(h.maps[frozenset({"S", "T"})]) == {(10,): 3}
    h.update("R", (1, 10), -1)
    assert h.result() == {(): 24}


def test_against_recomputation() -> None:
    for seed in range(60):
        rng = random.Random(seed)
        for atoms, vals, group in QUERIES:
            h = HigherOrderIVM(atoms, vals, group)
            rels = {n: Counter() for n in atoms}
            for _ in range(25):
                n = rng.choice(list(atoms))
                live = [t for t, c in rels[n].items() if c > 0]
                if live and rng.random() < 0.35:
                    t, w = rng.choice(live), -1
                else:
                    t, w = tuple(rng.randrange(3) for _ in atoms[n]), rng.choice([1, 1, 2])
                h.update(n, t, w)
                rels[n][t] += w
                rels[n] = +rels[n]
                check_all(h, rels, vals, group, atoms)


def test_insert_then_delete_returns_to_empty() -> None:
    rng = random.Random(7)
    h = HigherOrderIVM(CHAIN, ("A", "D"), ("B",))
    ups = [(rng.choice("RST"), (rng.randrange(3), rng.randrange(3))) for _ in range(30)]
    for n, t in ups:
        h.update(n, t)
    for n, t in reversed(ups):
        h.update(n, t, -1)
    assert h.result() == {}
    assert all(not m for s, m in h.maps.items() if s != h.full)


def test_any_order_of_signed_updates() -> None:
    # A deletion may arrive before its insertion; the maps stay exact for negative weights.
    for seed in range(20):
        rng = random.Random(100 + seed)
        ups = [(rng.choice("RST"), (rng.randrange(3), rng.randrange(3)), rng.choice([-1, 1, 2])) for _ in range(20)]
        results = []
        for order in (ups, list(reversed(ups)), rng.sample(ups, len(ups))):
            h = HigherOrderIVM(CHAIN, ("A",), ("D",))
            rels = {n: Counter() for n in CHAIN}
            for n, t, w in order:
                h.update(n, t, w)
                rels[n][t] += w
            rels = {n: Counter({t: c for t, c in r.items() if c}) for n, r in rels.items()}
            check_all(h, rels, ("A",), ("D",), CHAIN)
            results.append(h.result())
        assert results[0] == results[1] == results[2]


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        HigherOrderIVM({"R": ("A", "A")})
    with pytest.raises(ValueError):
        HigherOrderIVM({"R": ("A",)}, ("Z",))
    h = HigherOrderIVM({"R": ("A", "B")})
    with pytest.raises(ValueError):
        h.update("R", (1,))
