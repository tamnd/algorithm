# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pid-controller/. The authors are listed in prov/M0FN5Q.jsonl.

"""A sampled PID controller with a derivative filter, set-point weights,
output limits and anti-windup by back-calculation.

The continuous controller, in the ideal (standard) form, is

    U(s) = K (b R - Y) + K/(T_i s) (R - Y) + K T_d s/(1 + s T_d/N) (c R - Y).

The sampled version follows Astrom and Hagglund (2006), Section 13.3:
- the integral term uses the forward difference;
- the filtered derivative uses the backward difference, which gives a
  filter pole a_d = T_d/(T_d + N h) in [0, 1) for every h > 0;
- the integral state also takes a correction (h/T_t)(u - v), where v is
  the computed output and u the output after the limits.

The class works in exact arithmetic when every parameter and signal is an
int or a Fraction and there are no limits (or the limits are exact).
Use Ti = None for no integral action and Td = 0 for no derivative action,
and Tt = None for no anti-windup.
"""

import cmath
import math

__all__ = [
    "PID", "ideal_to_parallel", "parallel_to_ideal", "series_to_ideal",
    "ideal_to_series", "pid_frequency_response",
]


class PID:
    """Sampled PID controller (pseudocode lines L1 to L9)."""

    def __init__(self, K, Ti=None, Td=0, N=10, h=1, b=1, c=0,
                 Tt=None, umin=None, umax=None):
        if h <= 0:
            raise ValueError("the sampling period h must be positive")
        if Ti is not None and Ti <= 0:
            raise ValueError("Ti must be positive or None")
        if Td < 0 or N <= 0:
            raise ValueError("Td must be at least 0 and N positive")
        if Tt is not None and Tt <= 0:
            raise ValueError("Tt must be positive or None")
        if umin is not None and umax is not None and umin > umax:
            raise ValueError("umin is above umax")
        self.K, self.b, self.c = K, b, c
        self.umin, self.umax = umin, umax
        self.bi = 0 if Ti is None else K * h / Ti  # @line L1
        self.ar = 0 if Tt is None else h / Tt
        if Td == 0:
            self.ad, self.bd = 0, 0
        else:
            self.ad = Td / (Td + N * h)
            self.bd = K * Td * N / (Td + N * h)
        self.I = 0
        self.D = 0
        self.ed_old = None

    def _limit(self, v):
        if self.umax is not None and v > self.umax:
            return self.umax
        if self.umin is not None and v < self.umin:
            return self.umin
        return v

    def step(self, r, y, uff=0):
        """Return the output u for the set point r and the measurement y.

        uff is an optional feedforward term added before the limits.
        At the first call the derivative has no past value, so it starts
        at 0 (no derivative kick at start up).
        """
        ed = self.c * r - y  # @line L2
        if self.ed_old is None:
            self.ed_old = ed
        P = self.K * (self.b * r - y)  # @line L3
        self.D = self.ad * self.D + self.bd * (ed - self.ed_old)  # @line L4
        v = P + self.I + self.D + uff  # @line L5
        u = self._limit(v)  # @line L6
        self.I = self.I + self.bi * (r - y) + self.ar * (u - v)  # @line L7
        self.ed_old = ed  # @line L8
        return u  # @line L9

    def reset(self, I=0, D=0):
        """Set the integral and derivative states (for bumpless transfer)."""
        self.I, self.D, self.ed_old = I, D, None


def ideal_to_parallel(K, Ti, Td):
    """Return (kp, ki, kd) with kp + ki/s + kd s = K (1 + 1/(Ti s) + Td s)."""
    return K, K / Ti, K * Td


def parallel_to_ideal(kp, ki, kd):
    """Inverse of ideal_to_parallel; needs kp > 0 and ki > 0."""
    if kp <= 0 or ki <= 0:
        raise ValueError("the ideal form needs kp > 0 and ki > 0")
    return kp, kp / ki, kd / kp


def series_to_ideal(Ks, Tis, Tds):
    """Return (K, Ti, Td) with K (1 + 1/(Ti s) + Td s) equal to
    Ks (1 + 1/(Tis s)) (1 + Tds s)."""
    return Ks * (Tis + Tds) / Tis, Tis + Tds, Tis * Tds / (Tis + Tds)


def ideal_to_series(K, Ti, Td):
    """Return the series form of an ideal PID.

    It exists if and only if Ti >= 4 Td, because the zeros of the ideal
    form are real only then. The result is in floating point (a square
    root).
    """
    if Ti < 4 * Td:
        raise ValueError("no series form: the zeros are complex (Ti < 4 Td)")
    q = math.sqrt(1 - 4 * Td / Ti)
    return K * (1 + q) / 2, Ti * (1 + q) / 2, Ti * (1 - q) / 2


def pid_frequency_response(K, Ti, Td, N, omega, b=1, c=1):
    """Return C(j omega) of the continuous controller from e = r - y.

    N = None gives the ideal derivative K Td s. b and c weight the set
    point; C is the transfer function from the error when b = c = 1.
    """
    s = 1j * omega
    ci = 0 if Ti is None else 1 / (Ti * s)
    if Td == 0:
        cd = 0
    elif N is None:
        cd = Td * s
    else:
        cd = Td * s / (1 + s * Td / N)
    return complex(K * (1 + ci + cd))


def _self_test():
    k, ti, td = ideal_to_series(*series_to_ideal(2.0, 4.0, 1.0))
    assert abs(k - 2.0) < 1e-12 and abs(ti - 4.0) < 1e-12 and abs(td - 1.0) < 1e-12
    c = pid_frequency_response(1.0, 1.0, 0.0, None, 1.0)
    assert abs(c - (1 - 1j)) < 1e-15 and abs(cmath.phase(c) + math.pi / 4) < 1e-15
    return True


if __name__ == "__main__":
    _self_test()
