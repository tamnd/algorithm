# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trimmed-mean/. The authors are listed in prov/4F0CN9.jsonl.

import math
import random
from fractions import Fraction


def trim_count(n: int, alpha) -> int:
    """Return g = floor(alpha * n), computed exactly.

    A float alpha is read through its decimal repr, so 0.29 * 100 gives 29 and
    not 28 (the float product is 28.999999999999996).
    """
    a = Fraction(repr(alpha)) if isinstance(alpha, float) else Fraction(alpha)
    if not 0 <= a < Fraction(1, 2):
        raise ValueError("alpha must be in [0, 1/2)")
    return math.floor(a * n)


def select(a: list, lo: int, hi: int, k: int, rng: random.Random) -> None:
    """Rearrange a[lo..hi] in place so that a[k] is the value of rank k - lo.

    Afterwards a[lo..k-1] <= a[k] <= a[k+1..hi]. Quickselect with a random pivot
    and a three-way partition, so equal keys cost no extra time.
    Expected O(hi - lo + 1) comparisons.
    """
    while lo < hi:
        p = a[rng.randint(lo, hi)]
        lt, i, gt = lo, lo, hi  # a[lo..lt-1] < p, a[lt..i-1] == p, a[gt+1..hi] > p
        while i <= gt:
            if a[i] < p:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > p:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        if k < lt:
            hi = lt - 1
        elif k > gt:
            lo = gt + 1
        else:
            return


def trimmed_mean(xs, alpha=0.1, *, g=None, seed: int = 0):
    """Return the mean of x_(g+1), ..., x_(n-g), with g = floor(alpha * n).

    Pass g to set the number of points cut from each end directly. The input is
    not changed. Exact for int and Fraction data (the result is a Fraction).
    Expected Theta(n) time, Theta(n) extra space for the copy.
    """
    a = list(xs)
    n = len(a)  # @line L1
    if g is None:
        g = trim_count(n, alpha)  # @line L1
    if g < 0 or n - 2 * g < 1:  # @line L2
        raise ValueError("need n - 2 g >= 1")
    rng = random.Random(seed)
    select(a, 0, n - 1, g, rng)  # @line L3
    select(a, g, n - 1, n - g - 1, rng)  # @line L4
    s = sum(a[g:n - g], Fraction(0)) if all(isinstance(v, (int, Fraction)) for v in a) else math.fsum(a[g:n - g])  # @line L5
    return s / (n - 2 * g)  # @line L6


def winsorized_variance(xs, g: int):
    """Sample variance of the g-Winsorized sample (divide by n - 1).

    The Tukey-McLaughlin standard error of the trimmed mean is
    sqrt(winsorized_variance) / ((1 - 2 g / n) sqrt(n)).
    """
    s = sorted(xs)
    n = len(s)
    w = [s[g]] * g + s[g:n - g] + [s[n - g - 1]] * g
    m = sum(w) / n
    return sum((v - m) ** 2 for v in w) / (n - 1)
