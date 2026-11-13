# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fixed-point-quantum-search/. The authors are listed in prov/33JPWY.jsonl.
"""Fixed-point quantum search on the qs1 state-vector simulator.

The main function fixed_point_search is Grover's pi/3 recursion (2005).
The functions ylc_* are the optimal fixed-point search of Yoder, Low and
Chuang (2014), a variant on the page. The search space is {0, 1, ..., N - 1},
f(x) is 1 for a marked item, and lam = M / N is the unknown fraction of
marked items. Qubit 0 is the least significant bit of x.
"""

import cmath
import math
import random
from typing import Callable, Optional

from qsim import apply_diagonal, probabilities, sample

Oracle = Callable[[int], int]

OMEGA = cmath.exp(1j * math.pi / 3.0)


def num_qubits(n_items: int) -> int:
    if n_items < 1:
        raise ValueError("n_items must be at least 1")
    return max(1, (n_items - 1).bit_length())


def uniform_state(n_items: int) -> list[complex]:
    amp = 1.0 / math.sqrt(n_items)
    return [amp + 0j if x < n_items else 0j for x in range(1 << num_qubits(n_items))]


def r_target(state: list[complex], n_items: int, f: Oracle, ph: complex) -> None:
    """R_t = I - (1 - ph) P: multiply each marked item by ph. One query."""
    apply_diagonal(state, lambda x: ph if x < n_items and f(x) else 1.0)


def r_start(state: list[complex], n_items: int, ph: complex) -> None:
    """R_s = I - (1 - ph) |s><s|. No query."""
    c = 1.0 - ph
    mean = sum(state[:n_items]) / n_items
    for x in range(n_items):
        state[x] = state[x] - c * mean


def choose_depth(w_min: float, eps: float) -> int:
    """The smallest n with (1 - w_min)^(3^n) <= eps."""
    if not 0.0 < w_min <= 1.0 or not 0.0 < eps < 1.0:
        raise ValueError("need 0 < w_min <= 1 and 0 < eps < 1")
    depth = 0
    while (1.0 - w_min) ** (3 ** depth) > eps:
        depth += 1
    return depth


def apply_u(state: list[complex], n_items: int, f: Oracle, k: int, adjoint: bool,
            count: list[int]) -> None:
    """Apply U_k (or U_k^dag) in place, with U_0 = I and U_k = U_(k-1) R_s U_(k-1)^dag R_t U_(k-1)."""
    if k == 0:  # @line L6
        return
    if not adjoint:  # @line L7
        apply_u(state, n_items, f, k - 1, False, count)
        r_target(state, n_items, f, OMEGA)
        count[0] += 1
        apply_u(state, n_items, f, k - 1, True, count)
        r_start(state, n_items, OMEGA)
        apply_u(state, n_items, f, k - 1, False, count)
    else:  # @line L8
        apply_u(state, n_items, f, k - 1, True, count)
        r_start(state, n_items, OMEGA.conjugate())
        apply_u(state, n_items, f, k - 1, False, count)
        r_target(state, n_items, f, OMEGA.conjugate())
        count[0] += 1
        apply_u(state, n_items, f, k - 1, True, count)


def pi3_state(n_items: int, f: Oracle, depth: int) -> tuple[list[complex], int]:
    """U_depth |s> and its number of queries, (3^depth - 1) / 2."""
    count = [0]
    state = uniform_state(n_items)
    apply_u(state, n_items, f, depth, False, count)
    return state, count[0]


def fixed_point_search(n_items: int, f: Oracle, w_min: float, eps: float,
                       rng: random.Random) -> tuple[Optional[int], int]:
    """Run FIXED-POINT-SEARCH once. Return (a marked item or None, queries).

    w_min is a known lower bound on M / N. When M / N >= w_min, the run
    fails with probability at most eps. The count of queries includes the
    classical check.
    """
    depth = choose_depth(w_min, eps)  # @line L1
    count = [0]
    state = uniform_state(n_items)  # @line L2
    apply_u(state, n_items, f, depth, False, count)  # @line L3
    x = sample(probabilities(state), rng)  # @line L4
    if f(x):  # @line L5
        return x, count[0] + 1
    return None, count[0] + 1


# The variant of Yoder, Low and Chuang.

def chebyshev(order: float, x: float) -> float:
    """T_order(x) = cos(order arccos x) for |x| <= 1, cosh(order arccosh x) for x > 1."""
    if abs(x) <= 1.0:
        return math.cos(order * math.acos(x))
    if x > 1.0:
        return math.cosh(order * math.acosh(x))
    raise ValueError("x < -1 is not needed here")


def gamma(length: int, delta: float) -> float:
    """gamma = 1 / T_(1/L)(1/delta)."""
    return 1.0 / chebyshev(1.0 / length, 1.0 / delta)


def width(length: int, delta: float) -> float:
    """w = 1 - gamma^2. For each lam >= w, the success probability is at least 1 - delta^2."""
    return 1.0 - gamma(length, delta) ** 2


def ylc_length(w_min: float, delta: float) -> int:
    """The smallest odd L with width(L, delta) <= w_min."""
    if not 0.0 < w_min <= 1.0 or not 0.0 < delta < 1.0:
        raise ValueError("need 0 < w_min <= 1 and 0 < delta < 1")
    length = 1
    while width(length, delta) > w_min:
        length += 2
    return length


def ylc_phases(length: int, delta: float) -> tuple[list[float], list[float]]:
    """alpha_j = -beta_(l-j+1) = 2 arccot(tan(2 pi j / L) sqrt(1 - gamma^2)), j = 1 .. l."""
    l = (length - 1) // 2
    s = math.sqrt(width(length, delta))
    alpha = [2.0 * math.atan2(1.0, math.tan(2.0 * math.pi * j / length) * s) for j in range(1, l + 1)]
    beta = [-alpha[l - j] for j in range(1, l + 1)]
    return alpha, beta


def ylc_predicted(length: int, delta: float, lam: float) -> float:
    """P_L = 1 - delta^2 T_L(T_(1/L)(1/delta) sqrt(1 - lam))^2."""
    x = math.sqrt(max(0.0, 1.0 - lam)) / gamma(length, delta)
    return 1.0 - delta ** 2 * chebyshev(length, x) ** 2


def ylc_state(n_items: int, f: Oracle, length: int, delta: float) -> list[complex]:
    """G(alpha_l, beta_l) ... G(alpha_1, beta_1) |s>, with G(a, b) = -S_s(a) S_t(b).

    S_t(b) = I - (1 - e^(i b)) P is one query; S_s(a) = I - (1 - e^(-i a)) |s><s|.
    """
    alpha, beta = ylc_phases(length, delta)
    state = uniform_state(n_items)
    for a, b in zip(alpha, beta):
        r_target(state, n_items, f, cmath.exp(1j * b))
        r_start(state, n_items, cmath.exp(-1j * a))
        for x in range(n_items):
            state[x] = -state[x]
    return state


def ylc_success(n_items: int, f: Oracle, length: int, delta: float) -> float:
    probs = probabilities(ylc_state(n_items, f, length, delta))
    return sum(p for x, p in enumerate(probs[:n_items]) if f(x))


def ylc_search(n_items: int, f: Oracle, w_min: float, delta: float,
               rng: random.Random) -> tuple[Optional[int], int]:
    """One run of the Yoder-Low-Chuang search. Return (a marked item or None, queries)."""
    length = ylc_length(w_min, delta)
    state = ylc_state(n_items, f, length, delta)
    x = sample(probabilities(state), rng)
    queries = (length - 1) // 2 + 1
    return (x if f(x) else None), queries
