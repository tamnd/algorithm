# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-fragmentation/. The authors are listed in prov/P2N3SK.jsonl.

import random

import pytest

from external_fragmentation import (
    MIN_BLOCK,
    Heap,
    check,
    first_fit,
    footprint,
    largest_free_fraction,
    stranded,
    trace_measures,
    unusable_fraction,
    worst_fit,
)


def example_heap() -> Heap:
    h = Heap(64)
    ps = [h.malloc(n, first_fit) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        h.free(p)
    return h


def test_example() -> None:
    h = example_heap()
    assert [(a, s) for a, s, u in check(h) if not u] == [(0, 12), (16, 8), (28, 16), (48, 16)]
    assert largest_free_fraction(h) == pytest.approx(1 - 16 / 52)
    assert stranded(h, 17) and h.malloc(15, first_fit) is None  # 52 words free, 17 needed
    assert not stranded(h, 16)
    assert unusable_fraction(h, 17) == 1.0 and unusable_fraction(h, 9) == pytest.approx(8 / 52)
    assert footprint(h) == 48


def test_one_free_block_means_no_fragmentation() -> None:
    h = Heap(100)
    assert largest_free_fraction(h) == 0.0
    p = h.malloc(10, first_fit)
    assert largest_free_fraction(h) == 0.0
    h.free(p)
    assert largest_free_fraction(h) == 0.0
    h = Heap(4)
    h.malloc(2, first_fit)
    assert largest_free_fraction(h) == 0.0  # nothing is free


@pytest.mark.parametrize("seed", range(20))
def test_measures_on_random_traces(seed: int) -> None:
    rng = random.Random(seed)
    h, live = Heap(rng.randint(50, 600)), []
    for _ in range(300):
        if live and rng.random() < 0.45:
            h.free(live.pop(rng.randrange(len(live))))
        else:
            n = rng.randint(1, 40)
            need = max(MIN_BLOCK, n + 2)
            sizes = [s for _, s, u in check(h) if not u]  # the naive view: the block list
            want = 0.0 if not sizes else 1 - max(sizes) / sum(sizes)
            assert largest_free_fraction(h) == pytest.approx(want)
            was_stranded = stranded(h, need)
            p = h.malloc(n, first_fit)
            if p is None:
                # a failure is either a real lack of space or external fragmentation
                assert was_stranded or sum(sizes) < need
                assert was_stranded == (sum(sizes) >= need)
                if was_stranded:
                    assert want > 0
            else:
                live.append(p)
        check(h)


def random_ops(seed: int) -> list[tuple[str, int]]:
    rng = random.Random(seed)
    ops, k = [], 0
    for _ in range(3000):
        if k and rng.random() < 0.5:
            ops.append(("f", rng.randrange(1 << 20)))
            k -= 1
        else:
            ops.append(("m", rng.randint(1, 64)))
            k += 1
    return ops


def test_johnstone_wilson_measures() -> None:
    ff = trace_measures(Heap(1 << 16), random_ops(3), first_fit)
    wf = trace_measures(Heap(1 << 16), random_ops(3), worst_fit)
    assert [round(x, 2) for x in ff] == [1.68, 1.22]
    assert [round(x, 2) for x in wf] == [14.47, 16.35]
