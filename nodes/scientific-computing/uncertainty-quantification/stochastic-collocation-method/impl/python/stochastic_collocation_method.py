# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-collocation-method/. The authors are listed in prov/S37CZP.jsonl.
"""Stochastic collocation on a Smolyak sparse grid of nested Clenshaw-Curtis nodes.

The inputs xi_1..xi_d are independent and uniform on [-1, 1]. The 1D rule of
level l has m(0) = 1 node (the midpoint) and m(l) = 2^l + 1 nodes
x_j = -cos(pi j / 2^l) for l >= 1; the levels are nested. The Smolyak
surrogate of level L is the combination

    A_L = sum over l in N^d with L - d + 1 <= |l| <= L of
          (-1)^(L - |l|) binom(d - 1, L - |l|) U_(l_1) x ... x U_(l_d),

where U_l is Lagrange interpolation on the level l nodes. The model runs
once at each distinct node of the union of the tensor grids. The mean and
variance come from the matching sparse quadrature: E[q] ~ Q_L[q] and
Var[q] ~ Q_L[q^2] - Q_L[q]^2.
"""

import itertools
import math
from fractions import Fraction
from typing import Callable

Model = Callable[[list[float]], float]


def level_keys(level: int) -> list[Fraction]:
    """Nodes of a level as exact fractions t of pi, with node -cos(pi t); nested across levels."""
    if level == 0:
        return [Fraction(1, 2)]
    n = 2**level
    return [Fraction(j, n) for j in range(n + 1)]


def node(key: Fraction) -> float:
    """The node -cos(pi t) for the key t, with exact 0 and +-1."""
    if key == Fraction(1, 2):
        return 0.0
    if key == 0:
        return -1.0
    if key == 1:
        return 1.0
    return -math.cos(math.pi * key)


def cc_weights(level: int) -> list[float]:
    """Clenshaw-Curtis weights of a level for the uniform probability law on [-1, 1] (they sum to 1)."""
    if level == 0:
        return [1.0]
    n = 2**level
    w = []
    for j in range(n + 1):
        theta = math.pi * j / n
        s = 0.0
        for k in range(1, n // 2 + 1):
            b = 1.0 if 2 * k == n else 2.0
            s += b * math.cos(2 * k * theta) / (4 * k * k - 1)
        c = 1.0 if j in (0, n) else 2.0
        w.append(0.5 * c / n * (1.0 - s))
    return w


def lagrange(xs: list[float], x: float) -> list[float]:
    """Values at x of the Lagrange basis polynomials on the nodes xs."""
    out = []
    for i, xi in enumerate(xs):
        v = 1.0
        for j, xj in enumerate(xs):
            if j != i:
                v *= (x - xj) / (xi - xj)
        out.append(v)
    return out


def smolyak_terms(d: int, level: int) -> list[tuple[int, tuple[int, ...]]]:
    """The pairs (coefficient, level multi-index) of the combination formula."""
    terms = []
    for lv in itertools.product(range(level + 1), repeat=d):
        s = sum(lv)
        if level - d + 1 <= s <= level:
            coef = (-1) ** (level - s) * math.comb(d - 1, level - s)
            terms.append((coef, lv))
    return terms


def collocate(q: Model, d: int, level: int) -> dict:
    """Run the model on the sparse grid and return the surrogate data."""
    terms = smolyak_terms(d, level)  # @line L1
    grid = {}
    for _, lv in terms:  # @line L2
        for keys in itertools.product(*(level_keys(v) for v in lv)):
            grid.setdefault(keys, None)
    for keys in grid:  # @line L3
        grid[keys] = q([node(k) for k in keys])
    return {"d": d, "level": level, "terms": terms, "values": grid}


def evaluate(sc: dict, x: list[float]) -> float:
    """The Smolyak surrogate A_L at the point x."""
    total = 0.0
    for coef, lv in sc["terms"]:  # @line L4
        keys = [level_keys(v) for v in lv]
        basis = [lagrange([node(k) for k in ks], xk) for ks, xk in zip(keys, x)]
        for pick in itertools.product(*(range(len(ks)) for ks in keys)):
            y = sc["values"][tuple(keys[k][j] for k, j in enumerate(pick))]
            total += coef * y * math.prod(basis[k][j] for k, j in enumerate(pick))
    return total


def quadrature_weights(sc: dict) -> dict:
    """The sparse quadrature weight of each distinct node; the surrogate's mean is sum w y."""
    weights = {}
    for coef, lv in sc["terms"]:
        keys = [level_keys(v) for v in lv]
        ws = [cc_weights(v) for v in lv]
        for pick in itertools.product(*(range(len(ks)) for ks in keys)):
            key = tuple(keys[k][j] for k, j in enumerate(pick))
            weights[key] = weights.get(key, 0.0) + coef * math.prod(ws[k][j] for k, j in enumerate(pick))
    return weights


def moments(sc: dict) -> tuple[float, float]:
    """Mean Q_L[q] and variance Q_L[q^2] - Q_L[q]^2 from the sparse quadrature."""
    w = quadrature_weights(sc)  # @line L5
    mean = sum(w[k] * y for k, y in sc["values"].items())
    second = sum(w[k] * y * y for k, y in sc["values"].items())
    return mean, second - mean * mean  # @line L6


def ishigami(x: list[float], a: float = 7.0, b: float = 0.1) -> float:
    """The Ishigami function with inputs xi_k uniform on [-1, 1], mapped to pi xi_k."""
    x1, x2, x3 = (math.pi * v for v in x)
    return math.sin(x1) + a * math.sin(x2) ** 2 + b * x3**4 * math.sin(x1)
