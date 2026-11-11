# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-diameter/. The authors are listed in prov/5JD8RM.jsonl.

"""The diameter of an unweighted network in CONGEST.

exact_diameter runs the pipelined BFS of Holzer and Wattenhofer (one BFS
wave from each node, started in DFS order of a BFS tree), so that each node
learns its eccentricity, and then a convergecast and a broadcast on the tree
give the largest eccentricity to all nodes. The simulator is synchronous and
deterministic.

two_approx is one BFS: the eccentricity e of the root has e <= D <= 2e.

three_halves_estimate is the estimator of Roditty and Vassilevska Williams
that Holzer, Peleg, Roditty and Wattenhofer run in O((n log n)^(1/2) + D)
rounds. Here it is computed with sequential BFS, to check its guarantee
floor(2D/3) <= estimate <= D.
"""

import math
import random
from collections import deque


def adjacency(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return [sorted(a) for a in adj]


def bfs(adj: list[list[int]], s: int) -> list[int]:
    d = [-1] * len(adj)
    d[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1
                q.append(v)
    return d


def bfs_tree_phase(adj: list[list[int]], root: int = 0) -> tuple[int, list[int | None], list[list[int]]]:
    """Flood join messages from the root and echo done messages. Return the
    round in which the root knows that the tree is complete, the parents and
    the children."""
    n = len(adj)
    parent: list[int | None] = [None] * n
    if n == 1:
        return 0, parent, [[]]
    joined, sent_done = [False] * n, [False] * n
    heard, done_children = [0] * n, [0] * n
    children: list[list[int]] = [[] for _ in range(n)]
    joined[root] = True
    outbox: list[tuple[int, int, str]] = [(root, v, "join") for v in adj[root]]
    r = 0
    while True:
        r += 1
        inbox: list[list[tuple[int, str]]] = [[] for _ in range(n)]
        for u, v, kind in outbox:
            inbox[v].append((u, kind))
        outbox = []
        for v in range(n):
            joins = sorted(u for u, k in inbox[v] if k == "join")
            if not joined[v] and joins:
                joined[v], parent[v] = True, joins[0]
                outbox.append((v, joins[0], "child"))
                outbox += [(v, x, "join") for x in adj[v] if x != joins[0]]
                heard[v] += len(joins) - 1
                continue
            for u, k in inbox[v]:
                heard[v] += k in ("join", "child")
                if k == "child":
                    children[v].append(u)
                done_children[v] += k == "done"
        for v in range(n):
            others = len(adj[v]) - (parent[v] is not None)
            if joined[v] and not sent_done[v] and heard[v] == others and done_children[v] == len(children[v]):
                sent_done[v] = True
                if v == root:
                    return r, parent, [sorted(c) for c in children]
                outbox.append((v, parent[v], "done"))


def pipelined_waves(adj: list[list[int]], children: list[list[int]], parent: list[int | None], root: int) -> tuple[list[dict[int, int]], int, int]:
    """One BFS wave from each node, started when a DFS token first visits it.
    Return the distances that each node learns, the rounds, and the largest
    number of wave messages on one directed link in one round."""
    n = len(adj)
    dist: list[dict[int, int]] = [dict() for _ in range(n)]
    nxt = [0] * n
    token: int | None = root
    token_new = True
    fresh: list[tuple[int, int, int]] = []
    r = last = max_link = 0
    while token is not None or fresh:
        r += 1
        if token is not None:
            v = token
            if token_new:
                dist[v][v] = 0
                fresh.append((v, v, 0))
                token_new = False
            elif nxt[v] < len(children[v]):
                token, token_new = children[v][nxt[v]], True
                nxt[v] += 1
            else:
                token = parent[v]
        load: dict[tuple[int, int], int] = {}
        arrivals = []
        for w, src, d in fresh:
            for x in adj[w]:
                load[(w, x)] = load.get((w, x), 0) + 1
                arrivals.append((x, src, d + 1))
        fresh = []
        for x, src, d in arrivals:
            if src not in dist[x]:
                dist[x][src] = d
                fresh.append((x, src, d))
                last = r
        if load:
            max_link = max(max_link, max(load.values()))
    return dist, last, max_link


def exact_diameter(n: int, edges: list[tuple[int, int]], root: int = 0) -> dict:
    """Return the diameter that every node learns, the eccentricities, and
    the rounds of the three phases: the tree, the waves, and the
    convergecast with the broadcast."""
    adj = adjacency(n, edges)
    r_tree, parent, children = bfs_tree_phase(adj, root)
    dist, r_waves, max_link = pipelined_waves(adj, children, parent, root)
    ecc = [max(d.values()) for d in dist]
    # convergecast of the largest eccentricity, then a broadcast of it
    best = list(ecc)
    waiting = [len(c) for c in children]
    sent = [False] * n
    r_cast = 0
    while not sent[root]:
        r_cast += 1
        ready = [v for v in range(n) if not sent[v] and waiting[v] == 0]
        for v in ready:
            sent[v] = True
            p = parent[v]
            if p is not None:
                best[p] = max(best[p], best[v])
                waiting[p] -= 1
    depth = max(bfs(adj, root))
    known = [best[root]] * n  # the broadcast takes depth rounds
    return {
        "diameter": known,
        "ecc": ecc,
        "rounds": r_tree + r_waves + r_cast + depth,
        "phase_rounds": (r_tree, r_waves, r_cast, depth),
        "max_link_load": max_link,
    }


def two_approx(n: int, edges: list[tuple[int, int]], root: int = 0) -> int:
    """The eccentricity of the root, from one BFS: e <= D <= 2e."""
    return max(bfs(adjacency(n, edges), root))


def three_halves_estimate(n: int, edges: list[tuple[int, int]], rng: random.Random) -> tuple[int, bool]:
    """The estimator of Roditty and Vassilevska Williams.

    1. Sample S, each node with probability p, and run BFS from each node of S.
    2. Let w be a node farthest from S, and run BFS from w.
    3. Let N be the s nodes closest to w, and run BFS from each node of N.
    Return the largest eccentricity seen, and whether S meets N, which is the
    event under which the guarantee floor(2D/3) <= estimate holds."""
    adj = adjacency(n, edges)
    s = min(n, math.ceil(math.sqrt(n * math.log(n + 1))))
    p = min(1.0, 3 * math.log(n + 1) / s)
    S = [v for v in range(n) if rng.random() < p] or [0]
    est = 0
    to_s = [n] * n
    for x in S:
        d = bfs(adj, x)
        est = max(est, max(d))
        to_s = [min(a, b) for a, b in zip(to_s, d)]
    w = max(range(n), key=lambda v: (to_s[v], -v))
    dw = bfs(adj, w)
    est = max(est, max(dw))
    near = sorted(range(n), key=lambda v: (dw[v], v))[:s]
    for x in near:
        est = max(est, max(bfs(adj, x)))
    return est, bool(set(S) & set(near))


def brute_diameter(n: int, edges: list[tuple[int, int]]) -> int:
    adj = adjacency(n, edges)
    return max(max(bfs(adj, s)) for s in range(n))
