# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clustering-feature-tree/. The authors are listed in prov/0PD5NK.jsonl.

"""The CF tree of BIRCH (Zhang, Ramakrishnan and Livny).

A clustering feature CF = (N, LS, SS) holds the count, the vector sum and
the scalar sum of squared norms of a set of points. CFs add, and the
centroid, radius and diameter follow from them. A CF tree is a height
balanced tree: a nonleaf node has at most B entries (CF, child), a leaf
has at most L entries, and each leaf entry has radius at most T. The
threshold is given as t2 = T^2 so that exact arithmetic works.
"""


class CF:
    __slots__ = ("n", "ls", "ss")

    def __init__(self, n, ls, ss):
        self.n, self.ls, self.ss = n, ls, ss

    @classmethod
    def of_point(cls, x):
        return cls(1, list(x), sum(v * v for v in x))

    def __add__(self, other):
        return CF(self.n + other.n, [a + b for a, b in zip(self.ls, other.ls)], self.ss + other.ss)

    def __eq__(self, other):
        return (self.n, self.ls, self.ss) == (other.n, other.ls, other.ss)

    def centroid(self):
        return [v / self.n for v in self.ls]

    def radius_sq(self):
        """Mean squared distance of the points to the centroid."""
        return self.ss / self.n - sum((v / self.n) ** 2 for v in self.ls)

    def diameter_sq(self):
        """Mean squared distance over ordered pairs of distinct points."""
        if self.n < 2:
            return 0
        norm = sum(v * v for v in self.ls)
        return (2 * self.n * self.ss - 2 * norm) / (self.n * (self.n - 1))


def centroid_dist_sq(a, b):
    return sum((u - v) ** 2 for u, v in zip(a.centroid(), b.centroid()))


def total(entries):
    out = entries[0]
    for e in entries[1:]:
        out = out + e
    return out


class Node:
    def __init__(self, leaf):
        self.leaf = leaf
        self.entries = []   # CFs
        self.children = []  # child nodes (nonleaf only)
        self.next = None    # next leaf in the leaf chain (leaf only)


class CFTree:
    def __init__(self, B, L, t2):
        if B < 2 or L < 2:
            raise ValueError("need B >= 2 and L >= 2")
        self.B, self.L, self.t2 = B, L, t2
        self.root = Node(True)
        self.first_leaf = self.root

    def insert(self, x):
        self.insert_cf(CF.of_point(x))

    def insert_cf(self, cf):
        split = self._insert(self.root, cf)
        if split is not None:  # @line L9
            a, b = split
            root = Node(False)
            root.entries = [total(a.entries), total(b.entries)]
            root.children = [a, b]
            self.root = root

    def _closest(self, node, cf):
        return min(range(len(node.entries)), key=lambda i: (centroid_dist_sq(node.entries[i], cf), i))

    def _insert(self, node, cf):
        """Insert cf below node. Returns None, or the two halves if node split."""
        if node.leaf:
            if node.entries:
                i = self._closest(node, cf)  # @line L3
                merged = node.entries[i] + cf
                if merged.radius_sq() <= self.t2:  # @line L4
                    node.entries[i] = merged
                    return None
            node.entries.append(cf)  # @line L5
            return self._split(node) if len(node.entries) > self.L else None  # @line L6
        i = self._closest(node, cf)  # @line L1
        res = self._insert(node.children[i], cf)  # @line L2
        if res is None:
            node.entries[i] = node.entries[i] + cf  # @line L7
            return None
        a, b = res
        node.entries[i:i + 1] = [total(a.entries), total(b.entries)]  # @line L8
        node.children[i:i + 1] = [a, b]
        return self._split(node) if len(node.entries) > self.B else None

    def _split(self, node):
        """Split by the farthest pair of entries as seeds. The node keeps the
        first group and a new right sibling gets the second."""
        e = node.entries
        far = max(((centroid_dist_sq(e[i], e[j]), -i, -j) for i in range(len(e)) for j in range(i + 1, len(e))))
        s, t = -far[1], -far[2]
        left, right = [], []
        for i in range(len(e)):
            if i == s or (i != t and centroid_dist_sq(e[i], e[s]) <= centroid_dist_sq(e[i], e[t])):
                left.append(i)
            else:
                right.append(i)
        sib = Node(node.leaf)
        sib.entries = [e[i] for i in right]
        if not node.leaf:
            sib.children = [node.children[i] for i in right]
            node.children = [node.children[i] for i in left]
        node.entries = [e[i] for i in left]
        if node.leaf:
            sib.next, node.next = node.next, sib
        return node, sib

    def leaves(self):
        out, leaf = [], self.first_leaf
        while leaf is not None:
            out.append(leaf)
            leaf = leaf.next
        return out

    def leaf_entries(self):
        return [cf for leaf in self.leaves() for cf in leaf.entries]

    def node_count(self):
        stack, count = [self.root], 0
        while stack:
            node = stack.pop()
            count += 1
            stack.extend(node.children)
        return count

    def rebuild(self, t2):
        """A new tree with a larger threshold, built from the leaf entries."""
        if t2 < self.t2:
            raise ValueError("the threshold must not decrease")
        new = CFTree(self.B, self.L, t2)
        for cf in self.leaf_entries():
            new.insert_cf(cf)
        return new
