# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parks-mcclellan-algorithm/. The authors are listed in prov/6A2CCM.jsonl.

"""The Parks-McClellan algorithm for a type 1 linear phase low-pass FIR filter.

Frequencies are in radians per sample. The filter has N = 2L + 1 taps and the
amplitude A(w) = sum_(k=0..L) a_k cos(k w). The pass band is [0, wp] with
desired value 1 and weight 1; the stop band is [ws, pi] with desired value 0
and weight K. The algorithm minimizes max over both bands of
|W(w) (D(w) - A(w))| on a dense grid, by the Remez exchange.
"""

import math
from typing import NamedTuple


class Design(NamedTuple):
    h: list[float]  # the N = 2L + 1 coefficients, h[n] = h[N - 1 - n]
    delta: float  # the levelled error of the last reference set, with its sign
    extremals: list[float]  # the L + 2 reference frequencies of the last step
    iterations: int


def make_grid(taps: int, wp: float, ws: float, stop_weight: float, density: int):
    """Return the grid frequencies with their desired values, weights and band numbers."""
    half = (taps - 1) // 2
    total = density * (half + 1)
    width = wp + (math.pi - ws)
    n1 = max(2, round(total * wp / width))
    n2 = max(2, round(total * (math.pi - ws) / width))
    w = [wp * i / (n1 - 1) for i in range(n1)] + [ws + (math.pi - ws) * i / (n2 - 1) for i in range(n2)]
    d = [1.0] * n1 + [0.0] * n2
    wt = [1.0] * n1 + [stop_weight] * n2
    band = [0] * n1 + [1] * n2
    return w, d, wt, band


def _bary_weights(xs: list[float]) -> list[float]:
    out = []
    for k, xk in enumerate(xs):
        p = 1.0
        for i, xi in enumerate(xs):
            if i != k:
                p *= xk - xi
        out.append(1.0 / p)
    return out


def _interpolant(xs: list[float], cs: list[float]):
    """The polynomial of degree len(xs) - 1 in x = cos(w) through (xs, cs), in barycentric form."""
    bw = _bary_weights(xs)

    def value(x: float) -> float:
        num = den = 0.0
        for xk, ck, bk in zip(xs, cs, bw):
            diff = x - xk
            if diff == 0.0:
                return ck
            t = bk / diff
            num += t * ck
            den += t
        return num / den

    return value


def _extrema(err: list[float], band: list[int]) -> list[int]:
    """Indices of the local extrema of the signed error, with band edges as end points."""
    out = []
    n = len(err)
    for j in range(n):
        e = err[j]
        if e == 0.0:
            continue
        left = err[j - 1] if j > 0 and band[j - 1] == band[j] else None
        right = err[j + 1] if j + 1 < n and band[j + 1] == band[j] else None
        if e > 0 and (left is None or e >= left) and (right is None or e >= right):
            out.append(j)
        elif e < 0 and (left is None or e <= left) and (right is None or e <= right):
            out.append(j)
    return out


def parks_mcclellan_lowpass(taps: int, wp: float, ws: float, stop_weight: float = 1.0,
                            density: int = 16, max_iter: int = 100) -> Design:
    if taps < 3 or taps % 2 == 0:
        raise ValueError("this version designs type 1 filters: taps must be odd and at least 3")
    if not 0 < wp < ws < math.pi:
        raise ValueError("need 0 < wp < ws < pi")
    half = (taps - 1) // 2
    r = half + 2
    grid, d, wt, band = make_grid(taps, wp, ws, stop_weight, density)
    g = len(grid)
    ext = [round(i * (g - 1) / (r - 1)) for i in range(r)]  # @line L1
    delta = 0.0
    a_of_x = None
    it = 0
    for it in range(1, max_iter + 1):  # @line L2
        x = [math.cos(grid[j]) for j in ext]
        bw = _bary_weights(x)
        num = sum(bw[k] * d[ext[k]] for k in range(r))
        den = sum(bw[k] * (-1) ** k / wt[ext[k]] for k in range(r))
        delta = num / den  # @line L3: the levelled error on the reference set
        cs = [d[ext[k]] - (-1) ** k * delta / wt[ext[k]] for k in range(r)]
        a_of_x = _interpolant(x[:r - 1], cs[:r - 1])  # @line L4: A has degree L
        err = [wt[j] * (d[j] - a_of_x(math.cos(grid[j]))) for j in range(g)]  # @line L5
        cand = _extrema(err, band)  # @line L6
        merged: list[int] = []
        for j in cand:  # @line L7: keep the larger of two neighbours with one sign
            if merged and (err[j] > 0) == (err[merged[-1]] > 0):
                if abs(err[j]) > abs(err[merged[-1]]):
                    merged[-1] = j
            else:
                merged.append(j)
        while len(merged) > r:  # @line L8: drop the smaller end
            if abs(err[merged[0]]) < abs(err[merged[-1]]):
                merged.pop(0)
            else:
                merged.pop()
        emax = max(abs(e) for e in err)
        if len(merged) < r:
            break
        if merged == ext or emax - abs(delta) <= 1e-12 * emax:  # @line L9
            ext = merged
            break
        ext = merged  # @line L10
    assert a_of_x is not None
    # @line L11: the coefficients from L + 1 ... N samples of A, by the cosine sums
    amp = [a_of_x(math.cos(2 * math.pi * j / taps)) for j in range(taps)]
    a = [sum(amp) / taps] + [2 / taps * sum(amp[j] * math.cos(2 * math.pi * k * j / taps) for j in range(taps))
                              for k in range(1, half + 1)]
    h = [0.0] * taps
    h[half] = a[0]
    for k in range(1, half + 1):
        h[half - k] = h[half + k] = a[k] / 2
    return Design(h, delta, [grid[j] for j in ext], it)


def amplitude(h: list[float], w: float) -> float:
    """A(w) = sum h[n] cos(w (L - n)) of a symmetric filter with N = 2L + 1 taps."""
    half = (len(h) - 1) // 2
    return sum(c * math.cos(w * (half - n)) for n, c in enumerate(h))


def weighted_error(h: list[float], w: float, wp: float, ws: float, stop_weight: float = 1.0) -> float:
    """W(w) (D(w) - A(w)) on the two bands; 0 in the transition band, which is not part of the spec."""
    if w <= wp:
        return 1.0 - amplitude(h, w)
    if w >= ws:
        return -stop_weight * amplitude(h, w)
    return 0.0


def max_error(h: list[float], wp: float, ws: float, stop_weight: float = 1.0, points: int = 20001) -> float:
    """The largest weighted error on a uniform grid of the two bands."""
    best = 0.0
    n1 = max(2, round(points * wp / (wp + math.pi - ws)))
    n2 = max(2, points - n1)
    for i in range(n1):
        best = max(best, abs(weighted_error(h, wp * i / (n1 - 1), wp, ws, stop_weight)))
    for i in range(n2):
        best = max(best, abs(weighted_error(h, ws + (math.pi - ws) * i / (n2 - 1), wp, ws, stop_weight)))
    return best
