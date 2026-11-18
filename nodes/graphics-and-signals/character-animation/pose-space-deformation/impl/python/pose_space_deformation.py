# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pose-space-deformation/. The authors are listed in prov/1BB6ZV.jsonl.
"""Pose space deformation (Lewis, Cordner and Fong 2000) on a 2D skinned mesh.

The base layer is linear blend skinning: vertex i goes to A_i(p) v_i with
A_i(p) = sum_j w_ij M_j(p) B_j^(-1), a 3 by 3 homogeneous matrix in 2D.
For each example pose p_e an artist sculpts the shape s_e. The correction
d_ei = A_i(p_e)^(-1) s_ei - v_i is stored in the rest frame, before skinning,
and it is interpolated over the poses by Gaussian radial basis functions

    phi(r) = exp(-r^2 / (2 sigma^2)).

The width sigma is a tuning choice. At a pose p the mesh is

    v'_i = A_i(p) (v_i + sum_e c_ei phi(|p - p_e|)),

where the coefficients c solve Phi c = d with Phi_ef = phi(|p_e - p_f|).
"""

import math

from anim import T_apply, T_inv, make_T, mul, rot2, solve


def gaussian(r, sigma):
    """Return the Gaussian radial basis function exp(-r^2 / (2 sigma^2))."""
    return math.exp(-r * r / (2.0 * sigma * sigma))


def pose_distance(p, q):
    """Return the Euclidean distance between two pose vectors (joint angles)."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


def chain_transforms(pose, joints):
    """World transforms of a planar chain with joints at the rest points joints[j].

    Joint j turns by pose[j] about its rest point, after its parent j - 1.
    Return (M, B_inv), the current and inverse bind transforms (3 by 3).
    """
    m, b_inv = [], []
    parent = make_T(rot2(0.0), (0.0, 0.0))
    prev = (0.0, 0.0)
    for j, c in enumerate(joints):
        local = make_T(rot2(pose[j]), (c[0] - prev[0], c[1] - prev[1]))
        parent = mul(parent, local)
        m.append(parent)
        b_inv.append(T_inv(make_T(rot2(0.0), c)))
        prev = c
    return m, b_inv


def blend(influences, m, b_inv):
    """Return A = sum_j w_j M_j B_j^(-1) for one vertex."""
    a = [[0.0] * 3 for _ in range(3)]
    for j, w in influences:
        p = mul(m[j], b_inv[j])
        for r in range(3):
            for c in range(3):
                a[r][c] += w * p[r][c]
    return a


def skin(rest, weights, pose, joints):
    """Linear blend skinning of the rest vertices at a pose."""
    m, b_inv = chain_transforms(pose, joints)
    return [T_apply(blend(wi, m, b_inv), v) for v, wi in zip(rest, weights)]


def train(rest, weights, joints, poses, shapes, sigma):
    """Return the RBF coefficients c[e][i] (2D offsets) for the example poses and shapes."""
    d = []
    for p, s in zip(poses, shapes):  # @line L1
        m, b_inv = chain_transforms(p, joints)
        row = []
        for v, wi, si in zip(rest, weights, s):
            u = T_apply(T_inv(blend(wi, m, b_inv)), si)
            row.extend((u[0] - v[0], u[1] - v[1]))
        d.append(row)
    phi = [[gaussian(pose_distance(p, q), sigma) for q in poses] for p in poses]  # @line L2
    c = solve(phi, d)  # @line L3
    n = len(rest)
    return [[(row[2 * i], row[2 * i + 1]) for i in range(n)] for row in c]


def deform(rest, weights, joints, poses, coeffs, sigma, pose):
    """Return the pose space deformation of the mesh at a new pose."""
    r = [gaussian(pose_distance(pose, pe), sigma) for pe in poses]  # @line L4
    m, b_inv = chain_transforms(pose, joints)
    out = []
    for i, (v, wi) in enumerate(zip(rest, weights)):  # @line L5
        ox = sum(re * ce[i][0] for re, ce in zip(r, coeffs))
        oy = sum(re * ce[i][1] for re, ce in zip(r, coeffs))
        u = (v[0] + ox, v[1] + oy)  # @line L6
        out.append(T_apply(blend(wi, m, b_inv), u))  # @line L7
    return out  # @line L8
