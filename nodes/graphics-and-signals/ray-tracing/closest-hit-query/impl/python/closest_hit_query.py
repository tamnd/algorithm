# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/closest-hit-query/. The authors are listed in prov/Q9V10R.jsonl.

"""Reference solvers for the closest-hit query.

A query is a ray o + t d and an open interval (tmin, tmax). The answer is
a pair (t, k) where object k has a hit at t, tmin < t < tmax, and no
object has a hit with a smaller t; or None when no object has a hit in
the interval. If several objects share the smallest t, any of them is a
correct answer.

The objects are opaque. The caller passes intersect(obj, o, d, tmin, tmax),
which returns the smallest hit parameter of obj in (tmin, tmax) or None.
With exact (Fraction) intersection routines the answers are exact.
"""

from typing import Callable, List, Optional, Sequence, Tuple

Intersect = Callable[[object, Sequence, Sequence, object, object], Optional[object]]


def closest_hit_scan(objects: Sequence, o, d, tmin, tmax, intersect: Intersect) -> Optional[Tuple[object, int]]:
    """Linear scan that shrinks tmax to the best hit so far.

    Each object is tested once, so the cost is n primitive tests. Among
    objects with the same smallest t it returns the first one.
    """
    best = None
    for k, obj in enumerate(objects):
        t = intersect(obj, o, d, tmin, tmax)
        if t is not None:
            tmax, best = t, k          # later tests only look in (tmin, t)
    return None if best is None else (tmax, best)


def box_entry(lo: Sequence, hi: Sequence, o, d, tmin, tmax):
    """Slab test: the start of the overlap of the ray interval with the box
    [lo, hi], or None. Uses only comparisons and division, so it is exact
    with Fraction inputs."""
    for a in range(3):
        if d[a] == 0:
            if o[a] < lo[a] or o[a] > hi[a]:
                return None
            continue
        t0, t1 = (lo[a] - o[a]) / d[a], (hi[a] - o[a]) / d[a]
        if t0 > t1:
            t0, t1 = t1, t0
        tmin, tmax = max(tmin, t0), min(tmax, t1)
        if tmin > tmax:
            return None
    return tmin


def bounding_box(points: Sequence[Sequence]) -> Tuple[tuple, tuple]:
    return (tuple(min(p[a] for p in points) for a in range(3)),
            tuple(max(p[a] for p in points) for a in range(3)))


def closest_hit_groups(groups: List[Tuple[tuple, tuple, List[int]]], objects: Sequence,
                       o, d, tmin, tmax, intersect: Intersect) -> Optional[Tuple[object, int]]:
    """Closest hit with one level of bounding boxes.

    groups holds (lo, hi, indices): a box that contains the objects with
    those indices. The boxes are visited in order of their entry
    parameter, and the scan stops at the first box that starts at or
    after the best hit, because no object in it can be closer.
    """
    entries = []
    for lo, hi, idx in groups:
        e = box_entry(lo, hi, o, d, tmin, tmax)
        if e is not None:
            entries.append((e, idx))
    entries.sort(key=lambda x: x[0])
    best = None
    for e, idx in entries:
        if best is not None and e >= tmax:
            break
        for k in idx:
            t = intersect(objects[k], o, d, tmin, tmax)
            if t is not None:
                tmax, best = t, k
    return None if best is None else (tmax, best)
