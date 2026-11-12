# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/any-hit-query/. The authors are listed in prov/SSJP31.jsonl.

"""Reference solvers for the any-hit query.

A query is a ray o + t d and an open interval (tmin, tmax). The answer is
yes when some object has a hit with tmin < t < tmax, and no otherwise. A
solver may stop at the first hit it finds, in any order. An optional
accept(obj, t) filter rejects some hits (for example a texel with zero
alpha), and the search goes on after a rejected hit.

The objects are opaque. The caller passes intersect(obj, o, d, tmin, tmax),
which returns a hit parameter of obj in (tmin, tmax) or None.
"""

from typing import Callable, Optional, Sequence

Intersect = Callable[[object, Sequence, Sequence, object, object], Optional[object]]


def any_hit(objects: Sequence, o, d, tmin, tmax, intersect: Intersect,
            accept: Optional[Callable[[object, object], bool]] = None) -> Optional[int]:
    """Return the index of an object with an accepted hit in (tmin, tmax), or None.

    The scan stops at the first accepted hit, so a yes answer can cost
    one test, and a no answer costs one test per object.
    """
    for k, obj in enumerate(objects):
        t = intersect(obj, o, d, tmin, tmax)
        if t is not None and (accept is None or accept(obj, t)):
            return k
    return None


def visible(objects: Sequence, p: Sequence, q: Sequence, intersect: Intersect,
            eps=0) -> bool:
    """Shadow ray: True when nothing blocks the open segment from p to q.

    The ray is p + t (q - p) with t in (eps, 1 - eps); the small eps keeps
    the surfaces at p and at q from blocking the ray.
    """
    d = tuple(q[k] - p[k] for k in range(3))
    return any_hit(objects, p, d, eps, 1 - eps, intersect) is None
