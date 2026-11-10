# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-pack/. The authors are listed in prov/AGKZS1.jsonl.

import random

import pytest

from parallel_pack import (
    Stats,
    blocked_pack,
    pack_positions,
    pack_with_inclusive_scan_wrong,
    parallel_pack,
    split,
    split_radix_sort,
)

SIZES = [0, 1, 2, 3, 4, 5, 7, 8, 9, 16, 31, 100, 257]


def even(v: int) -> bool:
    return v % 2 == 0


def test_example() -> None:
    a = [3, 8, 1, 6, 4, 9, 2, 7]
    flags, x, k = pack_positions(even, a)
    assert flags == [0, 1, 0, 1, 1, 0, 1, 0]
    assert x == [0, 0, 1, 1, 2, 3, 3, 4]
    assert k == 4
    st = Stats()
    assert parallel_pack(even, a, st) == [8, 6, 4, 2]
    assert (st.work, st.rounds) == (30, 8)


def test_against_comprehension() -> None:
    rng = random.Random(21)
    for n in SIZES:
        for density in (0.0, 0.1, 0.5, 0.9, 1.0):
            a = [(rng.random() < density, rng.randint(0, 9), i) for i in range(n)]
            keep = lambda t: t[0]  # noqa: E731
            assert parallel_pack(keep, a) == [t for t in a if keep(t)]


def test_exact_counts() -> None:
    for n in range(1, 300):
        k = (n - 1).bit_length()
        m = 1 << k
        st = Stats()
        parallel_pack(even, list(range(n)), st)
        assert st.work == 2 * n + 2 * (m - 1)
        assert st.work < 6 * n
        assert st.rounds == 2 + 2 * k


def test_positions_distinct_ordered_in_range() -> None:
    rng = random.Random(22)
    for n in SIZES:
        a = [rng.randint(0, 9) for _ in range(n)]
        flags, x, k = pack_positions(lambda v: v < 4, a)
        kept = [x[i] for i in range(n) if flags[i]]
        assert kept == list(range(k))


def test_blocked_pack() -> None:
    rng = random.Random(23)
    for n in SIZES:
        a = [rng.randint(0, 99) for _ in range(n)]
        for p in (1, 2, 3, 7, 64):
            assert blocked_pack(lambda v: v > 40, a, p) == [v for v in a if v > 40]


def test_split_is_stable() -> None:
    rng = random.Random(24)
    a = [(rng.randint(0, 1), i) for i in range(50)]
    assert split(a, lambda t: t[0]) == sorted(a, key=lambda t: t[0])


def test_split_radix_sort() -> None:
    rng = random.Random(25)
    for n in SIZES:
        keys = [rng.randrange(256) for _ in range(n)]
        assert split_radix_sort(keys, 8) == sorted(keys)


def test_inclusive_scan_bug() -> None:
    with pytest.raises(IndexError):
        pack_with_inclusive_scan_wrong(even, [3, 8, 1, 6, 4, 9, 2, 7])
