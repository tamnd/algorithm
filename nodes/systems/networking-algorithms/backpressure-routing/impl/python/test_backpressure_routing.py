# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backpressure-routing/. The authors are listed in prov/0WEF6V.jsonl.

import random

from backpressure_routing import Backpressure, diamond


def run(bp: Backpressure, rates: dict, slots: int, seed: int):
    """rates: (node, commodity) -> mean arrivals per slot, as the integer
    part plus one more packet with the probability of the fraction.
    Returns (backlog at half time, backlog at the end, packets in)."""
    rng = random.Random(seed)
    half, total_in = None, 0
    for t in range(slots):
        arr = {}
        for key, lam in rates.items():
            k = int(lam) + (1 if rng.random() < lam - int(lam) else 0)
            arr[key] = k
            total_in += k
        bp.step(arr)
        if t == slots // 2 - 1:
            half = bp.total_backlog()
    return half, bp.total_backlog(), total_in


def test_hand_slot() -> None:
    bp = diamond()
    bp.q["s"]["d"], bp.q["a"]["d"], bp.q["b"]["d"] = 5, 3, 1
    # s->a: 5-3, s->b: 5-1, a->d: 3-0, b->d: 1-0
    assert [w for w, _ in bp.link_weights()] == [2, 4, 3, 1]
    # {s->a, b->d} has weight 3 and {s->b, a->d} has weight 7.
    assert bp.step({("s", "d"): 1}) == [1, 2]
    assert (bp.q["s"]["d"], bp.q["a"]["d"], bp.q["b"]["d"]) == (5, 2, 2)
    assert bp.delivered["d"] == 1


def test_stable_inside_the_capacity_region() -> None:
    # The wireless diamond carries at most 1 packet per slot from s to d.
    for seed in range(2):
        bp = diamond()
        half, end, total_in = run(bp, {("s", "d"): 0.8}, 10000, seed)
        assert max(half, end) < 50
        assert total_in == bp.delivered["d"] + end  # no packet is lost


def test_bursty_arrivals_near_the_boundary() -> None:
    # Up to 4 packets per slot, each with probability p. The mean backlog
    # grows as the load nears 1 but stays bounded below it.
    means = []
    for p in (0.2, 0.2375):
        bp = diamond()
        rng = random.Random(1)
        total = 0
        for _ in range(10000):
            bp.step({("s", "d"): sum(rng.random() < p for _ in range(4))})
            total += bp.total_backlog()
        assert bp.total_backlog() < 60
        means.append(total / 10000)
    assert means[0] < means[1] < 20


def test_queues_grow_outside_the_capacity_region() -> None:
    bp = diamond()
    half, end, _ = run(bp, {("s", "d"): 1.2}, 20000, 1)
    # The backlog grows by about 1.2 - 1 = 0.2 packets per slot.
    assert abs(end / 20000 - 0.2) < 0.02
    assert abs((end - half) / 10000 - 0.2) < 0.02


def test_wired_diamond_uses_both_paths() -> None:
    # With all four links active at once, the capacity is 2 per slot, and
    # backpressure splits the traffic over both paths without a routing table.
    bp = diamond(wireless=False)
    half, end, _ = run(bp, {("s", "d"): 1.9}, 20000, 2)
    assert max(half, end) < 50
    bp = diamond(wireless=False)
    _, end, _ = run(bp, {("s", "d"): 2.3}, 20000, 2)
    assert abs(end / 20000 - 0.3) < 0.03


def test_dead_end_and_two_commodities() -> None:
    # A wired line 0 - 1 - 2 with links both ways, plus a dead end 1 - 3.
    # Commodity 2 goes from 0 to 2, and commodity 0 from 2 to 0. Each link
    # carries one packet per slot.
    nodes = [0, 1, 2, 3]
    links = [(0, 1), (1, 0), (1, 2), (2, 1), (1, 3), (3, 1)]
    bp = Backpressure(nodes, links, [1] * 6, [list(range(6))], [0, 2])
    half, end, total_in = run(bp, {(0, 2): 0.9, (2, 0): 0.9}, 20000, 3)
    assert max(half, end) < 80
    assert total_in == bp.delivered[0] + bp.delivered[2] + end
