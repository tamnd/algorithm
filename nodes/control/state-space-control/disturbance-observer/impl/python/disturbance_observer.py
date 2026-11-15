# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disturbance-observer/. The authors are listed in prov/1HYDAN.jsonl.

"""Disturbance observer (DOB) for a single-input single-output plant.

The plant is y = P(s) (u + d) with an unknown input disturbance d. The
nominal model is P_n(s) = N(s) / D(s), strictly proper, with a stable
numerator N (minimum phase). The observer estimates d by

    d_hat = Q(s) (P_n(s)^(-1) y - u) = (D(s) y - N(s) u) / (N(s) (tau s + 1)^k),

with the low-pass filter Q(s) = 1 / (tau s + 1)^k. Q P_n^(-1) is proper
when k is at least the relative degree r = deg D - deg N. The control
u = u_c - d_hat cancels the low-frequency part of d. If P = P_n, then
d_hat = Q d exactly.

dob_filter returns a state-space realization (Af, Bf, Cf, Df) of the
two-input filter [y, u] -> d_hat in observable canonical form. Since
k >= 1, there is no direct feedthrough from u, so u = u_c - d_hat has no
algebraic loop. There is a direct feedthrough from y when k = r.
"""

from fractions import Fraction

from ctlmat import matvec, polymul

__all__ = ["dob_filter", "filter_rhs", "filter_output", "compensate", "q_filter", "is_hurwitz"]


def _strip(p):
    i = 0
    while i < len(p) - 1 and p[i] == 0:
        i += 1
    return list(p[i:])


def is_hurwitz(p):
    """Return True if every root of the real polynomial p has negative real part.

    Routh test: all coefficients must have one sign, and every entry of the
    first column of the Routh array must have that sign. A zero entry means a
    root on or to the right of the imaginary axis. Exact with int and Fraction
    coefficients.
    """
    p = _strip(p)
    if p[0] == 0:
        raise ValueError("zero polynomial")
    exact = all(isinstance(v, (int, Fraction)) for v in p)
    p = [Fraction(v) if exact else v for v in p]
    if p[0] < 0:
        p = [-v for v in p]
    if any(v <= 0 for v in p):
        return False
    r0, r1 = p[0::2], p[1::2]
    while r1:
        if r1[0] <= 0:
            return False
        f = r0[0] / r1[0]
        new = [r0[i + 1] - f * (r1[i + 1] if i + 1 < len(r1) else 0) for i in range(len(r0) - 1)]
        r0, r1 = r1, new
    return True


def q_filter(tau, k):
    """Return the denominator (tau s + 1)^k of Q(s) as a coefficient list."""
    p = [1]
    for _ in range(k):
        p = polymul(p, [tau, 1])
    return p


def dob_filter(num, den, tau, k):
    """Return (Af, Bf, Cf, Df) of d_hat = (D y - N u) / (N (tau s + 1)^k).

    num and den are N and D, highest power first. Inputs of the filter are
    [y, u]; the output is d_hat. Raises ValueError if tau <= 0, if k is
    less than the relative degree or less than 1, or if N has a root with
    real part >= 0.
    """
    N, D = _strip(num), _strip(den)
    if tau <= 0:
        raise ValueError("tau must be positive")
    r = (len(D) - 1) - (len(N) - 1)
    if r < 1:
        raise ValueError("the nominal plant must be strictly proper")
    if k < r or k < 1:  # @line L1
        raise ValueError("k must be at least the relative degree, or Q P_n^(-1) is not proper")
    if not is_hurwitz(N):
        raise ValueError("N(s) must be stable: P_n^(-1) would be unstable")
    a = polymul(N, q_filter(tau, k))  # @line L2
    n = len(a) - 1
    lead = a[0]
    exact = all(isinstance(v, (int, Fraction)) for v in a + D + N)
    div = (lambda v: Fraction(v) / Fraction(lead)) if exact else (lambda v: v / lead)
    a = [div(v) for v in a]
    by = [0] * (n + 1 - len(D)) + [div(v) for v in D]  # @line L3
    bu = [0] * (n + 1 - len(N)) + [-div(v) for v in N]
    Af = [[-a[i + 1] if j == 0 else (1 if j == i + 1 else 0) for j in range(n)] for i in range(n)]  # @line L4
    Bf, Df = [], []
    cols = []
    for b in (by, bu):
        d0 = b[0]  # coefficient of s^n: the direct feedthrough
        cols.append([b[i + 1] - d0 * a[i + 1] for i in range(n)])
        Df.append(d0)
    Bf = [[cols[0][i], cols[1][i]] for i in range(n)]
    Cf = [1] + [0] * (n - 1)
    return Af, Bf, Cf, Df  # @line L5


def filter_rhs(Af, Bf):
    """Return f(t, xf, (y, u)) = Af xf + Bf [y, u]."""
    def f(t, xf, yu):
        y, u = yu
        return [a + b0 * y + b1 * u for a, (b0, b1) in zip(matvec(Af, xf), Bf)]  # @line L6
    return f


def filter_output(Cf, Df, xf, y, u):
    """Return d_hat = Cf xf + Df [y, u]."""
    return sum(c * x for c, x in zip(Cf, xf)) + Df[0] * y + Df[1] * u  # @line L7


def compensate(u_c, d_hat):
    """Return the plant input u = u_c - d_hat."""
    return u_c - d_hat  # @line L8
