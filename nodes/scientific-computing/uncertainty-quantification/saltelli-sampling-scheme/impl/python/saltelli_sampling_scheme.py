# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/saltelli-sampling-scheme/. The authors are listed in prov/SEW99Y.jsonl.
"""First order and total Sobol indices by the Saltelli sampling scheme.

Two independent N by d sample matrices A and B give d more matrices AB_i:
the matrix A with its column i taken from B. The model runs on all rows of A,
B and AB_1, ..., AB_d, which is N (d + 2) runs. The estimators are those of
Saltelli et al. 2010: the first order numerator

    V_i = (1/N) sum_j f(B)_j (f(AB_i)_j - f(A)_j)

and the total numerator of Jansen 1999

    VT_i = (1/(2N)) sum_j (f(A)_j - f(AB_i)_j)^2,

both divided by the sample variance of the 2N values f(A) and f(B).

The inputs must be independent. The caller gives the map from the unit cube
to the input law, one coordinate at a time.
"""

import math
import random
from typing import Callable, Sequence

Model = Callable[[Sequence[float]], float]


def ishigami(x: Sequence[float], a: float = 7.0, b: float = 0.1) -> float:
    """The Ishigami function sin x1 + a sin^2 x2 + b x3^4 sin x1, inputs uniform on [-pi, pi]^3."""
    return math.sin(x[0]) + a * math.sin(x[1]) ** 2 + b * x[2] ** 4 * math.sin(x[0])


def ishigami_exact(a: float = 7.0, b: float = 0.1) -> dict:
    """The exact mean, variance, first order and total indices of the Ishigami function."""
    pi = math.pi
    v1 = 0.5 * (1 + b * pi**4 / 5) ** 2
    v2 = a * a / 8
    v13 = b * b * pi**8 * (1 / 18 - 1 / 50)
    v = v1 + v2 + v13
    return {
        "mean": a / 2,
        "variance": v,
        "S": [v1 / v, v2 / v, 0.0],
        "ST": [(v1 + v13) / v, v2 / v, v13 / v],
    }


def saltelli(f: Model, d: int, n: int, rng: random.Random, to_input: Callable[[float, int], float]) -> dict:
    """Estimate S_i and ST_i for i = 1..d with N (d + 2) model runs.

    to_input(u, i) maps a uniform number u in [0, 1) to coordinate i of the input.
    Returns the indices, their standard errors (with the variance taken as exact)
    and the number of model runs.
    """
    a = [[to_input(rng.random(), i) for i in range(d)] for _ in range(n)]  # @line L1
    b = [[to_input(rng.random(), i) for i in range(d)] for _ in range(n)]
    fa = [f(row) for row in a]  # @line L2
    fb = [f(row) for row in b]
    runs = 2 * n
    both = fa + fb
    mean = sum(both) / (2 * n)
    var = sum((y - mean) ** 2 for y in both) / (2 * n - 1)  # @line L3
    s, st, s_err, st_err = [], [], [], []
    for i in range(d):  # @line L4
        fab = []
        for j in range(n):
            row = list(a[j])  # @line L5
            row[i] = b[j][i]
            fab.append(f(row))  # @line L6
        runs += n
        t1 = [fb[j] * (fab[j] - fa[j]) for j in range(n)]  # @line L7
        t2 = [0.5 * (fa[j] - fab[j]) ** 2 for j in range(n)]  # @line L8
        s.append(sum(t1) / n / var)  # @line L9
        st.append(sum(t2) / n / var)
        s_err.append(_std_error(t1) / var)
        st_err.append(_std_error(t2) / var)
    sq = [((y - mean) ** 2 - var) ** 2 for y in both]
    var_rel_err = math.sqrt(sum(sq) / (2 * n - 1) / (2 * n)) / var
    return {"S": s, "ST": st, "S_err": s_err, "ST_err": st_err, "runs": runs, "variance": var, "variance_rel_err": var_rel_err}  # @line L10


def _std_error(t: Sequence[float]) -> float:
    n = len(t)
    m = sum(t) / n
    return math.sqrt(sum((x - m) ** 2 for x in t) / (n - 1) / n)


def brute_force_first_order(f: Model, d: int, i: int, n_outer: int, n_inner: int, rng: random.Random, to_input) -> float:
    """Var(E[Q | x_i]) by a double loop: n_outer values of x_i, n_inner samples of the rest for each.

    The inner means carry noise of variance about Var(Q | x_i) / n_inner, which this subtracts.
    """
    cond_means, cond_vars = [], []
    for _ in range(n_outer):
        xi = to_input(rng.random(), i)
        ys = []
        for _ in range(n_inner):
            x = [to_input(rng.random(), k) for k in range(d)]
            x[i] = xi
            ys.append(f(x))
        m = sum(ys) / n_inner
        cond_means.append(m)
        cond_vars.append(sum((y - m) ** 2 for y in ys) / (n_inner - 1))
    mm = sum(cond_means) / n_outer
    var_of_means = sum((m - mm) ** 2 for m in cond_means) / (n_outer - 1)
    return var_of_means - sum(cond_vars) / n_outer / n_inner
