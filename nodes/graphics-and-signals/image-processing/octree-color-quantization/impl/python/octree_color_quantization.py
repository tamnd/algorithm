# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/octree-color-quantization/. The authors are listed in prov/XZM37W.jsonl.

"""Octree color quantization in the manner of Gervautz and Purgathofer.

Colors are (r, g, b) tuples of integers in [0, 2^depth). A node at level l
(the root is level 0) chooses its child by bit depth - 1 - l of r, g and b.
A leaf holds the pixel count and the sum of the colors that reached it. Each
color is inserted at once, and while there are more than k leaves, a node at
the deepest level that has children is merged into one leaf. Among those nodes
the one with the fewest pixels is merged first, and a tie goes to the node that
comes first in child order. The palette is the mean of each leaf.
"""

from fractions import Fraction


class Node:
    __slots__ = ("level", "children", "leaf", "count", "sums")

    def __init__(self, level, leaf):
        self.level = level
        self.children = [None] * 8
        self.leaf = leaf
        self.count = 0
        self.sums = [0, 0, 0]


def child_index(color, level, depth):
    bit = depth - 1 - level
    r, g, b = color
    return ((r >> bit) & 1) << 2 | ((g >> bit) & 1) << 1 | ((b >> bit) & 1)


class OctreeQuantizer:
    def __init__(self, k, depth=8):
        self.k = k
        self.depth = depth
        self.root = Node(0, depth == 0)
        self.leaves = 1 if depth == 0 else 0
        self.merges = 0

    def insert(self, color):
        node = self.root  # @line L2
        while not node.leaf:  # @line L3
            i = child_index(color, node.level, self.depth)
            if node.children[i] is None:  # @line L4
                leaf = node.level + 1 == self.depth
                node.children[i] = Node(node.level + 1, leaf)
                self.leaves += leaf
            node = node.children[i]
        node.count += 1  # @line L5
        for a in range(3):
            node.sums[a] += color[a]
        while self.leaves > self.k:  # @line L6
            self.reduce()

    def inner_nodes(self):
        """Nodes with children, in depth-first child order."""
        out, stack = [], [self.root]
        while stack:
            node = stack.pop()
            if not node.leaf:
                out.append(node)
                stack.extend(c for c in reversed(node.children) if c is not None)
        return out

    def reduce(self):
        inner = self.inner_nodes()
        deepest = max(n.level for n in inner)
        candidates = [n for n in inner if n.level == deepest]  # @line L7
        node = min(candidates, key=lambda n: sum(c.count for c in n.children if c is not None))
        kids = [c for c in node.children if c is not None]  # @line L8
        node.count = sum(c.count for c in kids)
        node.sums = [sum(c.sums[a] for c in kids) for a in range(3)]
        node.children = [None] * 8
        node.leaf = True
        self.leaves -= len(kids) - 1  # @line L9
        self.merges += 1

    def leaf_nodes(self):
        out, stack = [], [self.root]
        while stack:
            node = stack.pop()
            if node.leaf:
                if node.count:
                    out.append(node)
            else:
                stack.extend(c for c in reversed(node.children) if c is not None)
        return out

    def palette(self):
        return [tuple(Fraction(s, n.count) for s in n.sums) for n in self.leaf_nodes()]  # @line L10


def octree_quantize(colors, k, depth=8):
    """Return (palette, index of the palette color for each pixel, the tree)."""
    tree = OctreeQuantizer(k, depth)
    for c in colors:  # @line L1
        tree.insert(c)
    pal = tree.palette()
    leaves = tree.leaf_nodes()
    position = {id(n): j for j, n in enumerate(leaves)}
    index = []
    for c in colors:
        node = tree.root
        while not node.leaf:
            node = node.children[child_index(c, node.level, tree.depth)]
        index.append(position[id(node)])  # @line L11
    return pal, index, tree


def squared_distance(p, q):
    return sum((x - y) ** 2 for x, y in zip(p, q))


def total_error(colors, pal, index):
    return sum(squared_distance(c, pal[j]) for c, j in zip(colors, index))
