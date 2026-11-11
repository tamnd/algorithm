# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epidemic-broadcast-tree/. The authors are listed in prov/HVTE8H.jsonl.

import random

from epidemic_broadcast_tree import Network, is_tree, random_overlay


def build(n: int = 200, seed: int = 1, timeout1: int = 3) -> tuple[Network, list[list[int]]]:
    adj = random_overlay(n, 3, random.Random(seed))
    return Network(adj, random.Random(seed + 1), timeout1=timeout1), adj


def test_first_broadcast_floods_and_leaves_a_spanning_tree() -> None:
    n = 200
    net, adj = build(n)
    links = sum(len(a) for a in adj) // 2
    c = net.broadcast(0, 0)
    assert c["delivered"] == n
    # Every node forwards to all neighbours but its first sender.
    assert c["payload received"] == 2 * links - (n - 1)
    assert is_tree(n, net.tree_edges()) and net.one_sided_eager() == 0


def test_later_broadcasts_use_only_the_tree() -> None:
    n = 200
    net, _ = build(n)
    first = net.broadcast(0, 0)
    for mid in range(1, 4):
        c = net.broadcast(0, mid)
        assert c["delivered"] == n
        assert c["payload received"] == n - 1  # RMR = 0
        assert c.get("GRAFT", 0) == 0 and c.get("PRUNE", 0) == 0
        assert c["ldh"] == first["ldh"]


def test_tree_repairs_after_link_failures() -> None:
    n = 200
    for seed in (1, 5):
        net, _ = build(n, seed)
        net.broadcast(0, 0)
        tree = sorted(tuple(sorted(e)) for e in net.tree_edges())
        for u, v in random.Random(seed + 10).sample(tree, 30):
            net.fail_link(u, v)
        c = net.broadcast(0, 1)
        assert c["delivered"] == n and c["GRAFT"] > 0
        edges = net.tree_edges()
        assert is_tree(n, edges) and not (edges & net.dead)
        c = net.broadcast(0, 2)
        assert c["delivered"] == n and c["payload received"] == n - 1


def test_several_senders_share_one_tree() -> None:
    n = 200
    net, _ = build(n, timeout1=12)
    rng = random.Random(9)
    net.broadcast(rng.randrange(n), 0)
    for mid in range(1, 6):
        c = net.broadcast(rng.randrange(n), mid)
        assert c["delivered"] == n and c["payload received"] == n - 1
    assert is_tree(n, net.tree_edges())


def test_short_timer_grafts_early_but_still_delivers() -> None:
    n = 200
    net, _ = build(n, timeout1=1)
    rng = random.Random(4)
    for mid in range(5):
        c = net.broadcast(rng.randrange(n), mid)
        assert c["delivered"] == n
    assert is_tree(n, net.tree_edges())


def test_deterministic_and_small_cases() -> None:
    a, _ = build(60, 3)
    b, _ = build(60, 3)
    assert a.broadcast(5, 0) == b.broadcast(5, 0)
    path = Network([[1], [0, 2], [1]], random.Random(0))
    c = path.broadcast(0, 0)
    assert c["delivered"] == 3 and c["payload received"] == 2 and c["ldh"] == 2
