# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/density-filtering/. The authors are listed in prov/FZQT96.jsonl.

"""The density filter of topology optimization on a grid of unit elements.

Element (i, j) of an nx by ny grid has its center at (i + 1/2, j + 1/2) and
the number i ny + j. The cone weights are H_ef = max(0, rmin - dist(e, f)),
D_e = sum_f H_ef, and the filtered density is x~ = D^-1 H x. All elements
have the same volume, so the volume factors of the general formula cancel.
"""

import math


class DensityFilter:
    def __init__(self, nx, ny, rmin):
        """L1: the sparse rows of H within the radius, and the row sums D."""
        self.nx, self.ny, self.rmin = nx, ny, rmin
        reach = math.ceil(rmin)
        self.rows = []
        for i in range(nx):
            for j in range(ny):
                row = []
                for k in range(max(0, i - reach), min(nx, i + reach + 1)):
                    for m in range(max(0, j - reach), min(ny, j + reach + 1)):
                        w = rmin - math.hypot(i - k, j - m)
                        if w > 0:
                            row.append((k * ny + m, w))
                self.rows.append(row)
        self.d = [sum(w for _, w in row) for row in self.rows]

    def apply(self, x):
        """L3: x~_e = sum_f H_ef x_f / D_e."""
        return [sum(w * x[f] for f, w in row) / d for row, d in zip(self.rows, self.d)]

    def transpose(self, g):
        """L5: the chain rule, dc/dx_f = sum_e H_ef (dc/dx~_e) / D_e. H is
        symmetric, so row f of H lists the same pairs as column f."""
        scaled = [ge / d for ge, d in zip(g, self.d)]
        return [sum(w * scaled[e] for e, w in row) for row in self.rows]


def direct_matrix(nx, ny, rmin):
    """The dense filter matrix W = D^-1 H from all pairs of elements, O(n^2)."""
    centers = [(i + 0.5, j + 0.5) for i in range(nx) for j in range(ny)]
    h = [[max(0.0, rmin - math.dist(a, b)) for b in centers] for a in centers]
    return [[v / sum(row) for v in row] for row in h], [sum(row) for row in h]


def matvec(m, x):
    return [sum(a * b for a, b in zip(row, x)) for row in m]


def matvec_transpose(m, g):
    n = len(m)
    return [sum(m[e][f] * g[e] for e in range(n)) for f in range(n)]


def filtered_descent(flt, x, model, update, maxit=100, tol=1e-9):
    """The template with the filter in place: model(xt) returns (c, dc/dxt),
    update(x, dc/dx) returns the new design."""
    hist = []
    for _ in range(maxit):  # @line L2
        xt = flt.apply(x)  # @line L3
        c, gt = model(xt)  # @line L4
        hist.append(c)
        g = flt.transpose(gt)  # @line L5
        new = update(x, g)  # @line L6
        done = max(abs(a - b) for a, b in zip(new, x)) < tol
        x = new
        if done:  # @line L7
            break
    return flt.apply(x), hist  # @line L8


def build(nx, ny, rmin):
    return DensityFilter(nx, ny, rmin)  # @line L1
