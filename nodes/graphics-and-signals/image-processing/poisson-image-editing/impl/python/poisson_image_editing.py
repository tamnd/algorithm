# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/poisson-image-editing/. The authors are listed in prov/9JM0B6.jsonl.

"""Poisson image editing (Perez, Gangnet and Blake 2003) for one channel.

The target t and the source g are lists of H rows of W numbers, already
aligned, and mask[y][x] is True for the pixels of the region Omega that
is to be replaced. Pixel centers are at integer coordinates, and the
neighbors of a pixel are its 4-neighbors inside the image. For p in Omega
the discrete Poisson equation of the paper is

    |N_p| f_p - sum_{q in N_p, q in Omega} f_q
        = sum_{q in N_p, q not in Omega} t_q + sum_{q in N_p} v_pq,

with v_pq = g_p - g_q (seamless cloning) or, with mixed=True, the one of
g_p - g_q and t_p - t_q with the larger absolute value (mixed gradients).
Pixels outside Omega keep their target values (the Dirichlet condition).
Neighbors outside the image are left out, which is a Neumann condition at
the image border.

The system is solved by Gauss-Seidel sweeps with over-relaxation factor
omega in (0, 2). Each sweep costs O(|Omega|) time; the extra space is
O(|Omega|).
"""

from typing import Dict, List, Sequence, Tuple

Image = List[List[float]]
Pixel = Tuple[int, int]

STEPS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def neighbors(x: int, y: int, w: int, h: int) -> List[Pixel]:
    return [(x + dx, y + dy) for dx, dy in STEPS if 0 <= x + dx < w and 0 <= y + dy < h]


def check_region(mask: Sequence[Sequence[bool]]) -> None:
    """Raise ValueError if some 4-connected part of Omega has no neighbor outside Omega."""
    h, w = len(mask), len(mask[0])
    seen = [[False] * w for _ in range(h)]
    for y0 in range(h):
        for x0 in range(w):
            if not mask[y0][x0] or seen[y0][x0]:
                continue
            stack = [(x0, y0)]
            seen[y0][x0] = True
            touches = False
            while stack:
                x, y = stack.pop()
                for qx, qy in neighbors(x, y, w, h):
                    if not mask[qy][qx]:
                        touches = True
                    elif not seen[qy][qx]:
                        seen[qy][qx] = True
                        stack.append((qx, qy))
            if not touches:
                raise ValueError("a part of the region has no boundary pixel; the system is singular")


def build_system(t: Sequence[Sequence[float]], g: Sequence[Sequence[float]],
                 mask: Sequence[Sequence[bool]], mixed: bool = False):
    """Return (pixels, n, b, inner): the pixels of Omega in raster order, |N_p|, the right
    side b_p, and for each pixel its neighbors inside Omega."""
    h, w = len(t), len(t[0])
    pixels: List[Pixel] = [(x, y) for y in range(h) for x in range(w) if mask[y][x]]
    n: Dict[Pixel, int] = {}
    b: Dict[Pixel, float] = {}
    inner: Dict[Pixel, List[Pixel]] = {}
    for x, y in pixels:
        nb = neighbors(x, y, w, h)
        n[(x, y)] = len(nb)
        s = 0
        ins: List[Pixel] = []
        for qx, qy in nb:
            v = g[y][x] - g[qy][qx]
            if mixed:
                vt = t[y][x] - t[qy][qx]
                if abs(vt) > abs(v):
                    v = vt
            s += v
            if mask[qy][qx]:
                ins.append((qx, qy))
            else:
                s += t[qy][qx]
        b[(x, y)] = s
        inner[(x, y)] = ins
    return pixels, n, b, inner


def poisson_edit(t: Sequence[Sequence[float]], g: Sequence[Sequence[float]],
                 mask: Sequence[Sequence[bool]], omega: float = 1.0, tol: float = 1e-10,
                 max_sweeps: int = 100000, mixed: bool = False) -> Image:
    """Seamless cloning of g into t over the region mask, by Gauss-Seidel or SOR.

    Precondition: t, g and mask have the same shape H x W, 0 < omega < 2, and
    each 4-connected part of the region has a 4-neighbor outside it.
    Stops when no pixel changes by more than tol in a sweep. Cost: O(|Omega|)
    per sweep.
    """
    h = len(t)
    if h == 0 or len(t[0]) == 0:
        raise ValueError("the image is empty")
    w = len(t[0])
    if len(g) != h or len(mask) != h or any(len(r) != w for r in g) or any(len(r) != w for r in mask):
        raise ValueError("t, g and mask must have the same shape")
    if not 0 < omega < 2:
        raise ValueError("omega must be in (0, 2)")
    check_region(mask)
    f: Image = [[float(v) for v in row] for row in t]  # @line L1
    pixels, n, b, inner = build_system(t, g, mask, mixed)  # @line L2
    for _ in range(max_sweeps):  # @line L3
        delta = 0.0  # @line L4
        for x, y in pixels:  # @line L5
            s = b[(x, y)]
            for qx, qy in inner[(x, y)]:
                s += f[qy][qx]
            new = s / n[(x, y)]  # @line L6
            new = f[y][x] + omega * (new - f[y][x])  # @line L7
            delta = max(delta, abs(new - f[y][x]))
            f[y][x] = new  # @line L8
        if delta < tol:  # @line L9
            break
    return f  # @line L10
