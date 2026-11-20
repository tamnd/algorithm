# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sato-algorithm/. The authors are listed in prov/2220NN.jsonl.

"""The Sato blind equalizer for PAM, and its form for square QAM.

The equalizer is an FIR filter c of N taps with output
z[k] = sum_i c[i] y[k-i]. The Sato error is e = z - gamma sgn(z), with the
constant gamma = E a^2 / E|a| of the PAM alphabet. The update is the LMS step
c <- c - mu e conj(u). It is a stochastic gradient step on the cost
J(c) = E[z^2 / 2 - gamma |z|] for real signals.

For square QAM, the same rule runs on the real and the imaginary parts:
csgn(z) = sgn(Re z) + j sgn(Im z), and gamma = E[(Re a)^2] / E|Re a|.
For real PAM the imaginary parts are 0 and the two forms agree.
"""


def _sgn(v: float) -> float:
    return 1.0 if v > 0 else (-1.0 if v < 0 else 0.0)


def csgn(z: complex) -> complex:
    """sgn(Re z) + j sgn(Im z), with sgn(0) = 0."""
    z = complex(z)
    return complex(_sgn(z.real), _sgn(z.imag))


def sato_gamma(levels: list[float]) -> float:
    """gamma = E a^2 / E|a| for equally likely real levels (one axis of PAM or square QAM)."""
    m1 = sum(abs(v) for v in levels)
    if m1 == 0:
        raise ValueError("all levels are zero")
    return sum(v * v for v in levels) / m1


def sato(y: list[complex], n: int, mu: float, gamma: float, spike: int | None = None) -> tuple[list[complex], list[complex]]:
    """Run the Sato algorithm over y. Returns the final taps and the outputs z[k] for k = N-1, ..., len(y)-1."""
    if n < 1 or mu <= 0 or gamma <= 0:
        raise ValueError("need N >= 1, mu > 0 and gamma > 0")
    if spike is None:
        spike = n // 2
    c = [0j] * n  # @line L1
    c[spike] = 1 + 0j  # @line L1
    out = []
    for k in range(n - 1, len(y)):  # @line L2
        u = [complex(y[k - i]) for i in range(n)]  # @line L3
        z = sum(ci * ui for ci, ui in zip(c, u))  # @line L4
        e = z - gamma * csgn(z)  # @line L5
        c = [ci - mu * e * ui.conjugate() for ci, ui in zip(c, u)]  # @line L6
        out.append(z)
    return c, out  # @line L7
