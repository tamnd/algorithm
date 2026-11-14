# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hodges-lehmann-estimator/. The authors are listed in prov/WF6BA7.jsonl.

import random
from fractions import Fraction


def count_le(a, b, start, v, strict=False):
    """Count the cells a[i] + b[j] <= v (or < v when strict) with j >= start[i].

    a and b are sorted ascending and start is nondecreasing. Returns the count and,
    for each row i, the last column last[i] whose cell is <= v (or < v); last[i]
    can be below start[i]. One staircase walk: O(len(a) + len(b)).
    """
    n = len(b)
    j = n - 1
    c = 0
    last = [0] * len(a)
    for i, ai in enumerate(a):  # @line L13
        if strict:
            while j >= 0 and ai + b[j] >= v:
                j -= 1
        else:
            while j >= 0 and ai + b[j] > v:  # @line L14
                j -= 1
        last[i] = j  # @line L15
        if j >= start[i]:
            c += j - start[i] + 1  # @line L16
    return c, last


def select_sum(a, b, start, k, rng):
    """Return the k-th smallest (k >= 1) of the cells a[i] + b[j] with j >= start[i].

    Randomized selection in the sorted matrix: each round takes a random active
    cell as pivot and moves the per-row bounds lo[i] and hi[i] past it.
    Expected O((len(a) + len(b)) log N) time for N cells.
    """
    m, n = len(a), len(b)
    lo = list(start)  # @line L1
    hi = [n - 1] * m  # @line L1
    while True:  # @line L2
        widths = [max(0, hi[i] - lo[i] + 1) for i in range(m)]
        w = sum(widths)  # @line L3
        if w == 0:
            raise ValueError("k is out of range")
        r = rng.randrange(w)  # @line L4
        i = 0
        while r >= widths[i]:
            r -= widths[i]
            i += 1
        v = a[i] + b[lo[i] + r]  # @line L4
        cle, le = count_le(a, b, start, v)  # @line L5
        clt, lt = count_le(a, b, start, v, strict=True)  # @line L5
        if clt >= k:  # @line L6
            for t in range(m):
                hi[t] = min(hi[t], lt[t])
        elif cle >= k:  # @line L7
            return v
        else:  # @line L8
            for t in range(m):
                lo[t] = max(lo[t], le[t] + 1)


def successor_sum(a, b, start, v):
    """Smallest cell value > v, or None. O(len(a) + len(b))."""
    _, le = count_le(a, b, start, v)
    best = None
    for i, ai in enumerate(a):
        j = max(le[i] + 1, start[i])
        if j < len(b):
            s = ai + b[j]
            if best is None or s < best:
                best = s
    return best


def _median_of_cells(a, b, start, total, rng):
    """Median of the multiset of cells (the average of the two middle ones if total is even)."""
    k = (total + 1) // 2
    s1 = select_sum(a, b, start, k, rng)  # @line L10
    if total % 2 == 1:
        s2 = s1
    else:
        cle, _ = count_le(a, b, start, s1)
        s2 = s1 if cle >= k + 1 else successor_sum(a, b, start, s1)  # @line L11
    if _exact(a) and _exact(b):
        return (Fraction(s1) + Fraction(s2)) / 2
    return (s1 + s2) / 2


def _exact(a):
    return all(isinstance(v, (int, Fraction)) for v in a)


def hodges_lehmann(xs, seed: int = 0):
    """One-sample Hodges-Lehmann estimate: the median of the Walsh averages (x_i + x_j)/2, i <= j.

    Exact (a Fraction) for int or Fraction data. Expected O(n log n) time, O(n) space.
    """
    x = sorted(xs)  # @line L9
    n = len(x)
    if n == 0:
        raise ValueError("empty sample")
    total = n * (n + 1) // 2  # @line L9
    med_sum = _median_of_cells(x, x, list(range(n)), total, random.Random(seed))  # @line L10
    return med_sum / 2  # @line L12


def hodges_lehmann_shift(xs, ys, seed: int = 0):
    """Two-sample Hodges-Lehmann shift estimate: the median of all y_j - x_i.

    Exact for int or Fraction data. Expected O((m + n) log(m n)) time after sorting.
    """
    if not xs or not ys:
        raise ValueError("empty sample")
    a = sorted(-v for v in xs)  # ascending, so a[i] = -x in descending order of x
    b = sorted(ys)
    return _median_of_cells(a, b, [0] * len(a), len(a) * len(b), random.Random(seed))
