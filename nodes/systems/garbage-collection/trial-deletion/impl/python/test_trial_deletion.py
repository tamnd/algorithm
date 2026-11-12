# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trial-deletion/. The authors are listed in prov/40TJAC.jsonl.

import random

from trial_deletion import BLACK, ROOT, CycleRCHeap


def reachable(h: CycleRCHeap) -> set[int]:
    seen, stack = {ROOT}, [ROOT]
    while stack:
        for c in h.children(stack.pop()):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def check_counts(h: CycleRCHeap) -> None:
    # a released object that waits in the buffer has count 0 and owns no counts
    zombie = {x for x in h.fields if x != ROOT and h.rc[x] == 0}
    assert zombie <= set(h.candidates)
    cnt = {x: 0 for x in h.fields if x != ROOT}
    for x, fs in h.fields.items():
        if x not in zombie:
            for c in fs:
                if c is not None:
                    cnt[c] += 1
    assert cnt == {x: h.rc[x] for x in h.fields if x != ROOT}
    assert not (h.freed & reachable(h))


def mutate(h: CycleRCHeap, rng: random.Random, roots: int) -> None:
    live = sorted(reachable(h) - {ROOT})
    op = rng.randrange(4)
    if op == 0 or not live:
        h.write(ROOT, rng.randrange(roots), h.new(rng.randrange(1, 4)))
    elif op == 1:
        h.write(ROOT, rng.randrange(roots), rng.choice(live + [None]))
    else:
        p = rng.choice(live)
        h.write(p, rng.randrange(len(h.fields[p])), rng.choice(live + [None]))


def test_random_graphs() -> None:
    for seed in range(80):
        rng = random.Random(seed)
        h = CycleRCHeap(roots=3)
        for step in range(400):
            mutate(h, rng, 3)
            check_counts(h)
            if step % 37 == 36:
                h.collect_cycles()
                check_counts(h)
                assert set(h.fields) == reachable(h)  # the live set is the reachable set
                assert all(c == BLACK for c in h.color.values())
                assert h.candidates == []


def test_two_cycle() -> None:
    h = CycleRCHeap(roots=1)
    a, b = h.new(1), h.new(1)
    h.write(ROOT, 0, a)
    h.write(a, 0, b)
    h.write(b, 0, a)
    h.write(ROOT, 0, None)
    assert h.candidates == [a] and h.rc == {ROOT: 1, a: 1, b: 1}
    assert h.collect_cycles() == {a, b}
    assert set(h.fields) == {ROOT}


def test_externally_referenced_cycle_survives() -> None:
    h = CycleRCHeap(roots=2)
    a, b, c = h.new(1), h.new(1), h.new(1)
    h.write(ROOT, 0, a)
    h.write(a, 0, b)
    h.write(b, 0, c)
    h.write(c, 0, a)
    h.write(ROOT, 1, b)
    h.write(ROOT, 0, None)  # a is a candidate, but b has a root
    assert h.collect_cycles() == set()
    assert h.rc == {ROOT: 1, a: 1, b: 2, c: 1}
    h.write(ROOT, 1, None)
    assert h.collect_cycles() == {a, b, c}
