# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rosenbrock-methods/. The authors are listed in prov/B4P23E.jsonl.

"""Rosenbrock (Rosenbrock-Wanner, ROW) methods with fixed steps.

A method is given by the strictly lower triangular matrices alpha and gamma, the weights b and
the diagonal value g (HNW II, Section IV.7). One step solves s linear systems with the single
matrix I - h g J; no Newton iteration. The order conditions up to order 3 and the stability
function are exact when the coefficients are Fractions.
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Optional, Sequence, Tuple

GRID_SLACK = 1e-9
F = Fraction


@dataclass
class RosenbrockMethod:
    name: str
    alpha: List[List[Any]]  # strictly lower triangular
    gamma: List[List[Any]]  # strictly lower triangular part of Gamma
    b: List[Any]
    g: Any  # the diagonal gamma

    @property
    def stages(self) -> int:
        return len(self.b)

    def alpha_i(self, i: int) -> Any:
        return sum(self.alpha[i][:i], self.g * 0)

    def gamma_i(self, i: int) -> Any:
        return self.g + sum(self.gamma[i][:i], self.g * 0)

    def beta(self) -> List[List[Any]]:
        """B = alpha + Gamma, lower triangular with g on the diagonal."""
        s = self.stages
        return [[(self.alpha[i][j] + self.gamma[i][j]) if j < i else (self.g if j == i else self.g * 0)
                 for j in range(s)] for i in range(s)]


LINEARLY_IMPLICIT_EULER = RosenbrockMethod("linearly implicit Euler", [[F(0)]], [[F(0)]], [F(1)], F(1))
_G2 = 1 + 1 / math.sqrt(2)
ROS2 = RosenbrockMethod("ROS2", [[0.0, 0.0], [1.0, 0.0]], [[0.0, 0.0], [-2 * _G2, 0.0]], [0.5, 0.5], _G2)
ROS2_HALF = RosenbrockMethod("ROS2 with g = 1/2", [[F(0), F(0)], [F(1), F(0)]], [[F(0), F(0)], [F(-1), F(0)]],
                             [F(1, 2), F(1, 2)], F(1, 2))
# 3 stages, order 3, g = 1/2 (A-stable), built from the order conditions with Simpson weights.
ROW3_HALF = RosenbrockMethod(
    "ROW3 with g = 1/2",
    [[F(0)] * 3, [F(1, 2), F(0), F(0)], [F(-1), F(2), F(0)]],
    [[F(0)] * 3, [F(0), F(0), F(0)], [F(0), F(-3), F(0)]],
    [F(1, 6), F(2, 3), F(1, 6)], F(1, 2))


def order_condition_residuals(m: RosenbrockMethod) -> List[Any]:
    """Residuals of the conditions for orders 1, 2, 3, 3 (exact J; HNW II Table IV.7.1)."""
    s, B, b, g = m.stages, m.beta(), m.b, m.g
    al = [m.alpha_i(i) for i in range(s)]
    bp = [sum(B[i][:i], g * 0) for i in range(s)]  # beta_i' = sum_{j < i} beta_ij
    return [sum(b) - 1,
            sum(b[i] * bp[i] for i in range(s)) - (F(1, 2) - g),
            sum(b[i] * al[i] ** 2 for i in range(s)) - F(1, 3),
            sum(b[i] * B[i][k] * bp[k] for i in range(s) for k in range(i)) - (F(1, 6) - g + g * g)]


def w_order2_residual(m: RosenbrockMethod) -> Any:
    """For order 2 with an arbitrary matrix in place of J (W-method), also sum b_i alpha_i = 1/2."""
    return sum(m.b[i] * m.alpha_i(i) for i in range(m.stages)) - F(1, 2)


def stability_function(m: RosenbrockMethod, z: Any) -> Any:
    """R(z) = 1 + z b^T (I - z B)^(-1) 1 with B = alpha + Gamma (lower triangular: forward substitution)."""
    B = m.beta()
    w: List[Any] = []
    for i in range(m.stages):
        w.append((1 + z * sum(B[i][j] * w[j] for j in range(i))) / (1 - z * B[i][i]))
    return 1 + z * sum(bi * wi for bi, wi in zip(m.b, w))


# ---------------------------------------------------------------- linear algebra

def lu_factor(M: List[List[float]]) -> Tuple[List[List[float]], List[int]]:
    n = len(M)
    a = [row[:] for row in M]
    piv = list(range(n))
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(a[i][k]))
        if a[p][k] == 0:
            raise ZeroDivisionError("singular matrix I - h g J")
        a[k], a[p] = a[p], a[k]
        piv[k], piv[p] = piv[p], piv[k]
        for i in range(k + 1, n):
            a[i][k] /= a[k][k]
            for j in range(k + 1, n):
                a[i][j] -= a[i][k] * a[k][j]
    return a, piv


def lu_solve(lu: Tuple[List[List[float]], List[int]], rhs: Sequence[float]) -> List[float]:
    a, piv = lu
    n = len(a)
    x = [rhs[piv[i]] for i in range(n)]
    for i in range(n):
        x[i] -= sum(a[i][j] * x[j] for j in range(i))
    for i in reversed(range(n)):
        x[i] = (x[i] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]
    return x


# ---------------------------------------------------------------- the integrator

@dataclass
class RosenbrockResult:
    t: float
    y: Any
    steps: int
    f_evals: int
    jac_evals: int
    lu_factorizations: int
    solves: int
    path: List[Tuple[float, Any]] = field(default_factory=list)


def step_count(t0: float, t_end: float, h: float) -> int:
    if not h > 0:
        raise ValueError("the step size h must be positive")
    if t_end < t0:
        raise ValueError("t_end must not be before t0")
    r = (t_end - t0) / h
    return max(0, math.ceil(r - GRID_SLACK * max(1.0, r)))


def rosenbrock(f: Callable, t0: float, y0: Any, t_end: float, h: float, method: RosenbrockMethod = ROS2,
               jac: Optional[Callable] = None, dfdt: Optional[Callable] = None,
               keep_path: bool = False) -> RosenbrockResult:
    """Integrate y' = f(t, y) with fixed steps of a Rosenbrock method.

    y0 is a float or a list of floats. jac(t, y) gives the Jacobian (a float for scalar y) and
    dfdt(t, y) the partial derivative in t; when absent they are formed by forward differences,
    which costs d + 1 extra evaluations of f per step. Any matrix may be passed as jac: the
    methods with sum b_i alpha_i = 1/2 keep order 2 (W-methods).
    """
    scalar = not isinstance(y0, list)
    fv = (lambda t, y: [f(t, y[0])]) if scalar else f
    y = [float(y0)] if scalar else [float(v) for v in y0]
    d, s = len(y), method.stages
    al = [[float(x) for x in row] for row in method.alpha]
    ga = [[float(x) for x in row] for row in method.gamma]
    b = [float(x) for x in method.b]
    g = float(method.g)
    ai = [float(method.alpha_i(i)) for i in range(s)]
    gi = [float(method.gamma_i(i)) for i in range(s)]
    N = step_count(t0, t_end, h)  # @line L1
    t = float(t0)
    out = RosenbrockResult(t, None, 0, 0, 0, 0, 0)
    if keep_path:
        out.path.append((t, y[0] if scalar else list(y)))
    for n in range(N):  # @line L2
        tau = h if n < N - 1 else t_end - t
        f0 = None
        if jac is not None:  # @line L3
            J = [[jac(t, y[0])]] if scalar else jac(t, y)
        else:
            f0 = fv(t, y)
            out.f_evals += 1
            J = [[0.0] * d for _ in range(d)]
            for j in range(d):
                e = math.sqrt(2.2e-16) * max(1.0, abs(y[j]))
                yp = list(y)
                yp[j] += e
                fp = fv(t, yp)
                for i in range(d):
                    J[i][j] = (fp[i] - f0[i]) / e
            out.f_evals += d
        out.jac_evals += 1
        if dfdt is not None:
            ft = [dfdt(t, y[0])] if scalar else dfdt(t, y)
        else:
            if f0 is None:
                f0 = fv(t, y)
                out.f_evals += 1
            e = math.sqrt(2.2e-16) * max(1.0, abs(t))
            fe = fv(t + e, y)
            out.f_evals += 1
            ft = [(a - c) / e for a, c in zip(fe, f0)]
        lu = lu_factor([[(1.0 if i == j else 0.0) - tau * g * J[i][j] for j in range(d)] for i in range(d)])
        out.lu_factorizations += 1
        ks: List[List[float]] = []
        for i in range(s):  # @line L4
            yi = [y[r] + sum(al[i][j] * ks[j][r] for j in range(i)) for r in range(d)]
            gv = fv(t + ai[i] * tau, yi)  # @line L5
            out.f_evals += 1
            gk = [sum(ga[i][j] * ks[j][r] for j in range(i)) for r in range(d)]
            Jgk = [sum(J[r][q] * gk[q] for q in range(d)) for r in range(d)]
            rhs = [tau * gv[r] + tau * Jgk[r] + gi[i] * tau * tau * ft[r] for r in range(d)]
            ks.append(lu_solve(lu, rhs))  # @line L6
            out.solves += 1
        y = [y[r] + sum(b[i] * ks[i][r] for i in range(s)) for r in range(d)]  # @line L7
        t = t + tau  # @line L8
        out.steps += 1
        if keep_path:
            out.path.append((t, y[0] if scalar else list(y)))
    out.t = t
    out.y = y[0] if scalar else y
    return out
