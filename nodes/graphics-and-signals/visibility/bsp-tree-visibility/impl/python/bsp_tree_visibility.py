# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bsp-tree-visibility/. The authors are listed in prov/Q78XXG.jsonl.

"""Hidden surface removal with a BSP tree of convex polygons in space.

A polygon is a list of at least three vertices (x, y, z), int or
Fraction, of a planar convex polygon. The viewer is a point E. Pixel
(i, j) is the point sample S = (i + 1/2, j + 1/2, 0) on the image plane
z = 0, and the pixel shows the nearest polygon that the ray E + t (S - E),
t > 0, meets. A polygon whose plane holds the ray is seen edge on and
covers no pixel. All arithmetic is exact.
"""

from fractions import Fraction
from typing import Optional, Sequence, Union

Num = Union[int, Fraction]
Vec = tuple[Fraction, Fraction, Fraction]


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Vec, b: Vec) -> Fraction:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


class Fragment:
    """A convex piece of input polygon `orig`."""

    __slots__ = ("verts", "orig", "n", "d")

    def __init__(self, verts: list[Vec], orig: int, plane: Optional[tuple[Vec, Fraction]] = None):
        self.verts, self.orig = verts, orig
        if plane is None:
            n = cross(sub(verts[1], verts[0]), sub(verts[2], verts[0]))
            plane = (n, dot(n, verts[0]))
        self.n, self.d = plane

    def plane(self) -> tuple[Vec, Fraction]:
        return self.n, self.d


class Node:
    __slots__ = ("n", "d", "on", "front", "back")

    def __init__(self, n: Vec, d: Fraction):
        self.n, self.d = n, d
        self.on: list[Fragment] = []
        self.front: Optional[Node] = None
        self.back: Optional[Node] = None

    def side(self, v: Vec) -> Fraction:
        return dot(self.n, v) - self.d


def cut(f: Fragment, t: Node) -> tuple[Fragment, Fragment]:
    """Split f, which has vertices strictly on both sides of the plane of t."""
    front: list[Vec] = []
    back: list[Vec] = []
    k = len(f.verts)
    for i in range(k):
        a, b = f.verts[i], f.verts[(i + 1) % k]
        sa, sb = t.side(a), t.side(b)
        if sa >= 0:
            front.append(a)
        if sa <= 0:
            back.append(a)
        if (sa > 0 > sb) or (sa < 0 < sb):
            r = sa / (sa - sb)
            m = (a[0] + r * (b[0] - a[0]), a[1] + r * (b[1] - a[1]), a[2] + r * (b[2] - a[2]))
            front.append(m)
            back.append(m)
    return Fragment(front, f.orig, f.plane()), Fragment(back, f.orig, f.plane())


def build_bsp(polygons: Sequence[Sequence[Sequence[Num]]]) -> Optional[Node]:
    """Build an autopartition: each node uses the plane of the first fragment of its group.

    This is BUILD of the BSP tree page, in space. An explicit stack replaces
    the recursion. Cost O(m) per node for m fragments in the tree.
    """
    frags = [Fragment([(Fraction(x), Fraction(y), Fraction(z)) for x, y, z in p], k) for k, p in enumerate(polygons)]
    root: list[Optional[Node]] = [None]
    stack: list[tuple[list[Fragment], object, str]] = [(frags, root, "root")]
    while stack:
        group, parent, slot = stack.pop()
        if not group:
            continue
        n, d = group[0].plane()
        if n == (0, 0, 0):
            raise ValueError("a polygon has collinear first three vertices")
        t = Node(n, d)
        if slot == "root":
            root[0] = t
        else:
            setattr(parent, slot, t)
        t.on.append(group[0])
        fr: list[Fragment] = []
        bk: list[Fragment] = []
        for r in group[1:]:
            s = [t.side(v) for v in r.verts]
            if all(x == 0 for x in s):
                t.on.append(r)
            elif all(x >= 0 for x in s):
                fr.append(r)
            elif all(x <= 0 for x in s):
                bk.append(r)
            else:
                a, b = cut(r, t)
                fr.append(a)
                bk.append(b)
        stack.append((fr, t, "front"))
        stack.append((bk, t, "back"))
    return root[0]


def ray_hit(f: Fragment, eye: Vec, s: Vec) -> Optional[Fraction]:
    """The parameter t > 0 where the ray eye + t (s - eye) meets f, or None."""
    n, d = f.plane()
    dirv = sub(s, eye)
    den = dot(n, dirv)
    if den == 0:
        return None
    t = (d - dot(n, eye)) / den
    if t <= 0:
        return None
    x = (eye[0] + t * dirv[0], eye[1] + t * dirv[1], eye[2] + t * dirv[2])
    pos = neg = False
    k = len(f.verts)
    for i in range(k):
        c = dot(n, cross(sub(f.verts[(i + 1) % k], f.verts[i]), sub(x, f.verts[i])))
        pos, neg = pos or c > 0, neg or c < 0
    return None if pos and neg else t


def samples(width: int, height: int) -> list[tuple[int, int, Vec]]:
    return [(i, j, (Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2), Fraction(0)))
            for j in range(height) for i in range(width)]


def bsp_paint(tree: Optional[Node], eye: Sequence[Num], width: int, height: int,
              background: int = -1) -> tuple[list[Fragment], list[list[int]]]:
    """Paint the fragments back to front as seen from `eye`.

    Returns (order, image); image[j][i] is the input index of the last
    fragment painted at pixel (i, j). Cost O(m) for the traversal, plus the
    painting.
    """
    e = (Fraction(eye[0]), Fraction(eye[1]), Fraction(eye[2]))
    pix = samples(width, height)
    image = [[background] * width for _ in range(height)]
    order: list[Fragment] = []
    stack: list[tuple[Optional[Node], bool]] = [(tree, False)]  # @line L1
    while stack:  # @line L2
        t, draw = stack.pop()  # @line L3
        if t is None:  # @line L4
            continue
        if draw:  # @line L5
            for f in t.on:
                order.append(f)
                for i, j, s in pix:
                    if ray_hit(f, e, s) is not None:
                        image[j][i] = f.orig
            continue
        if t.side(e) >= 0:  # @line L6
            near, far = t.front, t.back
        else:
            near, far = t.back, t.front
        stack += [(near, False), (t, True), (far, False)]  # @line L7
    return order, image


def bsp_front_to_back(tree: Optional[Node], eye: Sequence[Num], width: int, height: int,
                      background: int = -1) -> tuple[int, list[list[int]]]:
    """Draw front to back, write only empty pixels, and stop when all are full.

    Returns (the number of fragments drawn, image).
    """
    e = (Fraction(eye[0]), Fraction(eye[1]), Fraction(eye[2]))
    pix = samples(width, height)
    image = [[background] * width for _ in range(height)]
    written = [[False] * width for _ in range(height)]
    filled, drawn = 0, 0
    stack: list[tuple[Optional[Node], bool]] = [(tree, False)]  # @line L8
    while stack and filled < width * height:  # @line L9
        t, draw = stack.pop()  # @line L10
        if t is None:
            continue
        if draw:  # @line L11
            for f in t.on:
                drawn += 1
                for i, j, s in pix:
                    if not written[j][i] and ray_hit(f, e, s) is not None:
                        image[j][i], written[j][i] = f.orig, True
                        filled += 1
            continue
        if t.side(e) >= 0:
            near, far = t.front, t.back
        else:
            near, far = t.back, t.front
        stack += [(far, False), (t, True), (near, False)]  # @line L12
    return drawn, image


def tree_size(tree: Optional[Node]) -> int:
    count, stack = 0, [tree]
    while stack:
        t = stack.pop()
        if t is not None:
            count += len(t.on)
            stack += [t.front, t.back]
    return count
