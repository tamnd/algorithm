# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warp-aggregated-atomics/. The authors are listed in prov/714B67.jsonl.
import random
from collections import Counter as Multiset

from warp_aggregated_atomics import (
    WARP, ballot, expected_aggregated_atomics, ffs, filter_per_thread,
    filter_warp_aggregated, histogram_match_any, histogram_per_thread, popc,
)


def test_intrinsics():
    m = ballot([False, True, False, True, True])
    assert m == 0b11010
    assert popc(m) == 3 and ffs(m) == 2 and ffs(0) == 0
    # rank of lane 4 among the set lanes below it: lanes 1 and 3
    assert popc(m & ((1 << 4) - 1)) == 2


def test_filter_same_result_fewer_atomics():
    for seed in range(40):
        rng = random.Random(seed)
        n = rng.choice([0, 1, 31, 32, 33, 64, 100, rng.randrange(1, 2000)])
        data = [rng.randrange(1000) for _ in range(n)]
        q = rng.choice([0.0, 0.01, 0.1, 0.5, 1.0])
        pred = (lambda v: v < 1000 * q)
        a, atom_a = filter_per_thread(data, pred, random.Random(seed + 1))
        b, atom_b = filter_warp_aggregated(data, pred, random.Random(seed + 2))
        k = sum(1 for v in data if pred(v))
        warps_with_hit = sum(1 for w in range(0, n, WARP) if any(pred(v) for v in data[w:w + WARP]))
        assert Multiset(a) == Multiset(b) == Multiset(v for v in data if pred(v))
        assert atom_a == k
        assert atom_b == warps_with_hit <= min(k, -(-n // WARP))
        if k:
            assert atom_a <= WARP * atom_b


def test_aggregated_keeps_lane_order_inside_a_warp():
    rng = random.Random(5)
    data = list(range(256))
    out, _ = filter_warp_aggregated(data, lambda v: v % 3 == 0, rng)
    for w in range(0, 256, WARP):
        mine = [v for v in out if w <= v < w + WARP]
        start = out.index(mine[0])
        assert out[start:start + len(mine)] == mine == sorted(mine)


def test_all_pass_gives_32x_fewer_atomics():
    data = list(range(32 * 50))
    _, a = filter_per_thread(data, lambda v: True, random.Random(1))
    _, b = filter_warp_aggregated(data, lambda v: True, random.Random(2))
    assert (a, b) == (1600, 50)


def test_expected_count_for_random_predicate():
    n, q, trials = 32 * 64, 0.05, 30
    total = 0
    for seed in range(trials):
        rng = random.Random(1000 + seed)
        data = [rng.random() for _ in range(n)]
        total += filter_warp_aggregated(data, lambda v: v < q, rng)[1]
    mean = total / trials
    exp = expected_aggregated_atomics(n, q)
    assert abs(mean - exp) < 0.05 * exp
    assert abs(exp - 64 * (1 - 0.95 ** 32)) < 1e-9


def test_histogram_match_any():
    for seed in range(20):
        rng = random.Random(500 + seed)
        bins = rng.choice([1, 4, 16, 64])
        n = rng.randrange(0, 1000)
        keys = [rng.randrange(bins) for _ in range(n)]
        h1, a1 = histogram_per_thread(keys, bins, random.Random(seed))
        h2, a2 = histogram_match_any(keys, bins, random.Random(seed))
        assert h1 == h2 == [keys.count(b) for b in range(bins)]
        assert a1 == n
        assert a2 == sum(len(set(keys[w:w + WARP])) for w in range(0, n, WARP))
