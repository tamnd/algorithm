# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/garbage-first-collector/. The authors are listed in prov/CWW6G2.jsonl.

import itertools
import random

import pytest

from garbage_first_collector import G1, OutOfMemory, greedy_collection_set


class Shadow:
    """The same operations on a graph of identities, with no collector."""

    def __init__(self, registers: int) -> None:
        self.roots: list[int | None] = [None] * registers
        self.cells: dict[int, tuple[int, list[int | None]]] = {}
        self.next = 0

    def new(self, reg: int, size: int, nfields: int) -> None:
        self.cells[self.next] = (size, [None] * nfields)
        self.roots[reg] = self.next
        self.next += 1

    def load(self, dst: int, src: int, f: int) -> None:
        x = self.roots[src]
        if x is not None and f < len(self.cells[x][1]):
            self.roots[dst] = self.cells[x][1][f]

    def store(self, dst: int, f: int, src: int) -> None:
        x = self.roots[dst]
        if x is not None and f < len(self.cells[x][1]):
            self.cells[x][1][f] = self.roots[src]

    def move(self, dst: int, src: int) -> None:
        self.roots[dst] = self.roots[src]

    def logical_graph(self) -> tuple:
        seen: dict[int, tuple] = {}
        stack = [x for x in self.roots if x is not None]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            size, fields = self.cells[x]
            seen[x] = (size, tuple(fields))
            stack.extend(y for y in fields if y is not None)
        return tuple(self.roots), tuple(sorted(seen.items()))


def check_heap(h: G1) -> None:
    """Every pointer names an object, and every pointer between regions is in a remembered set."""
    for a in h.roots:
        assert a is None or a in h.objects
    for x, o in h.objects.items():
        assert h.kind[h.region(x)] != "free"
        for f, y in enumerate(o.fields):
            if y is None:
                continue
            assert y in h.objects, "a dangling pointer"
            if h.region(y) != h.region(x):
                assert (x, f) in h.rs[h.region(y)], "a remembered set misses a pointer"


def random_run(seed: int, steps: int = 3000, satb: bool = True) -> G1:
    rng = random.Random(seed)
    regs = 5
    h, s = G1(16, 64, regs, young_regions=3, budget=250, satb=satb), Shadow(regs)
    for _ in range(steps):
        if h.marking and rng.random() < 0.5:
            if not h.mark_step():
                h.finish_marking()
        elif not h.marking and h.kind.count("old") >= 5 and rng.random() < 0.1:
            h.start_marking()
        op = rng.random()
        r1, r2, f = rng.randrange(regs), rng.randrange(regs), rng.randrange(3)
        if op < 0.35:
            size, nf = rng.randint(1, 12), rng.randrange(4)
            try:
                h.new(r1, size, nf)
            except OutOfMemory:
                break
            s.new(r1, size, nf)
        elif op < 0.6:
            h.load(r1, r2, f)
            s.load(r1, r2, f)
        elif op < 0.85:
            h.store(r1, f, r2)
            s.store(r1, f, r2)
        elif op < 0.95:
            h.move(r1, r2)
            s.move(r1, r2)
        else:
            h.roots[r1] = s.roots[r1] = None
        check_heap(h)
        assert h.logical_graph() == s.logical_graph()
    return h


def test_random_runs_keep_the_graph_and_the_remembered_sets() -> None:
    pauses = markings = mixed = 0
    for seed in range(20):
        h = random_run(seed)
        pauses += h.pauses
        markings += h.markings
        mixed += sum(1 for _, old in h.collection_sets if old)
    assert (pauses, markings, mixed) == (751, 144, 93)


def satb_loss(satb: bool) -> G1:
    """a -> b, both old. Marking starts; the mutator moves b into a register and cuts a.f."""
    h = G1(8, 16, 3, young_regions=1, satb=satb)
    h.new(0, 4, 1)  # a
    h.new(1, 4, 0)  # b
    h.store(0, 0, 1)  # a.f = b
    h.roots[1] = None
    h.pause()  # a and b move to an old region
    assert all(h.kind[h.region(x)] == "old" for x in h.objects)
    h.start_marking()  # the snapshot roots: a
    h.load(2, 0, 0)  # register 2 = b
    h.roots[1] = None
    h.store(0, 0, 1)  # a.f = nil: the only heap pointer to b is gone
    h.finish_marking()
    return h


def test_the_satb_barrier_keeps_an_object_moved_into_a_register() -> None:
    h = satb_loss(True)
    check_heap(h)
    assert h.roots[2] in h.objects


def test_without_the_satb_barrier_marking_frees_a_reachable_object() -> None:
    h = satb_loss(False)
    assert h.roots[2] not in h.objects


def test_the_remembered_set_finds_an_object_with_no_root() -> None:
    # An old object points to a young one; the young object survives the pause only through the remembered set.
    h = G1(8, 16, 2, young_regions=2)
    h.new(0, 4, 1)
    h.pause()  # the first object is now old
    old = h.roots[0]
    h.new(1, 4, 0)
    h.store(0, 0, 1)  # old.f = young
    assert (old, 0) in h.rs[h.region(h.roots[1])]
    h.roots[1] = None
    h.pause()
    y = h.objects[old].fields[0]
    assert y is not None and h.objects[y].oid == 1
    check_heap(h)


def best_collection_set(old: list[tuple[int, int, int]], budget: int) -> int:
    best = 0
    for k in range(len(old) + 1):
        for sub in itertools.combinations(old, k):
            if sum(c for _, _, c in sub) <= budget:
                best = max(best, sum(g for _, g, _ in sub))
    return best


def test_greedy_against_brute_force() -> None:
    rng = random.Random(7)
    equal = 0
    trials = 2000
    for _ in range(trials):
        m = rng.randint(1, 7)
        old = [(r, rng.randint(1, 60), rng.randint(5, 40)) for r in range(m)]
        budget = rng.randint(5, 120)
        chosen, t = greedy_collection_set(old, budget)
        g = sum(gg for r, gg, _ in old if r in chosen)
        opt = best_collection_set(old, budget)
        assert t <= budget and g <= opt
        # The first region that does not fit bounds the loss: the fractional optimum is at most g plus its garbage.
        rest = sorted((x for x in old if x[0] not in chosen), key=lambda x: (-x[1] / x[2], x[0]))
        assert opt <= g + (rest[0][1] if rest else 0)
        equal += g == opt
    assert equal == 1644


def test_greedy_can_be_far_from_the_best() -> None:
    # A small region with the best ratio blocks a large one that would fill the budget.
    old = [(0, 10, 1), (1, 90, 10)]
    assert greedy_collection_set(old, 10) == ([0], 1)
    assert best_collection_set(old, 10) == 90


@pytest.mark.parametrize("budget", [20, 60, 200])
def test_the_budget_limits_the_old_regions(budget: int) -> None:
    rng = random.Random(budget)
    old = [(r, rng.randint(1, 60), rng.randint(5, 40)) for r in range(10)]
    chosen, t = greedy_collection_set(old, budget)
    assert t <= budget
    assert t == sum(c for r, _, c in old if r in chosen)
