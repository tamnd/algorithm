# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-apsp/. The authors are listed in prov/5J9KE7.jsonl.

"""Unweighted all-pairs shortest paths in CONGEST by pipelined BFS.

This is the scheme of Holzer and Wattenhofer (PODC 2012). Phase 1 builds a
BFS tree T from the root 0, with an echo so that the root knows when T is
complete. In phase 2 a token walks T in depth-first order. When the token
first reaches a node v, v starts a BFS wave, and the token waits one round
before it moves on. Then the start rounds of any two waves differ by more
than the distance of their sources, so no node ever gets two new waves in
one round, and each link carries at most one wave message in each round.

The simulator is synchronous and deterministic. It records the load of each
directed link in each round, so that the tests can check the no-collision
lemma.
"""

from collections import deque


def adjacency(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return [sorted(a) for a in adj]


def bfs_tree_phase(adj: list[list[int]], root: int = 0) -> tuple[int, list[list[int]], int]:
    """Phase 1: flood join messages from the root and echo done messages.

    Return the round in which the root learns that the tree is complete,
    the children of each node (sorted by identifier) and the messages."""
    n = len(adj)
    if n == 1:
        return 0, [[]], 0
    parent: list[int | None] = [None] * n
    joined = [False] * n
    heard = [0] * n  # replies from the neighbours other than the parent
    children: list[list[int]] = [[] for _ in range(n)]
    done_children = [0] * n
    sent_done = [False] * n
    joined[root] = True
    outbox: list[tuple[int, int, str]] = [(root, v, "join") for v in adj[root]]
    messages, r = 0, 0
    while True:
        r += 1
        messages += len(outbox)
        inbox: list[list[tuple[int, str]]] = [[] for _ in range(n)]
        for u, v, kind in outbox:
            inbox[v].append((u, kind))
        outbox = []
        for v in range(n):
            joins = sorted(u for u, k in inbox[v] if k == "join")
            if not joined[v] and joins:
                joined[v] = True
                parent[v] = joins[0]
                outbox.append((v, joins[0], "child"))
                outbox += [(v, x, "join") for x in adj[v] if x != joins[0]]
                heard[v] += len(joins) - 1
                continue
            for u, k in inbox[v]:
                if k in ("join", "child"):
                    heard[v] += 1
                if k == "child":
                    children[v].append(u)
                elif k == "done":
                    done_children[v] += 1
        for v in range(n):
            others = len(adj[v]) - (0 if parent[v] is None else 1)
            if joined[v] and not sent_done[v] and heard[v] == others and done_children[v] == len(children[v]):
                sent_done[v] = True
                if v == root:
                    return r, [sorted(c) for c in children], messages
                outbox.append((v, parent[v], "done"))


def pipelined_apsp(n: int, edges: list[tuple[int, int]], root: int = 0) -> dict:
    """Return dist[w][u] = d(u, w) as learned by node w, the rounds of both
    phases, the start round of each wave, the largest number of wave
    messages on one directed link in one round, the largest number of new
    waves that reach one node in one round, and the number of messages."""
    adj = adjacency(n, edges)
    r0, children, messages = bfs_tree_phase(adj, root)
    tparent: list[int | None] = [None] * n
    for v in range(n):
        for c in children[v]:
            tparent[c] = v
    dist: list[dict[int, int]] = [dict() for _ in range(n)]
    start = [-1] * n
    nxt = [0] * n  # index of the next child that the token visits
    token: int | None = root  # at the root at the end of round r0
    token_new = True
    fresh: list[tuple[int, int, int]] = []  # (node, source, its distance) to forward now
    max_link, max_new, r, last = 0, 0, r0, r0
    while token is not None or fresh:
        r += 1
        if token is not None:
            v = token
            if token_new:  # first visit: start the wave, keep the token
                start[v] = r
                dist[v][v] = 0
                fresh.append((v, v, 0))
                token_new = False
            elif nxt[v] < len(children[v]):
                token = children[v][nxt[v]]
                nxt[v] += 1
                token_new = True
                messages += 1
            else:
                token = tparent[v]
                messages += 0 if token is None else 1
        load: dict[tuple[int, int], int] = {}
        arrivals: list[tuple[int, int, int]] = []
        for w, src, d in fresh:
            for x in adj[w]:
                load[(w, x)] = load.get((w, x), 0) + 1
                arrivals.append((x, src, d + 1))
        messages += len(arrivals)
        fresh = []
        new_at: dict[int, set[int]] = {}
        for x, src, d in arrivals:
            if src not in dist[x]:
                dist[x][src] = d
                new_at.setdefault(x, set()).add(src)
                fresh.append((x, src, d))
        if load:
            max_link = max(max_link, max(load.values()))
        if new_at:
            max_new = max(max_new, max(len(s) for s in new_at.values()))
            last = r
    return {
        "dist": dist,
        "setup_rounds": r0,
        "rounds": last,
        "start": start,
        "max_link_load": max_link,
        "max_new_per_node": max_new,
        "messages": messages,
    }


def bfs_all(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """The oracle: one sequential BFS from each node."""
    adj = adjacency(n, edges)
    out = []
    for s in range(n):
        d = [-1] * n
        d[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if d[v] < 0:
                    d[v] = d[u] + 1
                    q.append(v)
        out.append(d)
    return out


def leaf_lower_bound_graph(bits: list[int]) -> tuple[int, list[tuple[int, int]]]:
    """The graph of the counting bound. Node 0 is a leaf on the hub 1, node 2
    is joined to the hub, and node 3 + i is joined to the hub if bits[i] is 1
    and to node 2 otherwise. Then d(0, 3 + i) = 3 - bits[i]."""
    edges = [(0, 1), (1, 2)]
    for i, b in enumerate(bits):
        edges.append((1 if b else 2, 3 + i))
    return 3 + len(bits), edges
