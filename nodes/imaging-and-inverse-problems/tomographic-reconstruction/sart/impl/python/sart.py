# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sart/. The authors are listed in prov/9QD7WM.jsonl.
"""SART, the simultaneous algebraic reconstruction technique.

The system matrix A is given as sparse rows: row i is a list of (column,
weight) pairs with nonnegative weights, as returned by
imgkit.parallel_beam_matrix. The rays are grouped into views: views[v] is the
list of the row indices of view v. For one view v, the update is

    x <- x + lam * C_v A_v^T R_v (y_v - A_v x),

with R_v = diag(1 / r_i) over the rays i of the view and C_v = diag(1 / c_vj),
c_vj the sum of column j over the rays of the view. A pixel with c_vj = 0 is
not changed by view v, and a ray with r_i = 0 is skipped. One sweep applies
the update once for each view, in the given order. The code works with float
or with fractions.Fraction data.
"""


def views_by_angle(nangles, nbins):
    """The views of imgkit.parallel_beam_matrix: angle a holds the rows a * nbins + b."""
    return [list(range(a * nbins, (a + 1) * nbins)) for a in range(nangles)]


def view_sums(rows, views):
    """The row sums r_i, and for each view a dict j -> c_vj of its column sums."""
    r = [sum(w for _, w in row) for row in rows]
    cs = []
    for view in views:
        c = {}
        for i in view:
            for j, w in rows[i]:
                c[j] = c.get(j, 0) + w
        cs.append(c)
    return r, cs


def sart(rows, ncols, y, views, lam=1.0, sweeps=10, x0=None, order=None, nonneg=False, callback=None):
    """Run SART and return x after the given number of sweeps.

    rows: the sparse rows of A; y: the data; views: the row indices of each
    view; lam: the relaxation, 0 < lam < 2; x0: the start (zero by default);
    order: the order of the views in a sweep (0, 1, 2, ... by default);
    nonneg: clip to x >= 0 after each view; callback(k, x) is called after
    sweep k.
    """
    r = [sum(w for _, w in row) for row in rows]  # @line L1
    x = list(x0) if x0 is not None else [0 * lam] * ncols  # @line L2
    seq = list(order) if order is not None else list(range(len(views)))
    for k in range(sweeps):  # @line L3
        for v in seq:  # @line L4
            g, c = {}, {}
            for i in views[v]:
                if r[i] == 0:
                    continue
                e = (y[i] - sum(w * x[j] for j, w in rows[i])) / r[i]  # @line L5
                for j, w in rows[i]:
                    g[j] = g.get(j, 0) + w * e  # @line L6
                    c[j] = c.get(j, 0) + w
            for j, gj in g.items():
                if c[j] != 0:
                    x[j] = x[j] + lam * gj / c[j]  # @line L7
                if nonneg and x[j] < 0:
                    x[j] = 0 * x[j]  # @line L8
        if callback is not None:
            callback(k + 1, list(x))
    return x  # @line L9
