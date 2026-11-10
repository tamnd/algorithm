# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scatter-and-gather/. The authors are listed in prov/FB12GR.jsonl.

import operator
import random

import pytest

from scatter_and_gather import WriteConflict, gather, inverse, is_exclusive, permute, scatter

SIZES = [0, 1, 2, 3, 5, 8, 17, 64, 100]


def test_example() -> None:
    a = ["a", "b", "c", "d"]
    assert gather(a, [2, 0, 0, 3]) == ["c", "a", "a", "d"]
    assert permute(a, [2, 0, 3, 1]) == ["b", "d", "a", "c"]
    out = scatter([5, 6, 7], [1, 1, 3], [0, 0, 0, 0], rule="priority")
    assert out == [0, 5, 0, 7]


def test_gather_against_comprehension() -> None:
    rng = random.Random(11)
    for n in SIZES:
        a = [rng.randint(-9, 9) for _ in range(max(n, 1))]
        idx = [rng.randrange(len(a)) for _ in range(n)]
        assert gather(a, idx) == [a[j] for j in idx]


def test_scatter_distinct_against_loop() -> None:
    rng = random.Random(12)
    for n in SIZES:
        m = n + rng.randint(0, 5)
        idx = rng.sample(range(m), n)
        a = [rng.randint(-9, 9) for _ in range(n)]
        want = [None] * m
        for i in range(n):
            want[idx[i]] = a[i]
        for rule in ("exclusive", "common", "arbitrary", "priority"):
            assert scatter(a, idx, [None] * m, rule=rule) == want
        assert is_exclusive(idx)


def test_crcw_rules_with_conflicts() -> None:
    rng = random.Random(13)
    for n in SIZES[2:]:
        m = max(1, n // 3)
        idx = [rng.randrange(m) for _ in range(n)]
        a = [rng.randint(-9, 9) for _ in range(n)]
        assert not is_exclusive(idx)
        with pytest.raises(WriteConflict):
            scatter(a, idx, [0] * m, rule="exclusive")
        # priority: the smallest writer wins, which a reversed serial loop gives
        want = [0] * m
        for i in reversed(range(n)):
            want[idx[i]] = a[i]
        assert scatter(a, idx, [0] * m, rule="priority") == want
        # arbitrary: each written cell gets one of its writers' values
        got = scatter(a, idx, [0] * m, rule="arbitrary", rng=random.Random(n))
        for j in set(idx):
            assert got[j] in [a[i] for i in range(n) if idx[i] == j]
        # combining with +: a histogram of the values by index
        want = [0] * m
        for i in range(n):
            want[idx[i]] += a[i]
        assert scatter(a, idx, [0] * m, rule="combining", combine=operator.add) == want


def test_common_rule() -> None:
    assert scatter([1, 1, 2], [0, 0, 1], [0, 0], rule="common") == [1, 2]
    with pytest.raises(WriteConflict):
        scatter([1, 3], [0, 0], [0], rule="common")


def test_permute_and_inverse() -> None:
    rng = random.Random(14)
    for n in SIZES:
        p = list(range(n))
        rng.shuffle(p)
        a = [rng.randint(0, 99) for _ in range(n)]
        b = permute(a, p)
        assert [b[p[i]] for i in range(n)] == a
        assert gather(b, p) == a
        q = inverse(p)
        assert all(q[p[i]] == i for i in range(n))
        assert gather(a, q) == b


def test_one_step_reads_old_values() -> None:
    # Shift right by one in a single step: every read sees the old array.
    a = [1, 2, 3, 4]
    assert scatter(a, [1, 2, 3, 0], list(a)) == [4, 1, 2, 3]
