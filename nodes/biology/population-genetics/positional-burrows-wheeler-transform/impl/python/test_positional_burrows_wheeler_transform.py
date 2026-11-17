# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/positional-burrows-wheeler-transform/. The authors are listed in prov/39NYBT.jsonl.

import random

import pytest

from positional_burrows_wheeler_transform import (build, long_matches, naive_divergence, naive_maximal_matches,
                                                  naive_set_maximal, naive_sort, set_maximal_matches, step)

EXAMPLE = [
    [0, 1, 0, 1, 0, 1],
    [1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 1, 0],
]


def random_haplotypes(rng, m, n, p=0.4):
    """Haplotypes copied in pieces from a few founders, with some mutation, so that long matches occur."""
    founders = [[int(rng.random() < p) for _ in range(n)] for _ in range(3)]
    out = []
    for _ in range(m):
        src = rng.randrange(3)
        h = []
        for k in range(n):
            if rng.random() < 0.15:
                src = rng.randrange(3)
            v = founders[src][k]
            if rng.random() < 0.05:
                v = 1 - v
            h.append(v)
        out.append(h)
    return out


def test_example_arrays():
    a, d = build(EXAMPLE)
    for k in range(7):
        assert a[k] == naive_sort(EXAMPLE, k)
        assert d[k] == naive_divergence(EXAMPLE, a[k], k)
    # Haplotypes 1 and 6 are identical, so they end next to each other with divergence 0.
    pos = a[6].index(1)
    assert a[6][pos + 1] == 6 and d[6][pos + 1] == 0


def test_one_step_by_hand():
    a, d = step([0, 1, 2, 3], [0, 0, 0, 0], [1, 0, 1, 0], 0)
    assert a == [1, 3, 0, 2]
    assert d == [1, 0, 1, 0]


def test_arrays_against_naive_sort():
    rng = random.Random(1)
    for _ in range(30):
        m, n = rng.randint(1, 12), rng.randint(0, 15)
        x = random_haplotypes(rng, m, n)
        a, d = build(x)
        assert len(a) == n + 1
        for k in range(n + 1):
            assert a[k] == naive_sort(x, k)
            assert d[k] == naive_divergence(x, a[k], k)


def test_set_maximal_against_brute_force():
    rng = random.Random(2)
    assert set_maximal_matches(EXAMPLE) == naive_set_maximal(EXAMPLE)
    for _ in range(60):
        m, n = rng.randint(2, 10), rng.randint(1, 14)
        x = random_haplotypes(rng, m, n)
        assert set_maximal_matches(x) == naive_set_maximal(x)


def test_long_matches_against_brute_force():
    rng = random.Random(3)
    for _ in range(40):
        m, n = rng.randint(2, 10), rng.randint(1, 14)
        x = random_haplotypes(rng, m, n)
        all_max = naive_maximal_matches(x)
        for length in (1, 2, 4, 7):
            want = {(i, j, s, e) for i, j, s, e in all_max if i < j and e - s >= length}
            assert long_matches(x, length) == want


def test_set_maximal_are_maximal_and_cover_each_haplotype():
    rng = random.Random(4)
    x = random_haplotypes(rng, 12, 40)
    sm = set_maximal_matches(x)
    maximal = naive_maximal_matches(x)
    assert sm <= maximal
    # Every haplotype has a set-maximal match that covers each site where it matches anyone.
    for i in range(12):
        mine = [(s, e) for a, _, s, e in sm if a == i]
        for k in range(40):
            if any(x[i][k] == x[j][k] for j in range(12) if j != i):
                assert any(s <= k < e for s, e in mine)


def test_identical_haplotypes():
    x = [[0, 1, 1], [0, 1, 1], [1, 0, 0]]
    assert set_maximal_matches(x) == {(0, 1, 0, 3), (1, 0, 0, 3)}
    assert long_matches(x, 3) == {(0, 1, 0, 3)}


def test_bad_input():
    with pytest.raises(ValueError):
        build([])
    with pytest.raises(ValueError):
        build([[0, 1], [1]])
    with pytest.raises(ValueError):
        build([[0, 2]])
    with pytest.raises(ValueError):
        long_matches([[0, 1]], 0)
