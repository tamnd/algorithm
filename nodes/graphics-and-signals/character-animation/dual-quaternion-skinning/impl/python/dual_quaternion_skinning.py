# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-quaternion-skinning/. The authors are listed in prov/SVNNAZ.jsonl.
"""Dual quaternion skinning (DQS) by dual quaternion linear blending.

A rigid transform with the rotation quaternion r and the translation t is the
unit dual quaternion r + eps d with d = (1/2) (0, t) r, and t = 2 d r*.
Each joint has the skinning transform P_j = M_j B_j^(-1), which must be
rigid. For a vertex with the weights w_j, the method (Kavan, Collins, Zara and
O'Sullivan 2007, 2008):

1. aligns the sign of each r_j with a pivot quaternion (the joint of the
   largest weight of the vertex), because r and -r are the same rotation;
2. blends b = sum_j w_j s_j (r_j + eps d_j);
3. normalizes: c0 = b0 / |b0|, ce = be / |b0| - (c0 . be / |b0|) c0;
4. applies the rigid transform of c0 + eps ce to the vertex and c0 to the
   normal.

Step 3 needs b0 != 0. With the pivot alignment, |b0| >= the pivot weight,
so this holds; without alignment (align=False) b0 can be zero, and the code
raises ValueError.
"""

import math

from anim import q_conj, q_dot, q_from_mat3, q_mul, q_rotate

REAL_PART_TOL = 1e-12


def dq_from_transform(m):
    """Return (r, d) of a rigid 4 by 4 transform, with d = (1/2) (0, t) r."""
    r = q_from_mat3([row[:3] for row in m[:3]])
    t = (0.0, m[0][3], m[1][3], m[2][3])
    d = tuple(0.5 * x for x in q_mul(t, r))
    return r, d


def dq_translation(r, d):
    """Return the translation t = 2 d r* (vector part) of a unit dual quaternion."""
    p = q_mul(d, q_conj(r))
    return (2.0 * p[1], 2.0 * p[2], 2.0 * p[3])


def dq_palette(palette):
    """Return the unit dual quaternions of the rigid skinning matrices."""
    return [dq_from_transform(p) for p in palette]  # @line L1


def blend(influences, dqs, align=True):
    """Return the normalized blend (c0, ce) of the dual quaternions of one vertex."""
    pivot = dqs[max(influences, key=lambda jw: jw[1])[0]][0]  # @line L3
    b0 = [0.0, 0.0, 0.0, 0.0]  # @line L4
    be = [0.0, 0.0, 0.0, 0.0]
    for j, w in influences:  # @line L5
        r, d = dqs[j]
        s = -1.0 if (align and q_dot(pivot, r) < 0.0) else 1.0  # @line L6
        for k in range(4):  # @line L7
            b0[k] += s * w * r[k]
            be[k] += s * w * d[k]
    n0 = math.sqrt(q_dot(b0, b0))
    if n0 <= REAL_PART_TOL:  # @line L8
        raise ValueError("the blended real part is zero: no rigid transform")
    c0 = tuple(x / n0 for x in b0)  # @line L9
    ce = tuple(x / n0 for x in be)
    k = q_dot(c0, ce)
    ce = tuple(e - k * c for e, c in zip(ce, c0))
    return c0, ce


def dq_apply(c0, ce, v):
    """Apply the rigid transform of the unit dual quaternion c0 + eps ce to a point."""
    t = dq_translation(c0, ce)  # @line L10
    p = q_rotate(c0, v)
    return (p[0] + t[0], p[1] + t[1], p[2] + t[2])  # @line L11


def dual_quaternion_skinning(vertices, weights, palette, normals=None, align=True):
    """Return (positions, normals) of the mesh skinned by DQS.

    vertices: rest positions in the bind pose; weights: per vertex, a list of
    (joint index, weight) pairs with nonnegative weights that sum to 1;
    palette: the rigid skinning matrices P_j = M_j B_j^(-1).
    """
    dqs = dq_palette(palette)
    out_v = []
    out_n = [] if normals is not None else None
    for i, v in enumerate(vertices):  # @line L2
        c0, ce = blend(weights[i], dqs, align)
        out_v.append(dq_apply(c0, ce, v))
        if normals is not None:
            out_n.append(q_rotate(c0, normals[i]))  # @line L11
    return out_v, out_n  # @line L12
