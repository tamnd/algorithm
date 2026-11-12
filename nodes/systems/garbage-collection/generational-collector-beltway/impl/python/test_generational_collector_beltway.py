# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generational-collector-beltway/. The authors are listed in prov/WR1XXS.jsonl.

import random

from generational_collector_beltway import Beltway, OutOfMemory


def configs(u: int) -> dict[str, tuple[list[int], bool]]:
    x = u // 4
    return {
        "BSS": ([u], False),
        "BA2": ([u, u], False),
        "X.X": ([x, x], True),
        "X.X.100": ([x, x, u], True),
    }


def snapshot(h: Beltway) -> dict[int, list]:
    return {x: list(h.fields[x]) for x in h.reachable()}


def check_kept(h: Beltway, before: dict[int, list], same_fields: bool = True) -> None:
    for x, fs in before.items():
        assert x in h.fields, "a reachable object was freed"
        assert h.fields[x] == fs or not same_fields
    assert h.remset_invariant()
    for k, xs in h.objects.items():
        assert xs and len(xs) <= h.sizes[h.belt_of[k]]
        assert all(h.inc_of[x] == k for x in xs)
    assert h.used() <= h.usable


def bound_live(h: Beltway, rng: random.Random) -> None:
    """Drop roots until at most half of the heap is reachable."""
    while len(h.reachable()) > h.usable // 2:
        live = [k for k, r in enumerate(h.roots) if r is not None]
        h.roots[rng.choice(live)] = None


def mutate(h: Beltway, rng: random.Random) -> None:
    bound_live(h, rng)
    live = [k for k, r in enumerate(h.roots) if r is not None]
    op = rng.random()
    if op < 0.45 or not live:
        h.alloc(rng.randint(0, 3))
    elif op < 0.8:
        s = rng.choice(live)
        nf = len(h.fields[h.roots[s]])
        if nf:
            h.write(s, rng.randrange(nf), rng.choice(live + [None]))
    elif op < 0.9:
        s = rng.choice(live)
        nf = len(h.fields[h.roots[s]])
        if nf:
            h.load(s, rng.randrange(nf), rng.randrange(len(h.roots)))
    else:
        h.roots[rng.choice(live)] = None


def test_random_safety_and_completeness() -> None:
    for seed in range(24):
        for name, (sizes, trig) in configs(40).items():
            rng = random.Random(seed)
            h = Beltway(sizes, 40, nursery_trigger=trig)
            try:
                for _ in range(300):
                    bound_live(h, rng)
                    before = snapshot(h)
                    if rng.random() < 0.1:
                        h.collect()
                        check_kept(h, before)
                    else:  # a store changes fields; an allocation may collect first
                        mutate(h, rng)
                        check_kept(h, before, same_fields=False)
            except OutOfMemory:
                assert name == "X.X", "a complete configuration ran out of memory"
                continue
            if name == "X.X":
                continue
            for _ in range(500):  # the mutator stops: all garbage must go
                if set(h.fields) == h.reachable():
                    break
                before = snapshot(h)
                h.collect()
                check_kept(h, before)
            assert set(h.fields) == h.reachable(), name


def ring(h: Beltway, belt: int, n: int) -> list[int]:
    """Place a garbage ring of n objects on a belt, in increments of its size."""
    xs = []
    for _ in range(n):
        x = h.next_obj
        h.next_obj += 1
        h.fields[x] = [None]
        h.place(x, h.youngest(belt))
        xs.append(x)
    for a, b in zip(xs, xs[1:] + xs[:1]):
        h.fields[a][0] = b
        h.record(a, 0)
    return xs


def test_page_example() -> None:
    # Beltway X.X with increments of 2: the ring a -> b -> c -> a never dies
    h = Beltway([2, 2], 8)
    a, b, c = ring(h, 1, 3)
    i1, i2 = h.belts[1]
    assert h.objects[i1] == [a, b] and h.objects[i2] == [c]
    assert h.remset[i1] == {(c, 0)} and h.remset[i2] == set()
    h.collect()  # i1: a is remembered from c; b follows a
    i3 = h.belts[1][-1]
    assert h.belts[1] == [i2, i3] and h.objects[i2] == [c, a] and h.objects[i3] == [b]
    for _ in range(100):
        h.collect()
        assert set(h.fields) == {a, b, c}
        assert len(h.belts[1]) == 2  # the ring always spans two increments
    # Beltway X.X.100: the third belt is collected whole
    h = Beltway([2, 2, 8], 8)
    a, b, c = ring(h, 1, 3)
    i1, i2 = h.belts[1]
    h.collect()  # i1: a and b go up to belt 2
    (top,) = h.belts[2]
    assert h.objects[top] == [a, b] and h.belts[1] == [i2]
    h.collect()  # i2: c is remembered from b on belt 2
    assert h.objects[top] == [a, b, c] and h.belts[1] == []
    h.collect()  # belt 2 is the whole heap: no root points into it
    assert h.fields == {} and h.collections == 3


def test_large_garbage_cycle_beltway_xx_versus_xx100() -> None:
    for sizes, complete in (([5, 5], False), ([5, 5, 40], True)):
        h = Beltway(sizes, 40, nursery_trigger=True)
        keep = [h.alloc(1) for _ in range(4)]
        for p, q in zip(keep, keep[1:]):
            h.write(p, 0, q)
        g = [h.alloc(1) for _ in range(17)]
        for p, q in zip(g, g[1:] + g[:1]):
            h.write(p, 0, q)
        cyc = {h.roots[k] for k in g}
        for k in g + keep[1:]:
            h.roots[k] = None
        for _ in range(300):
            before = snapshot(h)
            h.collect()
            check_kept(h, before)
        assert (not (cyc & set(h.fields))) == complete
        assert set(h.reachable()) <= set(h.fields)


def test_bss_is_a_semispace_collector() -> None:
    rng = random.Random(5)
    h = Beltway([60], 60)
    for _ in range(400):
        mutate(h, rng)
        if rng.random() < 0.05:
            live = h.reachable()
            copied = h.copied
            h.collect()
            assert set(h.fields) == live and h.copied - copied == len(live)
            assert len(h.belts[0]) == 1 or not live


def test_ba2_collects_the_nursery_first() -> None:
    rng = random.Random(9)
    h = Beltway([50, 50], 50)
    seen_old = 0
    for _ in range(600):
        mutate(h, rng)
        if rng.random() < 0.1:
            nursery = set(h.objects[h.belts[0][0]]) if h.belts[0] else set()
            old = set(h.inc_of) - nursery
            h.collect()
            if nursery:  # only the nursery is collected; survivors go to belt 1
                assert old <= set(h.fields) and not h.belts[0]
                assert all(h.belt_of[h.inc_of[x]] == 1 for x in nursery & set(h.fields))
            else:
                seen_old += 1
    assert seen_old > 0


def test_barrier_is_unidirectional() -> None:
    h = Beltway([2, 2, 10], 10)
    r0, r1 = h.alloc(1), h.alloc(1)
    for _ in range(3):
        h.collect()  # move both up
    young = h.alloc(1)
    h.write(young, 0, r0)  # young to old: the target is collected later, not remembered
    assert all(not s for s in h.remset.values())
    h.write(r1, 0, young)  # old to young: remembered
    assert sum(len(s) for s in h.remset.values()) == 1
