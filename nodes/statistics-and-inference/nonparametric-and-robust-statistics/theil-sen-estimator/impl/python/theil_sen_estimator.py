# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/theil-sen-estimator/. The authors are listed in prov/VFQ6SW.jsonl.

import random
from fractions import Fraction
from math import isqrt

NEG_INF = "-inf"
POS_INF = "+inf"


def _key(s, x, y, i):
    """Sort key of point i for the order of z = y - s x at the slope s.

    At s = -inf the order is by (x, y); at s = +inf it is by (-x, y).
    These are the limits of the order of y - s x.
    """
    if s == NEG_INF:
        return (x[i], y[i])
    if s == POS_INF:
        return (-x[i], y[i])
    return (y[i] - s * x[i],)


def _inversions(w):
    """Number of pairs a < b with w[a] > w[b], by merge sort. O(n log n)."""
    def sort(lo, hi):
        if hi - lo <= 1:
            return w[lo:hi], 0
        mid = (lo + hi) // 2
        left, cl = sort(lo, mid)
        right, cr = sort(mid, hi)
        out, c, i = [], cl + cr, 0
        for v in right:
            while i < len(left) and left[i] <= v:
                out.append(left[i])
                i += 1
            c += len(left) - i  # every left item still waiting is > v
            out.append(v)
        out.extend(left[i:])
        return out, c
    return sort(0, len(w))[1]


def _sequence(lo, hi, x, y):
    """The hi-keys listed in the order of the lo-keys (ties by hi-key)."""
    n = len(x)
    order = sorted(range(n), key=lambda i: (_key(lo, x, y, i), _key(hi, x, y, i)))
    return order, [_key(hi, x, y, i) for i in order]


def count_between(lo, hi, x, y):
    """Number of pairwise slopes s with lo < s < hi (lo, hi may be infinite).

    A pair is counted exactly when the order of y - s x at lo and at hi
    disagree, so this is an inversion count.
    """
    order, w = _sequence(lo, hi, x, y)  # @line L14
    return _inversions(w)  # @line L15


def count_less(s, x, y):
    """Number of slopes < s, as the inversions of y - s x in x order."""
    return count_between(NEG_INF, s, x, y)


def count_at_most(s, x, y):
    """Number of slopes <= s."""
    return count_between(NEG_INF, POS_INF, x, y) - count_between(s, POS_INF, x, y)


def _slope(x, y, i, j):
    return Fraction(y[j] - y[i]) / (x[j] - x[i])


def _enumerate(lo, hi, x, y):
    """All slopes strictly between lo and hi, by merge sort. O(n log n + C)."""
    order, w = _sequence(lo, hi, x, y)
    items = list(zip(w, order))
    out = []

    def sort(seq):
        if len(seq) <= 1:
            return seq
        mid = len(seq) // 2
        left, right = sort(seq[:mid]), sort(seq[mid:])
        merged, i = [], 0
        for v in right:
            while i < len(left) and left[i][0] <= v[0]:
                merged.append(left[i])
                i += 1
            for a in left[i:]:
                out.append(_slope(x, y, a[1], v[1]))
            merged.append(v)
        merged.extend(left[i:])
        return merged

    sort(items)
    return out


def _sample(lo, hi, x, y, r, rng):
    """r slopes drawn uniformly, with replacement, from those in (lo, hi)."""
    order, w = _sequence(lo, hi, x, y)
    n = len(w)
    vals = sorted(set(w))
    rank = {v: k + 1 for k, v in enumerate(vals)}
    m = len(vals)
    tree = [0] * (m + 1)

    def add(i):
        while i <= m:
            tree[i] += 1
            i += i & -i

    def prefix(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    def kth(k):  # smallest rank with prefix(rank) >= k
        pos, step = 0, 1 << m.bit_length()
        while step:
            if pos + step <= m and tree[pos + step] < k:
                pos += step
                k -= tree[pos]
            step >>= 1
        return pos + 1

    inv = []
    for b in range(n):  # inv[b] = #{a < b : w[a] > w[b]}
        inv.append(b - prefix(rank[w[b]]))
        add(rank[w[b]])
    total = sum(inv)
    picks = sorted(rng.randrange(total) for _ in range(r))
    tree = [0] * (m + 1)
    bucket = [[] for _ in range(m + 1)]
    out, acc, p = [], 0, 0
    for b in range(n):
        rb = rank[w[b]]
        while p < len(picks) and picks[p] < acc + inv[b]:
            t = picks[p] - acc  # the t-th (0-based) earlier item with a larger key
            below = prefix(rb)
            rk = kth(below + t + 1)
            a = bucket[rk][below + t - prefix(rk - 1)]
            out.append(_slope(x, y, a, order[b]))
            p += 1
        acc += inv[b]
        add(rb)
        bucket[rb].append(order[b])
    return out


def select_slope(x, y, k, rng=None):
    """The k-th smallest (1-based) pairwise slope, in expected O(n log n) time."""
    rng = rng or random.Random(0)
    n = len(x)
    lo, hi = NEG_INF, POS_INF  # @line L1
    below = 0  # number of slopes <= lo  # @line L2
    inside = count_between(lo, hi, x, y)  # @line L3
    r = max(n, 32)
    while inside > 4 * r:  # @line L4
        sample = sorted(_sample(lo, hi, x, y, r, rng))  # @line L5
        t = (k - below) * r / inside  # @line L6
        delta = 2 * isqrt(r) + 2  # at least 2 sqrt(r)
        a, b = int(t) - delta, int(t) + delta
        new_lo = sample[a] if a >= 0 else lo  # @line L7
        new_hi = sample[b] if b < r else hi
        nb = below if new_lo == lo else count_at_most(new_lo, x, y)  # @line L8
        if new_lo != lo and count_less(new_lo, x, y) < k <= nb:
            return new_lo
        nlt = (below + inside) if new_hi == hi else count_less(new_hi, x, y)
        if new_hi != hi and nlt < k <= count_at_most(new_hi, x, y):
            return new_hi
        if nb < k <= nlt:  # @line L9
            lo, hi, below, inside = new_lo, new_hi, nb, nlt - nb  # @line L10
        # else the sample missed; draw a new one  # @line L11
    cand = sorted(_enumerate(lo, hi, x, y))  # @line L12
    return cand[k - below - 1]  # @line L13


def theil_sen(x, y, rng=None):
    """Theil-Sen slope and intercept: the median of the pairwise slopes,
    then the median of y - b x. Pairs with equal x are skipped."""
    if len(x) != len(y):
        raise ValueError("x and y differ in length")
    x = [Fraction(v) for v in x]
    y = [Fraction(v) for v in y]
    total = count_between(NEG_INF, POS_INF, x, y)  # pairs with distinct x  # @line L16
    if total == 0:
        raise ValueError("need two points with different x")
    rng = rng or random.Random(0)
    if total % 2 == 1:  # @line L17
        b = select_slope(x, y, (total + 1) // 2, rng)
    else:
        b = (select_slope(x, y, total // 2, rng) + select_slope(x, y, total // 2 + 1, rng)) / 2
    res = sorted(yi - b * xi for xi, yi in zip(x, y))  # @line L18
    m = len(res)
    a = (res[(m - 1) // 2] + res[m // 2]) / 2
    return b, a


def naive_slopes(x, y):
    """All pairwise slopes with x_i != x_j, sorted. O(n^2 log n)."""
    n = len(x)
    return sorted(Fraction(y[j] - y[i]) / (x[j] - x[i])
                  for i in range(n) for j in range(i + 1, n) if x[i] != x[j])


def breakdown_count(n):
    """Least number m of replaced points that can carry the slope to infinity,
    for clean data with distinct x: the least m with C(n - m, 2) <= C(n, 2)/2."""
    total = n * (n - 1) // 2
    m = 0
    while 2 * ((n - m) * (n - m - 1) // 2) > total:
        m += 1
    return m
