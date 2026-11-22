# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jones-kelly-bounds-checking/. The authors are listed in prov/F1X4NS.jsonl.

import random

import pytest
from jones_kelly_bounds_checking import ILLEGAL, BoundsError, JonesKellyHeap


def test_page_example() -> None:
    h = JonesKellyHeap(64)
    a = h.alloc(8)
    b = h.alloc(4)
    assert (a, b) == (1, 10)  # bytes 1 to 8, pad byte 9, then b
    assert h.lookup(9) == a and h.lookup(10) == b
    end = h.add(a, 8)
    assert end == 9  # one past the end: a legal value
    with pytest.raises(BoundsError):
        h.load(end, 1)
    assert h.add(a, 9) == ILLEGAL  # would point at b
    q = h.add(a, 6)
    h.store(q, 2, 0x0102)
    with pytest.raises(BoundsError):
        h.store(q, 4, 7)  # 6 + 4 > 8
    with pytest.raises(BoundsError):
        h.add(h.add(a, 12), -12)  # out and back: a false alarm
    h.free(a)
    with pytest.raises(BoundsError):
        h.load(a, 1)  # the address is in no object
    c = h.alloc(8)
    assert c == a
    assert h.load(a, 1) == 0  # the old pointer now finds c: a missed use after free
    h.check_invariant()


def test_edges() -> None:
    h = JonesKellyHeap(16)
    with pytest.raises(BoundsError):
        h.load(ILLEGAL, 1)
    with pytest.raises(BoundsError):
        h.free(3)
    a = h.alloc(14)
    assert a == 1 and h.alloc(1) == 0
    with pytest.raises(BoundsError):
        h.free(a + 1)
    assert h.add(a, -1) == ILLEGAL
    assert h.add(0, 5) == 5  # a pointer outside every object is not checked by add
    h.free(a)
    with pytest.raises(BoundsError):
        h.free(a)
    with pytest.raises(ValueError):
        h.alloc(0)
    h.check_invariant()


def oracle_find(objs: list[dict], p: int) -> dict | None:
    """Linear scan over the live objects; [base, base + size] includes the pad byte."""
    for o in objs:
        if o["live"] and o["base"] <= p <= o["base"] + o["size"]:
            return o
    return None


def test_random_programs_against_object_oracle() -> None:
    rng = random.Random(1997)
    counts = {"caught": 0, "missed_uaf": 0, "false_alarm": 0, "ok": 0}
    for _ in range(600):
        h = JonesKellyHeap(rng.choice([40, 96, 200]))
        objs: list[dict] = []
        vals: list[int] = []  # the values the checked program holds
        meta: list[tuple[int, int, bool]] = []  # (object, offset, never left [0, size])
        for _ in range(rng.randint(5, 40)):
            op = rng.random()
            if op < 0.25 or not vals:
                n = rng.randint(1, 12)
                p = h.alloc(n)
                if p:
                    for o in objs:
                        if o["live"]:
                            assert p + n + 1 <= o["base"] or o["base"] + o["size"] + 1 <= p
                    objs.append({"base": p, "size": n, "live": True, "data": bytearray(n)})
                    vals.append(p)
                    meta.append((len(objs) - 1, 0, True))
            elif op < 0.45:
                i = rng.randrange(len(vals))
                k = rng.randint(-14, 14)
                p = vals[i]
                o = None if p == ILLEGAL else oracle_find(objs, p)
                if p == ILLEGAL:
                    want = "error"
                elif o is None or o["base"] <= p + k <= o["base"] + o["size"]:
                    want = p + k
                else:
                    want = ILLEGAL
                try:
                    got: int | str = h.add(p, k)
                except BoundsError:
                    got = "error"
                assert got == want
                oid, off, _ = meta[i]
                if got == "error" and objs[oid]["live"] and 0 <= off + k <= objs[oid]["size"]:
                    counts["false_alarm"] += 1  # out and back into the object
                if got != "error":
                    oid, off, clean = meta[i]
                    noff = off + k
                    vals.append(got)
                    meta.append((oid, noff, clean and 0 <= noff <= objs[oid]["size"]))
            elif op < 0.85:
                i = rng.randrange(len(vals))
                w = rng.choice([1, 2, 4])
                p = vals[i]
                o = None if p == ILLEGAL else oracle_find(objs, p)
                want_ok = o is not None and p + w <= o["base"] + o["size"]
                try:
                    if rng.random() < 0.5:
                        v = rng.randrange(1 << (8 * w))
                        h.store(p, w, v)
                        off = p - o["base"]
                        o["data"][off:off + w] = v.to_bytes(w, "little")
                    else:
                        got_v = h.load(p, w)
                        off = p - o["base"]
                        assert got_v == int.from_bytes(o["data"][off:off + w], "little")
                    got_ok = True
                except BoundsError:
                    got_ok = False
                assert got_ok == want_ok
                oid, off, clean = meta[i]
                intended = objs[oid]
                if intended["live"]:
                    in_bounds = 0 <= off and off + w <= intended["size"]
                    if not in_bounds:
                        assert not got_ok  # every spatial error on a live object is caught
                        counts["caught"] += 1
                    elif clean:
                        assert got_ok  # no false alarm when the pointer never left
                        counts["ok"] += 1
                    elif not got_ok:
                        counts["false_alarm"] += 1
                elif got_ok:
                    counts["missed_uaf"] += 1
            else:
                i = rng.randrange(len(vals))
                p = vals[i]
                o = next((x for x in objs if x["live"] and x["base"] == p), None)
                try:
                    h.free(p)
                    got_ok = True
                except BoundsError:
                    got_ok = False
                assert got_ok == (o is not None)
                if o is not None:
                    o["live"] = False
            h.check_invariant()
    assert counts["caught"] > 300 and counts["ok"] > 300
    assert counts["false_alarm"] > 0 and counts["missed_uaf"] > 0
