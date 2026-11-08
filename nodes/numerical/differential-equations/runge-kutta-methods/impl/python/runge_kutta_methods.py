# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/runge-kutta-methods/. The authors are listed in prov/EV2XHR.jsonl.

"""Explicit Runge-Kutta methods given by a Butcher tableau (A, b, c), with fixed steps.

Also: the order conditions up to order 4 and the stability polynomial, both exact
when the tableau holds Fractions.
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Sequence, Tuple

GRID_SLACK = 1e-9


@dataclass
class Tableau:
    """A Butcher tableau: A is s x s, b and c have length s."""

    A: List[List[Any]]
    b: List[Any]
    c: List[Any]

    @property
    def stages(self) -> int:
        return len(self.b)

    def is_explicit(self) -> bool:
        return all(self.A[i][j] == 0 for i in range(self.stages) for j in range(i, self.stages))


F = Fraction
EULER = Tableau([[F(0)]], [F(1)], [F(0)])
HEUN = Tableau([[F(0), F(0)], [F(1), F(0)]], [F(1, 2), F(1, 2)], [F(0), F(1)])
MIDPOINT = Tableau([[F(0), F(0)], [F(1, 2), F(0)]], [F(0), F(1)], [F(0), F(1, 2)])
KUTTA3 = Tableau([[F(0)] * 3, [F(1, 2), F(0), F(0)], [F(-1), F(2), F(0)]],
                 [F(1, 6), F(2, 3), F(1, 6)], [F(0), F(1, 2), F(1)])
RK4 = Tableau([[F(0)] * 4, [F(1, 2), F(0), F(0), F(0)], [F(0), F(1, 2), F(0), F(0)],
               [F(0), F(0), F(1), F(0)]],
              [F(1, 6), F(1, 3), F(1, 3), F(1, 6)], [F(0), F(1, 2), F(1, 2), F(1)])
RULE38 = Tableau([[F(0)] * 4, [F(1, 3), F(0), F(0), F(0)], [F(-1, 3), F(1), F(0), F(0)],
                  [F(1), F(-1), F(1), F(0)]],
                 [F(1, 8), F(3, 8), F(3, 8), F(1, 8)], [F(0), F(1, 3), F(2, 3), F(1)])


@dataclass
class RKResult:
    """The final time and value, the number of steps and of evaluations of f."""

    t: Any
    y: Any
    steps: int
    f_evals: int
    path: List[Tuple[Any, Any]] = field(default_factory=list)


def _comb(y: Any, h: Any, coeffs: Sequence[Any], ks: Sequence[Any]) -> Any:
    """Return y + h * sum(coeffs[j] * ks[j]) for a scalar y or a list y, skipping zero coefficients."""
    if isinstance(y, list):
        out = list(y)
        for a, k in zip(coeffs, ks):
            if a != 0:
                for i in range(len(out)):
                    out[i] += h * a * k[i]
        return out
    out = y
    for a, k in zip(coeffs, ks):
        if a != 0:
            out = out + h * a * k
    return out


def rk_step(f: Callable[[Any, Any], Any], t: Any, y: Any, h: Any, tab: Tableau) -> Any:
    """One step of the explicit method: s evaluations of f."""
    if not tab.is_explicit():
        raise ValueError("rk_step needs an explicit tableau (A strictly lower triangular)")
    ks: List[Any] = []
    for i in range(tab.stages):  # @line L1
        Y = _comb(y, h, tab.A[i][:i], ks)  # @line L2
        ks.append(f(t + tab.c[i] * h, Y))  # @line L3
    return _comb(y, h, tab.b, ks)  # @line L4


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


def runge_kutta(f: Callable[[Any, Any], Any], t0: Any, y0: Any, t_end: Any, h: Any,
                tab: Tableau = RK4, keep_path: bool = False) -> RKResult:
    """Integrate y' = f(t, y) from t0 to t_end with fixed steps of an explicit RK method.

    The grid is t_n = t0 + n h; the last step ends exactly at t_end. Cost: N s evaluations
    of f with N = ceil((t_end - t0)/h) and s stages; O(s d) extra space.
    """
    n_steps = step_count(t0, t_end, h)  # @line L5
    t, y = t0, (list(y0) if isinstance(y0, list) else y0)  # @line L6
    path = [(t, y)] if keep_path else []
    for n in range(n_steps):  # @line L7
        t_next = t_end if n == n_steps - 1 else t0 + (n + 1) * h  # @line L8
        y = rk_step(f, t, y, t_next - t, tab)  # @line L9
        t = t_next  # @line L10
        if keep_path:
            path.append((t, y))
    return RKResult(t, y, n_steps, n_steps * tab.stages, path)  # @line L11


def order_conditions(tab: Tableau) -> List[Tuple[str, Any, Any]]:
    """The 8 order conditions up to order 4 as (name, value, required value).

    Uses c_i = sum_j a_ij for the trees; the row-sum condition is checked separately.
    """
    s, A, b = tab.stages, tab.A, tab.b
    c = [sum(A[i]) for i in range(s)]
    Ac = [sum(A[i][j] * c[j] for j in range(s)) for i in range(s)]
    Ac2 = [sum(A[i][j] * c[j] ** 2 for j in range(s)) for i in range(s)]
    AAc = [sum(A[i][j] * Ac[j] for j in range(s)) for i in range(s)]
    dot = lambda u, v: sum(x * w for x, w in zip(u, v))
    one = [1] * s
    return [
        ("b.1", dot(b, one), F(1)),
        ("b.c", dot(b, c), F(1, 2)),
        ("b.c^2", dot(b, [x * x for x in c]), F(1, 3)),
        ("b.Ac", dot(b, Ac), F(1, 6)),
        ("b.c^3", dot(b, [x ** 3 for x in c]), F(1, 4)),
        ("b.(c*Ac)", dot(b, [x * y for x, y in zip(c, Ac)]), F(1, 8)),
        ("b.Ac^2", dot(b, Ac2), F(1, 12)),
        ("b.AAc", dot(b, AAc), F(1, 24)),
    ]


def order(tab: Tableau) -> int:
    """The order of the method as far as the conditions up to order 4 show (an answer of 4 means at least 4)."""
    if any(sum(tab.A[i]) != tab.c[i] for i in range(tab.stages)):
        raise ValueError("the tableau must satisfy c_i = sum_j a_ij")
    conds = order_conditions(tab)
    groups = [conds[0:1], conds[1:2], conds[2:4], conds[4:8]]
    p = 0
    for g in groups:
        if all(v == want for _, v, want in g):
            p += 1
        else:
            break
    return p


def stability_polynomial(tab: Tableau) -> List[Any]:
    """Coefficients r_0..r_s of R(z) = 1 + sum_k z^k b^T A^(k-1) 1 for an explicit tableau."""
    s = tab.stages
    coeffs = [F(1)]
    v = [F(1)] * s  # A^(k-1) 1
    for _ in range(s):
        coeffs.append(sum(bi * vi for bi, vi in zip(tab.b, v)))
        v = [sum(tab.A[i][j] * v[j] for j in range(s)) for i in range(s)]
    return coeffs
