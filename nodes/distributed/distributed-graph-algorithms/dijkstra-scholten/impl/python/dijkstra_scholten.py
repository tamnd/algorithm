# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dijkstra-scholten/. The authors are listed in prov/PQWDHA.jsonl.

"""The Dijkstra-Scholten algorithm for termination detection of a diffusing computation.

A diffusing computation starts at one root r, which is active; all other
nodes are passive. Only an active node sends basic messages, and a passive
node becomes active only on receipt of a basic message. Each node keeps a
deficit (basic messages sent and not yet signalled) and, while engaged, a
parent: the sender of the basic message that engaged it. Every basic message
is answered by exactly one SIGNAL, at once if the receiver is engaged, or
when the receiver leaves the tree otherwise. The root announces termination
when it is passive and its deficit is zero.

simulate() runs a seeded random basic computation on a connected graph and
checks the global state at the moment of the announcement.
Cost of the simulation: O((B + n) log B) time for B basic messages.
"""

import heapq
import random


class DSNode:
    def __init__(self, v: int, root: int) -> None:  # @line L1
        self.v = v
        self.is_root = v == root
        self.deficit = 0
        self.engaged = self.is_root
        self.active = self.is_root
        self.parent: int | None = v if self.is_root else None
        self.announced = False

    def on_send_basic(self) -> None:  # @line L2
        assert self.active
        self.deficit += 1

    def on_basic(self, u: int) -> list[int]:  # @line L3
        """Returns the list of nodes to which a SIGNAL is sent now."""
        self.active = True  # @line L4
        if not self.engaged:  # @line L5
            self.engaged = True
            self.parent = u
            return []
        return [u]  # @line L6

    def on_signal(self) -> list[int]:  # @line L7
        self.deficit -= 1
        return self.try_leave()

    def on_passive(self) -> list[int]:  # @line L8
        self.active = False
        return self.try_leave()

    def try_leave(self) -> list[int]:  # @line L9
        if self.active or self.deficit != 0 or not self.engaged:
            return []
        if self.is_root:
            self.announced = True  # @line L10
            return []
        p = self.parent  # @line L11
        self.engaged = False
        self.parent = None
        return [p]


def simulate(adj: list[list[int]], root: int, budget: int, seed: int = 0, fanout: int = 2) -> dict:
    """Seeded diffusing computation plus Dijkstra-Scholten on top of it.

    A node holds a number of pending work items. A work item, when it runs,
    sends 0 to `fanout` basic messages to random neighbours (while the global
    budget lasts). Each received basic message adds one work item. A node is
    active exactly while it has pending work. All delays are in (0, 1].
    """
    rng = random.Random(seed)
    n = len(adj)
    nodes = [DSNode(v, root) for v in range(n)]
    work = [0] * n
    work[root] = 1
    queue: list[tuple[float, int, str, int, int]] = []
    seq = 0
    now = 0.0
    stats = {"basic": 0, "signal": 0, "basic_in_transit": 0}
    state = {"budget": budget, "terminated_at": None, "announced_at": None, "clean": None}

    def push(t: float, kind: str, src: int, dst: int) -> None:
        nonlocal seq
        seq += 1
        heapq.heappush(queue, (t, seq, kind, src, dst))

    def send_signals(src: int, targets: list[int]) -> None:
        for w in targets:
            stats["signal"] += 1
            push(now + rng.uniform(0.01, 1.0), "SIGNAL", src, w)

    def terminated() -> bool:
        return stats["basic_in_transit"] == 0 and not any(x.active for x in nodes)

    def note() -> None:
        if state["terminated_at"] is None and terminated():
            state["terminated_at"] = now
        if nodes[root].announced and state["announced_at"] is None:
            state["announced_at"] = now
            state["clean"] = terminated()

    push(rng.uniform(0.0, 0.5), "WORK", root, root)
    while queue:
        now, _, kind, src, dst = heapq.heappop(queue)
        if kind == "WORK":
            x = nodes[dst]
            k = rng.randint(0, fanout) if state["budget"] > 0 else 0
            k = min(k, state["budget"])
            state["budget"] -= k
            for _ in range(k):
                w = rng.choice(adj[dst])
                x.on_send_basic()
                stats["basic"] += 1
                stats["basic_in_transit"] += 1
                push(now + rng.uniform(0.01, 1.0), "BASIC", dst, w)
            work[dst] -= 1
            if work[dst] == 0:
                send_signals(dst, x.on_passive())
        elif kind == "BASIC":
            stats["basic_in_transit"] -= 1
            work[dst] += 1
            send_signals(dst, nodes[dst].on_basic(src))
            push(now + rng.uniform(0.01, 1.0), "WORK", dst, dst)
        else:
            send_signals(dst, nodes[dst].on_signal())
        note()
    return {
        "basic": stats["basic"],
        "signal": stats["signal"],
        "terminated_at": state["terminated_at"],
        "announced_at": state["announced_at"],
        "clean": state["clean"],
        "deficits": [x.deficit for x in nodes],
        "engaged": [x.engaged for x in nodes],
    }
