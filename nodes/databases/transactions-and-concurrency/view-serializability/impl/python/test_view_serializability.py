# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/view-serializability/. The authors are listed in prov/S03CR7.jsonl.

import itertools
import random

from view_serializability import (
    final_writes,
    has_blind_write,
    herbrand,
    is_view_serializable,
    parse,
    reads_from,
    serial,
    view_equivalent,
    view_serial_order,
)


def conflict_serializable(s) -> bool:
    """Reference test by brute force: some serial order keeps every conflicting pair."""

    def pairs(z):
        tagged = []
        count = {}
        for p in z:
            count[p[1]] = count.get(p[1], 0) + 1
            tagged.append((p, count[p[1]]))
        return {
            (a, b)
            for i, a in enumerate(tagged)
            for b in tagged[i + 1 :]
            if a[0][1] != b[0][1] and a[0][2] == b[0][2] and "w" in (a[0][0], b[0][0])
        }

    want = pairs(s)
    return any(pairs(serial(s, o)) == want for o in itertools.permutations(sorted({p[1] for p in s})))


def random_schedule(rng: random.Random, ntx: int, nops: int, items: str) -> list:
    tx = {t: [(rng.choice("rw"), t, rng.choice(items)) for _ in range(nops)] for t in range(1, ntx + 1)}
    out = []
    while any(tx.values()):
        t = rng.choice([t for t in tx if tx[t]])
        out.append(tx[t].pop(0))
    return out


def test_classic_example() -> None:
    s = parse("r1(x) w2(x) w1(x) w3(x)")
    assert reads_from(s) == {((1, 1), None)}
    assert final_writes(s) == {"x": (3, 1)}
    assert view_serial_order(s) == (1, 2, 3)
    assert not conflict_serializable(s)
    assert has_blind_write(s)


def test_non_examples() -> None:
    assert not is_view_serializable(parse("r1(x) r2(x) w1(x) w2(x)"))
    # Without the final blind write of T3 the example is not view serializable.
    assert not is_view_serializable(parse("r1(x) w2(x) w1(x)"))
    assert not is_view_serializable(parse("w1(x) w2(x) w2(y) w1(y)"))
    assert view_serial_order(parse("w1(x) w2(x) w2(y) w1(y) w3(x) w3(y)")) == (1, 2, 3)


def test_hierarchy_on_random_schedules() -> None:
    rng = random.Random(99)
    gap = 0
    for _ in range(1500):
        s = random_schedule(rng, rng.randint(2, 4), rng.randint(1, 3), "xy")
        vsr = is_view_serializable(s)
        csr = conflict_serializable(s)
        assert not csr or vsr
        if vsr and not csr:
            gap += 1
            assert has_blind_write(s)
        if not has_blind_write(s):
            assert vsr == csr
    assert gap > 0


def test_view_equivalent_means_same_values() -> None:
    rng = random.Random(4)
    for _ in range(400):
        s = random_schedule(rng, rng.randint(2, 4), rng.randint(1, 3), "xyz")
        for o in itertools.permutations(sorted({p[1] for p in s})):
            ser = serial(s, o)
            if view_equivalent(s, ser):
                assert herbrand(s) == herbrand(ser)
