# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pineda-rasterization/. The authors are listed in prov/JW7NSM.jsonl.

Point = tuple[int, int]


def edge(a: Point, b: Point, p: Point) -> int:
    """Return the edge function E_ab(p) = (b - a) x (p - a), twice the signed area of (a, b, p)."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def pineda_rasterize(
    v0: Point, v1: Point, v2: Point, width: int, height: int, sub: int = 16
) -> list[tuple[int, int]]:
    """Return the pixels (i, j) whose centers a triangle covers, in row-major order.

    The vertices are integers in units of 1/sub pixel, with y growing downward.
    The center of pixel (i, j) is at (i*sub + sub/2, j*sub + sub/2), so sub must
    be even and positive. A center on an edge is decided by the top-left rule, so
    a center on an edge shared by two triangles goes to exactly one of them.
    Both windings are accepted. A degenerate triangle covers no pixel.

    Cost: O(1) setup and O(1) integer additions per pixel of the bounding box,
    clipped to the width by height screen. Extra space O(1) besides the output.
    """
    if sub <= 0 or sub % 2:
        raise ValueError("sub must be a positive even integer")
    area2 = edge(v0, v1, v2)  # @line L1
    if area2 == 0:  # @line L2
        return []
    if area2 < 0:  # @line L3
        v1, v2 = v2, v1
    verts = (v0, v1, v2)
    a_s: list[int] = []
    b_s: list[int] = []
    c_s: list[int] = []
    bias: list[int] = []
    for k in range(3):  # @line L4
        a, b = verts[(k + 1) % 3], verts[(k + 2) % 3]
        ak, bk = a[1] - b[1], b[0] - a[0]  # @line L5
        a_s.append(ak)
        b_s.append(bk)
        c_s.append(a[0] * b[1] - a[1] * b[0])
        bias.append(0 if ak > 0 or (ak == 0 and bk > 0) else -1)  # @line L6
    half = sub // 2
    xmin, xmax = min(v[0] for v in verts), max(v[0] for v in verts)
    ymin, ymax = min(v[1] for v in verts), max(v[1] for v in verts)
    i0 = max(0, -((half - xmin) // sub))  # @line L7
    i1 = min(width - 1, (xmax - half) // sub)
    j0 = max(0, -((half - ymin) // sub))
    j1 = min(height - 1, (ymax - half) // sub)
    out: list[tuple[int, int]] = []
    if i0 > i1 or j0 > j1:
        return out
    px, py = i0 * sub + half, j0 * sub + half  # @line L8
    row = [a_s[k] * px + b_s[k] * py + c_s[k] + bias[k] for k in range(3)]  # @line L9
    dx = [sub * a_s[k] for k in range(3)]
    dy = [sub * b_s[k] for k in range(3)]
    for j in range(j0, j1 + 1):  # @line L10
        e0, e1, e2 = row  # @line L11
        for i in range(i0, i1 + 1):  # @line L12
            if e0 >= 0 and e1 >= 0 and e2 >= 0:  # @line L13
                out.append((i, j))
            e0 += dx[0]  # @line L14
            e1 += dx[1]
            e2 += dx[2]
        row = [row[k] + dy[k] for k in range(3)]  # @line L15
    return out
