# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/region-quadtree/. The authors are listed in prov/74TKQQ.jsonl.
"""Region quadtree of a 2^D by 2^D binary image.

A node is either a leaf, stored as the int 0 (white) or 1 (black), or an
internal node, stored as a list of four children in the order NW, NE, SW, SE.
The child index of pixel (x, y) in a block of side s with origin (x0, y0) is
2 * (y >= y0 + s/2) + (x >= x0 + s/2). Row y = 0 is the top row.
The tree is kept *maximal*: no internal node has four leaf children of one
color.
"""

from __future__ import annotations

from typing import List, Union

Node = Union[int, list]


def _merge(children: list) -> Node:
    """Return a leaf if the four children are equal leaves, else the list."""
    a = children[0]
    if isinstance(a, int) and all(c == a for c in children):  # @line L4
        return a
    return children  # @line L5


def build(image: List[List[int]]) -> Node:
    """Build the region quadtree bottom up, level by level, in O(N^2) time."""
    n = len(image)
    if n == 0 or n & (n - 1) or any(len(row) != n for row in image):
        raise ValueError("image must be square with a power-of-two side")
    level: List[List[Node]] = [[1 if image[y][x] else 0 for x in range(n)]
                               for y in range(n)]  # @line L1
    s = n
    while s > 1:  # @line L2
        h = s // 2
        nxt: List[List[Node]] = []
        for y in range(h):
            row: List[Node] = []
            for x in range(h):
                kids = [level[2 * y][2 * x], level[2 * y][2 * x + 1],
                        level[2 * y + 1][2 * x], level[2 * y + 1][2 * x + 1]]  # @line L3
                row.append(_merge(kids))
            nxt.append(row)
        level = nxt
        s = h
    return level[0][0]


class RegionQuadTree:
    def __init__(self, image: List[List[int]]) -> None:
        self.n = len(image)
        self.root: Node = build(image)

    def get(self, x: int, y: int) -> int:
        """Color of pixel (x, y)."""
        if not (0 <= x < self.n and 0 <= y < self.n):
            raise IndexError("pixel outside the image")
        node, s, x0, y0 = self.root, self.n, 0, 0
        while not isinstance(node, int):  # @line L6
            s //= 2
            q = 2 * (y >= y0 + s) + (x >= x0 + s)  # @line L7
            x0 += s if q & 1 else 0
            y0 += s if q & 2 else 0
            node = node[q]
        return node  # @line L8

    def set(self, x: int, y: int, color: int) -> None:
        """Set pixel (x, y) to color, splitting and merging as needed."""
        if not (0 <= x < self.n and 0 <= y < self.n):
            raise IndexError("pixel outside the image")
        color = 1 if color else 0
        if self.get(x, y) == color:  # @line L9
            return
        if isinstance(self.root, int):
            self.root = [self.root] * 4 if self.n > 1 else color
            if self.n == 1:
                return
        path: List[tuple] = []  # (parent list, index)
        node, s, x0, y0 = self.root, self.n, 0, 0
        while s > 1:  # @line L10
            s //= 2
            q = 2 * (y >= y0 + s) + (x >= x0 + s)
            x0 += s if q & 1 else 0
            y0 += s if q & 2 else 0
            child = node[q]
            if isinstance(child, int) and s > 1:
                child = [child] * 4  # @line L11
                node[q] = child
            path.append((node, q))
            node = child
        parent, q = path[-1]
        parent[q] = color  # @line L12
        for i in range(len(path) - 1, 0, -1):  # @line L13
            p, pq = path[i - 1]
            p[pq] = _merge(path[i][0])
        self.root = _merge(self.root)

    def black_area(self) -> int:
        """Number of black pixels, from the leaves."""
        total = 0
        stack = [(self.root, self.n)]
        while stack:
            node, s = stack.pop()
            if isinstance(node, int):
                total += node * s * s
            else:
                for c in node:
                    stack.append((c, s // 2))
        return total

    def leaf_count(self) -> int:
        cnt, stack = 0, [self.root]
        while stack:
            node = stack.pop()
            if isinstance(node, int):
                cnt += 1
            else:
                stack.extend(node)
        return cnt

    def node_count(self) -> int:
        cnt, stack = 0, [self.root]
        while stack:
            node = stack.pop()
            cnt += 1
            if not isinstance(node, int):
                stack.extend(node)
        return cnt

    def to_image(self) -> List[List[int]]:
        img = [[0] * self.n for _ in range(self.n)]
        stack = [(self.root, 0, 0, self.n)]
        while stack:
            node, x0, y0, s = stack.pop()
            if isinstance(node, int):
                if node:
                    for y in range(y0, y0 + s):
                        for x in range(x0, x0 + s):
                            img[y][x] = 1
            else:
                h = s // 2
                for q in range(4):
                    stack.append((node[q], x0 + h * (q & 1), y0 + h * (q >> 1), h))
        return img

    def check_invariant(self) -> None:
        """Every internal node has four children and is not mergeable."""
        stack = [(self.root, self.n)]
        while stack:
            node, s = stack.pop()
            if isinstance(node, int):
                assert node in (0, 1)
                continue
            assert s > 1 and len(node) == 4
            assert not (isinstance(node[0], int)
                        and all(c == node[0] for c in node)), "mergeable node"
            for c in node:
                stack.append((c, s // 2))


def union(a: Node, b: Node) -> Node:
    """Union of two region quadtrees of the same image size."""
    if a == 1 or b == 1:  # @line L14
        return 1
    if a == 0:  # @line L15
        return b
    if b == 0:
        return a
    return _merge([union(a[i], b[i]) for i in range(4)])  # @line L16


def intersection(a: Node, b: Node) -> Node:
    """Intersection of two region quadtrees of the same image size."""
    if a == 0 or b == 0:
        return 0
    if a == 1:
        return b
    if b == 1:
        return a
    return _merge([intersection(a[i], b[i]) for i in range(4)])  # @line L17
