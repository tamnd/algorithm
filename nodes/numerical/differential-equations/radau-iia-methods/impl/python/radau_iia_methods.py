# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radau-iia-methods/. The authors are listed in prov/SBC09Y.jsonl.

"""Radau IIA implicit Runge-Kutta methods with s stages, fixed steps and simplified Newton.

The tableau is built from the nodes by integrating the Lagrange basis exactly, so it is exact
in Fractions when the nodes are rational (s = 1, 2). The stability function R(z) is computed
from the tableau and can be compared with the (s-1, s) Pade approximant of exp(z).
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Optional, Sequence, Tuple

GRID_SLACK = 1e-9


# ---------------------------------------------------------------- polynomials (lowest degree first)

def _pmul(p: Sequence[Any], q: Sequence[Any]) -> List[Any]:
    out = [p[0] * 0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def _peval(p: Sequence[Any], x: Any) -> Any:
    acc = p[-1] * 0
    for a in reversed(p):
        acc = acc * x + a
    return acc


def _pderiv(p: Sequence[Any]) -> List[Any]:
    return [k * p[k] for k in range(1, len(p))] or [p[0] * 0]


def radau_polynomial(s: int) -> List[Fraction]:
    """d^(s-1)/dx^(s-1) of x^(s-1) (x-1)^s, with Fraction coefficients; its zeros are the nodes."""
    p = [Fraction(1)]
    for _ in range(s - 1):
        p = _pmul(p, [Fraction(0), Fraction(1)])
    for _ in range(s):
        p = _pmul(p, [Fraction(-1), Fraction(1)])
    for _ in range(s - 1):
        p = _pderiv(p)
    return p


def radau_nodes(s: int) -> List[Any]:
    """The s Radau IIA nodes in (0, 1], c_s = 1. Fractions for s <= 2, floats otherwise."""
    if s < 1:
        raise ValueError("s must be at least 1")
    if s == 1:
        return [Fraction(1)]
    if s == 2:
        return [Fraction(1, 3), Fraction(1)]
    p = [float(a) for a in radau_polynomial(s)]
    dp = _pderiv(p)
    roots = []
    for k in range(s):  # Chebyshev-like starting guesses, then Newton with deflation
        x = 0.5 - 0.5 * math.cos(math.pi * (k + 0.75) / s)
        for _ in range(100):
            val = _peval(p, x)
            der = _peval(dp, x) - val * sum(1.0 / (x - r) for r in roots)
            dx = val / der
            x -= dx
            if abs(dx) < 1e-16:
                break
        roots.append(x)
    roots.sort()
    roots[-1] = 1.0
    return roots


@dataclass
class Tableau:
    A: List[List[Any]]
    b: List[Any]
    c: List[Any]

    @property
    def stages(self) -> int:
        return len(self.b)


def collocation_tableau(c: Sequence[Any]) -> Tableau:
    """a_ij = integral from 0 to c_i of the Lagrange basis l_j, b_j = integral from 0 to 1."""
    s = len(c)
    A = [[c[0] * 0] * s for _ in range(s)]
    b = [c[0] * 0] * s
    for j in range(s):
        lj = [c[0] * 0 + 1]
        for m in range(s):
            if m != j:
                d = c[j] - c[m]
                lj = _pmul(lj, [-c[m] / d, 1 / d])
        integ = [c[0] * 0] + [lj[k] / (k + 1) for k in range(len(lj))]
        for i in range(s):
            A[i][j] = _peval(integ, c[i])
        b[j] = _peval(integ, c[0] * 0 + 1)
    return Tableau(A, b, list(c))


def radau_tableau(s: int) -> Tableau:
    """The Radau IIA tableau with s stages (order 2s - 1)."""
    return collocation_tableau(radau_nodes(s))


# ---------------------------------------------------------------- linear algebra

def lu_factor(M: List[List[float]]) -> Tuple[List[List[float]], List[int]]:
    """LU with partial pivoting, in place on a copy. Raises ZeroDivisionError if singular."""
    n = len(M)
    a = [row[:] for row in M]
    piv = list(range(n))
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(a[i][k]))
        if a[p][k] == 0:
            raise ZeroDivisionError("singular iteration matrix")
        if p != k:
            a[k], a[p] = a[p], a[k]
            piv[k], piv[p] = piv[p], piv[k]
        for i in range(k + 1, n):
            a[i][k] /= a[k][k]
            m = a[i][k]
            if m != 0:
                rk, ri = a[k], a[i]
                for j in range(k + 1, n):
                    ri[j] -= m * rk[j]
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


def stability_function(tab: Tableau, z: Any) -> Any:
    """R(z) = 1 + z b^T (I - z A)^(-1) 1, by exact Gaussian elimination when z and the tableau are exact."""
    s = tab.stages
    M = [[(1 if i == j else 0) - z * tab.A[i][j] for j in range(s)] + [1] for i in range(s)]
    for k in range(s):  # Gauss-Jordan without pivoting search beyond nonzero
        p = next(i for i in range(k, s) if M[i][k] != 0)
        M[k], M[p] = M[p], M[k]
        for i in range(s):
            if i != k and M[i][k] != 0:
                m = M[i][k] / M[k][k]
                M[i] = [x - m * y for x, y in zip(M[i], M[k])]
    w = [M[i][s] / M[i][i] for i in range(s)]
    return 1 + z * sum(bi * wi for bi, wi in zip(tab.b, w))


def pade_exp(k: int, j: int, z: Any) -> Any:
    """The (k, j) Pade approximant of exp(z): numerator degree k, denominator degree j."""
    f = math.factorial
    P = sum(Fraction(f(k + j - i) * f(k), f(k + j) * f(i) * f(k - i)) * z ** i for i in range(k + 1))
    Q = sum(Fraction(f(k + j - i) * f(j), f(k + j) * f(i) * f(j - i)) * (-z) ** i for i in range(j + 1))
    return P / Q


# ---------------------------------------------------------------- the integrator

@dataclass
class RadauResult:
    t: Any
    y: Any
    steps: int
    f_evals: int
    jac_evals: int
    lu_factorizations: int
    newton_iterations: int
    path: List[Tuple[Any, Any]] = field(default_factory=list)


def step_count(t0: float, t_end: float, h: float) -> int:
    if not h > 0:
        raise ValueError("the step size h must be positive")
    if t_end < t0:
        raise ValueError("t_end must not be before t0")
    r = (t_end - t0) / h
    return max(0, math.ceil(r - GRID_SLACK * max(1.0, r)))


def fd_jacobian(f: Callable, t: float, y: List[float], fy: List[float]) -> List[List[float]]:
    """Forward-difference Jacobian: d evaluations of f."""
    d = len(y)
    J = [[0.0] * d for _ in range(d)]
    for j in range(d):
        e = math.sqrt(2.2e-16) * max(1.0, abs(y[j]))
        yp = list(y)
        yp[j] += e
        fp = f(t, yp)
        for i in range(d):
            J[i][j] = (fp[i] - fy[i]) / e
    return J


def radau_iia(f: Callable[[float, Any], Any], t0: float, y0: Any, t_end: float, h: float, s: int = 3,
              jac: Optional[Callable[[float, Any], Any]] = None, tol: float = 1e-12, max_iter: int = 20,
              keep_path: bool = False) -> RadauResult:
    """Integrate y' = f(t, y) with the s-stage Radau IIA method and fixed steps of size h.

    y0 may be a float or a list of floats; f must return the same kind. jac(t, y) returns the
    d x d Jacobian (a float for scalar y); without it, forward differences are used.
    Raises RuntimeError if simplified Newton does not converge in max_iter iterations.
    """
    scalar = not isinstance(y0, list)
    fv = (lambda t, y: [f(t, y[0])]) if scalar else f
    jv = None
    if jac is not None:
        jv = (lambda t, y: [[jac(t, y[0])]]) if scalar else jac
    y = [float(y0)] if scalar else [float(v) for v in y0]
    d = len(y)
    tab = radau_tableau(s)  # @line L1
    A = [[float(a) for a in row] for row in tab.A]
    c = [float(x) for x in tab.c]
    N = step_count(t0, t_end, h)
    t = float(t0)
    out = RadauResult(t, None, 0, 0, 0, 0, 0)
    if keep_path:
        out.path.append((t, y[0] if scalar else list(y)))
    for n in range(N):  # @line L2
        tau = h if n < N - 1 else t_end - t
        if jv is not None:  # @line L3
            J = jv(t, y)
        else:
            J = fd_jacobian(fv, t, y, fv(t, y))
            out.f_evals += d + 1
        out.jac_evals += 1
        M = [[(1.0 if r == q else 0.0) - tau * A[r // d][q // d] * J[r % d][q % d]
              for q in range(s * d)] for r in range(s * d)]
        lu = lu_factor(M)
        out.lu_factorizations += 1
        Z = [0.0] * (s * d)  # @line L4
        for k in range(max_iter + 1):  # @line L5
            if k == max_iter:
                raise RuntimeError("simplified Newton did not converge; reduce h")
            try:
                Fz = [fv(t + c[j] * tau, [y[i] + Z[j * d + i] for i in range(d)]) for j in range(s)]
            except OverflowError:
                raise RuntimeError("simplified Newton diverged; reduce h") from None
            out.f_evals += s
            G = [-Z[r] + tau * sum(A[r // d][j] * Fz[j][r % d] for j in range(s))  # @line L6
                 for r in range(s * d)]
            dZ = lu_solve(lu, G)  # @line L7
            Z = [z + dz for z, dz in zip(Z, dZ)]
            out.newton_iterations += 1
            scale = max(1.0, max(abs(v) for v in y))
            if not all(math.isfinite(v) for v in dZ):
                raise RuntimeError("simplified Newton diverged; reduce h")
            if max(abs(v) for v in dZ) <= tol * scale:  # @line L8
                break
        y = [y[i] + Z[(s - 1) * d + i] for i in range(d)]  # @line L9
        t = t + tau  # @line L10
        out.steps += 1
        if keep_path:
            out.path.append((t, y[0] if scalar else list(y)))
    out.t = t
    out.y = y[0] if scalar else y
    return out
