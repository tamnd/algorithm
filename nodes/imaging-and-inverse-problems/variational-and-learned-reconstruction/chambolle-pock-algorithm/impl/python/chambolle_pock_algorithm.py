# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chambolle-pock-algorithm/. The authors are listed in prov/JY6DNX.jsonl.
"""The primal-dual algorithm of Chambolle and Pock.

It solves min_x F(K x) + G(x) through the saddle point problem
min_x max_y <K x, y> + G(x) - F*(y). The caller gives K and its adjoint as
functions on flat lists of floats, and the two proximal maps
prox_{tau G} and prox_{sigma F*}. Two problems are built in: total variation
denoising (ROF) on an image and the LASSO.
"""

import math
from typing import Callable

Vec = list[float]
LinOp = Callable[[Vec], Vec]
Prox = Callable[[Vec, float], Vec]


def chambolle_pock(K: LinOp, KT: LinOp, prox_g: Prox, prox_fstar: Prox, x0: Vec, y0: Vec,
                   tau: float, sigma: float, iters: int,
                   theta: float = 1.0) -> tuple[Vec, Vec, Vec, Vec]:
    """Run iters steps and return (x, y, X, Y): the last iterates and the ergodic averages.

    prox_g(v, tau) must return prox_{tau G}(v) and prox_fstar(v, sigma) must
    return prox_{sigma F*}(v). Precondition: F and G closed proper convex,
    a saddle point exists, and tau * sigma * ||K||^2 < 1 (theta = 1).
    Cost: iters * (one K, one KT, two prox calls) plus O(n + m) per step.
    """
    x = x0[:]  # @line L1
    y = y0[:]
    xbar = x0[:]
    sx, sy = [0.0] * len(x), [0.0] * len(y)
    for _ in range(iters):  # @line L2
        kx = K(xbar)
        y = prox_fstar([a + sigma * b for a, b in zip(y, kx)], sigma)  # @line L3
        x_old = x  # @line L4
        kty = KT(y)
        x = prox_g([a - tau * b for a, b in zip(x, kty)], tau)  # @line L5
        xbar = [a + theta * (a - b) for a, b in zip(x, x_old)]  # @line L6
        sx = [a + b for a, b in zip(sx, x)]  # @line L7
        sy = [a + b for a, b in zip(sy, y)]
    n = max(iters, 1)
    return x, y, [a / n for a in sx], [a / n for a in sy]  # @line L8


def chambolle_pock_accelerated(K: LinOp, KT: LinOp, prox_g: Prox, prox_fstar: Prox, x0: Vec, y0: Vec,
                               tau: float, sigma: float, gamma: float, iters: int) -> tuple[Vec, Vec]:
    """Algorithm 2 of Chambolle and Pock for G that is gamma-strongly convex.

    The steps change as theta = 1 / sqrt(1 + 2 gamma tau), tau <- theta tau,
    sigma <- sigma / theta. Precondition: tau * sigma * ||K||^2 <= 1.
    Then ||x^N - x*|| = O(1/N). Cost as above.
    """
    x, y, xbar = x0[:], y0[:], x0[:]
    for _ in range(iters):
        kx = K(xbar)
        y = prox_fstar([a + sigma * b for a, b in zip(y, kx)], sigma)
        x_old = x
        kty = KT(y)
        x = prox_g([a - tau * b for a, b in zip(x, kty)], tau)
        theta = 1.0 / math.sqrt(1.0 + 2.0 * gamma * tau)
        tau, sigma = theta * tau, sigma / theta
        xbar = [a + theta * (a - b) for a, b in zip(x, x_old)]
    return x, y


# ---- Total variation denoising: G(x) = (1/2)||x - f||^2, F(q) = lam sum |q_ij|, K = grad.

def grad_op(n1: int, n2: int) -> LinOp:
    """Forward differences with a Neumann border, image in row major order; output (d1, d2) stacked."""
    def K(u: Vec) -> Vec:
        out = [0.0] * (2 * n1 * n2)
        for i in range(n1):
            for j in range(n2):
                k = i * n2 + j
                if i < n1 - 1:
                    out[k] = u[k + n2] - u[k]
                if j < n2 - 1:
                    out[n1 * n2 + k] = u[k + 1] - u[k]
        return out
    return K


def grad_adjoint(n1: int, n2: int) -> LinOp:
    """The adjoint of grad_op, which is minus the divergence."""
    N = n1 * n2

    def KT(q: Vec) -> Vec:
        out = [0.0] * N
        for i in range(n1):
            for j in range(n2):
                k = i * n2 + j
                if i < n1 - 1:
                    out[k] -= q[k]
                    out[k + n2] += q[k]
                if j < n2 - 1:
                    out[k] -= q[N + k]
                    out[k + 1] += q[N + k]
        return out
    return KT


def project_balls(lam: float, N: int) -> Prox:
    """prox of sigma F* for F = lam * isotropic TV: project each pixel pair onto the ball of radius lam."""
    def prox(v: Vec, sigma: float) -> Vec:
        out = v[:]
        for k in range(N):
            r = math.hypot(v[k], v[N + k])
            if r > lam:
                out[k] = v[k] * lam / r
                out[N + k] = v[N + k] * lam / r
        return out
    return prox


def rof_energy(u: Vec, f: Vec, lam: float, n1: int, n2: int) -> float:
    g = grad_op(n1, n2)(u)
    N = n1 * n2
    return 0.5 * sum((a - b) ** 2 for a, b in zip(u, f)) + lam * sum(math.hypot(g[k], g[N + k]) for k in range(N))


def rof_denoise(f: list[list[float]], lam: float, tau: float = 0.35, sigma: float = 0.35,
                iters: int = 500) -> list[list[float]]:
    """TV denoising of an image (list of rows). Needs tau * sigma * 8 < 1. Cost O(iters * pixels)."""
    n1, n2 = len(f), len(f[0])
    N = n1 * n2
    fl = [a for row in f for a in row]
    x, _, _, _ = chambolle_pock(grad_op(n1, n2), grad_adjoint(n1, n2),
                                lambda v, t: [(a + t * b) / (1 + t) for a, b in zip(v, fl)],
                                project_balls(lam, N), fl, [0.0] * (2 * N), tau, sigma, iters)
    return [x[i * n2:(i + 1) * n2] for i in range(n1)]


# ---- LASSO: G(x) = lam ||x||_1, F(z) = (1/2)||z - b||^2, K = A.

def soft(v: Vec, t: float) -> Vec:
    return [math.copysign(max(abs(a) - t, 0.0), a) for a in v]


def lasso(A: list[list[float]], b: Vec, lam: float, iters: int = 2000) -> Vec:
    """min (1/2)||A x - b||^2 + lam ||x||_1 with tau = sigma = 0.99 / ||A||_F."""
    m, n = len(A), len(A[0])
    L = math.sqrt(sum(a * a for row in A for a in row))  # ||A|| <= ||A||_F
    t = 0.99 / L
    K = lambda x: [sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]
    KT = lambda y: [sum(A[i][j] * y[i] for i in range(m)) for j in range(n)]
    x, _, _, _ = chambolle_pock(K, KT, lambda v, s: soft(v, s * lam),
                                lambda v, s: [(a - s * c) / (1 + s) for a, c in zip(v, b)],
                                [0.0] * n, [0.0] * m, t, t, iters)
    return x
