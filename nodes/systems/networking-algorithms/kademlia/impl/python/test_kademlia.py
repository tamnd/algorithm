# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kademlia/. The authors are listed in prov/Z8T5G5.jsonl.

import math
import random

from kademlia import (
    Network,
    RoutingTable,
    brute_closest,
    bucket_index,
    distance,
    full_network,
    sparse_network,
)


def test_xor_is_a_metric():
    rng = random.Random(1)
    for _ in range(2000):
        x, y, z = (rng.getrandbits(32) for _ in range(3))
        assert distance(x, x) == 0
        assert x == y or distance(x, y) > 0
        assert distance(x, y) == distance(y, x)
        assert distance(x, z) <= distance(x, y) + distance(y, z)
        assert distance(x, y) ^ distance(y, z) == distance(x, z)


def test_xor_is_unidirectional():
    bits = 8
    for x in range(1 << bits):
        dists = sorted(distance(x, y) for y in range(1 << bits))
        assert dists == list(range(1 << bits))


def test_bucket_index_matches_the_range():
    rng = random.Random(2)
    for _ in range(2000):
        a, b = rng.getrandbits(32), rng.getrandbits(32)
        if a == b:
            continue
        i = bucket_index(a, b)
        assert 2**i <= distance(a, b) < 2 ** (i + 1)


def test_bucket_update_rule():
    t = RoutingTable(own=0, bits=8, k=3)
    live = {16, 17, 18, 19}
    ping = lambda c: c in live  # noqa: E731
    for c in (16, 17, 18):  # all in bucket 4: distances 16 to 31
        t.update(c, ping)
    assert t.buckets[4] == [16, 17, 18]
    t.update(16, ping)  # a known contact moves to the tail
    assert t.buckets[4] == [17, 18, 16]
    t.update(19, ping)  # full, the head 17 is live: keep it, drop 19
    assert t.buckets[4] == [18, 16, 17]
    live.discard(18)
    t.update(19, ping)  # full, the head 18 is dead: evict it, add 19
    assert t.buckets[4] == [16, 17, 19]
    t.update(1, ping)  # another bucket
    assert t.buckets[0] == [1]


def test_lookup_equals_brute_force_on_full_tables():
    rng = random.Random(3)
    for _ in range(150):
        bits = rng.choice([6, 8, 16])
        n = rng.randint(1, min(150, 1 << bits))
        k = rng.choice([1, 2, 3, 5, 8, 20])
        alpha = rng.choice([1, 2, 3])
        ids = rng.sample(range(1 << bits), n)
        net = full_network(ids, bits, k, alpha, rng)
        for _ in range(5):
            u, t = rng.choice(ids), rng.randrange(1 << bits)
            got, _ = net.lookup(u, t)
            assert got == brute_closest(ids, t, k)


def test_one_contact_per_bucket_finds_the_closest_node():
    rng = random.Random(4)
    for _ in range(150):
        bits = rng.choice([8, 16, 32])
        n = rng.randint(1, 150)
        k = rng.choice([1, 2, 3, 5])
        alpha = rng.choice([1, 2, 3])
        ids = rng.sample(range(1 << bits), n)
        net = sparse_network(ids, bits, k, alpha, rng)
        for _ in range(5):
            u, t = rng.choice(ids), rng.randrange(1 << bits)
            got, rounds = net.lookup(u, t)
            assert got[0] == brute_closest(ids, t, 1)[0]
            assert rounds <= bits + 1


def test_rounds_grow_like_log_n():
    rng = random.Random(7)
    for n in (64, 1024):
        ids = rng.sample(range(1 << 32), n)
        net = sparse_network(ids, 32, 1, 1, rng)
        rounds = []
        for _ in range(200):
            got, r = net.lookup(rng.choice(ids), rng.randrange(1 << 32))
            rounds.append(r)
        assert sum(rounds) / len(rounds) <= math.log2(n)
        assert max(rounds) <= 2 * math.log2(n)


def test_failed_nodes_are_skipped():
    rng = random.Random(5)
    ids = rng.sample(range(1 << 32), 512)
    net = full_network(ids, 32, 20, 3, rng)
    dead = set(rng.sample(ids, 150))
    for d in dead:
        net.fail(d)
    live = [i for i in ids if i not in dead]
    closest_ok = 0
    for _ in range(200):
        t = rng.randrange(1 << 32)
        got, _ = net.lookup(rng.choice(live), t)
        assert not dead & set(got)
        assert got == sorted(got, key=lambda c: c ^ t)
        closest_ok += got[0] == brute_closest(live, t, 1)[0]
    assert closest_ok >= 190


def test_joins_build_working_tables():
    rng = random.Random(9)
    net = Network(32, 8, 3)
    first = rng.getrandbits(32)
    net.add_node(first)
    members = [first]
    for _ in range(200):
        x = rng.getrandbits(32)
        while x in net.nodes:
            x = rng.getrandbits(32)
        net.join(x, rng.choice(members), rng)
        members.append(x)
    for _ in range(100):
        t = rng.getrandbits(32)
        got, _ = net.lookup(rng.choice(members), t)
        assert got[0] == brute_closest(members, t, 1)[0]
