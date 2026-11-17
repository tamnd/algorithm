# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vocabulary-tree/. The authors are listed in prov/3BRV2P.jsonl.
"""The vocabulary tree of Nister and Stewenius (2006).

A tree with branch factor k and depth L, built by hierarchical k-means.
A descriptor is quantized by greedy descent: at each node, go to the child
with the nearest center (ties to the smaller index). Each node i has the
weight w_i = ln(N / N_i), where N is the number of database images and N_i
the number of images with at least one descriptor through node i. An image
is the vector of n_i w_i over the nodes (n_i descriptors through node i),
normalized to L1 norm 1. The score of a database image d for a query q is
||q - d||_1 = 2 + sum over the nodes in both of (|q_i - d_i| - q_i - d_i),
which the inverted files compute from the nodes the query uses.
Standard library only.
"""

import math
import random


def sq_dist(a, b):
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def mean(points):
    n = len(points)
    return [sum(p[j] for p in points) / n for j in range(len(points[0]))]


def nearest(x, centers):
    """Index of the nearest center, ties to the smaller index."""
    best, best_d = 0, sq_dist(x, centers[0])
    for j in range(1, len(centers)):
        d = sq_dist(x, centers[j])
        if d < best_d:
            best, best_d = j, d
    return best


def kmeans(points, k, rng, iters=50):
    """Lloyd iterations from k distinct points chosen at random; an empty cluster keeps its center."""
    distinct = sorted(set(tuple(p) for p in points))
    centers = [list(c) for c in rng.sample(distinct, k)]
    for _ in range(iters):
        groups = [[] for _ in range(k)]
        for p in points:
            groups[nearest(p, centers)].append(p)
        new = [mean(g) if g else centers[j] for j, g in enumerate(groups)]
        if new == centers:
            break
        centers = new
    groups = [[] for _ in range(k)]
    for p in points:
        groups[nearest(p, centers)].append(p)
    return centers, groups


def node(center, children=()):
    return {"center": list(center), "children": list(children)}


def build(points, k, L, seed=0):
    """Hierarchical k-means: a tree of depth at most L and branch factor at most k."""
    rng = random.Random(seed)

    def rec(pts, depth):
        center = mean(pts)  # @line L1
        if depth == L or len(set(tuple(p) for p in pts)) < k:  # @line L2
            return node(center)
        _, groups = kmeans(pts, k, rng)  # @line L3
        kids = [rec(g, depth + 1) for g in groups if g]  # @line L4
        return node(center, kids)  # @line L5

    return rec(points, 0)


class VocabularyTree:
    def __init__(self, root):
        self.root = root
        self.nodes = []
        self.leaves = []
        stack = [root]
        while stack:
            nd = stack.pop()
            nd["id"] = len(self.nodes)
            self.nodes.append(nd)
            if nd["children"]:
                stack.extend(reversed(nd["children"]))
            else:
                nd["word"] = len(self.leaves)
                self.leaves.append(nd)
        self.inverted = {}
        self.weights = {}
        self.N = 0
        self.norms = {}

    def path(self, x):
        """Node ids from the root to the leaf that greedy descent reaches."""
        nd = self.root  # @line L6
        out = [nd["id"]]
        while nd["children"]:  # @line L7
            kids = nd["children"]
            nd = kids[nearest(x, [c["center"] for c in kids])]  # @line L8
            out.append(nd["id"])
        return out  # @line L9

    def quantize(self, x):
        return self.nodes[self.path(x)[-1]]["word"]

    def counts(self, descriptors):
        n = {}
        for x in descriptors:
            for i in self.path(x):
                n[i] = n.get(i, 0) + 1
        return n

    def index(self, images):
        """images: dict id -> list of descriptors. Builds the weights and the inverted files."""
        self.N = len(images)
        raw = {d: self.counts(xs) for d, xs in images.items()}
        df = {}
        for n in raw.values():
            for i in n:
                df[i] = df.get(i, 0) + 1
        self.weights = {i: math.log(self.N / df[i]) for i in df}
        self.inverted = {}
        self.nonzero = set()
        for d, n in raw.items():
            vec = self.normalize({i: c * self.weights[i] for i, c in n.items()})
            if vec:
                self.nonzero.add(d)
            for i, val in vec.items():
                self.inverted.setdefault(i, {})[d] = val
        self.ids = list(images)

    def normalize(self, vec):
        s = sum(abs(t) for t in vec.values())
        return {i: t / s for i, t in vec.items() if t != 0} if s > 0 else {}

    def vector(self, descriptors):
        n = self.counts(descriptors)
        return self.normalize({i: c * self.weights.get(i, 0.0) for i, c in n.items()})

    def scores(self, descriptors):
        """L1 distance of the query vector to each database vector, by the inverted files."""
        q = self.vector(descriptors)
        acc = {d: 0.0 for d in self.ids}
        for i, qi in q.items():
            for d, di in self.inverted.get(i, {}).items():
                acc[d] += abs(qi - di) - qi - di
        has_q = 1.0 if q else 0.0
        out = {}
        for d in self.ids:
            out[d] = has_q + (1.0 if d in self.nonzero else 0.0) + acc[d]
        return out

    def query(self, descriptors, top=None):
        s = self.scores(descriptors)
        ranked = sorted(self.ids, key=lambda d: (s[d], str(d)))
        return [(s[d], d) for d in (ranked if top is None else ranked[:top])]
