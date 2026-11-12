# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timestamp-ordering/. The authors are listed in prov/X0WMGA.jsonl.

import random

from timestamp_ordering import run_to, run_to_on_schedule, start_timestamps


def parse(s: str) -> list:
    return [(a[0], int(a[1]), a[3]) for a in s.split()]


def conflict(p, q) -> bool:
    return p[1] != q[1] and p[2] == q[2] and "w" in (p[0], q[0])


def herbrand(s: list) -> tuple[dict, dict]:
    """Values under the Herbrand reading: a write depends on all earlier reads of its transaction."""
    db: dict = {}
    seen: dict = {}
    for op, t, x in s:
        if op == "r":
            seen.setdefault(t, []).append(db.get(x, x + "0"))
        else:
            db[x] = (t, len(seen.get(t, [])), tuple(seen.get(t, [])))
    return db, seen


def random_schedule(rng: random.Random) -> list:
    progs = {
        t: [(rng.choice("rw"), t, rng.choice("xyz")) for _ in range(rng.randint(1, 3))]
        for t in range(1, rng.randint(2, 4) + 1)
    }
    s = []
    while any(progs.values()):
        t = rng.choice([t for t in progs if progs[t]])
        s.append(progs[t].pop(0))
    return s


def test_examples() -> None:
    # Accepted by TO, not producible by 2PL: T3 starts first, then T1, then T2.
    s = parse("r3(z) r1(x) w2(x) w3(y) w1(y)")
    assert run_to_on_schedule(s) == (s, set())
    # Accepted by 2PL, rejected by TO: T2 is older but reads x after T1 wrote it.
    s = parse("r2(z) w1(x) r2(x)")
    out, rejected = run_to_on_schedule(s)
    assert rejected == {2}
    assert out == parse("r2(z) w1(x)")
    # A late write: T1 writes x after the younger T2 read it.
    out, rejected = run_to_on_schedule(parse("r1(y) r2(x) w1(x)"))
    assert rejected == {1}


def test_accepts_exactly_the_schedules_in_timestamp_order() -> None:
    rng = random.Random(4)
    for _ in range(3000):
        s = random_schedule(rng)
        ts = start_timestamps(s)
        in_order = all(
            ts[p[1]] < ts[q[1]] for i, p in enumerate(s) for q in s[i + 1 :] if conflict(p, q)
        )
        out, rejected = run_to_on_schedule(s)
        assert (not rejected) == in_order
        assert (out == s) == in_order


def test_accepted_conflicts_are_in_timestamp_order() -> None:
    rng = random.Random(5)
    for _ in range(3000):
        s = random_schedule(rng)
        ts = start_timestamps(s)
        out, rejected = run_to_on_schedule(s)
        for i, p in enumerate(out):
            for q in out[i + 1 :]:
                if conflict(p, q):
                    assert ts[p[1]] < ts[q[1]]


def test_fixpoint_runs_equal_serial_in_timestamp_order() -> None:
    rng = random.Random(6)
    nontrivial = 0
    for _ in range(2000):
        s = random_schedule(rng)
        ts = start_timestamps(s)
        while True:
            out, rejected = run_to_on_schedule(s, ts)
            if not rejected:
                break
            s = [p for p in s if p[1] not in rejected]
        serial = sorted(s, key=lambda p: ts[p[1]])  # sort is stable
        assert herbrand(out) == herbrand(serial)
        nontrivial += out != serial
    assert nontrivial > 100


def test_with_restarts() -> None:
    rng = random.Random(7)
    restarts = 0
    for _ in range(500):
        progs = {
            t: [(rng.choice("rw"), rng.choice("xyz")) for _ in range(rng.randint(1, 4))]
            for t in range(1, rng.randint(2, 5) + 1)
        }
        out = run_to(progs, rng)
        s, ts = out["committed"], out["ts"]
        for t in progs:
            assert [(op, x) for op, u, x in s if u == t] == progs[t]
        for i, p in enumerate(s):
            for q in s[i + 1 :]:
                if conflict(p, q):
                    assert ts[p[1]] < ts[q[1]]
        restarts += out["restarts"]
    assert restarts > 0
