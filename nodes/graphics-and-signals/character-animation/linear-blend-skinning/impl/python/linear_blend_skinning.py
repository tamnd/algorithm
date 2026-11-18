# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-blend-skinning/. The authors are listed in prov/1WQ6KE.jsonl.
"""Linear blend skinning (LBS) of a mesh by a skeleton.

Each joint j has a bind world transform B_j and a current world transform
M_j, both 4 by 4 homogeneous matrices (lists of rows, column vectors). The
skinning matrix of joint j is P_j = M_j B_j^(-1). A vertex v with the sparse
weights w_j >= 0, sum w_j = 1, goes to

    v' = (sum_j w_j P_j) v.

The normal goes through the inverse transpose of the blended 3 by 3 part,
and is normalized again. The cofactor matrix cof(A) = det(A) A^(-T) is used,
so that a singular blend does not raise in the matrix inverse.
"""

from anim import cross, mul, normalize, zeros

WEIGHT_SUM_TOL = 1e-9


def skinning_matrices(world, bind_inv):
    """Return the palette P_j = M_j B_j^(-1) for all joints."""
    return [mul(m, b) for m, b in zip(world, bind_inv)]  # @line L1


def check_weights(influences):
    """Raise ValueError unless the weights are nonnegative and sum to 1."""
    if any(w < 0.0 for _, w in influences):
        raise ValueError("negative skinning weight")
    if abs(sum(w for _, w in influences) - 1.0) > WEIGHT_SUM_TOL:
        raise ValueError("skinning weights do not sum to 1")


def blend_matrix(influences, palette):
    """Return the 4 by 4 matrix A = sum_j w_j P_j of one vertex."""
    a = zeros(4)  # @line L3
    for j, w in influences:  # @line L4
        p = palette[j]
        for r in range(4):
            for c in range(4):
                a[r][c] += w * p[r][c]
    return a


def cofactor3(a):
    """Return the cofactor matrix of the 3 by 3 part of a, det(A) A^(-T)."""
    c0 = (a[0][0], a[1][0], a[2][0])
    c1 = (a[0][1], a[1][1], a[2][1])
    c2 = (a[0][2], a[1][2], a[2][2])
    k0, k1, k2 = cross(c1, c2), cross(c2, c0), cross(c0, c1)
    return [[k0[i], k1[i], k2[i]] for i in range(3)]


def transform_normal(a, n):
    """Return the unit normal A^(-T) n / |A^(-T) n| for the 3 by 3 part of a."""
    k = cofactor3(a)
    d = sum(a[0][i] * k[0][i] for i in range(3))  # det A, by the first row
    m = tuple(sum(k[r][c] * n[c] for c in range(3)) for r in range(3))
    if d < 0.0:
        m = (-m[0], -m[1], -m[2])
    return normalize(m)


def apply_point(a, v):
    """Return the point A v for a 4 by 4 affine A and a 3D point v."""
    return tuple(a[r][0] * v[0] + a[r][1] * v[1] + a[r][2] * v[2] + a[r][3] for r in range(3))


def linear_blend_skinning(vertices, weights, palette, normals=None):
    """Return (positions, normals) of the skinned mesh.

    vertices: rest positions in the bind pose (3-tuples).
    weights: per vertex, a list of (joint index, weight) pairs.
    palette: the skinning matrices P_j = M_j B_j^(-1).
    normals: optional rest normals; the result is None if they are None.
    """
    out_v = []
    out_n = [] if normals is not None else None
    for i, v in enumerate(vertices):  # @line L2
        check_weights(weights[i])
        a = blend_matrix(weights[i], palette)
        out_v.append(apply_point(a, v))  # @line L5
        if normals is not None:
            out_n.append(transform_normal(a, normals[i]))  # @line L6
    return out_v, out_n  # @line L7


def skin_by_points(vertices, weights, palette):
    """Reference form: transform the vertex by each joint, then blend the points."""
    out = []
    for i, v in enumerate(vertices):
        acc = [0.0, 0.0, 0.0]
        for j, w in weights[i]:
            p = apply_point(palette[j], v)
            for k in range(3):
                acc[k] += w * p[k]
        out.append(tuple(acc))
    return out
