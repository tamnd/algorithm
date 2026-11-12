# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spanning-tree-protocol/. The authors are listed in prov/6GA09P.jsonl.

import random

from spanning_tree_protocol import (BLOCKED, DESIGNATED, ROOT, BridgedLAN,
                                    centralized_tree)


def random_bridged_lan(rng, nb, nl):
    ids = rng.sample(range(1, 200), nb)
    ports = []
    for b in ids:
        k = rng.randint(1, 4)
        for pid in range(1, k + 1):
            ports.append((b, rng.randrange(nl), pid, rng.choice([1, 2, 4, 10])))
    return ports


def roles_of(net):
    return {(p.bridge, p.pid): net.role[id(p)] for p in net.ports if p.bridge in net.alive}


def components(nodes, edges):
    parent = {x: x for x in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    joined = 0
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            joined += 1
    return len(nodes) - joined, {x: find(x) for x in nodes}


def check_tree(net):
    live = [p for p in net.ports if p.bridge in net.alive]
    nodes = {("B", p.bridge) for p in live} | {("L", p.lan) for p in live}
    all_edges = [(("B", p.bridge), ("L", p.lan)) for p in live]
    act = [(("B", b), ("L", l)) for b, l in net.active_edges()]
    k_all, comp_all = components(nodes, all_edges)
    k_act, comp_act = components(nodes, act)
    # same components, and the active edges form a forest
    assert k_all == k_act
    assert len(act) == len(nodes) - k_act
    for x in nodes:
        for y in nodes:
            if comp_all[x] == comp_all[y]:
                assert comp_act[x] == comp_act[y]


def test_matches_centralized_shortest_path_tree():
    for seed in range(80):
        rng = random.Random(seed)
        nb, nl = rng.randint(1, 12), rng.randint(1, 10)
        ports = random_bridged_lan(rng, nb, nl)
        net = BridgedLAN(ports, maxage=20)
        assert net.run()
        root, cost, roles = centralized_tree(ports)
        assert net.root == root and net.cost == cost
        assert roles_of(net) == roles
        check_tree(net)


def test_each_lan_has_one_designated_port_and_each_bridge_one_root_port():
    for seed in range(40):
        rng = random.Random(500 + seed)
        ports = random_bridged_lan(rng, rng.randint(2, 12), rng.randint(1, 8))
        net = BridgedLAN(ports)
        assert net.run()
        for lan, lst in net.by_lan.items():
            assert sum(net.role[id(p)] == DESIGNATED for p in lst) == 1
        for b, lst in net.by_bridge.items():
            n_root = sum(net.role[id(p)] == ROOT for p in lst)
            assert n_root == (0 if net.root[b] == b else 1)


def test_recovers_after_a_bridge_fails():
    for seed in range(40):
        rng = random.Random(900 + seed)
        ports = random_bridged_lan(rng, rng.randint(3, 12), rng.randint(2, 8))
        net = BridgedLAN(ports, maxage=16)
        assert net.run()
        victim = min(net.bridges) if seed % 2 == 0 else rng.choice(net.bridges)
        net.fail_bridge(victim)
        assert net.run()
        alive = set(net.bridges) - {victim}
        root, cost, roles = centralized_tree(ports, alive)
        assert {b: net.root[b] for b in alive} == root
        assert {b: net.cost[b] for b in alive} == cost
        assert roles_of(net) == roles
        check_tree(net)


def test_small_example():
    # bridges 1, 2, 3 on LANs a, b, c, as in the page
    ports = [(1, "a", 1, 1), (1, "b", 2, 1),
             (2, "a", 1, 1), (2, "c", 2, 1),
             (3, "b", 1, 1), (3, "c", 2, 1)]
    net = BridgedLAN(ports)
    assert net.run()
    r = roles_of(net)
    assert all(net.root[b] == 1 for b in (1, 2, 3))
    assert net.cost == {1: 0, 2: 1, 3: 1}
    assert r[(1, 1)] == r[(1, 2)] == DESIGNATED
    assert r[(2, 1)] == r[(3, 1)] == ROOT
    # on LAN c both offer cost 1; bridge 2 has the lower id
    assert r[(2, 2)] == DESIGNATED and r[(3, 2)] == BLOCKED


def test_two_ports_on_one_lan():
    ports = [(1, "a", 1, 1), (2, "a", 1, 1), (2, "a", 2, 1)]
    net = BridgedLAN(ports)
    assert net.run()
    r = roles_of(net)
    assert r[(2, 1)] == ROOT and r[(2, 2)] == BLOCKED
