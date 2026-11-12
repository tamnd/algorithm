# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midpoint-ellipse-algorithm/. The authors are listed in prov/VKBD4R.jsonl.


def ellipse_quadrant(a: int, b: int) -> list[tuple[int, int]]:
    """The pixels of the first quadrant of the ellipse b^2 x^2 + a^2 y^2 = a^2 b^2, from (0, b) to (a, 0).

    Precondition: a and b are integers, a >= 0 and b >= 0. Pixel centers are integer points.
    Region 1 takes one pixel per column and region 2 one pixel per row; each decision is the sign of
    4 F at the midpoint between the two candidates, with ties to the inner pixel. Integer additions,
    multiplications by constants and sign tests only. Cost: at most a + b + 1 steps, O(1) extra space.
    """
    a2, b2 = a * a, b * b
    x, y = 0, b  # @line L1
    d1 = 4 * b2 - 4 * a2 * b + a2
    out = [(x, y)]  # @line L2
    while a2 * (2 * y - 1) > 2 * b2 * (x + 1):  # @line L3
        if d1 < 0:  # @line L4
            d1 += 4 * b2 * (2 * x + 3)
        else:  # @line L5
            d1 += 4 * b2 * (2 * x + 3) - 8 * a2 * (y - 1)
            y -= 1
        x += 1  # @line L6
        out.append((x, y))
    d2 = b2 * (2 * x + 1) ** 2 + 4 * a2 * (y - 1) ** 2 - 4 * a2 * b2  # @line L7
    while y > 0:  # @line L8
        if d2 < 0:  # @line L9
            d2 += 8 * b2 * (x + 1) + 4 * a2 * (3 - 2 * y)
            x += 1
        else:  # @line L10
            d2 += 4 * a2 * (3 - 2 * y)
        y -= 1  # @line L11
        out.append((x, y))
    while x < a:  # @line L12
        x += 1
        out.append((x, 0))
    return out


def midpoint_ellipse(xc: int, yc: int, a: int, b: int) -> list[tuple[int, int]]:
    """All pixels of the axis-aligned ellipse with semi-axes a, b >= 0 about the integer point (xc, yc).

    The quadrant is mirrored four ways (PLOT-4). Pixels on the axes appear in two quadrants; each
    pixel is returned one time, sorted. Cost: Θ(a + b) time.
    """
    pts = set()
    for x, y in ellipse_quadrant(a, b):
        for sx in (1, -1):
            for sy in (1, -1):
                pts.add((xc + sx * x, yc + sy * y))
    return sorted(pts)
