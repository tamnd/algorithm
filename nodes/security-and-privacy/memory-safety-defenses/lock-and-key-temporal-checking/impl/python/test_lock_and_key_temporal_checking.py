# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-and-key-temporal-checking/. The authors are listed in prov/NYGPH2.jsonl.

import random

import pytest
from lock_and_key_temporal_checking import (
    NULL,
    WORD,
    AccessError,
    KeyedPtr,
    LockAndKeyHeap,
    TemporalError,
)


def test_page_example() -> None:
    h = LockAndKeyHeap(64)
    a = h.alloc(8)
    assert a == KeyedPtr(1, 1, 1) and h.locks[1] == 1
    cell = h.alloc(4)
    assert cell == KeyedPtr(9, 2, 2)
    q = h.add(a, 4)
    h.store(q, 1, 7)
    h.store_ptr(cell, q)
    assert h.meta[9] == (1, 1)
    h.free(a)
    assert h.locks[1] == 0
    with pytest.raises(TemporalError):
        h.load(q, 1)  # a copy in a register
    r = h.load_ptr(cell)
    assert r == q
    with pytest.raises(TemporalError):
        h.load(r, 1)  # a copy that was stored in memory
    c = h.alloc(8)
    assert c == KeyedPtr(1, 3, 1)  # same block, same lock location, new key
    with pytest.raises(TemporalError):
        h.load(a, 1)  # the lock now holds 3, not 1
    with pytest.raises(TemporalError):
        h.free(a)  # double free
    assert h.load(c, 1) == 0
    h.check_invariant()


def test_edges() -> None:
    h = LockAndKeyHeap(16)
    with pytest.raises(TemporalError):
        h.load(NULL, 1)
    with pytest.raises(TemporalError):
        h.load(h.int_to_ptr(3), 1)
    a = h.alloc(15)
    assert h.alloc(1) == NULL
    with pytest.raises(AccessError):
        h.free(h.add(a, 2))
    other = h.load_ptr(a)  # no entry: no valid key
    with pytest.raises(TemporalError):
        h.load(other, 1)
    h.free(a)
    h.check_invariant()
    with pytest.raises(ValueError):
        h.alloc(0)


def test_random_programs_against_object_oracle() -> None:
    rng = random.Random(2010)
    counts = {"uaf": 0, "reuse": 0, "double": 0, "ok": 0}
    for _ in range(600):
        h = LockAndKeyHeap(rng.choice([48, 96, 200]))
        objs: list[dict] = []
        regs: list[KeyedPtr] = []
        intent: list[tuple[int, int] | None] = []  # (object, offset) of each register pointer
        slots: dict[int, tuple[int, int] | None] = {}  # address -> intent of the pointer stored there

        def forget(a: int, w: int) -> None:
            for loc in [x for x in slots if x < a + w and a < x + WORD]:
                del slots[loc]

        def reused(o: dict) -> bool:
            return any(x["live"] and x["base"] < o["base"] + o["n"] and o["base"] < x["base"] + x["n"] for x in objs)

        for _ in range(rng.randint(5, 50)):
            op = rng.random()
            if op < 0.2 or not regs:
                n = rng.randint(1, 16)
                p = h.alloc(n)
                if p != NULL:
                    objs.append({"base": p.value, "n": n, "live": True, "data": bytearray(n)})
                    regs.append(p)
                    intent.append((len(objs) - 1, 0))
                continue
            i = rng.randrange(len(regs))
            p, t = regs[i], intent[i]
            if t is None:  # loaded from a cell an integer store overwrote: not tracked
                continue
            o = objs[t[0]]
            if op < 0.35:
                k = rng.randrange(o["n"]) - t[1]  # stay in bounds: only temporal errors happen
                regs.append(h.add(p, k))
                intent.append((t[0], t[1] + k))
            elif op < 0.75:
                w = rng.choice([1, 2, 4])
                off = t[1]
                w = min(w, o["n"] - off)
                try:
                    if rng.random() < 0.5:
                        v = rng.randrange(1 << (8 * w))
                        h.store(p, w, v)
                        o["data"][off:off + w] = v.to_bytes(w, "little")
                        forget(p.value, w)
                    else:
                        assert h.load(p, w) == int.from_bytes(o["data"][off:off + w], "little")
                    ok = True
                except TemporalError:
                    ok = False
                assert ok == o["live"]
                if not ok:
                    counts["reuse" if reused(o) else "uaf"] += 1
                else:
                    counts["ok"] += 1
            elif op < 0.85 and o["n"] - t[1] >= WORD:
                j = rng.randrange(len(regs))
                try:
                    h.store_ptr(p, regs[j])
                    ok = True
                except TemporalError:
                    ok = False
                assert ok == o["live"]
                if ok:
                    o["data"][t[1]:t[1] + WORD] = (regs[j].value % (1 << 32)).to_bytes(WORD, "little")
                    forget(p.value, WORD)
                    slots[p.value] = intent[j]
            elif op < 0.92 and o["n"] - t[1] >= WORD:
                try:
                    q = h.load_ptr(p)
                    ok = True
                except TemporalError:
                    ok = False
                assert ok == o["live"]
                if ok:
                    regs.append(q)
                    intent.append(slots.get(p.value))
            else:
                try:
                    h.free(p)
                    got = "ok"
                except TemporalError:
                    got = "temporal"
                except AccessError:
                    got = "interior"
                want = "temporal" if not o["live"] else ("ok" if t[1] == 0 else "interior")
                assert got == want
                if got == "ok":
                    o["live"] = False
                if got == "temporal":
                    counts["double"] += 1
            h.check_invariant()
    assert counts["uaf"] > 50 and counts["reuse"] > 50 and counts["double"] > 50 and counts["ok"] > 1000
