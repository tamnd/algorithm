# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leader-lease/. The authors are listed in prov/WTCD0Y.jsonl.
"""Leader leases with clocks that drift, in a small simulation.

Each node has a local clock local(t) = offset + rate * t, with a rate in
[1 - true_rho, 1 + true_rho]. A node that grants a lease promises, on its own
clock, not to grant to another node for T. The leader measures its lease on
its own clock from the moment it sent the request, and uses it for T_lease.
With the drift bound rho, the safe choice is T_lease = T * (1 - rho) / (1 + rho).

The leader serves reads from its own copy, with no messages, while its lease
holds. A write needs acknowledgements from a majority of nodes that are
promised to the leader. The checks: no two nodes hold a lease at one real
time, and no read returns a version older than one already committed.
"""

import heapq
import random

INF = float("inf")


class Node:
    def __init__(self, i: int, rate: float, offset: float) -> None:
        self.i, self.rate, self.offset = i, rate, offset
        self.promised_to = None
        self.promise_until = -INF          # local time
        self.version = (0, -1)             # (counter, writer)
        self.committed = (0, -1)
        self.lease_end = -INF              # local time
        self.rid = self.won = 0
        self.req_local = 0.0
        self.grants: dict = {}
        self.need = None                   # first write of a new term, until committed
        self.acks: dict = {}
        self.next_try = -INF

    def clock(self, t: float) -> float:
        return self.offset + self.rate * t


class LeaseSim:
    def __init__(self, seed: int, n: int = 3, T: float = 10.0, rho: float = 0.1,
                 true_rho=None, margin: bool = True, from_receipt: bool = False,
                 delay: float = 0.5, dt: float = 0.1, isolate_prob: float = 0.02) -> None:
        self.rng = rng = random.Random(seed)
        true_rho = rho if true_rho is None else true_rho
        self.n, self.T = n, T
        self.T_lease = T * (1 - rho) / (1 + rho) if margin else T
        self.from_receipt = from_receipt
        self.delay, self.dt, self.isolate_prob = delay, dt, isolate_prob
        self.nodes = [Node(i, rng.uniform(1 - true_rho, 1 + true_rho), rng.uniform(0, 100))
                      for i in range(n)]
        self.isolated: dict = {}           # node -> real time when it rejoins
        self.queue: list = []
        self.seq = 0
        self.t = 0.0
        self.max_commit = (0, -1)
        self.commits = self.reads = self.stale = self.overlap = 0

    # ---- messages ----
    def cut(self, a: int, t: float) -> bool:
        return self.isolated.get(a, -INF) > t

    def send(self, t: float, src: int, dst: int, msg: tuple) -> None:
        if src == dst:
            self.handle(t, dst, msg)
        elif not (self.cut(src, t) or self.cut(dst, t)):
            self.seq += 1
            heapq.heappush(self.queue, (t + self.rng.uniform(0, self.delay), self.seq, dst, msg))

    def handle(self, t: float, dst: int, msg: tuple) -> None:
        node, kind, src = self.nodes[dst], msg[0], msg[1]
        c = node.clock(t)
        major = self.n // 2 + 1
        if kind == "req":
            if c >= node.promise_until or node.promised_to == src:
                node.promised_to, node.promise_until = src, c + self.T
                self.send(t, dst, src, ("grant", dst, msg[2], node.version))
        elif kind == "grant":
            if msg[2] != node.rid or node.won == node.rid:
                return
            node.grants[src] = msg[3]
            # the node grants to itself last, and only if it is free to
            if c < node.promise_until and node.promised_to != dst:
                return
            if len(node.grants) + 1 < major:
                return
            node.won = node.rid
            node.promised_to, node.promise_until = dst, c + self.T
            end = (c if self.from_receipt else node.req_local) + self.T_lease
            if c >= node.lease_end:        # a new term: learn, then write first
                node.version = max([node.version] + list(node.grants.values()))
                node.lease_end = end
                node.need = self.write(t, dst)
            else:                          # a renewal
                node.lease_end = max(node.lease_end, end)
        elif kind == "write":
            v = msg[2]
            if node.promised_to == src and c < node.promise_until and v >= node.version:
                node.version = v
                self.send(t, dst, src, ("ack", dst, v))
        elif kind == "ack":
            s = node.acks.get(msg[2])
            if s is None or src in s:
                return
            s.add(src)
            if len(s) == major:
                self.commits += 1
                self.max_commit = max(self.max_commit, msg[2])
                node.committed = max(node.committed, msg[2])
                if node.need == msg[2]:
                    node.need = None

    # ---- node actions ----
    def write(self, t: float, i: int) -> tuple:
        node = self.nodes[i]
        v = (node.version[0] + 1, i)
        node.acks[v] = set()
        for d in range(self.n):
            self.send(t, i, d, ("write", i, v))
        return v

    def request(self, t: float, i: int) -> None:
        node = self.nodes[i]
        node.rid += 1
        node.grants = {}
        node.req_local = node.clock(t)
        for d in range(self.n):
            if d != i:
                self.send(t, i, d, ("req", i, node.rid))

    def step(self) -> None:
        rng = self.rng
        self.t = t = self.t + self.dt
        while self.queue and self.queue[0][0] <= t:
            tm, _, dst, msg = heapq.heappop(self.queue)
            self.handle(tm, dst, msg)
        if rng.random() < self.isolate_prob:
            live = [a for a in range(self.n) if not self.cut(a, t)]
            if len(live) > self.n // 2 + 1:
                self.isolated[rng.choice(live)] = t + rng.uniform(5, 30)
        holders = 0
        for node in self.nodes:
            c = node.clock(t)
            holding = c < node.lease_end
            holders += holding
            if holding and node.need is None:
                if rng.random() < 0.3:         # a local read, with no messages
                    self.reads += 1
                    if node.committed < self.max_commit:
                        self.stale += 1
                if rng.random() < 0.05:
                    self.write(t, node.i)
            if c >= node.next_try and (not holding or c > node.lease_end - self.T_lease / 2):
                self.request(t, node.i)
                node.next_try = c + (1.0 if holding else rng.uniform(1, 3))
        self.overlap += holders > 1

    def run(self, horizon: float = 200.0) -> "LeaseSim":
        while self.t < horizon:
            self.step()
        return self


def partition_scenario(leader_rate: float, other_rate: float, margin: bool,
                       rho: float = 0.1) -> LeaseSim:
    """Node 0 takes the lease. At real time 1 it is cut off, but it keeps
    serving local reads until its lease ends on its own clock. Node 1 asks
    for a new lease every 0.2 units of its own clock, and node 2 grants it
    as soon as its promise to node 0 has ended on its own clock."""
    sim = LeaseSim(0, n=3, rho=rho, margin=margin, delay=0.2, isolate_prob=0.0)
    for node, rate in zip(sim.nodes, (leader_rate, other_rate, other_rate)):
        node.rate, node.offset = rate, 0.0
    sim.nodes[1].next_try = sim.nodes[2].next_try = INF
    while sim.t < 1.0:
        sim.step()
    sim.isolated[0] = INF
    n1 = sim.nodes[1]
    while sim.t < 30.0:
        n1.next_try = min(n1.next_try, n1.clock(sim.t) + 0.2)
        sim.step()
    return sim
