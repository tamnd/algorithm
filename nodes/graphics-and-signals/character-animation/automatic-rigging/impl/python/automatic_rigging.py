# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/automatic-rigging/. The authors are listed in prov/FM8DXC.jsonl.
"""Automatic rigging by heat diffusion (Baran and Popovic 2007), in 2D.

The character is a simple polygon, and its surface is the closed boundary
polyline. The method has two parts.

1. Embedding. Each joint of a template skeleton is assigned to one of a set
   of candidate points inside the shape (the paper uses the centers of
   medial spheres). The cost of an assignment is a sum of nonnegative
   penalties of the bones. The best assignment is found by a best-first (A*)
   search over partial assignments, with an admissible lower bound for the
   bones that are not placed yet. The penalties here are a small set of the
   same kind as in the paper (length, direction, a bone that leaves the
   shape), not the paper's set.

2. Heat weights. For each bone i, the weights w^i on the surface vertices
   solve the discrete equation (K + M H) w^i = M H p^i, the weak form of
   -Lap w + H w = H p. K is the stiffness matrix of the polyline (1 / length
   per edge), M the lumped mass (half the length of the two edges at a
   vertex), H_jj = c / d(j)^2 with d(j) the distance from vertex j to the
   nearest bone that it can see, and p^i_j = 1 / k if bone i is one of the k
   nearest visible bones of j, else 0. A vertex that sees no bone has
   H_jj = 0. The matrix does not depend on i, so it is factored once by
   Cholesky.
"""

import heapq
import itertools
import math

from anim import cross2, dot, norm, sub


# ---------------------------------------------------------------- geometry


def _orient(a, b, c):
    return cross2(sub(b, a), sub(c, a))


def segments_cross(a, b, c, d):
    """Return True if the segments ab and cd cross at a point inside both (proper crossing)."""
    o1, o2 = _orient(a, b, c), _orient(a, b, d)
    o3, o4 = _orient(c, d, a), _orient(c, d, b)
    return o1 * o2 < 0.0 and o3 * o4 < 0.0


def closest_on_segment(p, a, b):
    """Return the point of the segment ab closest to p."""
    ab = sub(b, a)
    l2 = dot(ab, ab)
    if l2 == 0.0:
        return a
    t = max(0.0, min(1.0, dot(sub(p, a), ab) / l2))
    return (a[0] + t * ab[0], a[1] + t * ab[1])


def crosses_boundary(a, b, poly, skip=()):
    """Return True if the segment ab crosses an edge of the closed polygon, skipping edges that touch vertex indices in skip."""
    n = len(poly)
    for e in range(n):
        f = (e + 1) % n
        if e in skip or f in skip:
            continue
        if segments_cross(a, b, poly[e], poly[f]):
            return True
    return False


# ---------------------------------------------------------------- embedding


def bone_penalty(pa, pc, template, poly, alpha=(1.0, 1.0, 10.0)):
    """Return the nonnegative penalty of a bone placed from pa to pc.

    template is the bone vector of the skeleton. The terms are the relative
    length error squared, 1 - cos of the angle to the template direction, and
    a fixed penalty if the bone leaves the shape.
    """
    d = sub(pc, pa)
    ld, lt = norm(d), norm(template)
    length = ((ld - lt) / lt) ** 2
    direction = 1.0 if ld == 0.0 else 1.0 - dot(d, template) / (ld * lt)
    outside = 1.0 if crosses_boundary(pa, pc, poly) else 0.0
    return alpha[0] * length + alpha[1] * direction + alpha[2] * outside


def embed(parents, offsets, candidates, poly):
    """Return (cost, assignment, expanded) of the best embedding by A* search.

    parents[j] is the parent of joint j (-1 for the root, and parents[j] < j);
    offsets[j] is the template vector of the bone from parents[j] to j.
    assignment[j] is the index of the candidate point of joint j.
    """
    nj, nc = len(parents), len(candidates)
    table = [None] * nj  # @line L2
    low = [0.0] * nj
    for j in range(1, nj):
        table[j] = [
            [bone_penalty(candidates[a], candidates[b], offsets[j], poly) for b in range(nc)] for a in range(nc)
        ]
        low[j] = min(min(row) for row in table[j])
    rest = [sum(low[j + 1 :]) for j in range(nj)]
    heap = [(rest[0], 0.0, 0, ())]  # @line L3
    count = 1
    expanded = 0
    while heap:
        f, g, _, part = heapq.heappop(heap)  # @line L4
        if len(part) == nj:  # @line L5
            return g, list(part), expanded
        expanded += 1
        j = len(part)
        for c in range(nc):  # @line L6
            g2 = g if j == 0 else g + table[j][part[parents[j]]][c]
            heapq.heappush(heap, (g2 + rest[j], g2, count, part + (c,)))
            count += 1
    raise ValueError("no embedding")


def brute_force_embedding(parents, offsets, candidates, poly):
    """Return (cost, assignment) of the best embedding by trying every assignment."""
    nj, nc = len(parents), len(candidates)
    best = (math.inf, None)
    for part in itertools.product(range(nc), repeat=nj):
        cost = sum(bone_penalty(candidates[part[parents[j]]], candidates[part[j]], offsets[j], poly) for j in range(1, nj))
        if cost < best[0]:
            best = (cost, list(part))
    return best


# ---------------------------------------------------------------- heat weights


def stiffness_and_mass(poly):
    """Return (K, m): the stiffness matrix of the closed polyline and the lumped masses."""
    n = len(poly)
    k = [[0.0] * n for _ in range(n)]
    m = [0.0] * n
    for e in range(n):
        f = (e + 1) % n
        le = norm(sub(poly[f], poly[e]))
        k[e][e] += 1.0 / le
        k[f][f] += 1.0 / le
        k[e][f] -= 1.0 / le
        k[f][e] -= 1.0 / le
        m[e] += 0.5 * le
        m[f] += 0.5 * le
    return k, m


def nearest_visible(poly, bones, j, rel_tie=1e-9):
    """Return (d, ids): the distance to the nearest visible bones of vertex j and their indices."""
    v = poly[j]
    dist = []
    for i, (a, b) in enumerate(bones):
        c = closest_on_segment(v, a, b)
        if not crosses_boundary(v, c, poly, skip=(j,)):
            dist.append((norm(sub(c, v)), i))
    if not dist:
        return math.inf, []
    d = min(x for x, _ in dist)
    return d, [i for x, i in dist if x <= d * (1.0 + rel_tie)]


def cholesky(a):
    """Return the lower triangular L with a = L L^T. Raise ValueError if a is not positive definite."""
    n = len(a)
    lo = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(lo[i][k] * lo[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("matrix is not positive definite")
                lo[i][i] = math.sqrt(s)
            else:
                lo[i][j] = s / lo[j][j]
    return lo


def cholesky_solve(lo, b):
    """Solve L L^T x = b."""
    n = len(lo)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(lo[i][k] * y[k] for k in range(i))) / lo[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(lo[k][i] * x[k] for k in range(i + 1, n))) / lo[i][i]
    return x


def heat_system(poly, bones, c=1.0):
    """Return (A, rhs) with A = K + M H and rhs[i] = M H p^i for each bone i."""
    n, nb = len(poly), len(bones)
    k, m = stiffness_and_mass(poly)  # @line L7
    a = [row[:] for row in k]
    rhs = [[0.0] * n for _ in range(nb)]
    for j in range(n):
        d, ids = nearest_visible(poly, bones, j)  # @line L8
        if not ids:
            continue
        if d == 0.0:
            raise ValueError("a bone touches the surface; bones must lie strictly inside")
        h = c / (d * d)
        a[j][j] += m[j] * h
        for i in ids:
            rhs[i][j] = m[j] * h / len(ids)
    return a, rhs


def heat_weights(poly, bones, c=1.0):
    """Return w with w[i][j] the weight of bone i at vertex j."""
    a, rhs = heat_system(poly, bones, c)
    lo = cholesky(a)  # @line L9
    return [cholesky_solve(lo, r) for r in rhs]  # @line L10


def rig(poly, parents, offsets, candidates, c=1.0):
    """Return (joints, weights): the embedded joint positions and the heat weights of the bones 1..J-1."""
    _, part, _ = embed(parents, offsets, candidates, poly)  # @line L1
    joints = [candidates[x] for x in part]
    bones = [(joints[parents[j]], joints[j]) for j in range(1, len(parents))]
    return joints, heat_weights(poly, bones, c)
