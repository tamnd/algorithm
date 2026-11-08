# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verlet-integration/. The authors are listed in prov/S32WCK.jsonl.

"""Velocity Verlet (Stormer-Verlet, leapfrog) for q'' = a(q), written as q' = v, v' = a(q).

One step of size h (kick, drift, kick):
    v_half = v + (h/2) a(q)
    q_new  = q + h v_half
    v_new  = v_half + (h/2) a(q_new)
The force a(q_new) is reused as a(q) of the next step, so each step costs one evaluation of a.
Second order, symplectic and time-reversible. q and v are numbers or lists of numbers.
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Tuple

GRID_SLACK = 1e-9  # relative slack in the step count against rounding of (T - t0)/h


@dataclass
class VerletResult:
    """Final time, position and velocity, step count, force evaluations, optional path."""
    t: Any
    q: Any
    v: Any
    steps: int
    force_evals: int
    path: List[Tuple[Any, Any, Any]] = field(default_factory=list)


def _axpy(x, alpha, y):
    """x + alpha y for numbers or lists."""
    if isinstance(x, list):
        return [xi + alpha * yi for xi, yi in zip(x, y)]
    return x + alpha * y


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


def verlet_step(acc: Callable[[Any], Any], q: Any, v: Any, a: Any, h: Any):
    """One kick-drift-kick step; a = acc(q) is passed in. Returns (q_new, v_new, a_new)."""
    v_half = _axpy(v, h / 2, a)  # @line L6
    q_new = _axpy(q, h, v_half)  # @line L7
    a_new = acc(q_new)  # @line L8
    v_new = _axpy(v_half, h / 2, a_new)  # @line L9
    return q_new, v_new, a_new


def velocity_verlet(acc: Callable[[Any], Any], t0: Any, q0: Any, v0: Any, t_end: Any, h: Any,
                    keep_path: bool = False) -> VerletResult:
    """Integrate q'' = acc(q) from t0 to t_end with steps h; the last step ends exactly at t_end.

    A shortened last step keeps second order but is a different map; for long runs choose h
    so that (t_end - t0)/h is an integer.
    """
    N = step_count(t0, t_end, h)  # @line L1
    q, v, t = q0, v0, t0  # @line L2
    a = acc(q)  # @line L3
    evals = 1
    path = [(t, q, v)] if keep_path else []
    for n in range(N):  # @line L4
        t_next = t_end if n == N - 1 else t0 + (n + 1) * h  # @line L5
        q, v, a = verlet_step(acc, q, v, a, t_next - t)
        evals += 1
        t = t_next  # @line L10
        if keep_path:
            path.append((t, q, v))
    return VerletResult(t, q, v, N, evals, path)  # @line L11


def stormer_positions(acc: Callable[[Any], Any], q0: Any, v0: Any, h: Any, n: int) -> List[Any]:
    """The two-step form q_(k+1) = 2 q_k - q_(k-1) + h^2 a(q_k), started with
    q_1 = q_0 + h v_0 + (h^2/2) a(q_0). Returns q_0..q_n; equals the Verlet positions."""
    if n < 0:
        raise ValueError("n must not be negative")
    qs = [q0]
    if n == 0:
        return qs
    qs.append(_axpy(_axpy(q0, h, v0), h * h / 2, acc(q0)))
    for k in range(1, n):
        qs.append(_axpy(_axpy(qs[k], -1, qs[k - 1]), 1, _axpy(qs[k], h * h, acc(qs[k]))))
    return qs


def oscillator_matrix(h: Any, w: Any) -> List[List[Any]]:
    """The one-step matrix of velocity Verlet for q'' = -w^2 q acting on (q, v)."""
    z = h * w
    return [[1 - z * z / 2, h], [-h * w * w * (1 - z * z / 4), 1 - z * z / 2]]
