# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/precise-garbage-collection/. The authors are listed in prov/KYZMZH.jsonl.

import copy
import random

import pytest

from precise_garbage_collection import (
    Frame,
    NotAtSafepoint,
    Obj,
    StackMap,
    collect,
    conservative_roots,
)


def example() -> tuple[dict[int, Obj], dict[tuple[str, int], StackMap]]:
    heap = {
        1000: Obj(1, [1005, 10, 20]),  # A: one pointer field, then data
        1003: Obj(0, [1]),  # B
        1004: Obj(0, [2]),  # C
        1005: Obj(0, [3]),  # D
    }
    maps = {
        ("f", 8): StackMap(pointers=[0, 2]),  # before the last use of q
        ("f", 12): StackMap(pointers=[0], derived=[(0, 3)]),  # q is dead; slot 3 is p + 2
    }
    return heap, maps


def test_page_example() -> None:
    heap, maps = example()
    f = Frame("f", 12, [1000, 1004, 1003, 1002])  # p, an integer, a dead q, p + 2
    new, nxt = collect(heap, [f], maps, 2000)
    assert f.slots == [2000, 1004, 1003, 2002]
    assert new == {2000: Obj(1, [2003, 10, 20]), 2003: Obj(0, [3])} and nxt == 2004
    assert conservative_roots(heap, [Frame("f", 12, [1000, 1004, 1003, 1002])]) == {1000, 1003, 1004}
    g = Frame("f", 8, [1000, 1004, 1003, 1002])  # at pc 8, q is still live
    new, _ = collect(heap, [g], maps, 2000)
    assert g.slots[:3] == [2000, 1004, 2003] and len(new) == 3  # roots first, then D


def test_no_collection_outside_a_safepoint() -> None:
    heap, maps = example()
    with pytest.raises(NotAtSafepoint):
        collect(heap, [Frame("f", 9, [1000, 0, 0, 0])], maps, 2000)


def random_case(rng: random.Random):
    heap: dict[int, Obj] = {}
    addr = 1000
    addrs = []
    for _ in range(rng.randint(1, 25)):
        n = rng.randint(1, 4)
        heap[addr] = Obj(rng.randint(0, n), [0] * n)
        addrs.append(addr)
        addr += n
    for a, o in heap.items():
        for i in range(len(o.words)):
            if i < o.nptr:
                o.words[i] = rng.choice(addrs + [0])
            else:
                o.words[i] = rng.choice([rng.randrange(1000, addr), rng.randrange(100)])
    stack, maps, truth = [], {}, []
    for k in range(rng.randint(1, 4)):
        nslots = rng.randint(1, 6)
        slots, ptrs, derived = [], [], []
        for s in range(nslots):
            kind = rng.random()
            if kind < 0.4:
                slots.append(rng.choice(addrs))
                ptrs.append(s)  # a live pointer
            else:
                slots.append(rng.choice(addrs + [rng.randrange(100)]))  # dead pointer or integer
        for b in list(ptrs):
            if rng.random() < 0.3:  # a derived pointer into the base object
                slots.append(slots[b] + rng.randrange(len(heap[slots[b]].words)))
                derived.append((b, len(slots) - 1))
        func, pc = f"f{k}", rng.randrange(50)
        maps[(func, pc)] = StackMap(ptrs, derived)
        stack.append(Frame(func, pc, slots))
        truth.append((ptrs, derived))
    return heap, stack, maps, truth


def test_random_stacks() -> None:
    extra = 0  # roots a conservative scan would add, beyond the live objects
    for seed in range(400):
        rng = random.Random(seed)
        heap, stack, maps, truth = random_case(rng)
        old_stack = copy.deepcopy(stack)
        old_heap = copy.deepcopy(heap)
        # the true reachable set, from the live slots only
        live: set[int] = set()
        todo = [f.slots[s] for f, (ptrs, _) in zip(stack, truth) for s in ptrs]
        while todo:
            a = todo.pop()
            if a and a not in live:
                live.add(a)
                todo += heap[a].words[:heap[a].nptr]
        new, _ = collect(heap, stack, maps, 10_000)
        assert heap == old_heap, "the old space is not changed"
        assert len(new) == len(live), "exactly the reachable objects are copied"
        live_roots = {f.slots[s] for f, (ptrs, _) in zip(old_stack, truth) for s in ptrs}
        conservative = conservative_roots(heap, old_stack)
        assert live_roots <= conservative
        extra += len(conservative - live)
        # the copy is isomorphic to the reachable graph
        image: dict[int, int] = {}

        def same(a: int, b: int) -> None:
            if a == 0:
                assert b == 0
                return
            if a in image:
                assert image[a] == b
                return
            image[a] = b
            o, n = heap[a], new[b]
            assert o.nptr == n.nptr and o.words[o.nptr:] == n.words[n.nptr:]
            for x, y in zip(o.words[:o.nptr], n.words[:n.nptr]):
                same(x, y)

        for f0, f1, (ptrs, derived) in zip(old_stack, stack, truth):
            for s in range(len(f0.slots)):
                if s in ptrs:
                    same(f0.slots[s], f1.slots[s])
                elif all(s != d for _, d in derived):
                    assert f1.slots[s] == f0.slots[s], "a non-pointer slot was changed"
            for b, d in derived:
                assert f1.slots[d] - f1.slots[b] == f0.slots[d] - f0.slots[b]
    assert extra > 0  # dead slots and integers would keep garbage alive
