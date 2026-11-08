# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symplectic-euler-method/. The authors are listed in prov/B9ZN3M.jsonl.

"""Symplectic Euler for Hamiltonian systems p' = -H_q(p, q), q' = H_p(p, q).

Variant A (the one of the pseudocode):  p_new = p - h H_q(p_new, q),  q_new = q + h H_p(p_new, q).
Variant B (its adjoint):               q_new = q + h H_p(p, q_new),  p_new = p - h H_q(p, q_new).
For a separable H = T(p) + V(q) both are explicit:
    A: p_new = p - h V'(q),     q_new = q + h T'(p_new)
    B: q_new = q + h T'(p),     p_new = p - h V'(q_new)
Order 1, symplectic. q and p are numbers or lists of numbers.
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Tuple

GRID_SLACK = 1e-9  # relative slack in the step count against rounding of (T - t0)/h


@dataclass
class SEResult:
    """Final time, position q and momentum p, step count, gradient evaluations, optional path."""
    t: Any
    q: Any
    p: Any
    steps: int
    evals: int
    path: List[Tuple[Any, Any, Any]] = field(default_factory=list)


def _axpy(x, alpha, y):
    """x + alpha y for numbers or lists."""
    if isinstance(x, list):
        return [xi + alpha * yi for xi, yi in zip(x, y)]
    return x + alpha * y


def _dist(x, y):
    if isinstance(x, list):
        return max((abs(a - b) for a, b in zip(x, y)), default=0.0)
    return abs(x - y)


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


def se_step(dT: Callable, dV: Callable, q: Any, p: Any, h: Any, variant: str = "A"):
    """One explicit step for H = T(p) + V(q); dT = grad T, dV = grad V."""
    if variant == "A":
        p = _axpy(p, -h, dV(q))  # @line L4
        q = _axpy(q, h, dT(p))  # @line L5
    elif variant == "B":
        q = _axpy(q, h, dT(p))
        p = _axpy(p, -h, dV(q))
    else:
        raise ValueError("variant must be 'A' or 'B'")
    return q, p


def symplectic_euler(dT: Callable, dV: Callable, t0: Any, q0: Any, p0: Any, t_end: Any, h: Any,
                     variant: str = "A", keep_path: bool = False) -> SEResult:
    """Integrate a separable Hamiltonian system from t0 to t_end; the last step ends at t_end."""
    N = step_count(t0, t_end, h)  # @line L1
    q, p, t = q0, p0, t0  # @line L2
    path = [(t, q, p)] if keep_path else []
    for n in range(N):  # @line L3
        t_next = t_end if n == N - 1 else t0 + (n + 1) * h
        q, p = se_step(dT, dV, q, p, t_next - t, variant)
        t = t_next  # @line L6
        if keep_path:
            path.append((t, q, p))
    return SEResult(t, q, p, N, 2 * N, path)  # @line L7


def se_step_general(Hp: Callable, Hq: Callable, q: Any, p: Any, h: Any,
                    tol: float = 1e-14, max_iter: int = 100) -> Tuple[Any, Any, int]:
    """Variant A for a general H(p, q): solve p_new = p - h Hq(p_new, q) by fixed-point iteration.

    Converges when h times the Lipschitz constant of Hq in p is below 1.
    Returns (q_new, p_new, iterations).
    """
    p_new = p
    for it in range(1, max_iter + 1):
        nxt = _axpy(p, -h, Hq(p_new, q))
        size = max(abs(v) for v in nxt) if isinstance(nxt, list) else abs(nxt)
        if _dist(nxt, p_new) <= tol * (1 + size):
            p_new = nxt
            break
        p_new = nxt
    else:
        raise RuntimeError("fixed-point iteration did not converge")
    return _axpy(q, h, Hp(p_new, q)), p_new, it


def oscillator_matrix(h: Any) -> List[List[Any]]:
    """Variant A on H = (p^2 + q^2)/2 as a matrix acting on (q, p)."""
    return [[1 - h * h, h], [-h, 1]]
