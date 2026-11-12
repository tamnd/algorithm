# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-reference-counting/. The authors are listed in prov/BYX9WD.jsonl.

import random

from weighted_reference_counting import Ref, WRCHeap


def refs_of(h: WRCHeap, held: list[Ref]) -> list[Ref]:
    out = list(held)
    for fs in h.fields.values():
        out.extend(s for s in fs if s is not None)
    return out


def reach(h: WRCHeap, held: list[Ref]) -> set[int]:
    seen = {r.target for r in held}
    stack = list(seen)
    while stack:
        x = stack.pop()
        for s in h.fields[x]:
            if s is not None and s.target not in seen:
                seen.add(s.target)
                stack.append(s.target)
    return seen


def check(h: WRCHeap, held: list[Ref]) -> None:
    total = {x: 0 for x in h.fields}
    for r in refs_of(h, held):
        assert r.w >= 1 and r.w & (r.w - 1) == 0  # a power of two
        total[r.target] += r.w
    for x, w in h.queue:
        total[x] += w
    assert total == h.tw  # the weight invariant, in exact integers
    assert not (h.freed & reach(h, held))


def cyclic_garbage(h: WRCHeap, live: set[int]) -> set[int]:
    g = set(h.fields) - live
    sub = {x: [s.target for s in h.fields[x] if s is not None and s.target in g] for x in g}

    def r(starts: list[int]) -> set[int]:
        seen, st = set(starts), list(starts)
        while st:
            for c in sub[st.pop()]:
                if c not in seen:
                    seen.add(c)
                    st.append(c)
        return seen

    on_cycle = [x for x in g if x in r(sub[x])]
    return r(on_cycle)


def test_random() -> None:
    for seed in range(40):
        rng = random.Random(seed)
        h = WRCHeap(max_weight=8)  # small, so that indirection cells appear
        held: list[Ref] = []
        copies = 0
        for _ in range(300):
            op = rng.randrange(6)
            if op == 0 or not held:
                held.append(h.new(rng.randrange(3)))
            elif op == 1:
                held.append(h.copy(rng.choice(held)))
                copies += 1
            elif op == 2:
                h.delete(held.pop(rng.randrange(len(held))))
            elif op == 3:
                p = h.deref(rng.choice(held))
                if h.fields[p]:
                    h.store(p, rng.randrange(len(h.fields[p])), h.copy(rng.choice(held)))
                    copies += 1
            elif op == 4:
                p = h.deref(rng.choice(held))
                fs = [s for s in h.fields[p] if s is not None]
                if fs:
                    held.append(h.copy(rng.choice(fs)))
                    copies += 1
            for _ in range(rng.randrange(3)):
                if h.queue:
                    h.deliver(rng.randrange(len(h.queue)))
            check(h, held)
        before = h.messages
        h.deliver_all()
        check(h, held)
        live = reach(h, held)
        assert set(h.fields) - live == cyclic_garbage(h, live)
        assert h.messages >= before


def test_copy_sends_no_message() -> None:
    h = WRCHeap(max_weight=4)
    a = h.new(0)
    b = h.copy(a)
    c = h.copy(a)
    assert (a.w, b.w, c.w, h.messages) == (1, 2, 1, 0)
    d = h.copy(a)  # weight 1: an indirection cell is made
    cell = a.target
    assert cell in h.indirect and h.deref(a) == h.deref(d) == b.target
    assert (a.w, d.w, h.tw[cell], h.messages) == (2, 2, 4, 0)
    for r in (a, b, c, d):
        h.delete(r)
    h.deliver_all()
    assert h.fields == {} and h.messages == 5


def test_any_message_order() -> None:
    for seed in range(20):
        rng = random.Random(seed)
        h = WRCHeap(max_weight=16)
        held = [h.new(0)]
        for _ in range(10):
            held.append(h.copy(rng.choice(held)))
        rng.shuffle(held)
        for r in held:
            h.delete(r)
        while h.queue:
            assert h.fields  # the object lives until the last message
            h.deliver(rng.randrange(len(h.queue)))
        assert h.fields == {}
