# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zhang-suen-thinning/. The authors are listed in prov/PA7FJM.jsonl.

"""Zhang-Suen parallel thinning of a binary image (CACM 27(3), 1984).

An image is a list of H rows of W values 0 or 1, X[y][x], with y growing
downward. Pixels outside the image are background. The neighbors of a pixel
P1 are named clockwise from the north:

    P9 P2 P3
    P8 P1 P4
    P7 P6 P5

B(P1) is the number of foreground neighbors and A(P1) the number of 0 to 1
transitions in the circular sequence P2, P3, ..., P9, P2. One iteration has
two subiterations. Each marks, in parallel, the foreground pixels with
2 <= B <= 6, A = 1 and a step condition, and then deletes the marked pixels.
The iterations stop when an iteration deletes nothing.
"""

from typing import List, Sequence, Tuple

Image = List[List[int]]

# P2, P3, ..., P9 as offsets (dx, dy), clockwise from the north, y down.
RING = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def neighbors(img: Sequence[Sequence[int]], x: int, y: int) -> List[int]:
    """The values of P2, ..., P9 around (x, y); the outside is background."""
    h, w = len(img), len(img[0])
    out = []
    for (dx, dy) in RING:
        qx, qy = x + dx, y + dy
        out.append(img[qy][qx] if 0 <= qx < w and 0 <= qy < h else 0)
    return out


def zhang_suen(x: Sequence[Sequence[int]]) -> Tuple[Image, int]:
    """Thin x. Return the thinned image and the number of iterations run."""
    img = [list(row) for row in x]
    h = len(img)
    w = len(img[0]) if h else 0
    iterations = 0
    while True:  # @line L1
        iterations += 1
        changed = False  # @line L2
        for step in (1, 2):  # @line L3
            marked = []  # @line L4
            for y in range(h):  # @line L5
                for xx in range(w):
                    if not img[y][xx]:
                        continue
                    p2, p3, p4, p5, p6, p7, p8, p9 = n = neighbors(img, xx, y)
                    b = sum(n)  # @line L6
                    a = sum(1 for i in range(8) if n[i] == 0 and n[(i + 1) % 8] == 1)
                    if step == 1:
                        cond = p2 * p4 * p6 == 0 and p4 * p6 * p8 == 0
                    else:
                        cond = p2 * p4 * p8 == 0 and p2 * p6 * p8 == 0
                    if 2 <= b <= 6 and a == 1 and cond:  # @line L7
                        marked.append((xx, y))
            for (xx, y) in marked:  # @line L8
                img[y][xx] = 0
                changed = True
        if not changed:  # @line L9
            break
    return img, iterations  # @line L10
