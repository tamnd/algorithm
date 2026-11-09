# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cma-es/. The authors are listed in prov/BASB19.jsonl.

"""CMA-ES with rank-one and rank-mu updates and cumulative step-size adaptation.

The defaults follow Hansen, The CMA evolution strategy, a tutorial (arXiv:1604.00772),
with positive recombination weights only.
"""

import math
import random
from typing import Callable, Sequence

Vector = list[float]
Matrix = list[list[float]]


def jacobi_eigen(a: Matrix, sweeps: int = 50) -> tuple[Vector, Matrix]:
    """Eigenvalues and eigenvectors of a symmetric matrix by cyclic Jacobi rotations.

    Return (values, B) with the eigenvectors in the columns of B.
    """
    n = len(a)
    a = [row[:] for row in a]
    b = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off <= 1e-30 * sum(a[i][i] ** 2 for i in range(n)):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    bkp, bkq = b[k][p], b[k][q]
                    b[k][p], b[k][q] = c * bkp - s * bkq, s * bkp + c * bkq
    return [a[i][i] for i in range(n)], b


class CMAES:
    """State of one CMA-ES run on R^n."""

    def __init__(self, m0: Sequence[float], sigma0: float, lam: int | None = None):
        n = self.n = len(m0)
        self.lam = lam or 4 + int(3 * math.log(n))
        self.mu = self.lam // 2
        raw = [math.log(self.mu + 0.5) - math.log(i + 1) for i in range(self.mu)]
        self.w = [r / sum(raw) for r in raw]
        self.mueff = 1 / sum(w * w for w in self.w)
        mueff = self.mueff
        self.cs = (mueff + 2) / (n + mueff + 5)
        self.ds = 1 + 2 * max(0.0, math.sqrt((mueff - 1) / (n + 1)) - 1) + self.cs
        self.cc = (4 + mueff / n) / (n + 4 + 2 * mueff / n)
        self.c1 = 2 / ((n + 1.3) ** 2 + mueff)
        self.cmu = min(1 - self.c1, 2 * (mueff - 2 + 1 / mueff) / ((n + 2) ** 2 + mueff))
        self.chi = math.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n * n))
        self.m = list(m0)
        self.sigma = sigma0
        self.C = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        self.B = [row[:] for row in self.C]
        self.D = [1.0] * n
        self.ps = [0.0] * n
        self.pc = [0.0] * n
        self.gen = 0

    def ask(self, rng: random.Random) -> tuple[list[Vector], list[Vector]]:
        """Sample lambda points x = m + sigma * B D z. Return (z vectors, x vectors)."""
        n = self.n
        zs, xs = [], []
        for _ in range(self.lam):
            z = [rng.gauss(0.0, 1.0) for _ in range(n)]
            y = [sum(self.B[i][j] * self.D[j] * z[j] for j in range(n)) for i in range(n)]
            zs.append(z)
            xs.append([self.m[i] + self.sigma * y[i] for i in range(n)])
        return zs, xs

    def tell(self, zs: list[Vector], fs: Sequence[float]) -> None:
        """Update m, the paths, C and sigma from the z vectors and their f values."""
        n, mu, w = self.n, self.mu, self.w
        order = sorted(range(self.lam), key=lambda k: fs[k])[:mu]  # @line L4
        ys = [[sum(self.B[i][j] * self.D[j] * zs[k][j] for j in range(n)) for i in range(n)] for k in order]
        zw = [sum(w[r] * zs[order[r]][i] for r in range(mu)) for i in range(n)]
        yw = [sum(w[r] * ys[r][i] for r in range(mu)) for i in range(n)]
        self.m = [self.m[i] + self.sigma * yw[i] for i in range(n)]  # @line L5
        bz = [sum(self.B[i][j] * zw[j] for j in range(n)) for i in range(n)]  # C^(-1/2) y_w
        a = math.sqrt(self.cs * (2 - self.cs) * self.mueff)
        self.ps = [(1 - self.cs) * self.ps[i] + a * bz[i] for i in range(n)]  # @line L6
        self.gen += 1
        norm_ps = math.sqrt(sum(v * v for v in self.ps))
        hs = norm_ps / math.sqrt(1 - (1 - self.cs) ** (2 * self.gen)) < (1.4 + 2 / (n + 1)) * self.chi
        b = math.sqrt(self.cc * (2 - self.cc) * self.mueff) if hs else 0.0
        self.pc = [(1 - self.cc) * self.pc[i] + b * yw[i] for i in range(n)]  # @line L7
        old = 1 - self.c1 - self.cmu + (0.0 if hs else self.c1 * self.cc * (2 - self.cc))
        C = self.C
        for i in range(n):  # @line L8
            for j in range(i, n):  # compute the upper half and mirror it, so C is exactly symmetric
                rank_mu = sum(w[r] * ys[r][i] * ys[r][j] for r in range(mu))
                C[i][j] = old * C[i][j] + self.c1 * self.pc[i] * self.pc[j] + self.cmu * rank_mu
                C[j][i] = C[i][j]
        self.sigma *= math.exp((self.cs / self.ds) * (norm_ps / self.chi - 1))  # @line L9
        vals, self.B = jacobi_eigen(C)  # @line L10
        self.D = [math.sqrt(max(v, 0.0)) for v in vals]


def cma_es(
    f: Callable[[Sequence[float]], float],
    m0: Sequence[float],
    sigma0: float,
    max_evals: int,
    rng: random.Random,
    target: float = -math.inf,
    trace: list | None = None,
) -> tuple[Vector, float, int]:
    """Minimize f. Return (best point, its value, number of evaluations used).

    Stop after max_evals evaluations or when the best value is below target. If
    trace is a list, append the CMAES state after each generation as
    (generation, best value, sigma, copy of C).
    """
    es = CMAES(m0, sigma0)  # @line L1
    best, fbest, evals = list(m0), f(m0), 1
    while evals + es.lam <= max_evals and fbest >= target:  # @line L2
        zs, xs = es.ask(rng)  # @line L3
        fs = [f(x) for x in xs]
        evals += es.lam
        k = min(range(es.lam), key=lambda i: fs[i])
        if fs[k] < fbest:
            best, fbest = xs[k], fs[k]
        es.tell(zs, fs)
        if trace is not None:
            trace.append((es.gen, fbest, es.sigma, [row[:] for row in es.C]))
    return best, fbest, evals  # @line L11


def sphere(x: Sequence[float]) -> float:
    return sum(t * t for t in x)


def ellipsoid(x: Sequence[float]) -> float:
    n = len(x)
    return sum(10 ** (6 * i / (n - 1)) * t * t for i, t in enumerate(x))


def rosenbrock(x: Sequence[float]) -> float:
    return sum(100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2 for i in range(len(x) - 1))


def cholesky_ok(a: Matrix) -> bool:
    """True if the Cholesky factorization of a succeeds, that is, a is positive definite."""
    n = len(a)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s <= 0:
                    return False
                L[i][i] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return True
