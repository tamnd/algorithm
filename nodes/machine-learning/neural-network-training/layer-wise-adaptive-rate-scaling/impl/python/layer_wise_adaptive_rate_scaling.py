# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/layer-wise-adaptive-rate-scaling/. The authors are listed in prov/ZN48H9.jsonl.

"""LARS, layer-wise adaptive rate scaling (You, Gitman and Ginsburg 2017).

Each layer l gets the local learning rate
    lambda_l = eta * ||w_l|| / (||g_l|| + beta * ||w_l||)        (Eq. 6)
and the update of Algorithm 1 of the paper is momentum SGD with the global
rate gamma_t = gamma_0 (1 - t/T)^2 times lambda_l. Layers are lists of
floats; a model is a list of layers.
"""

import math


def norm(x):
    return math.sqrt(sum(a * a for a in x))


def poly_decay(base_lr, t, total, power=2):
    """gamma_t = gamma_0 (1 - t / T)^power."""
    return base_lr * (1 - t / total) ** power


def local_lr(w, g, eta, weight_decay):
    """The trust ratio of Eq. 6. A layer with zero weight norm or zero
    gradient gets ratio 1 instead, so it can still move."""
    wn, gn = norm(w), norm(g)
    denom = gn + weight_decay * wn
    if wn == 0 or denom == 0:
        return 1.0
    return eta * wn / denom


def lars(grad, layers, steps, base_lr=1.0, momentum=0.9, weight_decay=0.0, eta=0.001, power=2):
    """Algorithm 1 of the paper. grad(layers, t) returns one gradient per layer.
    Returns the list of models w_0, ..., w_T."""
    vel = [[0.0] * len(w) for w in layers]  # @line L1
    path = [[list(w) for w in layers]]
    for t in range(steps):  # @line L2
        grads = grad(layers, t)  # @line L3
        gamma = poly_decay(base_lr, t, steps, power)  # @line L4
        new_layers = []
        for l, (w, g) in enumerate(zip(layers, grads)):  # @line L5
            lam = local_lr(w, g, eta, weight_decay)  # @line L6
            vel[l] = [momentum * v + gamma * lam * (gi + weight_decay * wi)
                      for v, gi, wi in zip(vel[l], g, w)]  # @line L7
            new_layers.append([wi - v for wi, v in zip(w, vel[l])])  # @line L8
        layers = new_layers
        path.append([list(w) for w in layers])
    return path  # @line L9


def lars_lamb_form_step(w, g, m, lr, beta1=0.9, weight_decay=0.0, phi=lambda z: z):
    """One step of LARS as written in Algorithm 1 of You et al. (2020):
    m <- beta1 m + (1 - beta1)(g + lambda w), w <- w - lr phi(||w||) m / ||m||.
    Returns (new w, new m)."""
    m = [beta1 * a + (1 - beta1) * (gi + weight_decay * wi) for a, gi, wi in zip(m, g, w)]
    mn = norm(m)
    if mn == 0:
        return list(w), m
    scale = phi(norm(w))
    if scale == 0:
        scale = mn  # trust ratio 1 for a zero layer
    return [wi - lr * scale * a / mn for wi, a in zip(w, m)], m
