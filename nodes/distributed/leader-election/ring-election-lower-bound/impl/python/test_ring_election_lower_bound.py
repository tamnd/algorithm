# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ring-election-lower-bound/. The authors are listed in prov/6S7ZTH.jsonl.

import random

from ring_election_lower_bound import (
    bit_reversal_ring,
    burns_bound,
    lcr_sync,
    lemma_count,
    min_equivalent_count,
    sync_bound,
    time_slice,
    time_slice_run,
)


def harmonic(n: int) -> float:
    return sum(1 / k for k in range(1, n + 1))


def test_bit_reversal_example() -> None:
    assert bit_reversal_ring(8) == [0, 4, 2, 6, 1, 5, 3, 7]


def test_counting_lemma() -> None:
    for m in range(1, 8):
        n = 1 << m
        ids = bit_reversal_ring(n)
        for length in range(1, n + 1):
            got = min_equivalent_count(ids, length)
            assert got >= lemma_count(n, length)
            assert got * 2 * length > n


def test_lemma_count_is_exact_on_small_rings() -> None:
    for m in range(2, 8):
        n = 1 << m
        ids = bit_reversal_ring(n)
        for k in range(0, n // 4):
            assert min_equivalent_count(ids, 2 * k + 1) == lemma_count(n, 2 * k + 1)


def test_burns_recurrence_closed_form() -> None:
    for m in range(1, 16):
        n = 1 << m
        assert burns_bound(n) * 4 == n * (m + 1)


def test_sync_bound_values() -> None:
    assert [sync_bound(1 << m) for m in range(2, 7)] == [4, 10, 24, 56, 128]
    for m in range(2, 14):
        n = 1 << m
        assert sync_bound(n) >= n / 4 * harmonic(n // 4)


def test_lcr_meets_bound_on_bit_reversal_ring() -> None:
    for m in range(2, 10):
        n = 1 << m
        messages, rounds = lcr_sync(bit_reversal_ring(n))
        assert messages >= sync_bound(n)
        assert rounds == n


def test_order_preserving_relabelling_keeps_the_run() -> None:
    rng = random.Random(7)
    for m in range(2, 8):
        n = 1 << m
        ids = bit_reversal_ring(n)
        values = sorted(rng.sample(range(10**6), n))
        relabelled = [values[x] for x in ids]
        assert lcr_sync(relabelled) == lcr_sync(ids)


def test_time_slice_uses_n_messages() -> None:
    rng = random.Random(1)
    for n in range(1, 12):
        for _ in range(10):
            ids = rng.sample(range(1, 40), n)
            leader, messages, rounds = time_slice(ids)
            assert time_slice_run(ids) == (leader, messages, rounds)
            assert messages == n and rounds == n * min(ids)
