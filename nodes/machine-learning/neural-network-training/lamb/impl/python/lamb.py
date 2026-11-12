# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamb/. The authors are listed in prov/CJHJQ5.jsonl.

"""LAMB (You et al. 2020), Algorithm 2 of the paper.

Adam's moments and normalized direction r = m_hat / (sqrt(v_hat) + eps),
plus decoupled weight decay, then a per layer trust ratio: each layer i
moves by exactly lr_t * phi(||x_i||) along the unit vector of r_i + lambda x_i.
A model is a list of layers; a layer is a list of floats.
"""

import math


def norm(x):
    return math.sqrt(sum(a * a for a in x))


def clip_phi(lo=0.0, hi=math.inf):
    """phi(z) = min(max(z, lo), hi), the scaling function of the paper."""
    return lambda z: min(max(z, lo), hi)


def linear_decay(lr, total):
    """eta_t = lr (1 - (t - 1) / total) for t = 1..total, the schedule used for BERT."""
    return lambda t: lr * (1 - (t - 1) / total)


def lamb(grad, layers, steps, lr=1e-3, beta1=0.9, beta2=0.999, eps=1e-6, weight_decay=0.01,
         phi=lambda z: z, bias_correction=True):
    """Run LAMB. grad(layers, t) returns one gradient per layer; lr is a number
    or a function of t. Returns the list of models x_1, ..., x_{T+1}."""
    m = [[0.0] * len(x) for x in layers]  # @line L1
    v = [[0.0] * len(x) for x in layers]
    path = [[list(x) for x in layers]]
    for t in range(1, steps + 1):  # @line L2
        grads = grad(layers, t)  # @line L3
        eta = lr(t) if callable(lr) else lr
        c1 = 1 - beta1 ** t if bias_correction else 1.0
        c2 = 1 - beta2 ** t if bias_correction else 1.0
        new_layers = []
        for i, (x, g) in enumerate(zip(layers, grads)):  # @line L4
            m[i] = [beta1 * a + (1 - beta1) * b for a, b in zip(m[i], g)]  # @line L5
            v[i] = [beta2 * a + (1 - beta2) * b * b for a, b in zip(v[i], g)]  # @line L6
            r = [(a / c1) / (math.sqrt(b / c2) + eps) if b > 0 or eps > 0 else 0.0
                 for a, b in zip(m[i], v[i])]  # @line L7
            u = [ri + weight_decay * xi for ri, xi in zip(r, x)]  # @line L8
            un, scale = norm(u), phi(norm(x))
            # Trust ratio phi(||x||) / ||u||; ratio 1 when either norm is zero.
            ratio = scale / un if un > 0 and scale > 0 else 1.0  # @line L9
            new_layers.append([xi - eta * ratio * ui for xi, ui in zip(x, u)])  # @line L10
        layers = new_layers
        path.append([list(x) for x in layers])
    return path  # @line L11
