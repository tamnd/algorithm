# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contrast-stretching/. The authors are listed in prov/QDCGWA.jsonl.

"""Linear contrast stretching with percentile clipping.

The image is a list of rows of integers in 0 .. levels - 1. The low end lo
is the smallest level with more than p_lo * n pixels at or below it, and the
high end hi is the smallest level with at least (1 - p_hi) * n pixels at or
below it. Levels at or below lo go to 0, levels at or above hi go to L - 1,
and the levels between go on a straight line, rounded with halves up.
With p_lo = p_hi = 0 this is plain min-max stretching.
"""

from fractions import Fraction


def stretch_ends(hist: list[int], p_lo: Fraction, p_hi: Fraction) -> tuple[int, int]:
    """Return (lo, hi) from the histogram. Cost: O(L)."""
    n = sum(hist)
    c, lo, hi = 0, -1, -1  # @line L2
    for k, count in enumerate(hist):  # @line L3
        c += count  # @line L4
        if lo < 0 and c > p_lo * n:  # @line L5
            lo = k
        if hi < 0 and c >= (1 - p_hi) * n:  # @line L6
            hi = k
    return lo, hi


def stretch_table(levels: int, lo: int, hi: int) -> list[int]:
    """The table of the stretch from [lo, hi] to [0, L - 1]. Needs lo < hi."""
    table = [0] * levels
    d = hi - lo
    for k in range(levels):  # @line L8
        if k <= lo:  # @line L9
            table[k] = 0
        elif k >= hi:  # @line L10
            table[k] = levels - 1
        else:
            table[k] = (2 * (levels - 1) * (k - lo) + d) // (2 * d)  # @line L11
    return table


def contrast_stretching(
    image: list[list[int]],
    levels: int = 256,
    p_lo: Fraction = Fraction(0),
    p_hi: Fraction = Fraction(0),
) -> list[list[int]]:
    """Return the stretched image.

    Precondition: the image has at least one pixel, each value is in
    0 .. levels - 1, and 0 <= p_lo, 0 <= p_hi, p_lo + p_hi < 1. Use Fraction
    for p_lo and p_hi to keep the ends exact. Cost: O(W H + L) time and O(L)
    extra space.
    """
    if not 0 <= p_lo or not 0 <= p_hi or p_lo + p_hi >= 1:
        raise ValueError("need p_lo >= 0, p_hi >= 0 and p_lo + p_hi < 1")
    hist = [0] * levels  # @line L1
    for row in image:
        for g in row:
            if not 0 <= g < levels:
                raise ValueError(f"value {g} is outside 0 .. {levels - 1}")
            hist[g] += 1
    if sum(hist) == 0:
        raise ValueError("the image has no pixels")
    lo, hi = stretch_ends(hist, p_lo, p_hi)
    if lo >= hi:  # @line L7
        return [row[:] for row in image]
    table = stretch_table(levels, lo, hi)
    out = [[table[g] for g in row] for row in image]  # @line L12
    return out  # @line L13
