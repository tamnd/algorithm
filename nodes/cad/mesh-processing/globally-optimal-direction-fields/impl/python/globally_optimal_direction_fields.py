# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/globally-optimal-direction-fields/. The authors are listed in prov/8TE408.jsonl.

"""Smoothest n-direction fields on a triangle mesh (after Knoppel, Crane, Pinkall and Schroder 2013).

An n-direction field is stored at each vertex i as one complex number u_i in a
tangent frame at i: the n directions are the n-th roots of u_i / |u_i|. The
frame at i measures angles from one edge at i, with the corner angles at i
scaled so that they add up to 2 pi at an inner vertex. Moving across the edge
ij multiplies by r_ij = exp(i n (phi_j(i) + pi - phi_i(j))), where phi_i(j)
is the angle of the edge ij in the frame of i. The energy

    E(u) = sum over edges ij of w_ij |u_j - r_ij u_i|^2,  w_ij = (cot a + cot b) / 2,

is a Hermitian form u* A u. The smoothest field with u* M u = 1, M the
diagonal matrix of vertex areas, is an eigenvector of A u = lambda M u for the
smallest lambda, computed here by inverse iteration with a complex Cholesky
factor of A + eps M.
"""

import cmath
import math
import random

from mx2geom import length


def corner_angles(vertices, faces):
    """For each face, its three corner angles, from the 3D vertex positions."""
    out = []
    for tri in faces:
        p = [vertices[v] for v in tri]
        ang = []
        for k in range(3):
            a, b, c = p[k], p[(k + 1) % 3], p[(k + 2) % 3]
            u = [b[m] - a[m] for m in range(3)]
            v = [c[m] - a[m] for m in range(3)]
            dot = sum(x * y for x, y in zip(u, v))
            cr = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
            ang.append(math.atan2(math.sqrt(sum(x * x for x in cr)), dot))
        out.append(ang)
    return out


def tangent_frames(vertices, faces):
    """phi[i][j]: the angle of edge ij in the frame of i; scale[i]: the factor on the corner angles at i."""
    n = len(vertices)
    ang = corner_angles(vertices, faces)
    nxt = [dict() for _ in range(n)]  # around i, counterclockwise: neighbour a -> (neighbour b, corner angle)
    total = [0.0] * n
    for f, tri in enumerate(faces):
        for k in range(3):
            i, a, b = tri[k], tri[(k + 1) % 3], tri[(k + 2) % 3]
            nxt[i][a] = (b, ang[f][k])
            total[i] += ang[f][k]
    phi, scale = [], []
    for i in range(n):
        ends = set(b for b, _ in nxt[i].values())
        starts = [a for a in nxt[i] if a not in ends]
        inner = not starts
        s = 2 * math.pi / total[i] if inner else 1.0  # @line L1
        a = min(nxt[i]) if inner else starts[0]
        p = {a: 0.0}
        while a in nxt[i]:
            b, al = nxt[i][a]
            if b in p:
                break
            p[b] = p[a] + s * al
            a = b
        phi.append(p)
        scale.append(s)
    return phi, scale, ang


def transport(phi, i, j, n):
    """r_ij: the factor that carries an n-th power field value from the frame of i to the frame of j."""
    return cmath.exp(1j * n * (phi[j][i] + math.pi - phi[i][j]))


def energy_matrices(vertices, faces, n):
    """The Hermitian matrix A of the energy, the vertex areas M, and the edges with weights and transports."""
    nv = len(vertices)
    phi, scale, ang = tangent_frames(vertices, faces)
    weight = {}
    for f, tri in enumerate(faces):
        for k in range(3):
            i, j = tri[(k + 1) % 3], tri[(k + 2) % 3]
            e = (min(i, j), max(i, j))
            weight[e] = weight.get(e, 0.0) + 0.5 / math.tan(ang[f][k])
    a = [[0j] * nv for _ in range(nv)]
    edges = []
    for (i, j), w in sorted(weight.items()):
        r = transport(phi, i, j, n)  # @line L2
        edges.append((i, j, w, r))
        # w |u_j - r u_i|^2 = w |u_i|^2 + w |u_j|^2 - w conj(u_j) r u_i - w conj(u_i) conj(r) u_j
        a[i][i] += w  # @line L3
        a[j][j] += w
        a[j][i] -= w * r
        a[i][j] -= w * r.conjugate()
    m = [0.0] * nv
    for tri in faces:
        p0, p1, p2 = (vertices[v] for v in tri)
        l0, l1, l2 = length(p1, p2), length(p2, p0), length(p0, p1)
        s = (l0 + l1 + l2) / 2
        area = math.sqrt(max(0.0, s * (s - l0) * (s - l1) * (s - l2)))
        for v in tri:
            m[v] += area / 3  # @line L4
    return a, m, edges


def energy(edges, u):
    """E(u) = sum of w_ij |u_j - r_ij u_i|^2 over the edges."""
    return sum(w * abs(u[j] - r * u[i]) ** 2 for i, j, w, r in edges)


def hermitian_form(a, u):
    return sum((u[p].conjugate() * a[p][q] * u[q] for p in range(len(u)) for q in range(len(u)) if a[p][q])).real


def complex_cholesky(a):
    """The lower triangular l with a = l l^H, for a Hermitian positive definite a."""
    n = len(a)
    l = [[0j] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(l[i][k] * l[j][k].conjugate() for k in range(j))
            if i == j:
                if s.real <= 0:
                    raise ValueError("matrix is not positive definite")
                l[i][i] = complex(math.sqrt(s.real), 0.0)
            else:
                l[i][j] = s / l[j][j].real
    return l


def cholesky_solve(l, b):
    """Solve l l^H x = b."""
    n = len(l)
    y = [0j] * n
    for i in range(n):
        y[i] = (b[i] - sum(l[i][k] * y[k] for k in range(i))) / l[i][i].real
    x = [0j] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(l[k][i].conjugate() * x[k] for k in range(i + 1, n))) / l[i][i].real
    return x


def apply_a(edges, u):
    """A u, from the edge list (each edge adds its 2 by 2 block)."""
    out = [0j] * len(u)
    for i, j, w, r in edges:
        out[i] += w * (u[i] - r.conjugate() * u[j])
        out[j] += w * (u[j] - r * u[i])
    return out


def residual(edges, m, u, lam):
    """The size of A u - lambda M u in the M^(-1) norm."""
    au = apply_a(edges, u)
    return math.sqrt(sum(abs(au[p] - lam * m[p] * u[p]) ** 2 / m[p] for p in range(len(u))))


def smoothest_field(vertices, faces, n=4, seed=0, eps=1e-8, tol=1e-10, max_steps=10000):
    """The smoothest n-direction field: (u, lambda, steps), with u* M u = 1 and lambda = u* A u.

    The loop stops when the residual |A u - lambda M u| in the M^(-1) norm is at most
    tol * max(1, lambda); then some eigenvalue lies within that distance of lambda.
    """
    a, m, edges = energy_matrices(vertices, faces, n)
    nv = len(vertices)
    shift = eps * max(abs(a[i][i]) for i in range(nv)) / max(m)
    b = [[a[p][q] + (shift * m[p] if p == q else 0) for q in range(nv)] for p in range(nv)]
    l = complex_cholesky(b)  # @line L5
    rng = random.Random(seed)
    u = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(nv)]  # @line L6
    for step in range(1, max_steps + 1):
        y = cholesky_solve(l, [m[p] * u[p] for p in range(nv)])  # @line L7
        norm = math.sqrt(sum(m[p] * abs(y[p]) ** 2 for p in range(nv)))
        u = [x / norm for x in y]  # @line L8
        lam = energy(edges, u)  # @line L9
        if residual(edges, m, u, lam) <= tol * max(1.0, lam):  # @line L10
            return u, lam, step  # @line L11
    raise ArithmeticError("inverse iteration did not converge in max_steps steps")


def directions(u, n):
    """One of the n directions at each vertex, as an angle in the frame of the vertex (None where u = 0)."""
    return [cmath.phase(x) / n if abs(x) > 0 else None for x in u]


def face_indices(vertices, faces, u, n):
    """The index of the field in each face, a multiple of 1/n (the singularities are the faces with index != 0).

    index = (n K_f + sum of the turns) / (2 pi n), where K_f is the scaled angle sum of f minus pi (the
    curvature of the frames in f) and each turn, in (-pi, pi], is the angle from the transported value
    to the value at the next corner.
    """
    phi, scale, ang = tangent_frames(vertices, faces)
    out = []
    for f, tri in enumerate(faces):
        k_f = sum(scale[tri[c]] * ang[f][c] for c in range(3)) - math.pi
        turn = 0.0
        for c in range(3):
            p, q = tri[c], tri[(c + 1) % 3]
            turn += cmath.phase(u[q] / (transport(phi, p, q, n) * u[p]))
        out.append((turn + n * k_f) / (2 * math.pi * n))
    return out
