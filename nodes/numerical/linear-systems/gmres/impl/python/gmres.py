# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gmres/. The authors are listed in prov/JYTTHH.jsonl.

"""Restarted GMRES for A x = b with a modified Gram-Schmidt Arnoldi process.

The matrix is either a dense list of rows or a CSR object; only products
A v are used. The small Hessenberg least squares problem is solved by
Givens rotations, so the residual norm of every step is known without
forming x. Standard library only.
"""

import math


class CSR:
    """Compressed sparse row matrix: row i holds data[ptr[i]:ptr[i+1]]."""

    def __init__(self, n, ptr, ind, data):
        self.n, self.ptr, self.ind, self.data = n, ptr, ind, data

    @classmethod
    def from_dense(cls, a):
        ptr, ind, data = [0], [], []
        for row in a:
            for j, v in enumerate(row):
                if v != 0:
                    ind.append(j)
                    data.append(v)
            ptr.append(len(ind))
        return cls(len(a), ptr, ind, data)

    def matvec(self, x):
        out = [0.0] * self.n
        for i in range(self.n):
            acc = 0.0
            for p in range(self.ptr[i], self.ptr[i + 1]):
                acc += self.data[p] * x[self.ind[p]]
            out[i] = acc
        return out


def _matvec(a, x):
    if isinstance(a, CSR):
        return a.matvec(x)
    return [sum(aij * xj for aij, xj in zip(row, x)) for row in a]


def _norm(v):
    s = max((abs(t) for t in v), default=0.0)
    if s == 0.0:
        return 0.0
    return s * math.sqrt(sum((t / s) ** 2 for t in v))


class GMRESResult:
    def __init__(self, x, converged, iterations, restarts, history, status):
        self.x = x
        self.converged = converged
        self.iterations = iterations  # total Arnoldi steps (matvecs inside cycles)
        self.restarts = restarts
        self.history = history  # estimated ||r_k||_2, starting with ||r_0||_2
        self.status = status  # "converged", "maxit" or "breakdown"


def gmres(a, b, x0=None, tol=1e-10, restart=None, maxit=None):
    """Solve A x = b; stop when ||r_k||_2 <= tol * ||b||_2.

    restart = m gives GMRES(m); None means full GMRES (m = n).
    maxit bounds the total number of Arnoldi steps (default 10 n).
    status "breakdown" means h_{j+1,j} = 0 with a singular Hessenberg
    block, so A is singular on the Krylov space and no solution was found.
    """
    n = len(b)
    m = n if restart is None else max(1, min(restart, n))
    maxit = 10 * n if maxit is None else maxit
    x = [0.0] * n if x0 is None else [float(t) for t in x0]
    bnorm = _norm(b)
    target = tol * (bnorm if bnorm > 0 else 1.0)
    history = []
    total = 0
    restarts = 0
    while True:
        ax = _matvec(a, x)
        r = [bi - t for bi, t in zip(b, ax)]
        beta = _norm(r)  # @line L1
        if not history:
            history.append(beta)
        if beta <= target:
            return GMRESResult(x, True, total, restarts, history, "converged")
        if total >= maxit:
            return GMRESResult(x, False, total, restarts, history, "maxit")
        v = [[t / beta for t in r]]
        g = [beta] + [0.0] * m  # @line L2
        hcols = []  # hcols[j] = rotated column j of H, length j + 1
        cs, sn = [], []
        j = 0
        done = False
        breakdown = False
        while j < m and total < maxit:  # @line L3
            w = _matvec(a, v[j])  # @line L4
            total += 1
            h = [0.0] * (j + 2)
            for i in range(j + 1):  # @line L5
                hij = sum(p * q for p, q in zip(v[i], w))
                h[i] = hij
                w = [p - hij * q for p, q in zip(w, v[i])]
            hnext = _norm(w)
            h[j + 1] = hnext  # @line L6
            for i in range(j):  # @line L7
                t = cs[i] * h[i] + sn[i] * h[i + 1]
                h[i + 1] = -sn[i] * h[i] + cs[i] * h[i + 1]
                h[i] = t
            rho = math.hypot(h[j], h[j + 1])
            if rho == 0.0:
                c, s = 1.0, 0.0
            else:
                c, s = h[j] / rho, h[j + 1] / rho
            cs.append(c)
            sn.append(s)
            h[j] = rho
            h[j + 1] = 0.0
            g[j + 1] = -s * g[j]
            g[j] = c * g[j]
            hcols.append(h[: j + 1])
            j += 1
            history.append(abs(g[j]))
            scale = max(abs(hc[-1]) for hc in hcols)
            if rho <= 1e-14 * scale:
                breakdown = True
                break
            if abs(g[j]) <= target:  # @line L8
                done = True
                break
            if hnext == 0.0:
                done = True
                break
            v.append([t / hnext for t in w])
        if breakdown:
            j -= 1
            history.pop()
        y = [0.0] * j  # @line L9
        for i in range(j - 1, -1, -1):
            acc = g[i]
            for k in range(i + 1, j):
                acc -= hcols[k][i] * y[k]
            y[i] = acc / hcols[i][i]
        for k in range(j):
            vk = v[k]
            yk = y[k]
            x = [xi + yk * vi for xi, vi in zip(x, vk)]
        if breakdown:
            return GMRESResult(x, False, total, restarts, history, "breakdown")
        if done:
            ax = _matvec(a, x)
            if _norm([bi - t for bi, t in zip(b, ax)]) <= 10 * target:
                return GMRESResult(x, True, total, restarts, history, "converged")
        restarts += 1  # @line L10
