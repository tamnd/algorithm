# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cotton-schwab-clean/. The authors are listed in prov/R1NZQT.jsonl.
"""Cotton-Schwab CLEAN with exact major cycles.

The image is n x n, img[i][j], row i from the top. Pixel (i, j) sits at the
direction cosines l = (j - n/2) dl and m = (n/2 - i) dl. A visibility is a
tuple (u, v, w, V) with weight w > 0, and the measurement equation is exact:

    V = sum over pixels of x[i][j] exp(-2 pi i (u l + v m)).

The dirty image is (1/W) sum w Re(V exp(2 pi i (u l + v m))), W = sum w. The
beam is stored as a dict from pixel offsets (di, dj) to values; the dirty
image is exactly the (non-periodic) convolution of the sky with it. The minor
cycle subtracts only a patch of the beam, so its residual drifts; each major
cycle recomputes the residual from the visibilities, which removes the drift.
"""

import cmath
import math


def predict(model, vis, dl):
    """Model visibilities: sum_p M_p exp(-2 pi i (u l_p + v m_p)) for each (u, v) of vis."""
    n = len(model)
    comps = [((j - n / 2) * dl, (n / 2 - i) * dl, model[i][j]) for i in range(n) for j in range(n) if model[i][j] != 0]
    out = []
    for u, v, _, _ in vis:
        out.append(sum(f * cmath.exp(-2j * math.pi * (u * l + v * m)) for l, m, f in comps))
    return out


def dirty_from(vis, values, n, dl):
    """The dirty image (1/W) sum_j w_j Re(values_j exp(2 pi i (u_j l + v_j m)))."""
    total = sum(w for _, _, w, _ in vis)
    img = [[0.0] * n for _ in range(n)]
    for (u, v, w, _), val in zip(vis, values):
        if w == 0:
            continue
        eu = [cmath.exp(2j * math.pi * u * (j - n / 2) * dl) for j in range(n)]
        for i in range(n):
            ev = cmath.exp(2j * math.pi * v * (n / 2 - i) * dl) * val * w / total
            row = img[i]
            for j in range(n):
                row[j] += (ev * eu[j]).real
    return img


def dirty_beam(vis, n, dl):
    """The beam B(di, dj) = (1/W) sum w cos(2 pi (u dj dl - v di dl)) for |di|, |dj| < n."""
    total = sum(w for _, _, w, _ in vis)
    beam = {}
    for di in range(-(n - 1), n):
        for dj in range(-(n - 1), n):
            beam[(di, dj)] = sum(w * math.cos(2 * math.pi * (u * dj - v * di) * dl) for u, v, w, _ in vis) / total
    return beam


def misfit(vis, model, dl):
    """Q(M) = (1/W) sum w |V - (A M)|^2, the misfit to the measured visibilities."""
    total = sum(w for _, _, w, _ in vis)
    pred = predict(model, vis, dl)
    return sum(w * abs(val - p) ** 2 for (_, _, w, val), p in zip(vis, pred)) / total


def minor_cycle(r, model, beam, patch, gain, limit, max_iter):
    """Hogbom steps on the image r with the beam cut to |di|, |dj| <= patch, until max |r| <= limit."""
    n = len(r)
    b0 = beam[(0, 0)]
    steps = 0
    while steps < max_iter:
        i0, j0 = max(((i, j) for i in range(n) for j in range(n)), key=lambda p: abs(r[p[0]][p[1]]))
        peak = r[i0][j0]
        if abs(peak) <= limit:
            break
        c = gain * peak / b0
        model[i0][j0] += c
        for i in range(max(0, i0 - patch), min(n, i0 + patch + 1)):
            for j in range(max(0, j0 - patch), min(n, j0 + patch + 1)):
                r[i][j] -= c * beam[(i - i0, j - j0)]
        steps += 1
    return steps


def outside_sidelobe(beam, patch):
    """The largest |B| outside the patch |di|, |dj| <= patch (0 when the patch holds the whole beam)."""
    return max((abs(b) for (di, dj), b in beam.items() if max(abs(di), abs(dj)) > patch), default=0.0)


def cotton_schwab_clean(vis, n, dl, patch, gain=0.1, threshold=0.0, cycle_factor=None, max_major=10, max_minor=500):
    """Deconvolve visibilities. Returns (model, residual image, number of major cycles, minor steps per cycle).

    A minor cycle stops when its peak falls to cycle_factor times the peak at the
    start of the cycle; by default the factor is the largest beam value outside
    the patch, as in Clark's rule. The residual image returned is exact: it is
    computed from V - A M.
    """
    beam = dirty_beam(vis, n, dl)
    if cycle_factor is None:
        cycle_factor = outside_sidelobe(beam, patch)
    model = [[0.0] * n for _ in range(n)]  # @line L1
    data = [val for _, _, _, val in vis]
    res_vis = list(data)
    steps = []
    for _ in range(max_major):  # @line L2
        r = dirty_from(vis, res_vis, n, dl)  # @line L3
        peak = max(abs(x) for row in r for x in row)
        if peak <= threshold:  # @line L4
            break
        limit = max(threshold, cycle_factor * peak)  # @line L5
        steps.append(minor_cycle(r, model, beam, patch, gain, limit, max_minor))  # @line L6
        pred = predict(model, vis, dl)  # @line L7
        res_vis = [d - p for d, p in zip(data, pred)]
    r = dirty_from(vis, res_vis, n, dl)  # @line L8
    return model, r, len(steps), steps
