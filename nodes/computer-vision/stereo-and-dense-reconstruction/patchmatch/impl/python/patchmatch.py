# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/patchmatch/. The authors are listed in prov/2WYA23.jsonl.

"""PatchMatch (Barnes, Shechtman, Finkelstein and Goldman 2009).

Images are lists of rows of integers, indexed img[y][x]. A patch has radius r,
so it covers (2 r + 1)^2 pixels. Only patches that lie fully inside an image
are used: their centers are the pixels with r <= x < W - r and r <= y < H - r.
The nearest neighbor field f maps each patch center a of A to an offset
(dx, dy), so that a + f[a] is a patch center of B. The distance is the sum of
squared differences (SSD) of the two patches.
"""

import random

INF = float("inf")


def patch_distance(A, B, ax, ay, bx, by, r, limit=INF):
    """SSD between the patch of A at (ax, ay) and the patch of B at (bx, by).

    The sum stops early, and returns a value >= limit, as soon as it reaches limit.
    """
    total = 0
    for j in range(-r, r + 1):
        ra = A[ay + j]
        rb = B[by + j]
        for i in range(-r, r + 1):
            e = ra[ax + i] - rb[bx + i]
            total += e * e
        if total >= limit:
            return total
    return total


def _centers(img, r):
    h, w = len(img), len(img[0])
    return r, w - r - 1, r, h - r - 1  # x range and y range, inclusive


def patchmatch(A, B, r, iters, rng, init=None, search=True, history=None):
    """Return (f, D): the offset field and the patch distances, as dicts keyed by (x, y).

    rng is a random.Random. init, if given, is a starting offset field (a dict).
    search=False turns off the random search (used to test propagation alone).
    history, if a list, gets a copy of D after the initialization and after each iteration.
    """
    ax0, ax1, ay0, ay1 = _centers(A, r)
    bx0, bx1, by0, by1 = _centers(B, r)
    if ax0 > ax1 or ay0 > ay1 or bx0 > bx1 or by0 > by1:
        raise ValueError("an image is smaller than one patch")
    w = max(len(B), len(B[0]))
    f = {}
    D = {}
    for y in range(ay0, ay1 + 1):
        for x in range(ax0, ax1 + 1):
            if init is not None:
                dx, dy = init[(x, y)]
            else:
                dx, dy = rng.randint(bx0, bx1) - x, rng.randint(by0, by1) - y
            f[(x, y)] = (dx, dy)  # @line L1
            D[(x, y)] = patch_distance(A, B, x, y, x + dx, y + dy, r)
    if history is not None:
        history.append(dict(D))
    rows = list(range(ay0, ay1 + 1))
    cols = list(range(ax0, ax1 + 1))
    for k in range(1, iters + 1):  # @line L2
        if k % 2 == 1:  # @line L3
            ys, xs, step = rows, cols, -1
        else:
            ys, xs, step = rows[::-1], cols[::-1], 1
        for y in ys:
            for x in xs:  # @line L4
                a = (x, y)
                for n in ((x + step, y), (x, y + step)):  # @line L5
                    if n not in f:
                        continue
                    dx, dy = f[n]
                    bx, by = x + dx, y + dy
                    if bx0 <= bx <= bx1 and by0 <= by <= by1:  # @line L6
                        d = patch_distance(A, B, x, y, bx, by, r, D[a])
                        if d < D[a]:
                            f[a], D[a] = (dx, dy), d
                if not search:
                    continue
                vx, vy = x + f[a][0], y + f[a][1]  # @line L7
                rad = w  # @line L8
                while rad >= 1:  # @line L9
                    bx = rng.randint(max(vx - rad, bx0), min(vx + rad, bx1))  # @line L10
                    by = rng.randint(max(vy - rad, by0), min(vy + rad, by1))
                    d = patch_distance(A, B, x, y, bx, by, r, D[a])
                    if d < D[a]:  # @line L11
                        f[a], D[a] = (bx - x, by - y), d
                    rad //= 2  # @line L12
        if history is not None:
            history.append(dict(D))
    return f, D  # @line L13


def nnf_brute_force(A, B, r):
    """Exact nearest neighbor distances by trying every patch of B, for the tests."""
    ax0, ax1, ay0, ay1 = _centers(A, r)
    bx0, bx1, by0, by1 = _centers(B, r)
    best = {}
    for y in range(ay0, ay1 + 1):
        for x in range(ax0, ax1 + 1):
            m = INF
            for by in range(by0, by1 + 1):
                for bx in range(bx0, bx1 + 1):
                    m = min(m, patch_distance(A, B, x, y, bx, by, r, m))
            best[(x, y)] = m
    return best


def random_image(rng, w, h, levels=256):
    return [[rng.randrange(levels) for _ in range(w)] for _ in range(h)]


if __name__ == "__main__":
    rng = random.Random(1)
    B = random_image(rng, 20, 16)
    A = [row[3:15] for row in B[2:12]]
    f, D = patchmatch(A, B, 2, 5, random.Random(2))
    print(sum(1 for v in f.values() if v == (3, 2)), len(f))
