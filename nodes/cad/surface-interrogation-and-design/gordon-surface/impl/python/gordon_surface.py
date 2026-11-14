# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gordon-surface/. The authors are listed in prov/8125BY.jsonl.

"""Gordon surface through a compatible network of B-spline curves.

The input is two families of curves. The v-curves f_i(v), i = 0..n, have one
degree q and lie on the surface at u = us[i]. The u-curves g_j(u), j = 0..m,
have one degree p and lie at v = vs[j]. The network is compatible when
f_i(vs[j]) = g_j(us[i]) for all i and j. The surface is the Boolean sum

    S = S1 + S2 - T,

where S1 interpolates the v-curves across u with degree p, S2 interpolates the
u-curves across v with degree q, and T interpolates the points of
intersection with the same two interpolation operators. All three are brought
to one pair of knot vectors by knot insertion, which does not change them, and
then the control nets are added. With int or Fraction input every step is
exact. The caller raises the curves of a family to one degree first.
"""

from si3spline import (add, check_curve, curve_point, interpolate, merge_knots,
                       refine, refine_surface, sub)


def _degree(curve):
    knots, ctrl = curve
    p = len(knots) - len(ctrl) - 1
    check_curve(knots, p, ctrl)
    return p


def _common(curves):
    """Lines L1 and L2: one degree and one knot vector for a family of curves."""
    degs = {_degree(c) for c in curves}
    if len(degs) != 1:
        raise ValueError("the curves of a family must have one degree")
    p = degs.pop()
    K = merge_knots([c[0] for c in curves])
    return p, K, [refine(c[0], p, c[1], K)[1] for c in curves]


def _interpolate_across(params, rows, deg):
    """Interpolate the l-th entries of the rows at params, for every l.

    rows[i] is a list of points; the result R has R[k][l], k over the new basis.
    All entries share one matrix, so the rows are flattened and solved at once.
    """
    d = len(rows[0][0])
    flat = [tuple(x for pt in r for x in pt) for r in rows]
    knots, sol = interpolate(params, flat, deg)
    return knots, [[tuple(s[l * d:(l + 1) * d]) for l in range(len(rows[0]))] for s in sol]


def gordon_parts(u_curves, v_curves, us, vs, tol=0):
    """The three surfaces S1, S2 and T, each as (U, V, p, q, P)."""
    if len(v_curves) != len(us) or len(u_curves) != len(vs):
        raise ValueError("one parameter per curve")
    q, Vc, F = _common(v_curves)  # @line L1
    p, Uc, G = _common(u_curves)  # @line L2
    if len(us) < p + 1 or len(vs) < q + 1:
        raise ValueError("need at least p + 1 v-curves and q + 1 u-curves")
    if (us[0], us[-1]) != (Uc[0], Uc[-1]) or (vs[0], vs[-1]) != (Vc[0], Vc[-1]):
        raise ValueError("the outer curves of each family must lie on the domain boundary")
    pts = [[curve_point(Vc, q, F[i], v) for v in vs] for i in range(len(us))]  # @line L3
    for i, u in enumerate(us):
        for j in range(len(vs)):
            g = curve_point(Uc, p, G[j], u)
            if max(abs(a - b) for a, b in zip(pts[i][j], g)) > tol:  # @line L3
                raise ValueError("the network is not compatible at curve pair (%d, %d)" % (i, j))
    U1, P1 = _interpolate_across(us, F, p)  # @line L4
    V2, Q = _interpolate_across(vs, G, q)  # @line L5
    P2 = [[Q[l][k] for l in range(len(Q))] for k in range(len(Q[0]))]
    _, R = _interpolate_across(us, pts, p)  # @line L6
    RT = [[R[k][j] for k in range(len(R))] for j in range(len(vs))]
    _, X = _interpolate_across(vs, RT, q)  # @line L6
    P3 = [[X[l][k] for l in range(len(X))] for k in range(len(X[0]))]
    return (U1, Vc, p, q, P1), (Uc, V2, p, q, P2), (U1, V2, p, q, P3)


def gordon_surface(u_curves, v_curves, us, vs, tol=0):
    """The Gordon surface as one B-spline surface (U, V, p, q, P)."""
    S1, S2, T = gordon_parts(u_curves, v_curves, us, vs, tol)
    p, q = S1[2], S1[3]
    U = merge_knots([S1[0], S2[0]])  # @line L7
    V = merge_knots([S1[1], S2[1]])  # @line L7
    A, B, C = (refine_surface(S[0], S[1], p, q, S[4], U, V) for S in (S1, S2, T))  # @line L7
    P = [[sub(add(A[k][l], B[k][l]), C[k][l]) for l in range(len(A[0]))]  # @line L8
         for k in range(len(A))]
    return U, V, p, q, P  # @line L8
