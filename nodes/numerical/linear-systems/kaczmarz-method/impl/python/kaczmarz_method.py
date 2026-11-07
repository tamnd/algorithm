# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kaczmarz-method/. The authors are listed in prov/3ES5VF.jsonl.

"""The Kaczmarz method (cyclic or randomized) for A x = b, A of size m by n.

Each step projects the iterate onto the hyperplane of one equation. Works
with floats or with fractions.Fraction (then every projection is exact).
A is a dense list of rows or a CSR object. Standard library only.
"""

import math
import random


class CSR:
    """Compressed sparse row matrix with m rows and n columns."""

    def __init__(self, m, n, ptr, ind, data):
        self.m, self.n, self.ptr, self.ind, self.data = m, n, ptr, ind, data

    @classmethod
    def from_dense(cls, a):
        ptr, ind, data = [0], [], []
        for row in a:
            for j, v in enumerate(row):
                if v != 0:
                    ind.append(j)
                    data.append(v)
            ptr.append(len(ind))
        return cls(len(a), len(a[0]) if a else 0, ptr, ind, data)

    def row(self, i):
        """The nonzeros of row i as a list of (column, value)."""
        return [(self.ind[p], self.data[p]) for p in range(self.ptr[i], self.ptr[i + 1])]


class KaczmarzResult:
    def __init__(self, x, converged, sweeps, steps, history, status):
        self.x, self.converged, self.sweeps = x, converged, sweeps
        self.steps, self.history, self.status = steps, history, status


def _as_csr(a):
    return a if isinstance(a, CSR) else CSR.from_dense(a)


def residual(a, b, x):
    """b - A x."""
    a = _as_csr(a)
    return [b[i] - sum(v * x[j] for j, v in a.row(i)) for i in range(a.m)]


def kaczmarz(a, b, x0=None, tol=1e-10, maxit=1000, order="cyclic", seed=0,
             relax=1, trace=None):
    """Kaczmarz sweeps until ||b - A x||_2 <= tol ||b||_2 or maxit sweeps.

    order: "cyclic" (rows 0..m-1 in turn) or "random" (row i with
    probability ||a_i||^2 / ||A||_F^2, Strohmer and Vershynin). A sweep is
    m row steps. relax is the relaxation factor omega (0 < omega < 2).
    trace(step, i, x) is called after every row step (x is the live list).
    history holds ||b - A x||_2 / ||b||_2 after each sweep (as float).
    """
    a = _as_csr(a)
    m, n = a.m, a.n
    rows = [a.row(i) for i in range(m)]
    x = list(x0) if x0 is not None else [0 * b[0] if b else 0] * n  # @line L1
    nrm2 = [sum(v * v for _, v in r) for r in rows]
    total = float(sum(nrm2))
    cum, acc = [], 0.0
    for w in nrm2:
        acc += float(w)
        cum.append(acc)
    rng = random.Random(seed)
    bb = sum(v * v for v in b)
    history, steps = [], 0
    if bb == 0:
        return KaczmarzResult([0 * v for v in x], True, 0, 0, [0.0], "converged")
    for sweep in range(1, maxit + 1):  # @line L2
        for t in range(m):  # @line L3
            if order == "random":  # @line L4
                if total == 0:
                    break
                u = rng.random() * total
                lo, hi = 0, m - 1
                while lo < hi:
                    mid = (lo + hi) // 2
                    if cum[mid] > u:
                        hi = mid
                    else:
                        lo = mid + 1
                i = lo
            else:
                i = t
            if nrm2[i] == 0:  # @line L5
                continue
            delta = relax * (b[i] - sum(v * x[j] for j, v in rows[i])) / nrm2[i]  # @line L6
            for j, v in rows[i]:
                x[j] += delta * v  # @line L7
            steps += 1
            if trace is not None:
                trace(steps, i, x)
        r = residual(a, b, x)  # @line L8
        rr = sum(v * v for v in r)
        history.append(math.sqrt(float(rr) / float(bb)))
        if rr <= tol * tol * bb:  # @line L9
            return KaczmarzResult(x, True, sweep, steps, history, "converged")
    return KaczmarzResult(x, False, maxit, steps, history, "maxit")  # @line L10
