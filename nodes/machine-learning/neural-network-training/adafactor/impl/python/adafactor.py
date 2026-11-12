# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adafactor/. The authors are listed in prov/39XP8M.jsonl.

"""Adafactor (Shazeer and Stern 2018), Algorithms 4 (matrix) and 5 (vector).

For an n x m weight matrix the second moment estimate is kept as a row
vector R (n numbers) and a column vector C (m numbers); the full estimate
is the rank one matrix V_hat = R C / (1^T R). Matrices are lists of rows.
"""

import math


def factor(v):
    """Row sums R, column sums C of a nonnegative matrix v."""
    r = [sum(row) for row in v]
    c = [sum(col) for col in zip(*v)]
    return r, c


def expand(r, c):
    """V_hat = R C / (1^T R), the rank one matrix with row sums R and column sums C."""
    s = sum(r)
    return [[ri * cj / s for cj in c] for ri in r]


def i_divergence(v, w):
    """Generalized Kullback-Leibler divergence sum v log(v/w) - v + w."""
    total = 0.0
    for vr, wr in zip(v, w):
        for a, b in zip(vr, wr):
            total += (a * math.log(a / b) if a > 0 else 0.0) - a + b
    return total


def rms(x):
    """Root mean square of a vector or matrix."""
    flat = [a for row in x for a in row] if x and isinstance(x[0], list) else list(x)
    return math.sqrt(sum(a * a for a in flat) / len(flat))


def decay_rate(t, power=0.8):
    """beta2_hat_t = 1 - t^(-0.8); it is 0 at t = 1, so no bias correction is needed."""
    return 1 - t ** (-power)


def relative_step(t):
    """rho_t = min(1e-2, 1 / sqrt(t))."""
    return min(1e-2, 1 / math.sqrt(t))


def new_state(x):
    """Factored state for a matrix (R, C), full state for a vector."""
    if isinstance(x[0], list):
        return {"r": [0.0] * len(x), "c": [0.0] * len(x[0])}
    return {"v": [0.0] * len(x)}


def state_size(state):
    return sum(len(a) for a in state.values())


def adafactor_matrix_step(x, g, state, t, eps1=1e-30, eps2=1e-3, d=1.0, step=None):
    """One step of Algorithm 4 on an n x m matrix x with gradient g, in place on state.
    Returns the new x."""
    alpha = max(eps2, rms(x)) * (relative_step(t) if step is None else step(t))  # @line L4
    b = decay_rate(t)
    sq = [[gij * gij + eps1 for gij in row] for row in g]
    rows, cols = factor(sq)
    state["r"] = [b * a + (1 - b) * s for a, s in zip(state["r"], rows)]  # @line L5
    state["c"] = [b * a + (1 - b) * s for a, s in zip(state["c"], cols)]  # @line L6
    v_hat = expand(state["r"], state["c"])  # @line L7
    u = [[gij / math.sqrt(vij) for gij, vij in zip(gr, vr)] for gr, vr in zip(g, v_hat)]  # @line L8
    scale = max(1.0, rms(u) / d)
    u_hat = [[a / scale for a in row] for row in u]  # @line L9
    return [[a - alpha * uij for a, uij in zip(xr, ur)] for xr, ur in zip(x, u_hat)]  # @line L10


def adafactor_vector_step(x, g, state, t, eps1=1e-30, eps2=1e-3, d=1.0, step=None):
    """One step of Algorithm 5 on a vector: an unfactored second moment."""
    alpha = max(eps2, rms(x)) * (relative_step(t) if step is None else step(t))
    b = decay_rate(t)
    state["v"] = [b * a + (1 - b) * (gi * gi + eps1) for a, gi in zip(state["v"], g)]
    u = [gi / math.sqrt(vi) for gi, vi in zip(g, state["v"])]
    scale = max(1.0, rms(u) / d)
    return [a - alpha * ui / scale for a, ui in zip(x, u)]


def adafactor(grad, params, steps, **kw):
    """Run Adafactor on a list of parameters (matrices or vectors).

    grad(params, t) returns the list of gradients. Returns the final params."""
    states = [new_state(p) for p in params]  # @line L1
    for t in range(1, steps + 1):  # @line L2
        grads = grad(params, t)  # @line L3
        params = [adafactor_matrix_step(p, g, s, t, **kw) if isinstance(p[0], list)
                  else adafactor_vector_step(p, g, s, t, **kw)
                  for p, g, s in zip(params, grads, states)]
    return params  # @line L11
