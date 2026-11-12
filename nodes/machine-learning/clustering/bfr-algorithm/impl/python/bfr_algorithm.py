# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bfr-algorithm/. The authors are listed in prov/G9NW7V.jsonl.

"""The BFR algorithm (Bradley, Fayyad and Reina): k-means over data read in
chunks, with a discard set (DS) of k cluster summaries, a compressed set
(CS) of mini-cluster summaries and a retained set (RS) of single points.

A summary keeps N, SUM and SUMSQ per dimension, so the centroid and the
variance in each dimension are known without the points. A point joins a
cluster when its Mahalanobis distance (with the per-dimension standard
deviations) is below alpha times sqrt(d).
"""


class Summary:
    """(N, SUM, SUMSQ) of a set of d-dimensional points."""

    def __init__(self, d, ids=None):
        self.n = 0
        self.s = [0] * d
        self.sq = [0] * d
        self.ids = ids  # a list of point ids when tracking, else None

    @classmethod
    def of(cls, x, pid=None, track=False):
        out = cls(len(x), [] if track else None)
        out.add(x, pid)
        return out

    def add(self, x, pid=None):
        self.n += 1
        for i, v in enumerate(x):
            self.s[i] += v
            self.sq[i] += v * v
        if self.ids is not None:
            self.ids.append(pid)

    def merge(self, other):
        out = Summary(len(self.s), None if self.ids is None else self.ids + other.ids)
        out.n = self.n + other.n
        out.s = [a + b for a, b in zip(self.s, other.s)]
        out.sq = [a + b for a, b in zip(self.sq, other.sq)]
        return out

    def centroid(self):
        return [v / self.n for v in self.s]

    def variance(self):
        return [q / self.n - (v / self.n) ** 2 for v, q in zip(self.s, self.sq)]


def mahalanobis_sq(x, summ, var_floor):
    """Squared Mahalanobis distance with a diagonal covariance."""
    c, var = summ.centroid(), summ.variance()
    return sum((xi - ci) ** 2 / max(vi, var_floor) for xi, ci, vi in zip(x, c, var))


def _sqdist(a, b):
    return sum((u - v) ** 2 for u, v in zip(a, b))


def lloyd(points, k, rng, iters=50, restarts=5):
    """k-means on the first chunk: Lloyd's iteration from several k-means++
    starts, keeping the clusters with the least sum of squares. Returns the
    clusters as lists of indices."""
    best = None
    for _ in range(restarts):
        groups = _lloyd_once(points, k, rng, iters)
        sse = 0
        for g in groups:
            if g:
                c = [sum(points[j][i] for j in g) / len(g) for i in range(len(points[0]))]
                sse += sum(_sqdist(points[j], c) for j in g)
        if best is None or sse < best[0]:
            best = (sse, groups)
    return best[1]


def _lloyd_once(points, k, rng, iters):
    # k-means++ seeding: each next seed with probability proportional to D^2
    centers = [list(points[rng.randrange(len(points))])]
    while len(centers) < k:
        w = [float(min(_sqdist(p, c) for c in centers)) for p in points]
        r, j = rng.random() * sum(w), 0
        while j < len(points) - 1 and r >= w[j]:
            r -= w[j]
            j += 1
        centers.append(list(points[j]))
    groups = None
    for _ in range(iters):
        new = [[] for _ in range(k)]
        for j, p in enumerate(points):
            new[min(range(k), key=lambda a: (_sqdist(p, centers[a]), a))].append(j)
        if new == groups:
            break
        groups = new
        for a, g in enumerate(groups):
            if g:
                centers[a] = [sum(points[j][i] for j in g) / len(g) for i in range(len(points[0]))]
    return groups


def _compress(items, cs_var):
    """Merge the closest pair of summaries while the merged summary has
    variance at most cs_var in every dimension (secondary compression)."""
    items = list(items)
    while True:
        best = None
        for a in range(len(items)):
            for b in range(a + 1, len(items)):
                m = items[a].merge(items[b])
                if max(m.variance()) <= cs_var:
                    key = (_sqdist(items[a].centroid(), items[b].centroid()), a, b)
                    if best is None or key < best[0]:
                        best = (key, a, b, m)
        if best is None:
            return items
        _, a, b, m = best
        items = [s for t, s in enumerate(items) if t not in (a, b)] + [m]


class BFR:
    def __init__(self, k, rng, alpha=2, cs_var=1, var_floor=1e-9, track=False):
        self.k, self.rng, self.alpha = k, rng, alpha
        self.cs_var, self.var_floor, self.track = cs_var, var_floor, track
        self.ds, self.cs, self.rs = [], [], []
        self.seen = 0

    def first_chunk(self, chunk):
        d = len(chunk[0])
        for g in lloyd(chunk, self.k, self.rng):  # @line L1
            s = Summary(d, [] if self.track else None)
            for j in g:
                s.add(chunk[j], self.seen + j)
            if s.n:
                self.ds.append(s)
        self.seen += len(chunk)

    def _near(self, x, summaries):
        """Index of the summary with the least Mahalanobis distance if that
        distance is below alpha sqrt(d), else None."""
        d = len(x)
        best = None
        for a, s in enumerate(summaries):
            m = mahalanobis_sq(x, s, self.var_floor)
            if m < self.alpha ** 2 * d and (best is None or m < best[0]):
                best = (m, a)
        return None if best is None else best[1]

    def next_chunk(self, chunk):
        new_rs = []
        for j, x in enumerate(chunk):  # @line L2
            pid = self.seen + j
            a = self._near(x, self.ds)  # @line L3
            if a is not None:
                self.ds[a].add(x, pid)  # @line L4
                continue
            b = self._near(x, self.cs)  # @line L5
            if b is not None:
                self.cs[b].add(x, pid)
            else:
                new_rs.append(Summary.of(x, pid, self.track))  # @line L6
        self.seen += len(chunk)
        merged = _compress(self.cs + self.rs + new_rs, self.cs_var)  # @line L7
        self.cs = [s for s in merged if s.n > 1]
        self.rs = [s for s in merged if s.n == 1]

    def finish(self):
        """Last round: merge each CS and RS summary into the DS cluster with
        the nearest centroid. Returns the k DS summaries."""
        for s in self.cs + self.rs:  # @line L8
            c = s.centroid()
            a = min(range(len(self.ds)), key=lambda t: (_sqdist(c, self.ds[t].centroid()), t))
            self.ds[a] = self.ds[a].merge(s)
        self.cs, self.rs = [], []
        return self.ds

    def total(self):
        return sum(s.n for s in self.ds + self.cs + self.rs)


def bfr(chunks, k, rng, **kw):
    """Run BFR on a list of chunks. rng is a random.Random for k-means."""
    algo = BFR(k, rng, **kw)
    algo.first_chunk(chunks[0])
    for ch in chunks[1:]:
        algo.next_chunk(ch)
    return algo.finish()
