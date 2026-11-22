# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dangling-pointer-nullification/. The authors are listed in prov/2R0MXX.jsonl.

import random

import pytest
from dangling_pointer_nullification import NULL_PAGE, WORD, DangNullHeap, FreeError, NullFault


def test_page_example() -> None:
    h = DangNullHeap(128, globals_size=16)  # null page [0, 16), globals [16, 32), heap from 32
    a = h.alloc(8)
    b = h.alloc(8)
    c = h.alloc(8)
    assert (a, b, c) == (32, 40, 48)
    h.store_ptr(b, a + 4)  # b[0] points into a
    h.store_ptr(c + 4, a)  # c[1] points to a
    h.store_ptr(16, a)  # a global points to a: not tracked
    assert h.shadow[a].inb == {40, 52}
    assert h.shadow[b].outb == {40: 32} and h.shadow[c].outb == {52: 32}
    reg = h.load_ptr(b)  # a copy in a register
    h.store(c + 4, 4, 7)  # an integer overwrites c[1]; the relation stays
    h.store_ptr(c + 4, a)  # and a pointer store puts it back
    h.free(a)
    assert h.load_ptr(b) == 0 and h.load_ptr(c + 4) == 0  # both heap copies are null
    with pytest.raises(NullFault):
        h.load(h.load_ptr(b), 1)
    assert h.load_ptr(16) == a  # the global copy is not nullified
    assert reg == a + 4  # nor is the register copy
    assert h.shadow[b].outb == {} and h.shadow[c].outb == {}
    h.check_invariant()


def test_stale_relation_is_checked_against_the_range() -> None:
    h = DangNullHeap(128, globals_size=16)
    a = h.alloc(8)
    b = h.alloc(8)
    h.store_ptr(b, a)
    h.store(b, 4, 99)  # an integer store is not traced
    h.free(a)
    assert h.load(b, 4) == 99  # 99 is not inside a, so it is left alone
    h.check_invariant()


def test_edges() -> None:
    h = DangNullHeap(64, globals_size=16, nullify_value=8)
    with pytest.raises(FreeError):
        h.free(40)
    h.free(0)  # free of null does nothing
    a = h.alloc(16)
    b = h.alloc(16)
    assert h.alloc(1) == 0
    h.store_ptr(b, a)
    h.store_ptr(a, a + 8)  # a self pointer
    h.free(a)
    assert h.load(b, 4) == 8 and h.load(a, 4) == 8
    with pytest.raises(NullFault):
        h.load(8, 1)
    with pytest.raises(ValueError):
        DangNullHeap(64, nullify_value=16)
    h.check_invariant()


def test_random_programs_against_relation_oracle() -> None:
    rng = random.Random(2015)
    counts = {"nullified": 0, "register_missed": 0, "global_missed": 0, "faults": 0}
    for _ in range(500):
        size = rng.choice([96, 160, 256])
        h = DangNullHeap(size, globals_size=16)
        mem = bytearray(size)
        objs: list[dict] = []
        rel: dict[int, int] = {}  # location -> object that the traced pointer there points into
        regs: list[int] = [0]

        def live_at(a: int) -> int | None:
            for k, o in enumerate(objs):
                if o["live"] and o["base"] <= a < o["base"] + o["n"]:
                    return k
            return None

        for _ in range(rng.randint(5, 50)):
            op = rng.random()
            if op < 0.2:
                n = rng.randint(4, 16)
                p = h.alloc(n)
                if p:
                    objs.append({"base": p, "n": n, "live": True})
                    mem[p:p + n] = bytes(n)
                    regs.append(p)
            elif op < 0.3:
                r = rng.choice(regs) + rng.randint(-4, 12)
                regs.append(max(r, 0))
            elif op < 0.6:
                live = [o for o in objs if o["live"]]
                if rng.random() < 0.15:
                    lhs = rng.randrange(NULL_PAGE, NULL_PAGE + 16 - WORD + 1)  # a global
                elif live and rng.random() < 0.7:
                    o = rng.choice(live)  # a word inside a live object
                    lhs = o["base"] + rng.randrange(o["n"] - WORD + 1)
                else:
                    lhs = rng.randrange(h.heap_start, size - WORD + 1)
                lhs -= lhs % WORD  # pointers are stored at aligned addresses
                rhs = rng.choice(regs)
                src = live_at(lhs)
                if src is not None:
                    rel.pop(lhs, None)
                    dst = live_at(rhs)
                    if dst is not None:
                        rel[lhs] = dst
                h.store_ptr(lhs, rhs)
                mem[lhs:lhs + WORD] = rhs.to_bytes(WORD, "little")
            elif op < 0.7:
                a = rng.randrange(NULL_PAGE, size - WORD + 1)
                v = rng.randrange(1 << 32) if rng.random() < 0.5 else rng.randrange(size)
                h.store(a, WORD, v)
                mem[a:a + WORD] = v.to_bytes(WORD, "little")
            elif op < 0.8:
                a = rng.randrange(NULL_PAGE, size - WORD + 1)
                assert h.load_ptr(a) == int.from_bytes(mem[a:a + WORD], "little")
                regs.append(h.load_ptr(a))
            elif op < 0.88:
                r = rng.choice(regs)
                if r < NULL_PAGE:
                    with pytest.raises(NullFault):
                        h.load(r, 1)
                    counts["faults"] += 1
                elif r < size:
                    assert h.load(r, 1) == mem[r]
            else:
                live = [k for k, o in enumerate(objs) if o["live"]]
                if not live:
                    continue
                x = rng.choice(live)
                o = objs[x]
                lo, hi = o["base"], o["base"] + o["n"]
                for lhs in [l for l, t in rel.items() if t == x]:
                    if lo <= int.from_bytes(mem[lhs:lhs + WORD], "little") < hi:
                        mem[lhs:lhs + WORD] = bytes(WORD)
                        counts["nullified"] += 1
                    del rel[lhs]
                for lhs in [l for l in rel if lo <= l < hi]:
                    del rel[lhs]
                h.free(lo)
                o["live"] = False
                counts["register_missed"] += sum(1 for r in regs if lo <= r < hi)
                counts["global_missed"] += sum(
                    1 for g in range(NULL_PAGE, NULL_PAGE + 16 - WORD + 1)
                    if lo <= int.from_bytes(mem[g:g + WORD], "little") < hi
                )
            assert h.mem == mem
            h.check_invariant()
    assert counts["nullified"] > 100 and counts["faults"] > 50
    assert counts["register_missed"] > 50 and counts["global_missed"] > 5
