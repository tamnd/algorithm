# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thomas-write-rule/. The authors are listed in prov/NVC9CE.jsonl.

import random

from thomas_write_rule import (
    conflict_serializable,
    run_twr,
    serial,
    start_timestamps,
    view_of,
    view_serial_orders,
)


def parse(s: str) -> list:
    return [(a[0], int(a[1]), a[3]) for a in s.split()]


def random_schedule(rng: random.Random) -> list:
    progs = {
        t: [(rng.choice("rww"), t, rng.choice("xy")) for _ in range(rng.randint(1, 3))]
        for t in range(1, rng.randint(2, 4) + 1)
    }
    s = []
    while any(progs.values()):
        t = rng.choice([t for t in progs if progs[t]])
        s.append(progs[t].pop(0))
    return s


def fixpoint(s: list) -> tuple[list, dict, dict]:
    """Drop rejected transactions and run again, until nothing is rejected."""
    ts = start_timestamps(s)
    while True:
        out = run_twr(s, ts)
        if not out["rejected"]:
            return s, ts, out
        s = [p for p in s if p[1] not in out["rejected"]]


def test_view_but_not_conflict_serializable() -> None:
    s = parse("r1(x) w2(x) w1(x) w3(x)")
    out = run_twr(s)
    assert out["rejected"] == set()
    assert out["ignored"] == [(2, ("w", 1, "x"))]
    assert out["executed"] == parse("r1(x) w2(x) w3(x)")
    assert not conflict_serializable(s)
    assert view_serial_orders(s) == [(1, 2, 3)]


def test_accepted_but_plain_schedule_not_view_serializable() -> None:
    s = parse("r1(x) w2(x) w1(x)")
    out = run_twr(s)
    assert out["rejected"] == set() and out["ignored"] == [(2, ("w", 1, "x"))]
    assert view_serial_orders(s) == []  # the plain schedule is not VSR
    assert view_serial_orders(out["executed"]) == [(1, 2)]


def test_basic_to_would_reject() -> None:
    # The obsolete write is skipped, but a write after a younger read is still rejected.
    assert run_twr(parse("r1(y) r2(x) w1(x)"))["rejected"] == {1}
    out = run_twr(parse("r1(y) w2(x) w1(x)"))
    assert out["rejected"] == set() and out["ignored"] == [(2, ("w", 1, "x"))]


def overwritten_before_read(s: list, pos: int, dead: set) -> bool:
    """Is the write at pos followed by a live write of its item, with no read of it between?"""
    x = s[pos][2]
    for j in range(pos + 1, len(s)):
        op, _, y = s[j]
        if y != x:
            continue
        if op == "r":
            return False
        if j not in dead:
            return True
    return False


def test_random_schedules() -> None:
    rng = random.Random(11)
    gap = 0
    for _ in range(3000):
        s, ts, out = fixpoint(random_schedule(rng))
        order = sorted(ts, key=ts.__getitem__)
        order = [t for t in order if any(p[1] == t for p in s)]
        ex = out["executed"]
        # (1) every conflict among executed actions is in timestamp order
        for i, p in enumerate(ex):
            for q in ex[i + 1 :]:
                if p[1] != q[1] and p[2] == q[2] and "w" in (p[0], q[0]):
                    assert ts[p[1]] < ts[q[1]]
        # (2) reads-from and final writes equal those of the serial run in
        #     timestamp order, where the ignored writes count as never done
        dead = {pos for pos, _ in out["ignored"]}
        live = [p for i, p in enumerate(s) if i not in dead]
        assert view_of(ex) == view_of(serial(live, order))
        assert view_of(serial(live, order))[1] == view_of(serial(s, order))[1]
        # (3) if each ignored write is overwritten before x is read again, the
        #     plain schedule is view equivalent to the timestamp order
        if all(overwritten_before_read(s, pos, dead) for pos, _ in out["ignored"]):
            assert tuple(order) in view_serial_orders(s)
            gap += not conflict_serializable(s)
    assert gap > 0
