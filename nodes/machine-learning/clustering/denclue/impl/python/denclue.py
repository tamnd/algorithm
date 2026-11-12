# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/denclue/. The authors are listed in prov/HSSEG3.jsonl.

"""DENCLUE (Hinneburg and Keim 1998) with the Gaussian influence function.

Each point climbs the density f(x) = sum_i exp(-|x - x_i|^2 / (2 sigma^2)) to a
density attractor. DENCLUE 1.0 takes steps of fixed length delta along the
normalized gradient and stops when the next step would lower the density.
DENCLUE 2.0 (Hinneburg and Gabriel 2007) uses the fixed point step
x <- sum_i w_i x_i / sum_i w_i and stops when the relative gain is below tol.
Attractors with density below xi are noise. Center-defined clusters group the
points by attractor. Arbitrary-shape clusters also join two attractors when the
straight segment between them stays at density xi or more (a path test that
is sufficient, not necessary, for the path condition of the paper).
"""

import math

NOISE = -1


def sq_dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def density(x, points, sigma):
    return sum(math.exp(-sq_dist(x, p) / (2 * sigma * sigma)) for p in points)


def gradient(x, points, sigma):
    g = [0.0] * len(x)
    for p in points:
        w = math.exp(-sq_dist(x, p) / (2 * sigma * sigma))
        for k in range(len(x)):
            g[k] += w * (p[k] - x[k])
    return g  # equals sigma^2 times the true gradient of f


def climb_fixed_step(start, points, sigma, delta, max_iter=10000, trace=None):
    """DENCLUE 1.0 hill climbing along the normalized gradient."""
    x = tuple(start)  # @line L2
    fx = density(x, points, sigma)
    if trace is not None:
        trace.append(x)
    for _ in range(max_iter):  # @line L3
        g = gradient(x, points, sigma)  # @line L4
        norm = math.sqrt(sum(v * v for v in g))
        if norm == 0:  # @line L5
            break
        x_new = tuple(a + delta * v / norm for a, v in zip(x, g))  # @line L6
        f_new = density(x_new, points, sigma)
        if f_new < fx:  # @line L7
            break
        x, fx = x_new, f_new  # @line L8
        if trace is not None:
            trace.append(x)
    return x, fx


def climb_fixed_point(start, points, sigma, tol=1e-9, max_iter=10000, trace=None):
    """DENCLUE 2.0 hill climbing with the fixed point step."""
    x = tuple(start)
    fx = density(x, points, sigma)
    if trace is not None:
        trace.append(x)
    for _ in range(max_iter):
        w = [math.exp(-sq_dist(x, p) / (2 * sigma * sigma)) for p in points]
        total = sum(w)
        if total == 0:
            break
        x = tuple(sum(wi * p[k] for wi, p in zip(w, points)) / total for k in range(len(x)))
        f_new = density(x, points, sigma)
        if trace is not None:
            trace.append(x)
        gain = (f_new - fx) / f_new if f_new > 0 else 0.0
        fx = f_new
        if gain <= tol:
            break
    return x, fx


def segment_above(a, b, points, sigma, xi, samples):
    for s in range(samples + 1):
        t = s / samples
        p = tuple(u + t * (v - u) for u, v in zip(a, b))
        if density(p, points, sigma) < xi:
            return False
    return True


def denclue(points, sigma, xi, delta=None, merge_dist=None, shape="arbitrary",
            step="fixed", samples=20, max_iter=10000):
    """Return (labels, attractors). labels[j] is -1 for noise. attractors[c] is
    the representative attractor of the merged attractor group c."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    if delta is None:
        delta = sigma / 10
    if merge_dist is None:
        merge_dist = 2 * delta
    ends = []
    for x in points:  # @line L1
        if step == "fixed":
            ends.append(climb_fixed_step(x, points, sigma, delta, max_iter))  # @line L9
        else:
            ends.append(climb_fixed_point(x, points, sigma, max_iter=max_iter))
    reps, rep_f, group = [], [], []
    for x, fx in ends:  # @line L10
        for c, r in enumerate(reps):
            if math.sqrt(sq_dist(x, r)) < merge_dist:
                group.append(c)
                rep_f[c] = max(rep_f[c], fx)
                break
        else:
            reps.append(x)
            rep_f.append(fx)
            group.append(len(reps) - 1)
    root = list(range(len(reps)))

    def find(c):
        while root[c] != c:
            root[c] = root[root[c]]
            c = root[c]
        return c

    if shape == "arbitrary":  # @line L11
        strong = [c for c in range(len(reps)) if rep_f[c] >= xi]
        for i, a in enumerate(strong):
            for b in strong[i + 1:]:
                if find(a) != find(b) and segment_above(reps[a], reps[b], points, sigma, xi, samples):
                    root[find(a)] = find(b)
    labels, names = [], {}
    for c, (_, fx) in zip(group, ends):  # @line L12
        if fx < xi:
            labels.append(NOISE)  # the attractor of this point is too weak: an outlier
            continue
        labels.append(names.setdefault(find(c), len(names)))
    return labels, reps  # @line L13
