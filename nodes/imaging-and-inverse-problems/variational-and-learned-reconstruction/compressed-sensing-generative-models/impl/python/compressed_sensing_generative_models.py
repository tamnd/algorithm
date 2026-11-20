# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compressed-sensing-generative-models/. The authors are listed in prov/ZV36YT.jsonl.
"""Compressed sensing with a generative model (CSGM) of Bora, Jalal, Price and Dimakis.

The generator is given: a function gen(z) from R^k to R^n and a function
gen_vjp(z, v) that returns J_G(z)^T v. The method minimizes
loss(z) = ||A G(z) - y||^2 + lam ||z||^2 by gradient steps from several
starting codes and returns G(z) for the code with the lowest loss.
Matrices are lists of rows; vectors are lists of floats.
"""

import math


def matvec(a, x):
    """The product A x."""
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def rmatvec(a, r):
    """The product A^T r."""
    return [sum(a[i][j] * r[i] for i in range(len(a))) for j in range(len(a[0]))]


def loss(a, y, gen, z, lam):
    """||A G(z) - y||^2 + lam ||z||^2."""
    r = [p - q for p, q in zip(matvec(a, gen(z)), y)]
    return sum(v * v for v in r) + lam * sum(v * v for v in z)


def loss_grad(a, y, gen, gen_vjp, z, lam):
    """The gradient 2 J_G(z)^T A^T (A G(z) - y) + 2 lam z."""
    r = [p - q for p, q in zip(matvec(a, gen(z)), y)]
    g = gen_vjp(z, rmatvec(a, r))
    return [2.0 * gi + 2.0 * lam * zi for gi, zi in zip(g, z)]


def csgm(a, y, gen, gen_vjp, starts, step, iters, lam=0.0):
    """Run iters gradient steps from each start code and keep the best.

    Returns (x_hat, z_hat, loss). Each gradient step calls gen once,
    gen_vjp once, A once and A^T once.
    """
    best_z, best_loss = None, math.inf  # @line L1
    for z0 in starts:  # @line L2
        z = list(z0)  # @line L3
        for _ in range(iters):  # @line L4
            g = loss_grad(a, y, gen, gen_vjp, z, lam)  # @line L5
            z = [zi - step * gi for zi, gi in zip(z, g)]  # @line L6
        val = loss(a, y, gen, z, lam)
        if val < best_loss:  # @line L7
            best_z, best_loss = z, val  # @line L7
    return gen(best_z), best_z, best_loss  # @line L8


def tanh_generator(w, b):
    """The generator G(z) = tanh(W z + b) and its vector-Jacobian product.

    J_G(z)^T v = W^T (v * (1 - tanh(W z + b)^2)), entry by entry.
    """
    def gen(z):
        return [math.tanh(s + bi) for s, bi in zip(matvec(w, z), b)]

    def gen_vjp(z, v):
        out = gen(z)
        return rmatvec(w, [vi * (1.0 - oi * oi) for vi, oi in zip(v, out)])

    return gen, gen_vjp


def gaussian_matrix(rng, m, n):
    """A with independent N(0, 1/m) entries, the design of the CSGM theorems."""
    s = 1.0 / math.sqrt(m)
    return [[rng.gauss(0.0, s) for _ in range(n)] for _ in range(m)]
