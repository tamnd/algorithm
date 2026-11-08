# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/taylor-series-method/. The authors are listed in prov/9A499S.jsonl.

"""The Taylor series method of order p for y' = f(t, y).

The Taylor coefficients y_[k] = y^(k)(t_n)/k! of the solution are computed by automatic
differentiation in Taylor mode: if y is known up to order k, then f(t, y) is known up to
order k, and y_[k+1] = f(t, y)_[k] / (k + 1). The step is y_(n+1) = sum_k y_[k] h^k.

f is written with ordinary arithmetic and the functions exp, sin, cos of this module; it
receives t and y as Series objects (y as a list of Series when y is a vector).
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List

GRID_SLACK = 1e-9  # relative slack in the step count against rounding of (T - t0)/h


class Series:
    """A truncated power series c[0] + c[1] s + ... + c[m-1] s^(m-1)."""

    __slots__ = ("c",)

    def __init__(self, c):
        self.c = list(c)

    def _lift(self, other):
        if isinstance(other, Series):
            return other
        return Series([other] + [0 * other] * (len(self.c) - 1))

    def __len__(self):
        return len(self.c)

    def __add__(self, other):
        o = self._lift(other)
        return Series([a + b for a, b in zip(self.c, o.c)])

    __radd__ = __add__

    def __neg__(self):
        return Series([-a for a in self.c])

    def __sub__(self, other):
        return self + (-self._lift(other))

    def __rsub__(self, other):
        return self._lift(other) - self

    def __mul__(self, other):
        if not isinstance(other, Series):
            return Series([a * other for a in self.c])
        m = min(len(self.c), len(other.c))
        return Series([sum(self.c[i] * other.c[k - i] for i in range(k + 1)) for k in range(m)])

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, Series):
            return Series([a / other for a in self.c])
        m = min(len(self.c), len(other.c))
        if other.c[0] == 0:
            raise ZeroDivisionError("series division by a series with zero constant term")
        q = []
        for k in range(m):
            q.append((self.c[k] - sum(q[i] * other.c[k - i] for i in range(k))) / other.c[0])
        return Series(q)

    def __rtruediv__(self, other):
        return self._lift(other) / self

    def __pow__(self, n: int):
        if not isinstance(n, int) or n < 0:
            raise ValueError("only non-negative integer powers")
        r = self._lift(1 + 0 * self.c[0])
        for _ in range(n):
            r = r * self
        return r


def exp(x):
    """exp of a Series by the recurrence k e_k = sum_j j x_j e_(k-j)."""
    if not isinstance(x, Series):
        return math.exp(x)
    x0 = x.c[0]
    e = [Fraction(1) if isinstance(x0, Fraction) and x0 == 0 else math.exp(x0)]
    for k in range(1, len(x.c)):
        e.append(sum(j * x.c[j] * e[k - j] for j in range(1, k + 1)) / k)
    return Series(e)


def _sincos(x):
    s, c = [math.sin(x.c[0])], [math.cos(x.c[0])]
    for k in range(1, len(x.c)):
        s.append(sum(j * x.c[j] * c[k - j] for j in range(1, k + 1)) / k)
        c.append(-sum(j * x.c[j] * s[k - j] for j in range(1, k + 1)) / k)
    return Series(s), Series(c)


def sin(x):
    return _sincos(x)[0] if isinstance(x, Series) else math.sin(x)


def cos(x):
    return _sincos(x)[1] if isinstance(x, Series) else math.cos(x)


def taylor_coefficients(f: Callable, t: Any, y: Any, p: int) -> List[Any]:
    """Return [y_[0], ..., y_[p]], the normalized derivatives y^(k)(t)/k! of the solution through
    (t, y). Scalar y gives scalars, list y gives lists. Costs p evaluations of f on series."""
    if p < 0:
        raise ValueError("the order p must be non-negative")
    vec = isinstance(y, list)
    ys = [[v] for v in (y if vec else [y])]  # @line L2
    one = 1 + 0 * t
    for k in range(p):  # @line L3
        ts = Series(([t, one] + [0 * t] * k)[: k + 1])  # the series of t + s
        arg = [Series(c) for c in ys]
        val = f(ts, arg if vec else arg[0])  # @line L4
        val = val if vec else [val]
        for i in range(len(ys)):
            v = val[i]
            ck = v.c[k] if isinstance(v, Series) else (v if k == 0 else 0 * v)
            ys[i].append(ck / (k + 1))  # @line L5
    if vec:
        return [[ys[i][k] for i in range(len(ys))] for k in range(p + 1)]
    return [ys[0][k] for k in range(p + 1)]


def taylor_step(f: Callable, t: Any, y: Any, h: Any, p: int) -> Any:
    """One step: sum_k y_[k] h^k, evaluated by Horner's rule."""
    co = taylor_coefficients(f, t, y, p)
    if isinstance(y, list):
        acc = list(co[p])
        for k in range(p - 1, -1, -1):
            acc = [co[k][i] + h * acc[i] for i in range(len(y))]
        return acc
    acc = co[p]
    for k in range(p - 1, -1, -1):  # @line L6
        acc = co[k] + h * acc
    return acc


def step_count(t0: Any, t_end: Any, h: Any) -> int:
    """The number N of steps of length at most h (up to GRID_SLACK) from t0 to t_end."""
    if not h > 0:
        raise ValueError("the step size h must be positive")
    if t_end < t0:
        raise ValueError("t_end must not precede t0")
    r = (t_end - t0) / h
    if isinstance(r, (int, Fraction)):
        return math.ceil(r)
    return max(0, math.ceil(r - GRID_SLACK * max(1.0, r)))


@dataclass
class TaylorResult:
    t: Any
    y: Any
    steps: int
    series_evals: int
    path: List[Any] = field(default_factory=list)


def taylor_method(f: Callable, t0: Any, y0: Any, t_end: Any, h: Any, p: int,
                  keep_path: bool = False) -> TaylorResult:
    """Fixed-step Taylor method of order p from t0 to t_end; the last step ends at t_end."""
    if p < 1:
        raise ValueError("the order p must be at least 1")
    N = step_count(t0, t_end, h)  # @line L1
    t, y = t0, y0
    path = [(t, y)] if keep_path else []
    for n in range(N):
        t_next = t_end if n == N - 1 else t0 + (n + 1) * h
        y = taylor_step(f, t, y, t_next - t, p)
        t = t_next  # @line L7
        if keep_path:
            path.append((t, y))
    return TaylorResult(t, y, N, N * p, path)
