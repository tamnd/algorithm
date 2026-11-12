# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frustum-culling/. The authors are listed in prov/F4J7C6.jsonl.

"""Hierarchical view-frustum culling of axis-aligned boxes.

The frustum is a list of planes (n, d). A point x is inside a plane when
n . x + d >= 0, so each normal n points into the frustum. An object is an
axis-aligned box (lo, hi) with lo[k] <= hi[k]. The objects are put in a
bounding volume hierarchy, and the traversal tests each node box against
the planes that are still active: the p-vertex (the corner farthest along n)
decides if the box is wholly outside a plane, and the n-vertex (the nearest
corner) decides if it is wholly inside, so the plane can be dropped for the
whole subtree. With int or Fraction input every sign is exact.
"""

from fractions import Fraction
from typing import Optional, Sequence, Union

Num = Union[int, Fraction]
Vec = tuple
Plane = tuple  # (n, d) with n a 3-tuple
Box = tuple  # (lo, hi) with lo and hi 3-tuples


class Node:
    """A node of the hierarchy: its box, and either children or objects."""

    __slots__ = ("lo", "hi", "children", "objects")

    def __init__(self, lo, hi, children, objects):
        self.lo, self.hi = lo, hi
        self.children: list = children
        self.objects: list[int] = objects


def union_box(boxes: Sequence[Box], idx: Sequence[int]) -> Box:
    lo = tuple(min(boxes[i][0][k] for i in idx) for k in range(3))
    hi = tuple(max(boxes[i][1][k] for i in idx) for k in range(3))
    return lo, hi


def build_bvh(boxes: Sequence[Box], leaf_size: int = 2) -> Optional[Node]:
    """Median split on the longest axis of the node box, with an explicit stack."""
    if not boxes:
        return None
    root = Node(*union_box(boxes, range(len(boxes))), [], list(range(len(boxes))))
    stack = [root]
    while stack:
        v = stack.pop()
        if len(v.objects) <= leaf_size:
            continue
        axis = max(range(3), key=lambda k: v.hi[k] - v.lo[k])
        idx = sorted(v.objects, key=lambda i: (boxes[i][0][axis] + boxes[i][1][axis], i))
        half = len(idx) // 2
        for part in (idx[:half], idx[half:]):
            child = Node(*union_box(boxes, part), [], part)
            v.children.append(child)
            stack.append(child)
        v.objects = []
    return root


def p_vertex(lo, hi, n):
    """The corner of the box that is farthest in the direction n."""
    return tuple(hi[k] if n[k] >= 0 else lo[k] for k in range(3))


def n_vertex(lo, hi, n):
    """The corner of the box that is farthest in the direction -n."""
    return tuple(lo[k] if n[k] >= 0 else hi[k] for k in range(3))


def value(plane: Plane, x) -> Num:
    n, d = plane
    return n[0] * x[0] + n[1] * x[1] + n[2] * x[2] + d


def classify(lo, hi, planes: Sequence[Plane], active: Sequence[int]):
    """Return None if the box is wholly outside a plane, else the planes it still straddles."""
    left = []
    for j in active:  # @line L4
        if value(planes[j], p_vertex(lo, hi, planes[j][0])) < 0:  # @line L5
            return None  # @line L6
        if value(planes[j], n_vertex(lo, hi, planes[j][0])) < 0:  # @line L7
            left.append(j)
    return left


def subtree_objects(v: Node) -> list[int]:
    out, stack = [], [v]
    while stack:
        u = stack.pop()
        out.extend(u.objects)
        stack.extend(u.children)
    return out


def frustum_cull(root: Optional[Node], boxes: Sequence[Box], planes: Sequence[Plane]) -> list[int]:
    """Return the sorted indices of the boxes that are not proved to be outside the frustum."""
    kept: list[int] = []  # @line L1
    stack = [(root, list(range(len(planes))))] if root is not None else []
    while stack:  # @line L2
        v, active = stack.pop()  # @line L3
        left = classify(v.lo, v.hi, planes, active)
        if left is None:
            continue
        if not left:  # @line L8
            kept.extend(subtree_objects(v))  # the box is wholly inside the frustum
            continue
        if not v.children:  # @line L9
            for i in v.objects:  # @line L10
                if classify(boxes[i][0], boxes[i][1], planes, left) is not None:
                    kept.append(i)
        else:
            for child in v.children:  # @line L11
                stack.append((child, left))
    return sorted(kept)  # @line L12


def frustum_planes(eye, left, right, bottom, top, near, far) -> list[Plane]:
    """The six inward planes of a view frustum with apex `eye` that looks down -z.

    At the distance `near` the window is [left, right] x [bottom, top].
    """
    ex, ey, ez = eye
    raw = [
        ((near, 0, left), 0),  # x - ex >= left * (ez - z) / near
        ((-near, 0, -right), 0),  # x - ex <= right * (ez - z) / near
        ((0, near, bottom), 0),
        ((0, -near, -top), 0),
        ((0, 0, -1), -near),  # z - ez <= -near
        ((0, 0, 1), far),  # z - ez >= -far
    ]
    return [(n, d - (n[0] * ex + n[1] * ey + n[2] * ez)) for n, d in raw]
