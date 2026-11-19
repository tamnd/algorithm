# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-value-cache/. The authors are listed in prov/JVESYS.jsonl.

import copy
import math
import random

import pytest

from key_value_cache import (
    BlockPool,
    KVCache,
    cache_numbers,
    decode_step,
    forward_full,
    generate,
    make_params,
)

SHAPES = [(8, 2, 2), (8, 4, 2), (8, 4, 1)]  # (d, heads, kv_heads)


def close(a, b, tol=1e-9):
    return all(abs(x - y) <= tol for x, y in zip(a, b)) and len(a) == len(b)


def test_cached_logits_equal_recomputation() -> None:
    for seed in range(4):
        for d, h, g in SHAPES:
            params = make_params(seed, d=d, heads=h, kv_heads=g)
            rng = random.Random(seed)
            tokens = [rng.randrange(7) for _ in range(7)]
            full = forward_full(params, tokens)
            cache = KVCache(2, g, d // h)
            for i, t in enumerate(tokens):
                assert close(decode_step(params, t, i, cache), full[i])
            assert len(cache) == len(tokens)


def test_greedy_generation_is_the_same() -> None:
    for seed in range(3):
        params = make_params(seed, heads=4, kv_heads=2)
        with_cache = generate(params, [1, 2], 6, use_cache=True)
        without = generate(params, [1, 2], 6, use_cache=False)
        assert with_cache == without
        assert len(with_cache) == 8


def test_past_entries_never_change() -> None:
    params = make_params(5)
    cache = KVCache(2, 2, 4)
    snapshots = []
    for i, t in enumerate([3, 1, 4, 1, 5, 2]):
        decode_step(params, t, i, cache)
        snapshots.append(copy.deepcopy(cache.k))
    last = cache.k
    for i, snap in enumerate(snapshots):
        for layer in range(2):
            for g in range(2):
                assert last[layer][g][: i + 1] == snap[layer][g]


def test_score_counts() -> None:
    params = make_params(1, heads=2, kv_heads=2, layers=2)
    n = 4
    # Generating n tokens after a prompt of one token runs positions 0 to n - 1.
    params.counter["scores"] = 0
    generate(params, [0], n, use_cache=True)
    assert params.counter["scores"] == 2 * 2 * n * (n + 1) // 2
    params.counter["scores"] = 0
    generate(params, [0], n, use_cache=False)
    assert params.counter["scores"] == 2 * 2 * n * (n + 1) * (n + 2) // 6
    params.counter["scores"] = 0
    cache = KVCache(2, 2, 4)
    for i, t in enumerate([0, 3, 2, 6]):
        decode_step(params, t, i, cache)
    assert params.counter["scores"] == 2 * 2 * n * (n + 1) // 2  # 10 per head and layer
    params.counter["scores"] = 0
    for m in range(1, n + 1):
        forward_full(params, [0, 3, 2, 6][:m])
    assert params.counter["scores"] == 2 * 2 * n * (n + 1) * (n + 2) // 6  # 20 per head and layer


def test_memory_formula() -> None:
    for d, h, g in SHAPES:
        params = make_params(2, d=d, heads=h, kv_heads=g, layers=3)
        cache = KVCache(3, g, d // h)
        for i, t in enumerate([1, 2, 3, 4, 5]):
            decode_step(params, t, i, cache)
        stored = sum(len(v) for layer in cache.k + cache.v for head in layer for v in head)
        assert stored == cache.num_floats() == cache_numbers(3, 5, d, h, g)
        if g == h:
            assert cache.num_floats() == 2 * 3 * 5 * d
    full = cache_numbers(32, 4096, 4096, 32, 32)
    assert full == 1073741824
    assert full * 2 == 2 * 1024**3
    assert cache_numbers(32, 4096, 4096, 32, 8) * 4 == full


def test_paged_cache_matches_and_reuses_blocks() -> None:
    params = make_params(3, heads=4, kv_heads=2)
    pool = BlockPool(2, 2, 2, block_size=4, num_blocks=5)
    a, b = pool.new_sequence(), pool.new_sequence()
    ta, tb = [1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2]
    fa, fb = forward_full(params, ta), forward_full(params, tb)
    for i in range(6):
        assert close(decode_step(params, ta[i], i, a), fa[i])
        if i < 5:
            assert close(decode_step(params, tb[i], i, b), fb[i])
    assert len(a.table) == math.ceil(6 / 4) and len(b.table) == math.ceil(5 / 4)
    assert len(pool.free) == 1
    a.release()
    assert len(pool.free) == 3
    c = pool.new_sequence()
    tc = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
    fc = forward_full(params, tc)
    for i, t in enumerate(tc):
        assert close(decode_step(params, t, i, c), fc[i])
    assert len(c.table) == 3 and not pool.free
    with pytest.raises(MemoryError):
        decode_step(params, 1, 12, c)
