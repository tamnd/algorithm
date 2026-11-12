# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distance-vector-routing/. The authors are listed in prov/DWVTYT.jsonl.

import heapq
import random

from distance_vector_routing import INF, DVNetwork, rounds_to_reach, synchronous


def dijkstra(graph, s):
    dist = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, c in graph[u].items():
            if d + c < dist.get(v, float("inf")):
                dist[v] = d + c
                heapq.heappush(pq, (d + c, v))
    return dist


def random_graph(rng, n, extra, cmax):
    g = {i: {} for i in range(n)}
    for i in range(1, n):
        j = rng.randrange(i)
        c = rng.randint(1, cmax)
        g[i][j] = g[j][i] = c
    for _ in range(extra):
        i, j = rng.sample(range(n), 2)
        c = rng.randint(1, cmax)
        g[i][j] = g[j][i] = c
    return g


def assert_converged(net, graph):
    for s in graph:
        dist = dijkstra(graph, s)
        for d in graph:
            want = dist.get(d, INF)
            want = INF if want >= INF else want
            assert net.metric(s, d) == want, (s, d, net.metric(s, d), want)
            if s != d and want < INF:
                # follow next hops: loop free, and the cost adds up
                x, cost, seen = s, 0, {s}
                while x != d:
                    h = net.next_hop(x, d)
                    cost += graph[x][h]
                    x = h
                    assert x not in seen or x == d
                    seen.add(x)
                assert cost == want


def line():
    return {"A": {"B": 1}, "B": {"A": 1, "C": 1}, "C": {"B": 1}}


def test_line_converges():
    net = synchronous(line()).run(9)
    assert net.D["A"]["C"] == (2, "B")
    assert net.D["B"]["C"] == (1, "C")


def test_count_to_infinity_on_a_line():
    net = synchronous(line()).run(9)
    net.link_down(10, "B", "C")
    seen = []
    for r in range(1, 15):
        net.run(10 + 2 * r)
        seen.append((net.metric("A", "C"), net.metric("B", "C")))
    assert seen[:4] == [(4, 3), (4, 5), (6, 5), (6, 7)]
    assert seen[12] == (16, 15)       # A reaches 16 after 13 rounds
    assert seen[13] == (16, 16)       # B reaches 16 after 14 rounds


def test_split_horizon_fixes_the_line():
    for mode in ("split", "poison"):
        net = synchronous(line(), mode).run(9)
        net.link_down(10, "B", "C")
        net.run(12)
        assert net.metric("A", "C") == INF and net.metric("B", "C") == INF


def test_three_node_loop_counts_to_infinity_with_poison_reverse():
    g = {"A": {"B": 1, "C": 1}, "B": {"A": 1, "C": 1},
         "C": {"A": 1, "B": 1, "D": 1}, "D": {"C": 1}}
    for mode, want in (("none", 14), ("poison", 14), ("split", 14)):
        net = synchronous(g, mode).run(9)
        net.link_down(10, "C", "D")
        r = rounds_to_reach(net, "ABC", "D", INF, start_round=5)
        assert r == want, (mode, r)
    net = synchronous(g, "poison").run(9)
    net.link_down(10, "C", "D")
    net.run(10 + 2 * 3)
    # after three rounds the false route A -> C -> B -> A is in use somewhere
    assert net.D["B"]["D"] == (5, "C")


def test_cost_increase_on_triangle():
    g = {"x": {"y": 4, "z": 50}, "y": {"x": 4, "z": 1}, "z": {"x": 50, "y": 1}}
    counts = {}
    for mode in ("none", "poison"):
        net = synchronous(g, mode, inf=10 ** 6).run(9)
        net.set_cost(10, "x", "y", 60)
        r = 0
        while not (net.metric("y", "x") == 51 and net.metric("z", "x") == 50):
            r += 1
            net.run(10 + 2 * r)
        counts[mode] = r
    assert counts == {"none": 46, "poison": 2}


def test_random_graphs_all_modes_async():
    rng = random.Random(1058)
    for trial in range(60):
        n = rng.randint(2, 9)
        g = random_graph(rng, n, rng.randint(0, n), 3)
        mode = ("none", "split", "poison")[trial % 3]
        net = DVNetwork(g, mode=mode, period=30, delay=rng.randint(1, 3),
                        triggered=trial % 2 == 0, jitter=10, rng=rng)
        net.run(30 * (n + 3))
        assert_converged(net, g)


def test_after_failure_reconverges():
    rng = random.Random(2453)
    for trial in range(60):
        n = rng.randint(3, 9)
        g = random_graph(rng, n, n, 3)
        net = DVNetwork(g, mode="poison", period=30, delay=1, triggered=True,
                        jitter=5, rng=rng)
        net.run(30 * (n + 2))
        u = rng.randrange(n)
        v = rng.choice(sorted(g[u]))
        net.link_down(net.now + 1, u, v)
        del g[u][v], g[v][u]
        # even when the graph splits, every metric settles: reachable ones
        # to the true distance, unreachable ones to INF (within 16 periods)
        net.run(net.now + 30 * (INF + n + 2))
        assert_converged(net, g)


def test_silent_failure_needs_the_timeout():
    net = DVNetwork(line(), mode="poison", period=30, delay=1, timeout=180,
                    triggered=True)
    net.run(100)
    net.link_cut(101, "B", "C")
    net.run(250)
    assert net.metric("B", "C") == 1          # B still trusts C
    net.run(400)
    assert net.metric("B", "C") == INF and net.metric("A", "C") == INF


def test_converges_from_corrupt_tables():
    rng = random.Random(1992)
    for _ in range(40):
        n = rng.randint(2, 8)
        g = random_graph(rng, n, n, 3)
        net = synchronous(g, rng.choice(["none", "poison"]))
        for y in g:
            for x in g[y]:
                net.V[y][x] = {d: rng.randint(0, 15) for d in g if d != x}
                net.V[y][x][x] = 0
        bound = max(n - 1, INF)
        net.run(2 * (bound + 2))
        assert_converged(net, g)
