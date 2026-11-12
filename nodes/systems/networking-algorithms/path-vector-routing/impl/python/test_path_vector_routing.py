# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-vector-routing/. The authors are listed in prov/CAQP3D.jsonl.

import random
from collections import deque

from path_vector_routing import (
    EPS, PathVector, activation_graph, gadget, has_cycle, is_stable,
    list_rank, stable_assignments)


def bfs_hops(adj, d):
    dist, q = {d: 0}, deque([d])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def random_graph(rng, n, extra):
    g = {u: set() for u in range(n)}
    for v in range(1, n):
        u = rng.randrange(v)
        g[u].add(v)
        g[v].add(u)
    for _ in range(extra if n > 1 else 0):
        u, v = rng.sample(range(n), 2)
        g[u].add(v)
        g[v].add(u)
    return g


def check_shortest(net):
    hops = bfs_hops(net.adj, net.d)
    for u in net.adj:
        p = net.best[u]
        if u not in hops:
            assert p == EPS
            continue
        assert len(p) - 1 == hops[u]
        assert len(set(p)) == len(p)                      # simple path
        assert all(b in net.adj[a] for a, b in zip(p, p[1:]))   # real links
        if u != net.d:
            assert p[1:] == net.best[p[1]]               # consistent suffix


def test_shortest_paths_on_random_graphs():
    for seed in range(20):
        rng = random.Random(seed)
        g = random_graph(rng, rng.randint(1, 12), rng.randint(0, 10))
        net = PathVector(g, 0, rng=random.Random(seed))
        assert net.run()
        check_shortest(net)


def test_reconverges_after_failures_and_repairs():
    for seed in range(15):
        rng = random.Random(500 + seed)
        g = random_graph(rng, 10, 8)
        net = PathVector(g, 0, rng=random.Random(seed))
        net.run()
        edges = sorted({(min(u, v), max(u, v)) for u in g for v in g[u]})
        for _ in range(4):
            u, v = rng.choice(edges)
            if v in net.adj[u]:
                net.link_down(net.now + 1, u, v)
            else:
                net.link_up(net.now + 1, u, v)
            assert net.run()
            check_shortest(net)


def test_no_loop_at_any_time():
    rng = random.Random(3)
    g = random_graph(rng, 12, 14)
    net = PathVector(g, 0, rng=random.Random(4))
    net.run()
    net.link_down(net.now + 1, 0, sorted(g[0])[0])
    while net.events:
        net.run(until=net.events[0][0])
        for u in net.adj:
            p = net.best[u]
            assert len(set(p)) == len(p)


def test_path_exploration_after_withdrawal():
    # a clique plus the destination: when the destination leaves, the other
    # nodes try longer and longer stale paths before they give up
    n = 5
    g = {u: set(range(n + 1)) - {u} for u in range(n + 1)}
    net = PathVector(g, n, rng=random.Random(1))
    net.run()
    base = net.changes
    for u in range(n):
        net.link_down(net.now + 1, u, n)
    assert net.run()
    assert all(net.best[u] == EPS for u in range(n))
    assert net.changes - base > n            # more than one change per node


def test_disagree_has_exactly_two_solutions():
    adj, prefs = gadget("DISAGREE")
    sols = stable_assignments(prefs, adj, 0)
    got = sorted((s[1], s[2]) for s in sols)
    assert got == [((1, 0), (2, 1, 0)), ((1, 2, 0), (2, 0))]


def test_bad_gadget_has_no_solution_and_oscillates():
    adj, prefs = gadget("BAD")
    assert stable_assignments(prefs, adj, 0) == []
    states, edges = activation_graph(prefs, adj, 0)
    assert has_cycle(states, edges)
    # the protocol itself never settles
    net = PathVector(adj, 0, rank=list_rank(prefs), rng=random.Random(2))
    assert not net.run(max_events=20000)


def test_good_gadget_converges_from_every_order():
    adj, prefs = gadget("GOOD")
    sols = stable_assignments(prefs, adj, 0)
    assert len(sols) == 1
    s = sols[0]
    assert (s[1], s[2], s[3], s[4]) == ((1, 3, 0), (2, 0), (3, 0), (4, 3, 0))
    states, edges = activation_graph(prefs, adj, 0)
    assert not has_cycle(states, edges)
    # every dead end of the state graph is the stable solution
    nodes = sorted(adj)
    ends = {a for a in states} - {a for a, _ in edges}
    assert ends == {tuple(s[u] for u in nodes)}
    for seed in range(20):
        net = PathVector(adj, 0, rank=list_rank(prefs), rng=random.Random(seed))
        assert net.run()
        assert is_stable(prefs, net.best, adj, 0)


def test_naughty_gadget_has_a_solution_but_can_oscillate():
    adj, prefs = gadget("NAUGHTY")
    assert len(stable_assignments(prefs, adj, 0)) == 1
    # in lock step (every message takes one tick, no batching) it never settles
    net = PathVector(adj, 0, rank=list_rank(prefs), batch=0, max_delay=1)
    assert not net.run(max_events=20000)
    # with random delays it finds the solution
    for seed in range(20):
        net = PathVector(adj, 0, rank=list_rank(prefs), rng=random.Random(seed))
        assert net.run()
        assert is_stable(prefs, net.best, adj, 0)


def test_disagree_in_lock_step_never_settles():
    adj, prefs = gadget("DISAGREE")
    net = PathVector(adj, 0, rank=list_rank(prefs), batch=0, max_delay=1)
    assert not net.run(max_events=20000)
    assert net.best[1] in ((1, 0), (1, 2, 0))


def test_disagree_reaches_either_solution():
    adj, prefs = gadget("DISAGREE")
    seen = set()
    for seed in range(40):
        net = PathVector(adj, 0, rank=list_rank(prefs), rng=random.Random(seed))
        assert net.run()
        assert is_stable(prefs, net.best, adj, 0)
        seen.add((net.best[1], net.best[2]))
    assert len(seen) == 2
