# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decoupled-look-back-scan/. The authors are listed in prov/T9HRJ5.jsonl.
import random
from itertools import accumulate

from decoupled_look_back_scan import Deadlock, reduce_then_scan, simulate

SIZES = [0, 1, 2, 7, 8, 31, 32, 33, 64, 100, 255, 256, 257]


def test_matches_accumulate_on_random_inputs_and_orders():
    for seed in range(40):
        rng = random.Random(seed)
        n = rng.choice(SIZES + [rng.randrange(1, 600)])
        data = [rng.randrange(-50, 50) for _ in range(n)]
        tile = rng.choice([1, 2, 4, 8, 16, 32])
        slots = rng.randrange(1, 9)
        for window in (1, 4):
            m = simulate(data, tile, slots, random.Random(seed * 7 + window), window=window)
            assert m.out == list(accumulate(data))


def test_non_commutative_operator():
    for seed in range(20):
        rng = random.Random(100 + seed)
        n = rng.randrange(0, 120)
        data = [rng.choice("abcde") for _ in range(n)]
        m = simulate(data, rng.choice([1, 3, 8]), rng.randrange(1, 6), rng, op=lambda a, b: a + b)
        assert m.out == list(accumulate(data))


def test_chained_scan_also_correct():
    for seed in range(20):
        rng = random.Random(200 + seed)
        n = rng.randrange(0, 300)
        data = [rng.randrange(100) for _ in range(n)]
        m = simulate(data, rng.choice([2, 8, 16]), rng.randrange(1, 6), rng, mode="chained")
        assert m.out == list(accumulate(data))


def test_single_pass_traffic_is_2n_plus_descriptors():
    for seed in range(30):
        rng = random.Random(300 + seed)
        n = rng.randrange(1, 800)
        tile = rng.choice([4, 16, 32])
        slots = rng.randrange(1, 9)
        m = simulate([1] * n, tile, slots, rng)
        assert m.item_reads == n and m.item_writes == n
        t = m.tiles
        assert m.desc_writes == 2 * t - 1      # A and P for every tile but tile 0
        assert m.atomics == t                  # one atomicAdd per block
        assert m.desc_reads == sum(m.lookback.values())


def test_look_back_inspects_at_most_p_predecessors():
    for seed in range(30):
        rng = random.Random(400 + seed)
        slots = rng.randrange(1, 9)
        m = simulate(list(range(500)), 8, slots, rng, window=rng.choice([1, 2, 4]))
        assert max(m.lookback.values()) <= slots
        assert m.lookback[0] == 0


def test_reduce_then_scan_moves_about_3n():
    for n in [1, 31, 32, 33, 1000]:
        for tile in [4, 32]:
            data = list(range(n))
            out, reads, writes = reduce_then_scan(data, tile)
            t = (n + tile - 1) // tile
            assert out == list(accumulate(data))
            assert reads == 2 * n + 2 * t - 1
            assert writes == n + 2 * t
            assert reads + writes == 3 * n + 4 * t - 1


def test_static_tile_index_can_deadlock_dynamic_cannot():
    locked = 0
    for seed in range(40):
        try:
            simulate(list(range(64)), 4, 3, random.Random(seed), dynamic=False)
        except Deadlock:
            locked += 1
        simulate(list(range(64)), 4, 3, random.Random(seed), dynamic=True)
    assert locked > 0
    for seed in range(10):                     # all blocks resident: no deadlock
        simulate(list(range(64)), 4, 16, random.Random(seed), dynamic=False)
