# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radam/. The authors are listed in prov/KMW02T.jsonl.

"""RAdam, rectified Adam (Liu et al. 2020), Algorithm 2 of the paper.

rho_t is the length of the simple moving average that has the same center
of mass as Adam's bias-corrected exponential average of squared gradients.
While rho_t <= threshold (4 in the paper, 5 in the official code) the step
is bias-corrected momentum SGD; after that it is the Adam step times the
rectification term r_t.
"""

import math


def rho_inf(beta2):
    """Limit of rho_t as t grows: 2 / (1 - beta2) - 1."""
    return 2 / (1 - beta2) - 1


def rho(beta2, t):
    """rho_t = rho_inf - 2 t beta2^t / (1 - beta2^t). Exact for Fractions."""
    b = beta2 ** t
    return rho_inf(beta2) - 2 * t * b / (1 - b)


def sma_length_from_center_of_mass(beta2, t):
    """Length f of the simple moving average over steps t-f+1..t whose center
    of mass t - (f - 1)/2 equals that of the bias-corrected EMA, whose step i
    has weight (1 - beta2) beta2^(t-i) / (1 - beta2^t). Computed by summing."""
    total = sum((1 - beta2) * beta2 ** (t - i) * i for i in range(1, t + 1))
    com = total / (1 - beta2 ** t)
    return 2 * (t - com) + 1


def rectification(beta2, t):
    """r_t = sqrt((rho_t - 4)(rho_t - 2) rho_inf / ((rho_inf - 4)(rho_inf - 2) rho_t)).
    Defined for rho_t > 4 and rho_inf > 4."""
    ri, rt = rho_inf(beta2), rho(beta2, t)
    return math.sqrt((rt - 4) * (rt - 2) * ri / ((ri - 4) * (ri - 2) * rt))


def first_rectified_step(beta2, threshold=4):
    """Smallest t with rho_t > threshold, or None if rho_inf <= threshold."""
    if rho_inf(beta2) <= threshold:
        return None
    t = 1
    while rho(beta2, t) <= threshold:
        t += 1
    return t


def radam(grad, x, steps, lr=1e-3, beta1=0.9, beta2=0.999, eps=0.0, threshold=4):
    """Run RAdam. grad(x, t) is the minibatch gradient at x for step t.
    Returns the iterates x_0, ..., x_steps and the branch taken at each step
    ("sgdm" or "adaptive")."""
    d = len(x)
    m = [0.0] * d  # @line L1
    v = [0.0] * d
    r_inf = rho_inf(beta2)  # @line L2
    path, branch = [list(x)], []
    for t in range(1, steps + 1):  # @line L3
        g = grad(x, t)  # @line L4
        for i in range(d):
            v[i] = beta2 * v[i] + (1 - beta2) * g[i] * g[i]  # @line L5
            m[i] = beta1 * m[i] + (1 - beta1) * g[i]  # @line L6
        m_hat = [mi / (1 - beta1 ** t) for mi in m]  # @line L7
        r_t_len = r_inf - 2 * t * beta2 ** t / (1 - beta2 ** t)  # @line L8
        if r_t_len > threshold:  # @line L9
            # l_t = sqrt(1 - beta2^t) / (sqrt(v_t) + eps); a zero v means g was always 0.
            l_t = [math.sqrt(1 - beta2 ** t) / (math.sqrt(v[i]) + eps) if v[i] + eps > 0 else 0.0
                   for i in range(d)]  # @line L10
            r_t = math.sqrt((r_t_len - 4) * (r_t_len - 2) * r_inf
                            / ((r_inf - 4) * (r_inf - 2) * r_t_len))  # @line L11
            x = [x[i] - lr * r_t * m_hat[i] * l_t[i] for i in range(d)]  # @line L12
            branch.append("adaptive")
        else:
            x = [x[i] - lr * m_hat[i] for i in range(d)]  # @line L13
            branch.append("sgdm")
        path.append(x)
    return path, branch  # @line L14
