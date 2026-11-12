# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deferred-reference-counting/. The authors are listed in prov/0A4SH2.jsonl.

import random

from deferred_reference_counting import DRCHeap


def reach(fields: dict[int, list[int | None]], starts: list[int]) -> set[int]:
    seen = set(starts)
    stack = list(starts)
    while stack:
        x = stack.pop()
        for c in fields[x]:
            if c is not None and c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def live(h: DRCHeap) -> set[int]:
    return reach(h.fields, [r for r in h.roots if r is not None])


def heap_recount(h: DRCHeap) -> dict[int, int]:
    cnt = {x: 0 for x in h.fields}
    for fs in h.fields.values():
        for c in fs:
            if c is not None:
                cnt[c] += 1
    return cnt


def cyclic_garbage(h: DRCHeap, lv: set[int]) -> set[int]:
    g = set(h.fields) - lv
    sub = {x: [c for c in h.fields[x] if c in g] for x in g}
    on_cycle = [x for x in g if x in reach(sub, list(sub[x]))]
    return reach(sub, on_cycle) if on_cycle else set()


def check(h: DRCHeap, after_collect: bool) -> None:
    lv = live(h)
    assert h.rc == heap_recount(h)
    assert {x for x in h.fields if h.rc[x] == 0} <= h.zct
    assert not (h.freed & lv)
    if after_collect:
        assert set(h.fields) - lv == cyclic_garbage(h, lv)
        assert h.zct == {x for x in h.fields if h.rc[x] == 0}
        assert h.zct <= lv


def test_random() -> None:
    for seed in range(60):
        rng = random.Random(seed)
        h = DRCHeap(roots=3)
        for _ in range(250):
            lv = sorted(live(h))
            op = rng.randrange(6)
            if op == 0 or not lv:
                h.write_root(rng.randrange(3), h.new(rng.randrange(4)))
            elif op == 1:
                h.write_root(rng.randrange(3), rng.choice(lv + [None]))
            elif op == 2 and rng.random() < 0.3:
                freed = h.collect()
                assert not (set(freed) & set(lv))
                check(h, after_collect=True)
                continue
            else:
                ps = [x for x in lv if h.fields[x]]
                if ps:
                    p = rng.choice(ps)
                    h.write(p, rng.randrange(len(h.fields[p])), rng.choice(lv + [None]))
            check(h, after_collect=False)
        h.collect()
        check(h, after_collect=True)


def test_root_only_object_survives() -> None:
    h = DRCHeap(roots=1)
    a = h.new(0)
    h.write_root(0, a)
    assert h.collect() == [] and h.zct == {a}
    h.write_root(0, None)
    assert h.collect() == [a]


def test_example_of_page() -> None:
    h = DRCHeap(roots=2)
    a = h.new(1)
    h.write_root(0, a)
    b = h.new(1)
    h.write(a, 0, b)
    c = h.new(0)
    h.write(b, 0, c)
    h.write_root(1, c)
    assert h.rc == {a: 0, b: 1, c: 1} and h.zct == {a, b, c}
    h.write_root(0, None)
    assert h.rc == {a: 0, b: 1, c: 1}
    assert sorted(h.collect()) == [a, b]
    assert h.rc == {c: 0} and h.zct == {c}
