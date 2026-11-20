# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constant-modulus-algorithm/. The authors are listed in prov/BYWJFM.jsonl.

"""The constant modulus algorithm (CMA 2-2, the Godard algorithm with p = 2).

The equalizer is an FIR filter c of N taps with output
z[k] = sum_i c[i] y[k-i]. CMA adapts c by a stochastic gradient step on the
cost J(c) = E(|z[k]|^2 - R2)^2, with the dispersion constant
R2 = E|a|^4 / E|a|^2 of the symbol alphabet. It uses no training symbols.

For the analysis, g = c * h is the combined response of the channel h and the
equalizer. For independent circular symbols with E a^2 = 0, E|a|^2 = 1 and
E|a|^4 = kappa, and no noise, the cost is
J(g) = 2 s^2 + (kappa - 2) sum |g_k|^4 - 2 kappa s + kappa^2, s = sum |g_k|^2.
"""

import cmath

import cbb


def dispersion_constant(points: list[complex]) -> float:
    """R2 = E|a|^4 / E|a|^2 for equally likely points."""
    m2 = sum(abs(p) ** 2 for p in points)
    m4 = sum(abs(p) ** 4 for p in points)
    if m2 == 0:
        raise ValueError("all points are zero")
    return m4 / m2


def cma(y: list[complex], n: int, mu: float, r2: float, spike: int | None = None) -> tuple[list[complex], list[complex]]:
    """Run CMA over the samples y. Returns the final taps c and the outputs z[k] for k = N-1, ..., len(y)-1."""
    if n < 1 or mu <= 0 or r2 <= 0:
        raise ValueError("need N >= 1, mu > 0 and R2 > 0")
    if spike is None:
        spike = n // 2
    c = [0j] * n  # @line L1
    c[spike] = 1 + 0j  # @line L1
    out = []
    for k in range(n - 1, len(y)):  # @line L2
        u = [y[k - i] for i in range(n)]  # @line L3
        z = sum(ci * ui for ci, ui in zip(c, u))  # @line L4
        e = z * (abs(z) ** 2 - r2)  # @line L5
        c = [ci - mu * e * ui.conjugate() for ci, ui in zip(c, u)]  # @line L6
        out.append(z)
    return c, out  # @line L7


def cma_cost(g: list[complex], kappa: float) -> float:
    """The exact noiseless CMA cost E(|z|^2 - R2)^2 of a combined response g, with R2 = kappa."""
    s = sum(abs(v) ** 2 for v in g)
    s4 = sum(abs(v) ** 4 for v in g)
    return 2 * s * s + (kappa - 2) * s4 - 2 * kappa * s + kappa * kappa


def cma_cost_gradient(c: list[complex], h: list[complex], kappa: float) -> list[complex]:
    """The gradient dJ/d conj(c) of the noiseless cost at the taps c, for the channel h."""
    g = cbb.conv(c, h)
    s = sum(abs(v) ** 2 for v in g)
    dg = [4 * s * v + 2 * (kappa - 2) * abs(v) ** 2 * v - 2 * kappa * v for v in g]
    return [sum(dg[i + l] * complex(h[l]).conjugate() for l in range(len(h))) for i in range(len(c))]


def mean_cma(c: list[complex], h: list[complex], kappa: float, mu: float, steps: int) -> list[complex]:
    """Deterministic gradient descent on the noiseless cost: the mean behavior of CMA for a small step."""
    for _ in range(steps):
        grad = cma_cost_gradient(c, h, kappa)
        c = [ci - mu * gi for ci, gi in zip(c, grad)]
    return c


def residual_isi(g: list[complex]) -> float:
    """(sum |g|^2 - max |g|^2) / max |g|^2: 0 for a single tap."""
    p = [abs(v) ** 2 for v in g]
    m = max(p)
    return (sum(p) - m) / m


def phase_of_cursor(g: list[complex]) -> tuple[int, complex]:
    """The index of the largest tap of g and its unit-modulus phase: the delay and the rotation CMA leaves."""
    d = max(range(len(g)), key=lambda i: abs(g[i]))
    return d, cmath.exp(1j * cmath.phase(g[d]))
