# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learned-primal-dual/. The authors are listed in prov/8N7P4C.jsonl.
"""Learned primal-dual reconstruction (Adler and Oktem 2018, Algorithm 3).

The update maps are given functions. The primal state is a list of N_p
vectors in R^n and the dual state a list of N_d vectors in R^m. In step i:

    h <- dual_maps[i](h, A x[1], y)        (a list of N_d vectors)
    x <- primal_maps[i](x, A^T h[0])       (a list of N_p vectors)

and the result is x[0]. The forward operator is linear here, so the adjoint
of its derivative is A^T. The functions cp_maps and gradient_maps build the
update maps for which the scheme is Chambolle-Pock or gradient descent.
With N_p = 1 the forward operator is applied to x[0].
"""

import math


def learned_primal_dual(y, apply_a, apply_at, dual_maps, primal_maps, x0, h0):
    """Run len(dual_maps) steps of the learned primal-dual scheme.

    x0 is a list of N_p primal vectors and h0 a list of N_d dual vectors.
    Each step calls apply_a once, apply_at once and each map once.
    Returns the first primal component.
    """
    x = [list(v) for v in x0]  # @line L1
    h = [list(v) for v in h0]  # @line L1
    for gamma, lam in zip(dual_maps, primal_maps):  # @line L2
        h = gamma(h, apply_a(x[1] if len(x) > 1 else x[0]), y)  # @line L3
        x = lam(x, apply_at(h[0]))  # @line L4
    return x[0]  # @line L5


def cp_maps(prox_tau_g, prox_sigma_fstar, tau, sigma, theta=1.0):
    """The pair (Gamma, Lambda) for which one step is one Chambolle-Pock step.

    N_p = 2 (x and the extrapolated point x_bar) and N_d = 1.
    prox_sigma_fstar(v, y) must return prox_{sigma F_y*}(v), and
    prox_tau_g(v) must return prox_{tau G}(v).
    """
    def gamma(h, a_xbar, y):
        return [prox_sigma_fstar([a + sigma * b for a, b in zip(h[0], a_xbar)], y)]

    def lam(x, at_h):
        new = prox_tau_g([a - tau * b for a, b in zip(x[0], at_h)])
        xbar = [(1.0 + theta) * a - theta * b for a, b in zip(new, x[0])]
        return [new, xbar]

    return gamma, lam


def gradient_maps(step):
    """The pair (Gamma, Lambda) for which one step is a gradient step on (1/2)||A x - y||^2.

    N_p = 1 and N_d = 1: the dual state is the residual A x - y, and the
    primal map is x - step * A^T h. This is Landweber iteration.
    """
    def gamma(h, a_x, y):
        return [[a - b for a, b in zip(a_x, y)]]

    def lam(x, at_h):
        return [[a - step * b for a, b in zip(x[0], at_h)]]

    return gamma, lam


def least_squares_dual_prox(sigma):
    """prox_{sigma F_y*} for F_y(z) = (1/2)||z - y||^2, that is (v - sigma y) / (1 + sigma)."""
    def prox(v, y):
        return [(a - sigma * b) / (1.0 + sigma) for a, b in zip(v, y)]
    return prox


def l1_prox(weight):
    """prox of weight * ||x||_1: soft thresholding at weight."""
    def prox(v):
        return [a - weight if a > weight else a + weight if a < -weight else 0.0 for a in v]
    return prox


def residual_network(rng, n_in, n_out, width, scale):
    """A small given network: v -> v[:n_out] + W2 tanh(W1 v + b1), with seeded weights.

    It stands in for a trained update map in tests; it is not trained.
    """
    w1 = [[rng.gauss(0.0, scale) for _ in range(n_in)] for _ in range(width)]
    b1 = [rng.gauss(0.0, scale) for _ in range(width)]
    w2 = [[rng.gauss(0.0, scale) for _ in range(width)] for _ in range(n_out)]

    def net(v):
        hidden = [math.tanh(sum(w * t for w, t in zip(row, v)) + b) for row, b in zip(w1, b1)]
        return [v[i] + sum(w * t for w, t in zip(row, hidden)) for i, row in enumerate(w2)]
    return net
