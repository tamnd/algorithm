# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-element-method/. The authors are listed in prov/03WMHA.jsonl.

"""Direct boundary element method for the 2D Laplace equation, constant elements.

The boundary is a closed polygon, traversed counterclockwise, cut into M
straight elements. On each element u and the outward normal derivative
q = du/dn are constant, and the boundary integral equation

    (1/2) u(x) + int_G dG/dn_y(x, y) u(y) ds_y = int_G G(x, y) q(y) ds_y,
    G(x, y) = -(1 / (2 pi)) ln |x - y|,

is collocated at the element midpoints. The integrals over straight elements
are computed in closed form, including the weakly singular one.
"""

import math

import scimat


def segment_integrals(x, a, b):
    """Return (g, h) = (int G(x, y) ds_y, int dG/dn_y(x, y) ds_y) over the segment a b.

    The normal of the segment is the outward normal of a counterclockwise
    boundary: n = (t_y, -t_x) for the unit tangent t from a to b.
    The formula holds for any point x, also on the segment.
    """
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    tx, ty = (b[0] - a[0]) / length, (b[1] - a[1]) / length
    nx, ny = ty, -tx
    rx, ry = x[0] - a[0], x[1] - a[1]
    s0 = rx * tx + ry * ty  # projection of x on the line
    d = rx * nx + ry * ny  # signed distance of x from the line

    def prim(u):
        # antiderivative of ln sqrt(u^2 + d^2) in u
        if d == 0:
            return u * math.log(abs(u)) - u if u != 0 else 0.0
        return 0.5 * u * math.log(u * u + d * d) - u + d * math.atan(u / d)

    ln_int = prim(length - s0) - prim(-s0)
    g = -ln_int / (2 * math.pi)
    # int (y - x) . n / r^2 ds is the signed angle that the segment subtends at x
    ax, ay = a[0] - x[0], a[1] - x[1]
    bx, by = b[0] - x[0], b[1] - x[1]
    if d == 0:
        angle = 0.0
    else:
        angle = math.atan2(ax * by - ay * bx, ax * bx + ay * by)
        # the kernel (y - x) . n / r^2 equals -d / r^2, so the sign is that of -d
        angle = -abs(angle) if d > 0 else abs(angle)
    h = -angle / (2 * math.pi)
    return g, h


def polygon_elements(vertices, per_side):
    """Cut a counterclockwise polygon into per_side equal elements per side."""
    elems = []
    nv = len(vertices)
    for k in range(nv):
        p, r = vertices[k], vertices[(k + 1) % nv]
        for j in range(per_side):
            s, t = j / per_side, (j + 1) / per_side
            elems.append(((p[0] + s * (r[0] - p[0]), p[1] + s * (r[1] - p[1])), (p[0] + t * (r[0] - p[0]), p[1] + t * (r[1] - p[1]))))
    return elems


def midpoint(e):
    return ((e[0][0] + e[1][0]) / 2, (e[0][1] + e[1][1]) / 2)


def outward_normal(e):
    (ax, ay), (bx, by) = e
    length = math.hypot(bx - ax, by - ay)
    return ((by - ay) / length, -(bx - ax) / length)


def assemble(elems):
    """Return the M by M matrices G and H of the collocation system (H includes 1/2 I)."""
    m = len(elems)
    g = scimat.zeros(m)
    h = scimat.zeros(m)
    for i in range(m):  # @line L2
        xi = midpoint(elems[i])
        for j in range(m):
            gij, hij = segment_integrals(xi, elems[j][0], elems[j][1])
            g[i][j] = gij  # @line L3
            h[i][j] = hij + (0.5 if i == j else 0.0)  # @line L4
    return g, h


def bem_solve(elems, kinds, values):
    """Solve the mixed problem. kinds[j] is 'u' (u given) or 'q' (q given) on element j.

    Return (u, q, (G, H)): the boundary values of u and q on all elements.
    """
    m = len(elems)  # @line L1
    g, h = assemble(elems)
    # H u = G q; move the known values to the right side
    a = scimat.zeros(m)
    rhs = [0.0] * m
    for j in range(m):  # @line L5
        for i in range(m):
            if kinds[j] == "u":
                a[i][j] = -g[i][j]
                rhs[i] -= h[i][j] * values[j]
            else:
                a[i][j] = h[i][j]
                rhs[i] += g[i][j] * values[j]
    z = scimat.solve(a, rhs)  # @line L6
    u = [values[j] if kinds[j] == "u" else z[j] for j in range(m)]
    q = [z[j] if kinds[j] == "u" else values[j] for j in range(m)]
    return u, q, (g, h)


def interior_value(x, elems, u, q):
    """Return u(x) = sum_j (g_j(x) q_j - h_j(x) u_j) at a point x inside the domain."""
    total = 0.0
    for e, uj, qj in zip(elems, u, q):
        gj, hj = segment_integrals(x, e[0], e[1])
        total += gj * qj - hj * uj  # @line L7
    return total


def dirichlet(vertices, per_side, u_exact, points):
    """Solve the Dirichlet problem with boundary data u_exact; return (q, values at points)."""
    elems = polygon_elements(vertices, per_side)
    u_bc = [u_exact(*midpoint(e)) for e in elems]
    u, q, _ = bem_solve(elems, ["u"] * len(elems), u_bc)
    return q, [interior_value(p, elems, u, q) for p in points]  # @line L8
