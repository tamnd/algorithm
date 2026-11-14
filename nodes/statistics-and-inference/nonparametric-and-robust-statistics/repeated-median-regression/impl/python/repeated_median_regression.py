# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/repeated-median-regression/. The authors are listed in prov/DYDSMR.jsonl.

import random
from fractions import Fraction

NEG_INF = "-inf"
POS_INF = "+inf"


def _key(s, x, y, i):
    """Sort key of point i for the order of y - s x at the slope s."""
    if s == NEG_INF:
        return (x[i], y[i])
    if s == POS_INF:
        return (-x[i], y[i])
    return (y[i] - s * x[i],)


def per_point_between(lo, hi, x, y):
    """cnt[i] = number of j with lo < s_ij < hi, for every point i.

    The pairs counted are the inversions of the hi-keys listed in the order
    of the lo-keys; merge sort charges each inversion to both its ends.
    O(n log n) time.
    """
    n = len(x)
    order = sorted(range(n), key=lambda i: (_key(lo, x, y, i), _key(hi, x, y, i)))
    items = [(_key(hi, x, y, i), i) for i in order]
    cnt = [0] * n

    def sort(seq):
        if len(seq) <= 1:
            return seq
        mid = len(seq) // 2
        left, right = sort(seq[:mid]), sort(seq[mid:])
        out, i, j = [], 0, 0
        for v in right:
            while i < len(left) and left[i][0] <= v[0]:
                cnt[left[i][1]] += j  # right items already out are smaller
                out.append(left[i])
                i += 1
            cnt[v[1]] += len(left) - i  # left items still waiting are larger
            out.append(v)
            j += 1
        for item in left[i:]:
            cnt[item[1]] += j
            out.append(item)
        return out

    sort(items)
    return cnt


def _slopes_of(i, x, y):
    return [Fraction(y[j] - y[i]) / (x[j] - x[i]) for j in range(len(x)) if x[j] != x[i]]


def repeated_median_slope(x, y, rng=None):
    """Siegel's repeated median slope, with order-statistic medians:
    inner = high median (floor(d/2) + 1)-th smallest of the d slopes of a point,
    outer = low median ceil(n'/2)-th smallest of the n' point medians.
    Randomized selection over the point medians, O(n log^2 n) expected time."""
    rng = rng or random.Random(0)
    n = len(x)
    d = per_point_between(NEG_INF, POS_INF, x, y)  # @line L1
    keep = [i for i in range(n) if d[i] > 0]
    if not keep:
        raise ValueError("need two points with different x")
    k = [d[i] // 2 + 1 for i in range(n)]  # @line L2
    K = (len(keep) + 1) // 2
    le_lo = [0] * n  # slopes of j <= lo, at lo = -inf  # @line L3
    lt_hi = list(d)  # slopes of j < hi, at hi = +inf
    active = list(keep)  # @line L4
    while True:  # @line L5
        i = rng.choice(active)  # @line L6
        v = sorted(_slopes_of(i, x, y))[k[i] - 1]
        above = per_point_between(v, POS_INF, x, y)  # @line L7
        lt = per_point_between(NEG_INF, v, x, y)
        le = [d[j] - above[j] for j in range(n)]
        cl = sum(1 for j in keep if lt[j] >= k[j])  # m_j < v  # @line L8
        ce = sum(1 for j in keep if le[j] >= k[j])  # m_j <= v
        if cl < K <= ce:  # @line L9
            return v
        if K <= cl:  # @line L10
            lt_hi = lt
        else:
            le_lo = le
        # m_j > lo  iff  fewer than k_j slopes of j are <= lo; m_j < hi likewise.
        active = [j for j in active if le_lo[j] < k[j] and lt_hi[j] >= k[j]]  # @line L11


def repeated_median(x, y, rng=None):
    """Slope b by the repeated median, intercept a = median of y - b x."""
    if len(x) != len(y):
        raise ValueError("x and y differ in length")
    x = [Fraction(v) for v in x]
    y = [Fraction(v) for v in y]
    b = repeated_median_slope(x, y, rng)
    res = sorted(yi - b * xi for xi, yi in zip(x, y))  # @line L12
    m = len(res)
    return b, (res[(m - 1) // 2] + res[m // 2]) / 2  # @line L13


def naive_repeated_median_slope(x, y):
    """Direct O(n^2 log n) version with the same order-statistic medians."""
    x = [Fraction(v) for v in x]
    y = [Fraction(v) for v in y]
    meds = []
    for i in range(len(x)):
        s = sorted(_slopes_of(i, x, y))
        if s:
            meds.append(s[len(s) // 2])
    if not meds:
        raise ValueError("need two points with different x")
    meds.sort()
    return meds[(len(meds) + 1) // 2 - 1]


def breakdown_count(n):
    """Least number of replaced points that can carry the slope away,
    for clean data with distinct x: floor(n/2)."""
    return n // 2
