# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backward-euler-method/. The authors are listed in prov/8ARQ7F.jsonl.

"""Backward (implicit) Euler method for y' = f(t, y), y(t0) = y0.

One step solves the implicit equation

    Y = y_n + h f(t_n + h, Y)

for Y = y_{n+1} with Newton's method. The Jacobian of G(Y) = Y - y_n - h f(t_n + h, Y)
is I - h J, where J = df/dy at (t_n + h, Y). The caller can pass J; otherwise a forward
difference approximation is used. y0 may be a float (scalar problem) or a list of floats.
"""

from typing import Callable, List, Optional, Sequence, Tuple, Union

Vector = List[float]
State = Union[float, Sequence[float]]


def solve_linear(a: List[List[float]], b: Vector) -> Vector:
    """Solve a x = b by Gaussian elimination with partial pivoting (a and b are copied)."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(m[i][k]))
        if m[p][k] == 0.0:
            raise ZeroDivisionError("singular Newton matrix I - h J")
        m[k], m[p] = m[p], m[k]
        for i in range(k + 1, n):
            r = m[i][k] / m[k][k]
            if r != 0.0:
                for j in range(k, n + 1):
                    m[i][j] -= r * m[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / m[i][i]
    return x


def _fd_jacobian(f: Callable[[float, Vector], Vector], t: float, y: Vector, fy: Vector) -> List[List[float]]:
    d = len(y)
    jac = [[0.0] * d for _ in range(d)]
    for j in range(d):
        dy = 1e-7 * max(1.0, abs(y[j]))
        yp = list(y)
        yp[j] += dy
        fp = f(t, yp)
        for i in range(d):
            jac[i][j] = (fp[i] - fy[i]) / dy
    return jac


def backward_euler_step(
    f: Callable[[float, Vector], Vector],
    t: float,
    y: Vector,
    h: float,
    jac: Optional[Callable[[float, Vector], List[List[float]]]] = None,
    tol: float = 1e-12,
    max_newton: int = 50,
) -> Tuple[Vector, int]:
    """Return (y_{n+1}, number of Newton iterations) for one step of size h from (t, y)."""
    d = len(y)
    t1 = t + h
    big_y = list(y)  # @line L5: Newton starts at the old value
    for it in range(1, max_newton + 1):  # @line L6
        fy = f(t1, big_y)
        g = [big_y[i] - y[i] - h * fy[i] for i in range(d)]  # @line L7
        jm = jac(t1, big_y) if jac is not None else _fd_jacobian(f, t1, big_y, fy)
        a = [[(1.0 if i == j else 0.0) - h * jm[i][j] for j in range(d)] for i in range(d)]
        delta = solve_linear(a, [-gi for gi in g])  # @line L8
        big_y = [big_y[i] + delta[i] for i in range(d)]  # @line L9
        size = max(abs(v) for v in big_y) if d else 0.0
        if max((abs(v) for v in delta), default=0.0) <= tol * max(1.0, size):  # @line L10
            return big_y, it
    raise ArithmeticError("Newton iteration did not converge; try a smaller h")


def backward_euler(
    f: Callable,
    t0: float,
    y0: State,
    t_end: float,
    h: float,
    jac: Optional[Callable] = None,
    tol: float = 1e-12,
    max_newton: int = 50,
) -> Tuple[List[float], list]:
    """Integrate from t0 to t_end (t_end >= t0) with step h > 0.

    Returns the lists of times and values. The last step is shortened so that it ends at
    t_end exactly. For a scalar y0 the values are floats and f, jac use floats too.
    """
    if h <= 0.0:
        raise ValueError("h must be positive")
    if t_end < t0:
        raise ValueError("t_end must be at least t0")
    scalar = isinstance(y0, (int, float))
    if scalar:
        fv = lambda t, y: [f(t, y[0])]
        jv = (lambda t, y: [[jac(t, y[0])]]) if jac is not None else None
        y = [float(y0)]
    else:
        fv, jv, y = f, jac, [float(v) for v in y0]
    ts, ys = [t0], [y[0] if scalar else list(y)]  # @line L1
    t, n = t0, 0
    span = t_end - t0
    while t < t_end:  # @line L2
        n += 1  # @line L3
        t_next = t0 + n * h  # @line L4: computed from t0, so rounding does not drift
        if t_next > t_end or t_end - t_next <= 1e-12 * max(1.0, abs(span)):
            t_next = t_end
        y, _ = backward_euler_step(fv, t, y, t_next - t, jv, tol, max_newton)
        t = t_next  # @line L11
        ts.append(t)
        ys.append(y[0] if scalar else list(y))
    return ts, ys
