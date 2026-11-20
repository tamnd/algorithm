# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hogbom-clean/. The authors are listed in prov/0ZFP8H.jsonl.
"""Hogbom CLEAN on a periodic grid.

Images are lists of rows, img[i][j]. A 1D signal is a 1 x n image. The dirty
beam has the same size as the image and its center at index (0, 0), wrapped
around, so a beam that is a delta at (0, 0) gives the identity. On this grid
the dirty image is exactly the periodic convolution of the sky with the
dirty beam, when both come from the same gridded uv weights.
"""

import math

from imgkit import circ_conv2, dft2, idft2, new_image


def dirty_beam(weights):
    """The dirty beam of gridded uv weights w[k][l] >= 0, scaled to peak 1.

    The weights must be symmetric, w[-k][-l] = w[k][l], so that the beam is real.
    """
    total = sum(sum(row) for row in weights)
    b = idft2(weights)
    n1, n2 = len(weights), len(weights[0])
    s = n1 * n2 / total
    return [[(v * s).real for v in row] for row in b]


def dirty_image(sky, weights):
    """The dirty image of a sky: the inverse DFT of the weighted visibilities, scaled like the beam."""
    total = sum(sum(row) for row in weights)
    vis = dft2(sky)
    n1, n2 = len(sky), len(sky[0])
    s = n1 * n2 / total
    prod = [[w * v for w, v in zip(rw, rv)] for rw, rv in zip(weights, vis)]
    return [[(v * s).real for v in row] for row in idft2(prod)]


def data_misfit(model, sky, weights):
    """Q(M) = (1/W) sum_k w_k |V_k - M^_k|^2 with V = DFT(sky); CLEAN does not increase it for 0 < gain < 2."""
    total = sum(sum(row) for row in weights)
    vs, vm = dft2(sky), dft2(model)
    acc = 0.0
    for rw, ra, rb in zip(weights, vs, vm):
        for w, a, b in zip(rw, ra, rb):
            acc += w * abs(a - b) ** 2
    return acc / total


def find_peak(r, positive_only=False, window=None):
    """The position (i, j) of the largest |r| (or largest r), inside the window mask if one is given."""
    best, pos = -math.inf, None
    for i, row in enumerate(r):
        for j, v in enumerate(row):
            if window is not None and not window[i][j]:
                continue
            key = v if positive_only else abs(v)
            if key > best:
                best, pos = key, (i, j)
    return pos


def hogbom_clean(dirty, beam, gain=0.1, threshold=0.0, max_iter=1000, positive_only=False, window=None):
    """Deconvolve a dirty image with Hogbom CLEAN.

    Returns (model, residual, components); components is the list of
    (i, j, flux) in the order they were found. The invariant
    residual = dirty - beam * model (periodic convolution) holds after each step.
    """
    n1, n2 = len(dirty), len(dirty[0])
    b0 = beam[0][0]
    if b0 <= 0:
        raise ValueError("the beam peak must be positive")
    r = [list(row) for row in dirty]  # @line L1
    model = new_image(n1, n2)
    comps = []
    for _ in range(max_iter):  # @line L2
        p = find_peak(r, positive_only, window)  # @line L3
        if p is None:
            break
        i0, j0 = p
        peak = r[i0][j0]
        if abs(peak) <= threshold or (positive_only and peak <= 0):  # @line L4
            break
        c = gain * peak / b0  # @line L5
        model[i0][j0] += c  # @line L6
        comps.append((i0, j0, c))
        for i in range(n1):  # @line L7
            bi = beam[(i - i0) % n1]
            ri = r[i]
            for j in range(n2):
                ri[j] -= c * bi[(j - j0) % n2]
    return model, r, comps  # @line L8


def fit_clean_beam(beam):
    """An axis-aligned Gaussian clean beam, peak 1 at (0, 0), matched to the main lobe of the dirty beam.

    The widths come from the beam values next to the peak: b(1, 0) / b(0, 0) = exp(-1 / (2 s1^2))
    and the same for the other axis.
    """
    n1, n2 = len(beam), len(beam[0])
    b0 = beam[0][0]

    def width(nb):
        ratio = nb / b0
        if not 0.0 < ratio < 1.0:
            raise ValueError("the main lobe is not resolved by the grid")
        return math.sqrt(-1.0 / (2.0 * math.log(ratio)))

    s1 = width(0.5 * (beam[1 % n1][0] + beam[-1 % n1][0])) if n1 > 1 else None
    s2 = width(0.5 * (beam[0][1 % n2] + beam[0][-1 % n2])) if n2 > 1 else None
    out = new_image(n1, n2)
    for i in range(n1):
        di = min(i, n1 - i)
        for j in range(n2):
            dj = min(j, n2 - j)
            e = 0.0
            if s1:
                e += di * di / (2 * s1 * s1)
            elif di:
                continue
            if s2:
                e += dj * dj / (2 * s2 * s2)
            elif dj:
                continue
            out[i][j] = math.exp(-e)
    return out


def restore(model, residual, clean_beam):
    """The restored image: the model convolved with the clean beam, plus the residual."""
    smooth = circ_conv2(model, clean_beam)  # @line L9
    return [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(smooth, residual)]
