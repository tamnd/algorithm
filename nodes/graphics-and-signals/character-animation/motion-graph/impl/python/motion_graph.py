# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/motion-graph/. The authors are listed in prov/VP75X0.jsonl.
"""Motion graph construction (Kovar, Gleicher and Pighin 2002).

A motion database is a list of clips. A clip is a list of frames, and a
frame is a point cloud: the world positions (x, y, z) of the j joints, with
y up. The frames of all clips are numbered 0 .. f-1 in clip order.

The distance of frame a and frame b is the weighted squared distance of the
point clouds of the windows a .. a+k-1 and b .. b+k-1, after the 2D rigid
transform (a rotation about the vertical axis y and a translation in the
ground plane xz) that best aligns the second window to the first. That
transform has a closed form.

Construction:
  1. compute the distance for every pair of window starts (O(f^2) pairs);
  2. keep a pair (a, b) as a transition if its distance is a local minimum
     of the distance matrix and is below the threshold (a tuning);
  3. build the graph: an edge from every frame to the next frame of its
     clip, and an edge a -> b + k for every transition (the blend of the
     windows plays in between);
  4. prune the graph to its largest strongly connected component, found by
     Tarjan's algorithm, so that every frame left can reach every other.
"""

import math


def align_2d(P, Q, w=None):
    """Best (theta, x0, z0) so that rotating Q about y by theta and then
    moving it by (x0, 0, z0) is nearest to P in the weighted least squares
    sense. The rotation maps (x, z) to (x cos t + z sin t, -x sin t + z cos t).
    """
    n = len(P)
    if w is None:
        w = [1.0 / n] * n
    W = sum(w)
    w = [wi / W for wi in w]
    xb = sum(wi * p[0] for wi, p in zip(w, P))
    zb = sum(wi * p[2] for wi, p in zip(w, P))
    xb2 = sum(wi * q[0] for wi, q in zip(w, Q))
    zb2 = sum(wi * q[2] for wi, q in zip(w, Q))
    s = sum(wi * (p[0] * q[2] - q[0] * p[2]) for wi, p, q in zip(w, P, Q)) - (xb * zb2 - xb2 * zb)
    c = sum(wi * (p[0] * q[0] + p[2] * q[2]) for wi, p, q in zip(w, P, Q)) - (xb * xb2 + zb * zb2)
    t = math.atan2(s, c)  # @line L3
    x0 = xb - xb2 * math.cos(t) - zb2 * math.sin(t)
    z0 = zb + xb2 * math.sin(t) - zb2 * math.cos(t)
    return t, x0, z0


def transform(q, t, x0, z0):
    ct, st = math.cos(t), math.sin(t)
    return (q[0] * ct + q[2] * st + x0, q[1], -q[0] * st + q[2] * ct + z0)


def cloud_distance(P, Q, w=None, align=None):
    n = len(P)
    if w is None:
        w = [1.0 / n] * n
    W = sum(w)
    if align is None:
        align = align_2d(P, Q, w)
    t, x0, z0 = align
    total = 0.0
    for wi, p, q in zip(w, P, Q):
        r = transform(q, t, x0, z0)
        total += wi / W * ((p[0] - r[0]) ** 2 + (p[1] - r[1]) ** 2 + (p[2] - r[2]) ** 2)
    return total


def flatten(clips):
    frames, clip_of, starts = [], [], []
    for c, clip in enumerate(clips):
        starts.append(len(frames))
        for fr in clip:
            frames.append(fr)
            clip_of.append(c)
    return frames, clip_of, starts


def window_starts(clips, k):
    """Frame numbers a such that a .. a+k-1 lie in one clip."""
    out = []
    pos = 0
    for clip in clips:
        out.extend(range(pos, pos + len(clip) - k + 1))
        pos += len(clip)
    return out


def distance_matrix(clips, k):
    frames, _, _ = flatten(clips)
    starts = window_starts(clips, k)
    D = {}
    for a in starts:  # @line L1
        P = [p for fr in frames[a:a + k] for p in fr]
        for b in starts:
            Q = [q for fr in frames[b:b + k] for q in fr]
            D[(a, b)] = cloud_distance(P, Q)  # @line L2
    return D, starts


def transitions(D, starts, threshold, min_gap):
    """Pairs that are local minima of D (8 neighbors) and below threshold.
    Pairs with |a - b| < min_gap are skipped (they are the same motion)."""
    sset = set(starts)
    out = []
    for a in starts:
        for b in starts:
            if abs(a - b) < min_gap:
                continue
            v = D[(a, b)]
            if v >= threshold:  # @line L4
                continue
            ok = True
            for da in (-1, 0, 1):
                for db in (-1, 0, 1):
                    if (da or db) and (a + da) in sset and (b + db) in sset:
                        if D[(a + da, b + db)] < v:
                            ok = False
            if ok:  # @line L5
                out.append((a, b))
    return out


def build_graph(clips, trans, k):
    """Adjacency lists over the frames 0 .. f-1."""
    frames, clip_of, _ = flatten(clips)
    f = len(frames)
    adj = [[] for _ in range(f)]
    for u in range(f - 1):
        if clip_of[u] == clip_of[u + 1]:
            adj[u].append(u + 1)  # @line L6
    for a, b in trans:
        if b + k < f and clip_of[b + k] == clip_of[b]:
            adj[a].append(b + k)  # @line L7
    return adj


def tarjan_scc(adj):
    """Strongly connected components by Tarjan's algorithm (iterative)."""
    n = len(adj)
    index = [None] * n
    low = [0] * n
    on = [False] * n
    stack, comps = [], []
    counter = 0
    for root in range(n):
        if index[root] is not None:
            continue
        work = [(root, 0)]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on[root] = True
        while work:
            v, i = work[-1]
            if i < len(adj[v]):
                work[-1] = (v, i + 1)
                u = adj[v][i]
                if index[u] is None:
                    index[u] = low[u] = counter
                    counter += 1
                    stack.append(u)
                    on[u] = True
                    work.append((u, 0))
                elif on[u]:
                    low[v] = min(low[v], index[u])
            else:
                work.pop()
                if work:
                    p = work[-1][0]
                    low[p] = min(low[p], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        u = stack.pop()
                        on[u] = False
                        comp.append(u)
                        if u == v:
                            break
                    comps.append(sorted(comp))
    return comps


def prune(adj):
    """Keep the largest strongly connected component. Ties go to the
    component with the smallest frame number. Return (kept set, new adj)."""
    comps = tarjan_scc(adj)
    best = min(comps, key=lambda c: (-len(c), c[0]))  # @line L8
    keep = set(best)
    new = [[u for u in adj[v] if u in keep] if v in keep else [] for v in range(len(adj))]
    return keep, new


def blend_weight(p, k):
    """alpha(p) = 2((p+1)/k)^3 - 3((p+1)/k)^2 + 1 for -1 <= p <= k - 1."""
    s = (p + 1.0) / k
    return 2.0 * s ** 3 - 3.0 * s ** 2 + 1.0


def build(clips, k, threshold, min_gap=None):
    if min_gap is None:
        min_gap = k
    D, starts = distance_matrix(clips, k)
    trans = transitions(D, starts, threshold, min_gap)
    adj = build_graph(clips, trans, k)
    keep, pruned = prune(adj)
    return {"D": D, "starts": starts, "transitions": trans, "adj": adj,
            "keep": keep, "pruned": pruned}
