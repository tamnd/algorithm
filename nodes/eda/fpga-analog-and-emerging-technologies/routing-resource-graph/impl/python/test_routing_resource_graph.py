# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/routing-resource-graph/. The authors are listed in prov/4ASKQ1.jsonl.

import random

from routing_resource_graph import PAIRS, RoutingResourceGraph, expected_counts, track_map

PATTERNS = ["subset", "universal", "turning"]


def random_graph(rng: random.Random) -> RoutingResourceGraph:
    w = rng.randint(1, 3)
    return RoutingResourceGraph(
        rng.randint(1, 3),
        rng.randint(1, 3),
        w,
        rng.randint(1, 3),
        rng.randint(1, w),
        rng.randint(1, w),
        rng.choice(PATTERNS),
    )


def random_nets(g: RoutingResourceGraph, rng: random.Random) -> list[tuple[int, list[int]]]:
    blocks = [(x, y) for x in range(1, g.nx + 1) for y in range(1, g.ny + 1)]
    sinks = [(x, y, p) for x, y in blocks for p in range(g.pins)]
    rng.shuffle(blocks)
    rng.shuffle(sinks)
    nets = []
    for x, y in blocks[: rng.randint(1, len(blocks))]:
        k = rng.randint(1, 3)
        mine = [s for s in sinks if (s[0], s[1]) != (x, y)][:k]
        if not mine:
            continue
        for s in mine:
            sinks.remove(s)
        nets.append((g.node(("SOURCE", x, y)), [g.node(("SINK",) + s) for s in mine]))
    return nets


def reachable(g: RoutingResourceGraph, start: int, blocked: set[int]) -> set[int]:
    """Plain depth-first search, written apart from the router."""
    if start in blocked:
        return set()
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in g.out[u]:
            if v not in seen and v not in blocked:
                seen.add(v)
                stack.append(v)
    return seen


def is_out_tree(edges: set[tuple[int, int]], nodes: set[int], root: int, sinks: list[int]) -> bool:
    """The edges form an out-tree on nodes, rooted at root, whose leaves are sinks."""
    indeg = {v: 0 for v in nodes}
    outdeg = {v: 0 for v in nodes}
    for u, v in edges:
        if u not in nodes or v not in nodes:
            return False
        indeg[v] += 1
        outdeg[u] += 1
    if indeg[root] != 0 or any(indeg[v] != 1 for v in nodes if v != root):
        return False
    if len(edges) != len(nodes) - 1:
        return False
    adj: dict[int, list[int]] = {v: [] for v in nodes}
    for u, v in edges:
        adj[u].append(v)
    seen = {root}
    stack = [root]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    if seen != nodes or not set(sinks) <= nodes:
        return False
    leaves = {v for v in nodes if outdeg[v] == 0 and v != root}
    return leaves <= set(sinks)


def test_counts_match_closed_forms():
    for nx in range(1, 4):
        for ny in range(1, 4):
            for w in range(1, 5):
                for pins in range(1, 4):
                    for pattern in PATTERNS:
                        fc = (w + 1) // 2
                        g = RoutingResourceGraph(nx, ny, w, pins, fc, w, pattern)
                        g.check_invariant()
                        assert (g.num_nodes(), g.num_edges()) == expected_counts(nx, ny, w, pins, fc, w)


def test_track_maps_are_permutations():
    for w in range(1, 7):
        for pattern in PATTERNS:
            for a, b in PAIRS:
                assert sorted(track_map(pattern, a, b, t, w) for t in range(w)) == list(range(w))


def test_example_of_the_page():
    def path(g, keys):
        return [g.node(k) for k in keys]

    for pattern in ("universal", "subset"):
        g = RoutingResourceGraph(2, 1, 2, 1, 2, 1, pattern)
        assert (g.num_nodes(), g.num_edges()) == (22, 56)
        a = (g.node(("SOURCE", 1, 1)), [g.node(("SINK", 2, 1, 0))])
        b = (g.node(("SOURCE", 2, 1)), [g.node(("SINK", 1, 1, 0))])
        r = g.route_all([a, b])
        assert r[0] is not None and len(r[0][1]) == 5
        if pattern == "universal":
            assert r[1] is not None
            assert ("CHANX", 1, 1, 1) in {g.keys[v] for v in r[1][0]}
        else:
            # Both orders fail when routed one net at a time ...
            assert r[1] is None
            assert g.route_all([b, a])[1] is None
            # ... but a legal routing exists: net a goes around the bottom.
            p1 = path(g, [("SOURCE", 1, 1), ("OPIN", 1, 1), ("CHANX", 1, 0, 0), ("CHANX", 2, 0, 0), ("CHANY", 2, 1, 0), ("CHANX", 2, 1, 0), ("IPIN", 2, 1, 0), ("SINK", 2, 1, 0)])
            p2 = path(g, [("SOURCE", 2, 1), ("OPIN", 2, 1), ("CHANY", 1, 1, 0), ("CHANX", 1, 1, 0), ("IPIN", 1, 1, 0), ("SINK", 1, 1, 0)])
            es = g.edges()
            assert all(e in es for p in (p1, p2) for e in zip(p, p[1:]))
            assert not set(p1) & set(p2)


def test_routes_are_disjoint_trees_and_failures_are_real():
    rng = random.Random(4)
    routed = failed = 0
    for _ in range(600):
        g = random_graph(rng)
        nets = random_nets(g, rng)
        result = g.route_all(nets)
        used: set[int] = set()
        es = g.edges()
        for (source, sinks), r in zip(nets, result):
            if r is None:
                # The router gives up only if some sink is out of reach of the source.
                reach = reachable(g, source, used)
                assert not set(sinks) <= reach
                failed += 1
                continue
            nodes, edges = r
            assert nodes.isdisjoint(used)
            assert set(edges) <= es
            assert len(set(edges)) == len(edges)
            assert is_out_tree(set(edges), nodes, source, sinks)
            used |= nodes
            routed += 1
    assert routed > 500 and failed > 0


def test_each_new_path_is_shortest_from_the_tree():
    rng = random.Random(9)
    for _ in range(200):
        g = random_graph(rng)
        nets = random_nets(g, rng)
        if not nets:
            continue
        source, sinks = nets[0]
        r = g.route_net(source, sinks[:1], set())
        if r is None:
            # Possible with the subset pattern and few pin connections.
            assert sinks[0] not in reachable(g, source, set())
            continue
        nodes, edges = r
        # Breadth-first distance from the source, computed apart from the router.
        dist = {source: 0}
        layer = [source]
        while layer:
            nxt = []
            for u in layer:
                for v in g.out[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        nxt.append(v)
            layer = nxt
        assert len(edges) == dist[sinks[0]]


def test_subset_pattern_keeps_the_track():
    g = RoutingResourceGraph(2, 2, 3, 1, 1, 1, "subset")
    for u, v in g.edges():
        ku, kv = g.keys[u], g.keys[v]
        if ku[0] in ("CHANX", "CHANY") and kv[0] in ("CHANX", "CHANY"):
            assert ku[3] == kv[3]
