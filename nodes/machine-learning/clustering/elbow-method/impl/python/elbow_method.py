# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elbow-method/. The authors are listed in prov/1YN38V.jsonl.
"""The elbow method: compute W_k for k = 1, ..., K, then pick the bend of the curve.

The bend has no single definition. This file uses one concrete rule: scale both axes
to [0, 1] and take the point farthest below the chord from the first point to the last.
This is the offline knee of the Kneedle method of Satopaa et al. (2011) without smoothing.
W_k comes from an exact k-means solver for points on a line, so the curve is the true
optimum and never increases.
"""

from fractions import Fraction
from typing import Sequence


def wcss_1d_exact(xs: Sequence, kmax: int) -> list:
    """Optimal k-means cost W_k for k = 1..kmax on the line, by dynamic programming.

    On a line some optimal clustering uses runs of consecutive sorted points, so
    W_k(j) = min over i of W_{k-1}(i) + cost(points i..j-1). O(kmax n^2) time with prefix sums.
    """
    x = sorted(xs)
    n = len(x)
    s1 = [0] * (n + 1)
    s2 = [0] * (n + 1)
    for i, v in enumerate(x):
        s1[i + 1] = s1[i] + v
        s2[i + 1] = s2[i] + v * v

    def cost(i: int, j: int):  # sum of squared deviations of x[i:j] from their mean
        m = j - i
        t = s1[j] - s1[i]
        return (s2[j] - s2[i]) - Fraction(t * t, m) if isinstance(t, int) else (s2[j] - s2[i]) - t * t / m

    inf = None
    prev = [inf] * (n + 1)
    prev[0] = 0
    out = []
    for k in range(1, kmax + 1):
        cur = [inf] * (n + 1)
        for j in range(1, n + 1):
            best = inf
            for i in range(k - 1, j):
                if prev[i] is None:
                    continue
                c = prev[i] + cost(i, j)
                if best is None or c < best:
                    best = c
            cur[j] = best
        out.append(cur[n])
        prev = cur
    return out


def elbow_by_chord(ks: Sequence[int], ws: Sequence) -> int:
    """Return the k whose scaled point lies farthest below the chord from the first
    scaled point (0, 1) to the last one (1, 0). The signed gap is 1 - x - y.
    Ties go to the smaller k. Needs at least 3 points and W_first > W_last.
    """
    if len(ks) < 3 or len(ks) != len(ws):
        raise ValueError("need at least 3 values of k")
    k0, k1 = ks[0], ks[-1]
    hi, lo = ws[0], ws[-1]
    if not hi > lo:
        raise ValueError("the curve must drop from the first k to the last")
    best_k, best_gap = ks[0], None
    for k, w in zip(ks, ws):
        x = Fraction(k - k0, k1 - k0)
        y = (w - lo) / (hi - lo)
        gap = 1 - x - y
        if best_gap is None or gap > best_gap:
            best_k, best_gap = k, gap
    return best_k
