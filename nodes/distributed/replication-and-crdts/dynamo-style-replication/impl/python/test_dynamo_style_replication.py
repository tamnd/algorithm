# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamo-style-replication/. The authors are listed in prov/4YS13H.jsonl.

import random

from dynamo_style_replication import (Cluster, Ring, clock_of, descends, make_version, reconcile,
                                      sloppy_partition_run, values)

NAMES = ["A", "B", "C", "D", "E", "F"]


def test_preference_list_has_n_distinct_nodes() -> None:
    ring = Ring(NAMES, 8)
    for i in range(200):
        p = ring.preference_list(f"k{i}", 3)
        assert len(p) == 3 == len(set(p))
        assert ring.walk(f"k{i}")[:3] == p


def test_virtual_nodes_spread_keys() -> None:
    counts = {n: 0 for n in NAMES}
    ring = Ring(NAMES, 64)
    for i in range(3000):
        counts[ring.preference_list(f"k{i}", 1)[0]] += 1
    assert max(counts.values()) < 2 * min(counts.values())


def test_reconcile_keeps_concurrent_versions() -> None:
    a = make_version({"A": 2}, "x")
    b = make_version({"A": 1, "B": 1}, "y")
    c = make_version({"A": 2, "B": 1}, "z")
    assert values(reconcile([a, b])) == ["x", "y"]
    assert values(reconcile([a, b, c])) == ["z"]


def test_strict_quorum_reads_see_last_successful_write() -> None:
    for seed in range(200):
        rng = random.Random(seed)
        n = 3
        r, w = rng.choice([(2, 2), (1, 3), (3, 1)])
        c = Cluster(NAMES, n, r, w, seed=seed)
        last: dict[str, dict] = {}
        for step in range(40):
            if rng.random() < 0.3:  # a crash or a recovery between operations
                x = rng.choice(NAMES)
                c.up.symmetric_difference_update({x})
            key = f"k{rng.randrange(3)}"
            ok, ctx = c.get(key, repair=rng.random() < 0.5)
            if not ok:
                continue
            if key in last:
                # some returned version descends from the last successful write
                assert any(descends(clock_of(v), last[key]) for v in ctx), (seed, step)
            if rng.random() < 0.5:
                if c.put(key, f"{key}-{step}", ctx):
                    merged: dict = {}
                    for v in ctx:
                        for k, cnt in clock_of(v).items():
                            merged[k] = max(merged.get(k, 0), cnt)
                    coord = [x for x in c.homes(key) if x in c.up][0]
                    merged[coord] = merged.get(coord, 0) + 1
                    last[key] = merged


def test_sloppy_quorum_gives_a_stale_read() -> None:
    strict = sloppy_partition_run(sloppy=False)
    assert not strict["write_ok"]  # only one home on side 1: the put reports failure
    sloppy = sloppy_partition_run(sloppy=True)
    assert sloppy["write_ok"]  # W = 2 stand-in acks on side 1
    assert sloppy["read_ok"] and sloppy["read"] == ["old"]  # R = 2 on side 2, R + W > N
    c = sloppy["cluster"]
    hinted = [x for x in sloppy["side1"] if c.nodes[x].hints]
    assert len(hinted) == 2


def test_hinted_handoff_restores_the_home_replicas() -> None:
    run = sloppy_partition_run(sloppy=True)
    c, key, homes = run["cluster"], run["key"], run["homes"]
    assert c.handoff() == 2  # the partition heals; the hints go home
    for x in homes:
        assert values(c.nodes[x].get_local(key)) == ["new"]
    assert all(not node.hints for node in c.nodes.values())
    for x, node in c.nodes.items():
        if x not in homes:
            assert key not in node.store  # stand-ins drop their copy
    ok, got = c.get(key)
    assert ok and values(got) == ["new"]


def test_handoff_waits_for_the_home_to_come_back() -> None:
    c = Cluster(NAMES, 3, 2, 2, sloppy=True)
    key = "user:7"
    home = c.homes(key)[2]
    c.up.discard(home)
    assert c.put(key, "v1", [])
    assert c.handoff() == 0
    assert key not in c.nodes[home].store
    c.up.add(home)
    assert c.handoff() == 1
    assert values(c.nodes[home].get_local(key)) == ["v1"]


def test_read_repair_restores_replicas_that_are_read() -> None:
    for seed in range(100):
        c = Cluster(NAMES, 3, 3, 2, seed=seed)  # R = N: every read sees all homes
        rng = random.Random(seed)
        keys = [f"k{i}" for i in range(20)]
        down = rng.choice(NAMES)
        c.up.discard(down)
        for k in keys:
            c.put(k, f"{k}-v", [])
        c.up.add(down)
        read = keys[:10]
        for k in read:
            ok, got = c.get(k)
            assert ok and values(got) == [f"{k}-v"]
        for k in keys:
            homes = c.homes(k)
            if down not in homes:
                continue
            has = values(c.nodes[down].get_local(k))
            if k in read:
                assert has == [f"{k}-v"]
            else:
                assert has == []  # never read: read repair cannot fix it


def test_concurrent_puts_give_siblings_and_a_later_put_merges_them() -> None:
    c = Cluster(NAMES, 3, 2, 2)
    key = "cart:1"
    assert c.put(key, "{book}", [])
    _, ctx = c.get(key)
    homes = c.homes(key)
    # two clients write with the same context through different coordinators
    assert c.put(key, "{book, pen}", ctx, side=set(homes))
    assert c.put(key, "{book, cup}", ctx, side=set(homes[1:]) | set(x for x in NAMES if x not in homes))
    c.r = 3  # read all three homes
    ok, got = c.get(key)
    assert values(got) == ["{book, cup}", "{book, pen}"]
    assert c.put(key, "{book, cup, pen}", got)
    ok, got = c.get(key)
    assert values(got) == ["{book, cup, pen}"]
