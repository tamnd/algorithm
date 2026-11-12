# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-fifty-percent-rule/. The authors are listed in prov/T25KTC.jsonl.

import random

import pytest

from knuth_fifty_percent_rule import Heap, best_fit, census, check, first_fit, simulate


def test_census_of_the_example_heap() -> None:
    h = Heap(64)
    ps = [h.malloc(n, first_fit) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        h.free(p)
    # free (0,12) used (12,4) free (16,8) used (24,4) free (28,16) used (44,4) free (48,16)
    assert census(h) == (4, 3, 0, 0, 2)  # 2M = 2A + B + e: 8 = 6 + 0 + 2


@pytest.mark.parametrize("seed", range(20))
def test_counting_identity_on_random_heaps(seed: int) -> None:
    rng = random.Random(seed)
    h, live = Heap(rng.randint(4, 800)), []
    for _ in range(300):
        if live and rng.random() < 0.5:
            h.free(live.pop(rng.randrange(len(live))))
        else:
            p = h.malloc(rng.randint(1, 40), first_fit)
            if p is not None:
                live.append(p)
        check(h)
        M, A, B, C, e = census(h)
        assert 2 * M == 2 * A + B + e and A + B + C == len(live)


def test_identity_holds_at_every_step_of_the_simulation() -> None:
    r = simulate(1, warm=200, steps=800, audit=True)
    assert r["fails"] == 0


@pytest.mark.parametrize("seed", range(3))
def test_first_fit_ratio(seed: int) -> None:
    r = simulate(seed)
    assert r["fails"] == 0
    assert abs(r["ratio"] - r["predicted"]) < 0.01
    assert abs(r["ratio"] - r["p"] / 2) < 0.01


def test_reported_numbers() -> None:
    r = simulate(0)
    assert (round(r["ratio"], 3), round(r["p"], 3)) == (0.320, 0.625)
    r = simulate(0, choose=best_fit)
    assert (round(r["ratio"], 3), round(r["p"], 3)) == (0.208, 0.404)
    r = simulate(0, H=1 << 18, sizes=(1, 2000))
    assert (round(r["ratio"], 3), round(r["p"], 3)) == (0.498, 0.981)


def test_rule_fails_without_random_frees() -> None:
    r = simulate(0, lifo_frees=True)
    assert r["p"] == 1.0 and r["ratio"] == 1 / 200  # one free block, not N / 2


def test_one_size_means_no_splits() -> None:
    r = simulate(0, sizes=(10, 10))
    assert r["p"] < 0.01 and r["ratio"] < 0.01
