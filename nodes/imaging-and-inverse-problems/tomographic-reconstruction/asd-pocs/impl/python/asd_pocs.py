# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asd-pocs/. The authors are listed in prov/4RF9RF.jsonl.
"""ASD-POCS: adaptive steepest descent on total variation, alternated with
projections onto the data and positivity constraints (Sidky and Pan, 2008).

The image is a row-major vector of an n x n image. The system matrix A is
given as sparse rows of (column, weight) pairs, as returned by
imgkit.parallel_beam_matrix. The aim is a small total variation under the
constraints ||A x - y|| <= eps and x >= 0. The method is a heuristic: it has
no convergence proof.
"""

import math


def tv(x, n, eta=1e-8):
    """The smoothed isotropic total variation sum sqrt(dx^2 + dy^2 + eta^2).

    dx and dy are forward differences down the rows and along the columns,
    with a zero difference at the last row and the last column.
    """
    total = 0.0
    for i in range(n):
        for j in range(n):
            p = x[i * n + j]
            dx = x[(i + 1) * n + j] - p if i + 1 < n else 0.0
            dy = x[i * n + j + 1] - p if j + 1 < n else 0.0
            total += math.sqrt(dx * dx + dy * dy + eta * eta)
    return total


def tv_grad(x, n, eta=1e-8):
    """The exact gradient of tv(x, n, eta)."""
    g = [0.0] * (n * n)
    for i in range(n):
        for j in range(n):
            k = i * n + j
            p = x[k]
            dx = x[k + n] - p if i + 1 < n else 0.0
            dy = x[k + 1] - p if j + 1 < n else 0.0
            s = math.sqrt(dx * dx + dy * dy + eta * eta)
            if i + 1 < n:
                g[k + n] += dx / s
                g[k] -= dx / s
            if j + 1 < n:
                g[k + 1] += dy / s
                g[k] -= dy / s
    return g


def _norm(v):
    return math.sqrt(sum(t * t for t in v))


def residual_norm(rows, y, x):
    """||A x - y||."""
    return _norm([sum(w * x[j] for j, w in row) - yi for row, yi in zip(rows, y)])


def asd_pocs(rows, n, y, eps, iters=100, beta=1.0, beta_red=0.995, ng=20, alpha=0.2,
             alpha_red=0.95, r_max=0.95, eta=1e-8, callback=None):
    """Run ASD-POCS and return the image after the data and positivity steps
    of the last iteration.

    eps: the allowed data misfit ||A x - y||; beta, beta_red: the ART
    relaxation and its factor per iteration; ng: the number of TV steps per
    iteration (ng = 0 gives plain ART with positivity); alpha: the first TV
    step length as a fraction of the change made by the data steps; alpha_red
    and r_max: the adaptive rule for the TV step length. callback(k, x, dd)
    is called after the data steps of iteration k, with dd = ||A x - y||.
    """
    norms = [sum(w * w for _, w in row) for row in rows]
    x = [0.0] * (n * n)  # @line L1
    dtvg = None
    xres = x
    for k in range(iters):  # @line L2
        x0 = list(x)
        for row, yi, ai in zip(rows, y, norms):  # @line L3
            if ai > 0:
                t = beta * (yi - sum(w * x[j] for j, w in row)) / ai
                for j, w in row:
                    x[j] += t * w
        x = [t if t > 0 else 0.0 for t in x]  # @line L4
        xres = list(x)
        dd = residual_norm(rows, y, x)  # @line L5
        dp = _norm([a - b for a, b in zip(x, x0)])
        if dtvg is None:
            dtvg = alpha * dp
        if callback is not None:
            callback(k + 1, xres, dd)
        x1 = list(x)
        for _ in range(ng):  # @line L6
            g = tv_grad(x, n, eta)
            gn = _norm(g)
            if gn == 0.0:
                break
            x = [a - dtvg * b / gn for a, b in zip(x, g)]
        dg = _norm([a - b for a, b in zip(x, x1)])  # @line L7
        if dg > r_max * dp and dd > eps:
            dtvg *= alpha_red
        beta *= beta_red  # @line L8
    return xres  # @line L9
