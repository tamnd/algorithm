# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/i-tasser/. The authors are listed in prov/KNTH85.jsonl.

import math
import random
from collections import Counter

from i_tasser import boltzmann, i_tasser, replica_exchange_mc, spicker

RING = [0.0, 2.0, 3.0, 1.0, 4.0, 0.5, 2.0, 3.0]  # a small landscape with two wells, states 0 .. 7


def ring_energy(s: int) -> float:
    return RING[s]


def ring_move(s: int, rng: random.Random) -> int:
    return (s + rng.choice((-1, 1))) % len(RING)  # symmetric proposal


def test_each_replica_samples_its_boltzmann_distribution() -> None:
    temps = (0.7, 1.2, 2.0, 3.5)
    samples = replica_exchange_mc(ring_energy, ring_move, [0], temps, 60000, random.Random(1))
    for r, t in enumerate(temps):
        exact = boltzmann(ring_energy, range(len(RING)), t)
        seen = Counter(samples[r][1000:])  # drop a short burn-in
        total = sum(seen.values())
        tv = 0.5 * sum(abs(seen[s] / total - exact[s]) for s in exact)
        assert tv <= 0.03, (t, tv)  # total variation distance, tolerance for 59000 correlated samples


def test_swaps_help_a_cold_replica_cross_a_barrier() -> None:
    # A tall barrier at state 4 traps a single cold chain in the well it starts in.
    land = [0.5, 1.0, 3.0, 6.0, 9.0, 6.0, 3.0, 1.0, 0.0, 1.0]

    def e(s: int) -> float:
        return land[s]

    def move(s: int, rng: random.Random) -> int:
        y = s + rng.choice((-1, 1))
        return y if 0 <= y < len(land) else s  # rejection at the walls keeps the proposal symmetric

    alone = replica_exchange_mc(e, move, [0], (0.4,), 20000, random.Random(2))[0]
    mixed = replica_exchange_mc(e, move, [0], (0.4, 1.0, 2.5, 6.0), 20000, random.Random(2))[0]
    assert max(alone) < 4  # never crossed
    exact = boltzmann(e, range(len(land)), 0.4)
    right = sum(p for s, p in exact.items() if s > 4)
    frac = sum(1 for s in mixed if s > 4) / len(mixed)
    assert abs(frac - right) <= 0.05


def brute_force_clusters(points, cutoff):
    """The same greedy rule, recomputed from scratch with explicit distance checks each round."""
    left = list(range(len(points)))
    out = []
    while left:
        best = None
        for i in left:
            cnt = sum(1 for j in left if abs(points[i] - points[j]) <= cutoff)
            if best is None or cnt > best[0]:
                best = (cnt, i)
        c = best[1]
        members = [j for j in left if abs(points[c] - points[j]) <= cutoff]
        out.append((c, members))
        left = [j for j in left if j not in members]
    return out


def test_spicker_matches_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(100):
        pts = [round(rng.uniform(0, 10), 2) for _ in range(rng.randint(1, 25))]
        cut = rng.choice((0.3, 0.8, 1.5))
        got = spicker(pts, lambda a, b: abs(a - b), cut)
        assert got == brute_force_clusters(pts, cut)
        covered = sorted(j for _, m in got for j in m)
        assert covered == list(range(len(pts)))  # a partition of the decoys


def test_page_example_clusters() -> None:
    pts = [1.0, 1.4, 2.1, 2.3, 2.6, 5.0, 5.3, 9.0]
    got = spicker(pts, lambda a, b: abs(a - b), 0.8)
    assert got == [(2, [1, 2, 3, 4]), (5, [5, 6]), (0, [0]), (7, [7])]


def test_two_round_pipeline_finds_the_deep_well() -> None:
    def e(x: int) -> float:
        return min(0.02 * (x - 10) ** 2 - 3.0, 0.05 * (x - 45) ** 2 - 5.0) + 0.3 * math.sin(x)

    def move(x: int, rng: random.Random) -> int:
        y = x + rng.choice((-2, -1, 1, 2))
        return y if 0 <= y < 60 else x

    best, clusters = i_tasser(e, move, [10], lambda a, b: abs(a - b), 3.0,
                              (0.5, 1.0, 2.0, 4.0, 8.0), 6000, random.Random(4), restraint_weight=0.01)
    assert best == min(range(60), key=e)
    assert len(clusters[0][1]) >= len(clusters[-1][1])
