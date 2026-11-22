# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fat-pointer/. The authors are listed in prov/QJJ3SE.jsonl.

import random

import pytest
from fat_pointer import NULL, FatPointer, FatPointerHeap, SpatialError, TemporalError


def test_page_example() -> None:
    h = FatPointerHeap(64)
    a = h.alloc(8)
    assert a == FatPointer(1, 1, 9, 1)
    b = h.alloc(4)
    assert b == FatPointer(9, 9, 13, 2)
    q = h.add(a, 6)
    h.store(q, 2, 0x0102)
    assert h.load(h.add(a, 7), 1) == 0x01
    with pytest.raises(SpatialError):
        h.store(q, 4, 7)  # bytes 7 to 10, past the bound 9
    r = h.add(a, 8)  # one past the end: legal to form, not to use
    with pytest.raises(SpatialError):
        h.load(r, 1)
    h.free(a)
    c = h.alloc(8)  # first fit reuses the block of a
    assert c.base == a.base and c.cap == 3
    with pytest.raises(TemporalError):
        h.load(a, 1)  # in bounds of the new block, but the capability is dead
    assert h.load(c, 1) == 0
    h.check_invariant()


def test_edges() -> None:
    h = FatPointerHeap(16)
    with pytest.raises(SpatialError):
        h.load(NULL, 1)
    with pytest.raises(SpatialError):
        h.free(NULL)
    a = h.alloc(15)
    assert a.bound == 16
    assert h.alloc(1) == NULL
    with pytest.raises(SpatialError):
        h.free(h.add(a, 1))
    back = h.add(h.add(a, 40), -40)  # far out and back: the bounds never changed
    h.store(back, 1, 255)
    assert h.load(a, 1) == 255
    with pytest.raises(SpatialError):
        h.load(h.add(a, -1), 1)
    h.free(a)
    with pytest.raises(TemporalError):
        h.free(a)
    h.check_invariant()
    with pytest.raises(ValueError):
        h.alloc(0)


def outcome(fn) -> str:
    try:
        fn()
    except SpatialError:
        return "spatial"
    except TemporalError:
        return "temporal"
    return "ok"


def test_random_programs_against_object_oracle() -> None:
    rng = random.Random(1994)
    caught = {"spatial": 0, "temporal": 0}
    for _ in range(600):
        h = FatPointerHeap(rng.choice([48, 96, 256]))
        objs: list[dict] = []  # the oracle: size, live flag and bytes of each object
        fat: list[FatPointer] = []
        ref: list[tuple[int | None, int]] = []  # the oracle pointer: (object, offset)
        for _ in range(rng.randint(5, 40)):
            op = rng.random()
            if op < 0.25 or not fat:
                n = rng.randint(1, 16)
                p = h.alloc(n)
                if p == NULL:
                    fat.append(p)
                    ref.append((None, 0))
                else:
                    objs.append({"size": n, "live": True, "data": bytearray(n)})
                    fat.append(p)
                    ref.append((len(objs) - 1, 0))
            elif op < 0.45:
                i = rng.randrange(len(fat))
                k = rng.randint(-20, 20)
                fat.append(h.add(fat[i], k))
                ref.append((ref[i][0], ref[i][1] + k))
            elif op < 0.85:
                i = rng.randrange(len(fat))
                w = rng.choice([1, 2, 4])
                oid, off = ref[i]
                if oid is None or off < 0 or off + w > objs[oid]["size"]:
                    want = "spatial"
                elif not objs[oid]["live"]:
                    want = "temporal"
                else:
                    want = "ok"
                if rng.random() < 0.5:
                    v = rng.randrange(1 << (8 * w))
                    got = outcome(lambda: h.store(fat[i], w, v))
                    if want == "ok":
                        objs[oid]["data"][off:off + w] = v.to_bytes(w, "little")
                else:
                    box: list[int] = []
                    got = outcome(lambda: box.append(h.load(fat[i], w)))
                    if want == "ok":
                        assert box[0] == int.from_bytes(objs[oid]["data"][off:off + w], "little")
                assert got == want
                if want != "ok":
                    caught[want] += 1
            else:
                i = rng.randrange(len(fat))
                oid, off = ref[i]
                if oid is None or off != 0:
                    want = "spatial"
                elif not objs[oid]["live"]:
                    want = "temporal"
                else:
                    want = "ok"
                got = outcome(lambda: h.free(fat[i]))
                assert got == want
                if want == "ok":
                    objs[oid]["live"] = False
            h.check_invariant()
    assert caught["spatial"] > 200 and caught["temporal"] > 50
