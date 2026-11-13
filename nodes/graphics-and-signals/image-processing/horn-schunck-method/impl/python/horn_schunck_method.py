# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horn-schunck-method/. The authors are listed in prov/J0BY18.jsonl.

"""Horn-Schunck optical flow, as in the 1981 paper.

Two frames E1 and E2 of W x H gray values are lists of rows; row index y,
column index x. The brightness derivatives are estimated at the center of
each 2 x 2 x 2 cube of samples, so the flow has (W - 1) x (H - 1) points.
The local average uses weights 1/6 for the four edge neighbors and 1/12 for
the four corner neighbors; at the border, a missing neighbor is replaced by
the nearest point inside (index clamping). The iteration is the Jacobi form
of the paper. Values may be float or Fraction.
"""


def derivatives(e1: list[list], e2: list[list]) -> tuple[list[list], list[list], list[list]]:
    """Ex, Ey, Et at the cube centers: each is the mean of four first differences."""
    h, w = len(e1), len(e1[0])
    ex, ey, et = [], [], []
    for y in range(h - 1):
        rx, ry, rt = [], [], []
        for x in range(w - 1):
            a, b = e1, e2
            rx.append((a[y][x + 1] - a[y][x] + a[y + 1][x + 1] - a[y + 1][x] + b[y][x + 1] - b[y][x] + b[y + 1][x + 1] - b[y + 1][x]) / 4)
            ry.append((a[y + 1][x] - a[y][x] + a[y + 1][x + 1] - a[y][x + 1] + b[y + 1][x] - b[y][x] + b[y + 1][x + 1] - b[y][x + 1]) / 4)
            rt.append((b[y][x] - a[y][x] + b[y][x + 1] - a[y][x + 1] + b[y + 1][x] - a[y + 1][x] + b[y + 1][x + 1] - a[y + 1][x + 1]) / 4)
        ex.append(rx)
        ey.append(ry)
        et.append(rt)
    return ex, ey, et


def local_average(u: list[list]) -> list[list]:
    """The weighted mean of the 8 neighbors, 1/6 at the edges and 1/12 at the corners."""
    h, w = len(u), len(u[0])

    def at(y, x):
        return u[min(max(y, 0), h - 1)][min(max(x, 0), w - 1)]

    out = []
    for y in range(h):
        row = []
        for x in range(w):
            edges = at(y - 1, x) + at(y + 1, x) + at(y, x - 1) + at(y, x + 1)
            corners = at(y - 1, x - 1) + at(y - 1, x + 1) + at(y + 1, x - 1) + at(y + 1, x + 1)
            row.append(edges / 6 + corners / 12)
        out.append(row)
    return out


def horn_schunck(e1, e2, alpha2, iterations, u=None, v=None):
    """Run the Jacobi iteration; alpha2 is the weight of smoothness. Return (u, v)."""
    ex, ey, et = derivatives(e1, e2)  # @line L1
    h, w = len(ex), len(ex[0])
    if u is None:
        u = [[0] * w for _ in range(h)]  # @line L2
        v = [[0] * w for _ in range(h)]
    for _ in range(iterations):  # @line L3
        ub, vb = local_average(u), local_average(v)  # @line L4
        nu, nv = [], []
        for y in range(h):
            ru, rv = [], []
            for x in range(w):
                gx, gy = ex[y][x], ey[y][x]
                r = (gx * ub[y][x] + gy * vb[y][x] + et[y][x]) / (alpha2 + gx * gx + gy * gy)  # @line L5
                ru.append(ub[y][x] - gx * r)  # @line L6
                rv.append(vb[y][x] - gy * r)
            nu.append(ru)
            nv.append(rv)
        u, v = nu, nv
    return u, v  # @line L7
