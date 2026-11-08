# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/classical-runge-kutta-4/. The authors are listed in prov/349F36.jsonl.

"""The classical fourth-order Runge-Kutta method (RK4) for y' = f(t, y), y(t0) = y0.

Butcher tableau:

    0   |
    1/2 | 1/2
    1/2 | 0    1/2
    1   | 0    0    1
    ----+-------------------
        | 1/6  1/3  1/3  1/6

y0 may be a float (then f takes and returns floats) or a list of floats (then f takes
and returns lists). Each step costs four evaluations of f.
"""

from fractions import Fraction
from typing import Callable, List, Sequence, Tuple, Union

State = Union[float, Sequence[float]]

# The tableau with exact rational entries, for checking order conditions.
A = [
    [Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
    [Fraction(1, 2), Fraction(0), Fraction(0), Fraction(0)],
    [Fraction(0), Fraction(1, 2), Fraction(0), Fraction(0)],
    [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
]
B = [Fraction(1, 6), Fraction(1, 3), Fraction(1, 3), Fraction(1, 6)]
C = [Fraction(0), Fraction(1, 2), Fraction(1, 2), Fraction(1)]


def stability_function(z: complex) -> complex:
    """R(z) = 1 + z + z^2/2 + z^3/6 + z^4/24, the factor of one step on y' = lambda y, z = h lambda."""
    return 1 + z * (1 + z * (Fraction(1, 2) + z * (Fraction(1, 6) + z / 24)))


def _axpy(y: List[float], a: float, x: List[float]) -> List[float]:
    return [yi + a * xi for yi, xi in zip(y, x)]


def rk4_step(f: Callable[[float, List[float]], List[float]], t: float, y: List[float], h: float) -> List[float]:
    """One RK4 step of size h from (t, y), for a vector y given as a list."""
    k1 = f(t, y)  # @line L4
    k2 = f(t + h / 2, _axpy(y, h / 2, k1))  # @line L5
    k3 = f(t + h / 2, _axpy(y, h / 2, k2))  # @line L6
    k4 = f(t + h, _axpy(y, h, k3))  # @line L7
    return [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(y))]  # @line L8


def rk4(f: Callable, t0: float, y0: State, t_end: float, h: float) -> Tuple[List[float], list]:
    """Integrate from t0 to t_end >= t0 with step h > 0; the last step is shortened to end at t_end.

    Returns (ts, ys). For a scalar y0 the entries of ys are floats.
    """
    if h <= 0.0:
        raise ValueError("h must be positive")
    if t_end < t0:
        raise ValueError("t_end must be at least t0")
    scalar = isinstance(y0, (int, float))
    fv = (lambda t, y: [f(t, y[0])]) if scalar else f
    y = [float(y0)] if scalar else [float(v) for v in y0]
    ts, ys = [t0], [y[0] if scalar else list(y)]  # @line L1
    t, n = t0, 0
    while t < t_end:  # @line L2
        n += 1
        t_next = t0 + n * h  # @line L3: the grid point, computed from t0 so that it does not drift
        if t_next > t_end or t_end - t_next <= 1e-12 * max(1.0, abs(t_end - t0)):
            t_next = t_end
        y = rk4_step(fv, t, y, t_next - t)
        t = t_next  # @line L9
        ts.append(t)
        ys.append(y[0] if scalar else list(y))
    return ts, ys
