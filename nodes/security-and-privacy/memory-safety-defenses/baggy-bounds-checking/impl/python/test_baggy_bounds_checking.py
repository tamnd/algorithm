# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baggy-bounds-checking/. The authors are listed in prov/81GP9H.jsonl.

import random

import pytest
from baggy_bounds_checking import HALF, SLOT, BaggyHeap, BoundsError


def test_page_example() -> None:
    h = BaggyHeap(8)  # 256 bytes, 16 slots; slot 0 is reserved
    a = h.alloc(20)
    assert a == 32  # padded to 32 bytes, aligned to 32
    assert list(h.table[2:4]) == [5, 5] and h.table[1] == 8
    b = h.alloc(10)
    assert b == 16  # padded to one slot
    h.store(h.add(a, 19), 1, 7)  # the last requested byte
    h.store(h.add(a, 25), 1, 9)  # in the padding: allowed
    end = h.add(a, 32)
    assert h.is_marked(end) and end & ~h.mark == 64
    with pytest.raises(BoundsError):
        h.load(end, 1)
    back = h.add(end, -1)
    assert back == 63 and h.load(back, 1) == 0
    with pytest.raises(BoundsError):
        h.add(a, 40)  # 8 or more bytes past the padded end
    low = h.add(a, -3)
    assert h.is_marked(low)
    with pytest.raises(BoundsError):
        h.store(h.add(a, 30), 4, 1)  # bytes 62 to 65 cross the end
    h.free(a)
    assert h.load(a, 1) == 0  # no temporal checking
    h.check_invariant()


def test_edges() -> None:
    h = BaggyHeap(6)  # 64 bytes
    with pytest.raises(BoundsError):
        h.free(0)
    a = h.alloc(32)
    assert a == 32 and h.alloc(17) == 0
    c = h.alloc(16)
    assert c == 16 and h.alloc(1) == 0
    with pytest.raises(BoundsError):
        h.free(a + 1)
    h.free(a)
    with pytest.raises(BoundsError):
        h.free(a)
    h.free(c)
    h.check_invariant()
    assert h.alloc(32) == 32
    with pytest.raises(ValueError):
        h.alloc(0)


def expected_value(h: BaggyHeap, base: int, padded: int, off: int) -> int | None:
    """The pointer that baggy bounds must hold for a live object, or None for an error."""
    if 0 <= off < padded:
        return base + off
    if -HALF <= off < padded + HALF:
        return (base + off) | h.mark
    return None


def test_random_programs_against_object_oracle() -> None:
    rng = random.Random(2009)
    counts = {"caught": 0, "padding": 0, "far": 0, "missed_uaf": 0}
    for _ in range(500):
        h = BaggyHeap(rng.choice([8, 9, 10]))
        objs: list[dict] = []
        vals: list[int] = []
        meta: list[tuple[int, int]] = []  # (object, intended offset)
        for _ in range(rng.randint(5, 40)):
            op = rng.random()
            if op < 0.25 or not vals:
                n = rng.randint(1, 70)
                p = h.alloc(n)
                if p:
                    padded = max(SLOT, 1 << (n - 1).bit_length())
                    assert p % padded == 0
                    for o in objs:
                        if o["live"]:
                            assert p + padded <= o["base"] or o["base"] + o["padded"] <= p
                    objs.append({"base": p, "n": n, "padded": padded, "live": True, "data": bytearray(padded)})
                    vals.append(p)
                    meta.append((len(objs) - 1, 0))
            elif op < 0.45:
                i = rng.randrange(len(vals))
                k = rng.randint(-20, 20)
                oid, off = meta[i]
                o = objs[oid]
                try:
                    got: int | None = h.add(vals[i], k)
                except BoundsError:
                    got = None
                if o["live"]:
                    want = expected_value(h, o["base"], o["padded"], off + k)
                    assert got == want
                    if want is None:
                        counts["far"] += 1
                if got is not None:
                    vals.append(got)
                    meta.append((oid, off + k))
            elif op < 0.85:
                i = rng.randrange(len(vals))
                w = rng.choice([1, 2, 4, 8])
                oid, off = meta[i]
                o = objs[oid]
                p = vals[i]
                try:
                    if rng.random() < 0.5:
                        v = rng.randrange(1 << (8 * w))
                        h.store(p, w, v)
                        for j, byte in enumerate(v.to_bytes(w, "little")):
                            for x in objs:  # a dangling store lands in whatever object holds the byte
                                if x["live"] and x["base"] <= p + j < x["base"] + x["padded"]:
                                    x["data"][p + j - x["base"]] = byte
                        ok, loaded = True, None
                    else:
                        ok, loaded = True, h.load(p, w)
                except BoundsError:
                    ok, loaded = False, None
                if o["live"]:
                    in_padded = 0 <= off and off + w <= o["padded"]
                    assert ok == in_padded
                    if loaded is not None:
                        assert loaded == int.from_bytes(o["data"][off:off + w], "little")
                    if not in_padded:
                        counts["caught"] += 1
                    elif off + w > o["n"]:
                        counts["padding"] += 1
                elif ok:
                    counts["missed_uaf"] += 1
            else:
                i = rng.randrange(len(vals))
                p = vals[i]
                o = next((x for x in objs if x["live"] and x["base"] == p), None)
                try:
                    h.free(p)
                    ok = True
                except BoundsError:
                    ok = False
                assert ok == (o is not None)
                if o is not None:
                    o["live"] = False
            h.check_invariant()
    assert counts["caught"] > 100 and counts["padding"] > 50
    assert counts["far"] > 30 and counts["missed_uaf"] > 10
