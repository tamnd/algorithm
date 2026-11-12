# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cop-k-means/. The authors are listed in prov/CH7828.jsonl.

"""COP-KMEANS (Wagstaff, Cardie, Rogers and Schroedl 2001): k-means in
which each point, in a fixed order, goes to the nearest cluster that
violates no must-link or cannot-link constraint with the points already
assigned in this pass. If a point has no such cluster, the algorithm
reports failure. The constraints are first closed under transitivity,
as in Wagstaff and Cardie (2000).
"""


def sqdist(p, q):
    return sum((a - b) ** 2 for a, b in zip(p, q))


def mean(points):
    n = len(points)
    return [sum(p[i] for p in points) / n for i in range(len(points[0]))]


def closure(n, ml, cl):
    """Transitive closure of the constraints: ml_of[i] lists the other
    points of the must-link component of i, and cl_of[i] lists the points
    of every component that has a cannot-link pair with the component of i."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in ml:
        parent[find(a)] = find(b)
    members = {}
    for i in range(n):
        members.setdefault(find(i), []).append(i)
    apart = {r: set() for r in members}
    for a, b in cl:
        apart[find(a)].add(find(b))
        apart[find(b)].add(find(a))
    ml_of = [[j for j in members[find(i)] if j != i] for i in range(n)]
    cl_of = [[j for r in apart[find(i)] for j in members[r]] for i in range(n)]
    return ml_of, cl_of


def violates(i, c, labels, ml_of, cl_of):
    """True if putting point i into cluster c breaks a constraint with a
    point that already has a label in this pass."""
    for j in ml_of[i]:
        if labels[j] is not None and labels[j] != c:
            return True
    for j in cl_of[i]:
        if labels[j] == c:
            return True
    return False


def cop_kmeans(points, k, ml, cl, rng=None, centers=None, order=None, max_iter=100):
    """Return (labels, centers), or (None, centers) on failure.

    centers: the initial centers; if None, k distinct points chosen with
    rng (a random.Random). order: the order in which points are assigned
    (default 0, 1, ..., n - 1).
    """
    n = len(points)
    ml_of, cl_of = closure(n, ml, cl)
    if centers is None:
        centers = [list(points[i]) for i in rng.sample(range(n), k)]  # @line L1
    centers = [list(c) for c in centers]
    order = list(range(n)) if order is None else list(order)
    previous = None
    for _ in range(max_iter):  # @line L2
        labels = [None] * n
        for i in order:  # @line L3
            ranked = sorted(range(k), key=lambda c: (sqdist(points[i], centers[c]), c))
            for c in ranked:  # @line L4
                if not violates(i, c, labels, ml_of, cl_of):
                    labels[i] = c
                    break
            else:
                return None, centers  # @line L5
        for c in range(k):  # @line L6
            members = [points[i] for i in range(n) if labels[i] == c]
            if members:
                centers[c] = mean(members)
        if labels == previous:  # @line L7
            break
        previous = labels
    return labels, centers  # @line L8


def satisfies(labels, ml, cl):
    return all(labels[a] == labels[b] for a, b in ml) and all(labels[a] != labels[b] for a, b in cl)
