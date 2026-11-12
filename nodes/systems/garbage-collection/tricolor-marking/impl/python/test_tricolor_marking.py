# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tricolor-marking/. The authors are listed in prov/SZ1DX2.jsonl.

import copy
import random

from tricolor_marking import BLACK, GRAY, WHITE, TricolorHeap

A, B, C = 0, 1, 2
EXAMPLE = [[B, None], [C, None], [None, None]]
PROGRAM = [(A, 1, C), (B, 0, None)]  # A.g <- C, then B.f <- nil


def run_example(barrier: str) -> TricolorHeap:
    h = TricolorHeap(EXAMPLE, [A], barrier)
    h.marker_step(A)
    h.write(*PROGRAM[0])
    h.write(*PROGRAM[1])
    while h.grays():
        h.marker_step(h.grays()[0])
    return h


def test_lost_object_without_barrier() -> None:
    h = run_example("none")
    assert h.color == [BLACK, BLACK, WHITE]
    assert h.reachable() == {A, B, C}
    assert h.lost() == {C}


def test_barriers_save_the_object() -> None:
    assert run_example("dijkstra").lost() == set()
    assert run_example("yuasa").lost() == set()


def test_invariants_in_the_example() -> None:
    h = TricolorHeap(EXAMPLE, [A], "none")
    h.marker_step(A)
    h.write(*PROGRAM[0])
    assert not h.strong_invariant() and h.weak_invariant()
    h.write(*PROGRAM[1])
    assert not h.strong_invariant() and not h.weak_invariant()
    h = TricolorHeap(EXAMPLE, [A], "yuasa")
    h.marker_step(A)
    h.write(*PROGRAM[0])
    h.write(*PROGRAM[1])
    assert h.strong_invariant() and h.weak_invariant() and h.color[C] == GRAY


def outcomes(h: TricolorHeap, program: list[tuple[int, int, int | None]]) -> list[set[int]]:
    """The lost sets of all interleavings of the program with the marker."""
    if not program:
        while h.grays():
            h.marker_step(h.grays()[0])
        return [h.lost()]
    out = []
    g = copy.deepcopy(h)
    g.write(*program[0])
    out += outcomes(g, program[1:])
    if h.grays():
        g = copy.deepcopy(h)
        g.marker_step(g.grays()[0])
        out += outcomes(g, program)
    return out


def test_all_interleavings_of_the_example() -> None:
    lost = outcomes(TricolorHeap(EXAMPLE, [A], "none"), PROGRAM)
    assert len(lost) == 10 and lost.count({C}) == 1
    for barrier in ("dijkstra", "yuasa"):
        assert all(s == set() for s in outcomes(TricolorHeap(EXAMPLE, [A], barrier), PROGRAM))


def random_run(rng: random.Random, barrier: str) -> tuple[bool, bool, bool]:
    """Run one random interleaving. Return (strong held, weak held, nothing lost)."""
    n, k = rng.randint(2, 7), rng.randint(1, 2)
    fields = [[rng.choice([None, rng.randrange(n)]) for _ in range(k)] for _ in range(n)]
    roots = rng.sample(range(n), rng.randint(1, 2))
    h = TricolorHeap(fields, roots, barrier)
    strong = weak = True
    writes = 0
    while h.grays():
        if writes < 25 and rng.random() < 0.6:
            live = sorted(h.reachable())
            h.write(rng.choice(live), rng.randrange(k), rng.choice(live + [None]))
            writes += 1
        else:
            h.marker_step(rng.choice(h.grays()))
        strong = strong and h.strong_invariant()
        weak = weak and h.weak_invariant()
    assert all(c != GRAY for c in h.color)
    return strong, weak, not h.lost()


def test_dijkstra_barrier_keeps_the_strong_invariant() -> None:
    rng = random.Random(1978)
    for _ in range(600):
        strong, weak, safe = random_run(rng, "dijkstra")
        assert strong and weak and safe


def test_yuasa_barrier_keeps_the_weak_invariant() -> None:
    rng = random.Random(1990)
    for _ in range(600):
        strong, weak, safe = random_run(rng, "yuasa")
        assert weak and safe


def test_no_barrier_loses_objects() -> None:
    rng = random.Random(21)
    results = [random_run(rng, "none") for _ in range(600)]
    assert any(not safe for _, _, safe in results)
    assert all(not weak for _, weak, safe in results if not safe)
    assert any(not strong for strong, _, _ in results)
