# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plane-sweep-stereo/. The authors are listed in prov/8EH0Z3.jsonl.

"""Plane sweep stereo with plane-induced homographies.

Coordinates are those of the reference camera 0: K_0 [I | 0]. Camera k maps a
point X of the reference frame to X_k = R_k X + t_k and has intrinsics K_k.
A sweep plane is n^T X = d with a unit normal n and d > 0. Images are lists of
rows of gray values, indexed img[v][u].
"""

from cvla import inv, matvec, mul

INF = float("inf")


def plane_homography(K0, Kk, R, t, n, d):
    """H = K_k (R + t n^T / d) K_0^-1, which maps reference pixels on the plane n^T X = d to camera k."""
    A = [[R[i][j] + t[i] * n[j] / d for j in range(3)] for i in range(3)]
    return mul(mul(Kk, A), inv(K0))


def bilinear(img, u, v):
    """Bilinear sample at (u, v), or None outside [0, W-1] x [0, H-1]."""
    h, w = len(img), len(img[0])
    if not (0.0 <= u <= w - 1 and 0.0 <= v <= h - 1):
        return None
    i, j = min(int(u), w - 2), min(int(v), h - 2)
    a, b = u - i, v - j
    r0, r1 = img[j], img[j + 1]
    return ((1 - a) * (1 - b) * r0[i] + a * (1 - b) * r0[i + 1]
            + (1 - a) * b * r1[i] + a * b * r1[i + 1])


def pixel_costs(images, cams, n, d, miss):
    """Mean absolute difference between the reference and the warped images, per pixel.

    cams[k] = (K_k, R_k, t_k) for k >= 1; cams[0] holds K_0. A pixel that no
    other camera sees on this plane gets the cost miss.
    """
    ref = images[0]
    h, w = len(ref), len(ref[0])
    K0 = cams[0][0]
    Hs = [plane_homography(K0, cams[k][0], cams[k][1], cams[k][2], n, d)  # @line L3
          for k in range(1, len(images))]
    e = [[miss] * w for _ in range(h)]
    for v in range(h):
        for u in range(w):  # @line L4
            total, count = 0.0, 0
            for k, H in enumerate(Hs, start=1):
                x = matvec(H, [u, v, 1.0])
                if x[2] <= 0.0:
                    continue
                s = bilinear(images[k], x[0] / x[2], x[1] / x[2])
                if s is not None:
                    total += abs(ref[v][u] - s)
                    count += 1
            if count:
                e[v][u] = total / count  # @line L5
    return e


def box_sum(e, r):
    """Sum of e over the (2r+1) x (2r+1) window, cut at the image border, by an integral image."""
    h, w = len(e), len(e[0])
    S = [[0.0] * (w + 1) for _ in range(h + 1)]
    for v in range(h):
        acc = 0.0
        for u in range(w):
            acc += e[v][u]
            S[v + 1][u + 1] = S[v][u + 1] + acc
    out = [[0.0] * w for _ in range(h)]
    for v in range(h):
        v0, v1 = max(v - r, 0), min(v + r + 1, h)
        for u in range(w):
            u0, u1 = max(u - r, 0), min(u + r + 1, w)
            out[v][u] = S[v1][u1] - S[v0][u1] - S[v1][u0] + S[v0][u0]
    return out


def plane_sweep(images, cams, n, ds, r, miss=255.0):
    """Return (index, depth): the winning plane index and the depth Z per reference pixel.

    ds is the list of plane offsets d (the planes n^T X = d). Ties go to the
    first plane in the list.
    """
    ref = images[0]
    h, w = len(ref), len(ref[0])
    Kinv = inv(cams[0][0])
    best = [[INF] * w for _ in range(h)]  # @line L1
    index = [[-1] * w for _ in range(h)]
    for j, d in enumerate(ds):  # @line L2
        S = box_sum(pixel_costs(images, cams, n, d, miss), r)  # @line L6
        for v in range(h):
            for u in range(w):  # @line L7
                if S[v][u] < best[v][u]:  # @line L8
                    best[v][u] = S[v][u]
                    index[v][u] = j
    depth = [[0.0] * w for _ in range(h)]
    for v in range(h):
        for u in range(w):
            ray = matvec(Kinv, [u, v, 1.0])
            depth[v][u] = ds[index[v][u]] / sum(a * b for a, b in zip(n, ray))  # @line L9
    return index, depth  # @line L10


def inverse_depth_planes(z_near, z_far, f, b):
    """Fronto-parallel plane depths from z_near to z_far, spaced so that the
    disparity f b / Z changes by at most one pixel from one plane to the next."""
    q_near, q_far = 1.0 / z_near, 1.0 / z_far
    step = 1.0 / (f * b)
    count = int((q_near - q_far) / step) + 1
    if (q_near - q_far) / step > count - 1:
        count += 1
    return [1.0 / (q_near - (q_near - q_far) * i / (count - 1)) for i in range(count)]


if __name__ == "__main__":
    zs = inverse_depth_planes(1.0, 10.0, 500.0, 0.1)
    print(len(zs), zs[:3], zs[-1])
