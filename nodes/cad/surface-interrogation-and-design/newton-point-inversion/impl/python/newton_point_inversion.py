# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-point-inversion/. The authors are listed in prov/BYMVEB.jsonl.

"""Newton point inversion on a tensor product Bezier patch, in floating point.

The patch r(u, v) is given by its control net on the box [0, 1] x [0, 1]. The
method of Piegl and Tiller takes the best sample of an (n + 1) x (n + 1) grid
as the start, then runs Newton's method on the two equations
f = (r - p) . r_u = 0 and g = (r - p) . r_v = 0, and stops on one of three
tests: point coincidence, zero cosine, or a step that no longer moves the
point. This version adds the guards that the page describes: a parameter on
an edge of the box whose derivative points out of the box is frozen, the
Gauss-Newton matrix (the first fundamental form) replaces a Hessian that is
not positive definite, and a step that does not lower D = |r - p|^2 is
halved. So D never increases, except by steps shorter than 1e-6 (1 + |r - p|)
in space, which only occur next to a solution.
"""

from typing import Sequence

from si1geom import Vec, dot, norm, patch_derivs, patch_point, sub


def _clamp(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def _sq_dist(P: Sequence[Sequence[Vec]], p: Vec, u: float, v: float) -> float:
    w = sub(patch_point(P, u, v), p)
    return dot(w, w)


def _direction(u: float, v: float, f: float, g: float, hess: tuple, gn: tuple) -> tuple[float, float]:
    """A descent direction for D at (u, v) inside the box, or (0, 0) at a
    point that satisfies the first order conditions of the box exactly.

    hess = (a, b, c) is half the Hessian of D, gn = (E, F, G) the
    Gauss-Newton matrix. The gradient of D/2 is (f, g).
    """
    out_u = (u == 0.0 and f > 0) or (u == 1.0 and f < 0)
    out_v = (v == 0.0 and g > 0) or (v == 1.0 and g < 0)
    a, b, c = hess
    E, F, G = gn
    if out_u and out_v:
        return 0.0, 0.0
    if out_u:
        du, dv = 0.0, -g / (c if c > 0 else G)
    elif out_v:
        du, dv = -f / (a if a > 0 else E), 0.0
    else:
        if not (a > 0 and a * c - b * b > 0):
            a, b, c = E, F, G
        det = a * c - b * b
        du, dv = (-f * c + g * b) / det, (-g * a + f * b) / det
    # a component that would leave the box at once is dropped
    if (u == 0.0 and du < 0) or (u == 1.0 and du > 0):
        du = 0.0
    if (v == 0.0 and dv < 0) or (v == 1.0 and dv > 0):
        dv = 0.0
    if f * du + g * dv < 0:
        return du, dv
    # fallback: the scaled gradient, without the components that point out
    du = 0.0 if out_u else -f / E
    dv = 0.0 if out_v else -g / G
    return du, dv


def newton_point_inversion(
    P: Sequence[Sequence[Vec]],
    p: Vec,
    n_grid: int = 10,
    eps1: float = 1e-12,
    eps2: float = 1e-12,
    max_iter: int = 100,
    trace: list | None = None,
) -> tuple[float, float]:
    """Return parameters (u, v) in [0, 1]^2 of a foot point of p on the patch P.

    The result is a point at which the first order conditions of the box
    hold to the tolerance eps2, or the last iterate when a test of L4, L9 or
    the iteration limit fires first. It is the global nearest point when the
    best grid sample lies in the basin of the global minimizer. If trace is a
    list, the iterates (u, v, |r - p|, f, g) are appended to it.
    """
    best = None
    for i in range(n_grid + 1):  # @line L1
        for j in range(n_grid + 1):
            u0, v0 = i / n_grid, j / n_grid
            d = _sq_dist(P, p, u0, v0)
            if best is None or d < best[0]:
                best = (d, u0, v0)
    D, u, v = best
    for _ in range(max_iter):  # @line L2
        r, ru, rv, ruu, ruv, rvv = patch_derivs(P, u, v)  # @line L3
        w = sub(r, p)
        f, g = dot(w, ru), dot(w, rv)
        nw = norm(w)
        if trace is not None:
            trace.append((u, v, nw, f, g))
        if nw <= eps1:  # @line L4
            return u, v
        E, F, G = dot(ru, ru), dot(ru, rv), dot(rv, rv)
        ok_u = (u == 0.0 and f > 0) or (u == 1.0 and f < 0) or abs(f) <= eps2 * nw * E ** 0.5
        ok_v = (v == 0.0 and g > 0) or (v == 1.0 and g < 0) or abs(g) <= eps2 * nw * G ** 0.5
        if ok_u and ok_v:  # @line L5
            return u, v
        hess = (E + dot(w, ruu), F + dot(w, ruv), G + dot(w, rvv))  # @line L6
        du, dv = _direction(u, v, f, g, hess, (E, F, G))  # @line L7
        small = norm((du * ru[0] + dv * rv[0], du * ru[1] + dv * rv[1], du * ru[2] + dv * rv[2])) <= 1e-6 * (1 + nw)
        lam = 1.0
        while True:  # @line L8
            un, vn = _clamp(u + lam * du), _clamp(v + lam * dv)
            Dn = _sq_dist(P, p, un, vn)
            if small:
                Dn = min(Dn, D)
            if Dn <= D * (1 + 1e-14) or lam < 1e-12:
                break
            lam *= 0.5
        if Dn > D * (1 + 1e-14):
            return u, v
        moved = norm(((un - u) * ru[0] + (vn - v) * rv[0],
                      (un - u) * ru[1] + (vn - v) * rv[1],
                      (un - u) * ru[2] + (vn - v) * rv[2]))
        u, v, D = un, vn, Dn
        if moved <= eps1:  # @line L9
            return u, v
    return u, v  # @line L10
