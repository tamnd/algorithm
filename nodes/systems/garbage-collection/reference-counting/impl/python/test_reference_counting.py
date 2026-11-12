# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reference-counting/. The authors are listed in prov/3QGTQE.jsonl.

import random

from reference_counting import ROOT, RCHeap


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


def recount(h: RCHeap) -> dict[int, int]:
    cnt = {x: 0 for x in h.fields}
    for x, fs in h.fields.items():
        for c in fs:
            if c is not None:
                cnt[c] += 1
    return cnt


def cyclic_garbage(h: RCHeap, live: set[int]) -> set[int]:
    """Garbage objects that a cycle of garbage objects reaches."""
    g = set(h.fields) - live
    sub = {x: [c for c in h.fields[x] if c in g] for x in g}
    on_cycle = [x for x in g if x in reach(sub, [c for c in sub[x]])]
    return reach(sub, on_cycle) if on_cycle else set()


def check(h: RCHeap, full: bool) -> None:
    live = reach(h.fields, [ROOT])
    assert {x: h.rc[x] for x in h.fields if x != ROOT} == {
        x: c for x, c in recount(h).items() if x != ROOT
    }
    assert not (h.freed & live)
    assert all(h.rc[x] > 0 for x in live if x != ROOT)
    if full:
        assert set(h.fields) - live == cyclic_garbage(h, live)


def run(seed: int, lazy: bool, steps: int = 300) -> None:
    rng = random.Random(seed)
    h = RCHeap(roots=3, lazy=lazy)
    for _ in range(steps):
        live = sorted(reach(h.fields, [ROOT]) - {ROOT})
        op = rng.randrange(4)
        if op == 0 or not live:
            x = h.new(rng.randrange(4))
            h.write(ROOT, rng.randrange(3), x)
        elif op == 1:
            y = rng.choice(live + [None])
            h.write(ROOT, rng.randrange(3), y)
        else:
            with_fields = [x for x in live if h.fields[x]]
            if not with_fields:
                continue
            p = rng.choice(with_fields)
            y = rng.choice(live + [None])
            h.write(p, rng.randrange(len(h.fields[p])), y)
        check(h, full=not lazy)
    if lazy:
        h.drain()
        check(h, full=True)


def test_random_eager() -> None:
    for seed in range(40):
        run(seed, lazy=False)


def test_random_lazy() -> None:
    for seed in range(40):
        run(seed, lazy=True)


def test_list_cascade() -> None:
    h = RCHeap(roots=1)
    xs = [h.new(1) for _ in range(5)]
    for a, b in zip(xs, xs[1:]):
        h.write(a, 0, b)
    h.write(ROOT, 0, xs[0])
    assert [h.rc[x] for x in xs] == [1, 1, 1, 1, 1]
    h.write(ROOT, 0, None)
    assert h.freed == set(xs) and set(h.fields) == {ROOT}


def test_self_write() -> None:
    h = RCHeap(roots=1)
    a = h.new(0)
    h.write(ROOT, 0, a)
    h.write(ROOT, 0, a)  # increment before decrement keeps a alive
    assert h.rc[a] == 1 and a not in h.freed


def test_cycle_leak() -> None:
    h = RCHeap(roots=1)
    a = h.new(1)
    h.write(ROOT, 0, a)
    b = h.new(1)
    h.write(a, 0, b)
    h.write(b, 0, a)
    assert (h.rc[a], h.rc[b]) == (2, 1)
    h.write(ROOT, 0, None)
    assert (h.rc[a], h.rc[b]) == (1, 1)
    assert not h.freed
    assert reach(h.fields, [ROOT]) == {ROOT}


def test_lazy_bounds_work() -> None:
    h = RCHeap(roots=1, lazy=True)
    xs = [h.new(1) for _ in range(6)]
    for a, b in zip(xs, xs[1:]):
        h.write(a, 0, b)
    h.write(ROOT, 0, xs[0])
    h.write(ROOT, 0, None)
    assert h.freed == set() and h.pending == [xs[0]]
    h.new(0)
    assert h.freed == {xs[0]} and h.pending == [xs[1]]
    h.drain()
    assert h.freed == set(xs)
