# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hdbscan/. The authors are listed in prov/Q8SHE1.jsonl.

"""HDBSCAN* (Campello, Moulavi and Sander 2013) from the definitions.

Steps: core distances, the minimum spanning tree of the mutual reachability
graph by the dense form of Prim's algorithm, the condensed cluster tree by a
sweep over the distance levels from high to low, the stability of each
cluster, and the selection of flat clusters by a dynamic program on the tree.
Points are assumed distinct enough that every core distance is positive.
"""

import math

NOISE = -1


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def core_distances(points, min_pts, dist=euclidean):
    """Distance to the min_pts-th nearest point, the point itself counted."""
    out = []
    for p in points:
        ds = sorted(dist(p, q) for q in points)
        out.append(ds[min_pts - 1])
    return out


def mutual_reachability(points, core, i, j, dist=euclidean):
    if i == j:
        return core[i]
    return max(core[i], core[j], dist(points[i], points[j]))


def mst_prim(points, core, dist=euclidean):
    """Edges (u, v, w) of a minimum spanning tree of the complete mutual
    reachability graph, by Prim's algorithm with an array: O(n^2) distances."""
    n = len(points)
    if n == 0:
        return []
    in_tree = [False] * n
    best = [math.inf] * n
    parent = [-1] * n
    best[0] = 0.0
    edges = []
    for _ in range(n):
        u = min((i for i in range(n) if not in_tree[i]), key=lambda i: (best[i], i))
        in_tree[u] = True
        if parent[u] >= 0:
            edges.append((parent[u], u, best[u]))
        for v in range(n):
            if not in_tree[v]:
                w = mutual_reachability(points, core, u, v, dist)
                if w < best[v]:
                    best[v], parent[v] = w, u
    return edges


def _components(present, edges, level):
    """Union-find over the present points with the edges of weight < level."""
    root = {p: p for p in present}

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    for u, v, w in edges:
        if w < level and u in root and v in root:
            ru, rv = find(u), find(v)
            if ru != rv:
                root[ru] = rv
    return {p: find(p) for p in present}


def condensed_tree(n, edges, core, min_cluster_size):
    """Return (parent, birth, members, exit_lambda) for the condensed tree.

    Cluster 0 is the root, born at lambda = 0 with all points. members[c] is the
    set of points of c at its birth, and exit_lambda[c][x] is the lambda = 1/eps
    at which x leaves c (it becomes noise, or c splits or vanishes).
    """
    if any(c <= 0 for c in core):
        raise ValueError("a core distance is 0; remove duplicate points")
    parent, birth, members, exit_lambda = [-1], [0.0], [set(range(n))], [{}]
    active = {0: set(range(n))} if n >= max(1, min_cluster_size) else {}  # @line L7
    if not active:
        exit_lambda[0] = {x: 0.0 for x in range(n)}
    levels = sorted({w for _, _, w in edges} | set(core), reverse=True)
    for level in levels:  # @line L8
        if not active:
            break
        lam = 1.0 / level
        present = [x for x in range(n) if core[x] < level]  # @line L9
        comp = _components(present, edges, level)
        for c in list(active):  # @line L10
            current = active[c]
            groups = {}
            for x in current:
                if x in comp:
                    groups.setdefault(comp[x], set()).add(x)
            big = [g for g in groups.values() if len(g) >= min_cluster_size]  # @line L11
            if len(big) == 1 and len(big[0]) == len(current):  # @line L12
                continue  # nothing changes in c at this level
            if len(big) == 1:  # @line L13
                for x in current - big[0]:
                    exit_lambda[c][x] = lam  # these points become noise
                active[c] = big[0]
                continue
            for x in current:  # @line L14
                exit_lambda[c][x] = lam  # c splits or vanishes
            del active[c]
            if len(big) >= 2:  # @line L15
                for g in sorted(big, key=min):
                    parent.append(c)
                    birth.append(lam)
                    members.append(set(g))
                    exit_lambda.append({})
                    active[len(parent) - 1] = set(g)
    return parent, birth, members, exit_lambda


def stability(birth, members, exit_lambda):
    """S(C) = sum over the points x of C of (lambda_exit(x, C) - lambda_birth(C))."""
    return [sum(exit_lambda[c][x] - birth[c] for x in members[c]) for c in range(len(birth))]


def select_clusters(parent, stab, allow_single_cluster=False):
    """Choose clusters with no ancestor relation and the largest total stability.

    Bottom-up dynamic program: best(C) = max(S(C), sum of best(child)).
    A tie keeps the parent. The root (cluster 0) is a candidate only if
    allow_single_cluster is true.
    """
    m = len(parent)
    children = [[] for _ in range(m)]
    for c in range(1, m):
        children[parent[c]].append(c)
    best, chosen = [0.0] * m, [None] * m
    for c in range(m - 1, -1, -1):  # children have larger ids than parents  # @line L16
        if not children[c]:  # @line L17
            if c == 0 and not allow_single_cluster:
                best[c], chosen[c] = 0.0, []
            else:
                best[c], chosen[c] = stab[c], [c]
            continue
        child_sum = sum(best[ch] for ch in children[c])
        if (c != 0 or allow_single_cluster) and stab[c] >= child_sum:  # @line L18
            best[c], chosen[c] = stab[c], [c]
        else:
            best[c] = child_sum  # @line L19
            chosen[c] = [x for ch in children[c] for x in chosen[ch]]
    return sorted(chosen[0]), best[0]  # @line L20


def hdbscan(points, min_pts, min_cluster_size=None, allow_single_cluster=False, dist=euclidean):
    """Return labels by point index: -1 for noise, clusters 0, 1, 2, ..."""
    if min_cluster_size is None:
        min_cluster_size = min_pts
    n = len(points)
    if n == 0:
        return []
    core = core_distances(points, min_pts, dist)  # @line L1
    edges = mst_prim(points, core, dist)  # @line L2
    parent, birth, members, exit_lambda = condensed_tree(n, edges, core, min_cluster_size)  # @line L3
    stab = stability(birth, members, exit_lambda)  # @line L4
    selected, _ = select_clusters(parent, stab, allow_single_cluster)  # @line L5
    labels = [NOISE] * n
    for label, c in enumerate(selected):  # @line L6
        for x in members[c]:
            labels[x] = label
    return labels
