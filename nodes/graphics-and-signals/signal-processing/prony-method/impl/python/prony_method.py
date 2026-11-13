# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prony-method/. The authors are listed in prov/ATNC9Z.jsonl.

"""Prony's method: fit x[n] = sum over j of h[j] z[j]^n to equally spaced samples.

The three steps are a linear prediction system for the characteristic
polynomial, its roots, and a Vandermonde least-squares fit of the amplitudes.
A root z = rho e^(iw) is a damped complex sinusoid with damping rho per sample
and frequency w in radians per sample.
"""

from typing import Sequence


def _conj(v):
    return v.conjugate() if isinstance(v, complex) else v


def _abs(v):
    return abs(v)


def solve(a: list[list], b: list) -> list:
    """Solve the square system a y = b by Gaussian elimination with partial pivoting.

    Works for Fraction (exact) and complex (floating point) entries.
    Raises ValueError for a singular matrix. Cost: O(p^3).
    """
    n = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: _abs(m[r][col]))
        if m[piv][col] == 0:
            raise ValueError("singular system")
        m[col], m[piv] = m[piv], m[col]
        for r in range(col + 1, n):
            factor = m[r][col] / m[col][col]
            if factor != 0:
                for c in range(col, n + 1):
                    m[r][c] -= factor * m[col][c]
    y = [0] * n
    for r in range(n - 1, -1, -1):
        s = m[r][n] - sum(m[r][c] * y[c] for c in range(r + 1, n))
        y[r] = s / m[r][r]
    return y


def least_squares(rows: list[list], rhs: list) -> list:
    """Minimize sum of |row . y - rhs|^2 through the normal equations A^H A y = A^H rhs."""
    p = len(rows[0])
    if len(rows) == p:
        return solve(rows, rhs)
    gram = [[sum(_conj(r[i]) * r[j] for r in rows) for j in range(p)] for i in range(p)]
    proj = [sum(_conj(r[i]) * v for r, v in zip(rows, rhs)) for i in range(p)]
    return solve(gram, proj)


def prediction_polynomial(x: Sequence, p: int) -> list:
    """Return c = (1, c[1], ..., c[p]) with x[n] + sum of c[i] x[n - i] = 0 for n = p .. N - 1,
    solved exactly when N = 2p and in the least-squares sense when N > 2p."""
    n = len(x)
    if p < 1 or n < 2 * p:
        raise ValueError("need p >= 1 and N >= 2p")
    rows = [[x[t - i] for i in range(1, p + 1)] for t in range(p, n)]  # @line L1
    rhs = [-x[t] for t in range(p, n)]
    c = least_squares(rows, rhs)  # @line L2
    return [1] + c


def polynomial_roots(c: Sequence[complex], iterations: int = 500) -> list[complex]:
    """Roots of z^p + c[1] z^(p-1) + ... + c[p] by Durand-Kerner (Weierstrass) iteration."""
    p = len(c) - 1
    coeffs = [complex(v) for v in c]
    bound = 1 + max(abs(v) for v in coeffs[1:]) if p else 1
    z = [bound * (0.4 + 0.9j) ** i for i in range(p)]
    for _ in range(iterations):
        delta = 0.0
        new = []
        for i in range(p):
            val = 0j
            for v in coeffs:
                val = val * z[i] + v
            den = 1 + 0j
            for j in range(p):
                if j != i:
                    den *= z[i] - z[j]
            step = val / den if den != 0 else 0
            new.append(z[i] - step)
            delta = max(delta, abs(step))
        z = new
        if delta < 1e-15 * bound:
            break
    return z


def prony(x: Sequence[complex], p: int) -> tuple[list[complex], list[complex]]:
    """Return (z, h) with x[n] ~ sum over j of h[j] z[j]^n.

    Precondition: N >= 2p and the p roots are distinct and nonzero.
    Cost: O(N p^2 + p^3) for the two least-squares systems, plus the root finder.
    """
    c = prediction_polynomial([complex(v) for v in x], p)
    z = polynomial_roots(c)  # @line L3
    rows = [[zj ** t for zj in z] for t in range(len(x))]  # @line L4
    h = least_squares(rows, [complex(v) for v in x])
    return z, h  # @line L5


def evaluate(z: Sequence[complex], h: Sequence[complex], n: int) -> list[complex]:
    """The model samples sum over j of h[j] z[j]^t for t = 0 .. n - 1."""
    return [sum(hj * zj ** t for hj, zj in zip(h, z)) for t in range(n)]
