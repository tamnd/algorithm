# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cage-based-deformation/. The authors are listed in prov/K9W6TX.jsonl.
"""Cage-based deformation in 2D with mean value coordinates (Floater 2003).

A cage is a closed polygon c_0..c_{n-1}. Each point p of the shape gets
weights w_i(p) once, at bind time. When the cage vertices move to c'_i,
the point moves to p' = sum_i w_i(p) c'_i. The weights here are the mean
value coordinates

    w_i = (tan(a_{i-1} / 2) + tan(a_i / 2)) / r_i,   normalized to sum 1,

where r_i = |c_i - p| and a_i is the signed angle at p from c_i to c_{i+1}.
The half-angle tangent is computed as cross / (r_i r_{i+1} + dot), which
stays finite when p is on the line of an edge but not on the edge.
"""

import math


def mean_value_coordinates(p, cage, eps=1e-14):
    """Return the n mean value coordinates of p with respect to the cage."""
    n = len(cage)
    d = [(c[0] - p[0], c[1] - p[1]) for c in cage]
    r = [math.hypot(*v) for v in d]
    for i in range(n):
        if r[i] <= eps:
            return [1.0 if k == i else 0.0 for k in range(n)]
    tan_half = []
    for i in range(n):
        j = (i + 1) % n
        cr = d[i][0] * d[j][1] - d[i][1] * d[j][0]
        dt = d[i][0] * d[j][0] + d[i][1] * d[j][1]
        den = r[i] * r[j] + dt
        if den <= eps * r[i] * r[j]:
            # p lies on edge i: interpolate linearly along the edge.
            s = r[i] / (r[i] + r[j])
            out = [0.0] * n
            out[i], out[j] = 1 - s, s
            return out
        tan_half.append(cr / den)
    w = [(tan_half[i - 1] + tan_half[i]) / r[i] for i in range(n)]
    total = sum(w)
    return [x / total for x in w]


class Binding:
    """Bind a set of points to a cage once, then deform them for any new cage."""

    def __init__(self, points, cage):
        self.cage = [tuple(map(float, c)) for c in cage]
        self.weights = [mean_value_coordinates(p, self.cage) for p in points]  # @line L1

    def deform(self, new_cage):
        out = []
        for w in self.weights:  # @line L2
            x = sum(wi * c[0] for wi, c in zip(w, new_cage))  # @line L3
            y = sum(wi * c[1] for wi, c in zip(w, new_cage))
            out.append((x, y))
        return out  # @line L4
