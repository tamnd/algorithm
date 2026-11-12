# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-barrier/. The authors are listed in prov/YR5TKX.jsonl.

import random

from write_barrier import BLACK, GRAY, WHITE, Heap


def reachable(h: Heap) -> set[int]:
    seen: set[int] = set()
    stack = [r for r in h.roots if r is not None]
    while stack:
        o = stack.pop()
        if o in seen:
            continue
        assert o in h.fields, "a reachable object was freed"
        seen.add(o)
        stack.extend(t for t in h.fields[o] if t is not None)
    return seen


def mutate(h: Heap, rng: random.Random) -> None:
    live = [r for r in h.roots if r is not None]
    op = rng.random()
    if op < 0.2 or not live:
        h.alloc(rng.randint(0, 3), old=rng.random() < 0.5)
    elif op < 0.6:
        src = rng.choice(live)
        if h.fields[src]:
            h.write(src, rng.randrange(len(h.fields[src])), rng.choice(live + [None]))
    elif op < 0.85:
        src = rng.choice(live)
        if h.fields[src]:
            h.roots.append(h.fields[src][rng.randrange(len(h.fields[src]))])
    else:
        h.roots[rng.randrange(len(h.roots))] = None


def run_marking(kind: str, seed: int) -> None:
    rng = random.Random(seed)
    h = Heap(kind)
    for _ in range(rng.randint(5, 40)):
        mutate(h, rng)
    for _ in range(3):  # three collection cycles
        h.start_marking()
        snapshot = reachable(h)
        while h.gray or rng.random() < 0.3:
            if rng.random() < 0.5:
                h.mark_step()
            else:
                mutate(h, rng)
        dead = h.finish_marking()
        live = reachable(h)  # asserts that no reachable object was freed
        assert not (dead & live)
        if kind == "snapshot":
            assert not (dead & snapshot), "SATB keeps everything reachable at the start"
        for _ in range(rng.randint(0, 20)):
            mutate(h, rng)


def test_incremental_update_never_frees_a_live_object() -> None:
    for seed in range(300):
        run_marking("incremental", seed)


def test_snapshot_at_the_beginning_never_frees_a_live_object() -> None:
    for seed in range(300):
        run_marking("snapshot", 10_000 + seed)


def lost_object_scenario(kind: str) -> tuple[Heap, int]:
    """A black object gets the only pointer to a white one, and the gray
    object that pointed to it drops the pointer."""
    h = Heap(kind)
    a = h.alloc(1)
    b = h.alloc(1)
    c = h.alloc(0)
    h.write(b, 0, c)
    h.roots = [b, a]
    h.start_marking()
    h.mark_step()  # scans a: a is black, b is gray, c is white
    assert (h.color[a], h.color[b], h.color[c]) == (BLACK, GRAY, WHITE)
    h.roots.append(h.fields[b][0])  # the mutator loads c
    h.write(a, 0, c)  # stores c into the black object
    h.write(b, 0, None)  # and deletes the pointer from the gray one
    h.roots.pop()  # c is now reachable only through a
    h.finish_marking()
    return h, c


def test_no_barrier_loses_an_object() -> None:
    h, c = lost_object_scenario("none")
    assert c not in h.fields and h.fields[h.roots[1]][0] == c  # a dangling pointer


def test_both_marking_barriers_save_it() -> None:
    for kind in ("incremental", "snapshot"):
        h, c = lost_object_scenario(kind)
        assert c in h.fields
        reachable(h)


def test_generational_barrier_records_old_to_young() -> None:
    rng = random.Random(7)
    h = Heap("generational")
    for _ in range(400):
        mutate(h, rng)
        for o in h.old:
            for i, t in enumerate(h.fields[o]):
                if t is not None and t not in h.old:
                    assert (o, i) in h.remset


def test_card_barrier_dirties_every_written_slot() -> None:
    h = Heap("card", card_shift=2)
    o = h.alloc(3)
    h.write(o, 2, None)  # no test on the value
    assert h.dirty == {h.address(o, 2) >> 2}


def test_refcount_barrier_keeps_counts() -> None:
    rng = random.Random(11)
    h = Heap("refcount")
    for _ in range(500):
        mutate(h, rng)
        indeg = {o: 0 for o in h.fields}
        for o in h.fields:
            for t in h.fields[o]:
                if t is not None:
                    indeg[t] += 1
        assert indeg == h.rc
    h.alloc(1)
    x = h.roots[-1]
    h.write(x, 0, x)
    h.write(x, 0, x)  # increment before decrement: the self store keeps x
    assert h.rc[x] == 1
