# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chambolle-projection-algorithm/. The authors are listed in prov/R2YTGF.jsonl.
"""Chambolle's projection algorithm for total variation denoising.

The model is min_u (1/2) ||u - f||^2 + lam * TV(u) on an n1 x n2 image f
(a list of rows), with the isotropic discrete total variation of forward
differences and a Neumann border (the last difference in each direction is 0).
The minimizer is u = f - P(f), where P is the projection onto the set
lam * K, K = {div p : |p_ij| <= 1 at every pixel}. The algorithm computes the
dual field p by Chambolle's semi-implicit fixed point step.
"""

import math

Image = list[list[float]]
Field = tuple[Image, Image]


def zeros(n1: int, n2: int) -> Image:
    return [[0.0] * n2 for _ in range(n1)]


def grad(u: Image) -> Field:
    """Forward differences with a Neumann border. Cost O(n1 n2)."""
    n1, n2 = len(u), len(u[0])
    g1, g2 = zeros(n1, n2), zeros(n1, n2)
    for i in range(n1):
        for j in range(n2):
            if i < n1 - 1:
                g1[i][j] = u[i + 1][j] - u[i][j]
            if j < n2 - 1:
                g2[i][j] = u[i][j + 1] - u[i][j]
    return g1, g2


def div(p: Field) -> Image:
    """The divergence, defined as minus the adjoint of grad. Cost O(n1 n2)."""
    p1, p2 = p
    n1, n2 = len(p1), len(p1[0])
    d = zeros(n1, n2)
    for i in range(n1):
        for j in range(n2):
            a = (p1[i][j] if i < n1 - 1 else 0.0) - (p1[i - 1][j] if i > 0 else 0.0)
            b = (p2[i][j] if j < n2 - 1 else 0.0) - (p2[i][j - 1] if j > 0 else 0.0)
            d[i][j] = a + b
    return d


def total_variation(u: Image) -> float:
    g1, g2 = grad(u)
    return sum(math.hypot(a, b) for r1, r2 in zip(g1, g2) for a, b in zip(r1, r2))


def energy(u: Image, f: Image, lam: float) -> float:
    """The primal energy (1/2)||u - f||^2 + lam TV(u)."""
    fit = sum((a - b) ** 2 for ru, rf in zip(u, f) for a, b in zip(ru, rf))
    return 0.5 * fit + lam * total_variation(u)


def dual_energy(p: Field, f: Image, lam: float) -> float:
    """D(p) = (1/2)(||f||^2 - ||f - lam div p||^2), a lower bound of the energy for |p| <= 1."""
    d = div(p)
    ff = sum(a * a for r in f for a in r)
    rr = sum((a - lam * b) ** 2 for rf, rd in zip(f, d) for a, b in zip(rf, rd))
    return 0.5 * (ff - rr)


def chambolle_projection(f: Image, lam: float, tau: float = 0.125, iters: int = 200,
                         tol: float | None = None, p0: Field | None = None) -> tuple[Image, Field]:
    """Return (u, p): the TV denoised image and the dual field.

    Precondition: lam > 0 and 0 < tau <= 1/8 for the proved convergence
    (tau = 1/4 often works in practice but has no proof for this step).
    With tol set, stop when the duality gap E(u) - D(p) is at most tol;
    then ||u - u*||^2 <= 2 tol. Cost O(n1 n2) per iteration, O(n1 n2) space.
    """
    n1, n2 = len(f), len(f[0])
    p1, p2 = (zeros(n1, n2), zeros(n1, n2)) if p0 is None else ([r[:] for r in p0[0]], [r[:] for r in p0[1]])  # @line L1
    for k in range(iters):  # @line L2
        d = div((p1, p2))
        v = [[d[i][j] - f[i][j] / lam for j in range(n2)] for i in range(n1)]  # @line L3
        z1, z2 = grad(v)  # @line L4
        for i in range(n1):
            for j in range(n2):
                s = 1.0 + tau * math.hypot(z1[i][j], z2[i][j])  # @line L5
                p1[i][j] = (p1[i][j] + tau * z1[i][j]) / s
                p2[i][j] = (p2[i][j] + tau * z2[i][j]) / s
        if tol is not None and (k + 1) % 10 == 0:
            u = _primal(f, lam, (p1, p2))
            if energy(u, f, lam) - dual_energy((p1, p2), f, lam) <= tol:
                break
    return _primal(f, lam, (p1, p2)), (p1, p2)


def _primal(f: Image, lam: float, p: Field) -> Image:
    d = div(p)
    w = [[lam * a for a in r] for r in d]  # @line L6
    return [[f[i][j] - w[i][j] for j in range(len(f[0]))] for i in range(len(f))]  # @line L7


def dual_residual(f: Image, lam: float, p: Field) -> float:
    """||div p - f/lam||^2, the dual objective that the iteration decreases."""
    d = div(p)
    return sum((a - b / lam) ** 2 for rd, rf in zip(d, f) for a, b in zip(rd, rf))


def chambolle_step(f: Image, lam: float, tau: float, p: Field) -> Field:
    """One step of lines L3 to L5, returned as a new field (for tests of monotonicity)."""
    _, q = chambolle_projection(f, lam, tau, iters=1, p0=p)
    return q
