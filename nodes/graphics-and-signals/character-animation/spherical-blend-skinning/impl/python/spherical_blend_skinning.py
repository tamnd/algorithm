# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spherical-blend-skinning/. The authors are listed in prov/E1S4SH.jsonl.
"""Spherical blend skinning (SBS) of Kavan and Zara (2005).

Each joint has a rigid skinning transform C_j x = R_j x + t_j (that is
P_j = M_j B_j^(-1)). For a vertex with the joint set J and the weights w_j:

1. The center of rotation r_c is the least squares solution of the
   equations C_a r_c = C_b r_c for all pairs a < b in J, that is
   (R_a - R_b) r_c = t_b - t_a. If the solution is not unique, the one of
   minimal norm is taken. The center depends only on J, so it is cached.
2. The rotation Q is the normalized linear blend (QLERP) of the joint
   quaternions after the sign alignment with a pivot.
3. v' = Q (v - r_c) + sum_j w_j C_j r_c, and the normal goes to Q n.

The minimal norm solution is N^+ g with N = D^T D and g = D^T e, where D
stacks the blocks R_a - R_b and e the blocks t_b - t_a. The pseudo-inverse
of the symmetric 3 by 3 matrix N comes from its eigenvalues (cyclic Jacobi),
with the eigenvalues at most RANK_TOL times the largest one treated as zero.
An SVD of D is more accurate, because the normal equations square its
condition number; for this small test code the eigenvalues are enough.
"""

import math

from anim import add, matvec, q_dot, q_from_mat3, q_rotate, scale, sub

RANK_TOL = 1e-12


def sym_eig3(s):
    """Eigenvalues and unit eigenvectors of a symmetric 3 by 3 matrix (cyclic Jacobi)."""
    a = [list(map(float, row)) for row in s]
    v = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    for _ in range(60):
        off = a[0][1] ** 2 + a[0][2] ** 2 + a[1][2] ** 2
        if off <= 1e-32 * (sum(a[i][i] ** 2 for i in range(3)) + 1e-300):
            break
        for p, q in ((0, 1), (0, 2), (1, 2)):
            if a[p][q] == 0.0:
                continue
            th = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
            t = math.copysign(1.0, th) / (abs(th) + math.sqrt(th * th + 1.0))
            c = 1.0 / math.sqrt(t * t + 1.0)
            sn = t * c
            for k in range(3):
                akp, akq = a[k][p], a[k][q]
                a[k][p], a[k][q] = c * akp - sn * akq, sn * akp + c * akq
            for k in range(3):
                apk, aqk = a[p][k], a[q][k]
                a[p][k], a[q][k] = c * apk - sn * aqk, sn * apk + c * aqk
            for k in range(3):
                vkp, vkq = v[k][p], v[k][q]
                v[k][p], v[k][q] = c * vkp - sn * vkq, sn * vkp + c * vkq
    return [a[i][i] for i in range(3)], [tuple(v[k][i] for k in range(3)) for i in range(3)]


def split(m):
    """Return (R, t) of a 4 by 4 rigid transform."""
    return [row[:3] for row in m[:3]], (m[0][3], m[1][3], m[2][3])


def center_of_rotation(joints, palette):
    """Return the minimal norm least squares center of the joint set."""
    n = [[0.0] * 3 for _ in range(3)]
    g = [0.0, 0.0, 0.0]
    js = sorted(joints)
    for ia in range(len(js)):
        ra, ta = split(palette[js[ia]])
        for ib in range(ia + 1, len(js)):
            rb, tb = split(palette[js[ib]])
            d = [[ra[r][c] - rb[r][c] for c in range(3)] for r in range(3)]
            e = (tb[0] - ta[0], tb[1] - ta[1], tb[2] - ta[2])
            for r in range(3):
                for c in range(3):
                    n[r][c] += sum(d[k][r] * d[k][c] for k in range(3))
                g[r] += sum(d[k][r] * e[k] for k in range(3))
    vals, vecs = sym_eig3(n)
    top = max(vals)
    out = [0.0, 0.0, 0.0]
    for lam, u in zip(vals, vecs):  # minimal norm: drop the null space
        if top > 0.0 and lam > RANK_TOL * top:
            c = sum(u[k] * g[k] for k in range(3)) / lam
            for k in range(3):
                out[k] += c * u[k]
    return tuple(out)


def qlerp(influences, quats):
    """Return the normalized linear blend of the joint quaternions with aligned signs."""
    pivot = quats[max(influences, key=lambda jw: jw[1])[0]]
    s = [0.0, 0.0, 0.0, 0.0]
    for j, w in influences:
        q = quats[j]
        f = -w if q_dot(pivot, q) < 0.0 else w
        for k in range(4):
            s[k] += f * q[k]
    n = math.sqrt(q_dot(s, s))
    return tuple(x / n for x in s)


def spherical_blend_skinning(vertices, weights, palette, normals=None, cache=None, linear_rotation=False):
    """Return (positions, normals) of the mesh skinned by SBS.

    palette: rigid skinning matrices P_j = M_j B_j^(-1). cache: an optional
    dict from joint sets to centers, kept by the caller for one frame.
    linear_rotation=True replaces Q by the matrix sum_j w_j R_j, which turns
    the formula into linear blend skinning (for the tests).
    """
    if cache is None:
        cache = {}
    quats = [q_from_mat3(split(p)[0]) for p in palette]
    out_v = []
    out_n = [] if normals is not None else None
    for i, v in enumerate(vertices):  # @line L1
        key = tuple(sorted(j for j, _ in weights[i]))  # @line L2
        if key not in cache:  # @line L3
            rc = center_of_rotation(key, palette)  # @line L4
            cache[key] = rc  # @line L5
        rc = cache[key]  # @line L6
        m = (0.0, 0.0, 0.0)
        for j, w in weights[i]:
            m = add(m, scale(add(matvec(split(palette[j])[0], rc), split(palette[j])[1]), w))
        if linear_rotation:
            a = [[sum(w * split(palette[j])[0][r][c] for j, w in weights[i]) for c in range(3)] for r in range(3)]
            out_v.append(add(matvec(a, sub(v, rc)), m))
            continue
        q = qlerp(weights[i], quats)  # @line L7
        out_v.append(add(q_rotate(q, sub(v, rc)), m))  # @line L8
        if normals is not None:
            out_n.append(q_rotate(q, normals[i]))  # @line L9
    return out_v, out_n  # @line L10
