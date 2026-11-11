# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyparview/. The authors are listed in prov/9B51BZ.jsonl.

import random

from hyparview import HyParView


def build(seed: int, n: int = 1000) -> HyParView:
    h = HyParView(seed)
    h.grow(n)
    for _ in range(5):
        h.shuffle_round()
    h.check_failures(refill=True)
    return h


def test_views_are_valid():
    h = build(1, 500)
    for p in h.alive:
        assert len(h.active[p]) <= h.amax
        assert len(h.passive[p]) <= h.pmax
        assert p not in h.active[p] and p not in h.passive[p]
        assert not (h.active[p] & h.passive[p])
    assert h.symmetric()
    assert h.largest_component() == 500


def test_join_reaches_active_and_passive_views():
    h = build(2, 400)
    n = h.join()
    assert 1 <= len(h.active[n]) <= h.amax
    assert all(n in h.active[q] for q in h.active[n])
    assert sum(n in h.passive[p] for p in h.alive) >= 1


def test_stays_connected_after_80_percent_crash():
    for seed in range(3):
        h = build(seed)
        rng = random.Random(seed + 10)
        h.crash(rng.sample(sorted(h.alive), 800))
        # without repair the old active overlay falls apart
        assert h.largest_component() < 100
        h.check_failures()
        assert h.symmetric()
        assert h.largest_component() == 200
        assert h.broadcast(min(h.alive)) == 1.0


def test_most_nodes_stay_connected_after_90_percent_crash():
    for seed in range(3):
        h = build(seed)
        rng = random.Random(seed + 10)
        h.crash(rng.sample(sorted(h.alive), 900))
        h.check_failures()
        assert h.largest_component() >= 95


def test_broadcast_repairs_the_links_it_finds_broken():
    h = build(4)
    rng = random.Random(4)
    h.crash(rng.sample(sorted(h.alive), 300))
    src = min(h.alive)
    h.broadcast(src)
    # the first broadcast finds broken links on its way and repairs them,
    # so the second one reaches almost every live node
    second = h.broadcast(src)
    assert second >= 0.95
