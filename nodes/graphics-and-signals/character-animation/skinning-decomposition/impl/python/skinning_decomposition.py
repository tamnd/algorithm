# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skinning-decomposition/. The authors are listed in prov/H700TR.jsonl.
"""Smooth skinning decomposition with rigid bones (SSDR, Le and Deng 2012), in 2D.

Input: rest vertices v_i and example meshes q_(f,i) for the frames f. Output:
weights w_(i,b) and one rigid transform (R_(f,b), T_(f,b)) per frame and bone,
so that linear blend skinning reproduces the examples:

    E = sum_f sum_i | q_(f,i) - sum_b w_(i,b) (R_(f,b) v_i + T_(f,b)) |^2.

The weights are nonnegative, sum to 1 and have at most K nonzero entries per
vertex. The method alternates two steps.

- Weights, per vertex: least squares over the simplex. This code solves it
  exactly for a few bones by trying every support (the equality-constrained
  solution on each support, kept if it is nonnegative), then keeps the K
  largest weights and solves again on them. If the sparse weights give a
  larger error than the old weights of the vertex, the old ones are kept;
  this safeguard is ours, not the paper's.
- Bones, one at a time with the others fixed, per frame: a weighted
  Procrustes problem with a closed form solution.

The initial bones come from k-means on the vertex trajectories and a rigid
fit per cluster.
"""

import itertools
import math
import random

from anim import cross2, dot, solve


def transform(rt, v):
    """Apply (theta, (tx, ty)) to a 2D point."""
    theta, t = rt
    c, s = math.cos(theta), math.sin(theta)
    return (c * v[0] - s * v[1] + t[0], s * v[0] + c * v[1] + t[1])


def skin(rest, weights, bones, f):
    """Return the skinned mesh of frame f; bones[b][f] = (theta, t)."""
    out = []
    for v, w in zip(rest, weights):
        x = y = 0.0
        for b, wb in enumerate(w):
            if wb != 0.0:
                p = transform(bones[b][f], v)
                x += wb * p[0]
                y += wb * p[1]
        out.append((x, y))
    return out


def error(rest, frames, weights, bones):
    """Return E, the sum of squared distances over all frames and vertices."""
    e = 0.0
    for f, q in enumerate(frames):
        for p, r in zip(skin(rest, weights, bones, f), q):
            e += (p[0] - r[0]) ** 2 + (p[1] - r[1]) ** 2
    return e


def weighted_procrustes(points, targets, w):
    """Return (theta, t) minimizing sum_i |targets_i - w_i (R points_i + t)|^2."""
    sw2 = sum(x * x for x in w)
    if sw2 == 0.0:
        return 0.0, (0.0, 0.0)
    pbar = tuple(sum(x * x * p[k] for x, p in zip(w, points)) / sw2 for k in range(2))
    qbar = tuple(sum(x * r[k] for x, r in zip(w, targets)) / sw2 for k in range(2))
    sc = sd = 0.0
    for x, p, r in zip(w, points, targets):
        pt = (x * (p[0] - pbar[0]), x * (p[1] - pbar[1]))
        qt = (r[0] - x * qbar[0], r[1] - x * qbar[1])
        sc += cross2(pt, qt)
        sd += dot(pt, qt)
    theta = math.atan2(sc, sd)
    c, s = math.cos(theta), math.sin(theta)
    t = (qbar[0] - (c * pbar[0] - s * pbar[1]), qbar[1] - (s * pbar[0] + c * pbar[1]))
    return theta, t


def simplex_lsq(cols, target, allowed):
    """Return the w >= 0 with sum 1 and support in allowed minimizing |sum_b w_b cols_b - target|^2.

    cols[b] is a vector; every support inside allowed is tried.
    """
    best, best_e = None, math.inf
    for r in range(1, len(allowed) + 1):
        for sup in itertools.combinations(allowed, r):
            k = len(sup)
            a = [[0.0] * (k + 1) for _ in range(k + 1)]
            rhs = [0.0] * (k + 1)
            for i, bi in enumerate(sup):
                for j, bj in enumerate(sup):
                    a[i][j] = 2.0 * dot(cols[bi], cols[bj])
                a[i][k] = a[k][i] = 1.0
                rhs[i] = 2.0 * dot(cols[bi], target)
            rhs[k] = 1.0
            try:
                sol = solve(a, rhs)
            except ValueError:
                continue
            if min(sol[:k]) < 0.0:
                continue
            w = [0.0] * len(cols)
            if k == 1:
                sol[0] = 1.0  # the only point of a one-bone simplex, without rounding
            for i, bi in enumerate(sup):
                w[bi] = sol[i]
            res = [-t for t in target]
            for b in sup:
                res = [x + w[b] * y for x, y in zip(res, cols[b])]
            e = dot(res, res)
            if e < best_e:
                best, best_e = w, e
    return best, best_e


def vertex_columns(v, bones, nframes):
    """Return, per bone, the stacked positions of v under the bone over all frames."""
    cols = []
    for bone in bones:
        col = []
        for f in range(nframes):
            col.extend(transform(bone[f], v))
        cols.append(col)
    return cols


def update_weights(rest, frames, weights, bones, k_max):
    """Return the new weights of every vertex (the weight step)."""
    nb = len(bones)
    out = []
    for i, v in enumerate(rest):
        cols = vertex_columns(v, bones, len(frames))
        target = [c for q in frames for c in q[i]]
        w, _ = simplex_lsq(cols, target, list(range(nb)))  # @line L3
        keep = sorted(range(nb), key=lambda b: -w[b])[:k_max]
        w, e = simplex_lsq(cols, target, sorted(keep))  # @line L4
        old = weights[i]
        res = [-t for t in target]
        for b in range(nb):
            if old[b] != 0.0:
                res = [x + old[b] * y for x, y in zip(res, cols[b])]
        if dot(res, res) < e:  # @line L5
            w = list(old)
        out.append(w)
    return out


def update_bone(rest, frames, weights, bones, b):
    """Return the new transforms of bone b for all frames, with the others fixed."""
    w = [weights[i][b] for i in range(len(rest))]
    new = []
    for f, q in enumerate(frames):
        targets = []
        for i, v in enumerate(rest):  # @line L6
            r = list(q[i])
            for c, wc in enumerate(weights[i]):
                if c != b and wc != 0.0:
                    p = transform(bones[c][f], v)
                    r[0] -= wc * p[0]
                    r[1] -= wc * p[1]
            targets.append(tuple(r))
        new.append(weighted_procrustes(rest, targets, w))  # @line L7
    return new


def kmeans(points, k, rng, iters=100):
    """Return the cluster index of each point (Lloyd's algorithm, k-means++ seeding)."""
    centers = [points[rng.randrange(len(points))]]
    while len(centers) < k:
        d = [min(sum((a - b) ** 2 for a, b in zip(p, c)) for c in centers) for p in points]
        r = rng.random() * sum(d)
        acc = 0.0
        for p, x in zip(points, d):
            acc += x
            if acc >= r:
                centers.append(p)
                break
    labels = None
    for _ in range(iters):
        new = [min(range(k), key=lambda j: sum((a - b) ** 2 for a, b in zip(p, centers[j]))) for p in points]
        if new == labels:
            break
        labels = new
        for j in range(k):
            members = [p for p, lab in zip(points, labels) if lab == j]
            if members:
                centers[j] = tuple(sum(c) / len(members) for c in zip(*members))
    return labels


def initialize(rest, frames, nbones, rng):
    """Return (weights, bones) from k-means on the trajectories and a rigid fit per cluster."""
    traj = [tuple(c for q in frames for c in q[i]) for i in range(len(rest))]
    labels = kmeans(traj, nbones, rng)
    weights = [[1.0 if labels[i] == b else 0.0 for b in range(nbones)] for i in range(len(rest))]
    bones = []
    for b in range(nbones):
        w = [weights[i][b] for i in range(len(rest))]
        bones.append([weighted_procrustes(rest, q, w) for q in frames])
    return weights, bones


def ssdr(rest, frames, nbones, k_max=2, iters=30, seed=0, tol=1e-12):
    """Return (weights, bones, errors), errors[0] being the error after initialization."""
    rng = random.Random(seed)
    weights, bones = initialize(rest, frames, nbones, rng)  # @line L1
    errors = [error(rest, frames, weights, bones)]
    for _ in range(iters):  # @line L2
        weights = update_weights(rest, frames, weights, bones, k_max)
        for b in range(nbones):
            bones[b] = update_bone(rest, frames, weights, bones, b)
        errors.append(error(rest, frames, weights, bones))
        if errors[-2] - errors[-1] <= tol * (1.0 + errors[-2]):  # @line L8
            break
    return weights, bones, errors  # @line L9
