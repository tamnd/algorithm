# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/curvature-tensor-estimation/. The authors are listed in prov/TJZ7S2.jsonl.

"""Principal curvatures and directions at the vertices of a triangle mesh.

taubin_curvature follows Taubin (ICCV 1995). At each vertex it samples a
normal curvature along each edge, kappa_ij = 2 N.(x_i - x_j) / |x_i - x_j|^2,
averages kappa_ij T T^T over the edge directions T in the tangent plane, and
reads k1 = 3 m1 - m2, k2 = 3 m2 - m1 from the eigenvalues m1 >= m2 of the
average. The sign is chosen so that a sphere with outward normals has
positive curvature.

edge_curvature follows Cohen-Steiner and Morvan (SoCG 2003). It sums
beta(e) |e cap B| e e^T over the edges, with beta the signed dihedral angle,
and divides by the area of a region B around the vertex. Here B is the mixed
Voronoi cell of the vertex, and with rings = r also the cells of the vertices
at most r edges away. Each cell holds half of each edge at its vertex and no
other edge. An eigenvector e of the tensor is a direction of no bending, so
its eigenvalue is the curvature in the tangent direction N x e.

Both functions return, for each vertex, (k1, k2, d1, d2, N) with k1 >= k2,
d1 and d2 the unit principal directions and N the unit normal used. A vertex
whose region meets the border gets None.
"""

import math

from mx1mesh import (boundary_vertices, cross, dot, edge_faces, face_area, face_cross, mixed_area, neighbours, norm,
                     orient3d, scale, sub, unit)


def vertex_normals(points, faces):
    """The unit normal at each vertex: the sum of the face normals weighted by the face areas."""
    acc = [(0.0, 0.0, 0.0) for _ in points]
    for f in faces:
        c = face_cross(points, f)  # twice the area times the unit normal
        for i in f:
            acc[i] = tuple(a + b for a, b in zip(acc[i], c))
    return [unit(a) for a in acc]


def tangent_basis(N):
    """Two unit vectors E1, E2 such that E1, E2, N is a right-handed orthonormal frame."""
    e = min(((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)), key=lambda t: abs(dot(t, N)))
    E1 = unit(cross(N, e))
    return E1, cross(N, E1)


def eigen2(a, b, c):
    """Eigenvalues l1 >= l2 and unit eigenvectors (2-tuples) of the symmetric matrix [[a, b], [b, c]]."""
    mean, half = (a + c) / 2, math.hypot((a - c) / 2, b)
    phi = 0.5 * math.atan2(2 * b, a - c)  # the angle of the eigenvector of l1
    return mean + half, mean - half, (math.cos(phi), math.sin(phi)), (-math.sin(phi), math.cos(phi))


def principal_from_samples(samples):
    """Taubin's step from samples (w, kappa, t1, t2): weight, normal curvature, unit tangent direction in 2D.

    Returns k1 >= k2 and their directions (2-tuples) from the eigenvalues m1 >= m2 of
    M = sum w kappa t t^T / sum w, with k1 = 3 m1 - m2 and k2 = 3 m2 - m1.
    """
    a = b = c = W = 0.0
    for w, kappa, t1, t2 in samples:
        a += w * kappa * t1 * t1  # @line L6
        b += w * kappa * t1 * t2
        c += w * kappa * t2 * t2
        W += w
    m1, m2, v1, v2 = eigen2(a / W, b / W, c / W)  # @line L7
    return 3 * m1 - m2, 3 * m2 - m1, v1, v2  # @line L8


def _lift(E1, E2, v):
    return tuple(v[0] * p + v[1] * q for p, q in zip(E1, E2))


def taubin_curvature(points, faces, normals=None):
    n = len(points)
    N = normals if normals is not None else vertex_normals(points, faces)  # @line L1
    nb = neighbours(n, faces)
    ef = edge_faces(faces)
    border = boundary_vertices(faces)
    out = []
    for i in range(n):  # @line L2
        if i in border or not nb[i]:
            out.append(None)
            continue
        E1, E2 = tangent_basis(N[i])
        samples = []
        for j in nb[i]:  # @line L3
            d = sub(points[i], points[j])
            t = sub(d, scale(dot(d, N[i]), N[i]))  # @line L4
            t1, t2 = dot(t, E1), dot(t, E2)
            tn = math.hypot(t1, t2)
            kappa = 2 * dot(N[i], d) / dot(d, d)
            w = sum(face_area(points, faces[k]) for k in ef[(min(i, j), max(i, j))])  # @line L5
            samples.append((w, kappa, t1 / tn, t2 / tn))
        k1, k2, v1, v2 = principal_from_samples(samples)
        out.append((k1, k2, _lift(E1, E2, v1), _lift(E1, E2, v2), N[i]))
    return out


def dihedral(points, faces, e, f1, f2):
    """The signed angle between the normals of the faces f1 and f2 at the edge e: positive at a convex edge."""
    n1, n2 = unit(face_cross(points, faces[f1])), unit(face_cross(points, faces[f2]))
    angle = math.atan2(norm(cross(n1, n2)), dot(n1, n2))
    opp = next(v for v in faces[f2] if v not in e)
    a, b, c = (points[v] for v in faces[f1])
    # exact sign: at a convex edge the far corner of f2 lies below the plane of f1
    return -angle if orient3d(a, b, c, points[opp]) > 0 else angle


def edge_curvature(points, faces, normals=None, rings=0):
    n = len(points)
    N = normals if normals is not None else vertex_normals(points, faces)
    border = boundary_vertices(faces)
    nb = neighbours(n, faces)
    A = mixed_area(points, faces)
    T = [[0.0] * 6 for _ in range(n)]  # xx, xy, xz, yy, yz, zz of each cell
    for e, fs in edge_faces(faces).items():
        if len(fs) != 2:
            continue
        beta = dihedral(points, faces, e, *fs)
        d = sub(points[e[1]], points[e[0]])
        L = norm(d)
        u = scale(1 / L, d)
        m = (u[0] * u[0], u[0] * u[1], u[0] * u[2], u[1] * u[1], u[1] * u[2], u[2] * u[2])
        for v in e:  # the cell of v holds half of the edge
            for k in range(6):
                T[v][k] += beta * (L / 2) * m[k]
    out = []
    for i in range(n):
        region = {i}
        for _ in range(rings):
            region |= {j for v in region for j in nb[v]}
        if region & border or not nb[i]:
            out.append(None)
            continue
        area = sum(A[v] for v in region)
        xx, xy, xz, yy, yz, zz = (sum(T[v][k] for v in region) / area for k in range(6))
        M = ((xx, xy, xz), (xy, yy, yz), (xz, yz, zz))
        E1, E2 = tangent_basis(N[i])

        def q(p, r):
            return dot(p, tuple(dot(row, r) for row in M))

        l1, l2, v1, v2 = eigen2(q(E1, E1), q(E1, E2), q(E2, E2))
        # the eigenvalue of the direction e is the curvature across e, in the direction N x e
        pairs = [(l1, cross(N[i], _lift(E1, E2, v1))), (l2, cross(N[i], _lift(E1, E2, v2)))]
        (k1, d1), (k2, d2) = sorted(pairs, key=lambda t: -t[0])
        out.append((k1, k2, d1, d2, N[i]))
    return out
