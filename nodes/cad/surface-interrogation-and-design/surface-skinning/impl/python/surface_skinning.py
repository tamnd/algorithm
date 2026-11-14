# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-skinning/. The authors are listed in prov/5J15FM.jsonl.

"""Skinning (lofting) a B-spline surface through section curves.

The sections C_0(u), ..., C_K(u) are B-spline curves of one degree p. The
method of Piegl and Tiller, Section 10.3, makes them compatible by merging
their knot vectors and inserting the missing knots into each, so that all
sections have control points on one basis. It chooses a parameter v_k for
each section, by averaging the chord length parameters of the columns of
control points, and averaged knots in v. Then it interpolates each column of
control points across the sections with degree q. The surface S has
S(u, v_k) = C_k(u) for every k, exactly.

With int or Fraction control points and given parameters every step is
exact. The default parameters use square roots in floating point; they are
then turned into exact fractions, so the rest stays exact. The caller raises
the sections to one degree first.
"""

from fractions import Fraction
from math import dist

from si3spline import check_curve, interpolate, merge_knots, refine


def chord_parameters(rows):
    """Average over the columns of the chord length parameters, from 0 to 1.

    rows[k] is the list of control points of section k. A column whose points
    all coincide carries no information and is skipped.
    """
    K = len(rows) - 1
    total = [0.0] * (K + 1)
    used = 0
    for i in range(len(rows[0])):
        d = [dist(map(float, rows[k][i]), map(float, rows[k + 1][i])) for k in range(K)]
        s = sum(d)
        if s == 0:
            continue
        used += 1
        acc = 0.0
        for k in range(1, K):
            acc += d[k - 1]
            total[k] += acc / s
    if used == 0:
        raise ValueError("all sections are the same curve")
    vs = [Fraction(0)] + [Fraction(total[k] / used) for k in range(1, K)] + [Fraction(1)]
    return vs


def surface_skinning(sections, q=3, vs=None):
    """Skin the sections; return (U, V, p, q, P) with P[i][l], i along u.

    sections is a list of (knots, control points). q is the degree in v; it is
    lowered to the number of sections minus one if needed. vs, if given, are
    the parameters of the sections; otherwise they are chord length averages.
    """
    if len(sections) < 2:
        raise ValueError("need at least two sections")
    degs = set()
    for knots, ctrl in sections:
        p = len(knots) - len(ctrl) - 1
        check_curve(knots, p, ctrl)
        degs.add(p)
    if len(degs) != 1:
        raise ValueError("the sections must have one degree")
    p = degs.pop()
    U = merge_knots([kn for kn, _ in sections])  # @line L1
    rows = [refine(kn, p, ctrl, U)[1] for kn, ctrl in sections]  # @line L1
    if vs is None:
        vs = chord_parameters(rows)  # @line L2
    if len(vs) != len(sections):
        raise ValueError("one parameter per section")
    q = min(q, len(sections) - 1)
    d = len(rows[0][0])
    flat = [tuple(x for pt in r for x in pt) for r in rows]
    V, sol = interpolate(vs, flat, q)  # @line L3
    # sol[l] holds the l-th control point of every column; P[i][l] is column i, row l
    P = [[tuple(sol[l][i * d:(i + 1) * d]) for l in range(len(sol))]  # @line L4
         for i in range(len(rows[0]))]
    return U, V, p, q, P  # @line L5
