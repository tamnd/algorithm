# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/awerbuch-leader-election/. The authors are listed in prov/ESZB9E.jsonl.

"""Election by fragment merging, the structure under Awerbuch's algorithm.

Fragments are subtrees of the minimum spanning tree, where the weight of the
link {u, v} is (min id, max id), so all weights are distinct. In each phase:
the root of every fragment broadcasts INITIATE with the fragment name; each
node tests its links that are not rejected, in increasing weight, with TEST,
and gets REJECT (same fragment, the link is rejected for good at both ends)
or ACCEPT (stop); REPORT carries the smallest accepted weight to the root;
the root sends CHANGE along the tree path to the end of the minimum outgoing
link, which sends CONNECT over it. Fragments joined by CONNECT links merge,
and the end with the larger id of the link chosen from both sides is the new
root. A root that finds no outgoing link is the leader and tells everyone.

The phases run one after another, as if they were kept in step; every
message of the protocol is counted. Awerbuch's changes that bring the time
down to O(n) are not part of this code.
"""

import random


def weight(ids: list[int], u: int, v: int) -> tuple[int, int]:
    a, b = ids[u], ids[v]
    return (min(a, b), max(a, b))


def awerbuch_structure(adj: list[list[int]], ids: list[int]) -> dict:
    n = len(adj)
    counts = {"HELLO": 0, "INITIATE": 0, "TEST": 0, "ACCEPT": 0, "REJECT": 0, "REPORT": 0,
              "CHANGE": 0, "CONNECT": 0, "LEADER": 0}
    # Every node starts as a fragment of its own, and learns the identifiers
    # of its neighbours, to know the weights of its links.  # @line L1
    counts["HELLO"] = sum(len(a) for a in adj)
    root = list(range(n))  # the root of the fragment of each node
    tree: list[set[int]] = [set() for _ in range(n)]  # fragment tree links
    rejected: list[set[int]] = [set() for _ in range(n)]
    order = [sorted(adj[v], key=lambda w: weight(ids, v, w)) for v in range(n)]
    phases = 0
    leader = None
    while True:
        phases += 1
        frags: dict[int, list[int]] = {}
        for v in range(n):
            frags.setdefault(root[v], []).append(v)
        # INITIATE down each fragment tree.  # @line L2
        for r, members in frags.items():
            counts["INITIATE"] += len(members) - 1
        # Each node finds its smallest outgoing link.  # @line L3
        local: list = [None] * n
        for v in range(n):
            for w in order[v]:
                if w in rejected[v] or w in tree[v]:
                    continue
                counts["TEST"] += 1
                if root[w] == root[v]:
                    counts["REJECT"] += 1
                    rejected[v].add(w)
                    rejected[w].add(v)
                else:
                    counts["ACCEPT"] += 1
                    local[v] = (weight(ids, v, w), v, w)
                    break
        # REPORT up each fragment tree; the root picks the minimum.  # @line L4
        moe: dict[int, tuple] = {}
        for r, members in frags.items():
            counts["REPORT"] += len(members) - 1
            cands = [local[v] for v in members if local[v] is not None]
            if cands:
                moe[r] = min(cands)
        if not moe:  # @line L5
            (leader,) = frags.keys()
            counts["LEADER"] += n - 1
            break
        # CHANGE along the path to the end of the link, then CONNECT.  # @line L6
        for r, (_, v, w) in moe.items():
            counts["CHANGE"] += path_length(tree, r, v)
            counts["CONNECT"] += 1
        # Merge along the chosen links.  # @line L7
        chosen = {}
        for r, (_, v, w) in moe.items():
            key = (min(v, w), max(v, w))
            chosen[key] = chosen.get(key, 0) + 1
        for (v, w) in chosen:
            tree[v].add(w)
            tree[w].add(v)
        cores = [e for e, c in chosen.items() if c == 2]
        seen = [False] * n
        for v, w in cores:
            new_root = v if ids[v] > ids[w] else w
            stack = [new_root]
            seen[new_root] = True
            while stack:
                x = stack.pop()
                root[x] = new_root
                for y in tree[x]:
                    if not seen[y]:
                        seen[y] = True
                        stack.append(y)
        assert all(seen)
    edges = sorted({(min(v, w), max(v, w)) for v in range(n) for w in tree[v]})
    return {
        "leader": leader,
        "roots": root,
        "tree": edges,
        "phases": phases,
        "counts": counts,
        "messages": sum(counts.values()),
    }


def path_length(tree: list[set[int]], s: int, t: int) -> int:
    if s == t:
        return 0
    dist = {s: 0}
    stack = [s]
    while stack:
        x = stack.pop()
        for y in tree[x]:
            if y not in dist:
                dist[y] = dist[x] + 1
                if y == t:
                    return dist[y]
                stack.append(y)
    raise ValueError("not in the same fragment")


def random_connected_graph(n: int, extra: int, rng: random.Random) -> list[list[int]]:
    adj: list[set[int]] = [set() for _ in range(n)]
    for v in range(1, n):
        u = rng.randrange(v)
        adj[u].add(v)
        adj[v].add(u)
    for _ in range(extra):
        u, v = rng.sample(range(n), 2) if n > 1 else (0, 0)
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    return [sorted(s) for s in adj]


def kruskal(adj: list[list[int]], ids: list[int]) -> list[tuple[int, int]]:
    n = len(adj)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edges = sorted({(min(v, w), max(v, w)) for v in range(n) for w in adj[v]},
                   key=lambda e: weight(ids, *e))
    out = []
    for v, w in edges:
        a, b = find(v), find(w)
        if a != b:
            parent[a] = b
            out.append((v, w))
    return sorted(out)
