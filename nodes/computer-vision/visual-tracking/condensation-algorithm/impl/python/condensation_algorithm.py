# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/condensation-algorithm/. The authors are listed in prov/SEFHQG.jsonl.
"""CONDENSATION: a sample set of contours, propagated by select, predict and measure.

The contour is a circle of fixed radius, so the shape space is the translations
of the plane. A state is (previous center, current center), the state of a
second-order autoregressive model. Measurements are edge pixels found along the
normals of the contour. Images are edge maps, edge[v][u] is True on an edge,
and pixel (u, v) has its center at (u, v).
"""

import bisect
import math
import random


def contour(center, radius, m):
    """m points on the circle and their unit normals, the radial directions."""
    cx, cy = center
    out = []
    for k in range(m):
        a = 2 * math.pi * k / m
        nx, ny = math.cos(a), math.sin(a)
        out.append(((cx + radius * nx, cy + radius * ny), (nx, ny)))
    return out


def features_on_normal(edge, point, normal, reach):
    """Signed offsets nu in [-reach, reach] (step 1) where the normal meets an edge pixel."""
    h, w = len(edge), len(edge[0])
    (px, py), (nx, ny) = point, normal
    out = []
    for t in range(-reach, reach + 1):
        u, v = round(px + t * nx), round(py + t * ny)
        if 0 <= u < w and 0 <= v < h and edge[v][u]:
            out.append(t)
    return out


def clutter_density(nus, sigma, alpha):
    """The density of one normal, up to a constant: 1 + sum exp(-nu^2 / 2 sigma^2) / (sqrt(2 pi) sigma alpha)."""
    c = 1.0 / (math.sqrt(2 * math.pi) * sigma * alpha)
    return 1.0 + c * sum(math.exp(-nu * nu / (2 * sigma * sigma)) for nu in nus)


def nearest_feature_log_likelihood(nearest, r, mu):
    """log of exp(-sum over normals of min(nu_1^2, mu^2) / (2 r M)); None means no feature on that normal."""
    m = len(nearest)
    return -sum(mu * mu if nu is None else min(nu * nu, mu * mu) for nu in nearest) / (2 * r * m)


def log_likelihood(edge, center, radius, m, reach, sigma, alpha):
    """log p(z | x): the product of the clutter densities of the m normals."""
    return sum(math.log(clutter_density(features_on_normal(edge, p, n, reach), sigma, alpha))
               for p, n in contour(center, radius, m))


def select(cumulative, r):
    """The smallest j with cumulative[j] >= r, by binary subdivision."""
    j = bisect.bisect_left(cumulative, r)
    return min(j, len(cumulative) - 1)


class Condensation:
    def __init__(self, center, radius, n=300, spread=3.0, damping=1.0, noise=1.0,
                 m=16, reach=6, sigma=1.0, alpha=0.05, seed=0):
        self.rng = random.Random(seed)
        self.radius, self.m, self.reach = radius, m, reach
        self.sigma, self.alpha = sigma, alpha
        self.damping, self.noise = damping, noise
        g = self.rng.gauss
        self.samples = []
        for _ in range(n):  # the prior: a Gaussian around the first center, zero mean velocity
            cur = (center[0] + g(0, spread), center[1] + g(0, spread))
            prev = (cur[0] + g(0, noise), cur[1] + g(0, noise))
            self.samples.append((prev, cur))
        self.weights = [1.0 / n] * n
        self.cumulative = [(k + 1) / n for k in range(n)]

    def step(self, edge):
        n = len(self.samples)
        g = self.rng.gauss
        new = []
        for _ in range(n):
            r = self.rng.random() * self.cumulative[-1]  # @line L1
            prev, cur = self.samples[select(self.cumulative, r)]  # @line L2
            vx, vy = cur[0] - prev[0], cur[1] - prev[1]  # @line L3
            nxt = (cur[0] + self.damping * vx + self.noise * g(0, 1),
                   cur[1] + self.damping * vy + self.noise * g(0, 1))
            new.append((cur, nxt))
        logs = [log_likelihood(edge, s[1], self.radius, self.m, self.reach, self.sigma, self.alpha)
                for s in new]  # @line L4
        top = max(logs)
        w = [math.exp(t - top) for t in logs]
        total = sum(w)
        self.weights = [t / total for t in w]  # @line L5
        c, acc = [], 0.0
        for t in self.weights:  # @line L6
            acc += t
            c.append(acc)
        self.samples, self.cumulative = new, c
        return self.mean()  # @line L7

    def mean(self):
        x = sum(wt * s[1][0] for wt, s in zip(self.weights, self.samples))
        y = sum(wt * s[1][1] for wt, s in zip(self.weights, self.samples))
        return (x, y)


def draw_circle(edge, center, radius):
    """Mark the pixel nearest to each of about 8 pi radius points of the circle."""
    h, w = len(edge), len(edge[0])
    k = max(8, int(8 * math.pi * radius))
    for i in range(k):
        a = 2 * math.pi * i / k
        u, v = round(center[0] + radius * math.cos(a)), round(center[1] + radius * math.sin(a))
        if 0 <= u < w and 0 <= v < h:
            edge[v][u] = True
