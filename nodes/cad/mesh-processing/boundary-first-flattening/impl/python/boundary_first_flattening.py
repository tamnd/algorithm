# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-first-flattening/. The authors are listed in prov/HE01QC.jsonl.

"""Boundary first flattening (Sawhney and Crane 2017), with a dense solver.

A conformal change of metric with log scale factor u changes the discrete
curvature by the cotangent Laplacian A (positive semidefinite, with
A_ij = -(cot a + cot b)/2 for an edge ij):

    new curvature = old curvature + A u,

at interior vertices (angle defect Omega) and at boundary vertices (turning
angle k). A flat image needs the new Omega to be 0 at the interior vertices.
Given the scale factors on the boundary (Dirichlet data), the code finds the
new turning angles, and given the turning angles (Neumann data), it finds
the scale factors. It then builds the boundary polygon, closes it by the
smallest weighted change of its lengths, and extends it to the interior by
a harmonic map.
"""

import math

from mx2geom import boundary_loop, corner_angle, length, solve


def curvatures_and_laplacian(vertices, faces):
    """The cotangent Laplacian (dense), the angle sum at each vertex and the boundary loop."""
    n = len(vertices)
    a = [[0.0] * n for _ in range(n)]
    angle_sum = [0.0] * n
    for tri in faces:
        ls = [length(vertices[tri[(k + 1) % 3]], vertices[tri[(k + 2) % 3]]) for k in range(3)]
        for k in range(3):
            # ls[k] is the edge opposite corner k.
            theta = corner_angle(ls[k], ls[(k + 1) % 3], ls[(k + 2) % 3])
            angle_sum[tri[k]] += theta
            w = 0.5 / math.tan(theta)
            i, j = tri[(k + 1) % 3], tri[(k + 2) % 3]
            a[i][j] -= w
            a[j][i] -= w
            a[i][i] += w
            a[j][j] += w
    return a, angle_sum, boundary_loop(faces)


def dirichlet_to_neumann(a, angle_sum, loop, u_boundary):
    """Scale factors u_B on the boundary -> (u at all vertices, new turning angles k~ on the boundary)."""
    n = len(a)
    on_b = set(loop)
    inner = [v for v in range(n) if v not in on_b]
    u = [0.0] * n
    for v, x in zip(loop, u_boundary):
        u[v] = x
    if inner:
        rows = [[a[i][j] for j in inner] for i in inner]
        rhs = [[-(2 * math.pi - angle_sum[i]) - sum(a[i][b] * u[b] for b in loop)] for i in inner]
        for i, x in zip(inner, solve(rows, rhs)):  # @line L3
            u[i] = x[0]
    k_new = [(math.pi - angle_sum[b]) + sum(a[b][j] * u[j] for j in range(n)) for b in loop]  # @line L4
    return u, k_new


def neumann_to_dirichlet(a, angle_sum, loop, k_target):
    """Turning angles k~ on the boundary (adding up to 2 pi) -> u at all vertices, with u = 0 at loop[0]."""
    n = len(a)
    if abs(sum(k_target) - 2 * math.pi) > 1e-9:
        raise ValueError("the target turning angles must add up to 2 pi")
    target = [-(2 * math.pi - angle_sum[v]) for v in range(n)]
    for b, k in zip(loop, k_target):
        target[b] = k - (math.pi - angle_sum[b])
    # A u = target has a one-dimensional kernel (the constants); fix u at loop[0].
    fix = loop[0]
    free = [v for v in range(n) if v != fix]
    rows = [[a[i][j] for j in free] for i in free]
    x = solve(rows, [[target[i]] for i in free])  # @line L6
    u = [0.0] * n
    for v, xv in zip(free, x):
        u[v] = xv[0]
    return u


def boundary_polygon(vertices, loop, u, k_new):
    """The closed boundary polygon with turning angles k_new and lengths near e^((u_i+u_j)/2) l_ij.

    Returns the points, the asked lengths and the lengths after closing.
    """
    m = len(loop)
    lt = []
    for t in range(m):
        i, j = loop[t], loop[(t + 1) % m]
        lt.append(math.exp((u[i] + u[j]) / 2) * length(vertices[i], vertices[j]))  # @line L7
    phi, tang = 0.0, []
    for t in range(m):
        # The edge from loop[t] to loop[t+1] leaves vertex loop[t], where the curve turns by k_new[t].
        phi += k_new[t]
        tang.append((math.cos(phi), math.sin(phi)))  # @line L8
    # Close the curve: minimize sum (l* - l~)^2 / l~ subject to sum l* T = 0, a 2 x 2 system.
    g = [[sum(lt[t] * tang[t][r] * tang[t][c] for t in range(m)) for c in range(2)] for r in range(2)]
    gap = [sum(lt[t] * tang[t][r] for t in range(m)) for r in range(2)]
    lam = solve(g, [[gap[0]], [gap[1]]])
    ls = [lt[t] - lt[t] * (tang[t][0] * lam[0][0] + tang[t][1] * lam[1][0]) for t in range(m)]  # @line L9
    pts, p = {}, (0.0, 0.0)
    for t in range(m):
        pts[loop[t]] = p  # @line L10
        p = (p[0] + ls[t] * tang[t][0], p[1] + ls[t] * tang[t][1])
    return pts, lt, ls


def harmonic_extension(a, loop, pts, n):
    """Extend the boundary positions to the interior: (A x)_i = 0 at every interior vertex."""
    on_b = set(loop)
    inner = [v for v in range(n) if v not in on_b]
    out = [pts.get(v) for v in range(n)]
    if inner:
        rows = [[a[i][j] for j in inner] for i in inner]
        rhs = [[-sum(a[i][b] * pts[b][c] for b in loop) for c in range(2)] for i in inner]
        for i, x in zip(inner, solve(rows, rhs)):  # @line L11
            out[i] = (x[0], x[1])
    return out


def bff(vertices, faces, u_boundary=None, k_target=None):
    """Flatten a disk mesh. Give the boundary scale factors u_boundary or the turning angles k_target.

    With neither, u_boundary = 0 (keep the boundary lengths). Returns (points, info), where info has
    the boundary loop, the scale factors u, the turning angles k, the asked boundary lengths and the
    boundary lengths after closing, in the order of the loop.
    """
    a, angle_sum, loop = curvatures_and_laplacian(vertices, faces)  # @line L1
    if k_target is None:  # @line L2
        if u_boundary is None:
            u_boundary = [0.0] * len(loop)
        u, k_new = dirichlet_to_neumann(a, angle_sum, loop, u_boundary)
    else:  # @line L5
        k_new = list(k_target)
        u = neumann_to_dirichlet(a, angle_sum, loop, k_new)
    pts, asked, closed = boundary_polygon(vertices, loop, u, k_new)
    out = harmonic_extension(a, loop, pts, len(vertices))
    return out, {"loop": loop, "u": u, "k": k_new, "asked": asked, "lengths": closed}  # @line L12
