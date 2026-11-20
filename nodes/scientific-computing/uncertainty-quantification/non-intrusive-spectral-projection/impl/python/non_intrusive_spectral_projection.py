# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-intrusive-spectral-projection/. The authors are listed in prov/K2M34Y.jsonl.
"""Non-intrusive spectral projection (pseudospectral projection) of a model output.

The input xi = (xi_1..xi_d) has independent components. Each component is
"uniform" (on [-1, 1], with the orthonormal Legendre basis sqrt(2n+1) P_n)
or "normal" (standard normal, with the orthonormal probabilists' Hermite basis
He_n / sqrt(n!)). The coefficient of Psi_a in the expansion of q(xi) is the
projection c_a = E[q Psi_a], and this code evaluates it with a tensor Gauss
rule of m points per input. The Gauss rules come from the Golub-Welsch
method: the nodes are the eigenvalues of the Jacobi matrix of the
recurrence, and the weights are the squared first components of its unit
eigenvectors. The eigenvalues are computed by the cyclic Jacobi method.
"""

import itertools
import math
from typing import Callable

Model = Callable[[list[float]], float]


def jacobi_eigen(a: list[list[float]], tol: float = 1e-15, max_sweeps: int = 100) -> tuple[list[float], list[list[float]]]:
    """Eigenvalues and unit eigenvectors (columns of V) of a symmetric matrix, by cyclic Jacobi rotations."""
    n = len(a)
    m = [list(map(float, row)) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off <= tol * tol * max(1.0, sum(m[i][i] ** 2 for i in range(n))):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p] = c * mkp - s * mkq
                    m[k][q] = s * mkp + c * mkq
                for k in range(n):
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k] = c * mpk - s * mqk
                    m[q][k] = s * mpk + c * mqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    return [m[i][i] for i in range(n)], v


def recurrence_offdiag(family: str, k: int) -> float:
    """b_k in x psi_(k-1) = b_k psi_k + b_(k-1) psi_(k-2) for the orthonormal family."""
    if family == "uniform":
        return k / math.sqrt((2 * k - 1) * (2 * k + 1))
    if family == "normal":
        return math.sqrt(k)
    raise ValueError("family must be 'uniform' or 'normal'")


def gauss_rule(family: str, m: int) -> tuple[list[float], list[float]]:
    """The m point Gauss rule for the probability law of the family (weights sum to 1), sorted by node."""
    jac = [[0.0] * m for _ in range(m)]
    for k in range(1, m):
        jac[k - 1][k] = jac[k][k - 1] = recurrence_offdiag(family, k)
    vals, vecs = jacobi_eigen(jac)
    pairs = sorted((vals[j], vecs[0][j] ** 2) for j in range(m))
    return [x for x, _ in pairs], [w for _, w in pairs]


def basis_1d(family: str, x: float, p: int) -> list[float]:
    """psi_0(x)..psi_p(x), orthonormal for the law of the family."""
    vals = [1.0]
    if p >= 1:
        vals.append(x / recurrence_offdiag(family, 1))
    for k in range(2, p + 1):
        bk, bk1 = recurrence_offdiag(family, k), recurrence_offdiag(family, k - 1)
        vals.append((x * vals[k - 1] - bk1 * vals[k - 2]) / bk)
    return vals


def total_degree_set(d: int, p: int) -> list[tuple[int, ...]]:
    """All a in N^d with |a| <= p, sorted by total degree; the zero index is first."""
    out = [a for a in itertools.product(range(p + 1), repeat=d) if sum(a) <= p]
    out.sort(key=lambda a: (sum(a), [-v for v in a]))
    return out


def nisp(q: Model, families: list[str], p: int, m: int) -> tuple[list[tuple[int, ...]], list[float], int]:
    """Coefficients c_a = sum_j w_j q(x_j) Psi_a(x_j) on the tensor Gauss grid; returns (index, coeffs, runs)."""
    d = len(families)
    rules = [gauss_rule(fam, m) for fam in families]  # @line L1
    index = total_degree_set(d, p)  # @line L2
    coeffs = [0.0] * len(index)
    runs = 0
    for pick in itertools.product(range(m), repeat=d):  # @line L3
        x = [rules[k][0][j] for k, j in enumerate(pick)]
        w = math.prod(rules[k][1][j] for k, j in enumerate(pick))
        y = q(x)  # @line L4
        runs += 1
        tables = [basis_1d(families[k], x[k], p) for k in range(d)]
        for i, a in enumerate(index):  # @line L5
            coeffs[i] += w * y * math.prod(tables[k][a[k]] for k in range(d))
    return index, coeffs, runs  # @line L6


def mean_variance(coeffs: list[float]) -> tuple[float, float]:
    """Mean c_0 and variance sum_{a != 0} c_a^2 of an orthonormal expansion."""
    return coeffs[0], sum(c * c for c in coeffs[1:])


def sobol_from_coefficients(index: list[tuple[int, ...]], coeffs: list[float]) -> tuple[list[float], list[float]]:
    """First order and total Sobol indices of an orthonormal expansion (Sudret 2008)."""
    d = len(index[0])
    _, var = mean_variance(coeffs)
    first = [0.0] * d
    total = [0.0] * d
    for a, c in zip(index, coeffs):
        active = [k for k in range(d) if a[k] > 0]
        if len(active) == 1:
            first[active[0]] += c * c
        for k in active:
            total[k] += c * c
    return [s / var for s in first], [s / var for s in total]


def evaluate(index: list[tuple[int, ...]], coeffs: list[float], families: list[str], x: list[float]) -> float:
    """The expansion sum_a c_a Psi_a(x)."""
    p = max(sum(a) for a in index)
    tables = [basis_1d(families[k], x[k], p) for k in range(len(x))]
    return sum(c * math.prod(tables[k][a[k]] for k in range(len(x))) for a, c in zip(index, coeffs))


def ishigami(x: list[float], a: float = 7.0, b: float = 0.1) -> float:
    """The Ishigami function with inputs xi_k uniform on [-1, 1], mapped to pi xi_k."""
    x1, x2, x3 = (math.pi * v for v in x)
    return math.sin(x1) + a * math.sin(x2) ** 2 + b * x3**4 * math.sin(x1)
