# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epstein-levin-eptas-bin-packing/. The authors are listed in prov/XKC6Z1.jsonl.

"""The robust form of the Epstein-Levin scheme, in its simplest variant: bins of size 1 + eps, items arriving one by
one, and after each arrival only a few bins are packed again.

Large items (size at least eps / 4) are rounded up to powers of 1 + eps / 4, once and for all. The large items of a
bin form a pattern, and the packing is a vector y of pattern counts with A y = u, where u counts the large items of
each rounded size. When a large item arrives, u changes in one entry, and the new y' is chosen as close to y as
possible; the proximity theorem of integer programming bounds the distance by d * Delta * 3. Sizes are Fractions."""

from fractions import Fraction
from itertools import combinations
from typing import Optional


def round_up(size: Fraction, eps: Fraction) -> Fraction:
    """The least power of 1 + eps/4 (exponent at most 0) that is at least the size."""
    q, r = 1 + eps / 4, Fraction(1)
    while r / q >= size:
        r /= q
    return r


def patterns(classes: list, cap: Fraction) -> list[tuple]:
    """All multisets of rounded sizes with sum at most cap, as sorted tuples, the empty one first."""
    out, stack = [], [((), 0, Fraction(0))]
    while stack:
        pat, start, load = stack.pop()
        out.append(pat)
        for i in range(start, len(classes)):
            if load + classes[i] <= cap:
                stack.append((pat + (classes[i],), i, load + classes[i]))
    return sorted(out, key=lambda p: (len(p), p))


def determinant(rows: list[list]) -> Fraction:
    a = [[Fraction(x) for x in r] for r in rows]
    n, det = len(a), Fraction(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if a[r][c] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != c:
            a[c], a[piv] = a[piv], a[c]
            det = -det
        det *= a[c][c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            for k in range(c, n):
                a[r][k] -= f * a[c][k]
    return det


def matrix(classes: list, pats: list[tuple]) -> list[list[int]]:
    """One row per rounded size (how many items of that size each pattern holds), and a row of ones (bins)."""
    return [[p.count(c) for p in pats] for c in classes] + [[1] * len(pats)]


def max_subdeterminant(a: list[list[int]]) -> int:
    best = 1
    for k in range(1, len(a) + 1):
        for rows in combinations(range(len(a)), k):
            for cols in combinations(range(len(a[0])), k):
                best = max(best, abs(determinant([[a[r][c] for c in cols] for r in rows])))
    return int(best)


def min_bins(pats: list[tuple], classes: list, counts: dict) -> int:
    """The least number of patterns whose sum is exactly the count vector, bottom-up over all smaller vectors."""
    sizes = [counts[c] for c in classes]
    vecs = [()]
    for s in sizes:
        vecs = [v + (j,) for v in vecs for j in range(s + 1)]
    vecs.sort(key=sum)
    vectors = [tuple(p.count(c) for c in classes) for p in pats if p]
    best = {tuple(0 for _ in classes): 0}
    for v in vecs[1:]:
        best[v] = min(1 + best[tuple(a - b for a, b in zip(v, w))] for w in vectors
                      if all(b <= a for a, b in zip(v, w)))
    return best[tuple(sizes)]


def closest(pats: list[tuple], counts: dict, bins: int, old: dict, limit: int) -> Optional[dict]:
    """A vector y' >= 0 with A y' = counts and sum y' = bins whose largest change from old is least, searching
    distances 0, 1, ..., limit; None if there is none within the limit. The empty pattern comes first in pats and
    takes the bins that are left."""
    order = pats[1:] + pats[:1]
    for radius in range(limit + 1):
        stack = [(0, dict(counts), bins, {})]
        while stack:
            i, need, left, y = stack.pop()
            if i == len(order) - 1:
                base = old.get((), 0)
                if all(v == 0 for v in need.values()) and abs(left - base) <= radius:
                    y[()] = left
                    return {p: v for p, v in y.items() if v}
                continue
            p, base = order[i], old.get(order[i], 0)
            for v in range(max(0, base - radius), base + radius + 1):
                if v > left:
                    break
                rest = dict(need)
                for c in p:
                    rest[c] -= v
                if all(x >= 0 for x in rest.values()):
                    stack.append((i + 1, rest, left - v, {**y, p: v}))
    return None


_DELTA: dict = {}


class RobustPacking:
    """Bins of size 1 + eps. Each bin is a dict with its large items, small items and pattern."""

    def __init__(self, eps: Fraction):
        self.eps, self.cap = eps, 1 + eps
        self.bins: list[dict] = []
        self.classes: list = []
        self.log: list[dict] = []

    def y(self) -> dict:
        out: dict = {}
        for b in self.bins:
            out[b["pattern"]] = out.get(b["pattern"], 0) + 1
        return out

    def load(self, b: dict) -> Fraction:
        return sum(s for s, _ in b["large"]) + sum(b["small"])

    def any_fit(self, size: Fraction) -> int:
        """First Fit by original sizes; opens a bin with the empty pattern if no bin has room. Returns bins opened."""
        for b in self.bins:
            if self.load(b) + size <= self.cap:
                b["small"].append(size)
                return 0
        self.bins.append({"large": [], "small": [size], "pattern": ()})
        return 1

    def delta(self) -> tuple[int, int]:
        """(d, Delta): the number of patterns and the largest subdeterminant of the matrix, kept across runs."""
        key = (tuple(self.classes), self.cap)
        if key not in _DELTA:
            pats = patterns(self.classes, self.cap)
            _DELTA[key] = (len(pats), max_subdeterminant(matrix(self.classes, pats)))
        return _DELTA[key]

    def add(self, size: Fraction) -> dict:
        """Pack one arriving item and return a record of what moved."""
        if size < self.eps / 4:
            opened = self.any_fit(size)  # @line L1
            rec = {"size": size, "large": False, "opened": opened, "moved": Fraction(0), "repacked": 0}
            self.log.append(rec)
            return rec
        r = round_up(size, self.eps)  # @line L2
        if r not in self.classes:
            self.classes = sorted(self.classes + [r], reverse=True)
        pats = patterns(self.classes, self.cap)
        old = self.y()  # @line L3
        counts = {c: 0 for c in self.classes}
        for b in self.bins:
            for _, c in b["large"]:
                counts[c] += 1
        counts[r] += 1
        d, delta = self.delta()
        rec = {"size": size, "large": True, "d": d, "delta": delta, "opened": 0}
        found = None
        if min_bins(pats, self.classes, counts) <= len(self.bins):
            found = closest(pats, counts, len(self.bins), old, 3 * d * delta)  # @line L4
            if found is None:
                raise AssertionError("the proximity theorem promises a solution within 3 d Delta")
        if found is None:
            self.bins.append({"large": [(size, r)], "small": [], "pattern": (r,)})  # @line L5
            rec.update(opened=1, moved=Fraction(0), repacked=0, distance=None)
            self.log.append(rec)
            return rec
        rec["distance"] = max(abs(found.get(p, 0) - old.get(p, 0)) for p in set(found) | set(old))
        keep: dict = {}
        kept, pool_large, pool_small = [], [(size, r)], []
        for b in self.bins:  # @line L6
            if keep.get(b["pattern"], 0) < found.get(b["pattern"], 0):
                keep[b["pattern"]] = keep.get(b["pattern"], 0) + 1
                kept.append(b)
            else:
                pool_large += b["large"]
                pool_small += b["small"]
        rec["repacked"] = len(self.bins) - len(kept)
        rec["moved"] = sum(s for s, _ in pool_large[1:]) + sum(pool_small)
        self.bins = kept
        by_class: dict = {}
        for item in pool_large:
            by_class.setdefault(item[1], []).append(item)
        for p, v in found.items():
            for _ in range(v - keep.get(p, 0)):
                self.bins.append({"large": [by_class[c].pop() for c in p], "small": [], "pattern": p})
        for s in pool_small:
            rec["opened"] += self.any_fit(s)
        self.log.append(rec)
        return rec
