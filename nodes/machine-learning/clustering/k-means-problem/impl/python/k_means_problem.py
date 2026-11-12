# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-means-problem/. The authors are listed in prov/2GYFP1.jsonl.

"""The k-means objective, the centroid, a brute force optimum and the exact 1D dynamic program.

Points are tuples of numbers. Use fractions.Fraction coordinates to get exact results.
"""

from typing import Iterator, Sequence

Point = tuple


def sq_dist(x: Sequence, y: Sequence):
    """Squared Euclidean distance."""
    return sum((a - b) * (a - b) for a, b in zip(x, y))


def centroid(cluster: Sequence[Point]) -> Point:
    """The mean of a non-empty list of points."""
    n = len(cluster)
    d = len(cluster[0])
    return tuple(sum(p[t] for p in cluster) / n for t in range(d))


def cost(points: Sequence[Point], centers: Sequence[Point]):
    """The k-means cost: each point pays its squared distance to the nearest center."""
    return sum(min(sq_dist(x, c) for c in centers) for x in points)


def partition_cost(clusters: Sequence[Sequence[Point]]):
    """The cost of a partition when each cluster uses its centroid as the center."""
    total = 0
    for cl in clusters:
        if cl:
            m = centroid(cl)
            total += sum(sq_dist(x, m) for x in cl)
    return total


def set_partitions(n: int, k: int) -> Iterator[list[int]]:
    """Yield each labeling of 0..n-1 into exactly k non-empty blocks once.

    The labelings are restricted growth strings: labels[0] = 0 and each label is at
    most one more than the largest label before it.
    """
    if not 1 <= k <= n:
        return
    labels = [0] * n
    while True:
        if max(labels) == k - 1:
            yield list(labels)
        # next restricted growth string with all labels < k
        i = n - 1
        while i > 0:
            prefix_max = max(labels[:i])
            if labels[i] <= prefix_max and labels[i] < k - 1:
                labels[i] += 1
                for j in range(i + 1, n):
                    labels[j] = 0
                break
            i -= 1
        if i == 0:
            return


def brute_force(points: Sequence[Point], k: int):
    """Return (best cost, best labels) over all partitions into exactly k non-empty clusters."""
    best, best_labels = None, None
    for labels in set_partitions(len(points), k):
        clusters = [[points[i] for i in range(len(points)) if labels[i] == j] for j in range(k)]
        c = partition_cost(clusters)
        if best is None or c < best:
            best, best_labels = c, labels
    return best, best_labels


def optimal_1d(xs: Sequence, k: int):
    """Exact 1D k-means by dynamic programming in O(k n^2) time and O(k n) space.

    Returns (cost, clusters), where clusters is a list of k sorted lists of values.
    """
    a = sorted(xs)
    n = len(a)
    if not 1 <= k <= n:
        raise ValueError("need 1 <= k <= n")
    s1 = [0] * (n + 1)
    s2 = [0] * (n + 1)
    for i, v in enumerate(a):
        s1[i + 1] = s1[i] + v
        s2[i + 1] = s2[i] + v * v

    def sse(j: int, i: int):  # the cost of a[j..i-1] around its own mean
        s = s1[i] - s1[j]
        return (s2[i] - s2[j]) - s * s / (i - j)

    D = [[None] * (n + 1) for _ in range(k + 1)]  # D[m][i]: best cost of a[0..i-1] in m clusters
    B = [[0] * (n + 1) for _ in range(k + 1)]
    D[0][0] = 0
    for m in range(1, k + 1):
        for i in range(m, n + 1):
            for j in range(m - 1, i):
                if D[m - 1][j] is None:
                    continue
                v = D[m - 1][j] + sse(j, i)
                if D[m][i] is None or v < D[m][i]:
                    D[m][i], B[m][i] = v, j
    clusters = []
    i = n
    for m in range(k, 0, -1):
        j = B[m][i]
        clusters.append(a[j:i])
        i = j
    clusters.reverse()
    return D[k][n], clusters
