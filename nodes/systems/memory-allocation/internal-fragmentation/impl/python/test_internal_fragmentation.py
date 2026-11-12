# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/internal-fragmentation/. The authors are listed in prov/EYH51V.jsonl.

import random

import pytest

from internal_fragmentation import (
    Heap,
    check,
    class_of,
    first_fit,
    geometric_classes,
    heap_waste,
    pow2_class,
    round_up,
    waste_fraction,
)


def test_rounding_examples() -> None:
    assert [round_up(n, 8) for n in (1, 8, 9, 17)] == [8, 8, 16, 24]
    assert [pow2_class(n) for n in (1, 2, 3, 5, 17, 64, 65)] == [1, 2, 4, 8, 32, 64, 128]
    g = geometric_classes(64, 4)
    assert g == [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64]
    assert [class_of(n, g) for n in (9, 17, 33, 57)] == [10, 20, 40, 64]


def test_worst_case_bounds() -> None:
    g = geometric_classes(1 << 12, 4)
    for n in range(1, 1 << 12):
        assert round_up(n, 16) - n <= 15
        c = pow2_class(n)
        assert c >= n and (c == 1 or c < 2 * n)  # less than half the block is waste
        c = class_of(n, g)
        assert c >= n and 5 * (c - n) < c  # less than 1/(k+1) of the block, k = 4


def test_average_waste_on_uniform_sizes() -> None:
    sizes = list(range(1, 1025))
    g = geometric_classes(1024, 4)
    got = [
        waste_fraction(sizes, lambda n: round_up(n, 8)),
        waste_fraction(sizes, lambda n: round_up(n, 16)),
        waste_fraction(sizes, pow2_class),
        waste_fraction(sizes, lambda n: class_of(n, g)),
    ]
    assert [round(x, 4) for x in got] == [0.0068, 0.0144, 0.2493, 0.076]


def test_heap_example() -> None:
    h = Heap(16)
    live = {}
    p = h.malloc(1, first_fit)  # needs 3 words, gets the minimum block of 4
    live[p] = 1
    q = h.malloc(7, first_fit)  # needs 9 words; the remainder of 3 cannot be split off
    live[q] = 7
    assert check(h) == [(0, 4, 1), (4, 12, 1)]
    assert heap_waste(h, live) == (4, 1 + 3)


@pytest.mark.parametrize("seed", range(15))
def test_words_add_up(seed: int) -> None:
    rng = random.Random(seed)
    H = rng.randint(4, 600)
    h, live = Heap(H), {}
    for _ in range(300):
        if live and rng.random() < 0.45:
            p = rng.choice(sorted(live))
            h.free(p)
            del live[p]
        else:
            n = rng.randint(1, 40)
            p = h.malloc(n, first_fit)
            if p is not None:
                live[p] = n
        bl = check(h)
        free = sum(s for _, s, u in bl if not u)
        tags, slack = heap_waste(h, live)
        assert free + sum(live.values()) + tags + slack == H
        for p, n in live.items():  # minimum-size padding plus a remainder below MIN_BLOCK
            need = max(4, n + 2)
            assert 0 <= h.size(p - 1) - need <= 3


def test_trace_numbers() -> None:
    rng = random.Random(1)
    h, live = Heap(1 << 14), {}
    for _ in range(3000):
        if live and rng.random() < 0.5:
            p = rng.choice(list(live))
            h.free(p)
            del live[p]
        else:
            n = rng.randint(1, 64)
            p = h.malloc(n, first_fit)
            if p:
                live[p] = n
    assert (len(live), sum(live.values()), heap_waste(h, live)) == (30, 1051, (60, 16))
