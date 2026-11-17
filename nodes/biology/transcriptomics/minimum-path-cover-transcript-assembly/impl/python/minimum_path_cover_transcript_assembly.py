# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-path-cover-transcript-assembly/. The authors are listed in prov/9NY424.jsonl.

"""The fewest transcripts that explain a set of fragments, by Dilworth's theorem.

The graph is a DAG on the nodes 0 to n - 1, numbered so that every edge
(u, v) has u < v; the nodes of a splice graph in coordinate order have this
property. A fragment is a path of the graph, given as its list of nodes: the
node path of a read or of a read pair whose gap is known. The task is to find
the fewest paths of the graph such that every fragment is a contiguous part of
at least one of them.

This is the parsimony step of Cufflinks in its simplest form. Cufflinks also
works on fragments that disagree (they cannot be on one transcript), weights
the matching by how close the abundances of two fragments are, and estimates
abundances afterwards. None of this is here.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Sequence, Set, Tuple

Path = Tuple[int, ...]


def _is_subpath(x: Path, y: Path) -> bool:
    """True if x is a contiguous part of y. A path visits each node once, so one lookup is enough."""
    if x[0] not in y:
        return False
    i = y.index(x[0])
    return y[i:i + len(x)] == x


def reach(n: int, edges: Sequence[Tuple[int, int]]) -> List[int]:
    """reach[u] is a bit set of the nodes v != u that can be reached from u."""
    succ: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        if not u < v:
            raise ValueError("edges must go from a smaller to a larger node id")
        succ[u].append(v)
    r = [0] * n
    for u in range(n - 1, -1, -1):
        for v in succ[u]:
            r[u] |= (1 << v) | r[v]
    return r


def precedes(x: Path, y: Path, r: Sequence[int]) -> bool:
    """x <= y: some path of the graph holds x and then y, and x starts first.

    The fragments must not be contiguous parts of each other.
    """
    if not x[0] < y[0]:  # @line L2
        return False
    if y[0] in x:  # @line L3
        i = x.index(y[0])
        return x[i:] == y[:len(x) - i]
    return x[-1] < y[0] and bool(r[x[-1]] >> y[0] & 1)  # @line L4


def _connect(succ: Sequence[Sequence[int]], s: int, t: int) -> List[int]:
    """A path from s to t by breadth-first search, without s and with t."""
    parent: Dict[int, int] = {s: -1}
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            break
        for v in succ[u]:
            if v not in parent:
                parent[v] = u
                q.append(v)
    out = []
    v = t
    while v != s:
        out.append(v)
        v = parent[v]
    return out[::-1]


def _max_matching(adj: Sequence[Sequence[int]], n: int) -> List[int]:
    """Kuhn's augmenting path algorithm. Returns match_right[y] = x, or -1."""
    match_left, match_right = [-1] * n, [-1] * n
    for root in range(n):
        seen: Set[int] = set()
        # Iterative depth-first search for an augmenting path from root.
        stack = [(root, iter(adj[root]))]
        trail: List[Tuple[int, int]] = []
        found = False
        while stack and not found:
            x, it = stack[-1]
            for y in it:
                if y in seen:
                    continue
                seen.add(y)
                if match_right[y] == -1:
                    trail.append((x, y))
                    found = True
                    break
                trail.append((x, y))
                stack.append((match_right[y], iter(adj[match_right[y]])))
                break
            else:
                stack.pop()
                if trail:
                    trail.pop()
        if found:
            for x, y in trail:
                match_left[x], match_right[y] = y, x
    return match_right


def min_path_cover(n: int, edges: Sequence[Tuple[int, int]],
                   fragments: Sequence[Sequence[int]]) -> List[List[int]]:
    """The fewest paths of the DAG that hold every fragment as a contiguous part."""
    r = reach(n, edges)
    succ: List[List[int]] = [[] for _ in range(n)]
    for u, v in sorted(set(edges)):
        succ[u].append(v)
    for f in fragments:
        if not f or any(not (v in succ[u]) for u, v in zip(f, f[1:])):
            raise ValueError("each fragment must be a nonempty path of the graph")
    distinct = sorted(set(tuple(f) for f in fragments))
    frags = [x for x in distinct  # @line L1
             if not any(x != y and _is_subpath(x, y) for y in distinct)]
    k = len(frags)
    adj = [[j for j in range(k) if precedes(frags[i], frags[j], r)]  # @line L5
           for i in range(k)]
    match_right = _max_matching(adj, k)  # @line L6
    nxt = [-1] * k
    for y, x in enumerate(match_right):
        if x != -1:
            nxt[x] = y
    paths = []
    for start in range(k):  # @line L7
        if match_right[start] != -1:
            continue
        path = list(frags[start])
        j = nxt[start]
        while j != -1:  # @line L8
            y = frags[j]
            if y[0] in path:
                i = path.index(y[0])
                path.extend(y[len(path) - i:])
            else:
                path.extend(_connect(succ, path[-1], y[0]))
                path.extend(y[1:])
            j = nxt[j]
        paths.append(path)
    return paths  # @line L9
