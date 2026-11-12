# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sticky-sessions/. The authors are listed in prov/GNHJ0X.jsonl.

import random

from sticky_sessions import (CookieBalancer, Ring, ip_key, load_per_server, mod_server,
                             moved_by_mod_removal)


def random_clients(rng: random.Random, n: int) -> list[str]:
    return [f"10.{rng.randrange(256)}.{rng.randrange(256)}.{rng.randrange(256)}" for _ in range(n)]


def test_cookie_affinity_and_rebinds():
    # Each session stays on one server while it is in the pool; when the server
    # leaves, exactly its sessions move, each once, and then stay put.
    for seed in range(30):
        rng = random.Random(seed)
        servers = [f"s{i}" for i in range(rng.randint(2, 6))]
        lb = CookieBalancer(servers)
        cookie: dict[str, str | None] = {}
        where: dict[str, str] = {}
        removed_sessions: set[str] = set()
        moves = 0
        for step in range(400):
            sess = f"c{rng.randrange(60)}"
            server, new_cookie = lb.route(sess, cookie.get(sess))
            if new_cookie is not None:
                cookie[sess] = new_cookie
                if sess in where:
                    assert sess in removed_sessions
                    removed_sessions.discard(sess)
                    moves += 1
            elif sess in where:
                assert server == where[sess]
            where[sess] = server
            if step % 97 == 96 and len(lb.pool) > 1:
                gone = rng.choice(lb.pool)
                lost = lb.remove(gone)
                assert lost == {c for c, s in where.items() if s == gone}
                removed_sessions |= lost
        assert moves == lb.rebinds


def test_new_server_gets_only_new_sessions():
    lb = CookieBalancer(["A", "B"])
    cookies = {f"c{i}": lb.route(f"c{i}", None)[1] for i in range(1, 7)}
    assert [cookies[f"c{i}"] for i in range(1, 7)] == ["A", "B", "A", "B", "A", "B"]
    lost = lb.remove("A")
    assert lost == {"c1", "c3", "c5"}
    for c in sorted(lost):
        server, cookies[c] = lb.route(c, cookies[c])
        assert server == "B"
    lb.add("C")
    assert all(lb.route(c, cookies[c])[0] == "B" for c in cookies)
    assert [lb.route(f"n{i}", None)[0] for i in range(7)] == ["C"] * 6 + ["B"]
    assert lb.rebinds == 3


def test_mod_removal_moves_all_but_one_nth():
    # Theorem: removing any one of n servers keeps exactly n - 1 of every n(n - 1) keys.
    for n in range(2, 16):
        for j in range(n):
            assert moved_by_mod_removal(n, j) == n * (n - 1) - (n - 1)
    servers = ["s0", "s1", "s2", "s3"]
    assert [k for k in range(12) if mod_server(k, servers) == mod_server(k, servers[:3])] == [0, 1, 2]


def test_ring_moves_only_the_lost_server_clients():
    rng = random.Random(1)
    clients = random_clients(rng, 10000)
    keys = {c: ip_key(c) for c in clients}
    servers = ["s0", "s1", "s2", "s3"]
    ring = Ring(servers, 100)
    before = {c: ring.lookup(k) for c, k in keys.items()}
    ring.remove("s3")
    after = {c: ring.lookup(k) for c, k in keys.items()}
    moved = {c for c in clients if before[c] != after[c]}
    assert moved == {c for c in clients if before[c] == "s3"}
    assert len(moved) == 2366
    mod_before = {c: mod_server(k, servers) for c, k in keys.items()}
    mod_after = {c: mod_server(k, servers[:3]) for c, k in keys.items()}
    assert sum(1 for c in clients if mod_before[c] != mod_after[c]) == 7514
    ring2 = Ring(servers, 100)
    ring2.add("s4")
    grown = {c: ring2.lookup(k) for c, k in keys.items()}
    assert all(grown[c] == "s4" for c in clients if grown[c] != before[c])


def test_shared_address_concentrates_load():
    # Many users behind one NAT address all land on one server.
    rng = random.Random(2)
    clients = random_clients(rng, 8000) + ["203.0.113.7"] * 2000
    ring = Ring(["s0", "s1", "s2", "s3"], 100)
    count: dict[str, int] = {}
    for c in clients:
        s = ring.lookup(ip_key(c))
        count[s] = count.get(s, 0) + 1
    target = ring.lookup(ip_key("203.0.113.7"))
    assert count[target] == max(count.values())
    assert count[target] >= 2000


def test_prefix_key_groups_a_subnet():
    keys = {ip_key(f"192.0.2.{i}", prefix_octets=3) for i in range(256)}
    assert len(keys) == 1
    assert len({ip_key(f"192.0.2.{i}") for i in range(256)}) == 256


def test_heavy_session_skews_load():
    assign = {"a1": "A", "a2": "A", "a3": "A", "b1": "B", "b2": "B", "b3": "B"}
    weight = {"a1": 50, "a2": 1, "a3": 1, "b1": 1, "b2": 1, "b3": 1}
    assert load_per_server(assign, weight) == {"A": 52, "B": 3}
