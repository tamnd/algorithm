# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bicgstab/. The authors are listed in prov/ED04G2.jsonl.

"""BiCGSTAB (van der Vorst 1992) for A x = b with A nonsymmetric.

Works with floats or fractions.Fraction (then the run is exact). A is a
dense list of rows or a CSR object; only products with A are used.
Standard library only.
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


def _mv(a, x):
    if isinstance(a, CSR):
        return a.matvec(x)
    return [sum((aij * xj for aij, xj in zip(row, x)), 0 * x[0]) for row in a]


def _dot(u, v):
    return sum((p * q for p, q in zip(u, v)), 0 * u[0])


class BiCGSTABResult:
    def __init__(self, x, status, iterations, history, omegas):
        self.x = x
        self.status = status  # converged, maxit, rho-breakdown, pivot-breakdown, omega-breakdown
        self.converged = status == "converged"
        self.iterations = iterations
        self.history = history  # ||r_k||_2^2 of the updated residuals
        self.omegas = omegas  # the stabilizing parameters omega_1, omega_2, ...


def bicgstab(a, b, x0=None, shadow=None, tol=1e-10, maxit=None):
    """Run BiCGSTAB until ||r||_2 <= tol ||b||_2 (squared norms are compared)."""
    n = len(b)
    maxit = 2 * n if maxit is None else maxit
    zero = 0 * b[0]
    x = [zero] * n if x0 is None else list(x0)
    r = [bi - t for bi, t in zip(b, _mv(a, x))]  # @line L1
    rh = list(r) if shadow is None else list(shadow)
    p = list(r)  # @line L2
    rho = _dot(rh, r)
    target = tol * tol * _dot(b, b)
    history = [_dot(r, r)]
    omegas = []
    for k in range(maxit + 1):  # @line L3
        if history[-1] <= target:
            return BiCGSTABResult(x, "converged", k, history, omegas)
        if k == maxit:
            break
        if rho == 0:
            return BiCGSTABResult(x, "rho-breakdown", k, history, omegas)
        v = _mv(a, p)  # @line L4
        sigma = _dot(rh, v)
        if sigma == 0:
            return BiCGSTABResult(x, "pivot-breakdown", k, history, omegas)
        alpha = rho / sigma
        s = [ri - alpha * vi for ri, vi in zip(r, v)]  # @line L5
        ss = _dot(s, s)
        if ss <= target:  # @line L6
            x = [xi + alpha * pi for xi, pi in zip(x, p)]
            history.append(ss)
            return BiCGSTABResult(x, "converged", k + 1, history, omegas)
        t = _mv(a, s)  # @line L7
        tt = _dot(t, t)
        ts = _dot(t, s)
        if ts == 0:
            # omega = 0 would make the next rho zero: stabilization breakdown
            x = [xi + alpha * pi for xi, pi in zip(x, p)]
            history.append(ss)
            return BiCGSTABResult(x, "omega-breakdown", k + 1, history, omegas)
        omega = ts / tt  # @line L8
        omegas.append(omega)
        x = [xi + alpha * pi + omega * si for xi, pi, si in zip(x, p, s)]  # @line L9
        r = [si - omega * ti for si, ti in zip(s, t)]
        rho_new = _dot(rh, r)  # @line L10
        beta = (rho_new / rho) * (alpha / omega)
        rho = rho_new
        p = [ri + beta * (pi - omega * vi) for ri, pi, vi in zip(r, p, v)]  # @line L11
        history.append(_dot(r, r))
    return BiCGSTABResult(x, "maxit", maxit, history, omegas)
