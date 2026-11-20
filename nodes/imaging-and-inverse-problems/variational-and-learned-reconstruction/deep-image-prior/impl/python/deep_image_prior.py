# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deep-image-prior/. The authors are listed in prov/E31RHQ.jsonl.
"""Deep image prior (DIP) of Ulyanov, Vedaldi and Lempitsky.

The generator is given: gen(theta) returns the image x = G_theta(z) for the
fixed input z, and gen_vjp(theta, v) returns the gradient of <v, G_theta(z)>
in the weights theta. DIP fits the weights to the data by gradient steps on
||A G_theta(z) - y||^2 and stops after a chosen number of steps.
Vectors and flat weight lists are lists of floats.
"""

import math


def dip(apply_a, apply_at, y, gen, gen_vjp, theta0, step, iters, on_step=None):
    """Run iters gradient steps on the weights. Return (x, theta, losses).

    on_step(k, x), if given, is called with the image after step k.
    Each step calls gen once, gen_vjp once, A once and A^T once.
    """
    theta = list(theta0)  # @line L1
    losses = []
    for k in range(1, iters + 1):  # @line L2
        x = gen(theta)  # @line L3
        r = [p - q for p, q in zip(apply_a(x), y)]  # @line L4
        losses.append(sum(v * v for v in r))
        g = gen_vjp(theta, [2.0 * v for v in apply_at(r)])  # @line L5
        theta = [t - step * gi for t, gi in zip(theta, g)]  # @line L6
        if on_step is not None:
            on_step(k, gen(theta))
    return gen(theta), theta, losses  # @line L7


def one_layer_generator(z, n, activation="tanh"):
    """G_W(z) = phi(W z) with W an n by q matrix stored row by row in theta.

    The gradient of <v, phi(W z)> in W is (v * phi'(W z)) z^T.
    """
    q = len(z)

    def pre(theta):
        return [sum(theta[i * q + j] * z[j] for j in range(q)) for i in range(n)]

    if activation == "tanh":
        def gen(theta):
            return [math.tanh(s) for s in pre(theta)]

        def slope(theta):
            return [1.0 - math.tanh(s) ** 2 for s in pre(theta)]
    else:
        def gen(theta):
            return pre(theta)

        def slope(theta):
            return [1.0] * n

    def gen_vjp(theta, v):
        d = [vi * si for vi, si in zip(v, slope(theta))]
        return [d[i] * z[j] for i in range(n) for j in range(q)]

    return gen, gen_vjp


def periodic_blur(kernel, n):
    """Return (apply_a, apply_at) for periodic convolution with a centered kernel."""
    half = len(kernel) // 2

    def apply_a(x):
        return [sum(kernel[k] * x[(i + k - half) % n] for k in range(len(kernel)))
                for i in range(n)]

    def apply_at(r):
        return [sum(kernel[k] * r[(j - k + half) % n] for k in range(len(kernel)))
                for j in range(n)]

    return apply_a, apply_at
