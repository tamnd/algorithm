# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boykov-jolly-graph-cuts/. The authors are listed in prov/DCZHC7.jsonl.

"""Boykov-Jolly interactive graph cuts for a gray image.

Pixel p = v * w + u is (u, v) with the gray value img[v][u]. A labeling A
gives each pixel 1 (object) or 0 (background). The energy is

    E(A) = lam * sum_p R_p(A_p) + sum_{p,q neighbors} B_pq [A_p != A_q],

with the hard constraints A_p = 1 on the object seeds O and A_p = 0 on the
background seeds G. The minimum cut of the graph of Boykov and Jolly (2001)
gives a labeling of minimum energy. The max flow is Edmonds-Karp on a small
residual graph; it can continue from an old flow after a seed is added.
"""

import itertools
import math
from collections import deque


def neighbor_pairs(w, h, eight=True):
    """Return the neighbor pairs (p, q) with p < q and their distance."""
    steps = [(1, 0), (0, 1)]
    if eight:
        steps += [(1, 1), (-1, 1)]
    out = []
    for v in range(h):
        for u in range(w):
            for du, dv in steps:
                uu, vv = u + du, v + dv
                if 0 <= uu < w and 0 <= vv < h:
                    out.append((v * w + u, vv * w + uu, math.hypot(du, dv)))
    return out


def histogram_costs(img, seeds, nbins, vmax):
    """Return -ln Pr(I_p | seeds) for every pixel, from a histogram with add-one smoothing."""
    w = len(img[0])
    counts = [0] * nbins

    def bin_of(val):
        return min(nbins - 1, int(val * nbins / (vmax + 1)))

    for p in seeds:
        counts[bin_of(img[p // w][p % w])] += 1
    total = len(seeds) + nbins
    return [-math.log((counts[bin_of(val)] + 1) / total) for row in img for val in row]


def boundary_weights(img, sigma, eight=True):
    """Return a list of (p, q, B_pq) with B_pq = exp(-(I_p - I_q)^2 / (2 sigma^2)) / dist(p, q)."""
    h, w = len(img), len(img[0])
    flat = [val for row in img for val in row]
    return [(p, q, math.exp(-((flat[p] - flat[q]) ** 2) / (2 * sigma * sigma)) / d)
            for p, q, d in neighbor_pairs(w, h, eight)]


class FlowGraph:
    """A residual graph with Edmonds-Karp augmentation that can be resumed."""

    def __init__(self, n):
        self.n = n
        self.res = [dict() for _ in range(n)]
        self.flow = 0.0

    def add_capacity(self, a, b, c):
        self.res[a][b] = self.res[a].get(b, 0.0) + c
        self.res[b].setdefault(a, 0.0)

    def max_flow(self, s, t, eps=1e-12):
        """Augment along shortest paths until no s-t path is left; return the total flow."""
        while True:
            parent = {s: None}
            queue = deque([s])
            while queue and t not in parent:
                a = queue.popleft()
                for b, c in self.res[a].items():
                    if c > eps and b not in parent:
                        parent[b] = a
                        queue.append(b)
            if t not in parent:
                return self.flow
            path = []
            b = t
            while parent[b] is not None:
                path.append((parent[b], b))
                b = parent[b]
            delta = min(self.res[a][b] for a, b in path)
            for a, b in path:
                self.res[a][b] -= delta
                self.res[b][a] += delta
            self.flow += delta

    def source_side(self, s, eps=1e-12):
        """Return the set of nodes reachable from s in the residual graph."""
        seen = {s}
        queue = deque([s])
        while queue:
            a = queue.popleft()
            for b, c in self.res[a].items():
                if c > eps and b not in seen:
                    seen.add(b)
                    queue.append(b)
        return seen


class InteractiveCut:
    """Boykov-Jolly segmentation with seeds that can be added after the first cut."""

    def __init__(self, img, obj, bkg, lam, sigma, nbins=4, vmax=255, eight=True, region=None):
        h, w = len(img), len(img[0])
        n = w * h
        self.n, self.lam = n, lam
        self.obj, self.bkg = set(obj), set(bkg)
        if self.obj & self.bkg:
            raise ValueError("a pixel cannot be an object seed and a background seed")
        if region is None:
            r_obj = histogram_costs(img, sorted(self.obj), nbins, vmax)  # @line L1
            r_bkg = histogram_costs(img, sorted(self.bkg), nbins, vmax)
        else:
            r_obj, r_bkg = region
        self.r_obj, self.r_bkg = r_obj, r_bkg
        self.pairs = boundary_weights(img, sigma, eight)  # @line L2
        deg = [0.0] * n
        for p, q, b in self.pairs:
            deg[p] += b
            deg[q] += b
        self.K = 1.0 + max(deg)  # @line L3
        self.s, self.t = n, n + 1
        g = FlowGraph(n + 2)  # @line L4
        for p, q, b in self.pairs:
            g.add_capacity(p, q, b)
            g.add_capacity(q, p, b)
        for p in range(n):
            if p in self.obj:  # @line L5
                g.add_capacity(self.s, p, self.K)
                g.add_capacity(p, self.t, 0.0)
            elif p in self.bkg:  # @line L6
                g.add_capacity(self.s, p, 0.0)
                g.add_capacity(p, self.t, self.K)
            else:  # @line L7
                g.add_capacity(self.s, p, lam * r_bkg[p])
                g.add_capacity(p, self.t, lam * r_obj[p])
        self.g = g
        self.offset = 0.0
        self.augment()

    def augment(self):
        self.g.max_flow(self.s, self.t)  # @line L8
        side = self.g.source_side(self.s)
        self.labels = [1 if p in side else 0 for p in range(self.n)]  # @line L9
        return self.labels  # @line L10

    def cut_value(self):
        """The minimum cut of the original construction, without the offsets of added seeds."""
        return self.g.flow - self.offset

    def add_seed(self, p, label):
        """Make pixel p a hard object (label 1) or background (label 0) seed and resume the flow."""
        if p in self.obj or p in self.bkg:
            if (p in self.obj) == (label == 1):
                return self.labels
            raise ValueError("pixel already has the other seed label")
        c = self.lam * (self.r_obj[p] + self.r_bkg[p])  # @line L11
        if label == 1:
            self.g.res[self.s][p] += self.K + c - self.lam * self.r_bkg[p]  # @line L12
            self.g.res[p][self.t] += c - self.lam * self.r_obj[p]
            self.obj.add(p)
        else:
            self.g.res[self.s][p] += c - self.lam * self.r_bkg[p]
            self.g.res[p][self.t] += self.K + c - self.lam * self.r_obj[p]
            self.bkg.add(p)
        self.offset += c
        return self.augment()  # @line L13


def energy(labels, r_obj, r_bkg, pairs, lam):
    """E(A) = lam * sum_p R_p(A_p) + sum B_pq [A_p != A_q]."""
    e = sum(lam * (r_obj[p] if a == 1 else r_bkg[p]) for p, a in enumerate(labels))
    return e + sum(b for p, q, b in pairs if labels[p] != labels[q])


def brute_force(n, obj, bkg, r_obj, r_bkg, pairs, lam):
    """Return the minimum energy and all minimizing labelings that satisfy the seeds."""
    free = [p for p in range(n) if p not in obj and p not in bkg]
    best, arg = math.inf, []
    for bits in itertools.product((0, 1), repeat=len(free)):
        lab = [1 if p in obj else 0 for p in range(n)]
        for p, a in zip(free, bits):
            lab[p] = a
        e = energy(lab, r_obj, r_bkg, pairs, lam)
        if e < best - 1e-9:
            best, arg = e, [lab]
        elif abs(e - best) <= 1e-9:
            arg.append(lab)
    return best, arg


def seed_constant(obj, bkg, r_obj, r_bkg, lam):
    """The energy of the seeds' region terms, which the cut does not see (Theorem 1)."""
    return sum(lam * r_obj[p] for p in obj) + sum(lam * r_bkg[p] for p in bkg)
