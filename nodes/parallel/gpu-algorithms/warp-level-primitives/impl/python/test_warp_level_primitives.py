# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warp-level-primitives/.

import random
from itertools import accumulate

import pytest

from warp_level_primitives import (FULL, all_sync, any_sync, ballot, match_all, match_any,
                                   reduce_add, shfl, shfl_down, shfl_up, shfl_xor,
                                   warp_allreduce_xor, warp_compact_offsets, warp_inclusive_scan,
                                   warp_reduce_down)

L = list(range(32))


def test_shuffle_rules():
    assert shfl(FULL, L, 5) == [5] * 32
    assert shfl(FULL, L, 3, width=8) == [8 * (l // 8) + 3 for l in L]
    assert shfl_up(FULL, L, 4) == [l if l < 4 else l - 4 for l in L]
    assert shfl_down(FULL, L, 4) == [l + 4 if l < 28 else l for l in L]
    assert shfl_up(FULL, L, 1, width=16) == [l if l % 16 == 0 else l - 1 for l in L]
    assert shfl_xor(FULL, L, 1) == [l ^ 1 for l in L]
    assert shfl_xor(FULL, L, 16, width=16)[:16] == list(range(16))  # later segment: own value
    assert shfl_xor(FULL, L, 16, width=16)[16:] == list(range(16))  # earlier segment: allowed
    assert shfl(FULL, L, [31 - l for l in L]) == L[::-1]


def test_mask_rules():
    half = (1 << 16) - 1
    out = shfl_down(half, L, 1, width=16)
    assert out[:16] == [l + 1 if l < 15 else l for l in range(16)] and out[16:] == [None] * 16
    with pytest.raises(AssertionError):
        shfl(half, L, 20)


def test_votes_and_matches():
    pred = [l % 3 == 0 for l in L]
    b = ballot(FULL, pred)
    assert b == sum(1 << l for l in L if l % 3 == 0)
    assert any_sync(FULL, pred) and not all_sync(FULL, pred)
    assert all_sync(0b1001, pred)  # lanes 0 and 3
    keys = [l % 4 for l in L]
    assert match_any(FULL, keys)[1] == sum(1 << l for l in L if l % 4 == 1)
    assert match_all(FULL, [7] * 32) == (FULL, True) and match_all(FULL, keys) == (0, False)
    assert reduce_add(FULL, L) == [496] * 32


def test_reduce_and_scan_in_five_steps():
    rng = random.Random(14)
    for _ in range(200):
        x = [rng.randrange(-10**6, 10**6) for _ in range(32)]
        s, steps = warp_reduce_down(x)
        assert s == sum(x) and steps == 5
        v, steps = warp_allreduce_xor(x)
        assert v == [sum(x)] * 32 and steps == 5
        v, steps = warp_inclusive_scan(x)
        assert v == list(accumulate(x)) and steps == 5
        assert warp_reduce_down(x, max)[0] == max(x)
        assert warp_inclusive_scan(x, max)[0] == list(accumulate(x, max))


def test_ballot_compaction():
    rng = random.Random(15)
    for _ in range(100):
        pred = [rng.random() < 0.4 for _ in range(32)]
        slots, count = warp_compact_offsets(pred)
        assert count == sum(pred)
        assert [s for s in slots if s is not None] == list(range(count))
