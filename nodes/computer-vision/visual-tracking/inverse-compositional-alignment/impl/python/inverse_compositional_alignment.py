# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-compositional-alignment/. The authors are listed in prov/ZVVMQX.jsonl.

"""Inverse compositional image alignment (Baker and Matthews) for an affine
warp, with the forwards additive Lucas-Kanade algorithm as a reference.

Images are lists of rows, indexed img[v][u]; the center of pixel (u, v) is
the point (u, v). The template T is an image and the region is a list of
integer points (u, v) of T, each at least one pixel inside T. The affine warp
has the parameters p = (p1, ..., p6) of Baker and Matthews:

    W(x; p) = ((1 + p1) u + p3 v + p5, p2 u + (1 + p4) v + p6),

so p = 0 is the identity. The goal is the p that minimizes
sum over the region of (I(W(x; p)) - T(x))^2.
"""

import math

from cvla import inv, mul, solve


def sample(img, u, v):
    """Bilinear sample at the real point (u, v), indices clamped."""
    h, w = len(img), len(img[0])
    u0, v0 = math.floor(u), math.floor(v)
    fu, fv = u - u0, v - v0

    def at(vv, uu):
        return img[min(max(vv, 0), h - 1)][min(max(uu, 0), w - 1)]

    top = (1 - fu) * at(v0, u0) + fu * at(v0, u0 + 1)
    bottom = (1 - fu) * at(v0 + 1, u0) + fu * at(v0 + 1, u0 + 1)
    return (1 - fv) * top + fv * bottom


def warp_matrix(p):
    """The 3 x 3 matrix of W(.; p) in homogeneous coordinates."""
    return [[1 + p[0], p[2], p[4]], [p[1], 1 + p[3], p[5]], [0.0, 0.0, 1.0]]


def params(a):
    """The parameters p of an affine 3 x 3 matrix (last row 0, 0, 1)."""
    return [a[0][0] - 1, a[1][0], a[0][1], a[1][1] - 1, a[0][2], a[1][2]]


def warp(p, u, v):
    """The point W((u, v); p)."""
    return ((1 + p[0]) * u + p[2] * v + p[4], p[1] * u + (1 + p[3]) * v + p[5])


def warp_jacobian(u, v):
    """dW/dp at (u, v): a 2 x 6 matrix, the same for every p."""
    return [[u, 0.0, v, 0.0, 1.0, 0.0], [0.0, u, 0.0, v, 0.0, 1.0]]


def compose_inverse(p, dp):
    """The parameters of W(.; p) composed with the inverse of W(.; dp)."""
    return params(mul(warp_matrix(p), inv(warp_matrix(dp))))


def cost(t, region, img, p):
    """The sum of squared differences of the problem."""
    return sum((sample(img, *warp(p, u, v)) - t[v][u]) ** 2 for u, v in region)


def precompute(t, region):
    """Steepest descent images S(x) = grad T(x) dW/dp(x; 0) and the Hessian
    H = sum S(x)^T S(x). The gradient is the central difference of T."""
    sd = []
    for u, v in region:
        gu = (t[v][u + 1] - t[v][u - 1]) / 2  # @line L1
        gv = (t[v + 1][u] - t[v - 1][u]) / 2
        jac = warp_jacobian(u, v)  # @line L2
        sd.append([gu * jac[0][i] + gv * jac[1][i] for i in range(6)])  # @line L3
    hess = [[sum(s[i] * s[j] for s in sd) for j in range(6)] for i in range(6)]  # @line L4
    return sd, hess


def ic_align(t, region, img, p0=None, iters=100, tol=1e-8):
    """Inverse compositional alignment. Returns (p, costs), where costs[j] is
    the cost before step j. Raises ValueError if the Hessian is singular."""
    p = list(p0) if p0 is not None else [0.0] * 6
    sd, hess = precompute(t, region)
    costs = []
    for _ in range(iters):  # @line L5
        err = [sample(img, *warp(p, u, v)) - t[v][u] for u, v in region]  # @line L6
        costs.append(sum(e * e for e in err))
        g = [sum(s[i] * e for s, e in zip(sd, err)) for i in range(6)]  # @line L7
        dp = solve(hess, g)  # @line L8
        p = compose_inverse(p, dp)  # @line L9
        if math.sqrt(sum(x * x for x in dp)) < tol:  # @line L10
            break
    costs.append(cost(t, region, img, p))
    return p, costs  # @line L11


def fa_align(t, region, img, p0=None, iters=100, tol=1e-8):
    """Forwards additive Lucas-Kanade, the reference: the gradient of the
    image at the warped points and a new Hessian at every step."""
    p = list(p0) if p0 is not None else [0.0] * 6
    for _ in range(iters):
        sd, err = [], []
        for u, v in region:
            wu, wv = warp(p, u, v)
            gu = (sample(img, wu + 1, wv) - sample(img, wu - 1, wv)) / 2
            gv = (sample(img, wu, wv + 1) - sample(img, wu, wv - 1)) / 2
            jac = warp_jacobian(u, v)
            sd.append([gu * jac[0][i] + gv * jac[1][i] for i in range(6)])
            err.append(t[v][u] - sample(img, wu, wv))
        hess = [[sum(s[i] * s[j] for s in sd) for j in range(6)] for i in range(6)]
        g = [sum(s[i] * e for s, e in zip(sd, err)) for i in range(6)]
        dp = solve(hess, g)
        p = [a + b for a, b in zip(p, dp)]
        if math.sqrt(sum(x * x for x in dp)) < tol:
            break
    return p
