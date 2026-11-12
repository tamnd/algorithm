# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chord/. The authors are listed in prov/W8KBGE.jsonl.

import math
import random

import pytest

from chord import Ring, between, rounds_to_ideal, successor_of


def test_between_matches_modular_definition():
    size = 16
    for a in range(size):
        for b in range(size):
            for c in range(size):
                if a == c:
                    want = b != a
                else:
                    want = 0 < (b - a) % size < (c - a) % size
                assert between(a, b, c) == want


def test_page_example():
    ring = Ring(6, 2)
    ring.create([1, 8, 14, 21, 32, 38, 42, 48, 51, 56])
    assert ring.nodes[8].finger == [14, 14, 14, 21, 32, 42]
    assert ring.find_successor(8, 54) == (56, 2)  # 8 -> 42 -> 51, whose successor is 56
    assert ring.find_successor(42, 3) == (8, 1)  # 42 -> 1, whose successor is 8
    assert ring.find_successor(1, 1) == (1, 2)  # 1 -> 38 -> 56, whose successor is 1


def test_lookups_on_ideal_ring():
    rng = random.Random(3)
    m = 10
    for n in (5, 17, 64, 300):
        ring = Ring(m, 3)
        ring.create(rng.sample(range(1 << m), n))
        live = ring.live_ids()
        for key in range(1 << m):
            start = rng.choice(live)
            got, hops = ring.find_successor(start, key)
            assert got == successor_of(live, key)
            assert hops <= m


def test_mean_hops_near_half_log_n():
    rng = random.Random(4)
    m, n = 32, 1024
    ring = Ring(m, 4)
    ring.create(rng.sample(range(1 << m), n))
    live = ring.live_ids()
    hops = [ring.find_successor(rng.choice(live), rng.randrange(1 << m))[1] for _ in range(3000)]
    mean = sum(hops) / len(hops)
    assert 0.4 * math.log2(n) < mean < 0.6 * math.log2(n)


def test_create_needs_r_plus_one_nodes():
    with pytest.raises(ValueError):
        Ring(8, 3).create([1, 2, 3])


def test_joins_and_failures_converge():
    rng = random.Random(5)
    m, r = 16, 3
    for trial in range(4):
        ring = Ring(m, r)
        ids = rng.sample(range(1 << m), 160)
        ring.create(ids[: r + 1])
        for ident in ids[r + 1:]:
            ring.join(ident, rng.choice(ring.live_ids()))
            for _ in range(rng.randrange(4)):
                ring.stabilize(rng.choice(ring.live_ids()))
            assert ring.has_live_successor()
        rounds_to_ideal(ring, rng)
        # Fail nodes while each successor list keeps a live entry.
        for ident in rng.sample(ring.live_ids(), 40):
            ring.fail(ident)
            if not ring.has_live_successor():
                ring.nodes[ident].alive = True
            if rng.random() < 0.3:
                ring.stabilize(rng.choice(ring.live_ids()))
        rounds_to_ideal(ring, rng)
        live = ring.live_ids()
        # The ring is ideal, so lookups are right even with stale fingers.
        for _ in range(500):
            key = rng.randrange(1 << m)
            assert ring.find_successor(rng.choice(live), key)[0] == successor_of(live, key)
        for ident in live:
            for i in range(m):
                ring.fix_finger(ident, i)
                assert ring.nodes[ident].finger[i] == successor_of(live, (ident + (1 << i)) % (1 << m))
