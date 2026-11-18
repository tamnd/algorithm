# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimized-centers-of-rotation-skinning/. The authors are listed in prov/3BKQB9.jsonl.
"""Skinning with optimized centers of rotation (Le and Hodgins 2016).

Precomputation, once per mesh in the rest pose. For each vertex i with the
weight vector w_i, the center of rotation is the mean of the triangle
centroids c_t, weighted by the triangle area a_t and by the similarity of
w_i to the mean weight vector of the triangle:

    p_i = sum_t s(w_i, w_t) a_t c_t / sum_t s(w_i, w_t) a_t,

    s(w_p, w_v) = sum_{j < k} w_pj w_pk w_vj w_vk
                  exp(-(w_pj w_vk - w_pk w_vj)^2 / sigma^2).

The similarity is zero unless both vectors have at least two joints in
common, so a vertex with one joint has no center. The code then sets
p_i = v_i, which makes the frame step give linear blend skinning, that is
the rigid motion of the joint.

The mesh is first subdivided so that the weights vary little across each
triangle; the subdivision only serves the integral, and the skinned
vertices are the original ones. Here every triangle is split into four,
level by level, until the weights of the two ends of each edge differ by at
most eps. sigma and eps are tuning values.

Each frame: q is the normalized sum of the joint quaternions with the signs
aligned to the joint of the largest weight, R is its rotation, and

    t = sum_j w_ij C_j p_i - R p_i,   v_i' = R v_i + t,   n_i' = R n_i.

The cost of the precomputation here is the plain double loop over vertices
and triangles; the paper speeds it up, which this code does not do.
"""

import math

from anim import add, cross, matvec, norm, q_dot, q_from_mat3, q_to_mat3, scale, sub

SIGMA = 0.1
EPS = 0.1


def similarity(wp, wv, sigma=SIGMA):
    """Return s(w_p, w_v) for two dense weight vectors."""
    s = 0.0
    nz = [j for j in range(len(wp)) if wp[j] > 0.0 and wv[j] > 0.0]
    for a in range(len(nz)):
        j = nz[a]
        for b in range(a + 1, len(nz)):
            k = nz[b]
            d = wp[j] * wv[k] - wp[k] * wv[j]
            s += wp[j] * wp[k] * wv[j] * wv[k] * math.exp(-(d * d) / (sigma * sigma))
    return s


def subdivide(vertices, triangles, weights):
    """Split each triangle into four at the edge midpoints, with linear weights."""
    verts = list(vertices)
    ws = [list(w) for w in weights]
    mid = {}

    def midpoint(a, b):
        key = (a, b) if a < b else (b, a)
        if key not in mid:
            verts.append(scale(add(verts[a], verts[b]), 0.5))
            ws.append([0.5 * (x + y) for x, y in zip(ws[a], ws[b])])
            mid[key] = len(verts) - 1
        return mid[key]

    tris = []
    for a, b, c in triangles:
        ab, bc, ca = midpoint(a, b), midpoint(b, c), midpoint(c, a)
        tris += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
    return verts, tris, ws


def max_edge_weight_change(triangles, weights):
    m = 0.0
    for t in triangles:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            m = max(m, norm(sub(weights[a], weights[b])))
    return m


def refine(vertices, triangles, weights, eps=EPS, max_levels=4):
    """Subdivide until the weights change by at most eps along every edge."""
    for _ in range(max_levels):
        if max_edge_weight_change(triangles, weights) <= eps:
            break
        vertices, triangles, weights = subdivide(vertices, triangles, weights)
    return vertices, triangles, weights


def triangle_data(vertices, triangles, weights):
    """Return the areas, centroids and mean weight vectors of the triangles."""
    out = []
    for a, b, c in triangles:
        area = 0.5 * norm(cross(sub(vertices[b], vertices[a]), sub(vertices[c], vertices[a])))
        cen = scale(add(add(vertices[a], vertices[b]), vertices[c]), 1.0 / 3.0)
        wbar = [(x + y + z) / 3.0 for x, y, z in zip(weights[a], weights[b], weights[c])]
        out.append((area, cen, wbar))
    return out


def centers_of_rotation(vertices, triangles, weights, sigma=SIGMA, eps=EPS, max_levels=4):
    """Return one center of rotation per vertex (the precomputation)."""
    fv, ft, fw = refine(vertices, triangles, weights, eps, max_levels)
    data = triangle_data(fv, ft, fw)  # @line L1
    centers = []
    for i, v in enumerate(vertices):  # @line L2
        num = (0.0, 0.0, 0.0)  # @line L3
        den = 0.0
        for area, cen, wbar in data:  # @line L4
            s = similarity(weights[i], wbar, sigma) * area
            if s > 0.0:
                num = add(num, scale(cen, s))
                den += s
        centers.append(scale(num, 1.0 / den) if den > 0.0 else tuple(v))  # @line L5
    return centers


def blend_rotation(wi, quats):
    """Return the rotation matrix of the normalized, sign-aligned quaternion sum."""
    pivot = quats[max(range(len(wi)), key=lambda j: wi[j])]
    s = [0.0, 0.0, 0.0, 0.0]
    for j, w in enumerate(wi):
        if w == 0.0:
            continue
        q = quats[j]
        f = -w if q_dot(pivot, q) < 0.0 else w
        for k in range(4):
            s[k] += f * q[k]
    n = math.sqrt(q_dot(s, s))
    return q_to_mat3([x / n for x in s])


def apply_rigid(m, p):
    return tuple(m[r][0] * p[0] + m[r][1] * p[1] + m[r][2] * p[2] + m[r][3] for r in range(3))


def cor_skinning(vertices, weights, centers, palette, normals=None):
    """Return (positions, normals) skinned with the precomputed centers.

    palette: rigid skinning matrices C_j = M_j B_j^(-1) of the frame.
    weights: dense weight vectors, one per vertex.
    """
    quats = [q_from_mat3([row[:3] for row in p[:3]]) for p in palette]
    out_v = []
    out_n = [] if normals is not None else None
    for i, v in enumerate(vertices):  # @line L6
        wi = weights[i]
        r = blend_rotation(wi, quats)  # @line L7
        p = centers[i]
        lp = (0.0, 0.0, 0.0)
        for j, w in enumerate(wi):
            if w != 0.0:
                lp = add(lp, scale(apply_rigid(palette[j], p), w))
        t = sub(lp, matvec(r, p))  # @line L8
        out_v.append(add(matvec(r, v), t))  # @line L9
        if normals is not None:
            out_n.append(matvec(r, normals[i]))  # @line L10
    return out_v, out_n  # @line L11


def lbs(vertices, weights, palette):
    """Linear blend skinning with dense weights, the reference of the tests."""
    out = []
    for v, wi in zip(vertices, weights):
        p = (0.0, 0.0, 0.0)
        for j, w in enumerate(wi):
            if w != 0.0:
                p = add(p, scale(apply_rigid(palette[j], v), w))
        out.append(p)
    return out
