# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-predictive-control/. The authors are listed in prov/J9ZFD5.jsonl.

"""Generalized predictive control (GPC) of Clarke, Mohtadi and Tuffs (1987).

Single input, single output. Polynomials are lists of coefficients in
increasing powers of the backward shift q^-1, so [1, -0.8] is 1 - 0.8 q^-1.
The plant model is the CARIMA model

    A(q^-1) y(t) = B(q^-1) u(t-1) + e(t) / Delta,   Delta = 1 - q^-1,

with A monic. A dead time of d samples is written as d leading zeros in B.
With At = Delta A, the Diophantine identity

    1 = E_j(q^-1) At(q^-1) + q^-j F_j(q^-1),   deg E_j = j - 1, deg F_j = deg A,

gives the j-step predictor yhat(t+j | t) = G_j du(t+j-1) + F_j y(t) with
G_j = E_j B. The first j coefficients of G_j are the step response
coefficients g_0, ..., g_(j-1) of B / A, so the predictions over j = N1..N2
are G du + f, where G holds the g_i and f (the free response) holds F_j y(t)
and the terms of G_j that multiply past moves. The control law minimizes

    sum_(j=N1)^N2 (w - yhat(t+j | t))^2 + lam sum_(i=0)^(Nu-1) du(t+i)^2,

which gives du = (G^T G + lam I)^-1 G^T (w - f); only the first move is used.

All arithmetic is generic: with int and Fraction data the Diophantine
polynomials and the RST polynomials are exact.
"""

__all__ = ["poly_mul", "diophantine", "GPC"]


def poly_mul(a, b):
    """Product of two polynomials in q^-1."""
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def diophantine(At, j):
    """Return (E_j, F_j) with 1 = E_j At + q^-j F_j, for a monic At.

    E_j is the first j terms of the series 1 / At (long division); F_j is
    the remainder divided by q^-j.
    """
    if At[0] != 1:
        raise ValueError("At must be monic")
    rem = [1] + [0] * (j + len(At) - 1)
    E = []
    for i in range(j):
        e = rem[i]
        E.append(e)
        for k, a in enumerate(At):
            rem[i + k] -= e * a
    F = rem[j:j + len(At) - 1]
    return E, F


def _solve(a, b):
    n = len(a)
    m = [list(r) + [v] for r, v in zip(a, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


class GPC:
    """Unconstrained GPC with the horizons N1..N2, the control horizon Nu and the move weight lam."""

    def __init__(self, A, B, N1, N2, Nu, lam):
        if A[0] != 1:
            raise ValueError("A must be monic")
        self.A, self.B = list(A), list(B)
        self.N1, self.N2, self.Nu, self.lam = N1, N2, Nu, lam
        self.At = poly_mul(A, [1, -1])  # @line L1
        self.E, self.F, self.Gj = {}, {}, {}
        for j in range(N1, N2 + 1):
            self.E[j], self.F[j] = diophantine(self.At, j)  # @line L2
            self.Gj[j] = poly_mul(self.E[j], self.B)  # @line L3
        g = self.Gj[N2][:N2]  # step response coefficients g_0..g_(N2-1)
        self.g = g
        self.G = [[g[j - 1 - l] if j - 1 - l >= 0 else 0 for l in range(Nu)] for j in range(N1, N2 + 1)]
        ny = N2 - N1 + 1
        GtG = [[sum(self.G[i][a] * self.G[i][b] for i in range(ny)) + (lam if a == b else 0) for b in range(Nu)]
               for a in range(Nu)]
        cols = [_solve(GtG, [self.G[i][a] for a in range(Nu)]) for i in range(ny)]
        self.K = [cols[i][0] for i in range(ny)]  # @line L4
        self.ys = [0] * len(self.F[N1])  # y(t), y(t-1), ..., y(t-deg A)
        self.nb = max(1, len(B) - 1)
        self.dus = [0] * (self.nb + 1)  # du(t-1), du(t-2), ..., one extra for predict()
        self.u = 0

    def free_response(self):
        """f_j for j = N1..N2 from the stored outputs and past moves."""
        f = []
        for j in range(self.N1, self.N2 + 1):
            fj = sum(c * y for c, y in zip(self.F[j], self.ys))
            fj += sum(self.Gj[j][i] * self.dus[i - j] for i in range(j, len(self.Gj[j])))
            f.append(fj)
        return f

    def step(self, y, w):
        """Return u(t) for the measured y(t) and the constant setpoint w."""
        self.ys = [y] + self.ys[:-1]
        f = self.free_response()  # @line L5
        du = sum(k * (w - fj) for k, fj in zip(self.K, f))  # @line L6
        self.dus = [du] + self.dus[:-1]
        self.u += du  # @line L7
        return self.u

    def predict(self, du_future):
        """yhat(t+j | t), j = N1..N2, for the future moves du(t..t+Nu-1), after step() at time t."""
        saved = self.dus
        self.dus = self.dus[1:]  # the moves before du(t), which is a decision variable here
        f = self.free_response()
        self.dus = saved
        return [fj + sum(self.G[i][l] * du_future[l] for l in range(self.Nu)) for i, fj in enumerate(f)]

    def rst(self):
        """Return (R, S, T) with R(q^-1) du(t) = T w - S(q^-1) y(t), the same law as step()."""
        js = list(range(self.N1, self.N2 + 1))
        R = [1] + [0] * self.nb
        for k, j in zip(self.K, js):
            for i in range(j, len(self.Gj[j])):
                R[1 + i - j] += k * self.Gj[j][i]
        S = [0] * len(self.F[self.N1])
        for k, j in zip(self.K, js):
            for i, c in enumerate(self.F[j]):
                S[i] += k * c
        return R, S, sum(self.K)

    def closed_loop_polynomial(self):
        """Return At R + q^-1 B S, the closed-loop characteristic polynomial in q^-1."""
        R, S, _ = self.rst()
        p1 = poly_mul(self.At, R)
        p2 = [0] + poly_mul(self.B, S)
        n = max(len(p1), len(p2))
        return [(p1[i] if i < len(p1) else 0) + (p2[i] if i < len(p2) else 0) for i in range(n)]
