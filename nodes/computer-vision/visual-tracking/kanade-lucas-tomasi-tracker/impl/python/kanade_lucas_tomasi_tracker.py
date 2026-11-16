# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kanade-lucas-tomasi-tracker/. The authors are listed in prov/GW9GYD.jsonl.

"""Kanade-Lucas-Tomasi feature tracker: Shi-Tomasi selection, pyramidal
Lucas-Kanade tracking in the form of Bouguet, and a forward-backward check.

Images are lists of rows of gray values, indexed img[v][u]: u is the column
(to the right) and v is the row (down). The center of pixel (u, v) is the
point (u, v). Off-grid values come from bilinear interpolation with the
indices clamped to the image. Level l of a pyramid has the pixel (u, v) at
the point (2^l u, 2^l v) of level 0.
"""

import math

LOST = None


def sample(img, u, v):
    """Bilinear sample at the real point (u, v), indices clamped."""
    h, w = len(img), len(img[0])
    u0, v0 = math.floor(u), math.floor(v)
    fu, fv = u - u0, v - v0

    def at(vv, uu):
        return img[min(max(vv, 0), h - 1)][min(max(uu, 0), w - 1)]

    top = (1 - fu) * at(v0, u0) + fu * at(v0, u0 + 1)
    bottom = (1 - fu) * at(v0 + 1, u0) + fu * at(v0 + 1, u0 + 1)
    return (1 - fv) * top + fv * bottom


def reduce_level(img):
    """Blur with the binomial filter (1, 4, 6, 4, 1) / 16 in both directions,
    then keep the pixels with even u and even v."""
    h, w = len(img), len(img[0])
    k = (1, 4, 6, 4, 1)
    tmp = [[sum(k[i + 2] * row[min(max(u + i, 0), w - 1)] for i in range(-2, 3)) / 16
            for u in range(w)] for row in img]
    return [[sum(k[i + 2] * tmp[min(max(v + i, 0), h - 1)][u] for i in range(-2, 3)) / 16
             for u in range(0, w, 2)] for v in range(0, h, 2)]


def pyramid(img, levels):
    """The list [level 0, ..., level levels] of a Gaussian pyramid."""
    pyr = [img]
    for _ in range(levels):
        pyr.append(reduce_level(pyr[-1]))
    return pyr


def min_eigenvalue(a, b, c):
    """The smaller eigenvalue of the symmetric matrix [[a, b], [b, c]]."""
    return (a + c - math.sqrt((a - c) ** 2 + 4 * b * b)) / 2


def corner_strength(img, r):
    """Map (u, v) -> smaller eigenvalue of the structure tensor of the
    (2r+1) x (2r+1) window, for every pixel whose window and gradients lie
    inside the image. Gradients are central differences."""
    h, w = len(img), len(img[0])
    gx = [[0.0] * w for _ in range(h)]
    gy = [[0.0] * w for _ in range(h)]
    for v in range(1, h - 1):
        for u in range(1, w - 1):
            gx[v][u] = (img[v][u + 1] - img[v][u - 1]) / 2
            gy[v][u] = (img[v + 1][u] - img[v - 1][u]) / 2
    lam = {}
    for v in range(r + 1, h - r - 1):
        for u in range(r + 1, w - r - 1):
            a = b = c = 0.0
            for y in range(v - r, v + r + 1):
                for x in range(u - r, u + r + 1):
                    a += gx[y][x] * gx[y][x]
                    b += gx[y][x] * gy[y][x]
                    c += gy[y][x] * gy[y][x]
            lam[(u, v)] = min_eigenvalue(a, b, c)  # @line L9
    return lam


def select_features(img, r=3, quality=0.05, min_dist=5.0, max_count=None):
    """Shi-Tomasi selection: pixels whose smaller eigenvalue is at least
    quality times the largest one, taken greedily in decreasing order and
    kept only when they are at least min_dist from every point kept before."""
    lam = corner_strength(img, r)
    if not lam:
        return []
    top = max(lam.values())
    cand = sorted((p for p in lam if lam[p] >= quality * top and lam[p] > 0),
                  key=lambda p: (-lam[p], p[1], p[0]))  # @line L10
    kept = []
    for p in cand:  # @line L11
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 >= min_dist * min_dist for q in kept):
            kept.append(p)
            if max_count is not None and len(kept) == max_count:
                break
    return [(float(u), float(v)) for u, v in kept]  # @line L12


def pyr_lk(ipyr, jpyr, p, r=3, iters=20, tol=0.01, lam_min=1e-6):
    """Track the point p of image I into image J, given their pyramids.
    Returns the displacement (du, dv) at level 0, or LOST when the window
    has too little texture at some level."""
    levels = len(ipyr) - 1
    g = (0.0, 0.0)  # @line L13
    for lev in range(levels, -1, -1):  # @line L14
        img, jmg = ipyr[lev], jpyr[lev]
        qu, qv = p[0] / 2 ** lev, p[1] / 2 ** lev  # @line L15
        win = []
        a = b = c = 0.0
        for j in range(-r, r + 1):
            for i in range(-r, r + 1):
                u, v = qu + i, qv + j
                ix = (sample(img, u + 1, v) - sample(img, u - 1, v)) / 2
                iy = (sample(img, u, v + 1) - sample(img, u, v - 1)) / 2
                win.append((u, v, ix, iy, sample(img, u, v)))
                a += ix * ix
                b += ix * iy
                c += iy * iy
        if min_eigenvalue(a, b, c) < lam_min:  # @line L16
            return LOST
        det = a * c - b * b
        nu = (0.0, 0.0)  # @line L17
        for _ in range(iters):  # @line L18
            bx = by = 0.0
            for u, v, ix, iy, ival in win:  # @line L19
                diff = ival - sample(jmg, u + g[0] + nu[0], v + g[1] + nu[1])
                bx += ix * diff
                by += iy * diff
            eta = ((c * bx - b * by) / det, (a * by - b * bx) / det)  # @line L20
            nu = (nu[0] + eta[0], nu[1] + eta[1])
            if math.hypot(eta[0], eta[1]) < tol:  # @line L21
                break
        if lev > 0:  # @line L22
            g = (2 * (g[0] + nu[0]), 2 * (g[1] + nu[1]))
        else:
            g = (g[0] + nu[0], g[1] + nu[1])
    return g  # @line L23


def klt_track(frames, levels=2, r=3, fb_max=0.5, quality=0.05, min_dist=5.0,
              max_count=None, iters=20, tol=0.01, lam_min=1e-6):
    """Select points in frames[0] and track them through the other frames.
    Returns one track per selected point: the list of its positions, which
    stops at the frame where the point is dropped."""
    pts = select_features(frames[0], r, quality, min_dist, max_count)  # @line L1
    tracks = [[p] for p in pts]
    alive = list(range(len(pts)))
    prev = pyramid(frames[0], levels)
    for t in range(1, len(frames)):  # @line L2
        cur = pyramid(frames[t], levels)
        still = []
        for k in alive:  # @line L3
            p = tracks[k][-1]
            d = pyr_lk(prev, cur, p, r, iters, tol, lam_min)  # @line L4
            if d is LOST:
                continue
            q = (p[0] + d[0], p[1] + d[1])
            back = pyr_lk(cur, prev, q, r, iters, tol, lam_min)  # @line L5
            if back is LOST or math.hypot(d[0] + back[0], d[1] + back[1]) > fb_max:  # @line L6
                continue
            tracks[k].append(q)  # @line L7
            still.append(k)
        alive = still
        prev = cur
    return tracks  # @line L8
