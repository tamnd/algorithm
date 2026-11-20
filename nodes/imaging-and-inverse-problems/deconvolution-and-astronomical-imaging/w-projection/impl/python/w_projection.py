# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/w-projection/. The authors are listed in prov/0A2NXG.jsonl.
"""W-projection on a small grid, with the exact sums to compare against.

The image is n x n, img[i][j]. Pixel (i, j) has the offsets a = i - n//2 and
b = j - n//2 and the direction cosines l = b dl, m = a dl, with
nn = sqrt(1 - l^2 - m^2). The uv cell is du = 1 / (n dl). A visibility is a
tuple (ku, kv, w, value, weight): it sits on the grid point u = ku du,
v = kv du, and w is any real number. The measurement equation is

    V = sum over pixels of x / nn * exp(-2 pi i (u l + v m + w (nn - 1))).

On this grid the equation is a DFT of y = x * G_w / nn with
G_w = exp(-2 pi i w (nn - 1)), so V_w = K_w (*) V_0 (circular convolution)
with the kernel K_w = DFT(G_w) / n^2. Cutting K_w to a small support is the
w-projection approximation. Kernels and grids are stored wrapped, with
offset 0 at index 0.
"""

import cmath
import math

from imgkit import dft2, idft2, ifftshift


def cosines(n, dl):
    """Lists (l, m, nn) per pixel, as three n x n images."""
    ls = [[(j - n // 2) * dl for j in range(n)] for _ in range(n)]
    ms = [[(i - n // 2) * dl for _ in range(n)] for i in range(n)]
    nns = [[math.sqrt(1.0 - l * l - m * m) for l, m in zip(rl, rm)] for rl, rm in zip(ls, ms)]
    return ls, ms, nns


def w_kernel(n, dl, w, support=None):
    """The kernel K_w as a dict {(qv, qu): value} over signed offsets.

    support = None keeps every offset; otherwise only |qv|, |qu| <= support.
    """
    _, _, nns = cosines(n, dl)
    g = [[cmath.exp(-2j * math.pi * w * (nn - 1.0)) for nn in row] for row in nns]  # @line L7
    full = dft2(ifftshift(g))  # @line L8
    lo, hi = -(n // 2), n - n // 2
    if support is not None:
        lo, hi = max(lo, -support), min(hi, support + 1)
    return {(qv, qu): full[qv % n][qu % n] / (n * n) for qv in range(lo, hi) for qu in range(lo, hi)}  # @line L9


def predict_direct(sky, vis, dl):
    """The exact model visibilities, by the sum over pixels."""
    n = len(sky)
    ls, ms, nns = cosines(n, dl)
    du = 1.0 / (n * dl)
    out = []
    for ku, kv, w, _, _ in vis:
        u, v = ku * du, kv * du
        acc = 0j
        for i in range(n):
            for j in range(n):
                if sky[i][j] != 0:
                    nn = nns[i][j]
                    acc += sky[i][j] / nn * cmath.exp(-2j * math.pi * (u * ls[i][j] + v * ms[i][j] + w * (nn - 1.0)))
        out.append(acc)
    return out


def image_direct(vis, n, dl):
    """The exact dirty image (1/W) sum_j weight_j Re(V_j conj(a_jp)), the adjoint of predict_direct."""
    ls, ms, nns = cosines(n, dl)
    du = 1.0 / (n * dl)
    total = sum(vis_j[4] for vis_j in vis)
    img = [[0.0] * n for _ in range(n)]
    for ku, kv, w, val, wt in vis:
        u, v = ku * du, kv * du
        for i in range(n):
            for j in range(n):
                nn = nns[i][j]
                a = cmath.exp(-2j * math.pi * (u * ls[i][j] + v * ms[i][j] + w * (nn - 1.0))) / nn
                img[i][j] += wt * (val * a.conjugate()).real / total
    return img


def _kernels(vis, n, dl, support):
    cache = {}
    for _, _, w, _, _ in vis:
        if w not in cache:
            cache[w] = w_kernel(n, dl, w, support)
    return cache


def w_project_image(vis, n, dl, support=None):
    """The dirty image by w-projection: grid each visibility through conj(K_w), one FFT, divide by nn."""
    kernels = _kernels(vis, n, dl, support)
    total = sum(vis_j[4] for vis_j in vis)
    grid = [[0j] * n for _ in range(n)]  # @line L1
    for ku, kv, w, val, wt in vis:  # @line L2
        kern = kernels[w]  # @line L3
        for (qv, qu), kq in kern.items():  # @line L4
            grid[(kv - qv) % n][(ku - qu) % n] += wt * kq.conjugate() * val
    img = idft2(grid)  # @line L5
    _, _, nns = cosines(n, dl)
    shifted = [[v * n * n for v in row] for row in img]
    # the grid index is wrapped; move offset 0 back to pixel n // 2
    back = [[shifted[(i - n // 2) % n][(j - n // 2) % n] for j in range(n)] for i in range(n)]
    return [[back[i][j].real / (total * nns[i][j]) for j in range(n)] for i in range(n)]  # @line L6


def w_project_predict(sky, vis, dl, support=None):
    """Model visibilities by w-projection: one FFT of x / nn, then each value through K_w."""
    n = len(sky)
    _, _, nns = cosines(n, dl)
    y = [[x / nn for x, nn in zip(rx, rn)] for rx, rn in zip(sky, nns)]
    v0 = dft2(ifftshift(y))
    kernels = _kernels(vis, n, dl, support)
    out = []
    for ku, kv, w, _, _ in vis:
        kern = kernels[w]
        out.append(sum(kq * v0[(kv - qv) % n][(ku - qu) % n] for (qv, qu), kq in kern.items()))
    return out
