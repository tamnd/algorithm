# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hexahedral-sweeping/. The authors are listed in prov/AETFHW.jsonl.

"""One-to-one sweeping of a planar quad mesh into layers of hexahedra.

The source face is a planar quad mesh: points pts[v] = (x, y) and quads
(a, b, c, d) listed counterclockwise. The boundary loop of the source face
is a list of vertex indices. The linking sides are already meshed, so the
positions of the loop vertices on each layer k = 0..K are given as 3D points.
Each layer places its interior vertices by the least squares affine map from
the source plane that best fits the loop of that layer, as in the affine
sweep of Knupp. Every hex joins a quad of layer k to the same quad of layer
k + 1. With int or Fraction input every value and every sign is exact.
"""

from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from mg4geom import corners_positive, det3, solve

Point2 = Tuple
Point3 = Tuple
Affine = Tuple[List[List], List]  # (L as 3 rows of 2 entries, t as 3 entries)


def fit_affine(pts: Sequence[Point2], loop: Sequence[int], targets: Sequence[Point3]) -> Affine:
    """The least squares affine map p -> L p + t from the plane to space with L p_v + t ~ targets[i].

    Precondition: the loop points pts[loop[i]] are not all on one line, so the
    normal equations are regular. Cost: O(n) for n loop points, all exact.
    """
    sxx = sxy = syy = sx = sy = Fraction(0)
    n = len(loop)
    for v in loop:
        x, y = pts[v]
        sxx += x * x
        sxy += x * y
        syy += y * y
        sx += x
        sy += y
    normal = [[sxx, sxy, sx], [sxy, syy, sy], [sx, sy, n]]
    lin, tr = [], []
    for c in range(3):
        rhs = [Fraction(0)] * 3
        for v, q in zip(loop, targets):
            x, y = pts[v]
            rhs[0] += x * q[c]
            rhs[1] += y * q[c]
            rhs[2] += q[c]
        a, b, t = solve(normal, rhs)
        lin.append([a, b])
        tr.append(t)
    return lin, tr


def apply_affine(m: Affine, p: Point2) -> Point3:
    """L p + t."""
    lin, tr = m
    return tuple(lin[c][0] * p[0] + lin[c][1] * p[1] + tr[c] for c in range(3))


def sweep(
    pts: Sequence[Point2],
    quads: Sequence[Tuple[int, int, int, int]],
    loop: Sequence[int],
    layers: Sequence[Sequence[Point3]],
):
    """Sweep the source mesh through the K + 1 given loop layers.

    layers[k][i] is the position of loop vertex loop[i] on layer k. Returns
    (nodes, hexes, maps, ok): nodes[k][v] is the position of vertex v on layer
    k, hexes is the list of K * len(quads) hexes in the standard vertex order,
    maps[k] is the fitted affine map of layer k, and ok tells whether every hex
    has 8 positive corner Jacobians.
    Precondition: K >= 1 and the loop is not collinear.
    Cost: O(K n) time and space for n source vertices and quads.
    """
    on_loop = {v: i for i, v in enumerate(loop)}
    nodes: List[List[Point3]] = []
    maps: List[Affine] = []
    for k in range(len(layers)):  # @line L1
        m = fit_affine(pts, loop, layers[k])  # @line L2
        maps.append(m)
        row = []
        for v in range(len(pts)):  # @line L3
            row.append(tuple(layers[k][on_loop[v]]) if v in on_loop else apply_affine(m, pts[v]))  # @line L4
        nodes.append(row)
    hexes = []  # @line L5
    for k in range(len(layers) - 1):  # @line L6
        for a, b, c, d in quads:  # @line L7
            lo, hi = nodes[k], nodes[k + 1]
            hexes.append([lo[a], lo[b], lo[c], lo[d], hi[a], hi[b], hi[c], hi[d]])  # @line L8
    ok = all(corners_positive(h) for h in hexes)  # @line L9
    return nodes, hexes, maps, ok  # @line L10


def slab_coefficients(m0: Affine, m1: Affine, p: Point2):
    """The Bernstein coefficients (b0, b1, b2) in w of det DF at the source point p.

    F(p, w) = (1 - w)(L0 p + t0) + w (L1 p + t1) is the slab map between two
    affine layers. Its Jacobian has the columns (1 - w) L0 + w L1 (two columns)
    and d(p) = (L1 - L0) p + t1 - t0, so det DF is a quadratic in w.
    """
    (l0, _), (l1, _) = m0, m1
    d = tuple(a - b for a, b in zip(apply_affine(m1, p), apply_affine(m0, p)))
    a1 = tuple(l0[c][0] for c in range(3))
    a2 = tuple(l0[c][1] for c in range(3))
    c1 = tuple(l1[c][0] for c in range(3))
    c2 = tuple(l1[c][1] for c in range(3))
    b0 = det3(a1, a2, d)
    b2 = det3(c1, c2, d)
    b1 = (det3(a1, c2, d) + det3(c1, a2, d)) / Fraction(2)
    return b0, b1, b2


def quadratic_positive(b0, b1, b2) -> bool:
    """Exact test that b0 (1 - w)^2 + 2 b1 w (1 - w) + b2 w^2 > 0 for all w in [0, 1]."""
    return b0 > 0 and b2 > 0 and (b1 >= 0 or b1 * b1 < b0 * b2)


def certify(pts: Sequence[Point2], loop: Sequence[int], nodes, maps) -> bool:
    """Prove that every hex is valid at every point, not only at its corners.

    Returns True when (1) every layer is exactly the affine image of the source
    plane, so each hex is the image of a source quad times [0, 1] under the slab
    map, and (2) det DF > 0 on the convex hull of the loop times [0, 1] for each
    slab. det DF is affine in p, so it is enough to test the loop vertices.
    The source quads must be strictly convex for the conclusion; see the proof.
    Cost: O(K n).
    """
    for k, m in enumerate(maps):  # @line L11
        if any(nodes[k][v] != apply_affine(m, pts[v]) for v in range(len(pts))):  # @line L12
            return False
    for k in range(len(maps) - 1):  # @line L13
        for v in loop:  # @line L14
            b0, b1, b2 = slab_coefficients(maps[k], maps[k + 1], pts[v])  # @line L15
            if not quadratic_positive(b0, b1, b2):  # @line L16
                return False
    return True  # @line L17


def grid_mesh(xs: Sequence, ys: Sequence):
    """A structured quad mesh of the rectangle with the given breakpoints, and its boundary loop.

    Returns (pts, quads, loop); vertex (i, j) has the index i * len(ys) + j, quads are
    counterclockwise, and the loop runs counterclockwise from (xs[0], ys[0]).
    """
    nx, ny = len(xs), len(ys)
    pts = [(Fraction(x), Fraction(y)) for x in xs for y in ys]
    idx = lambda i, j: i * ny + j
    quads = [(idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)) for i in range(nx - 1) for j in range(ny - 1)]
    loop = [idx(i, 0) for i in range(nx)] + [idx(nx - 1, j) for j in range(1, ny)]
    loop += [idx(i, ny - 1) for i in range(nx - 2, -1, -1)] + [idx(0, j) for j in range(ny - 2, 0, -1)]
    return pts, quads, loop


def planar_layer(pts: Sequence[Point2], loop: Sequence[int], a: Sequence[Sequence], t: Sequence, z) -> List[Point3]:
    """The loop of a planar layer: (A p + t, z) for each loop vertex p."""
    out = []
    for v in loop:
        x, y = pts[v]
        out.append((a[0][0] * x + a[0][1] * y + t[0], a[1][0] * x + a[1][1] * y + t[1], Fraction(z)))
    return out
