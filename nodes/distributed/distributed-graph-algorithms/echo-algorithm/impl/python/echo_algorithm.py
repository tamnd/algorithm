# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/echo-algorithm/. The authors are listed in prov/F5917B.jsonl.

"""The echo algorithm (Chang 1982; Segall's PIF) in a synchronous and an asynchronous network.

The network is a connected undirected graph given by adjacency lists. The
initiator sends a token to all neighbours. A node that gets its first token
takes the sender as parent and sends the token to all other neighbours. When
a node has received a token on every incident edge, it sends a token to its
parent (the echo), and the initiator decides. Exactly one token crosses each
edge in each direction, so the run sends exactly 2m messages.

The simulators record, at the moment the initiator decides, whether every
node has received a token on every edge and no token is in transit.
Cost of the simulation: O(n + m log m) time.
"""

import heapq
import random


class EchoNode:
    """The local state of one node."""

    def __init__(self, v: int, nbrs: list[int], initiator: bool) -> None:
        self.v = v
        self.nbrs = nbrs
        self.initiator = initiator
        self.reached = False
        self.rec = 0
        self.parent: int | None = None
        self.decided = False

    def start(self) -> list[int]:  # @line L1
        self.reached = True  # @line L2
        out = list(self.nbrs)  # @line L3
        if not self.nbrs:
            self.decided = True
        return out

    def receive(self, u: int) -> list[int]:  # @line L4
        out: list[int] = []
        self.rec += 1  # @line L5
        if not self.reached:  # @line L6
            self.reached = True  # @line L7
            self.parent = u
            out = [w for w in self.nbrs if w != u]  # @line L8
        if self.rec == len(self.nbrs):  # @line L9
            if self.initiator:
                self.decided = True  # @line L10
            else:
                out.append(self.parent)  # @line L11
        return out


def _all_done(nodes: list[EchoNode]) -> bool:
    return all(x.rec == len(x.nbrs) for x in nodes if not (x.initiator and not x.nbrs))


def echo_sync(adj: list[list[int]], init: int) -> dict:
    """Lock-step rounds. Tokens that arrive in one round are handled in port order."""
    n = len(adj)
    nodes = [EchoNode(v, adj[v], v == init) for v in range(n)]
    outbox = {init: nodes[init].start()}
    messages = 0
    rnd = 0
    decide_round = 0 if nodes[init].decided else None
    clean = True
    while outbox:
        rnd += 1
        inbox: dict[int, list[int]] = {}
        for v in sorted(outbox):
            for w in outbox[v]:
                inbox.setdefault(w, []).append(v)
                messages += 1
        outbox = {}
        for w in sorted(inbox):
            out: list[int] = []
            for u in sorted(inbox[w], key=adj[w].index):
                out += nodes[w].receive(u)
            if out:
                outbox[w] = out
        if decide_round is None and nodes[init].decided:
            decide_round = rnd
            clean = _all_done(nodes) and not outbox
    return {
        "parent": [x.parent for x in nodes],
        "messages": messages,
        "decide_round": decide_round,
        "clean": clean,
    }


def echo_async(adj: list[list[int]], init: int, seed: int = 0, schedule: str = "random") -> dict:
    """Seeded asynchronous run. Each delay is in (0, 1]. The "chain" schedule
    makes every message of the initiator slow except its first one, so first
    tokens arrive along long paths and the tree is deep."""
    n = len(adj)
    rng = random.Random(seed)
    nodes = [EchoNode(v, adj[v], v == init) for v in range(n)]
    queue: list[tuple[float, int, int, int]] = []
    seq = 0
    messages = 0
    now = 0.0

    def send(src: int, dst: int) -> None:
        nonlocal seq, messages
        seq += 1
        messages += 1
        if schedule == "chain":
            d = 1.0 if src == init and seq > 1 else rng.uniform(0.0001, 0.001)
        else:
            d = rng.uniform(0.01, 1.0)
        heapq.heappush(queue, (now + d, seq, src, dst))

    for w in nodes[init].start():
        send(init, w)
    decide_time = 0.0 if nodes[init].decided else None
    clean = True
    while queue:
        now, _, src, dst = heapq.heappop(queue)
        for w in nodes[dst].receive(src):
            send(dst, w)
        if decide_time is None and nodes[init].decided:
            decide_time = now
            clean = _all_done(nodes) and not queue
    return {
        "parent": [x.parent for x in nodes],
        "messages": messages,
        "decide_time": decide_time,
        "clean": clean,
    }
