# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fiat-shamir-with-aborts/. The authors are listed in prov/NJ9J4P.jsonl.
"""A toy version of the Lyubashevsky (2012) signature: Fiat-Shamir with aborts.

Key: A uniform in Z_q^(n x m), S in {-d..d}^(m x k), T = A S mod q.
Sign(mu):
  1. y <- D_sigma^m (discrete Gaussian, center 0)
  2. c = H(A y mod q, mu), a vector in {-1, 0, 1}^k with kappa nonzero entries
  3. z = S c + y
  4. output (z, c) with probability
     min(1, D_sigma^m(z) / (M D_{Sc,sigma}^m(z)))
       = min(1, exp((-2 <z, Sc> + |Sc|^2) / (2 sigma^2)) / M);
     otherwise go back to step 1.
Verify(mu, (z, c)): |z| <= eta sigma sqrt(m) and c = H(A z - T c mod q, mu).

sigma = alpha * Tb, where Tb = d kappa sqrt(m) bounds |S c|, and
M = exp(12 / alpha + 1 / (2 alpha^2)) (Lyubashevsky 2012, Section 4). With
alpha = 12, M is about e, so a signature takes about 2.7 tries.

Here sigma is the standard deviation: rho(x) = exp(-|x|^2 / (2 sigma^2)).
The parameters are tiny and the challenge space is small. For study only:
floating point, not constant time, not for real use.
"""

import bisect
import hashlib
import math
import random


class DiscreteGaussian:
    """D_sigma over Z with center 0, by a cumulative table cut at 12 sigma."""

    def __init__(self, sigma):
        bound = int(math.ceil(12 * sigma))
        self.values = list(range(-bound, bound + 1))
        weights = [math.exp(-x * x / (2 * sigma * sigma)) for x in self.values]
        total = sum(weights)
        acc, self.cdf = 0.0, []
        for wt in weights:
            acc += wt / total
            self.cdf.append(acc)
        self.cdf[-1] = 1.0

    def sample(self, rng):
        return self.values[bisect.bisect_left(self.cdf, rng.random())]


class Lyu12:
    def __init__(self, n, m, k, kappa, d=1, q=8380417, alpha=12.0, eta=2.0, seed=None):
        rng = random.Random(seed) if seed is not None else random.SystemRandom()
        self.n, self.m, self.k, self.kappa, self.d, self.q = n, m, k, kappa, d, q
        self.a = [[rng.randrange(q) for _ in range(m)] for _ in range(n)]
        self.s = [[rng.randint(-d, d) for _ in range(k)] for _ in range(m)]
        self.t = [[sum(self.a[i][j] * self.s[j][c] for j in range(m)) % q for c in range(k)] for i in range(n)]
        self.bound_sc = d * kappa * math.sqrt(m)
        self.sigma = alpha * self.bound_sc
        self.M = math.exp(12 / alpha + 1 / (2 * alpha * alpha))
        self.beta = eta * self.sigma * math.sqrt(m)
        self.gauss = DiscreteGaussian(self.sigma)

    def hash_to_challenge(self, w, msg):
        data = b"".join(x.to_bytes(4, "little") for x in w) + msg
        stream = hashlib.shake_256(data).digest(8 * self.k + 64)
        c, pos, placed = [0] * self.k, 0, 0
        while placed < self.kappa:
            i = stream[pos] % self.k
            if c[i] == 0:
                c[i] = 1 if stream[pos + 1] & 1 else -1
                placed += 1
            pos += 2
        return c

    def _sc(self, c):
        return [sum(row[i] * c[i] for i in range(self.k)) for row in self.s]

    def accept(self, z, v, rng):
        """Step 4: keep z with probability min(1, exp((-2 <z, v> + |v|^2) / (2 sigma^2)) / M)."""
        dot = sum(a * b for a, b in zip(z, v))
        vv = sum(a * a for a in v)
        return rng.random() < min(1.0, math.exp((-2 * dot + vv) / (2 * self.sigma ** 2)) / self.M)

    def respond(self, c, rng, reject=True):
        """One attempt of steps 1, 3 and 4 for a given c. Returns z, or None on abort."""
        y = [self.gauss.sample(rng) for _ in range(self.m)]
        v = self._sc(c)
        z = [a + b for a, b in zip(y, v)]
        if reject and not self.accept(z, v, rng):
            return None
        return z

    def sign(self, msg, rng=None, reject=True):
        """Return (z, c, tries)."""
        rng = rng or random.SystemRandom()
        tries = 0
        while True:
            tries += 1
            # @line L1
            y = [self.gauss.sample(rng) for _ in range(self.m)]
            # @line L2
            w = [sum(p * x for p, x in zip(row, y)) % self.q for row in self.a]
            # @line L3
            c = self.hash_to_challenge(w, msg)
            # @line L4
            v = self._sc(c)
            z = [a + b for a, b in zip(y, v)]
            # @line L5
            if reject and not self.accept(z, v, rng):
                continue
            return z, c, tries

    def verify(self, msg, sig):
        z, c = sig[0], sig[1]
        # @line L6
        if math.sqrt(sum(x * x for x in z)) > self.beta:
            return False
        # @line L7
        w = [(sum(p * x for p, x in zip(arow, z)) - sum(t * ci for t, ci in zip(trow, c))) % self.q for arow, trow in zip(self.a, self.t)]
        return self.hash_to_challenge(w, msg) == c


def estimate_secret(pairs, m, k):
    """Least squares S ~ E[z c^T] E[c c^T]^-1 from (z, c) pairs."""
    zc = [[0.0] * k for _ in range(m)]
    cc = [[0.0] * k for _ in range(k)]
    for z, c in pairs:
        for i in range(k):
            if c[i]:
                for j in range(m):
                    zc[j][i] += z[j] * c[i]
                for j in range(k):
                    cc[j][i] += c[j] * c[i]
    inv = _invert(cc)
    return [[sum(zc[j][t] * inv[t][i] for t in range(k)) for i in range(k)] for j in range(m)]


def _invert(a):
    n = len(a)
    aug = [row[:] + [float(i == j) for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[piv] = aug[piv], aug[col]
        p = aug[col][col]
        aug[col] = [x / p for x in aug[col]]
        for r in range(n):
            if r != col:
                f = aug[r][col]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[col])]
    return [row[n:] for row in aug]
