# SPDX-License-Identifier: MIT
# Shared helper of the ma4 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Axis-aligned boxes for the assembly planning pages.

A box is a tuple (x0, y0, z0, x1, y1, z1) with x0 < x1, y0 < y1 and z0 < z1.
Coordinates are int or Fraction, so every test here is exact. A part is a
closed box, and two parts of an assembly may touch but their interiors must
be disjoint.
"""

from fractions import Fraction

AXES6 = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))

AXIS_NAMES = {
    (1, 0, 0): "+x", (-1, 0, 0): "-x",
    (0, 1, 0): "+y", (0, -1, 0): "-y",
    (0, 0, 1): "+z", (0, 0, -1): "-z",
}


def check_box(b):
    if len(b) != 6 or not all(b[k] < b[k + 3] for k in range(3)):
        raise ValueError("a box is (x0, y0, z0, x1, y1, z1) with x0 < x1, y0 < y1, z0 < z1")


def interiors_overlap(a, b):
    """True if the open boxes a and b meet, that is, the parts collide."""
    return all(a[k] < b[k + 3] and b[k] < a[k + 3] for k in range(3))


def is_valid_assembly(boxes):
    for b in boxes:
        check_box(b)
    n = len(boxes)
    return all(not interiors_overlap(boxes[i], boxes[j])
               for i in range(n) for j in range(i + 1, n))


def face_contact(a, b):
    """Return (k, s, area) if a and b share a planar patch of positive area.

    The contact normal from a to b is s times the unit vector e_k. Boxes that
    touch only along an edge or at a corner give None.
    """
    for k in range(3):
        if a[k + 3] == b[k]:
            s = 1
        elif b[k + 3] == a[k]:
            s = -1
        else:
            continue
        area = 1
        for m in range(3):
            if m == k:
                continue
            w = min(a[m + 3], b[m + 3]) - max(a[m], b[m])
            if w <= 0:
                area = 0
                break
            area *= w
        if area > 0:
            return (k, s, area)
    return None


def translate(b, d, t):
    """The box b moved by t times the vector d."""
    return tuple(b[k] + t * d[k % 3] for k in range(6))


def blocks(a, b, d):
    """True if box b blocks box a when a translates to infinity along d.

    d is one of AXES6. This is the extended translation model: a moves by
    t d for all t > 0, and b blocks it if a + t d meets the interior of b
    for some t > 0.
    """
    k = 0 if d[0] else (1 if d[1] else 2)
    for m in range(3):
        if m != k and not (a[m] < b[m + 3] and b[m] < a[m + 3]):
            return False
    if d[k] > 0:
        return b[k] >= a[k + 3]
    return b[k + 3] <= a[k]


def free_by_sampling(movers, others, d):
    """Reference test: do the boxes movers leave along d without a collision?

    Only for integer corners. Each collision of two boxes happens for t in an
    open interval with integer ends, so the half integers t = 1/2, 1, 3/2, ...
    up to the size of the scene meet every such interval.
    """
    span = 0
    for b in list(movers) + list(others):
        span = max(span, max(abs(c) for c in b))
    for step in range(1, 4 * span + 3):
        t = Fraction(step, 2)
        for a in movers:
            moved = translate(a, d, t)
            if any(interiors_overlap(moved, b) for b in others):
                return False
    return True


def members(mask):
    """The indices of the set bits of mask, in increasing order."""
    out = []
    i = 0
    while mask:
        if mask & 1:
            out.append(i)
        mask >>= 1
        i += 1
    return out


def random_boxes(rng, n, size=4, max_side=2, connected=True, tries=400):
    """n boxes with integer corners in [0, size]^3 and disjoint interiors.

    With connected=True, each new box shares a face patch with an earlier
    box, so the contact graph is connected. The result depends only on rng.
    """
    while True:
        boxes = []
        for _ in range(tries):
            lo = []
            hi = []
            for _k in range(3):
                side = rng.randint(1, max_side)
                x0 = rng.randint(0, size - side)
                lo.append(x0)
                hi.append(x0 + side)
            b = tuple(lo + hi)
            if any(interiors_overlap(b, c) for c in boxes):
                continue
            if connected and boxes and not any(face_contact(b, c) for c in boxes):
                continue
            boxes.append(b)
            if len(boxes) == n:
                return boxes
