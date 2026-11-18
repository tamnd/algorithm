# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pgm-index/. The authors are listed in prov/YYKWMY.jsonl.

"""PGM-index of Ferragina and Vinciguerra (2020), static version.

The bottom level is an optimal piecewise linear approximation (PLA) of the
points (key, position) with a maximum error eps: every key is predicted
within eps of its position. The first keys of the segments are indexed in the
same way with the error eps_rec, level by level, until one segment is left.

The PLA is built greedily: a segment grows while some line stays within eps of
all its points. The set of such lines is a convex polygon in the (slope,
intercept) plane. Each new point cuts the polygon with two half-planes. The
arithmetic uses Fraction, so the test "is the polygon empty" is exact.
"""

from bisect import bisect_right
from fractions import Fraction
from typing import List, Sequence, Tuple


class Segment:
    __slots__ = ("key", "slope", "intercept", "start", "end")

    def __init__(self, key, slope, intercept, start: int, end: int):
        self.key = key              # the first key covered
        self.slope = slope
        self.intercept = intercept
        self.start = start          # the positions start..end of the level array
        self.end = end

    def predict(self, x) -> Fraction:
        return self.intercept + self.slope * (x - self.key)

    def __repr__(self):
        return f"Segment(key={self.key}, slope={self.slope}, intercept={self.intercept}, {self.start}..{self.end})"


Point = Tuple[Fraction, Fraction]   # (slope, intercept)


def _clip(poly: List[Point], dx, lo, hi) -> List[Point]:
    """Cut the convex polygon with lo <= s * dx + c <= hi."""
    for sign, bound in ((1, hi), (-1, -lo)):
        out: List[Point] = []
        n = len(poly)
        for i in range(n):
            p, q = poly[i], poly[(i + 1) % n]
            hp = bound - sign * (p[0] * dx + p[1])
            hq = bound - sign * (q[0] * dx + q[1])
            if hp >= 0:
                out.append(p)
            if (hp > 0 > hq) or (hp < 0 < hq):
                t = hp / (hp - hq)
                out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
        poly = out
        if not poly:
            break
    return poly


def build_pla(xs: Sequence[int], eps: int, base: int = 0) -> List[Segment]:
    """The greedy PLA of the points (xs[i], base + i) with the error eps.

    It gives the fewest segments of any PLA with the error eps.
    """
    segs: List[Segment] = []
    n = len(xs)
    i = 0                                                            # @line L1
    while i < n:                                                     # @line L2
        x0 = xs[i]
        if i == n - 1:
            segs.append(Segment(x0, Fraction(0), Fraction(base + i), base + i, base + i))  # @line L7
            break
        d = xs[i + 1] - x0                                           # @line L3
        y0, y1 = base + i, base + i + 1
        poly: List[Point] = []
        for c, v in ((y0 - eps, y1 - eps), (y0 - eps, y1 + eps), (y0 + eps, y1 + eps), (y0 + eps, y1 - eps)):
            poly.append((Fraction(v - c, d), Fraction(c)))           # @line L3
        j = i + 2                                                    # @line L4
        while j < n:                                                 # @line L5
            cut = _clip(poly, xs[j] - x0, base + j - eps, base + j + eps)  # @line L5
            if not cut:
                break
            poly = cut                                               # @line L6
            j += 1                                                   # @line L6
        s = sum(p[0] for p in poly) / len(poly)
        c = sum(p[1] for p in poly) / len(poly)
        if s < 0:
            # A valid line with a negative slope exists only if the run is
            # shorter than 2 eps; then the flat line at the middle is valid.
            s, c = Fraction(0), Fraction(2 * base + i + j - 1, 2)
        segs.append(Segment(x0, s, c, base + i, base + j - 1))       # @line L7
        i = j                                                        # @line L8
    return segs


class PGMIndex:
    """A static PGM-index over strictly increasing integer keys."""

    def __init__(self, keys: Sequence[int], eps: int = 8, eps_rec: int = 4):
        if eps < 1 or eps_rec < 1:
            raise ValueError("eps and eps_rec must be at least 1")
        keys = list(keys)
        for a, b in zip(keys, keys[1:]):
            if not a < b:
                raise ValueError("keys must be strictly increasing")
        self.keys = keys
        self.eps = eps
        self.eps_rec = eps_rec
        # levels[0] is the root level; arrays[l] is the array that levels[l] indexes.
        self.levels: List[List[Segment]] = []
        self.arrays: List[List[int]] = []
        self.errors: List[int] = []
        if not keys:
            return
        a, e = keys, eps                                             # @line L9
        while True:
            segs = build_pla(a, e)                                   # @line L10
            self.levels.append(segs)
            self.arrays.append(a)
            self.errors.append(e)
            if len(segs) == 1:                                       # @line L12
                break
            a, e = [s.key for s in segs], eps_rec                    # @line L11
        self.levels.reverse()
        self.arrays.reverse()
        self.errors.reverse()
        self.probes = 0

    @property
    def height(self) -> int:
        return len(self.levels)

    def segment_counts(self) -> List[int]:
        """The number of segments on each level, from the bottom up."""
        return [len(s) for s in reversed(self.levels)]

    def rank(self, x) -> int:
        """The number of keys <= x."""
        self.probes = 0
        if not self.keys or x < self.keys[0]:                        # @line L13
            return 0
        seg = self.levels[0][0]                                      # @line L14
        top = len(self.levels) - 1
        for lvl in range(len(self.levels)):                          # @line L15
            e, arr = self.errors[lvl], self.arrays[lvl]
            pos = min(max(seg.predict(x), seg.start), seg.end)       # @line L16
            p = pos.numerator // pos.denominator                     # @line L16
            lo = max(seg.start, p - e)                               # @line L17
            hi = min(seg.end + 1, p + e + 1)                         # @line L17
            r = bisect_right(arr, x, lo, hi)                         # @line L17
            self.probes = max(self.probes, hi - lo)
            if lvl == top:                                           # @line L18
                return r                                             # @line L18
            seg = self.levels[lvl + 1][r - 1]                        # @line L19
        raise AssertionError("unreachable")

    def lower_bound(self, x) -> int:
        """The position of the first key >= x."""
        r = self.rank(x)
        return r - 1 if r and self.keys[r - 1] == x else r

    def contains(self, x) -> bool:
        r = self.rank(x)
        return r > 0 and self.keys[r - 1] == x

    def range(self, lo, hi) -> List[int]:
        """The keys k with lo <= k <= hi."""
        return self.keys[self.lower_bound(lo):self.rank(hi)]

    def max_error(self) -> int:
        """The largest |prediction - position| over the keys of each level (for the tests)."""
        worst = Fraction(0)
        for segs, arr in zip(self.levels, self.arrays):
            for s in segs:
                for i in range(s.start, s.end + 1):
                    worst = max(worst, abs(s.predict(arr[i]) - i))
        return worst
