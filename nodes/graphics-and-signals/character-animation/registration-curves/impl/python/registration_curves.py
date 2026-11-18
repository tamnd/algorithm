# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/registration-curves/. The authors are listed in prov/2DMA1Q.jsonl.
"""Registration curves (Kovar and Gleicher 2003) for two motions.

A motion is a list of frames; a frame is a point cloud, the world positions
(x, y, z) of its joints with y up. The registration of motion A (n frames)
and motion B (m frames) has two parts that this file computes:

  * the time warp: a path of frame pairs (i, j) from (0, 0) to
    (n - 1, m - 1), found by dynamic time warping of the frame distance
    matrix. Each step is (1, 0), (0, 1) or (1, 1), and at most L steps in a
    row go in the same non-diagonal direction (the slope limit). So the path
    is monotone in both i and j, and its slope stays in [1/L, L] over any
    L + 1 steps;
  * the alignment curve: for each pair on the path, the 2D rigid transform
    (rotation about y and translation in the ground plane) that best aligns
    frame j of B to frame i of A, with the angle unwrapped along the path.

blend() then plays the path with weight w on A: the blended frame for path
pair (i, j) is w A_i + (1 - w) T(B_j), and its time is
w i + (1 - w) j, which never decreases along the path.
"""

import math


def align_2d(P, Q):
    n = len(P)
    xb = sum(p[0] for p in P) / n
    zb = sum(p[2] for p in P) / n
    xb2 = sum(q[0] for q in Q) / n
    zb2 = sum(q[2] for q in Q) / n
    s = sum(p[0] * q[2] - q[0] * p[2] for p, q in zip(P, Q)) / n - (xb * zb2 - xb2 * zb)
    c = sum(p[0] * q[0] + p[2] * q[2] for p, q in zip(P, Q)) / n - (xb * xb2 + zb * zb2)
    t = math.atan2(s, c)
    x0 = xb - xb2 * math.cos(t) - zb2 * math.sin(t)
    z0 = zb + xb2 * math.sin(t) - zb2 * math.cos(t)
    return t, x0, z0


def transform(q, t, x0, z0):
    ct, st = math.cos(t), math.sin(t)
    return (q[0] * ct + q[2] * st + x0, q[1], -q[0] * st + q[2] * ct + z0)


def frame_distance(P, Q):
    t, x0, z0 = align_2d(P, Q)
    s = 0.0
    for p, q in zip(P, Q):
        r = transform(q, t, x0, z0)
        s += (p[0] - r[0]) ** 2 + (p[1] - r[1]) ** 2 + (p[2] - r[2]) ** 2
    return s / len(P)


def distance_grid(A, B):
    return [[frame_distance(a, b) for b in B] for a in A]


STEPS = ((1, 1), (1, 0), (0, 1))  # diagonal, along i, along j


def time_warp(D, L):
    """Minimum cost path through D with the slope limit L >= 1.

    The state is (i, j, s, r): s is the kind of the last step (0 diagonal,
    1 along i, 2 along j) and r the number of such steps in a row. A step
    of kind 1 or 2 is allowed only if it does not make r exceed L.
    Return (cost, path).
    """
    n, m = len(D), len(D[0])
    INF = math.inf
    best = {}
    best[(0, 0, 0, 0)] = (D[0][0], None)  # @line L1
    for i in range(n):  # @line L2
        for j in range(m):
            for s in range(3):
                for r in range(L + 1):
                    key = (i, j, s, r)
                    if key not in best:
                        continue
                    c = best[key][0]
                    for k, (di, dj) in enumerate(STEPS):  # @line L3
                        a, b = i + di, j + dj
                        if a >= n or b >= m:
                            continue
                        if k == 0:
                            nr = 0
                        elif k == s:
                            nr = r + 1
                        else:
                            nr = 1
                        if nr > L:  # @line L4
                            continue
                        nk = (a, b, k, nr)
                        nc = c + D[a][b]  # @line L5
                        if nc < best.get(nk, (INF,))[0]:
                            best[nk] = (nc, key)
    ends = [k for k in best if k[0] == n - 1 and k[1] == m - 1]
    if not ends:
        raise ValueError("no path satisfies the slope limit")
    end = min(ends, key=lambda k: best[k][0])  # @line L6
    path = []
    k = end
    while k is not None:
        path.append((k[0], k[1]))
        k = best[k][1]
    path.reverse()  # @line L7
    return best[end][0], path


def alignment_curve(A, B, path):
    """The transform of each path pair, with the angle unwrapped."""
    out = []
    prev = None
    for i, j in path:
        t, x0, z0 = align_2d(A[i], B[j])
        if prev is not None:
            while t - prev > math.pi:
                t -= 2 * math.pi
            while t - prev < -math.pi:
                t += 2 * math.pi
        out.append((t, x0, z0))  # @line L8
        prev = t
    return out


def register(A, B, L=2):
    D = distance_grid(A, B)
    cost, path = time_warp(D, L)
    return {"cost": cost, "path": path, "align": alignment_curve(A, B, path), "D": D}


def blend(A, B, reg, w):
    """Blended frames and their times along the path, weight w on A."""
    frames, times = [], []
    for (i, j), (t, x0, z0) in zip(reg["path"], reg["align"]):
        fb = [transform(q, t, x0, z0) for q in B[j]]
        frames.append([tuple(w * a + (1 - w) * b for a, b in zip(pa, pb))
                       for pa, pb in zip(A[i], fb)])
        times.append(w * i + (1 - w) * j)
    return frames, times
