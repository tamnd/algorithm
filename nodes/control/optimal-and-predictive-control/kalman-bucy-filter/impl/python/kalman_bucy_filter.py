# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kalman-bucy-filter/. The authors are listed in prov/HYX6WP.jsonl.

"""The Kalman-Bucy filter: the continuous-time Kalman filter.

Plant: dx = (A x + B u) dt + dw, dz = C x dt + dv, where z is the integrated
measurement (y = dz/dt in the white noise notation) and w, v are independent
Wiener processes with intensities W >= 0 and V > 0.

The filter is

    dxhat = (A xhat + B u) dt + L_o (dz - C xhat dt),  L_o = S C^T V^-1,
    S' = A S + S A^T + W - S C^T V^-1 C S,             S(0) = S_0.

The class KalmanBucy advances the filter over steps of length h: xhat by one
Euler-Maruyama step driven by the measurement increment dz of the step, S by
one RK4 step of the Riccati differential equation (ctlsim.rk4_step).
steady_state integrates the Riccati equation until it stops changing, which
gives the stabilizing solution of the filter algebraic Riccati equation when
(C, A) is detectable and (A, W^(1/2)) is stabilizable.
"""

from ctlmat import add, inv, matvec, mul, sub, transpose
from ctlsim import rk4_step

__all__ = ["riccati_rhs", "gain", "KalmanBucy", "steady_state"]


def _flat(S):
    return [v for row in S for v in row]


def _mat(s, n):
    return [[s[i * n + j] for j in range(n)] for i in range(n)]


def _sym(S):
    n = len(S)
    return [[(S[i][j] + S[j][i]) / 2 for j in range(n)] for i in range(n)]


def riccati_rhs(A, C, W, V):
    """Return f(t, s, u) for the flattened Riccati equation S' = A S + S A^T + W - S C^T V^-1 C S."""
    n = len(A)
    M = mul(mul(transpose(C), inv(V)), C)
    At = transpose(A)

    def f(t, s, u):
        S = _mat(s, n)
        dS = add(add(mul(A, S), mul(S, At)), sub(W, mul(mul(S, M), S)))
        return _flat(dS)
    return f


def gain(S, C, V):
    """Return the filter gain L_o = S C^T V^-1."""
    return mul(mul(S, transpose(C)), inv(V))


class KalmanBucy:
    """Kalman-Bucy filter advanced in steps of length h."""

    def __init__(self, A, B, C, W, V, xhat0, S0):
        self.A, self.B, self.C, self.V = A, B, C, V
        self.n = len(A)
        self.f = riccati_rhs(A, C, W, V)
        self.xhat = list(xhat0)  # @line L1
        self.S = _sym(S0)
        self.t = 0.0

    def step(self, u, dz, h):
        """Advance by h with input u (flat list) and measurement increment dz = integral of y over the step."""
        A, B, C = self.A, self.B, self.C
        Lo = gain(self.S, C, self.V)  # @line L3
        x = self.xhat
        drift = matvec(A, x)
        if B is not None and u is not None:
            drift = [d + b for d, b in zip(drift, matvec(B, u))]
        innov = [dzi - h * cx for dzi, cx in zip(dz, matvec(C, x))]
        corr = matvec(Lo, innov)
        self.xhat = [xi + h * di + ci for xi, di, ci in zip(x, drift, corr)]  # @line L4
        s = rk4_step(self.f, self.t, _flat(self.S), None, h)  # @line L5
        self.S = _sym(_mat(s, self.n))
        self.t += h
        return self.xhat, self.S  # @line L6

    def run(self, inputs, increments, h):
        """Run over the lists of inputs and measurement increments; return the list of (xhat, S)."""
        out = []
        for u, dz in zip(inputs, increments):  # @line L2
            xh, S = self.step(u, dz, h)
            out.append((list(xh), [row[:] for row in S]))
        return out


def riccati_solution(A, C, W, V, S0, t1, h):
    """Return S(t1) of the Riccati differential equation from S(0) = S0, RK4 with step h."""
    f = riccati_rhs(A, C, W, V)
    n = len(A)
    steps = round(t1 / h)
    if abs(steps * h - t1) > 1e-9 * max(t1, h):
        raise ValueError("t1 is not an integer multiple of h")
    s = _flat(S0)
    for k in range(steps):
        s = rk4_step(f, k * h, s, None, h)
    return _sym(_mat(s, n))


def steady_state(A, C, W, V, S0=None, h=0.01, tol=1e-12, max_steps=1000000):
    """Integrate the Riccati equation until |S'| <= tol; return (S, L_o)."""
    n = len(A)
    f = riccati_rhs(A, C, W, V)
    s = _flat(S0 if S0 is not None else [[0.0] * n for _ in range(n)])  # @line L7
    for k in range(max_steps):  # @line L8
        if max(abs(v) for v in f(0.0, s, None)) <= tol:
            S = _sym(_mat(s, n))
            return S, gain(S, C, V)  # @line L9
        s = rk4_step(f, k * h, s, None, h)
    raise ArithmeticError("the Riccati equation did not settle; check detectability and stabilizability")
