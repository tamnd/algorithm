# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partitioning-around-medoids/. The authors are listed in prov/52CM06.jsonl.

"""PAM (Kaufman and Rousseeuw): the greedy BUILD phase and the SWAP phase
of best single swaps, on a dissimilarity matrix."""


def total_cost(D, medoids):
    return sum(min(D[j][m] for m in medoids) for j in range(len(D)))


def _nearest_two(D, medoids):
    """For each object j: (distance to nearest medoid, the medoid, distance
    to the second nearest medoid or None when k = 1)."""
    out = []
    for j in range(len(D)):
        ds = sorted((D[j][m], m) for m in medoids)
        out.append((ds[0][0], ds[0][1], ds[1][0] if len(ds) > 1 else None))
    return out


def build(D, k):
    """Greedy BUILD: the first medoid has the least total dissimilarity;
    each next medoid gives the largest decrease of the total cost."""
    n = len(D)
    first = min(range(n), key=lambda i: (sum(D[i]), i))  # @line L1
    medoids = [first]
    near = [D[j][first] for j in range(n)]  # @line L2
    while len(medoids) < k:  # @line L3
        best, best_gain = None, None
        for i in range(n):
            if i in medoids:
                continue
            gain = sum(max(near[j] - D[j][i], 0) for j in range(n))  # @line L4
            if best_gain is None or gain > best_gain:
                best, best_gain = i, gain
        medoids.append(best)  # @line L5
        near = [min(near[j], D[j][best]) for j in range(n)]
    return medoids


def swap_delta(D, medoids, info, m, h):
    """Change of the total cost when medoid m is replaced by object h,
    from the nearest and second nearest distances, in O(n) time."""
    delta = 0
    for j in range(len(D)):
        dj, mj, ej = info[j]
        dh = D[j][h]
        if mj == m:
            new = dh if ej is None else min(ej, dh)
        else:
            new = min(dj, dh)
        delta += new - dj
    return delta


def swap(D, medoids, trace=None):
    """SWAP: apply the best single swap while it lowers the cost.

    Returns the medoids of a local optimum: no replacement of one medoid
    by one non-medoid lowers the total cost.
    """
    n = len(D)
    medoids = list(medoids)
    while True:  # @line L6
        info = _nearest_two(D, medoids)
        best = None
        for m in medoids:  # @line L7
            for h in range(n):
                if h in medoids:
                    continue
                t = swap_delta(D, medoids, info, m, h)  # @line L8
                if best is None or t < best[0]:
                    best = (t, m, h)
        if best is None or best[0] >= 0:  # @line L9
            return medoids
        t, m, h = best
        medoids[medoids.index(m)] = h  # @line L10
        if trace is not None:
            trace.append((m, h, t))


def pam(D, k, trace=None):
    """Run BUILD then SWAP. Returns (medoids, labels, cost).

    D is a symmetric n x n dissimilarity matrix with a zero diagonal; it need
    not be a metric. labels[j] is the index in medoids of the nearest medoid
    (ties to the smaller index).
    """
    n = len(D)
    if not 1 <= k <= n:
        raise ValueError("need 1 <= k <= n")
    medoids = swap(D, build(D, k), trace)
    labels = [min(range(k), key=lambda a: (D[j][medoids[a]], a)) for j in range(n)]
    return medoids, labels, total_cost(D, medoids)
