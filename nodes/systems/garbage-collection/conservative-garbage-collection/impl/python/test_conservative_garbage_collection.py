# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conservative-garbage-collection/. The authors are listed in prov/BZ71R7.jsonl.

import random

from conservative_garbage_collection import ConservativeHeap


def hits(h: ConservativeHeap, w: int) -> list[int]:
    """The objects a word looks like a pointer to, by a linear scan."""
    out = []
    for o, n in h.size_of.items():
        if w == o or (h.interior and o <= w < o + n):
            out.append(o)
    return out


def oracle_closure(h: ConservativeHeap, roots: list[int]) -> set[int]:
    """Every object reachable through words that look like pointers."""
    seen: set[int] = set()
    frontier = [o for w in roots for o in hits(h, w)]
    while frontier:
        o = frontier.pop()
        if o not in seen:
            seen.add(o)
            frontier += [p for w in h.words(o) for p in hits(h, w)]
    return seen


def precise_reachable(h: ConservativeHeap, roots: list[tuple[int, bool]],
                      is_ptr: dict[int, bool]) -> set[int]:
    """The objects reachable through the words that really are pointers."""
    seen: set[int] = set()
    frontier = [w for w, p in roots if p]
    while frontier:
        w = frontier.pop()
        (o,) = hits(h, w)  # a real pointer always points into one live object
        if o not in seen:
            seen.add(o)
            frontier += [h.load(a) for a in range(o, o + h.size_of[o]) if is_ptr.get(a)]
    return seen


def random_word(h: ConservativeHeap, rng: random.Random) -> tuple[int, bool]:
    r = rng.random()
    if r < 0.4 and h.starts:
        o = rng.choice(h.starts)
        off = rng.randrange(h.size_of[o]) if h.interior else 0
        return o + off, True  # a real pointer
    if r < 0.6:
        return rng.randrange(h.lo, h.hi), False  # an integer that may look like a pointer
    return rng.randrange(0, 600), False  # a small integer


def test_random_programs() -> None:
    false_retained = 0
    for seed in range(30):
        rng = random.Random(seed)
        h = ConservativeHeap(1000, 100, interior=rng.random() < 0.5)
        is_ptr: dict[int, bool] = {}  # the truth, which the collector never sees
        roots: list[tuple[int, bool]] = []
        for step in range(220):
            r = rng.random()
            words = [w for w, _ in roots]
            if r < 0.4:
                n = rng.randint(1, 4)
                o = h.alloc_or_collect(n, words) if rng.random() < 0.5 else h.alloc(n)
                if o is None:
                    continue
                for a in range(o, o + n):
                    is_ptr.pop(a, None)
                for a in range(o, o + n):
                    w, p = random_word(h, rng)
                    h.store(a, w)
                    is_ptr[a] = p
                roots.append((o, True))
            elif r < 0.55 and roots:
                roots.pop(rng.randrange(len(roots)))
            elif r < 0.7:
                roots.append(random_word(h, rng))
            elif r < 0.85 and h.starts:
                o = rng.choice(sorted(precise_reachable(h, roots, is_ptr)) or [None])
                if o is not None:  # the program stores into a live object
                    a = o + rng.randrange(h.size_of[o])
                    w, p = random_word(h, rng)
                    h.store(a, w)
                    is_ptr[a] = p
            else:
                words = [w for w, _ in roots]
                live = precise_reachable(h, roots, is_ptr)
                expect = oracle_closure(h, words)
                before = {o: h.words(o) for o in h.starts}
                freed = h.collect(words)
                kept = set(h.starts)
                assert live <= kept, "a reachable object was freed"
                assert kept == expect, "kept exactly the pointer-looking closure"
                assert freed == set(before) - kept
                for o in kept:
                    assert h.words(o) == before[o], "a kept object moved or changed"
                false_retained += len(kept - live)
            # the free list and the objects tile the heap
            spans = sorted([(o, h.size_of[o]) for o in h.starts] + h.free)
            pos = h.lo
            for s, m in spans:
                assert s == pos and m > 0
                pos += m
            assert pos == h.hi
    assert false_retained > 0  # integers that look like pointers do keep garbage


def test_page_example() -> None:
    h = ConservativeHeap(1000, 12)
    a, b, c, d, e = (h.alloc(n) for n in (3, 2, 2, 3, 2))
    assert (a, b, c, d, e) == (1000, 1003, 1005, 1007, 1010)
    for addr, w in zip(range(a, a + 3), (1003, 7, 2000)):
        h.store(addr, w)
    h.store(b, 42)
    h.store(c, 1003)
    h.store(d, 1010)
    h.store(d + 2, 1)
    roots = [1000, 1008, 5]  # 1008 is the value of a counter, not a pointer
    freed = h.collect(roots)
    assert freed == {c} and h.starts == [a, b, d, e]  # d and e are falsely retained
    h2 = ConservativeHeap(1000, 12, interior=False)
    for n in (3, 2, 2, 3, 2):
        h2.alloc(n)
    h2.mem = [1003, 7, 2000, 42, 0, 1003, 0, 1010, 0, 1, 0, 0]
    assert h2.collect(roots) == {c, d, e}  # 1008 is not the start of an object


def test_interior_pointers_must_be_recognised() -> None:
    # a C program that keeps only p + 2 for an array p still uses the array
    h = ConservativeHeap(1000, 16, interior=True)
    p = h.alloc(4)
    assert h.collect([p + 2]) == set() and h.starts == [p]
    h = ConservativeHeap(1000, 16, interior=False)
    p = h.alloc(4)
    assert h.collect([p + 2]) == {p}  # without interior pointers, the array is lost


def test_out_of_bounds_and_gaps_are_not_pointers() -> None:
    h = ConservativeHeap(1000, 10)
    x = h.alloc(2)
    y = h.alloc(2)
    h.collect([y])  # x is freed; its words are a gap now
    assert h.starts == [y]
    assert h.object_at(x) is None and h.object_at(999) is None and h.object_at(1010) is None
    assert h.collect([x, 999, 1010, -5]) == {y}
