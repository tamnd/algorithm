# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blossom-quad/. The authors are listed in prov/ZDC65T.jsonl.

"""Blossom-Quad: merge the triangles of a triangle mesh into quads by a minimum
cost perfect matching of the dual graph.

Two triangles that share an edge and form a strictly convex quad give a dual
edge. Its cost is 1 - eta, where eta = max(0, 1 - (2/pi) max_k |pi/2 - alpha_k|)
is an angle quality of the quad (1 for a rectangle), scaled to an integer so
that the matching is exact. A minimum cost perfect matching of the dual graph
is found by Edmonds' weighted blossom algorithm, in the O(n^3) primal-dual form
described by Galil, run as a maximum weight matching with the weights
K + C - cost, where K is large enough that size comes first. The quality measure and the scale are parameters of this
code. When the dual graph has no perfect matching, a full mesher must change
the triangle mesh, for example near the boundary; here the code reports
failure instead.
"""

import math
from typing import List, Optional, Sequence, Tuple

from mg3geom import orient2d

SCALE = 10 ** 6


# ---------------------------------------------------------------------------
# Edmonds' weighted blossom algorithm (maximum weight matching, optionally of
# the largest size). Vertices 0..n-1; edges (i, j, w) with integer w. Each edge
# k has two endpoints, 2k (the end i) and 2k + 1 (the end j); mate[v] is the
# endpoint at the far side of the matched edge of v, or -1.
# ---------------------------------------------------------------------------

def max_weight_matching(n: int, edges: Sequence[Tuple[int, int, int]], max_cardinality: bool = False) -> List[int]:
    """Return partner[v] (or -1) of a maximum weight matching; with
    max_cardinality, of a maximum weight matching among the largest matchings.
    Edge weights must be integers; all dual values stay integers."""
    if not edges:
        return [-1] * n
    edges = [(i, j, 2 * w) for i, j, w in edges]   # doubled, so every dual change is an integer
    m = len(edges)
    end = [edges[p // 2][p % 2] for p in range(2 * m)]
    remote = [[] for _ in range(n)]
    for k, (i, j, _) in enumerate(edges):
        remote[i].append(2 * k + 1)
        remote[j].append(2 * k)
    top = max(0, max(w for _, _, w in edges))
    mate = [-1] * n
    label = [0] * (2 * n)          # 0 free, 1 outer (S), 2 inner (T); 5 is a scan mark
    label_end = [-1] * (2 * n)
    in_blossom = list(range(n))
    parent = [-1] * (2 * n)
    children: List[Optional[list]] = [None] * (2 * n)
    base = list(range(n)) + [-1] * n
    child_ends: List[Optional[list]] = [None] * (2 * n)
    best_edge = [-1] * (2 * n)
    best_list: List[Optional[list]] = [None] * (2 * n)
    free_ids = list(range(n, 2 * n))
    dual = [top] * n + [0] * n
    allowed = [False] * m
    queue: List[int] = []

    def slack(k):
        i, j, w = edges[k]
        return dual[i] + dual[j] - 2 * w

    def leaves(b):
        if b < n:
            yield b
        else:
            for t in children[b]:
                yield from leaves(t)

    def assign_label(w, t, p):
        b = in_blossom[w]
        label[w] = label[b] = t
        label_end[w] = label_end[b] = p
        best_edge[w] = best_edge[b] = -1
        if t == 1:
            queue.extend(leaves(b))
        else:
            bb = base[b]
            assign_label(end[mate[bb]], 1, mate[bb] ^ 1)

    def scan_blossom(v, w):
        """Trace back from v and w; return the base of a new blossom, or -1
        if the two paths reach different roots (an augmenting path)."""
        path, found = [], -1
        while v != -1 or w != -1:
            b = in_blossom[v]
            if label[b] & 4:
                found = base[b]
                break
            path.append(b)
            label[b] = 5
            if label_end[b] == -1:
                v = -1
            else:
                v = end[label_end[b]]
                b = in_blossom[v]
                v = end[label_end[b]]
            if w != -1:
                v, w = w, v
        for b in path:
            label[b] = 1
        return found

    def add_blossom(bs, k):
        v, w, _ = edges[k]
        bb, bv, bw = in_blossom[bs], in_blossom[v], in_blossom[w]
        b = free_ids.pop()
        base[b] = bs
        parent[b] = -1
        parent[bb] = b
        path, ends = [], []
        while bv != bb:
            parent[bv] = b
            path.append(bv)
            ends.append(label_end[bv])
            v = end[label_end[bv]]
            bv = in_blossom[v]
        path.append(bb)
        path.reverse()
        ends.reverse()
        ends.append(2 * k)
        while bw != bb:
            parent[bw] = b
            path.append(bw)
            ends.append(label_end[bw] ^ 1)
            w = end[label_end[bw]]
            bw = in_blossom[w]
        children[b], child_ends[b] = path, ends
        label[b] = 1
        label_end[b] = label_end[bb]
        dual[b] = 0
        for x in leaves(b):
            if label[in_blossom[x]] == 2:
                queue.append(x)
            in_blossom[x] = b
        best_to = [-1] * (2 * n)
        for c in path:
            lists = ([[p // 2 for p in remote[x]] for x in leaves(c)] if best_list[c] is None else [best_list[c]])
            for lst in lists:
                for e in lst:
                    i, j, _ = edges[e]
                    if in_blossom[j] == b:
                        i, j = j, i
                    bj = in_blossom[j]
                    if bj != b and label[bj] == 1 and (best_to[bj] == -1 or slack(e) < slack(best_to[bj])):
                        best_to[bj] = e
            best_list[c] = None
            best_edge[c] = -1
        best_list[b] = [e for e in best_to if e != -1]
        best_edge[b] = -1
        for e in best_list[b]:
            if best_edge[b] == -1 or slack(e) < slack(best_edge[b]):
                best_edge[b] = e

    def expand_blossom(b, end_stage):
        for s in children[b]:
            parent[s] = -1
            if s < n:
                in_blossom[s] = s
            elif end_stage and dual[s] == 0:
                expand_blossom(s, end_stage)
            else:
                for x in leaves(s):
                    in_blossom[x] = s
        if not end_stage and label[b] == 2:
            entry = in_blossom[end[label_end[b] ^ 1]]
            j = children[b].index(entry)
            if j & 1:
                j -= len(children[b])
                step, trick = 1, 0
            else:
                step, trick = -1, 1
            p = label_end[b]
            while j != 0:
                label[end[p ^ 1]] = 0
                label[end[child_ends[b][j - trick] ^ trick ^ 1]] = 0
                assign_label(end[p ^ 1], 2, p)
                allowed[child_ends[b][j - trick] // 2] = True
                j += step
                p = child_ends[b][j - trick] ^ trick
                allowed[p // 2] = True
                j += step
            bv = children[b][j]
            label[end[p ^ 1]] = label[bv] = 2
            label_end[end[p ^ 1]] = label_end[bv] = p
            best_edge[bv] = -1
            j += step
            while children[b][j] != entry:
                bv = children[b][j]
                if label[bv] == 1:
                    j += step
                    continue
                hit = None
                for x in leaves(bv):
                    if label[x] != 0:
                        hit = x
                        break
                if hit is not None:
                    label[hit] = 0
                    label[end[mate[base[bv]]]] = 0
                    assign_label(hit, 2, label_end[hit])
                j += step
        label[b] = label_end[b] = -1
        children[b] = child_ends[b] = None
        base[b] = -1
        best_list[b] = None
        best_edge[b] = -1
        free_ids.append(b)

    def augment_blossom(b, v):
        t = v
        while parent[t] != b:
            t = parent[t]
        if t >= n:
            augment_blossom(t, v)
        i = j = children[b].index(t)
        if i & 1:
            j -= len(children[b])
            step, trick = 1, 0
        else:
            step, trick = -1, 1
        while j != 0:
            j += step
            t = children[b][j]
            p = child_ends[b][j - trick] ^ trick
            if t >= n:
                augment_blossom(t, end[p])
            j += step
            t = children[b][j]
            if t >= n:
                augment_blossom(t, end[p ^ 1])
            mate[end[p]] = p ^ 1
            mate[end[p ^ 1]] = p
        children[b] = children[b][i:] + children[b][:i]
        child_ends[b] = child_ends[b][i:] + child_ends[b][:i]
        base[b] = base[children[b][0]]

    def augment(k):
        v, w, _ = edges[k]
        for s, p in ((v, 2 * k + 1), (w, 2 * k)):
            while True:
                bs = in_blossom[s]
                if bs >= n:
                    augment_blossom(bs, s)
                mate[s] = p
                if label_end[bs] == -1:
                    break
                t = end[label_end[bs]]
                bt = in_blossom[t]
                s = end[label_end[bt]]
                j = end[label_end[bt] ^ 1]
                if bt >= n:
                    augment_blossom(bt, j)
                mate[j] = label_end[bt]
                p = label_end[bt] ^ 1

    for _ in range(n):
        label[:] = [0] * (2 * n)
        best_edge[:] = [-1] * (2 * n)
        for b in range(n, 2 * n):
            best_list[b] = None
        allowed[:] = [False] * m
        queue[:] = []
        for v in range(n):
            if mate[v] == -1 and label[in_blossom[v]] == 0:
                assign_label(v, 1, -1)
        augmented = False
        while True:
            while queue and not augmented:
                v = queue.pop()
                for p in remote[v]:
                    k = p // 2
                    w = end[p]
                    if in_blossom[v] == in_blossom[w]:
                        continue
                    if not allowed[k]:
                        ks = slack(k)
                        if ks <= 0:
                            allowed[k] = True
                    if allowed[k]:
                        if label[in_blossom[w]] == 0:
                            assign_label(w, 2, p ^ 1)
                        elif label[in_blossom[w]] == 1:
                            bs = scan_blossom(v, w)
                            if bs >= 0:
                                add_blossom(bs, k)
                            else:
                                augment(k)
                                augmented = True
                                break
                        elif label[w] == 0:
                            label[w] = 2
                            label_end[w] = p ^ 1
                    elif label[in_blossom[w]] == 1:
                        b = in_blossom[v]
                        if best_edge[b] == -1 or ks < slack(best_edge[b]):
                            best_edge[b] = k
                    elif label[w] == 0:
                        if best_edge[w] == -1 or ks < slack(best_edge[w]):
                            best_edge[w] = k
            if augmented:
                break
            kind, delta, d_edge, d_blossom = -1, None, -1, -1
            if not max_cardinality:
                kind, delta = 1, min(dual[:n])
            for v in range(n):
                if label[in_blossom[v]] == 0 and best_edge[v] != -1:
                    d = slack(best_edge[v])
                    if kind == -1 or d < delta:
                        kind, delta, d_edge = 2, d, best_edge[v]
            for b in range(2 * n):
                if parent[b] == -1 and label[b] == 1 and best_edge[b] != -1:
                    ks = slack(best_edge[b])
                    assert ks % 2 == 0
                    d = ks // 2
                    if kind == -1 or d < delta:
                        kind, delta, d_edge = 3, d, best_edge[b]
            for b in range(n, 2 * n):
                if base[b] >= 0 and parent[b] == -1 and label[b] == 2 and (kind == -1 or dual[b] < delta):
                    kind, delta, d_blossom = 4, dual[b], b
            if kind == -1:
                kind, delta = 1, max(0, min(dual[:n]))
            for v in range(n):
                if label[in_blossom[v]] == 1:
                    dual[v] -= delta
                elif label[in_blossom[v]] == 2:
                    dual[v] += delta
            for b in range(n, 2 * n):
                if base[b] >= 0 and parent[b] == -1:
                    if label[b] == 1:
                        dual[b] += delta
                    elif label[b] == 2:
                        dual[b] -= delta
            if kind == 1:
                break
            if kind == 2:
                allowed[d_edge] = True
                i, j, _ = edges[d_edge]
                if label[in_blossom[i]] == 0:
                    i, j = j, i
                queue.append(i)
            elif kind == 3:
                allowed[d_edge] = True
                queue.append(edges[d_edge][0])
            else:
                expand_blossom(d_blossom, False)
        if not augmented:
            break
        for b in range(n, 2 * n):
            if parent[b] == -1 and base[b] >= 0 and label[b] == 1 and dual[b] == 0:
                expand_blossom(b, True)
    return [end[mate[v]] if mate[v] >= 0 else -1 for v in range(n)]


def min_cost_perfect_matching(n: int, edges: Sequence[Tuple[int, int, int]]) -> Optional[List[int]]:
    """A perfect matching of least total cost, as partner[v], or None if the
    graph has no perfect matching. Costs are integers."""
    if n % 2:
        return None
    if n == 0:
        return []
    # weight K + C - cost: with K = n C, a larger matching always weighs more,
    # so a maximum weight matching has the largest size and, among those, the least cost
    C = 1 + max((c for _, _, c in edges), default=0)
    K = n * C
    partner = max_weight_matching(n, [(i, j, K + C - c) for i, j, c in edges])
    return partner if all(p >= 0 for p in partner) else None


# ---------------------------------------------------------------------------
# The mesher.
# ---------------------------------------------------------------------------

def quad_quality(P, q) -> float:
    """max(0, 1 - (2/pi) max_k |pi/2 - alpha_k|) over the four corner angles."""
    worst = 0.0
    for s in range(4):
        a, b, c = P[q[s - 1]], P[q[s]], P[q[(s + 1) % 4]]
        u = (float(a[0] - b[0]), float(a[1] - b[1]))
        v = (float(c[0] - b[0]), float(c[1] - b[1]))
        ang = abs(math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1]))
        worst = max(worst, abs(math.pi / 2 - ang))
    return max(0.0, 1.0 - 2.0 * worst / math.pi)


def dual_graph(P, tris: Sequence[Tuple[int, int, int]]):
    """The dual edges (t1, t2, cost, quad) of pairs of triangles that share an
    edge and form a strictly convex quad."""
    own = {}
    for k, (a, b, c) in enumerate(tris):
        for e in ((a, b), (b, c), (c, a)):
            own[e] = k
    out = []
    for (u, v), t1 in sorted(own.items()):
        t2 = own.get((v, u))
        if t2 is None or t1 > t2:
            continue
        k = next(x for x in tris[t1] if x not in (u, v))
        l = next(x for x in tris[t2] if x not in (u, v))
        q = (u, l, v, k)
        if all(orient2d(P[q[s]], P[q[(s + 1) % 4]], P[q[(s + 2) % 4]]) > 0 for s in range(4)):  # @line L3
            out.append((t1, t2, round(SCALE * (1.0 - quad_quality(P, q))), q))
    return out


def blossom_quad(P, tris: Sequence[Tuple[int, int, int]]):
    """Return (quads, total cost) or (None, reason). Quads are counterclockwise."""
    if len(tris) % 2:  # @line L1
        return None, "an odd number of triangles cannot be paired"
    dual = dual_graph(P, tris)  # @line L2
    partner = min_cost_perfect_matching(len(tris), [(t1, t2, c) for t1, t2, c, _ in dual])  # @line L4
    if partner is None:  # @line L5
        return None, "the dual graph has no perfect matching"
    quads, cost = [], 0
    for t1, t2, c, q in dual:  # @line L6
        if partner[t1] == t2:
            quads.append(q)
            cost += c
    return quads, cost  # @line L7
