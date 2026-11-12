# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midpoint-circle-algorithm/. The authors are listed in prov/MR2G6P.jsonl.


def circle_octant(r: int) -> list[tuple[int, int]]:
    """The pixels of the second octant (0 <= x <= y) of the circle of radius r about the origin.

    Precondition: r is an integer, r >= 0. Pixel centers are integer points. In each column x of
    the octant the pixel is (x, y) with y the integer nearest to (r^2 - x^2)^(1/2); there is never a tie.
    Integer additions and sign tests only. Cost: about r / 2^(1/2) + 1 steps, O(1) extra space.
    """
    x, y, d = 0, r, 1 - r  # @line L1
    out: list[tuple[int, int]] = []
    while x <= y:  # @line L2
        out.append((x, y))  # @line L3
        if d < 0:  # @line L4
            d += 2 * x + 3
        else:  # @line L5
            d += 2 * (x - y) + 5
            y -= 1
        x += 1  # @line L6
    return out


def midpoint_circle(xc: int, yc: int, r: int) -> list[tuple[int, int]]:
    """All pixels of the circle of integer radius r >= 0 about the integer point (xc, yc).

    The octant is mirrored eight ways (PLOT-8). Pixels on the axes and on the diagonals appear in
    two octants; each pixel is returned one time, sorted. Cost: Θ(r) time and output size.
    """
    pts = set()
    for x, y in circle_octant(r):
        for u, v in ((x, y), (y, x)):
            for su in (1, -1):
                for sv in (1, -1):
                    pts.add((xc + su * u, yc + sv * v))
    return sorted(pts)
