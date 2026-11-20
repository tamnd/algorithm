# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-interpolation-method/. The authors are listed in prov/003ET5.jsonl.
"""The empirical interpolation method (EIM) of Barrault, Maday, Nguyen and Patera.

A parametrized function g(x; mu) is sampled on a grid of points x (the grid stands for the
domain, and the sup norm is the max over the grid). The offline stage chooses parameters
mu_1..mu_M, magic points x_1..x_M and basis functions q_1..q_M by a greedy loop. The online
stage needs the M values g(x_i; mu) only, and solves a lower triangular system.
"""

from typing import Callable

Vector = list[float]


def sup_norm(v: Vector) -> float:
    return max(abs(t) for t in v)


def argmax_abs(v: Vector) -> int:
    """Index of the largest |v_i|; ties go to the first index."""
    best = 0
    for i in range(1, len(v)):
        if abs(v[i]) > abs(v[best]):
            best = i
    return best


def forward_solve(b: list[Vector], rhs: Vector) -> Vector:
    """Solve the lower triangular system b c = rhs (b has a unit diagonal)."""
    c: Vector = []
    for i in range(len(rhs)):
        c.append((rhs[i] - sum(b[i][j] * c[j] for j in range(i))) / b[i][i])
    return c


class EIM:
    """The output of the offline stage: parameters, magic point indices, basis and the matrix B."""

    def __init__(self) -> None:
        self.mus: list[float] = []
        self.pts: list[int] = []  # indices of the magic points in the grid
        self.q: list[Vector] = []  # basis functions on the grid
        self.b: list[Vector] = []  # b[i][j] = q_j(x_i), lower triangular with a unit diagonal

    def coefficients(self, values: Vector) -> Vector:
        """Coefficients of the interpolant from the values at the magic points."""
        return forward_solve(self.b, values)

    def interpolate(self, gvec: Vector) -> Vector:
        """I_M g on the grid, for a function given on the grid (only its magic point values are used)."""
        c = self.coefficients([gvec[i] for i in self.pts])
        return [sum(cj * qj[k] for cj, qj in zip(c, self.q)) for k in range(len(gvec))]

    def lebesgue_constant(self) -> float:
        """max over the grid of sum_j |l_j(x)|, with the Lagrange functions l_j(x_i) = delta_ij."""
        m = len(self.q)
        lag = []
        for j in range(m):
            e = [1.0 if i == j else 0.0 for i in range(m)]
            c = forward_solve(self.b, e)
            lag.append([sum(ck * qk[x] for ck, qk in zip(c, self.q)) for x in range(len(self.q[0]))])
        return max(sum(abs(l[x]) for l in lag) for x in range(len(self.q[0])))


def eim_offline(g: Callable[[float, float], float], xs: Vector, train: list[float], tol: float, m_max: int) -> tuple[EIM, list[float]]:
    """Run the greedy loop. Return the EIM data and the list err_0, err_1, ... of the largest
    sup norm error over train after M = 0, 1, ... terms (err_0 = max ||g(.; mu)||)."""
    snaps = [[g(x, mu) for x in xs] for mu in train]
    eim = EIM()
    errs: list[float] = []
    res = [list(s) for s in snaps]  # @line L1: residuals g - I_M g on the grid; I_0 g = 0
    while True:
        norms = [sup_norm(r) for r in res]  # @line L2: the error of every training function
        k = max(range(len(train)), key=lambda i: norms[i])  # @line L3
        errs.append(norms[k])
        if norms[k] <= tol or len(eim.q) >= m_max:  # @line L4
            return eim, errs  # @line L5
        r = res[k]  # @line L6: the residual at the chosen parameter
        p = argmax_abs(r)  # @line L7: the new magic point
        qn = [t / r[p] for t in r]  # @line L8
        eim.mus.append(train[k])
        for i in range(len(eim.b)):  # @line L9: extend B by a row; the new column is 0 above the diagonal
            eim.b[i].append(0.0)
        eim.b.append([qj[p] for qj in eim.q] + [1.0])
        eim.pts.append(p)
        eim.q.append(qn)
        # @line L10: residuals of all training functions for the new interpolant
        res =[[a - b for a, b in zip(s, eim.interpolate(s))] for s in snaps]
