# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/biconjugate-gradient/. The authors are listed in prov/4SSPDC.jsonl.

"""The biconjugate gradient method (BiCG) for A x = b, A nonsymmetric.

Works with floats or with fractions.Fraction (then the run is exact).
A is a dense list of rows or a CSR object; BiCG needs products with A
and with A^T. Standard library only.
"""


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
        out = []
        for i in range(self.n):
            acc = 0 * x[0] if x else 0
            for p in range(self.ptr[i], self.ptr[i + 1]):
                acc += self.data[p] * x[self.ind[p]]
            out.append(acc)
        return out

    def rmatvec(self, y):
        """A^T y, scattering row i of A times y_i."""
        out = [0 * y[0] for _ in range(self.n)] if y else []
        for i in range(self.n):
            yi = y[i]
            for p in range(self.ptr[i], self.ptr[i + 1]):
                out[self.ind[p]] += self.data[p] * yi
        return out


def _mv(a, x):
    if isinstance(a, CSR):
        return a.matvec(x)
    return [sum((aij * xj for aij, xj in zip(row, x)), 0 * x[0]) for row in a]


def _rmv(a, y):
    if isinstance(a, CSR):
        return a.rmatvec(y)
    n = len(y)
    return [sum((a[i][j] * y[i] for i in range(n)), 0 * y[0]) for j in range(n)]


def _dot(u, v):
    return sum((p * q for p, q in zip(u, v)), 0 * u[0])


class BiCGResult:
    def __init__(self, x, status, iterations, history):
        self.x = x
        self.status = status  # "converged", "maxit", "rho-breakdown" or "pivot-breakdown"
        self.converged = status == "converged"
        self.iterations = iterations
        self.history = history  # ||r_k||_2^2 for k = 0, 1, ...


def bicg(a, b, x0=None, shadow=None, tol=1e-10, maxit=None, trace=None):
    """Run BiCG until ||r_k||_2 <= tol ||b||_2.

    shadow is the shadow residual r~_0 (default r_0). trace, if a list,
    receives (r_k, r~_k, p_k, p~_k) for every k, for tests of
    biorthogonality.
    """
    n = len(b)
    maxit = 2 * n if maxit is None else maxit
    zero = 0 * b[0]
    x = [zero] * n if x0 is None else list(x0)
    r = [bi - t for bi, t in zip(b, _mv(a, x))]  # @line L1
    rt = list(r) if shadow is None else list(shadow)
    p, pt = list(r), list(rt)  # @line L2
    rho = _dot(rt, r)
    target = tol * tol * _dot(b, b)
    history = [_dot(r, r)]
    for k in range(maxit + 1):  # @line L3
        if trace is not None:
            trace.append((list(r), list(rt), list(p), list(pt)))
        if history[-1] <= target:  # @line L4
            return BiCGResult(x, "converged", k, history)
        if k == maxit:
            break
        if rho == 0:
            return BiCGResult(x, "rho-breakdown", k, history)
        q = _mv(a, p)  # @line L5
        qt = _rmv(a, pt)
        sigma = _dot(pt, q)
        if sigma == 0:
            return BiCGResult(x, "pivot-breakdown", k, history)
        alpha = rho / sigma  # @line L6
        x = [xi + alpha * pi for xi, pi in zip(x, p)]  # @line L7
        r = [ri - alpha * qi for ri, qi in zip(r, q)]
        rt = [ri - alpha * qi for ri, qi in zip(rt, qt)]  # @line L8
        rho_new = _dot(rt, r)  # @line L9
        beta = rho_new / rho
        rho = rho_new
        p = [ri + beta * pi for ri, pi in zip(r, p)]  # @line L10
        pt = [ri + beta * pi for ri, pi in zip(rt, pt)]
        history.append(_dot(r, r))
    return BiCGResult(x, "maxit", maxit, history)
