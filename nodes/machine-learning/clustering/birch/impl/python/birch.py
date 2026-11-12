# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/birch/. The authors are listed in prov/3BD165.jsonl.

"""BIRCH (Zhang, Ramakrishnan and Livny): phase 1 builds a CF tree in one
scan and rebuilds it with a larger threshold when it has too many leaf
entries; phase 3 clusters the leaf entries with agglomerative (Ward)
clustering on the clustering features; phase 4 assigns each point to the
nearest phase 3 centroid in a second scan. Phase 2 (condensing) is
optional and is done here by the same rebuild rule.
"""


class CF:
    __slots__ = ("n", "ls", "ss")

    def __init__(self, n, ls, ss):
        self.n, self.ls, self.ss = n, ls, ss

    @classmethod
    def of_point(cls, x):
        return cls(1, list(x), sum(v * v for v in x))

    def __add__(self, o):
        return CF(self.n + o.n, [a + b for a, b in zip(self.ls, o.ls)], self.ss + o.ss)

    def __eq__(self, o):
        return (self.n, self.ls, self.ss) == (o.n, o.ls, o.ss)

    def centroid(self):
        return [v / self.n for v in self.ls]

    def radius_sq(self):
        return self.ss / self.n - sum((v / self.n) ** 2 for v in self.ls)

    def sse(self):
        """Sum of squared distances of the points to their centroid."""
        return self.ss - sum(v * v for v in self.ls) / self.n


def sqdist(a, b):
    return sum((u - v) ** 2 for u, v in zip(a, b))


def ward_increase(a, b):
    """Increase of the sum of squares when the clusters a and b are joined."""
    return a.n * b.n * sqdist(a.centroid(), b.centroid()) / (a.n + b.n)


def total(cfs):
    out = cfs[0]
    for c in cfs[1:]:
        out = out + c
    return out


class _Node:
    def __init__(self, leaf):
        self.leaf, self.entries, self.children = leaf, [], []


class CFTree:
    """A CF tree with branching factor B, leaf size L and threshold T^2 = t2."""

    def __init__(self, B, L, t2):
        self.B, self.L, self.t2 = B, L, t2
        self.root = _Node(True)

    def insert_cf(self, cf):
        res = self._insert(self.root, cf)
        if res:
            root = _Node(False)
            root.entries = [total(h.entries) for h in res]
            root.children = list(res)
            self.root = root

    def _closest(self, node, cf):
        c = cf.centroid()
        return min(range(len(node.entries)), key=lambda i: (sqdist(node.entries[i].centroid(), c), i))

    def _insert(self, node, cf):
        if node.leaf:
            if node.entries:
                i = self._closest(node, cf)
                m = node.entries[i] + cf
                if m.radius_sq() <= self.t2:
                    node.entries[i] = m
                    return None
            node.entries.append(cf)
            return self._split(node) if len(node.entries) > self.L else None
        i = self._closest(node, cf)
        res = self._insert(node.children[i], cf)
        if res is None:
            node.entries[i] = node.entries[i] + cf
            return None
        node.entries[i:i + 1] = [total(h.entries) for h in res]
        node.children[i:i + 1] = list(res)
        return self._split(node) if len(node.entries) > self.B else None

    def _split(self, node):
        e = node.entries
        cs = [x.centroid() for x in e]
        _, s, t = max((sqdist(cs[i], cs[j]), -i, -j) for i in range(len(e)) for j in range(i + 1, len(e)))
        s, t = -s, -t
        left = [i for i in range(len(e)) if i == s or (i != t and sqdist(cs[i], cs[s]) <= sqdist(cs[i], cs[t]))]
        right = [i for i in range(len(e)) if i not in left]
        halves = []
        for part in (left, right):
            h = _Node(node.leaf)
            h.entries = [e[i] for i in part]
            if not node.leaf:
                h.children = [node.children[i] for i in part]
            halves.append(h)
        return halves

    def leaves(self):
        out, stack = [], [self.root]
        while stack:
            node = stack.pop()
            if node.leaf:
                out.append(node)
            else:
                stack.extend(reversed(node.children))
        return out

    def leaf_entries(self):
        return [cf for leaf in self.leaves() for cf in leaf.entries]


def _next_threshold(tree):
    """A larger T^2: the least radius^2 of a merge of two entries of the same
    leaf, and at least twice the old value."""
    best = None
    for leaf in tree.leaves():
        e = leaf.entries
        for i in range(len(e)):
            for j in range(i + 1, len(e)):
                r = (e[i] + e[j]).radius_sq()
                if best is None or r < best:
                    best = r
    if best is None or best <= tree.t2:
        e = tree.leaf_entries()
        pos = [r for r in ((e[i] + e[j]).radius_sq() for i in range(len(e)) for j in range(i + 1, len(e)))
               if r > tree.t2]
        best = min(pos) if pos else tree.t2 + 1
    return max(best, 2 * tree.t2)


def phase1(points, B, L, max_entries, t2=0):
    """Build a CF tree in one scan, keeping at most max_entries leaf entries."""
    tree = CFTree(B, L, t2)  # @line L1
    rebuilds = 0
    for x in points:  # @line L2
        tree.insert_cf(CF.of_point(x))
        while len(tree.leaf_entries()) > max_entries:  # @line L3
            new = CFTree(B, L, _next_threshold(tree))  # @line L4
            for cf in tree.leaf_entries():
                new.insert_cf(cf)
            tree = new
            rebuilds += 1
    return tree, rebuilds


def phase3(entries, k):
    """Agglomerative clustering of the leaf CFs by the least Ward increase.
    Returns k CFs and, for each cluster, the indices of its entries."""
    clusters = [(cf, [i]) for i, cf in enumerate(entries)]  # @line L5
    while len(clusters) > k:
        _, a, b = min((ward_increase(clusters[a][0], clusters[b][0]), a, b)
                      for a in range(len(clusters)) for b in range(a + 1, len(clusters)))  # @line L6
        merged = (clusters[a][0] + clusters[b][0], clusters[a][1] + clusters[b][1])
        clusters = [c for t, c in enumerate(clusters) if t not in (a, b)] + [merged]
    return clusters


def phase4(points, centroids):
    """One scan: label each point with the nearest centroid, then recompute
    the centroids. Returns (labels, new centroids)."""
    k = len(centroids)
    labels = [min(range(k), key=lambda a: (sqdist(x, centroids[a]), a)) for x in points]  # @line L7
    new = []
    for a in range(k):
        members = [x for x, l in zip(points, labels) if l == a]
        new.append(total([CF.of_point(x) for x in members]).centroid() if members else centroids[a])  # @line L8
    return labels, new


def birch(points, k, B=4, L=4, max_entries=50, refine_passes=1):
    """Run phases 1, 3 and 4. Returns (labels, centroids)."""
    tree, _ = phase1(points, B, L, max_entries)
    entries = tree.leaf_entries()
    clusters = phase3(entries, min(k, len(entries)))
    centroids = [cf.centroid() for cf, _ in clusters]
    labels = None
    for _ in range(refine_passes):
        labels, centroids = phase4(points, centroids)
    return labels, centroids
