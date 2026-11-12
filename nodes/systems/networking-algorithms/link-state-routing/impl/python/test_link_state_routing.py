# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/link-state-routing/. The authors are listed in prov/454KX4.jsonl.

import heapq
import random

from link_state_routing import LSA, LSNetwork, dijkstra_next_hops


def true_dist(graph, s):
    dist, pq = {s: 0}, [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, c in graph[u].items():
            if d + c < dist.get(v, float("inf")):
                dist[v] = d + c
                heapq.heappush(pq, (d + c, v))
    return dist


def random_graph(rng, n, extra, maxw=9):
    g = {u: {} for u in range(n)}
    for v in range(1, n):
        u = rng.randrange(v)
        g[u][v] = g[v][u] = rng.randint(1, maxw)
    for _ in range(extra):
        u, v = rng.sample(range(n), 2)
        g[u][v] = g[v][u] = rng.randint(1, maxw)
    return g


def run_until_quiet(net, step=50, limit=20000):
    t = net.now
    while t < limit:
        t += step
        net.run(t)
        if net.quiet():
            return t
    raise AssertionError("flooding did not finish")


def assert_converged(net):
    g = net.w
    dbs = [{o: (l.seq, tuple(sorted(l.links.items()))) for o, (l, _) in net.DB[y].items()}
           for y in g]
    for y in g:
        want = true_dist(g, y)
        assert net.dist[y] == want
        # only the routers that y can reach must be in its database
        assert set(want) <= set(net.DB[y])
    # routers in one component have the same view of that component
    for y in g:
        for z in true_dist(g, y):
            comp = true_dist(g, y)
            a = {o: v for o, v in dbs[list(g).index(y)].items() if o in comp}
            b = {o: v for o, v in dbs[list(g).index(z)].items() if o in comp}
            assert a == b
    # every pair: the next hops lead to t, without a loop, along a shortest path
    for s in g:
        for t, d in true_dist(g, s).items():
            u, cost, seen = s, 0, {s}
            while u != t:
                h = net.next[u][t]
                assert h in g[u]
                cost += g[u][h]
                u = h
                assert u not in seen
                seen.add(u)
            assert cost == d


def test_dijkstra_helper():
    g = {0: {1: 1, 2: 4}, 1: {0: 1, 2: 1, 3: 5}, 2: {0: 4, 1: 1, 3: 1}, 3: {1: 5, 2: 1}}
    dist, first = dijkstra_next_hops(g, 0)
    assert dist == {0: 0, 1: 1, 2: 2, 3: 3}
    assert first[3] == 1 and first[2] == 1


def test_small_network():
    g = {"A": {"B": 1, "C": 5}, "B": {"A": 1, "C": 1}, "C": {"A": 5, "B": 1}}
    net = LSNetwork(g)
    run_until_quiet(net)
    assert_converged(net)
    assert net.next["A"]["C"] == "B"


def test_random_graphs_with_loss():
    for seed in range(12):
        rng = random.Random(seed)
        g = random_graph(rng, rng.randint(2, 14), rng.randint(0, 12))
        net = LSNetwork(g, loss=0.25, rng=random.Random(seed + 100))
        run_until_quiet(net)
        assert_converged(net)


def test_failures_and_cost_changes():
    for seed in range(10):
        rng = random.Random(1000 + seed)
        g = random_graph(rng, 10, 8)
        net = LSNetwork(g, loss=0.1, rng=random.Random(seed))
        t = run_until_quiet(net)
        edges = sorted({(min(u, v), max(u, v)) for u in g for v in g[u]})
        for k in range(3):
            u, v = rng.choice(edges)
            if v in net.w[u]:
                if rng.random() < 0.5:
                    net.link_down(t + 1, u, v)
                else:
                    net.set_cost(t + 1, u, v, rng.randint(1, 20))
            t = run_until_quiet(net)
            assert_converged(net)


def test_flood_cost_is_about_two_messages_per_link():
    rng = random.Random(7)
    g = random_graph(rng, 20, 30)
    m = sum(len(nb) for nb in g.values()) // 2
    net = LSNetwork(g)
    run_until_quiet(net)
    # each LSA crosses each link at most once in each direction, plus one ack
    assert net.sent <= 2 * (2 * m) * len(g)


def test_linear_sequence_numbers_end_the_flood():
    # the three LSAs of the 1980 ARPANET incident, with linear comparison
    g = {i: {} for i in range(6)}
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3)]:
        g[u][v] = g[v][u] = 1
    net = LSNetwork(g, rxmt=4)
    run_until_quiet(net)
    links = {9: 1}
    for at, seq in [(1, 8), (3, 40), (5, 44)]:
        net.inject(net.now + 1, at, LSA(9, seq, 0, links))
    run_until_quiet(net)
    assert all(net.DB[y][9][0].seq == 44 for y in g)


def test_circular_sequence_numbers_cycle():
    # 6-bit sequence numbers compared as in the ARPANET: 8 < 40 < 44 < 8
    net = LSNetwork({0: {}}, seq_bits=6)
    assert net.newer(40, 8) and net.newer(44, 40) and net.newer(8, 44)
    g = {i: {} for i in range(6)}
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3)]:
        g[u][v] = g[v][u] = 1
    net = LSNetwork(g, rxmt=4, seq_bits=6)
    run_until_quiet(net)
    links = {9: 1}
    for at, seq in [(1, 8), (3, 40), (5, 44)]:
        net.inject(net.now + 1, at, LSA(9, seq, 0, links))
    t, s0 = net.now, net.sent
    net.run(t + 10)
    s1 = net.sent
    net.run(t + 20)
    s2 = net.sent
    # each version replaces the one before it everywhere, so the flood
    # never ends, and here the copies in flight even multiply
    assert not net.quiet()
    assert s2 - s1 > 5 * (s1 - s0) > 0


def test_max_age_flushes_a_dead_router():
    g = {0: {1: 1}, 1: {0: 1, 2: 1}, 2: {1: 1}}
    net = LSNetwork(g, maxage=60, refresh=20)
    net.run(100)
    assert set(net.DB[0]) == {0, 1, 2}
    # router 2 is cut off and stops refreshing: its LSA ages out at 0
    net.link_down(101, 1, 2)
    net.run(300)
    assert 2 not in net.dist[0]
    assert 2 not in net.next[0]
    assert 2 not in net.DB[0] and 2 not in net.DB[1]
