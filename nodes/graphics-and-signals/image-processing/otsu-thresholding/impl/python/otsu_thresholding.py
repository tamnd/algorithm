# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/otsu-thresholding/. The authors are listed in prov/5FBGX8.jsonl.

"""Otsu's threshold (Otsu 1979) on an integer gray image.

An image is a list of rows of integers in 0..L-1. A threshold t splits the
levels into the class C0 = {0, ..., t} and the class C1 = {t+1, ..., L-1};
a pixel is foreground when its value is greater than t. Otsu's rule picks
the t that maximizes the between-class variance

    sigma_B^2(t) = (mu_T * omega(t) - mu(t))^2 / (omega(t) * (1 - omega(t))),

where omega(t) is the fraction of pixels in C0, mu(t) is the first moment
of C0 (the sum of i * p_i over i <= t) and mu_T is the mean of the image.
The scan uses running sums, so the cost is O(N + L) for N pixels.

All arithmetic is exact (integers and Fraction). Ties go to the smallest t.
"""

from fractions import Fraction
from typing import List, Optional, Sequence, Tuple


def histogram(img: Sequence[Sequence[int]], levels: int) -> List[int]:
    """Counts h[i] of the pixels with value i, for i in 0..levels-1. O(N + L)."""
    h = [0] * levels
    for row in img:
        for v in row:
            if not 0 <= v < levels:
                raise ValueError("pixel value out of range")
            h[v] += 1
    return h


def between_class_variances(h: Sequence[int]) -> List[Optional[Fraction]]:
    """sigma_B^2(t) for t = 0..L-2, or None where one class is empty. O(L)."""
    n = sum(h)
    s = sum(i * c for i, c in enumerate(h))
    out: List[Optional[Fraction]] = []
    n0 = 0
    s0 = 0
    for t in range(len(h) - 1):
        n0 += h[t]  # running count of C0
        s0 += t * h[t]  # running first moment of C0
        if n0 == 0 or n0 == n:
            out.append(None)
            continue
        # (mu_T omega - mu)^2 / (omega (1 - omega)) with omega = n0/n, mu = s0/n.
        out.append(Fraction((s * n0 - n * s0) ** 2, n * n * n0 * (n - n0)))
    return out


def otsu_threshold_from_histogram(h: Sequence[int]) -> Optional[int]:
    """The smallest t that maximizes sigma_B^2(t), or None if fewer than two levels occur."""
    n = sum(h)  # @line L1
    s = sum(i * c for i, c in enumerate(h))  # @line L2
    best_t: Optional[int] = None  # @line L3
    best: Fraction = Fraction(-1)
    n0 = 0  # @line L4
    s0 = 0
    for t in range(len(h) - 1):  # @line L5
        n0 += h[t]  # @line L6
        s0 += t * h[t]
        if n0 == 0 or n0 == n:  # @line L7
            continue
        num = (s * n0 - n * s0) ** 2  # @line L8
        val = Fraction(num, n * n * n0 * (n - n0))
        if val > best:  # @line L9
            best = val  # @line L10
            best_t = t
    return best_t  # @line L11


def otsu_threshold(img: Sequence[Sequence[int]], levels: int = 256) -> Optional[int]:
    """Otsu's threshold of an integer image with values in 0..levels-1. O(N + L)."""
    return otsu_threshold_from_histogram(histogram(img, levels))


def binarize(img: Sequence[Sequence[int]], t: int) -> List[List[int]]:
    """1 where the value is greater than t, else 0."""
    return [[1 if v > t else 0 for v in row] for row in img]


def multi_otsu_from_histogram(h: Sequence[int], classes: int) -> Optional[Tuple[int, ...]]:
    """Thresholds t_1 < ... < t_(M-1) that maximize the between-class variance for M classes.

    Class k holds the levels t_(k-1)+1 .. t_k (with t_0 = -1 and t_M = L-1).
    The between-class variance is sum_k omega_k mu_k^2 - mu_T^2 (mu_k the class
    mean), so maximizing it means maximizing sum_k s_k^2 / n_k over the classes,
    with an empty class counted as 0. A dynamic program over the last level of
    each class finds it in O(M L^2). Each class has at least one level, but it
    may have no pixels. Returns None if M > L.
    """
    big_l = len(h)
    if classes < 1 or classes > big_l:
        return None
    pn = [0] * (big_l + 1)
    ps = [0] * (big_l + 1)
    for i, c in enumerate(h):
        pn[i + 1] = pn[i] + c
        ps[i + 1] = ps[i] + i * c

    def score(a: int, b: int) -> Fraction:
        """s^2 / n for the class of levels a..b-1 (half open), 0 if empty."""
        cnt = pn[b] - pn[a]
        if cnt == 0:
            return Fraction(0)
        return Fraction((ps[b] - ps[a]) ** 2, cnt)

    # f[c][j]: best value for the first j levels split into c nonempty-range classes.
    neg = None
    f = [[neg] * (big_l + 1) for _ in range(classes + 1)]
    arg = [[0] * (big_l + 1) for _ in range(classes + 1)]
    f[0][0] = Fraction(0)
    for c in range(1, classes + 1):
        for j in range(c, big_l + 1):
            best = neg
            for i in range(c - 1, j):
                if f[c - 1][i] is None:
                    continue
                v = f[c - 1][i] + score(i, j)
                if best is None or v > best:
                    best = v
                    arg[c][j] = i
            f[c][j] = best
    cuts = []
    j = big_l
    for c in range(classes, 0, -1):
        i = arg[c][j]
        cuts.append(i - 1)
        j = i
    cuts.reverse()
    return tuple(cuts[1:])
