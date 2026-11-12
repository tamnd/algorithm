# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aodv/. The authors are listed in prov/NQ1A74.jsonl.

import random

from aodv import AODV, HOPS, NEXT, SEQ, VALID


def random_links(rng, n, r):
    """A connected unit disk graph on n random points in the unit square."""
    while True:
        pts = [(rng.random(), rng.random()) for _ in range(n)]
        links = [
            (u, v)
            for u in range(n)
            for v in range(u + 1, n)
            if (pts[u][0] - pts[v][0]) ** 2 + (pts[u][1] - pts[v][1]) ** 2 <= r * r
        ]
        if reachable(adjacency(n, links), 0) == set(range(n)):
            return links


def adjacency(n, links):
    adj = [set() for _ in range(n)]
    for u, v in links:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def reachable(adj, s):
    seen, stack = {s}, [s]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def churn(net, rng, rounds, check):
    """Requests, link failures and new links, interleaved with message deliveries."""
    n = net.n
    for _ in range(rounds):
        a = rng.random()
        if a < 0.5:
            s, d = rng.sample(range(n), 2)
            net.request(s, d)
        elif a < 0.8:
            cur = sorted((u, v) for u in range(n) for v in net.adj[u] if u < v)
            if cur:
                net.remove_link(*rng.choice(cur))
        else:
            net.add_link(*rng.sample(range(n), 2))
        if rng.random() < 0.2:  # lose the messages on one link
            busy = sorted(k for k, q in net.queues.items() if q)
            if busy:
                net.queues[rng.choice(busy)].clear()
        check(net)
        for _ in range(rng.randrange(40)):
            if not net.step():
                break
            check(net)


def test_line_discovery():
    net = AODV(5, [(0, 1), (1, 2), (2, 3), (3, 4)], random.Random(1))
    net.request(0, 4)
    net.run()
    assert net.route(0, 4) == [0, 1, 2, 3, 4]
    assert net.route(4, 0) == [4, 3, 2, 1, 0]  # the reverse route from the request
    assert net.table[0][4][HOPS] == 4 and net.table[0][4][SEQ] == 0


def test_break_and_repair_on_a_ring():
    ring = [(i, (i + 1) % 6) for i in range(6)]
    net = AODV(6, ring, random.Random(2))
    net.request(0, 2)
    net.run()
    assert net.route(0, 2) == [0, 1, 2]
    net.remove_link(1, 2)
    net.run()
    e = net.table[0][2]
    assert not e[VALID] and e[SEQ] == 1  # the error carried the larger number back to 0
    net.request(0, 2)
    net.run()
    assert net.route(0, 2) == [0, 5, 4, 3, 2]
    assert net.seq[2] == 1  # the destination raised its number to the requested one


def test_no_loops_and_the_invariant_hold_under_churn():
    def check(net):
        assert net.invariant_violations() == []
        assert not net.has_loop()

    for seed in range(15):
        rng = random.Random(seed)
        net = AODV(12, random_links(rng, 12, 0.4), random.Random(seed + 1000))
        churn(net, rng, 30, check)
        net.run(check=check)


def test_discovery_succeeds_after_the_churn_stops():
    for seed in range(15):
        rng = random.Random(seed)
        net = AODV(12, random_links(rng, 12, 0.4), random.Random(seed + 1000))
        churn(net, rng, 30, lambda x: None)
        net.run()
        for _ in range(10):
            s, d = rng.sample(range(12), 2)
            if d not in reachable(net.adj, s):
                assert net.route(s, d) is None
                continue
            for _ in range(5):
                if net.route(s, d):
                    break
                net.request(s, d)
                net.run()
            assert net.route(s, d) is not None


class NoSequenceNumbers(AODV):
    """A broken variant: ignore sequence numbers and keep them at 0."""

    @staticmethod
    def fresher(entry, seq, hops):
        return entry is None or not entry[VALID] or hops < entry[HOPS]

    def link_broken(self, u, v):
        lost = []
        for d, e in sorted(self.table[u].items()):
            if e[VALID] and e[NEXT] == v:
                e[VALID] = False
                lost.append((d, e[SEQ]))
        if lost:
            self.broadcast(u, ("RERR", tuple(lost)))


def lost_error_scene(cls):
    """Line 0-1-2-3. The link 2-3 breaks, the error from 2 to 1 is lost, and 2 asks for 3."""
    net = cls(4, [(0, 1), (1, 2), (2, 3)], random.Random(3))
    net.request(0, 3)
    net.run()
    net.remove_link(2, 3)
    net.queues[(2, 1)].clear()
    net.request(2, 3)
    net.run()
    return net


def test_a_lost_error_message_cannot_make_a_loop():
    net = lost_error_scene(AODV)
    assert not net.has_loop()
    assert net.invariant_violations() == []
    assert net.route(2, 3) is None  # 3 is unreachable and no false route appears
    assert net.table[1][3][VALID]  # 1 still has its stale route, but 2 will not use it


def test_without_sequence_numbers_the_same_scene_loops():
    net = lost_error_scene(NoSequenceNumbers)
    assert net.has_loop()
    assert net.table[2][3][NEXT] == 1 and net.table[1][3][NEXT] == 2
