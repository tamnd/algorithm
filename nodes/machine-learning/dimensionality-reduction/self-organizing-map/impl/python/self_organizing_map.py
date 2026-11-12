# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/self-organizing-map/. The authors are listed in prov/MBT904.jsonl.

"""Kohonen's self-organizing map (1982): the online rule, the batch rule and two error measures.

Units sit at fixed grid positions r_j and hold weight vectors w_j in the input space.
Online rule, for one input x with best matching unit c = argmin_j |x - w_j|:
    w_j <- w_j + alpha(t) h_cj(t) (x - w_j),  h_cj = exp(-|r_j - r_c|^2 / (2 sigma(t)^2)),
with alpha falling linearly to 0 and sigma falling geometrically from sigma0 to sigma1.
Batch rule: w_j <- sum_i h_{c(i) j} x_i / sum_i h_{c(i) j}.
"""

import math


def grid(rows, cols):
    """Grid positions of a rows x cols rectangular map, in row-major order."""
    return [(float(r), float(c)) for r in range(rows) for c in range(cols)]


def sq(u, v):
    return sum((a - b) ** 2 for a, b in zip(u, v))


def best_matching_unit(weights, x):
    """Index of the unit whose weight is nearest to x (the lowest index on ties)."""
    return min(range(len(weights)), key=lambda j: (sq(weights[j], x), j))


def neighborhood(pos, c, sigma):
    """Gaussian neighborhood h_cj = exp(-|r_j - r_c|^2 / (2 sigma^2)) for every unit j."""
    return [math.exp(-sq(r, pos[c]) / (2.0 * sigma * sigma)) for r in pos]


def update(weights, pos, x, alpha, sigma):
    """One online step for input x; returns the best matching unit."""
    c = best_matching_unit(weights, x)  # @line L4
    h = neighborhood(pos, c, sigma)  # @line L6
    for j, w in enumerate(weights):
        for k in range(len(w)):
            w[k] += alpha * h[j] * (x[k] - w[k])  # @line L7
    return c


def som(data, pos, rng, steps=2000, alpha0=0.5, sigma0=None, sigma1=0.5):
    """Online SOM. data: list of vectors; pos: grid positions; rng: random.Random. Returns the weights."""
    if sigma0 is None:
        sigma0 = max(max(abs(a - b) for a, b in zip(p, q)) for p in pos for q in pos) / 2.0 or 1.0
    dim = len(data[0])
    lo = [min(x[k] for x in data) for k in range(dim)]
    hi = [max(x[k] for x in data) for k in range(dim)]
    weights = [[rng.uniform(lo[k], hi[k]) for k in range(dim)] for _ in pos]  # @line L1
    for t in range(steps):  # @line L2
        x = data[rng.randrange(len(data))]  # @line L3
        alpha = alpha0 * (1.0 - t / steps)  # @line L5
        sigma = sigma0 * (sigma1 / sigma0) ** (t / steps)
        update(weights, pos, x, alpha, sigma)
    return weights  # @line L8


def batch_som(data, pos, weights, sigmas):
    """Batch SOM: one pass per value in sigmas, each w_j set to the h-weighted mean of the data."""
    weights = [w[:] for w in weights]
    dim = len(data[0])
    for sigma in sigmas:
        num = [[0.0] * dim for _ in pos]
        den = [0.0] * len(pos)
        for x in data:
            h = neighborhood(pos, best_matching_unit(weights, x), sigma)
            for j in range(len(pos)):
                den[j] += h[j]
                for k in range(dim):
                    num[j][k] += h[j] * x[k]
        weights = [[num[j][k] / den[j] for k in range(dim)] if den[j] > 0.0 else weights[j] for j in range(len(pos))]
    return weights


def quantization_error(data, weights):
    """Mean distance from each input to the weight of its best matching unit."""
    return sum(math.sqrt(sq(x, weights[best_matching_unit(weights, x)])) for x in data) / len(data)


def topographic_error(data, weights, pos):
    """Share of inputs whose best and second best units are not grid neighbors (grid distance > 1)."""
    bad = 0
    for x in data:
        order = sorted(range(len(weights)), key=lambda j: (sq(weights[j], x), j))
        if sq(pos[order[0]], pos[order[1]]) > 1.0 + 1e-12:
            bad += 1
    return bad / len(data)
