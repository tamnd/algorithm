# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bsp-tree/. The authors are listed in prov/MSZB1N.jsonl.

import random
from fractions import Fraction
from typing import Optional, Sequence

Num = Fraction
Point = tuple[Fraction, Fraction]
Segment = tuple[Point, Point]


def _pt(p: Sequence[object]) -> Point:
    return (Fraction(p[0]), Fraction(p[1]))  # type: ignore[arg-type]


def side(seg: Segment, p: Point) -> Fraction:
    """Twice the signed area of (seg[0], seg[1], p): > 0 left (front), < 0 right (back)."""
    (ax, ay), (bx, by) = seg
    return (bx - ax) * (p[1] - ay) - (by - ay) * (p[0] - ax)


class Node:
    """A node of the BSP tree: the line through `line`, the segments on it,
    and the subtrees for the open front (left) and back (right) half-planes."""

    __slots__ = ("line", "on", "front", "back")

    def __init__(self, line: Segment) -> None:
        self.line = line
        self.on: list[Segment] = [line]
        self.front: Optional[Node] = None
        self.back: Optional[Node] = None


def split(line: Segment, s: Segment) -> tuple[Optional[Segment], Optional[Segment], bool]:
    """Classify s against the line: (front part, back part, lies on the line). O(1)."""
    p, q = s
    sp, sq = side(line, p), side(line, q)
    if sp == 0 and sq == 0:
        return None, None, True
    if sp >= 0 and sq >= 0:
        return s, None, False
    if sp <= 0 and sq <= 0:
        return None, s, False
    t = sp / (sp - sq)  # the parameter where s crosses the line, 0 < t < 1
    m = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
    if sp > 0:
        return (p, m), (m, q), False
    return (m, q), (p, m), False


class BspTree:
    """A binary space partition of a set of segments in the plane (an autopartition).

    Each node splits by the line through one of the input segments. Invariant:
    every fragment in the front subtree of a node lies in the closed front
    half-plane of the node's line, every fragment in the back subtree in the
    closed back half-plane, and the fragments of the node itself lie on the line.
    Coordinates are exact rationals.
    """

    def __init__(self, segments: Sequence[Sequence[Sequence[object]]] = (), seed: Optional[int] = None) -> None:
        """Build the tree, using the segments in the given order, or in a random
        order when seed is given (expected O(n log n) fragments). O(n^2) worst time."""
        segs = [(_pt(s[0]), _pt(s[1])) for s in segments]
        for a, b in segs:
            if a == b:
                raise ValueError("a segment has length zero")
        if seed is not None:
            random.Random(seed).shuffle(segs)
        self.root = self._build(segs)

    @staticmethod
    def _build(segs: list[Segment]) -> Optional[Node]:
        root: Optional[Node] = None
        # Each task: (list of segments, parent node, True if front child).
        stack: list[tuple[list[Segment], Optional[Node], bool]] = [(segs, None, True)]
        while stack:
            group, parent, is_front = stack.pop()
            if not group:  # @line L1
                continue
            s = group[0]  # @line L2
            t = Node(s)  # @line L3
            front: list[Segment] = []  # @line L4
            back: list[Segment] = []
            for r in group[1:]:  # @line L5
                f, b, on = split(s, r)
                if on:  # @line L6
                    t.on.append(r)
                elif b is None:  # @line L7
                    front.append(r)
                elif f is None:
                    back.append(r)
                else:  # @line L8: r crosses the line and is cut in two
                    front.append(f)
                    back.append(b)
            if parent is None:
                root = t
            elif is_front:
                parent.front = t
            else:
                parent.back = t
            stack.append((back, t, False))  # @line L9
            stack.append((front, t, True))
        return root

    def insert(self, seg: Sequence[Sequence[object]]) -> None:
        """Filter a segment down the tree, cutting it at node lines. O(size of the tree) worst."""
        s0 = (_pt(seg[0]), _pt(seg[1]))
        if s0[0] == s0[1]:
            raise ValueError("a segment has length zero")
        if self.root is None:
            self.root = Node(s0)
            return
        stack: list[tuple[Segment, Node]] = [(s0, self.root)]
        while stack:
            s, t = stack.pop()
            f, b, on = split(t.line, s)
            if on:
                t.on.append(s)
                continue
            for part, is_front in ((f, True), (b, False)):
                if part is None:
                    continue
                child = t.front if is_front else t.back
                if child is None:
                    n = Node(part)
                    if is_front:
                        t.front = n
                    else:
                        t.back = n
                else:
                    stack.append((part, child))

    def back_to_front(self, v: Sequence[object]) -> list[Segment]:
        """The fragments in an order in which no fragment hides a later one from v
        (the painter's order). O(size of the tree)."""
        eye = _pt(v)
        out: list[Segment] = []
        # A task is a node to expand, or a list of fragments to output.
        stack: list[object] = [self.root]
        while stack:
            x = stack.pop()
            if x is None:  # @line L10
                continue
            if isinstance(x, list):
                out.extend(x)
                continue
            assert isinstance(x, Node)
            d = side(x.line, eye)
            if d > 0:  # @line L11: v is in front: back first, then the node, then front
                stack.extend([x.front, x.on, x.back])
            elif d < 0:  # @line L12: v is behind: front first
                stack.extend([x.back, x.on, x.front])
            else:  # @line L13: v is on the line; the node's segments are seen edge on
                stack.extend([x.back, x.on, x.front])
        return out

    def fragments(self) -> list[Segment]:
        out: list[Segment] = []
        stack = [self.root]
        while stack:
            t = stack.pop()
            if t is not None:
                out.extend(t.on)
                stack.extend([t.front, t.back])
        return out

    def size(self) -> int:
        """The number of fragments stored."""
        return len(self.fragments())

    def height(self) -> int:
        best = 0
        stack = [(self.root, 1)]
        while stack:
            t, d = stack.pop()
            if t is not None:
                best = max(best, d)
                stack.extend([(t.front, d + 1), (t.back, d + 1)])
        return best

    def check_invariant(self) -> None:
        """Check that each fragment lies on the correct side of each ancestor line."""
        stack: list[tuple[Optional[Node], list[tuple[Segment, int]]]] = [(self.root, [])]
        while stack:
            t, cons = stack.pop()
            if t is None:
                continue
            for s in t.on:
                assert s[0] != s[1]
                assert side(t.line, s[0]) == 0 and side(t.line, s[1]) == 0
                for line, sign in cons:
                    for p in s:
                        assert side(line, p) * sign >= 0
            stack.append((t.front, cons + [(t.line, 1)]))
            stack.append((t.back, cons + [(t.line, -1)]))
