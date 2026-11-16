# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/j-linkage/. The authors are listed in prov/ZDYX7K.jsonl.
"""J-linkage, Toldo and Fusiello 2008, for several lines in the plane.

1. Draw M minimal samples with locality: the first point is uniform, and each
   other point x_j is drawn with probability proportional to
   exp(-|x_j - x_i|^2 / sigma^2), where x_i is the first point.
2. The preference set of a point is the set of hypotheses whose residual at
   the point is below eps (stored as a bit mask).
3. Start with one cluster per point. The preference set of a cluster is the
   intersection of the preference sets of its points. Merge the two clusters
   of least Jaccard distance while that distance is below 1.
4. Keep the clusters with at least m_min points and fit one model to each.

Lines are (a, b, c) with a x + b y + c = 0 and a^2 + b^2 = 1, s = 2.
Standard library only.
"""

import math
import random


def line_through(sample):
    """The line through two points, as (a, b, c) with a^2 + b^2 = 1, or None if they coincide."""
    (x1, y1), (x2, y2) = sample
    a, b = y1 - y2, x2 - x1
    nrm = math.hypot(a, b)
    if nrm == 0.0:
        return None
    a, b = a / nrm, b / nrm
    if a < 0 or (a == 0 and b < 0):
        a, b = -a, -b
    return (a, b, -(a * x1 + b * y1))


def point_line_distance(line, pt):
    a, b, c = line
    return abs(a * pt[0] + b * pt[1] + c)


def fit_line_tls(points):
    """Total least squares line through the centroid; None for fewer than 2 distinct points."""
    n = len(points)
    if n < 2:
        return None
    mx = sum(p[0] for p in points) / n
    my = sum(p[1] for p in points) / n
    sxx = sum((p[0] - mx) ** 2 for p in points)
    syy = sum((p[1] - my) ** 2 for p in points)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in points)
    if sxx + syy == 0.0:
        return None
    ang = 0.5 * math.atan2(2.0 * sxy, sxx - syy)  # direction of largest spread
    return line_through([(mx, my), (mx + math.cos(ang), my + math.sin(ang))])


def popcount(x):
    return bin(x).count("1")


def jaccard_distance(a, b):
    """(|A u B| - |A n B|) / |A u B| for bit masks; 1 when both are empty."""
    union = popcount(a | b)
    if union == 0:
        return 1.0
    return (union - popcount(a & b)) / union


def locality_sample(data, s, sigma, rng):
    """s distinct indices: the first uniform, the others with weight exp(-|x - x_first|^2 / sigma^2)."""
    first = rng.randrange(len(data))
    chosen = [first]
    x0 = data[first]
    rest = [j for j in range(len(data)) if j != first]
    while len(chosen) < s:
        wts = [math.exp(-((data[j][0] - x0[0]) ** 2 + (data[j][1] - x0[1]) ** 2) / (sigma * sigma)) for j in rest]
        if sum(wts) == 0.0:
            j = rng.choice(rest)
        else:
            j = rng.choices(rest, weights=wts)[0]
        chosen.append(j)
        rest.remove(j)
    return chosen


def make_hypotheses(data, M, sigma, rng, s=2, fit_minimal=line_through):
    hyps = []
    if len(data) < s:
        return hyps
    for _ in range(M):  # @line L1
        idx = locality_sample(data, s, sigma, rng)  # @line L2
        h = fit_minimal([data[j] for j in idx])  # @line L3
        if h is not None:
            hyps.append(h)
    return hyps


def preference_sets(data, hyps, eps, residual=point_line_distance):
    return [sum(1 << j for j, h in enumerate(hyps) if residual(h, x) < eps) for x in data]


def cluster(prefs, on_merge=None):
    """Agglomerative clustering by Jaccard distance. Return a list of (member indices, preference mask).

    Ties are broken by the order of the clusters, which are kept sorted by their least member.
    """
    clusters = [([i], ps) for i, ps in enumerate(prefs)]  # @line L5
    while True:  # @line L6
        best = None
        for i in range(len(clusters)):  # @line L7
            for j in range(i + 1, len(clusters)):
                d = jaccard_distance(clusters[i][1], clusters[j][1])
                if best is None or d < best[0]:
                    best = (d, i, j)
        if best is None or best[0] >= 1.0:  # @line L8
            return clusters
        d, i, j = best
        if on_merge is not None:
            on_merge(clusters[i][0], clusters[j][0], d)
        merged = (sorted(clusters[i][0] + clusters[j][0]), clusters[i][1] & clusters[j][1])  # @line L9
        clusters = [c for t, c in enumerate(clusters) if t not in (i, j)] + [merged]
        clusters.sort(key=lambda c: c[0][0])


def j_linkage(data, eps, M=500, sigma=1.0, m_min=3, rng=None, hypotheses=None, s=2,
              residual=point_line_distance, fit=fit_line_tls):
    """Return (models, clusters): one model per cluster with at least m_min points, and all clusters."""
    rng = rng if rng is not None else random.Random()
    hyps = list(hypotheses) if hypotheses is not None else make_hypotheses(data, M, sigma, rng, s)
    prefs = preference_sets(data, hyps, eps, residual)  # @line L4
    clusters = cluster(prefs)
    models = []
    for members, _ in clusters:  # @line L10
        if len(members) >= m_min:
            model = fit([data[i] for i in members])  # @line L11
            if model is not None:
                models.append((model, members))
    return models, clusters  # @line L12
