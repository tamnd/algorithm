# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/density-peak-clustering/. The authors are listed in prov/E4EF5R.jsonl.

"""Clustering by fast search and find of density peaks (Rodriguez and Laio 2014).

Tie rule: points are ranked by density, higher first, and equal densities by
index, lower first. "Higher density" in the definition of delta means "earlier
in this ranking", so every point except the first has a nearest point of higher
density, and the first point is always a center. Among earlier points at the
same distance, the earliest one is the nearest neighbor of higher density.
"""

import math


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def local_density(points, d_c, kernel="cutoff", dist=euclidean):
    n = len(points)
    rho = [0.0] * n
    for i in range(n):
        for j in range(n):
            if i != j:
                d = dist(points[i], points[j])
                if kernel == "cutoff":
                    rho[i] += 1 if d < d_c else 0
                else:
                    rho[i] += math.exp(-(d / d_c) ** 2)
    return rho


def delta_and_parent(points, rho, dist=euclidean):
    """Return (order, delta, parent). parent[i] is the nearest point of higher
    density (earlier in order), or -1 for the first point."""
    n = len(points)
    order = sorted(range(n), key=lambda i: (-rho[i], i))  # @line L2
    delta, parent = [0.0] * n, [-1] * n
    if n == 0:
        return order, delta, parent
    top = order[0]
    delta[top] = max(dist(points[top], q) for q in points)  # @line L3
    for r in range(1, n):  # @line L4
        i = order[r]
        best, arg = math.inf, -1
        for s in range(r):  # @line L5
            d = dist(points[i], points[order[s]])
            if d < best:
                best, arg = d, order[s]
        delta[i], parent[i] = best, arg
    return order, delta, parent


def choose_centers(order, rho, delta, n_centers=None, rho_min=None, delta_min=None):
    """Centers from the decision graph: the n_centers largest gamma = rho * delta,
    or all points with rho > rho_min and delta > delta_min. The first point of the
    order is always a center."""
    if not order:
        return set()
    rank = {p: r for r, p in enumerate(order)}
    if n_centers is not None:
        by_gamma = sorted(order, key=lambda i: (-rho[i] * delta[i], rank[i]))
        centers = set(by_gamma[:n_centers])
    else:
        centers = {i for i in order if rho[i] > rho_min and delta[i] > delta_min}
    centers.add(order[0])
    return centers


def halo(points, labels, rho, d_c, dist=euclidean):
    """Return a list of booleans: True for the halo points of each cluster."""
    n = len(points)
    rho_b = {}
    for i in range(n):
        for j in range(n):
            if labels[i] != labels[j] and dist(points[i], points[j]) < d_c:
                rho_b[labels[i]] = max(rho_b.get(labels[i], -math.inf), rho[i])  # @line L10
    return [rho[i] <= rho_b.get(labels[i], -math.inf) for i in range(n)]  # @line L11


def density_peak_clustering(points, d_c, n_centers=None, rho_min=None, delta_min=None,
                            kernel="cutoff", with_halo=False, dist=euclidean):
    """Return (labels, centers in label order), and the halo flags if with_halo."""
    if n_centers is None and (rho_min is None or delta_min is None):
        raise ValueError("give n_centers, or both rho_min and delta_min")
    rho = local_density(points, d_c, kernel, dist)  # @line L1
    order, delta, parent = delta_and_parent(points, rho, dist)
    centers = choose_centers(order, rho, delta, n_centers, rho_min, delta_min)  # @line L6
    labels, center_list = [None] * len(points), []
    for i in order:  # @line L7
        if i in centers:
            labels[i] = len(center_list)  # @line L8
            center_list.append(i)
        else:
            labels[i] = labels[parent[i]]  # @line L9
    if with_halo:
        return labels, center_list, halo(points, labels, rho, d_c, dist)
    return labels, center_list  # @line L12
