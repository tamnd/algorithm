# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiscale-clean/. The authors are listed in prov/KXJYFX.jsonl.
"""Multiscale CLEAN on a periodic grid.

Images are lists of rows, img[i][j]; a 1D signal is a 1 x n image. Kernels
(the dirty beam, the scale functions) have their center at index (0, 0),
wrapped around. Scale 0 is the delta function, so plain Hogbom CLEAN is the
case of one scale.
"""

import math

from imgkit import dft2, idft2, new_image


def scale_function(n1, n2, size):
    """A unit-sum bump of radius size: 1 - (r / size)^2 for r < size, 0 outside.

    size = 0 gives the delta function at (0, 0). The bump is symmetric under
    (i, j) -> (-i, -j), which the proof needs.
    """
    out = new_image(n1, n2)
    if size <= 0:
        out[0][0] = 1.0
        return out
    for i in range(n1):
        di = min(i, n1 - i)
        for j in range(n2):
            dj = min(j, n2 - j)
            r2 = (di * di + dj * dj) / (size * size)
            if r2 < 1.0:
                out[i][j] = 1.0 - r2
    total = sum(sum(row) for row in out)
    return [[v / total for v in row] for row in out]


def conv_fft(*imgs):
    """The periodic convolution of several real images of the same size, by the DFT."""
    prod = dft2(imgs[0])
    for img in imgs[1:]:
        f = dft2(img)
        prod = [[a * b for a, b in zip(ra, rb)] for ra, rb in zip(prod, f)]
    return [[v.real for v in row] for row in idft2(prod)]


def multiscale_clean(dirty, beam, sizes, gain=0.1, threshold=0.0, max_iter=1000, bias=None):
    """Deconvolve a dirty image with components of several sizes.

    sizes lists the scale radii in pixels and must hold 0 (the delta scale).
    A step at scale s and pixel p lowers the misfit by (2g - g^2) I_s(p)^2 / B_ss(0),
    so the pick maximizes bias[s] |I_s(p)| / sqrt(B_ss(0)); with no bias it is the
    largest drop. Returns (model, residual, components, smoothed); components is
    a list of (scale index, i, j, flux), smoothed[s] = phi_s * residual.
    """
    if 0 not in sizes:
        raise ValueError("the scales must include the delta scale 0")
    n1, n2 = len(dirty), len(dirty[0])
    if bias is None:
        bias = [1.0] * len(sizes)
    if any(b <= 0 for b in bias):
        raise ValueError("the bias must be positive")
    phis = [scale_function(n1, n2, s) for s in sizes]
    ns = len(sizes)
    smoothed = [conv_fft(dirty, ph) for ph in phis]  # @line L1
    cross = [[conv_fft(phis[s], phis[t], beam) for t in range(ns)] for s in range(ns)]  # @line L2
    if any(cross[s][s][0][0] <= 0 for s in range(ns)):
        raise ValueError("a scale is not seen by the array")
    weight = [bias[s] / math.sqrt(cross[s][s][0][0]) for s in range(ns)]
    model = new_image(n1, n2)
    comps = []
    for _ in range(max_iter):  # @line L3
        best, pick = -1.0, None
        for s in range(ns):  # @line L4
            for i, row in enumerate(smoothed[s]):
                for j, v in enumerate(row):
                    if weight[s] * abs(v) > best:
                        best, pick = weight[s] * abs(v), (s, i, j)
        s, i0, j0 = pick
        peak = smoothed[s][i0][j0]
        if abs(peak) <= threshold:  # @line L5
            break
        c = gain * peak / cross[s][s][0][0]  # @line L6
        ph = phis[s]
        for i in range(n1):  # @line L7
            pi = ph[(i - i0) % n1]
            mi = model[i]
            for j in range(n2):
                mi[j] += c * pi[(j - j0) % n2]
        comps.append((s, i0, j0, c))
        for t in range(ns):  # @line L8
            bst = cross[s][t]
            img = smoothed[t]
            for i in range(n1):
                bi = bst[(i - i0) % n1]
                ri = img[i]
                for j in range(n2):
                    ri[j] -= c * bi[(j - j0) % n2]
    residual = [list(row) for row in smoothed[sizes.index(0)]]
    return model, residual, comps, smoothed  # @line L9


def scale_misfit(model, sky, weights):
    """Q(M) = (1/W) sum_k w_k |V_k - M^_k|^2, the misfit to the measured visibilities."""
    total = sum(sum(row) for row in weights)
    vs, vm = dft2(sky), dft2(model)
    acc = 0.0
    for rw, ra, rb in zip(weights, vs, vm):
        for w, a, b in zip(rw, ra, rb):
            acc += w * abs(a - b) ** 2
    return acc / total


def gaussian_blob(n1, n2, ci, cj, width, flux):
    """A periodic Gaussian of the given width (pixels) centered at (ci, cj), with the given total flux."""
    out = new_image(n1, n2)
    for i in range(n1):
        di = min(abs(i - ci), n1 - abs(i - ci))
        for j in range(n2):
            dj = min(abs(j - cj), n2 - abs(j - cj))
            out[i][j] = math.exp(-(di * di + dj * dj) / (2 * width * width))
    total = sum(sum(row) for row in out)
    return [[flux * v / total for v in row] for row in out]
