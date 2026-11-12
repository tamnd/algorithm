# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/train-algorithm/. The authors are listed in prov/GG2PBV.jsonl.

import random

from train_algorithm import TrainHeap


def check_collect(h: TrainHeap) -> None:
    """Collect once and check that only garbage was freed."""
    live = h.reachable()
    graph = {x: list(h.fields[x]) for x in live}
    h.collect()
    for x in live:
        assert x in h.fields, "a reachable object was freed"
        assert h.fields[x] == graph[x]
    assert h.remset_invariant()
    for c, xs in h.objects.items():
        assert len(xs) <= h.car_size
        assert all(h.car_of[x] == c for x in xs)


def mutate(h: TrainHeap, rng: random.Random) -> None:
    live = [k for k, r in enumerate(h.roots) if r is not None]
    op = rng.random()
    if op < 0.3 or not live:
        h.alloc(rng.randint(0, 3))
    elif op < 0.7:
        s = rng.choice(live)
        nf = len(h.fields[h.roots[s]])
        if nf:
            h.write(s, rng.randrange(nf), rng.choice(live + [None]))
    elif op < 0.85:
        s = rng.choice(live)
        nf = len(h.fields[h.roots[s]])
        if nf:
            h.load(s, rng.randrange(nf), rng.randrange(len(h.roots)))
    else:
        h.roots[rng.choice(live)] = None


def test_random_safety_and_completeness() -> None:
    for seed in range(60):
        rng = random.Random(seed)
        h = TrainHeap(car_size=rng.randint(1, 4), fix_futile=rng.random() < 0.5)
        for _ in range(250):
            if rng.random() < 0.25:
                check_collect(h)
            else:
                mutate(h, rng)
        # the mutator stops: all garbage, cycles included, must go
        for _ in range(5000):
            if set(h.fields) == h.reachable():
                break
            check_collect(h)
        assert set(h.fields) == h.reachable(), "garbage was never freed"


def build_ring(h: TrainHeap, n: int) -> list[int]:
    ks = [h.alloc(1) for _ in range(n)]
    for a, b in zip(ks, ks[1:] + ks[:1]):
        h.write(a, 0, b)
    return ks


def test_large_garbage_cycle_across_cars_is_freed() -> None:
    h = TrainHeap(car_size=3)
    keep = build_ring(h, 7)  # a live ring
    ring = build_ring(h, 40)  # a garbage ring over 14 cars
    cyc = {h.roots[k] for k in ring}
    assert len({h.car_of[x] for x in cyc}) >= 14
    for k in ring:
        h.roots[k] = None
    for k in keep[1:]:
        h.roots[k] = None  # the live ring is reachable through its first object
    steps = 0
    while cyc & set(h.fields):
        check_collect(h)
        steps += 1
        assert steps < 200
    assert h.reachable() == set(h.fields) and len(h.fields) == 7


def test_whole_train_freed_at_once() -> None:
    h = TrainHeap(car_size=2)
    h.alloc(0)  # train 0
    ring = build_ring(h, 6)  # train 1, three cars
    for k in ring:
        h.roots[k] = None
    h.roots[0] = None
    h.collect()  # frees train 0 (no outside reference)
    n = h.collections
    h.collect()  # train 1 has no outside reference: all three cars go in one step
    assert h.collections == n + 1 and h.fields == {}


def test_page_example() -> None:
    h = TrainHeap(car_size=3)
    t1, t2 = h.new_train(), h.new_train()

    def make(t: int) -> int:
        x = h.next_obj
        h.next_obj += 1
        h.fields[x] = [None, None]
        h.place(x, t)
        return x

    def store(s: int, i: int, v: int) -> None:
        h.fields[s][i] = v
        h.record(s, i)

    a, b, w = make(t1), make(t1), make(t1)
    h.new_car(t1)
    x, y = make(t1), make(t1)
    e = make(t2)
    store(e, 0, b)
    store(w, 0, x)
    store(x, 0, y)
    store(y, 0, x)
    store(x, 1, b)
    h.roots = [a]
    c1, c2, c3 = h.trains[t1] + h.trains[t2]
    assert h.remset[c1] == {(x, 1), (e, 0)} and h.remset[c2] == set()
    h.collect()  # car 1: a by the root and b by e go to train 2; w is freed
    assert h.objects[c3] == [e, a, b] and h.freed == {w}
    h.collect()  # train 1 has no outside reference: x and y go together
    assert h.freed == {w, x, y} and t1 not in h.trains
    h.collect()  # car 3: a goes to a new train 3; e and b are garbage
    assert h.freed == {w, x, y, e, b} and list(h.objects.values()) == [[a]]


def adversary_run(fix: bool, collections: int) -> tuple[TrainHeap, set[int]]:
    """The mutator keeps its only reference into the lowest train out of the
    lowest car, so that each collection of that car is futile."""
    h = TrainHeap(car_size=2, fix_futile=fix)
    ring = build_ring(h, 12)
    h.new_train()
    garbage = build_ring(h, 6)
    g = {h.roots[k] for k in garbage}
    for k in garbage + ring[1:]:
        h.roots[k] = None
    for _ in range(collections):
        if not (g & set(h.fields)):
            break
        lowest_car = h.trains[h.lowest_train()][0]
        for _ in range(12):
            if h.car_of[h.roots[0]] != lowest_car:
                break
            h.load(0, 0, 0)  # follow the ring
        check_collect(h)
    return h, g


def test_futile_collections_without_the_fix() -> None:
    h, g = adversary_run(fix=False, collections=1000)
    assert g <= set(h.fields), "the garbage ring was never reached"
    assert h.futile > 900


def test_the_fix_makes_progress() -> None:
    h, g = adversary_run(fix=True, collections=1000)
    assert not (g & set(h.fields))
    assert h.collections < 300
