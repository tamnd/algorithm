# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conflict-serializability/. The authors are listed in prov/YBK3Q3.jsonl.

import itertools
import random

from conflict_serializability import (
    brute_force_orders,
    conflict_equivalent,
    is_conflict_serializable,
    parse,
    serial,
    serialization_order,
    swap_closure,
    transactions,
)


def random_schedule(rng: random.Random, ntx: int, nops: int, items: str) -> list:
    tx = {t: [(rng.choice("rw"), t, rng.choice(items)) for _ in range(nops)] for t in range(1, ntx + 1)}
    out = []
    while any(tx.values()):
        t = rng.choice([t for t in tx if tx[t]])
        out.append(tx[t].pop(0))
    return out


def test_examples() -> None:
    s = parse("r1(x) w1(x) r2(x) r1(y) w2(x) w1(y)")
    assert serialization_order(s) == [1, 2]
    assert brute_force_orders(s) == [(1, 2)]
    lost_update = parse("r1(x) r2(x) w1(x) w2(x)")
    assert serialization_order(lost_update) is None
    assert brute_force_orders(lost_update) == []
    s3 = parse("r1(x) r2(y) r3(z) w1(y)")
    assert serialization_order(s3) == [2, 3, 1]
    assert sorted(brute_force_orders(s3)) == [(2, 1, 3), (2, 3, 1), (3, 2, 1)]


def test_view_but_not_conflict() -> None:
    s = parse("r1(x) w2(x) w1(x) w3(x)")
    assert not is_conflict_serializable(s)


def test_theorem_against_brute_force() -> None:
    rng = random.Random(2024)
    seen_yes = seen_no = 0
    for _ in range(600):
        s = random_schedule(rng, rng.randint(1, 4), rng.randint(1, 3), "xyz")
        order = serialization_order(s)
        brute = brute_force_orders(s)
        assert (order is not None) == bool(brute)
        if order is not None:
            assert tuple(order) in brute
            assert conflict_equivalent(s, serial(s, order))
            seen_yes += 1
        else:
            seen_no += 1
    assert seen_yes > 50 and seen_no > 50


def test_swaps_reach_exactly_the_equivalent_serial_schedules() -> None:
    rng = random.Random(5)
    for _ in range(120):
        s = random_schedule(rng, rng.randint(2, 3), rng.randint(1, 2), "xy")
        closure = swap_closure(s)
        for o in itertools.permutations(transactions(s)):
            ser = tuple(serial(s, o))
            assert (ser in closure) == conflict_equivalent(s, list(ser))
        for t in closure:
            assert conflict_equivalent(s, list(t))
