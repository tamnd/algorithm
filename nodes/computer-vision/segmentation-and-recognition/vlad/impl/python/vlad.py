# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vlad/. The authors are listed in prov/D9847P.jsonl.
"""VLAD: the vector of locally aggregated descriptors.

Each local descriptor x (a list of D floats) is assigned to its nearest center
c_k of a fixed codebook C of K centers, ties going to the smaller index. For
each center the residuals x - c_k of its descriptors are summed, and the K
sums are concatenated into one vector of K D values. Optional steps: intra
normalization (each block of D values scaled to unit L2 norm), power
normalization z -> sign(z) |z|^alpha, and a final L2 normalization.
Standard library only. Cost: O(n K D) for n descriptors with a linear scan
for the nearest center, and O(K D) extra space.
"""

import math


def sq_dist(a, b):
    """Squared Euclidean distance of two vectors."""
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def nearest_center(x, centers):
    """Index of the nearest center; ties go to the smaller index."""
    best, best_d = 0, sq_dist(x, centers[0])
    for k in range(1, len(centers)):
        d = sq_dist(x, centers[k])
        if d < best_d:
            best, best_d = k, d
    return best


def l2_normalize(z):
    """Scale z to unit L2 norm; the zero vector stays zero."""
    s = math.sqrt(sum(t * t for t in z))
    if s == 0.0:
        return list(z)
    return [t / s for t in z]


def power_normalize(z, alpha):
    """Signed power: sign(t) |t|^alpha for each entry. alpha = 0.5 is the signed square root."""
    return [math.copysign(abs(t) ** alpha, t) if t != 0 else 0.0 for t in z]


def vlad_blocks(descriptors, centers):
    """The K residual sums v_k (lists of D floats), before any normalization."""
    K, D = len(centers), len(centers[0])
    v = [[0.0] * D for _ in range(K)]  # @line L1
    for x in descriptors:  # @line L2
        k = nearest_center(x, centers)  # @line L3
        ck = centers[k]
        vk = v[k]
        for i in range(D):  # @line L4
            vk[i] += x[i] - ck[i]
    return v


def vlad(descriptors, centers, alpha=1.0, intra=False, l2=True):
    """The VLAD vector of a set of descriptors, as a flat list of K D floats.

    alpha = 1.0 means no power normalization; Jegou et al. use alpha = 0.5.
    intra = True scales each block to unit norm first (Arandjelovic and Zisserman).
    """
    v = vlad_blocks(descriptors, centers)
    if intra:  # @line L5
        v = [l2_normalize(block) for block in v]
    z = [t for block in v for t in block]  # @line L6
    if alpha != 1.0:  # @line L7
        z = power_normalize(z, alpha)
    if l2:  # @line L8
        z = l2_normalize(z)
    return z  # @line L9


def sum_match_kernel(xs, ys, centers):
    """Brute force: the sum over pairs (x, y) in the same cell k of <x - c_k, y - c_k>."""
    total = 0.0
    for x in xs:
        kx = nearest_center(x, centers)
        for y in ys:
            if nearest_center(y, centers) == kx:
                c = centers[kx]
                total += sum((a - ci) * (b - ci) for a, b, ci in zip(x, y, c))
    return total


def cell_means(descriptors, centers):
    """For each center: the count n_k and the mean of its descriptors (None if empty)."""
    K, D = len(centers), len(centers[0])
    sums = [[0.0] * D for _ in range(K)]
    counts = [0] * K
    for x in descriptors:
        k = nearest_center(x, centers)
        counts[k] += 1
        for i in range(D):
            sums[k][i] += x[i]
    means = [None if counts[k] == 0 else [s / counts[k] for s in sums[k]] for k in range(K)]
    return counts, means
