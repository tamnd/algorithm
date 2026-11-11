# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trapdoor-sampling-lattices/. The authors are listed in prov/M0ZP5R.jsonl.
"""Gadget trapdoors of Micciancio and Peikert (2012) with q = 2^k.

Gadget: g = (1, 2, ..., 2^(k-1)) and G = I_n (tensor) g^T, an n x nk matrix.
Trapdoor: A = [Abar | G - Abar R] with Abar uniform (n x mbar) and R a
small matrix in {-1, 0, 1}^(mbar x nk). Then A [R; I] = G mod q.

* gadget_inverse(u): the binary digits of u, a 0/1 vector x with G x = u.
* sample_g(u, s): a discrete Gaussian x with G x = u, digit by digit
  (each digit from the coset of 2Z fixed by the remaining target).
* sample_pre(u): the preimage sampler of MP12 Section 5.4. A perturbation p
  with covariance s^2 I - s_G^2 [R; I][R; I]^T is added first, so that the
  output x = p + [R; I] z is a spherical Gaussian that hides R.
* sample_pre_no_perturbation(u): x = [R; I] z, also a short preimage, but
  its shape follows R. The tests use it to show the leak.

Parameters follow the convention rho_s(x) = exp(-pi |x|^2 / s^2). Floating
point is used for the perturbation. For study only: not constant time,
toy sizes, and not for real use.
"""

import math
import random

TAU = 6.0


def sample_z(s, c, rng):
    """D_{Z,s,c} by rejection sampling on a window of width 2 TAU sigma."""
    sigma = s / math.sqrt(2 * math.pi)
    lo, hi = math.floor(c - TAU * sigma), math.ceil(c + TAU * sigma)
    while True:
        x = rng.randint(lo, hi)
        if rng.random() < math.exp(-math.pi * (x - c) ** 2 / (s * s)):
            return x


def cholesky(m):
    n = len(m)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            acc = m[i][j] - sum(low[i][t] * low[j][t] for t in range(j))
            if i == j:
                if acc <= 0:
                    raise ValueError("matrix is not positive definite")
                low[i][j] = math.sqrt(acc)
            else:
                low[i][j] = acc / low[j][j]
    return low


def spectral_norm(r, iters=60):
    """Largest singular value of r by power iteration on r^T r."""
    cols = len(r[0])
    v = [1.0] * cols
    lam = 0.0
    for _ in range(iters):
        rv = [sum(a * b for a, b in zip(row, v)) for row in r]
        w = [sum(r[i][j] * rv[i] for i in range(len(r))) for j in range(cols)]
        lam = math.sqrt(sum(x * x for x in w))
        v = [x / lam for x in w]
    return math.sqrt(lam)


class GadgetTrapdoor:
    def __init__(self, n, k, mbar, rng, s_g=9.0, r_round=4.5):
        self.n, self.k, self.q, self.mbar = n, k, 1 << k, mbar
        self.w = n * k
        self.m = mbar + self.w
        self.s_g, self.r_round = s_g, r_round
        q = self.q
        # @line L1
        self.abar = [[rng.randrange(q) for _ in range(mbar)] for _ in range(n)]
        self.r = [[rng.choice((-1, 0, 0, 1)) for _ in range(self.w)] for _ in range(mbar)]
        # @line L2
        g = self.gadget()
        ar = [[sum(self.abar[i][t] * self.r[t][j] for t in range(mbar)) for j in range(self.w)] for i in range(n)]
        self.a = [self.abar[i] + [(g[i][j] - ar[i][j]) % q for j in range(self.w)] for i in range(n)]
        # @line L3
        # T = [R; I] (m x w); Sigma_p = s^2 I - s_g^2 T T^T must stay above r_round^2 I
        self.t = [row[:] for row in self.r] + [[1 if i == j else 0 for j in range(self.w)] for i in range(self.w)]
        s1 = spectral_norm(self.r)
        self.s = 1.1 * math.sqrt(s_g * s_g * (s1 * s1 + 1) + r_round * r_round)
        tt = [[sum(a * b for a, b in zip(self.t[i], self.t[j])) for j in range(self.m)] for i in range(self.m)]
        cov = [[(self.s ** 2 - r_round ** 2 if i == j else 0.0) - s_g ** 2 * tt[i][j] for j in range(self.m)] for i in range(self.m)]
        self.chol = cholesky(cov)

    def gadget(self):
        g = [[0] * self.w for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.k):
                g[i][i * self.k + j] = 1 << j
        return g

    def mul_a(self, x):
        return [sum(a * b for a, b in zip(row, x)) % self.q for row in self.a]

    def gadget_inverse(self, u):
        return [(ui >> j) & 1 for ui in u for j in range(self.k)]

    def sample_g(self, u, rng):
        out = []
        for ui in u:
            t = ui
            for _ in range(self.k):
                # x in 2Z + t: x = t mod 2, written x = (t mod 2) + 2 y with y ~ D_{Z, s/2, -(t mod 2)/2}
                b = t & 1
                x = b + 2 * sample_z(self.s_g / 2, -b / 2, rng)
                out.append(x)
                t = (t - x) >> 1
        return out

    def _expand(self, z):
        return [sum(a * b for a, b in zip(row, z)) for row in self.t]

    def sample_pre_no_perturbation(self, u, rng):
        return self._expand(self.sample_g(u, rng))

    def sample_pre(self, u, rng):
        # @line L4
        g = [rng.gauss(0, 1 / math.sqrt(2 * math.pi)) for _ in range(self.m)]
        y = [sum(self.chol[i][j] * g[j] for j in range(i + 1)) for i in range(self.m)]
        p = [sample_z(self.r_round, yi, rng) for yi in y]
        # @line L5
        v = [(ui - ai) % self.q for ui, ai in zip(u, self.mul_a(p))]
        # @line L6
        z = self.sample_g(v, rng)
        # @line L7
        return [pi + xi for pi, xi in zip(p, self._expand(z))]
