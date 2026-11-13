# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram-equalization/. The authors are listed in prov/JQ35J4.jsonl.

"""Global histogram equalization of a gray image with integer levels.

An image is a list of rows, and each value is an integer in 0 .. levels - 1.
The level k is mapped to round((levels - 1) * c(k) / n), where c(k) is the
number of pixels with a value of at most k and n is the number of pixels.
Halves round up. All arithmetic is on integers, so the table is exact.
"""


def equalization_table(hist: list[int]) -> list[int]:
    """Return the table T with T[k] = round((L - 1) * c(k) / n), halves up.

    hist[k] is the number of pixels at level k, L = len(hist), and n is the
    sum of hist, which must be positive. Cost: O(L) time.
    """
    levels = len(hist)
    n = sum(hist)
    if n <= 0:
        raise ValueError("the histogram must count at least one pixel")
    table = [0] * levels
    c = 0  # @line L4
    for k in range(levels):  # @line L5
        c += hist[k]  # @line L6
        table[k] = (2 * (levels - 1) * c + n) // (2 * n)  # @line L7
    return table


def histogram_equalization(image: list[list[int]], levels: int = 256) -> list[list[int]]:
    """Return the equalized image.

    Precondition: the image has at least one pixel, and each value is an
    integer in 0 .. levels - 1. Cost: O(W H + L) time and O(L) extra space
    besides the output, for a W by H image with L levels.
    """
    n = sum(len(row) for row in image)  # @line L1
    if n == 0:
        raise ValueError("the image has no pixels")
    hist = [0] * levels  # @line L2
    for row in image:
        for g in row:
            if not 0 <= g < levels:
                raise ValueError(f"value {g} is outside 0 .. {levels - 1}")
            hist[g] += 1  # @line L3
    table = equalization_table(hist)
    out = [[table[g] for g in row] for row in image]  # @line L8
    return out  # @line L9
