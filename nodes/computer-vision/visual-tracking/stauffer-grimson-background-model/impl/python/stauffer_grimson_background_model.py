# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stauffer-grimson-background-model/. The authors are listed in prov/193Y4C.jsonl.
"""Adaptive Gaussian mixture background model (Stauffer and Grimson 1999), gray values.

Each pixel has K Gaussian components (w, mu, var). For a new value x:
  1. order the components by w / sigma and take the first one with
     |x - mu| <= 2.5 sigma as the match;
  2. no match: replace the last component by (w0, x, v0) and scale the
     other weights so that all weights sum to 1;
  3. match m: w_k <- (1 - alpha) w_k + alpha [k = m] for all k, then
     rho = alpha * eta(x | mu_m, var_m), mu_m <- (1 - rho) mu_m + rho x,
     var_m <- (1 - rho) var_m + rho (x - mu_m)^2 with the new mu_m;
  4. order again by w / sigma; the first B components, B the smallest b with
     w_(1) + ... + w_(b) > T, are the background;
  5. the pixel is background if its match is one of the first B components.

rho_mode "paper" uses rho = alpha * eta as in the paper; "alpha_over_w" uses
rho = alpha / w_m, a common faster choice. var_min is a floor on the variance,
an implementation choice that keeps the density finite.
An image is a list of rows of gray values. Cost per pixel and frame: O(K log K).
"""

import math


def gaussian_density(x, mu, var):
    return math.exp(-0.5 * (x - mu) ** 2 / var) / math.sqrt(2.0 * math.pi * var)


def ranked(comps):
    """Indices of the components by w / sigma, largest first (ties: lower index first)."""
    return sorted(range(len(comps)), key=lambda k: (-comps[k][0] / math.sqrt(comps[k][2]), k))


def background_set(comps, t):
    """The first B components by w / sigma, B the smallest b with a weight sum above t."""
    order = ranked(comps)
    total, chosen = 0.0, []
    for k in order:
        chosen.append(k)
        total += comps[k][0]
        if total > t:
            break
    return set(chosen)


class PixelMixture:
    """The mixture of one pixel: a list of [w, mu, var]."""

    def __init__(self, x, k=3, v0=900.0):
        self.comps = [[1.0, float(x), v0]] + [[0.0, 0.0, v0] for _ in range(k - 1)]

    def update(self, x, alpha=0.01, t=0.7, v0=900.0, w0=0.05, rho_mode="paper", var_min=4.0):
        """Feed one value. Returns True if the value is background."""
        c = self.comps
        order = ranked(c)
        match = None
        for k in order:  # @line L1
            if c[k][0] > 0 and abs(x - c[k][1]) <= 2.5 * math.sqrt(c[k][2]):
                match = k
                break
        if match is None:  # @line L2
            last = order[-1]
            rest = sum(c[k][0] for k in range(len(c)) if k != last)
            for k in range(len(c)):
                if k != last:
                    c[k][0] = c[k][0] * (1.0 - w0) / rest if rest > 0 else (1.0 - w0) / (len(c) - 1)
            c[last] = [w0, float(x), v0]
            return False
        for k in range(len(c)):  # @line L3
            c[k][0] = (1.0 - alpha) * c[k][0] + (alpha if k == match else 0.0)
        w, mu, var = c[match]
        if rho_mode == "paper":  # @line L4
            rho = min(1.0, alpha * gaussian_density(x, mu, var))
        else:
            rho = min(1.0, alpha / w)
        mu = (1.0 - rho) * mu + rho * x
        var = max(var_min, (1.0 - rho) * var + rho * (x - mu) ** 2)
        c[match][1], c[match][2] = mu, var
        bg = background_set(c, t)  # @line L5
        return match in bg  # @line L6


class BackgroundModel:
    """A Stauffer-Grimson model for gray images of a fixed size."""

    def __init__(self, first_frame, k=3, alpha=0.01, t=0.7, v0=900.0, w0=0.05,
                 rho_mode="paper", var_min=4.0):
        self.params = dict(alpha=alpha, t=t, v0=v0, w0=w0, rho_mode=rho_mode, var_min=var_min)
        self.pixels = [[PixelMixture(x, k, v0) for x in row] for row in first_frame]

    def apply(self, frame):
        """Returns the foreground mask of the frame: a list of rows of 0 and 1."""
        return [[0 if p.update(x, **self.params) else 1 for p, x in zip(prow, row)]
                for prow, row in zip(self.pixels, frame)]
