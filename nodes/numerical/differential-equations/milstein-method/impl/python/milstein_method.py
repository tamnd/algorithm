# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/milstein-method/. The authors are listed in prov/C27YYP.jsonl.

"""The Milstein method for the Ito SDE dX = a(t, X) dt + b(t, X) dW.

One step from (t_n, X_n) with step h_n and Brownian increment dW_n:

    X_(n+1) = X_n + a h_n + b dW_n + (1/2) b b' (dW_n^2 - h_n)

where b' is the derivative of b with respect to x.  X may be a scalar or a
list; for a list the noise is diagonal: component i is driven by its own
Brownian motion W_i, and b_i and db_i depend on x_i only through the
derivative db_i = d b_i / d x_i (this is commutative noise, the case where
the scheme needs no iterated Ito integrals).

scheme="euler" drops the correction (Euler-Maruyama); scheme="platen" is the
derivative-free Runge-Kutta variant that replaces b b' by a difference of b.
"""

import math
import random
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Optional, Sequence

GRID_SLACK = 1e-9


@dataclass
class SDEResult:
    """Final time and value, steps taken, evaluations of a, b and db."""

    t: Any
    x: Any
    steps: int
    a_evals: int
    b_evals: int
    db_evals: int
    path: List[Any] = field(default_factory=list)


def step_count(t0: Any, t_end: Any, h: Any) -> int:
    """The number of steps of length at most h (up to GRID_SLACK) from t0 to t_end."""
    if not h > 0:
        raise ValueError("the step size h must be positive")
    if t_end < t0:
        raise ValueError("t_end must not be before t0")
    r = (t_end - t0) / h
    if isinstance(r, (int, Fraction)):
        return math.ceil(r)
    return max(0, math.ceil(r - GRID_SLACK * max(1.0, r)))


def _map(fn, *args):
    if isinstance(args[0], list):
        return [fn(*xs) for xs in zip(*args)]
    return fn(*args)


def _sqrt(h: Any) -> Any:
    return math.sqrt(h)


def milstein_step(a_val: Any, b_val: Any, db_val: Any, x: Any, h: Any, dw: Any) -> Any:
    """One Milstein step from the values a, b, b' at (t_n, X_n)."""
    return _map(lambda xi, ai, bi, di, wi: xi + ai * h + bi * wi + bi * di * (wi * wi - h) / 2,
                x, a_val, b_val, db_val, dw)


def milstein(a: Callable[[Any, Any], Any], b: Callable[[Any, Any], Any],
             db: Optional[Callable[[Any, Any], Any]], x0: Any, t0: Any, t_end: Any,
             h: Any, rng: Optional[random.Random] = None,
             dW: Optional[Sequence[Any]] = None, scheme: str = "milstein",
             keep_path: bool = False) -> SDEResult:
    """Integrate dX = a dt + b dW from t0 to t_end with steps of length h.

    The increments are taken from dW (one per step, scalar or list like x0)
    or drawn as sqrt(h_n) N(0, 1) from rng.  The last step is shortened so
    that it ends exactly at t_end.
    """
    if scheme not in ("milstein", "euler", "platen"):
        raise ValueError("unknown scheme " + repr(scheme))
    if scheme == "milstein" and db is None:
        raise ValueError("the Milstein scheme needs db = d b / d x")
    N = step_count(t0, t_end, h)                         # @line L1
    if dW is not None and len(dW) < N:
        raise ValueError("need one Brownian increment per step")
    if dW is None and rng is None and N > 0:
        raise ValueError("give either rng or dW")
    vec = isinstance(x0, list)
    t, x = t0, (list(x0) if vec else x0)                 # @line L2
    na = nb = nd = 0
    path = [(t, x)] if keep_path else []
    for n in range(N):                                   # @line L3
        t_next = t_end if n == N - 1 else t0 + (n + 1) * h
        hn = t_next - t                                  # @line L4
        if dW is not None:                               # @line L5
            dw = dW[n]
        else:
            s = _sqrt(hn)
            dw = [rng.gauss(0.0, 1.0) * s for _ in x] if vec else rng.gauss(0.0, 1.0) * s
        av = a(t, x)                                     # @line L6
        bv = b(t, x)
        na += 1
        nb += 1
        if scheme == "milstein":
            dv = db(t, x)                                # @line L7
            nd += 1
            x = milstein_step(av, bv, dv, x, hn, dw)     # @line L8
        elif scheme == "euler":
            x = _map(lambda xi, ai, bi, wi: xi + ai * hn + bi * wi, x, av, bv, dw)
        else:
            s = _sqrt(hn)
            ups = _map(lambda xi, ai, bi: xi + ai * hn + bi * s, x, av, bv)
            bu = b(t, ups)
            nb += 1
            x = _map(lambda xi, ai, bi, ui, wi: xi + ai * hn + bi * wi + (ui - bi) * (wi * wi - hn) / (2 * s),
                     x, av, bv, bu, dw)
        t = t_next                                       # @line L9
        if keep_path:
            path.append((t, x))
    return SDEResult(t, x, N, na, nb, nd, path)          # @line L10


def brownian_increments(rng: random.Random, T: float, n_fine: int) -> List[float]:
    """n_fine independent N(0, T/n_fine) increments of one Brownian path."""
    s = math.sqrt(T / n_fine)
    return [rng.gauss(0.0, 1.0) * s for _ in range(n_fine)]


def coarsen(dw: Sequence[Any], factor: int) -> List[Any]:
    """Sum consecutive groups of `factor` increments (the same path, coarser grid)."""
    return [sum(dw[i:i + factor]) for i in range(0, len(dw), factor)]
