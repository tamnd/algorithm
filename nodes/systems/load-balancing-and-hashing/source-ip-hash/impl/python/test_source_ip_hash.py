# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/source-ip-hash/. The authors are listed in prov/39Q693.jsonl.

import random
from collections import Counter

from source_ip_hash import MOD, SourceIpHash, key_bytes, mod_n_pick, step


def random_ipv4(rng: random.Random, n: int) -> list[str]:
    return ["%d.%d.%d.%d" % (rng.randrange(1, 224), rng.randrange(256), rng.randrange(256), rng.randrange(256)) for _ in range(n)]


def reference(ip: str, servers, weights, down=frozenset()):
    """Brute force: expand each server by its weight into a list of slots, and follow the same hash chain."""
    slots = [s for s, w in zip(servers, weights) for _ in range(w)]
    h = 89
    for _ in range(21):
        h = step(h, key_bytes(ip))
        s = slots[h % len(slots)]
        if s not in down:
            return s
    return None


def test_hash_by_hand():
    # 192.168.1.10: 89 -> (89*113 + 192) % 6271 -> ... over 192, 168, 1
    h = 89
    for b in (192, 168, 1):
        h = (h * 113 + b) % 6271
    assert step(89, key_bytes("192.168.1.10")) == h == 154
    assert key_bytes("192.168.1.10") == bytes([192, 168, 1])
    assert len(key_bytes("2001:db8::1")) == 16


def test_matches_the_reference():
    rng = random.Random(1)
    servers = ["s1", "s2", "s3", "s4"]
    for weights in ([1, 1, 1, 1], [1, 2, 3, 4], [5, 1, 1, 2]):
        lb = SourceIpHash(servers, weights)
        for down in (frozenset(), frozenset({"s2"}), frozenset({"s1", "s3"})):
            for ip in random_ipv4(rng, 300):
                assert lb.pick(ip, down) == reference(ip, servers, weights, down)


def test_same_prefix_same_server_and_ipv6_uses_all_bytes():
    lb = SourceIpHash(["a", "b", "c"])
    assert len({lb.pick("10.1.2.%d" % i) for i in range(256)}) == 1
    picks = {lb.pick("2001:db8::%x" % i) for i in range(1, 200)}
    assert len(picks) == 3


def test_marking_down_moves_only_the_clients_of_that_server():
    rng = random.Random(2)
    servers = ["s%d" % i for i in range(5)]
    lb = SourceIpHash(servers)
    ips = random_ipv4(rng, 5000)
    before = [lb.pick(ip) for ip in ips]
    after = [lb.pick(ip, {"s2"}) for ip in ips]
    for b, a in zip(before, after):
        if b != "s2":
            assert a == b
        else:
            assert a is not None and a != "s2"


def test_removing_a_server_from_the_list_moves_most_clients():
    rng = random.Random(3)
    servers = ["s%d" % i for i in range(5)]
    ips = random_ipv4(rng, 5000)
    moved = sum(1 for ip in ips if mod_n_pick(ip, servers) != mod_n_pick(ip, servers[:2] + servers[3:]))
    assert moved > 0.7 * len(ips)


def test_all_down_gives_up():
    lb = SourceIpHash(["a", "b"])
    assert lb.pick("1.2.3.4", {"a", "b"}) is None


def test_weighted_shares_over_all_hash_values():
    # Every hash value 0..6270 once: the share of a server is its count of residues.
    servers, weights = ["a", "b", "c"], [1, 2, 3]
    slots = [s for s, w in zip(servers, weights) for _ in range(w)]
    cnt = Counter(slots[h % 6] for h in range(MOD))
    assert cnt == Counter({"a": 1046, "b": 2090, "c": 3135})


def test_random_clients_spread_by_weight():
    rng = random.Random(4)
    lb = SourceIpHash(["a", "b", "c"], [1, 2, 3])
    cnt = Counter(lb.pick(ip) for ip in random_ipv4(rng, 30000))
    for s, p in zip("abc", (1 / 6, 2 / 6, 3 / 6)):
        assert abs(cnt[s] / 30000 - p) < 0.02
