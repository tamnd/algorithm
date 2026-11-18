# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deformation-transfer/. The authors are listed in prov/CM6PX4.jsonl.
"""Deformation transfer for triangle meshes (Sumner and Popovic 2004).

Each triangle (v1, v2, v3) gets a fourth vertex

    v4 = v1 + (v2 - v1) x (v3 - v1) / sqrt(|(v2 - v1) x (v3 - v1)|),

and the frame V = [v2 - v1, v3 - v1, v4 - v1] (columns). The deformation of
a source triangle is the matrix S = V~ V^(-1). For the target, the frames of
the unknown deformed triangles are linear in the unknown vertices (the n
mesh vertices and one fourth vertex per triangle), so the transfer is the
least squares problem

    min sum over pairs (t, s) of |V~_t V_t^(-1) - S_s|_F^2,

with one vertex fixed to remove the global translation. The normal matrix
depends only on the target rest mesh; it is factored once and used for the
x, y and z coordinates.
"""

import math

from anim import cross, inv, matvec, mul, norm, solve, sub, transpose


def fourth_vertex(v1, v2, v3):
    """Return v1 + c / sqrt(|c|) with c = (v2 - v1) x (v3 - v1)."""
    c = cross(sub(v2, v1), sub(v3, v1))
    s = math.sqrt(norm(c))
    if s == 0.0:
        raise ValueError("degenerate triangle")
    return tuple(a + b / s for a, b in zip(v1, c))


def frame(v1, v2, v3):
    """Return the 3 by 3 matrix with the columns v2 - v1, v3 - v1 and v4 - v1."""
    v4 = fourth_vertex(v1, v2, v3)
    cols = [sub(v2, v1), sub(v3, v1), sub(v4, v1)]
    return transpose(cols)


def source_deformations(src_rest, src_def, tris):
    """Return S_s = V~_s V_s^(-1) for every source triangle."""
    out = []
    for a, b, c in tris:  # @line L1
        v = frame(src_rest[a], src_rest[b], src_rest[c])
        vt = frame(src_def[a], src_def[b], src_def[c])
        out.append(mul(vt, inv(v)))
    return out


def transfer(tgt_rest, tgt_tris, pairs, s_mats, fixed):
    """Return (vertices, fourth vertices) of the deformed target.

    pairs is a list of (target triangle, source triangle) indices; the
    correspondence may be many to many. fixed is (vertex index, position).
    """
    n = len(tgt_rest)
    q = [inv(frame(tgt_rest[a], tgt_rest[b], tgt_rest[c])) for a, b, c in tgt_tris]  # @line L2
    rows, rhs = [], []
    for t, s in pairs:  # @line L3
        a, b, c = tgt_tris[t]
        qt = q[t]
        for k in range(3):
            coef = {b: qt[0][k], c: qt[1][k], n + t: qt[2][k]}
            coef[a] = coef.get(a, 0.0) - (qt[0][k] + qt[1][k] + qt[2][k])
            rows.append(coef)
            rhs.append(tuple(s_mats[s][r][k] for r in range(3)))
    fi, fp = fixed
    unknowns = [u for u in range(n + len(tgt_tris)) if u != fi]  # @line L4
    col = {u: i for i, u in enumerate(unknowns)}
    size = len(unknowns)
    ata = [[0.0] * size for _ in range(size)]
    atb = [[0.0] * 3 for _ in range(size)]
    for coef, r in zip(rows, rhs):
        r = [r[d] - coef.get(fi, 0.0) * fp[d] for d in range(3)]
        items = [(col[u], w) for u, w in coef.items() if u != fi]
        for i, wi in items:
            for j, wj in items:
                ata[i][j] += wi * wj
            for d in range(3):
                atb[i][d] += wi * r[d]
    x = solve(ata, atb)  # @line L5
    out = []
    for v in range(n):  # @line L6
        out.append(tuple(fp) if v == fi else tuple(x[col[v]]))
    fourth = [tuple(x[col[n + t]]) for t in range(len(tgt_tris))]
    return out, fourth  # @line L7


def energy(tgt_rest, tgt_tris, pairs, s_mats, verts, fourth):
    """Return the transfer energy for target vertices and free fourth vertices."""
    e = 0.0
    for t, s in pairs:
        a, b, c = tgt_tris[t]
        qt = inv(frame(tgt_rest[a], tgt_rest[b], tgt_rest[c]))
        vt = transpose([sub(verts[b], verts[a]), sub(verts[c], verts[a]), sub(fourth[t], verts[a])])
        m = mul(vt, qt)
        e += sum((m[i][j] - s_mats[s][i][j]) ** 2 for i in range(3) for j in range(3))
    return e


def apply_affine(m, t, p):
    """Return m p + t."""
    return tuple(x + y for x, y in zip(matvec(m, p), t))
