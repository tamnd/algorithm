# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/addresssanitizer/. The authors are listed in prov/B574DH.jsonl.

import random
from collections import deque

import pytest
from addresssanitizer import REDZONE, ASanError, ASanHeap, round_up


def test_page_example() -> None:
    h = ASanHeap(256, quarantine_limit=64)
    p = h.malloc(13)  # chunk [0, 48): redzone, 16 bytes for the object, redzone
    q = h.malloc(8)  # chunk [48, 88)
    assert (p, q) == (16, 64)
    assert [h.mem[h.shadow_addr(a)] for a in range(0, 48, 8)] == [0xFA, 0xFA, 0, 5, 0xFA, 0xFA]
    h.store(p + 12, 1, 7)
    assert h.load(p + 12, 1) == 7 and h.load(p + 8, 4) == 0
    for a, w in [(p + 13, 1), (p + 12, 4), (p - 8, 8), (p + 16, 1)]:
        with pytest.raises(ASanError) as e:
            h.load(a, w)
        assert e.value.kind == "heap-buffer-overflow"
    h.free(p)  # the chunk of 48 bytes goes into the quarantine
    with pytest.raises(ASanError) as e:
        h.load(p, 1)
    assert e.value.kind == "heap-use-after-free"
    with pytest.raises(ASanError) as e:
        h.free(p)
    assert e.value.kind == "double-free"
    h.free(q)  # 88 bytes in the quarantine: the chunk of p leaves it
    r = h.malloc(13)
    assert r == p  # the memory of p is reused
    assert h.load(p, 1) == 0  # so the stale pointer p is not reported
    with pytest.raises(ASanError):
        h.load(q, 1)  # q is still in the quarantine
    h.check_invariant()


def test_edges() -> None:
    h = ASanHeap(128, quarantine_limit=0)
    with pytest.raises(ValueError):
        h.malloc(0)
    with pytest.raises(ValueError):
        ASanHeap(100)
    p = h.malloc(16)
    h.store(p + 8, 8, -1)
    assert h.load(p + 8, 8) == (1 << 64) - 1
    with pytest.raises(ValueError):
        h.load(p + 2, 4)  # not aligned
    with pytest.raises(ValueError):
        h.load(p, 3)
    with pytest.raises(ASanError) as e:
        h.free(p + 8)
    assert e.value.kind == "bad-free"
    assert h.malloc(100) == 0  # no hole is large enough
    h.free(p)  # a quarantine of 0 bytes reuses the chunk at once
    assert h.malloc(16) == p
    h.check_invariant()


def test_random_programs_against_byte_oracle() -> None:
    rng = random.Random(2012)
    counts = {"caught": 0, "overflow_missed": 0, "uaf_missed": 0, "uaf_caught": 0}
    for _ in range(500):
        size = rng.choice([256, 512])
        limit = rng.choice([0, 64, 256])
        h = ASanHeap(size, quarantine_limit=limit)
        data = bytearray(size)
        objs: list[dict] = []
        quarantine: deque[tuple[int, int]] = deque()  # (chunk start, chunk length)
        held = 0

        def addressable(a: int) -> bool:
            return any(o["live"] and o["base"] <= a < o["base"] + o["n"] for o in objs)

        for _ in range(rng.randint(10, 60)):
            op = rng.random()
            if op < 0.25:
                n = rng.randint(1, 40)
                b = h.malloc(n)
                if b:
                    lo, hi = b - REDZONE, b + round_up(n) + REDZONE
                    for o in objs:  # disjoint from every live chunk
                        if o["live"]:
                            assert hi <= o["base"] - REDZONE or o["base"] + round_up(o["n"]) + REDZONE <= lo
                    for c, l in quarantine:  # and from every chunk in the quarantine
                        assert hi <= c or c + l <= lo
                    objs.append({"base": b, "n": n, "live": True})
            elif op < 0.37:
                if not objs:
                    continue
                o = rng.choice(objs)
                same = [x for x in objs if x["live"] and x["base"] == o["base"]]
                if same:  # a stale base that was reused frees the new object
                    o = same[0]
                    h.free(o["base"])
                    o["live"] = False
                    length = 2 * REDZONE + round_up(o["n"])
                    quarantine.append((o["base"] - REDZONE, length))
                    held += length
                    while held > limit:
                        held -= quarantine.popleft()[1]
                else:
                    with pytest.raises(ASanError):
                        h.free(o["base"])
            elif objs:
                o = rng.choice(objs)
                w = rng.choice([1, 2, 4, 8])
                a = o["base"] + rng.randint(-40, o["n"] + 40)
                a -= a % w
                if a < 0 or a + w > size:
                    continue
                bad = not all(addressable(x) for x in range(a, a + w))
                real_bug = not o["live"] or a < o["base"] or a + w > o["base"] + o["n"]
                assert not bad or real_bug  # an access inside a live object is never a bug
                try:
                    if op < 0.7:
                        v = rng.randrange(1 << (8 * w))
                        h.store(a, w, v)
                        data[a:a + w] = v.to_bytes(w, "little")
                    else:
                        assert h.load(a, w) == int.from_bytes(data[a:a + w], "little")
                    reported = False
                except ASanError:
                    reported = True
                assert reported == bad  # exact for aligned accesses
                if real_bug and reported:
                    counts["caught"] += 1
                    counts["uaf_caught"] += not o["live"]
                elif real_bug:
                    counts["uaf_missed" if not o["live"] else "overflow_missed"] += 1
            assert h.mem[:size] == data
            h.check_invariant()
    assert counts["caught"] > 1000 and counts["uaf_caught"] > 200
    assert counts["overflow_missed"] > 20 and counts["uaf_missed"] > 20
