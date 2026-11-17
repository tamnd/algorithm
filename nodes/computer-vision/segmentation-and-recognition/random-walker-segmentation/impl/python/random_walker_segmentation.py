# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-walker-segmentation/. The authors are listed in prov/TCA3BR.jsonl.

"""Random walker segmentation of Grady (2006).

Pixel p = v * w + u is (u, v) with the gray value img[v][u]. The pixels form a
4-connected grid graph. The edge weight is w_pq = exp(-beta d_pq), where d_pq
is the squared gray difference divided by the largest squared difference in
the image. The seeds are a dict from pixel to label 0 .. K-1. For each label
s the probability x^s is the harmonic function that is 1 on the seeds of s,
0 on the other seeds, and solves L_U x_U = -B^T m on the free pixels. Each
pixel gets the label of largest probability. The dense solver of cvla is
used, so the code suits small images only.
"""

import math

from cvla import solve, zeros


def grid_edges(h, w):
    """The 4-connected pairs (p, q) with p < q."""
    edges = []
    for v in range(h):
        for u in range(w):
            p = v * w + u
            if u + 1 < w:
                edges.append((p, p + 1))
            if v + 1 < h:
                edges.append((p, p + w))
    return edges


def edge_weights(img, edges, beta):
    """w_pq = exp(-beta d_pq) with the normalized squared difference d_pq."""
    flat = [x for row in img for x in row]
    d2 = [(flat[p] - flat[q]) ** 2 for p, q in edges]
    top = max(d2) if d2 else 0.0
    if top <= 0:
        top = 1.0
    return [math.exp(-beta * d / top) for d in d2]


def laplacian(n, edges, weights):
    """The dense graph Laplacian L = D - W."""
    lap = zeros(n, n)
    for (p, q), wt in zip(edges, weights):
        lap[p][p] += wt
        lap[q][q] += wt
        lap[p][q] -= wt
        lap[q][p] -= wt
    return lap


def solve_labels(lap, n, seeds, labels, free=None):
    """Solve L_U X = -B^T M for the given labels; return {s: x^s over all pixels}."""
    marked = sorted(seeds)
    if free is None:
        free = [p for p in range(n) if p not in seeds]
    out = {s: [0.0] * n for s in labels}
    for p in marked:
        if seeds[p] in out:
            out[seeds[p]][p] = 1.0
    if not free or not labels:
        return out
    lu = [[lap[i][j] for j in free] for i in free]
    rhs = [[-sum(lap[i][p] for p in marked if seeds[p] == s) for s in labels] for i in free]
    xu = solve(lu, rhs)
    for r, p in enumerate(free):
        for c, s in enumerate(labels):
            out[s][p] = xu[r][c]
    return out


def random_walker(img, seeds, beta, nlabels=None):
    """Return (probs, labels): probs[s][p] is the probability that a walker
    from pixel p first reaches a seed of label s, and labels[p] is the argmax.
    Every connected part of the grid must hold a seed (a grid is connected)."""
    h, w = len(img), len(img[0])
    n = h * w
    k = nlabels if nlabels is not None else max(seeds.values()) + 1
    if k < 2:
        raise ValueError("need at least two labels")
    edges = grid_edges(h, w)
    weights = edge_weights(img, edges, beta)  # @line L1
    lap = laplacian(n, edges, weights)  # @line L2
    free = [p for p in range(n) if p not in seeds]  # @line L3
    first = list(range(k - 1))  # @line L4
    part = solve_labels(lap, n, seeds, first, free)  # @line L5
    probs = [part[s] for s in first]
    probs.append([1.0 - sum(probs[s][p] for s in first) for p in range(n)])  # @line L6
    labels = [max(range(k), key=lambda s: probs[s][p]) for p in range(n)]  # @line L7
    return probs, labels  # @line L8


def random_walker_all(img, seeds, beta, nlabels):
    """The same probabilities from K solves, without the sum rule. For tests."""
    h, w = len(img), len(img[0])
    n = h * w
    edges = grid_edges(h, w)
    lap = laplacian(n, edges, edge_weights(img, edges, beta))
    part = solve_labels(lap, n, seeds, list(range(nlabels)))
    return [part[s] for s in range(nlabels)]


def dirichlet_energy(edges, weights, x):
    """D[x] = 1/2 x^T L x = 1/2 sum over edges of w_pq (x_p - x_q)^2."""
    return 0.5 * sum(wt * (x[p] - x[q]) ** 2 for (p, q), wt in zip(edges, weights))


def conjugate_gradient(a, b, tol=1e-12, maxit=None):
    """Solve a x = b for a symmetric positive definite a by conjugate gradients."""
    n = len(b)
    x = [0.0] * n
    r = list(b)
    d = list(r)
    rr = sum(t * t for t in r)
    for _ in range(maxit or 10 * n):
        if math.sqrt(rr) <= tol:
            break
        ad = [sum(a[i][j] * d[j] for j in range(n)) for i in range(n)]
        step = rr / sum(d[i] * ad[i] for i in range(n))
        x = [x[i] + step * d[i] for i in range(n)]
        r = [r[i] - step * ad[i] for i in range(n)]
        rr_new = sum(t * t for t in r)
        d = [r[i] + (rr_new / rr) * d[i] for i in range(n)]
        rr = rr_new
    return x


def monte_carlo(img, seeds, beta, start, walks, rng):
    """Estimate the probabilities at pixel start by simulating walks."""
    h, w = len(img), len(img[0])
    edges = grid_edges(h, w)
    weights = edge_weights(img, edges, beta)
    nbr = [[] for _ in range(h * w)]
    for (p, q), wt in zip(edges, weights):
        nbr[p].append((q, wt))
        nbr[q].append((p, wt))
    k = max(seeds.values()) + 1
    hits = [0] * k
    for _ in range(walks):
        p = start
        while p not in seeds:
            total = sum(wt for _, wt in nbr[p])
            t = rng.random() * total
            for q, wt in nbr[p]:
                t -= wt
                if t <= 0:
                    break
            p = q
        hits[seeds[p]] += 1
    return [c / walks for c in hits]
