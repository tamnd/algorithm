# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-shape-approximation/. The authors are listed in prov/J5DY1Y.jsonl.

"""Variational shape approximation with planar proxies and the L^(2,1) error.

Cohen-Steiner, Alliez and Desbrun (SIGGRAPH 2004). Each region R_i of faces
has a proxy, a unit normal N_i and a point X_i. The error of a face T in R_i
is area(T) |n_T - N_i|^2, and the energy is the sum over all faces.

The loop alternates two steps, as in Lloyd's algorithm. The fit step sets
N_i to the unit vector along the sum of area(T) n_T over R_i, which is the
best normal for R_i. The partition step grows the regions again from one
seed face each, in order of error, so that each region stays connected. The
grown partition is kept only if its energy is not larger than the energy of
the old partition with the same proxies. With this guard the energy never
increases. Proxies are added one at a time, at the face with the largest
error in the region with the largest total error, until there are k.

coarse_mesh then puts an anchor at each vertex where three or more regions
meet, moved to the mean of its projections to the planes of those regions,
and gives each region the polygon of the anchors on its border, in order.
"""

import heapq

from mx1mesh import add, dot, face_adjacency, face_area, face_cross, scale, sub, unit


def face_data(points, faces):
    areas = [face_area(points, f) for f in faces]
    normals = [unit(face_cross(points, f)) for f in faces]
    return areas, normals


def error(area, n, N):
    d = sub(n, N)
    return area * dot(d, d)


def energy(areas, normals, label, N):
    return sum(error(areas[t], normals[t], N[label[t]]) for t in range(len(label)))


def fit(areas, normals, label, N):
    """The best unit normal of each region: unit(sum of area n_T), or the old normal if the sum is 0."""
    m = [(0.0, 0.0, 0.0) for _ in N]
    for t, i in enumerate(label):
        m[i] = add(m[i], scale(areas[t], normals[t]))
    return [unit(m[i]) if dot(m[i], m[i]) > 0 else N[i] for i in range(len(N))]  # @line L4


def flood(areas, normals, adj, label, N):
    """Grow each region from its best face, always taking the free face with the least error to the proxy that reached it."""
    best = {}
    for t, i in enumerate(label):
        e = error(areas[t], normals[t], N[i])
        if i not in best or e < best[i][0]:
            best[i] = (e, t)
    new = [-1] * len(label)
    heap, count = [], 0
    for i in sorted(best):  # @line L5
        t = best[i][1]
        new[t] = i
        for u in adj[t]:
            heapq.heappush(heap, (error(areas[u], normals[u], N[i]), count, u, i))
            count += 1
    while heap:  # @line L6
        _, _, t, i = heapq.heappop(heap)
        if new[t] != -1:
            continue
        new[t] = i
        for u in adj[t]:
            if new[u] == -1:
                heapq.heappush(heap, (error(areas[u], normals[u], N[i]), count, u, i))
                count += 1
    return new


def vsa(points, faces, k, iters=30):
    """Partition the faces of a connected mesh into at most k regions with planar proxies.

    Returns (label, N, X, history): the region of each face, the proxy normals,
    the proxy points (area-weighted centroids), and the energy after each step.
    """
    areas, normals = face_data(points, faces)
    adj = face_adjacency(faces)
    label = [0] * len(faces)  # @line L1
    N = [normals[0]]
    history = [energy(areas, normals, label, N)]
    while True:  # @line L2
        for _ in range(iters):  # @line L3
            N = fit(areas, normals, label, N)
            history.append(energy(areas, normals, label, N))
            new = flood(areas, normals, adj, label, N)
            if new != label and energy(areas, normals, new, N) <= history[-1]:  # @line L7
                label = new
                history.append(energy(areas, normals, label, N))
            else:
                break
        N = fit(areas, normals, label, N)
        history.append(energy(areas, normals, label, N))
        if len(N) >= k or history[-1] == 0:  # @line L8
            break
        total = [0.0] * len(N)
        for t, i in enumerate(label):
            total[i] += error(areas[t], normals[t], N[i])
        worst = max(range(len(N)), key=lambda i: total[i])  # @line L9
        t = max((t for t in range(len(faces)) if label[t] == worst), key=lambda t: error(areas[t], normals[t], N[worst]))
        label[t] = len(N)  # @line L10
        N = N + [normals[t]]
        history.append(energy(areas, normals, label, N))
    X = []
    for i in range(len(N)):
        a = sum(areas[t] for t in range(len(faces)) if label[t] == i)
        c = (0.0, 0.0, 0.0)
        for t in range(len(faces)):
            if label[t] == i:
                g = scale(1 / 3, add(add(points[faces[t][0]], points[faces[t][1]]), points[faces[t][2]]))
                c = add(c, scale(areas[t] / a, g))
        X.append(c)
    return label, N, X, history


def coarse_mesh(points, faces, label, N, X):
    """Anchors where three or more regions meet, and for each region the loops of anchors on its border.

    Returns (anchor_points, polygons), where each polygon is (region, list of anchor indices).
    A border loop with fewer than three anchors gives no polygon.
    """
    regions = [set() for _ in points]
    for t, f in enumerate(faces):
        for v in f:
            regions[v].add(label[t])
    anchor, anchor_points = {}, []
    for v, rs in enumerate(regions):
        if len(rs) >= 3:
            p = (0.0, 0.0, 0.0)
            for i in rs:  # project to the plane of each proxy and average
                q = sub(points[v], scale(dot(sub(points[v], X[i]), N[i]), N[i]))
                p = add(p, scale(1 / len(rs), q))
            anchor[v] = len(anchor_points)
            anchor_points.append(p)
    owner = {}
    for t, f in enumerate(faces):
        for c in range(3):
            owner[(f[c], f[(c + 1) % 3])] = label[t]
    polygons = []
    for i in sorted(set(label)):
        nxt = {}
        for t, f in enumerate(faces):
            if label[t] != i:
                continue
            for c in range(3):
                a, b = f[c], f[(c + 1) % 3]
                if owner.get((b, a)) != i:  # a border half-edge of the region
                    nxt.setdefault(a, []).append(b)
        while nxt:
            start = min(nxt)
            loop, v = [], start
            while True:
                loop.append(v)
                w = nxt[v].pop()
                if not nxt[v]:
                    del nxt[v]
                v = w
                if v == start:
                    break
            poly = [anchor[v] for v in loop if v in anchor]
            if len(poly) >= 3:
                polygons.append((i, poly))
    return anchor_points, polygons
