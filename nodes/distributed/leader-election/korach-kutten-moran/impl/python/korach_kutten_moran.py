# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/korach-kutten-moran/. The authors are listed in prov/KB0GBC.jsonl.

"""Election by competing traversals on an asynchronous complete network.

Each candidate traverses the network one node at a time with the star
traversal: it asks the nodes, one link after the other, to join its domain.
A candidate has a pair (level, id), where level is the number of nodes it
has captured. When two traversals meet, the larger pair wins and the other
candidate dies. Messages: CAP (capture request), Q (query to the owner of
the node), YES / NO (answer of the owner), ACC / REJ (answer to the
candidate). The scheduler delivers any message in transit, chosen by a
seeded generator, so channels are not FIFO; with sync true, every message
takes exactly one time unit.
"""

import random


class Node:
    def __init__(self, v: int, ident: int, ports: list[int]) -> None:
        self.v = v
        self.id = ident
        self.ports = ports  # the order of the star traversal
        self.lev = -1  # -1 while the node has never been a candidate
        self.alive = False
        self.owner = v
        self.busy = None  # the capture this node is checking with its owner
        self.queue: list[tuple] = []
        self.idx = 0
        self.leader = False
        self.got_message = False

    def pair(self) -> tuple[int, int]:
        return (self.lev, self.id)


def kkm_complete(n: int, ids: list[int], initiators: list[int], seed: int = 0,
                 sync: bool = False) -> dict:
    """Run one election. Returns the leaders, the message counts, the levels and the time."""
    rng = random.Random(seed)
    nodes = []
    for v in range(n):
        ports = [w for w in range(n) if w != v]
        rng.shuffle(ports)
        nodes.append(Node(v, ids[v], ports))
    transit: list[tuple] = []  # (src, dst, msg)
    counts = {"CAP": 0, "Q": 0, "YES": 0, "NO": 0, "ACC": 0, "REJ": 0}
    candidates: list[int] = []

    def send(src: int, dst: int, msg: tuple) -> None:
        transit.append((src, dst, msg))
        counts[msg[0]] += 1

    def next_capture(c: int) -> None:
        nd = nodes[c]
        if nd.lev == n - 1:
            nd.leader = True
            return
        x = nd.ports[nd.idx]
        nd.idx += 1
        send(c, x, ("CAP", nd.pair()))

    def start(c: int) -> None:  # @line L1
        nd = nodes[c]
        if nd.got_message:
            return
        nd.alive, nd.lev = True, 0
        candidates.append(c)
        next_capture(c)

    def serve(x: int, c: int, p: tuple) -> None:
        nd = nodes[x]
        if nd.owner == x:  # @line L2
            if p > nd.pair():
                nd.alive = False
                nd.owner = c
                send(x, c, ("ACC",))
            else:
                send(x, c, ("REJ",))
        else:  # @line L3
            nd.busy = (c, p)
            send(x, nd.owner, ("Q", p))

    def receive(src: int, dst: int, msg: tuple) -> None:
        nd = nodes[dst]
        nd.got_message = True
        kind = msg[0]
        if kind == "CAP":
            if nd.busy is not None:
                nd.queue.append((src, msg[1]))
            else:
                serve(dst, src, msg[1])
        elif kind == "Q":  # @line L4
            if msg[1] > nd.pair():
                nd.alive = False
                send(dst, src, ("YES",))
            else:
                send(dst, src, ("NO",))
        elif kind in ("YES", "NO"):  # @line L5
            c, _ = nd.busy
            nd.busy = None
            if kind == "YES":
                nd.owner = c
                send(dst, c, ("ACC",))
            else:
                send(dst, c, ("REJ",))
            while nd.queue and nd.busy is None:
                c2, p2 = nd.queue.pop(0)
                serve(dst, c2, p2)
        elif kind == "ACC":  # @line L6
            if nd.alive:
                nd.lev += 1
                next_capture(dst)
        elif kind == "REJ":  # @line L7
            nd.alive = False

    time = 0
    if n == 1:
        nodes[0].leader = True
        candidates.append(0)
        nodes[0].lev = 0
    elif sync:
        for c in initiators:
            start(c)
        while transit:
            time += 1
            batch, transit[:] = list(transit), []
            rng.shuffle(batch)
            for src, dst, msg in batch:
                receive(src, dst, msg)
    else:
        pending = list(initiators)
        while transit or pending:
            k = rng.randrange(len(transit) + len(pending))
            if k < len(pending):
                start(pending.pop(k))
                continue
            src, dst, msg = transit.pop(k - len(pending))
            receive(src, dst, msg)
    return {
        "leaders": [v for v in range(n) if nodes[v].leader],
        "counts": counts,
        "messages": sum(counts.values()),
        "levels": {c: nodes[c].lev for c in candidates},
        "time": time,
    }


def harmonic(n: int) -> float:
    return sum(1.0 / j for j in range(1, n + 1))
