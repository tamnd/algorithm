# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/amsgrad/. The authors are listed in prov/VZ3Q5P.jsonl.

"""AMSGrad (Reddi, Kale and Kumar 2018) and Adam in the same framework.

Both follow Algorithm 2 of the paper: no bias correction, step size
alpha_t = alpha / sqrt(t), and an optional projection onto a box. The only
difference is line L6: AMSGrad divides by the running maximum of v.
"""

import math


def clip_box(lo, hi):
    """Projection onto the box [lo, hi]^d. In a box the projection in the
    norm weighted by sqrt(v_hat) is the same coordinatewise clipping."""
    return lambda x: [min(hi, max(lo, xi)) for xi in x]


def amsgrad(grad, x, steps, alpha=0.1, beta1=0.0, beta2=0.999, eps=0.0, project=None, use_max=True, decay_alpha=True):
    """Run AMSGrad (use_max=True) or Adam (use_max=False).

    grad(x, t) is the gradient of the loss f_t at x. Returns the iterates
    x_1, ..., x_{steps+1}.
    """
    d = len(x)
    m = [0.0] * d  # @line L1
    v = [0.0] * d
    v_hat = [0.0] * d
    path = [list(x)]
    for t in range(1, steps + 1):  # @line L2
        g = grad(x, t)  # @line L3
        a_t = alpha / math.sqrt(t) if decay_alpha else alpha
        new = []
        for i in range(d):
            m[i] = beta1 * m[i] + (1 - beta1) * g[i]  # @line L4
            v[i] = beta2 * v[i] + (1 - beta2) * g[i] * g[i]  # @line L5
            v_hat[i] = max(v_hat[i], v[i]) if use_max else v[i]  # @line L6
            denom = math.sqrt(v_hat[i]) + eps
            new.append(x[i] - a_t * m[i] / denom if denom > 0 else x[i])  # @line L7
        x = project(new) if project else new  # @line L8
        path.append(x)
    return path  # @line L9


def adam(grad, x, steps, **kw):
    """Adam without bias correction, as analysed by Reddi, Kale and Kumar."""
    return amsgrad(grad, x, steps, use_max=False, **kw)


def counterexample_grad(c):
    """The online problem of Theorem 1: f_t(x) = c x if t mod 3 = 1, else -x."""
    return lambda x, t: [float(c) if t % 3 == 1 else -1.0]


def counterexample_loss(c, x, t):
    return c * x if t % 3 == 1 else -x


def regret(c, path):
    """Regret of x_1, ..., x_T against the best fixed point x = -1 (c > 2)."""
    total = 0.0
    for t, x in enumerate(path[:-1], start=1):
        total += counterexample_loss(c, x[0], t) - counterexample_loss(c, -1.0, t)
    return total
