# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyphase-merge-sort/. The authors are listed in prov/VP4CSM.jsonl.

import random

import pytest

from polyphase_merge_sort import perfect_distribution, polyphase_merge_sort


def test_example() -> None:
    f = [12, 3, 8, 1, 14, 6, 2, 11, 9, 5, 13, 4, 10, 7]
    assert polyphase_merge_sort(f, 2, 4) == 3
    assert f == list(range(1, 15))


def test_perfect_distributions() -> None:
    assert perfect_distribution(7, 3) == (3, [4, 3, 2])
    assert perfect_distribution(57, 3) == (6, [24, 20, 13])
    totals = [sum(perfect_distribution(s, 2)[1]) for s in (1, 2, 3, 4, 6, 9, 13)]
    assert totals == [1, 2, 3, 5, 8, 13, 13]


def test_edges() -> None:
    a: list[int] = []
    assert polyphase_merge_sort(a) == 0 and a == []
    a = [1]
    assert polyphase_merge_sort(a) == 0 and a == [1]
    a = [5] * 9
    polyphase_merge_sort(a, 2, 3)
    assert a == [5] * 9
    a = list(range(40, 0, -1))
    polyphase_merge_sort(a, 1, 3)
    assert a == list(range(1, 41))
    with pytest.raises(ValueError):
        polyphase_merge_sort([1], 2, 2)


def test_random_against_sorted() -> None:
    rng = random.Random(1960)
    for _ in range(600):
        n = rng.randint(0, 120)
        m = rng.randint(1, 6)
        t = rng.randint(3, 9)
        f = [rng.randint(-40, 40) for _ in range(n)]
        want = sorted(f)
        phases = polyphase_merge_sort(f, m, t)
        assert f == want
        s = -(-n // m)
        assert phases == (perfect_distribution(s, t - 1)[0] if s > 1 else 0)
