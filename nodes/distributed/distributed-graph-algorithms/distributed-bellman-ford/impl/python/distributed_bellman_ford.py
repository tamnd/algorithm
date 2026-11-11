# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-bellman-ford/. The authors are listed in prov/FVKNH6.jsonl.

"""Distributed Bellman-Ford: synchronous, asynchronous, and count to infinity.

The network is an undirected graph with non-negative integer weights. The
synchronous version runs in lock-step rounds of the CONGEST model and stops
after exactly n - 1 rounds. The asynchronous version sends a node's estimate
to all neighbours each time it improves; a discrete event simulator with
FIFO channels and a fixed delay per edge delivers the messages.
"""

import heapq
import math

INF = math.inf


def message_bits(d: float) -> int:
    """Bits to encode one distance estimate: 2 bits for infinity, else 2 plus
    the binary length."""
    return 2 if d == INF else 2 + max(1, int(d).bit_length())


def sync_bellman_ford(
    n: int, edges: list[tuple[int, int, int]], s: int, rounds: int | None = None
) -> dict:
    """Run the synchronous algorithm from source s for n - 1 rounds (or the
    given number). Return dist, parent, the messages and the largest message
    in bits, and the estimates after each round."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = [INF] * n  # @line L1
    parent: list[int | None] = [None] * n
    dist[s] = 0
    messages, max_bits, history = 0, 0, [list(dist)]
    for _ in range(n - 1 if rounds is None else rounds):  # @line L2
        inbox: list[list[tuple[int, float]]] = [[] for _ in range(n)]
        for u in range(n):  # @line L3
            for v, _w in adj[u]:
                inbox[v].append((u, dist[u]))
                messages += 1
                max_bits = max(max_bits, message_bits(dist[u]))
        for v in range(n):  # every node computes on the messages of this round
            for u, d in inbox[v]:  # @line L4
                w = min(wt for x, wt in adj[v] if x == u)
                if d + w < dist[v]:  # @line L5
                    dist[v], parent[v] = d + w, u  # @line L6
        history.append(list(dist))
    return {"dist": dist, "parent": parent, "messages": messages, "max_bits": max_bits, "history": history}  # @line L7


def async_bellman_ford(
    n: int, edges: list[tuple[int, int, int]], s: int, delay: dict[tuple[int, int], float]
) -> dict:
    """Run the asynchronous algorithm. delay[(u, v)] is the fixed delay of
    the channel from u to v (default 1). Return dist, the number of messages,
    and the list of estimates that each node held, in order."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = [INF] * n
    dist[s] = 0
    seen: list[list[float]] = [[d] for d in dist]
    events: list[tuple[float, int, int, int, float]] = []
    last: dict[tuple[int, int], float] = {}
    seq = 0
    messages = 0

    def broadcast(u: int, now: float) -> None:
        nonlocal seq, messages
        for v, _w in adj[u]:
            t = max(now + delay.get((u, v), 1.0), last.get((u, v), 0.0))  # FIFO
            last[(u, v)] = t
            seq += 1
            messages += 1
            heapq.heappush(events, (t, seq, v, u, dist[u]))

    broadcast(s, 0.0)
    while events:
        t, _, v, u, d = heapq.heappop(events)
        w = min(wt for x, wt in adj[v] if x == u)
        if d + w < dist[v]:
            dist[v] = d + w
            seen[v].append(dist[v])
            broadcast(v, t)
    return {"dist": dist, "messages": messages, "seen": seen}


def blowup_instance(k: int) -> tuple[int, list[tuple[int, int, int]], dict[tuple[int, int], float]]:
    """The chain v0, ..., vk. Between v(j-1) and vj there is a direct edge of
    weight 2^(k-j) with delay 1, and a slow path v(j-1), uj, vj with weights
    0 and 0. The slow path of stage j has delay 3^(k-j+1) on each edge, so it
    is slower the closer it is to the source v0. Nodes 0..k are v0..vk and
    nodes k+1..2k are u1..uk."""
    edges, delay = [], {}
    for j in range(1, k + 1):
        a, b, u = j - 1, j, k + j
        edges.append((a, b, 2 ** (k - j)))
        edges += [(a, u, 0), (u, b, 0)]
        slow = 3.0 ** (k - j + 1)
        for x, y in ((a, u), (u, b)):
            delay[(x, y)] = delay[(y, x)] = slow
    return 2 * k + 1, edges, delay


def count_to_infinity(cap: int) -> list[tuple[int, int]]:
    """The chain s - A - B with unit weights, after the link s - A fails.

    A and B start with the correct estimates 1 and 2. In each synchronous
    round each node sets its estimate to 1 plus the smallest estimate of its
    remaining neighbours (the distance-vector rule), capped at cap, which plays
    the role of infinity. Return the pairs (dA, dB) after each round until both
    reach cap."""
    a, b = 1, 2
    out = [(a, b)]
    while (a, b) != (cap, cap):
        a, b = min(b + 1, cap), min(a + 1, cap)
        out.append((a, b))
    return out


def dijkstra(n: int, edges: list[tuple[int, int, int]], s: int) -> list[float]:
    """The oracle: Dijkstra with a binary heap."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = [INF] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist
