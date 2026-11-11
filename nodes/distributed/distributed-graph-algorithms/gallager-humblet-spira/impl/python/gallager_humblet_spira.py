# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gallager-humblet-spira/. The authors are listed in prov/2BCNZB.jsonl.

"""The Gallager-Humblet-Spira (GHS) minimum spanning tree algorithm.

Each node runs the code of the 1983 paper (responses (1) to (12) of its
appendix). The network is asynchronous with FIFO channels. A deterministic
discrete event simulator delivers the messages: each message on channel
(u, v) gets a seeded random delay in (0, 1], and a message never overtakes an
earlier message on the same channel. Each node serves its input queue first
come, first served; a message that must wait goes back to the end of the
queue, as in the paper.

Precondition: the graph is connected, has at least two nodes, and the edge
weights are distinct. Cost: at most 5 n log2 n + 2 m messages; with all nodes
awake at time 0 and each delay at most 1, at most 5 n log2 n time units.
"""

import heapq
import math
import random
from collections import deque

INF = math.inf
SLEEPING, FIND, FOUND = "Sleeping", "Find", "Found"
BASIC, BRANCH, REJECTED = "Basic", "Branch", "Rejected"


def message_bits(msg: tuple, n: int) -> int:
    """Bits of an encoded message: a 4-bit type tag, then each field.

    A level or weight costs 2 bits plus its binary length, infinity costs 2
    bits, and a fragment name is an edge weight.
    """
    bits = 4
    for x in msg[1:]:
        if x is None or x == INF:
            bits += 2
        elif isinstance(x, str):
            bits += 2
        else:
            bits += 2 + max(1, int(x).bit_length())
    return bits


class Node:
    """The local state of one node, with the variables of the paper."""

    def __init__(self, uid: int, edges: dict[int, int]) -> None:
        self.uid = uid
        self.w = dict(edges)  # neighbour -> weight of the edge
        self.SN = SLEEPING
        self.SE = {j: BASIC for j in edges}
        self.FN: float = 0
        self.LN = 0
        self.best_edge: int | None = None
        self.best_wt: float = INF
        self.test_edge: int | None = None
        self.in_branch: int | None = None
        self.find_count = 0
        self.halted = False
        self.out: list[tuple[int, tuple]] = []  # messages to send

    def send(self, j: int, msg: tuple) -> None:
        self.out.append((j, msg))

    # (2) procedure wakeup
    def wakeup(self) -> None:
        m = min(self.w, key=lambda j: self.w[j])  # @line L1
        self.SE[m] = BRANCH  # @line L2
        self.LN, self.SN, self.find_count = 0, FOUND, 0
        self.send(m, ("Connect", 0))  # @line L3

    def handle(self, j: int, msg: tuple) -> bool:
        """Serve one message from neighbour j. Return False to defer it."""
        kind = msg[0]
        if kind == "Connect":
            return self.on_connect(j, msg[1])
        if kind == "Initiate":
            self.on_initiate(j, msg[1], msg[2], msg[3])
            return True
        if kind == "Test":
            return self.on_test(j, msg[1], msg[2])
        if kind == "Accept":
            self.on_accept(j)
            return True
        if kind == "Reject":
            self.on_reject(j)
            return True
        if kind == "Report":
            return self.on_report(j, msg[1])
        assert kind == "Change-root"
        self.change_root()  # @line L36
        return True

    # (3) Connect(L) on edge j
    def on_connect(self, j: int, L: int) -> bool:
        if self.SN == SLEEPING:  # @line L4
            self.wakeup()
        if L < self.LN:  # @line L5
            self.SE[j] = BRANCH  # absorb the lower fragment
            self.send(j, ("Initiate", self.LN, self.FN, self.SN))  # @line L6
            if self.SN == FIND:
                self.find_count += 1
            return True
        if self.SE[j] == BASIC:  # @line L7
            return False  # wait: the other fragment is not our MOE yet
        self.send(j, ("Initiate", self.LN + 1, self.w[j], FIND))  # @line L8
        return True

    # (4) Initiate(L, F, S) on edge j
    def on_initiate(self, j: int, L: int, F: float, S: str) -> None:
        self.LN, self.FN, self.SN = L, F, S  # @line L9
        self.in_branch = j
        self.best_edge, self.best_wt = None, INF
        for i in self.SE:  # @line L10
            if i != j and self.SE[i] == BRANCH:
                self.send(i, ("Initiate", L, F, S))
                if S == FIND:
                    self.find_count += 1
        if S == FIND:  # @line L11
            self.test()

    # (5) procedure test
    def test(self) -> None:
        basic = [i for i in self.SE if self.SE[i] == BASIC]
        if basic:  # @line L12
            self.test_edge = min(basic, key=lambda i: self.w[i])
            self.send(self.test_edge, ("Test", self.LN, self.FN))  # @line L13
        else:
            self.test_edge = None  # @line L14
            self.report()

    # (6) Test(L, F) on edge j
    def on_test(self, j: int, L: int, F: float) -> bool:
        if self.SN == SLEEPING:  # @line L15
            self.wakeup()
        if L > self.LN:
            return False  # our level is too low to answer
        if F != self.FN:  # @line L16
            self.send(j, ("Accept",))
            return True
        if self.SE[j] == BASIC:  # @line L17
            self.SE[j] = REJECTED
        if self.test_edge != j:  # @line L18
            self.send(j, ("Reject",))
        else:
            self.test()  # @line L19
        return True

    # (7) Accept on edge j
    def on_accept(self, j: int) -> None:
        self.test_edge = None  # @line L20
        if self.w[j] < self.best_wt:
            self.best_edge, self.best_wt = j, self.w[j]
        self.report()  # @line L21

    # (8) Reject on edge j
    def on_reject(self, j: int) -> None:
        if self.SE[j] == BASIC:  # @line L22
            self.SE[j] = REJECTED
        self.test()  # @line L23

    # (9) procedure report
    def report(self) -> None:
        if self.find_count == 0 and self.test_edge is None:  # @line L24
            self.SN = FOUND
            assert self.in_branch is not None
            self.send(self.in_branch, ("Report", self.best_wt))  # @line L25

    # (10) Report(w) on edge j
    def on_report(self, j: int, w: float) -> bool:
        if j != self.in_branch:  # @line L26
            self.find_count -= 1  # @line L27
            if w < self.best_wt:
                self.best_wt, self.best_edge = w, j
            self.report()  # @line L28
            return True
        if self.SN == FIND:  # @line L29
            return False
        if w > self.best_wt:  # @line L30
            self.change_root()
        elif w == self.best_wt == INF:  # @line L31
            self.halted = True
        return True

    # (11) procedure change-root
    def change_root(self) -> None:
        assert self.best_edge is not None
        if self.SE[self.best_edge] == BRANCH:  # @line L32
            self.send(self.best_edge, ("Change-root",))  # @line L33
        else:
            self.send(self.best_edge, ("Connect", self.LN))  # @line L34
            self.SE[self.best_edge] = BRANCH  # @line L35


def ghs(
    n: int,
    edges: list[tuple[int, int, int]],
    seed: int = 0,
    wake: list[int] | None = None,
    schedule: str = "random",
) -> dict:
    """Run GHS on the graph and return the result and the costs.

    edges holds (u, v, weight) with distinct weights. wake lists the nodes
    that wake up on their own at time 0 (default: all). schedule is "random"
    (delays uniform in (0, 1]), "unit" (every delay 1) or "slowlow" (edges at
    nodes with a small id are slow). Returns a dict with the MST as a set of
    weights, the number of messages, the number of messages of each type,
    the finish time, the largest message in bits and the halted nodes.
    """
    adj: list[dict[int, int]] = [dict() for _ in range(n)]
    for u, v, w in edges:
        adj[u][v] = w
        adj[v][u] = w
    nodes = [Node(i, adj[i]) for i in range(n)]
    rng = random.Random(seed)
    events: list[tuple[float, int, int, int, tuple]] = []  # time, seq, to, from, msg
    last: dict[tuple[int, int], float] = {}
    queues = [deque() for _ in range(n)]
    seq = 0
    stats = {"messages": 0, "by_type": {}, "time": 0.0, "max_bits": 0}

    def delay(u: int, v: int) -> float:
        if schedule == "unit":
            return 1.0
        if schedule == "slowlow":
            return 1.0 if min(u, v) < n // 3 else 0.01 + 0.09 * rng.random()
        return 1.0 - rng.random()  # in (0, 1]

    def flush(u: int, now: float) -> None:
        nonlocal seq
        for v, msg in nodes[u].out:
            t = max(now + delay(u, v), last.get((u, v), 0.0))
            last[(u, v)] = t
            seq += 1
            heapq.heappush(events, (t, seq, v, u, msg))
            stats["messages"] += 1
            stats["by_type"][msg[0]] = stats["by_type"].get(msg[0], 0) + 1
            stats["max_bits"] = max(stats["max_bits"], message_bits(msg, n))
        nodes[u].out.clear()

    def serve(v: int, now: float) -> None:
        q = queues[v]
        waiting = 0
        while q and waiting < len(q):
            j, msg = q.popleft()
            if nodes[v].handle(j, msg):
                waiting = 0
            else:
                q.append((j, msg))  # back to the end of the queue
                waiting += 1
            flush(v, now)  # a deferred message may still have woken the node

    for u in range(n) if wake is None else wake:
        if nodes[u].SN == SLEEPING:
            nodes[u].wakeup()
            flush(u, 0.0)
    while events:
        t, _, v, u, msg = heapq.heappop(events)
        stats["time"] = t
        queues[v].append((u, msg))
        serve(v, t)
    assert all(not q for q in queues), "a message waits forever"
    mst = set()
    for u in range(n):
        for j, state in nodes[u].SE.items():
            if state == BRANCH:
                mst.add(adj[u][j])
    stats["mst"] = mst
    stats["halted"] = [u for u in range(n) if nodes[u].halted]
    stats["levels"] = [nodes[u].LN for u in range(n)]
    return stats


def kruskal(n: int, edges: list[tuple[int, int, int]]) -> set[int]:
    """The weights of the MST edges, by Kruskal with union-find (the oracle)."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = set()
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            out.add(w)
    return out


def random_connected_graph(n: int, extra: int, rng: random.Random) -> list[tuple[int, int, int]]:
    """A random connected graph: a random tree plus extra edges, with distinct
    weights from 1 to n^3."""
    pairs = set()
    for v in range(1, n):
        pairs.add((rng.randrange(v), v))
    all_pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    rng.shuffle(all_pairs)
    for p in all_pairs:
        if len(pairs) >= n - 1 + extra:
            break
        pairs.add(p)
    weights = rng.sample(range(1, max(n**3, len(pairs)) + 1), len(pairs))
    return [(u, v, w) for (u, v), w in zip(sorted(pairs), weights)]
