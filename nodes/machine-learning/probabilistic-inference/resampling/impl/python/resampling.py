# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/resampling/. The authors are listed in prov/DF7EPS.jsonl.

"""Four resampling schemes for a weighted particle set.

Each function takes normalized weights w[0..N-1] (non-negative, sum 1) and an
object rng with a method random() that returns a uniform number in [0, 1).
It returns N ancestor indices in increasing order. The expected number of
copies of particle i is N * w[i] for all four schemes.

The code uses only +, -, *, / and comparisons on the weights, so it also runs
on fractions.Fraction weights, which the tests use for exact expectations.
"""

from bisect import bisect_right


def _cumulative(w):
    c, s = [], 0
    for x in w:
        s += x
        c.append(s)
    return c


def _search(c, u):
    """Smallest i with u < c[i], clamped to the last index against rounding."""
    return min(bisect_right(c, u), len(c) - 1)


def multinomial_resample(w, rng):
    """N independent draws from w by inverse transform. O(N log N)."""
    c = _cumulative(w)  # @line L1
    idx = [_search(c, rng.random()) for _ in range(len(w))]  # @line L2
    idx.sort()  # @line L3
    return idx


def residual_resample(w, rng):
    """floor(N w_i) copies of i, then multinomial draws on the residues."""
    n = len(w)
    idx, res = [], []
    for i, x in enumerate(w):  # @line L4
        k = int(n * x)  # floor, since n * x >= 0
        idx.extend([i] * k)
        res.append(n * x - k)
    r = n - len(idx)  # @line L5
    if r > 0:
        c = _cumulative([x / r for x in res])  # @line L6
        idx.extend(_search(c, rng.random()) for _ in range(r))
    idx.sort()  # @line L7
    return idx


def _ordered_points(w, points):
    """Merge sorted points in [0, 1) with the cumulative weights. O(N)."""
    idx, s, i, n = [], w[0], 0, len(w)  # @line L12
    for u in points:  # @line L13
        while u >= s and i < n - 1:
            i += 1
            s += w[i]
        idx.append(i)
    return idx


def stratified_resample(w, rng):
    """One uniform point in each stratum [j/N, (j+1)/N). O(N)."""
    n = len(w)
    u = [(j + rng.random()) / n for j in range(n)]  # @line L8
    return _ordered_points(w, u)  # @line L9


def systematic_resample(w, rng):
    """One uniform U, then the points (j + U)/N. O(N)."""
    n = len(w)
    v = rng.random()  # @line L10
    return _ordered_points(w, [(j + v) / n for j in range(n)])  # @line L11


def ess(w):
    """Effective sample size 1 / sum w_i^2 of normalized weights."""
    return 1 / sum(x * x for x in w)


SCHEMES = {
    "multinomial": multinomial_resample,
    "residual": residual_resample,
    "stratified": stratified_resample,
    "systematic": systematic_resample,
}
