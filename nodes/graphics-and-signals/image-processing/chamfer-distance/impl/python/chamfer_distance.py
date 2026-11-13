# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chamfer-distance/. The authors are listed in prov/HJGGJE.jsonl.

"""The two pass chamfer distance transform of a binary image.

Each pixel gets the length of the cheapest path to a feature pixel, where a
step to one of the 4 edge neighbors costs a and a step to one of the 4 corner
neighbors costs b. The forward pass runs in raster order and looks at the
neighbors above and to the left; the backward pass runs in reverse raster
order and looks at the neighbors below and to the right.

For 0 < a <= b <= 2a, the result at a pixel p is the minimum over the feature
pixels q of a (M - m) + b m, where M and m are the larger and the smaller of
|p.x - q.x| and |p.y - q.y|. With the weights 3 and 4, dividing by 3 gives an
approximation of the Euclidean distance.
"""

from typing import List, Optional, Sequence

INF = float("inf")


def chamfer(image: Sequence[Sequence[int]], a: int = 3, b: int = 4) -> List[List[Optional[int]]]:
    """Return the chamfer distance to the nearest pixel with value 1.

    The result is None at every pixel when the image has no pixel with value 1.
    Pixels outside the image are skipped, not treated as features.
    """
    h = len(image)
    w = len(image[0]) if h else 0
    d = [[0 if image[y][x] else INF for x in range(w)] for y in range(h)]  # @line L1
    for y in range(h):  # @line L2
        for x in range(w):  # @line L3
            t = d[y][x]  # @line L4
            if x > 0:
                t = min(t, d[y][x - 1] + a)
            if y > 0:
                t = min(t, d[y - 1][x] + a)
                if x > 0:
                    t = min(t, d[y - 1][x - 1] + b)
                if x + 1 < w:
                    t = min(t, d[y - 1][x + 1] + b)
            d[y][x] = t
    for y in range(h - 1, -1, -1):  # @line L5
        for x in range(w - 1, -1, -1):  # @line L6
            t = d[y][x]  # @line L7
            if x + 1 < w:
                t = min(t, d[y][x + 1] + a)
            if y + 1 < h:
                t = min(t, d[y + 1][x] + a)
                if x + 1 < w:
                    t = min(t, d[y + 1][x + 1] + b)
                if x > 0:
                    t = min(t, d[y + 1][x - 1] + b)
            d[y][x] = t
    return [[None if t == INF else int(t) for t in row] for row in d]  # @line L8
