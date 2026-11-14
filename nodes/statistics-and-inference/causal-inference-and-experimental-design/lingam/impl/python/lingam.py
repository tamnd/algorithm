# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lingam/. The authors are listed in prov/YZF859.jsonl.
"""DirectLiNGAM: the causal order of a linear non-Gaussian acyclic model.

The model is x = B x + e, where B is the weight matrix of a DAG and the
components of e are independent and non-Gaussian. DirectLiNGAM (Shimizu et
al. 2011) finds an exogenous variable, regresses it out of the others, and
repeats. To find the exogenous variable this module uses the pairwise
likelihood ratio of Hyvarinen and Smith (2013) with their entropy
approximation, as many implementations do. After the order is known, each
variable is regressed on the earlier ones and small coefficients are set to 0.

Data are given as a dict: variable name -> list of floats (one per sample).
"""

import math
from typing import NamedTuple

K1, K2, GAMMA = 79.047, 7.4129, 0.37457


class LiNGAMResult(NamedTuple):
    order: list   # causal order, causes first
    b: dict       # (cause, effect) -> estimated weight, only kept weights


def mean(u):
    return sum(u) / len(u)


def standardize(u):
    m = mean(u)
    c = [x - m for x in u]
    s = math.sqrt(sum(x * x for x in c) / len(c))
    return [x / s for x in c]


def residual(xi, xj):
    """Residual of xi after least-squares regression on xj (both centred)."""
    b = sum(a * c for a, c in zip(xi, xj)) / sum(c * c for c in xj)
    return [a - b * c for a, c in zip(xi, xj)]


def entropy(u):
    """Approximate differential entropy of a standardized sample (Hyvarinen 1998
    maximum entropy approximation, constants as in Hyvarinen and Smith 2013)."""
    n = len(u)
    lc = sum(abs(x) + math.log1p(math.exp(-2 * abs(x))) - math.log(2) for x in u) / n  # log cosh
    ge = sum(x * math.exp(-x * x / 2) for x in u) / n
    return (1 + math.log(2 * math.pi)) / 2 - K1 * (lc - GAMMA) ** 2 - K2 * ge ** 2


def likelihood_ratio(xi, xj):
    """R(i, j): positive when the model xi -> xj fits better than xj -> xi."""
    ri_j = standardize(residual(xi, xj))
    rj_i = standardize(residual(xj, xi))
    return entropy(xj) + entropy(ri_j) - entropy(xi) - entropy(rj_i)


def causal_order(data):
    """The DirectLiNGAM search for a causal order."""
    x = {v: standardize(col) for v, col in data.items()}
    left = sorted(x)  # @line L1
    order = []
    while len(left) > 1:  # @line L2
        score = {i: 0.0 for i in left}  # @line L3
        for a in range(len(left)):  # @line L4
            for c in range(a + 1, len(left)):  # @line L5
                i, j = left[a], left[c]
                r = likelihood_ratio(x[i], x[j])
                score[i] += min(0.0, r) ** 2  # @line L6
                score[j] += min(0.0, -r) ** 2
        m = min(left, key=lambda v: (score[v], v))  # @line L7
        order.append(m)
        for j in left:
            if j != m:
                x[j] = standardize(residual(x[j], x[m]))  # @line L8
        left.remove(m)  # @line L9
    order.extend(left)  # @line L10
    return order


def solve(a, rhs):
    """Solve a small linear system by Gaussian elimination with pivoting."""
    k = len(rhs)
    m = [row[:] + [r] for row, r in zip(a, rhs)]
    for i in range(k):
        p = max(range(i, k), key=lambda r: abs(m[r][i]))
        m[i], m[p] = m[p], m[i]
        for r in range(i + 1, k):
            f = m[r][i] / m[i][i]
            for c in range(i, k + 1):
                m[r][c] -= f * m[i][c]
    out = [0.0] * k
    for i in reversed(range(k)):
        out[i] = (m[i][k] - sum(m[i][j] * out[j] for j in range(i + 1, k))) / m[i][i]
    return out


def fit_weights(data, order, threshold=0.1):
    """Least squares of each variable on the earlier ones; drop |b| < threshold."""
    cen = {v: [x - mean(col) for x in col] for v, col in data.items()}

    def dot(u, w):
        return sum(p * q for p, q in zip(u, w)) / len(u)

    b = {}
    for t, y in enumerate(order):
        preds = order[:t]
        if not preds:
            continue
        coef = solve([[dot(cen[p], cen[q]) for q in preds] for p in preds], [dot(cen[p], cen[y]) for p in preds])
        for p, c in zip(preds, coef):
            if abs(c) >= threshold:
                b[(p, y)] = c
    return b


def direct_lingam(data, threshold=0.1):
    order = causal_order(data)
    b = fit_weights(data, order, threshold)  # @line L11
    return LiNGAMResult(order, b)  # @line L12


def simulate(order, weights, n, rng, noise):
    """Samples of x = B x + e; weights maps (cause, effect) -> float, order is
    a causal order, noise(rng) draws one error with mean 0 and variance 1."""
    data = {v: [] for v in order}
    for _ in range(n):
        x = {}
        for v in order:
            x[v] = noise(rng) + sum(w * x[p] for (p, c), w in weights.items() if c == v)
            data[v].append(x[v])
    return data


def uniform_noise(rng):
    return rng.uniform(-math.sqrt(3), math.sqrt(3))


def gaussian_noise(rng):
    return rng.gauss(0.0, 1.0)


if __name__ == "__main__":
    import random
    rng = random.Random(1)
    w = {("A", "B"): 0.8, ("A", "C"): 0.7, ("B", "D"): 0.6, ("C", "D"): 0.6, ("D", "E"): 0.9}
    data = simulate(["A", "B", "C", "D", "E"], w, 1000, rng, uniform_noise)
    # Present the variables in a scrambled order to show the order is found from data.
    data = {v: data[v] for v in ["E", "C", "A", "D", "B"]}
    res = direct_lingam(data)
    print(res.order, {k: round(v, 2) for k, v in sorted(res.b.items())})
