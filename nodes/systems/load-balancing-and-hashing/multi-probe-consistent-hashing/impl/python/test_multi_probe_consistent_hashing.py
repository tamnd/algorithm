# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-probe-consistent-hashing/. The authors are listed in prov/JQ763C.jsonl.

import bisect
import random

from multi_probe_consistent_hashing import (
    RING,
    MultiProbeRing,
    arcs,
    exact_shares,
    loads,
    peak_to_mean,
    point,
)


def keys(rng: random.Random, count: int) -> list[str]:
    return ["key-%016x" % rng.getrandbits(64) for _ in range(count)]


def test_one_probe_is_the_plain_ring():
    ring = MultiProbeRing(["n%d" % i for i in range(12)], k=1)
    for key in keys(random.Random(1), 500):
        q = point(key, 1)
        j = bisect.bisect_left(ring.points, q) % len(ring.points)
        assert ring.lookup(key) == ring.owner[ring.points[j]]


def test_exact_shares_sum_to_one_and_k1_gives_arcs():
    ring = MultiProbeRing(["n%d" % i for i in range(50)], k=1)
    a = arcs(ring)
    assert abs(sum(a.values()) - 1) < 1e-12
    for k in [1, 2, 5, 21]:
        sh = exact_shares(a, k)
        assert abs(sum(sh.values()) - 1) < 1e-9
    sh1 = exact_shares(a, 1)
    for name in a:
        assert abs(sh1[name] - a[name]) < 1e-12


def test_simulated_loads_follow_exact_shares():
    rng = random.Random(2)
    nodes = ["n%d" % i for i in range(20)]
    ks = keys(rng, 20000)
    for k in [1, 21]:
        ring = MultiProbeRing(nodes, k)
        sh = exact_shares(arcs(ring), k)
        c = loads(ring, ks)
        for name in nodes:
            mean = sh[name] * len(ks)
            assert abs(c[name] - mean) <= 5 * (mean ** 0.5) + 5


def test_peak_to_mean_k1_against_k21():
    # Median of the exact peak-to-mean over 21 node sets of 1000 nodes.
    peaks = {1: [], 21: []}
    for s in range(21):
        names = ["s%d-n%d" % (s, i) for i in range(1000)]
        a = arcs(MultiProbeRing(names, 1))
        for k in peaks:
            sh = exact_shares(a, k)
            peaks[k].append(max(sh.values()) * len(names))
    med1 = sorted(peaks[1])[10]
    med21 = sorted(peaks[21])[10]
    assert med1 > 5.0  # about ln n for one probe
    assert abs(med21 - 21 / 20) < 0.02  # K / (K - 1) = 1.05
    assert max(peaks[21]) < 1.1


def test_peak_to_mean_of_counts():
    assert peak_to_mean({"a": 1, "b": 3}) == 1.5


def test_monotone_when_a_node_is_added():
    rng = random.Random(3)
    nodes = ["n%d" % i for i in range(30)]
    ks = keys(rng, 3000)
    for k in [1, 21]:
        ring = MultiProbeRing(nodes, k)
        before = {x: ring.lookup(x) for x in ks}
        ring.add("new")
        moved = 0
        for x in ks:
            after = ring.lookup(x)
            if after != before[x]:
                assert after == "new"
                moved += 1
        assert moved > 0


def test_only_the_keys_of_a_removed_node_move():
    rng = random.Random(4)
    nodes = ["n%d" % i for i in range(30)]
    ks = keys(rng, 3000)
    ring = MultiProbeRing(nodes, 21)
    before = {x: ring.lookup(x) for x in ks}
    ring.remove("n7")
    for x in ks:
        if before[x] != "n7":
            assert ring.lookup(x) == before[x]
        else:
            assert ring.lookup(x) != "n7"


def test_distance_wraps_around_the_ring():
    ring = MultiProbeRing(["only"], k=3)
    assert ring.lookup("anything") == "only"
    assert len(arcs(ring)) == 1 and arcs(ring)["only"] == RING / RING
