# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bresenham-line-algorithm/. The authors are listed in prov/VSRX7E.jsonl.


def bresenham_line(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    """Return the pixels of the segment from (x0, y0) to (x1, y1), in order from the start.

    The endpoints are integer pixel centers. Along the major axis (the axis with the larger
    change) the line gets one pixel per step. On the minor axis it gets the pixel nearest to the
    exact line. A tie (the exact line passes half way between two pixels) goes to the pixel
    nearer to the start. Only integer additions, subtractions and sign tests are used.
    Cost: max(|x1 - x0|, |y1 - y0|) + 1 steps, O(1) extra space besides the output.
    """
    dx, dy = abs(x1 - x0), abs(y1 - y0)  # @line L1
    sx = 1 if x1 >= x0 else -1  # @line L2
    sy = 1 if y1 >= y0 else -1
    x_major = dx >= dy  # @line L3
    m, n = (dx, dy) if x_major else (dy, dx)
    e = 2 * n - m  # @line L4
    x, y = x0, y0
    out: list[tuple[int, int]] = []
    for _ in range(m + 1):  # @line L5
        out.append((x, y))  # @line L6
        if e > 0:  # @line L7
            if x_major:  # @line L8
                y += sy
            else:
                x += sx
            e -= 2 * m  # @line L9
        e += 2 * n  # @line L10
        if x_major:  # @line L11
            x += sx
        else:
            y += sy
    return out
