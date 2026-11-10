# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/munro-paterson-algorithm/. The authors are listed in prov/T3177E.jsonl.

import math
import random

import pytest

from munro_paterson_algorithm import build_sample, lemma2_bounds, select, thin

STREAM = [14, 3, 25, 9, 30, 1, 18, 22, 7, 27, 12, 5, 20, 31, 16, 0, 29, 10, 24, 2, 13, 26, 8, 19, 4, 28, 11, 23, 6, 17, 15, 21]


def passes_over(data: list):
    return lambda: iter(data)


def test_worked_example() -> None:
    blocks = [sorted(STREAM[i : i + 8]) for i in range(0, 32, 8)]
    assert [thin(b) for b in blocks] == [[3, 14, 22, 30], [5, 12, 20, 31], [8, 13, 24, 29], [6, 15, 21, 28]]
    sample, r = build_sample([(0, x, i) for i, x in enumerate(STREAM)], 8)
    assert r == 2
    assert [key[1] for key in sample] == [5, 8, 14, 15, 22, 24, 29, 31]
    value, stats = select(passes_over(STREAM), 11, 8, cap=16)
    assert value == 10
    assert stats["passes"] == 2
    assert stats["populations"] == [32, 10]
    assert stats["bounds"] == [14]


def test_lemma2_on_random_populations() -> None:
    rng = random.Random(1980)
    for _ in range(300):
        s = rng.choice([2, 4, 6, 8])
        n = rng.randint(1, 150)
        keys = [(0, x, 0) for x in rng.sample(range(1000), n)]
        sample, r = build_sample(keys, s)
        assert len(sample) == s
        order = sorted(keys)
        for j, key in enumerate(sample, 1):
            if key[0] == 1:
                continue
            low, high = lemma2_bounds(r, j)
            assert low <= order.index(key) <= high


def test_edges() -> None:
    assert select(passes_over([7]), 1, 2)[0] == 7
    assert select(passes_over([4, 4, 4, 4, 4]), 3, 4)[0] == 4
    data = list(range(100, 0, -1))
    assert select(passes_over(data), 1, 16)[0] == 1
    assert select(passes_over(data), 100, 16)[0] == 100
    with pytest.raises(ValueError):
        select(passes_over(data), 101, 16)
    with pytest.raises(ValueError):
        select(passes_over(data), 1, 3)


def test_random_exact_selection_against_sorting() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randint(1, 300)
        s = 4 * math.ceil(math.log2(n + 1)) + rng.choice([0, 2, 4])
        data = [rng.randint(0, rng.choice([5, 50, 10**6])) for _ in range(n)]
        if rng.random() < 0.2:
            data.sort(reverse=rng.random() < 0.5)
        k = rng.randint(1, n)
        value, stats = select(passes_over(data), k, s, cap=2 * s)
        assert value == sorted(data)[k - 1]
        for r, peak in zip(stats["levels"], stats["peaks"]):
            assert peak <= r * s // 2 + s  # the storage bound of one sampling pass
        for r, later, bound in zip(stats["levels"], stats["populations"][1:], stats["bounds"]):
            assert later <= bound <= (2 * r - 1) * (1 << r) + 2 or r == 0


def test_pass_count_on_a_larger_stream() -> None:
    n = 1 << 14
    data = list(range(n))
    random.Random(3).shuffle(data)
    value, stats = select(passes_over(data), n // 2, 64, cap=512)
    assert value == n // 2 - 1
    assert stats["passes"] <= 4
    assert stats["levels"][0] == 8 and stats["bounds"][0] == 15 * 256 + 2
    assert max(stats["peaks"]) <= 8 * 32 + 64
