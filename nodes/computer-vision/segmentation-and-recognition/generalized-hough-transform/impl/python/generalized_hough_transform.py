# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-hough-transform/. The authors are listed in prov/GZ6ZY6.jsonl.
"""The generalized Hough transform of Ballard (1981) for a shape given by a template image.

An image is a list of rows, img[v][u], with u the column (to the right) and v
the row (down). Edge points come from the Sobel gradient: a pixel is an edge
point when gx^2 + gy^2 >= t^2. The gradient direction phi = atan2(gy, gx) is
put into one of B bins centered at the multiples of 2 pi / B. For B = 8 the
bin edges are at 22.5 + 45 j degrees; integer gradients never lie exactly on
them, since tan(22.5 degrees) is irrational.

R-table: for each template edge point x with bin b, store r = c - x in R[b],
where c is the reference point. Detection: each image edge point y with bin b
votes at y + r for every r in R[b]. A copy of the template moved by t gives
at least m votes at c + t, where m is the number of template edge points.
The rotation extension rotates r and shifts the bin; it is exact for 90 degree
steps. Standard library only. Cost: O(e m_max) votes for e image edge
points and at most m_max entries per bin.
"""

import math


def sobel(img):
    """Sobel gradients (gx along u, gy along v); 0 on the one-pixel border."""
    H, W = len(img), len(img[0])
    gx = [[0] * W for _ in range(H)]
    gy = [[0] * W for _ in range(H)]
    for v in range(1, H - 1):
        a, b, c = img[v - 1], img[v], img[v + 1]
        for u in range(1, W - 1):
            gx[v][u] = (a[u + 1] + 2 * b[u + 1] + c[u + 1]) - (a[u - 1] + 2 * b[u - 1] + c[u - 1])
            gy[v][u] = (c[u - 1] + 2 * c[u] + c[u + 1]) - (a[u - 1] + 2 * a[u] + a[u + 1])
    return gx, gy


def direction_bin(gx, gy, B=8):
    """Bin of the gradient direction: round(phi / (2 pi / B)) mod B."""
    phi = math.atan2(gy, gx)
    return int(math.floor(phi / (2.0 * math.pi / B) + 0.5)) % B


def edge_points(img, threshold, B=8):
    """List of (u, v, bin) for the pixels whose gradient magnitude is at least the threshold."""
    gx, gy = sobel(img)
    t2 = threshold * threshold
    out = []
    for v in range(len(img)):
        for u in range(len(img[0])):
            x, y = gx[v][u], gy[v][u]
            if x * x + y * y >= t2 and (x != 0 or y != 0):
                out.append((u, v, direction_bin(x, y, B)))
    return out


def build_r_table(template_edges, ref, B=8):
    """R[b] = list of offsets ref - x for the template edge points x in bin b."""
    R = [[] for _ in range(B)]
    for u, v, b in template_edges:  # @line L1
        R[b].append((ref[0] - u, ref[1] - v))  # @line L2
    return R


def vote(edges, R, W, H):
    """Accumulator A[v][u] of size H x W: the votes of the image edge points."""
    A = [[0] * W for _ in range(H)]  # @line L3
    for u, v, b in edges:  # @line L4
        for du, dv in R[b]:  # @line L5
            cu, cv = u + du, v + dv  # @line L6
            if 0 <= cu < W and 0 <= cv < H:
                A[cv][cu] += 1  # @line L7
    return A


def peak(A):
    """(votes, u, v) of the largest cell; ties go to the smallest v, then the smallest u."""
    best = (-1, 0, 0)
    for v, row in enumerate(A):
        for u, a in enumerate(row):
            if a > best[0]:
                best = (a, u, v)
    return best  # @line L8


def detect(img, R, threshold, B=8):
    """Edge points of img, votes, and the peak (votes, u, v)."""
    A = vote(edge_points(img, threshold, B), R, len(img[0]), len(img))
    return peak(A), A


def rotate_offset(r, steps, B):
    """Rotate (du, dv) by steps * 2 pi / B, rounded to integers (exact for 90 degree steps)."""
    a = steps * 2.0 * math.pi / B
    c, s = math.cos(a), math.sin(a)
    du, dv = r
    return (int(round(c * du - s * dv)), int(round(s * du + c * dv)))


def vote_rotations(edges, R, W, H, B=8, steps=None, scales=(1.0,)):
    """Votes over (rotation step, scale, v, u): the 4D accumulator of the extension.

    An edge point with bin b, under the rotation by k steps, reads R[(b - k) mod B]
    and votes at y + s * rot_k(r). Returns {(k, s): accumulator}.
    """
    steps = range(B) if steps is None else steps
    out = {}
    for k in steps:
        for s in scales:
            rows = []
            for b in range(B):
                rb = R[(b - k) % B]
                rows.append([rotate_offset((s * du, s * dv), k, B) for du, dv in rb])
            out[(k, s)] = vote(edges, rows, W, H)
    return out


def rotate90(img):
    """Rotate the image content by +90 degrees in the (u, v) frame: (u, v) -> (H - 1 - v, u)."""
    H, W = len(img), len(img[0])
    out = [[0] * H for _ in range(W)]
    for v in range(H):
        for u in range(W):
            out[u][H - 1 - v] = img[v][u]
    return out


def paste(canvas, img, du, dv):
    """Copy img into canvas with its top left pixel at (du, dv)."""
    for v, row in enumerate(img):
        for u, val in enumerate(row):
            canvas[dv + v][du + u] = val
    return canvas
