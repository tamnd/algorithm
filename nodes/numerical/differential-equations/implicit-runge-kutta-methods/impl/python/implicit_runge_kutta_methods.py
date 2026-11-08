# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-runge-kutta-methods/. The authors are listed in prov/W7X2PW.jsonl.

"""Implicit Runge-Kutta methods for y' = f(t, y), y(t0) = y0, with simplified Newton.

One step with tableau (A, b, c) and s stages solves for the stage increments
Z_i = Y_i - y_n the s d equations

    Z_i = h sum_j a_ij f(t_n + c_j h, y_n + Z_j)        (i = 1..s)

by simplified Newton iteration with the matrix I - h (A kron J), J = f_y(t_n, y_n),
factored once per step, and then sets y_(n+1) = y_n + sum_i d_i Z_i with
d^T = b^T A^(-1) when A is nonsingular, else y_(n+1) = y_n + h sum_i b_i f(Y_i).
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

GRID_SLACK = 1e-9  # relative slack in the step count against rounding of (T - t0)/h

_S3 = math.sqrt(3.0)
Fr = Fraction

# Tableaux (A, b, c). Rational ones are exact; the Gauss method of order 4 has sqrt(3).
METHODS: Dict[str, Tuple[list, list, list]] = {
    "backward-euler": ([[Fr(1)]], [Fr(1)], [Fr(1)]),
    "implicit-midpoint": ([[Fr(1, 2)]], [Fr(1)], [Fr(1, 2)]),
    "gauss2": ([[0.25, 0.25 - _S3 / 6], [0.25 + _S3 / 6, 0.25]], [0.5, 0.5],
               [0.5 - _S3 / 6, 0.5 + _S3 / 6]),
    "radau2a": ([[Fr(5, 12), Fr(-1, 12)], [Fr(3, 4), Fr(1, 4)]], [Fr(3, 4), Fr(1, 4)],
                [Fr(1, 3), Fr(1)]),
    "lobatto3a": ([[Fr(0), Fr(0), Fr(0)], [Fr(5, 24), Fr(1, 3), Fr(-1, 24)],
                   [Fr(1, 6), Fr(2, 3), Fr(1, 6)]], [Fr(1, 6), Fr(2, 3), Fr(1, 6)],
                  [Fr(0), Fr(1, 2), Fr(1)]),
    "lobatto3c": ([[Fr(1, 2), Fr(-1, 2)], [Fr(1, 2), Fr(1, 2)]], [Fr(1, 2), Fr(1, 2)],
                  [Fr(0), Fr(1)]),
    # Not implicit: explicit Euler as a tableau, to show what implicitness buys.
    "explicit-euler": ([[Fr(0)]], [Fr(1)], [Fr(0)]),
}
ORDERS = {"backward-euler": 1, "implicit-midpoint": 2, "gauss2": 4, "radau2a": 3,
          "lobatto3a": 4, "lobatto3c": 2, "explicit-euler": 1}


@dataclass
class IRKResult:
    """Final time and value, and the cost counters of the run."""

    t: Any
    y: Any
    steps: int
    f_evals: int
    jac_evals: int
    lu_factorizations: int
    newton_iterations: int
    path: List[Tuple[Any, Any]] = field(default_factory=list)


def step_count(t0: Any, t_end: Any, h: Any) -> int:
    """The number N of steps of length at most h (up to GRID_SLACK) from t0 to t_end."""
    if not h > 0:
        raise ValueError("the step size h must be positive")
    if t_end < t0:
        raise ValueError("t_end must not be before t0")
    r = (t_end - t0) / h
    if isinstance(r, (int, Fraction)):
        return math.ceil(r)
    return max(0, math.ceil(r - GRID_SLACK * max(1.0, r)))


def lu_factor(m: List[List[Any]]) -> Tuple[List[List[Any]], List[int]]:
    """LU factorization with partial pivoting of a square matrix (copied). Raises on singular."""
    n = len(m)
    a = [row[:] for row in m]
    piv = list(range(n))
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(a[i][k]))
        if a[p][k] == 0:
            raise ZeroDivisionError("singular matrix")
        if p != k:
            a[k], a[p] = a[p], a[k]
            piv[k], piv[p] = piv[p], piv[k]
        for i in range(k + 1, n):
            a[i][k] = a[i][k] / a[k][k]
            if a[i][k] != 0:
                lik = a[i][k]
                rk = a[k]
                ri = a[i]
                for j in range(k + 1, n):
                    ri[j] -= lik * rk[j]
    return a, piv


def lu_solve(lu: Tuple[List[List[Any]], List[int]], rhs: Sequence[Any]) -> List[Any]:
    """Solve M x = rhs from the factors of lu_factor."""
    a, piv = lu
    n = len(a)
    x = [rhs[piv[i]] for i in range(n)]
    for i in range(n):
        for j in range(i):
            x[i] -= a[i][j] * x[j]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            x[i] -= a[i][j] * x[j]
        x[i] = x[i] / a[i][i]
    return x


def _tableau(method: Any) -> Tuple[list, list, list]:
    if isinstance(method, str):
        if method not in METHODS:
            raise ValueError("unknown method " + method)
        return METHODS[method]
    a, b, c = method
    return a, b, c


def weights_d(a: List[List[Any]], b: List[Any]) -> Optional[List[Any]]:
    """d^T = b^T A^(-1), or None when A is singular."""
    s = len(b)
    at = [[a[j][i] for j in range(s)] for i in range(s)]
    try:
        return lu_solve(lu_factor(at), b)
    except ZeroDivisionError:
        return None


def stability_function(z: Any, method: Any = "radau2a") -> Any:
    """R(z) = 1 + z b^T (I - z A)^(-1) 1, exact for Fraction z and a rational tableau."""
    a, b, _ = _tableau(method)
    s = len(b)
    m = [[(1 if i == j else 0) - z * a[i][j] for j in range(s)] for i in range(s)]
    x = lu_solve(lu_factor(m), [1] * s)
    return 1 + z * sum(b[i] * x[i] for i in range(s))


def fd_jacobian(f: Callable, t: Any, y: List[Any], fy: List[Any]) -> List[List[Any]]:
    """Forward difference Jacobian: d extra evaluations of f."""
    d = len(y)
    cols = []
    for j in range(d):
        eta = 1.4901161193847656e-08 * max(1.0, abs(float(y[j])))
        yp = y[:]
        yp[j] = yp[j] + eta
        fp = _as_list(f(t, yp))
        cols.append([(fp[i] - fy[i]) / eta for i in range(d)])
    return [[cols[j][i] for j in range(d)] for i in range(d)]


def _as_list(v: Any) -> List[Any]:
    return list(v) if isinstance(v, (list, tuple)) else [v]


def implicit_runge_kutta(f: Callable[[Any, Any], Any], t0: Any, y0: Any, t_end: Any, h: Any,
                         method: Any = "radau2a",
                         jac: Optional[Callable[[Any, Any], Any]] = None,
                         tol: float = 1e-12, max_iter: int = 50,
                         keep_path: bool = False) -> IRKResult:
    """Integrate y' = f(t, y) from t0 to t_end with an implicit Runge-Kutta method.

    y0 is a number or a list; f returns the same shape. jac(t, y) returns the d x d
    Jacobian (a number for scalar y); without it a forward difference Jacobian is used.
    Per step: one Jacobian, one LU of size s d, and per Newton iteration s evaluations of f
    and one solve. Raises RuntimeError if Newton does not converge in max_iter iterations.
    """
    a, b, c = _tableau(method)
    s = len(b)
    scalar = not isinstance(y0, (list, tuple))
    dvec = weights_d(a, b)
    n_steps = step_count(t0, t_end, h)  # @line L1
    t, y = t0, _as_list(y0)  # @line L2
    dim = len(y)
    nf = nj = nlu = nit = 0
    path = [(t, y0 if scalar else y[:])] if keep_path else []
    for n in range(n_steps):  # @line L3
        t_next = t_end if n == n_steps - 1 else t0 + (n + 1) * h  # @line L4
        k = t_next - t  # @line L5
        if jac is not None:  # @line L6
            jm = jac(t, y if not scalar else y[0])
            jm = [[jm]] if scalar else [list(r) for r in jm]
        else:
            fy = _as_list(f(t, y[0] if scalar else y))
            nf += 1
            jm = fd_jacobian(lambda tt, yy: f(tt, yy[0] if scalar else yy), t, y, fy)
            nf += dim
        nj += 1
        sd = s * dim
        mat = [[0] * sd for _ in range(sd)]  # @line L7
        for i in range(s):
            for j in range(s):
                for p in range(dim):
                    for q in range(dim):
                        mat[i * dim + p][j * dim + q] = ((1 if (i == j and p == q) else 0)
                                                         - k * a[i][j] * jm[p][q])
        lu = lu_factor(mat)
        nlu += 1
        z = [[0 * yi for yi in y] for _ in range(s)]  # @line L8
        converged = False
        for _ in range(max_iter):  # @line L9
            fs = []
            for i in range(s):  # @line L10
                yi = [y[p] + z[i][p] for p in range(dim)]
                fs.append(_as_list(f(t + c[i] * k, yi[0] if scalar else yi)))
            nf += s
            nit += 1
            rhs = []  # @line L11
            for i in range(s):
                for p in range(dim):
                    rhs.append(-z[i][p] + k * sum(a[i][j] * fs[j][p] for j in range(s)))
            dz = lu_solve(lu, rhs)
            for i in range(s):  # @line L12
                for p in range(dim):
                    z[i][p] = z[i][p] + dz[i * dim + p]
            size = max(abs(v) for v in dz) if dz else 0
            scale = max([1.0] + [abs(v) for v in y])
            if size <= tol * scale:  # @line L13
                converged = True
                break
        if not converged:
            raise RuntimeError("simplified Newton did not converge; reduce h")
        if dvec is not None:  # @line L14
            y = [y[p] + sum(dvec[i] * z[i][p] for i in range(s)) for p in range(dim)]
        else:
            fs = [_as_list(f(t + c[i] * k, (lambda v: v[0] if scalar else v)(
                [y[p] + z[i][p] for p in range(dim)]))) for i in range(s)]
            nf += s
            y = [y[p] + k * sum(b[i] * fs[i][p] for i in range(s)) for p in range(dim)]
        t = t_next  # @line L15
        if keep_path:
            path.append((t, y[0] if scalar else y[:]))
    return IRKResult(t, y[0] if scalar else y, n_steps, nf, nj, nlu, nit, path)  # @line L16
