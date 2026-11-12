# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conservative-rasterization/. The authors are listed in prov/HFMB32.jsonl.

Point = tuple[int, int]


def conservative_rasterize(
    v0: Point, v1: Point, v2: Point, width: int, height: int, sub: int = 16, inner: bool = False
) -> list[tuple[int, int]]:
    """Return the pixels whose closed squares meet the closed triangle, in row-major order.

    With inner=True, return instead the pixels whose closed squares lie inside the closed
    triangle (the underestimate). The vertices are integers in units of 1/sub pixel, y down,
    and pixel (i, j) is the square [i*sub, (i+1)*sub] x [j*sub, (j+1)*sub] with its center at
    (i*sub + sub/2, j*sub + sub/2); sub must be even and positive. Precondition: the triangle
    has nonzero area; a degenerate triangle returns no pixel. Both windings are accepted.

    Cost: O(1) setup and O(1) integer additions per pixel of the bounding box grown by
    one pixel and clipped to the width by height screen. Extra space O(1) besides the output.
    """
    if sub <= 0 or sub % 2:
        raise ValueError("sub must be a positive even integer")
    area2 = (v1[0] - v0[0]) * (v2[1] - v0[1]) - (v1[1] - v0[1]) * (v2[0] - v0[0])  # @line L1
    if area2 == 0:
        return []
    if area2 < 0:  # @line L2
        v1, v2 = v2, v1
    verts = (v0, v1, v2)
    half = sub // 2
    eqs = []
    for k in range(3):  # @line L3
        a, b = verts[(k + 1) % 3], verts[(k + 2) % 3]
        ak, bk = a[1] - b[1], b[0] - a[0]
        ck = a[0] * b[1] - a[1] * b[0]
        r = (abs(ak) + abs(bk)) * half  # @line L4
        eqs.append((ak, bk, ck - r if inner else ck + r))  # @line L5
    xmin, xmax = min(v[0] for v in verts), max(v[0] for v in verts)
    ymin, ymax = min(v[1] for v in verts), max(v[1] for v in verts)
    if inner:  # @line L6
        i0, i1 = -(-xmin // sub), xmax // sub - 1
        j0, j1 = -(-ymin // sub), ymax // sub - 1
    else:
        i0, i1 = -(-xmin // sub) - 1, xmax // sub
        j0, j1 = -(-ymin // sub) - 1, ymax // sub
    i0, i1 = max(0, i0), min(width - 1, i1)
    j0, j1 = max(0, j0), min(height - 1, j1)
    out: list[tuple[int, int]] = []
    if i0 > i1 or j0 > j1:
        return out
    px, py = i0 * sub + half, j0 * sub + half
    row = [a * px + b * py + c for a, b, c in eqs]  # @line L7
    for j in range(j0, j1 + 1):  # @line L8
        e0, e1, e2 = row
        for i in range(i0, i1 + 1):  # @line L9
            if e0 >= 0 and e1 >= 0 and e2 >= 0:  # @line L10
                out.append((i, j))
            e0 += sub * eqs[0][0]  # @line L11
            e1 += sub * eqs[1][0]
            e2 += sub * eqs[2][0]
        row = [row[k] + sub * eqs[k][1] for k in range(3)]  # @line L12
    return out
