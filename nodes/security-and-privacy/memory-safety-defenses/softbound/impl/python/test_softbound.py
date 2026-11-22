# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/softbound/. The authors are listed in prov/4RX746.jsonl.

import random

import pytest
from softbound import NULL, WORD, BoundsError, Ptr, SoftBoundMemory


def test_page_example() -> None:
    m = SoftBoundMemory(64)
    s = m.alloc(12)  # a struct: char name[8]; int count;
    assert s == Ptr(4, 4, 16)
    cell = m.alloc(4)  # a cell that holds one pointer
    assert cell == Ptr(16, 16, 20)
    name = m.field(s, 0, 8)
    assert name == Ptr(4, 4, 12)
    m.store(m.add(name, 7), 1, 65)
    with pytest.raises(BoundsError):
        m.store(m.add(name, 8), 1, 66)  # into count: caught by the field bounds
    m.store(m.add(s, 8), 4, 3)  # count itself, through s
    m.store_ptr(cell, name)
    assert m.meta == {16: (4, 12)}
    q = m.load_ptr(cell)
    assert q == name
    with pytest.raises(BoundsError):
        m.load(m.add(q, 8), 1)  # the bounds came back from the table
    m.store(cell, 4, 4)  # an integer store over the pointer leaves the entry
    assert m.load_ptr(cell) == Ptr(4, 4, 12)
    forged = m.int_to_ptr(8)
    with pytest.raises(BoundsError):
        m.load(forged, 1)
    other = m.alloc(4)
    assert m.load_ptr(other) == Ptr(0, 0, 0)  # no entry: empty bounds


def test_edges() -> None:
    m = SoftBoundMemory(16)
    with pytest.raises(BoundsError):
        m.load(NULL, 1)
    a = m.alloc(12)
    assert m.alloc(1) == NULL
    with pytest.raises(BoundsError):
        m.store_ptr(m.add(a, 9), a)  # a 4-byte pointer store needs 4 bytes in bounds
    wide = m.field(a, -4, 40)
    assert (wide.base, wide.bound) == (a.base, a.bound)  # a field never widens the bounds
    empty = m.field(a, 20, 4)
    assert empty.base == empty.bound
    with pytest.raises(ValueError):
        m.alloc(0)


def test_random_programs_against_provenance_oracle() -> None:
    rng = random.Random(2009)
    caught = 0
    for _ in range(600):
        size = rng.choice([64, 128, 256])
        m = SoftBoundMemory(size)
        objs: list[tuple[int, int]] = []  # (base, size)
        mem = bytearray(size)  # the oracle copy of memory
        regs: list[Ptr] = []
        intent: list[tuple[int, int, int, int] | None] = []  # (object, offset, lo, hi) relative to the base
        slots: dict[int, tuple[int, int, int, int]] = {}  # address -> intent of the pointer stored there

        def forget(a: int, w: int) -> None:
            for loc in [x for x in slots if x < a + w and a < x + WORD]:
                del slots[loc]

        def within_one_object(lo: int, hi: int) -> bool:
            return lo == hi or any(b <= lo and hi <= b + n for b, n in objs)

        for _ in range(rng.randint(5, 50)):
            op = rng.random()
            if op < 0.15 or not regs:
                n = rng.randint(1, 16)
                p = m.alloc(n)
                if p != NULL:
                    objs.append((p.base, n))
                    regs.append(p)
                    intent.append((len(objs) - 1, 0, 0, n))
                continue
            i = rng.randrange(len(regs))
            p, t = regs[i], intent[i]
            if op < 0.30:
                k = rng.randint(-10, 10)
                regs.append(m.add(p, k))
                intent.append(None if t is None else (t[0], t[1] + k, t[2], t[3]))
                continue
            if op < 0.38:
                off, sz = rng.randint(-2, 10), rng.randint(0, 8)
                q = m.field(p, off, sz)
                regs.append(q)
                if t is None:
                    intent.append(None)
                else:
                    o = t[1] + off
                    lo = max(o, t[2])
                    intent.append((t[0], o, lo, max(lo, min(o + sz, t[3]))))
                continue
            if op < 0.42:
                regs.append(m.int_to_ptr(rng.randrange(size)))
                intent.append(None)
                continue
            w = WORD if op >= 0.75 else rng.choice([1, 2, 4])
            if t is not None:
                base = objs[t[0]][0]
                assert (p.value, p.base, p.bound) == (base + t[1], base + t[2], base + t[3])
                want_ok = t[2] <= t[1] and t[1] + w <= t[3]
            else:
                want_ok = None
            try:
                if op < 0.60:
                    v = rng.randrange(1 << (8 * w))
                    m.store(p, w, v)
                    mem[p.value:p.value + w] = v.to_bytes(w, "little")
                    forget(p.value, w)
                elif op < 0.75:
                    assert m.load(p, w) == int.from_bytes(mem[p.value:p.value + w], "little")
                elif op < 0.88:
                    j = rng.randrange(len(regs))
                    m.store_ptr(p, regs[j])
                    mem[p.value:p.value + WORD] = (regs[j].value % (1 << 32)).to_bytes(WORD, "little")
                    forget(p.value, WORD)
                    if intent[j] is not None and regs[j].value >= 0:  # a negative value wraps in memory
                        slots[p.value] = intent[j]
                else:
                    q = m.load_ptr(p)
                    assert q.value == int.from_bytes(mem[p.value:p.value + WORD], "little")
                    assert within_one_object(q.base, q.bound)  # bounds always come from one object
                    regs.append(q)
                    intent.append(slots.get(p.value))
                ok = True
            except BoundsError:
                ok = False
            if want_ok is not None:
                assert ok == want_ok
                caught += not ok
            if ok:
                assert within_one_object(p.base, p.bound) and p.base <= p.value and p.value + w <= p.bound
    assert caught > 500
