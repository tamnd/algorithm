# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/umbrella-sampling/. The authors are listed in prov/H90CB5.jsonl.
"""Umbrella sampling (Torrie and Valleau 1977) on a one-dimensional coordinate.

Each window k adds the bias w_k(s) = (kappa / 2) (s - s_k)^2 to the potential
and samples exp(-beta (U + w_k)). In window k the free energy is known up to a
constant from the biased histogram,

    F(b) = -kT ln n_k(b) - w_k(b) + c_k,

and the constants c_k are fixed by asking neighbouring windows to agree on the
bins they share. This file uses that simple join (a least-squares match on the
shared bins). WHAM is the better way to combine the windows; see the WHAM page.

The coordinate is s = x here, so the exact free energy profile is U itself,
which the tests use.
"""

import math
from typing import Callable, Sequence


def double_well(height: float) -> Callable[[float], float]:
    """U(x) = height (x^2 - 1)^2, minima at x = -1 and x = 1, barrier height at x = 0."""
    return lambda x: height * (x * x - 1.0) ** 2


def harmonic_bias(center: float, kappa: float) -> Callable[[float], float]:
    return lambda s: 0.5 * kappa * (s - center) ** 2


def metropolis(u: Callable[[float], float], beta: float, x0: float, step: float,
               n: int, rng, burn: int = 500) -> list[float]:
    """Random walk Metropolis chain for the density exp(-beta u)."""
    x, ux = x0, u(x0)
    out = []
    for i in range(burn + n):
        y = x + step * (2.0 * rng.random() - 1.0)
        uy = u(y)
        if uy <= ux or rng.random() < math.exp(-beta * (uy - ux)):
            x, ux = y, uy
        if i >= burn:
            out.append(x)
    return out


def histogram(values: Sequence[float], lo: float, hi: float, nbins: int) -> list[int]:
    counts = [0] * nbins
    width = (hi - lo) / nbins
    for v in values:
        b = int((v - lo) // width)
        if 0 <= b < nbins:
            counts[b] += 1
    return counts


def bin_centers(lo: float, hi: float, nbins: int) -> list[float]:
    width = (hi - lo) / nbins
    return [lo + (b + 0.5) * width for b in range(nbins)]


def unbias(counts: Sequence[int], bias: Callable[[float], float], centers: Sequence[float],
           beta: float, min_count: int = 50) -> list:
    """-kT ln n(b) - w(b) on bins with at least min_count samples, None elsewhere."""
    return [(-math.log(c) / beta - bias(s)) if c >= min_count else None
            for c, s in zip(counts, centers)]


def join_windows(profiles: Sequence[list], counts: Sequence[Sequence[int]]) -> list:
    """Join window profiles, in order along s, into one profile with minimum 0."""
    f = list(profiles[0])                                        # @line L5
    weight = [c if p is not None else 0 for p, c in zip(f, counts[0])]
    for prof, cnt in zip(profiles[1:], counts[1:]):              # @line L6
        shared = [b for b, (a, p) in enumerate(zip(f, prof)) if a is not None and p is not None]
        if not shared:
            raise ValueError("neighbouring windows share no bins")
        shift = sum(f[b] - prof[b] for b in shared) / len(shared)  # @line L6
        for b, p in enumerate(prof):                             # @line L7
            if p is None:
                continue
            p += shift
            if f[b] is None:
                f[b], weight[b] = p, cnt[b]
            else:                                                # count-weighted mean
                f[b] = (weight[b] * f[b] + cnt[b] * p) / (weight[b] + cnt[b])
                weight[b] += cnt[b]
    m = min(v for v in f if v is not None)
    return [v - m if v is not None else None for v in f]         # @line L8


def umbrella_sampling(u: Callable[[float], float], centers_s: Sequence[float], kappa: float,
                      beta: float, n: int, step: float, lo: float, hi: float, nbins: int,
                      rng) -> tuple[list, list[list[int]]]:
    """Free energy profile on the bins of [lo, hi], and the window histograms."""
    centers = bin_centers(lo, hi, nbins)
    profiles, all_counts = [], []
    for s_k in centers_s:                                        # @line L1
        w = harmonic_bias(s_k, kappa)
        xs = metropolis(lambda x: u(x) + w(x), beta, s_k, step, n, rng)  # @line L2
        counts = histogram(xs, lo, hi, nbins)                    # @line L3
        profiles.append(unbias(counts, w, centers, beta))        # @line L4
        all_counts.append(counts)
    return join_windows(profiles, all_counts), all_counts
