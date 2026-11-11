# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gpv-signature/. The authors are listed in prov/ZA5GEM.jsonl.
"""GPV hash-and-sign (Gentry, Peikert and Vaikuntanathan 2008), toy sizes.

Public key: A in Z_q^(n x m). Secret key: a short basis S of the lattice
Lambda^perp(A) = {x in Z^m : A x = 0 mod q}.
Sign(msg): pick a salt r, set u = H(msg, r) in Z_q^n, take any t with
A t = u, and sample v from D_{Lambda^perp(A), s, -t} with Klein's
randomized nearest plane over S. The signature is (r, x = t + v), a short
vector with A x = u. Verify: A x = H(msg, r) mod q and |x| <= s sqrt(m).

The toy trapdoor is the gadget construction of Micciancio and Peikert
(2012): A = [Abar | G - Abar R], with the short basis
S = [[I, R], [0, I]] [[0, I], [S_G, W]] where G W = -Abar mod q. The salt
makes each signed syndrome fresh, so two signatures never give two
preimages of the same u.

The second part is the attack of Nguyen and Regev (2006) on GGH-style
signatures, which sign with Babai rounding: each signature leaks a point
that is uniform in the parallelepiped of the secret basis, and a fourth
moment descent recovers the basis.

For study only: floating point, not constant time, toy sizes.
"""

import hashlib
import math
import random
from fractions import Fraction

TAU = 6.0


def sample_z(s, c, rng):
    sigma = s / math.sqrt(2 * math.pi)
    lo, hi = math.floor(c - TAU * sigma), math.ceil(c + TAU * sigma)
    while True:
        x = rng.randint(lo, hi)
        if rng.random() < math.exp(-math.pi * (x - c) ** 2 / (s * s)):
            return x


def gram_schmidt(vectors):
    gs = []
    for b in vectors:
        v = [Fraction(x) for x in b]
        for u in gs:
            mu = sum(x * y for x, y in zip(v, u)) / sum(y * y for y in u)
            v = [x - mu * y for x, y in zip(v, u)]
        gs.append(v)
    return [[float(x) for x in v] for v in gs]


def klein(basis, gs, s, center, rng):
    """Randomized nearest plane: a lattice vector from D_{L(basis), s, center}."""
    c = list(map(float, center))
    v = [0] * len(basis[0])
    for i in range(len(basis) - 1, -1, -1):
        g = gs[i]
        gg = sum(x * x for x in g)
        z = sample_z(s / math.sqrt(gg), sum(x * y for x, y in zip(c, g)) / gg, rng)
        c = [x - z * y for x, y in zip(c, basis[i])]
        v = [x + z * y for x, y in zip(v, basis[i])]
    return v


class GPV:
    def __init__(self, n=2, k=8, mbar=8, seed=None):
        rng = random.Random(seed) if seed is not None else random.SystemRandom()
        self.n, self.k, self.q = n, k, 1 << k
        w = n * k
        self.m = mbar + w
        q = self.q
        # @line L1
        abar = [[rng.randrange(q) for _ in range(mbar)] for _ in range(n)]
        r = [[rng.choice((-1, 0, 0, 1)) for _ in range(w)] for _ in range(mbar)]
        g = [[(1 << (j % k)) if j // k == i else 0 for j in range(w)] for i in range(n)]
        # @line L2
        ar = [[sum(abar[i][t] * r[t][j] for t in range(mbar)) for j in range(w)] for i in range(n)]
        self.a = [abar[i] + [(g[i][j] - ar[i][j]) % q for j in range(w)] for i in range(n)]
        self.r = r
        # @line L3
        # S_G: block diagonal, columns 2 e_j - e_(j+1) and 2 e_(k-1) in each block
        sg = [[0] * w for _ in range(w)]
        for blk in range(n):
            for j in range(k):
                col = blk * k + j
                sg[col][col] = 2
                if j + 1 < k:
                    sg[col + 1][col] = -1
        # W = G^-1(-Abar): column c holds the bits of -Abar[:, c] mod q
        wmat = [[0] * mbar for _ in range(w)]
        for c in range(mbar):
            for i in range(n):
                val = (-abar[i][c]) % q
                for j in range(k):
                    wmat[i * k + j][c] = (val >> j) & 1
        # S = [[R S_G, I + R W], [S_G, W]] as a list of column vectors
        cols = []
        for c in range(w):
            top = [sum(r[i][t] * sg[t][c] for t in range(w)) for i in range(mbar)]
            cols.append(top + [sg[i][c] for i in range(w)])
        for c in range(mbar):
            top = [(1 if i == c else 0) + sum(r[i][t] * wmat[t][c] for t in range(w)) for i in range(mbar)]
            cols.append(top + [wmat[i][c] for i in range(w)])
        self.basis = cols
        self.gs = gram_schmidt(cols)
        # @line L4
        max_gs = max(math.sqrt(sum(x * x for x in v)) for v in self.gs)
        eta = math.sqrt(math.log(2 * self.m * (1 + 2 ** 20)) / math.pi)
        self.s = max_gs * eta
        self.beta = self.s * math.sqrt(self.m)
        self.mbar, self.w, self.sg, self.wmat = mbar, w, sg, wmat

    def public_key(self):
        return self.a

    def mul_a(self, x):
        return [sum(p * v for p, v in zip(row, x)) % self.q for row in self.a]

    def hash_to_syndrome(self, msg, salt):
        d = hashlib.shake_256(b"GPV-toy" + salt + msg).digest(2 * self.n)
        return [int.from_bytes(d[2 * i : 2 * i + 2], "little") % self.q for i in range(self.n)]

    def any_preimage(self, u):
        """t = [R; I] G^-1(u), so A t = G G^-1(u) = u."""
        bits = [(ui >> j) & 1 for ui in u for j in range(self.k)]
        top = [sum(a * b for a, b in zip(row, bits)) for row in self.r]
        return top + bits

    def sign(self, msg, rng=None):
        rng = rng or random.SystemRandom()
        # @line L5
        salt = bytes(rng.getrandbits(8) for _ in range(16))
        # @line L6
        u = self.hash_to_syndrome(msg, salt)
        # @line L7
        t = self.any_preimage(u)
        # @line L8
        v = klein(self.basis, self.gs, self.s, [-x for x in t], rng)
        # @line L9
        return salt, [a + b for a, b in zip(t, v)]

    def verify(self, msg, sig):
        salt, x = sig
        # @line L10
        if len(x) != self.m or math.sqrt(sum(v * v for v in x)) > self.beta:
            return False
        # @line L11
        return self.mul_a(x) == self.hash_to_syndrome(msg, salt)


# ---- Nguyen and Regev (2006): learning a parallelepiped ----------------------


class GGHToySigner:
    """Signs a target point m in Z^n with Babai rounding over the secret basis B (rows)."""

    def __init__(self, n, rng):
        self.n = n
        while True:
            b = [[(4 * n if i == j else 0) + rng.randint(-4, 4) for j in range(n)] for i in range(n)]
            if abs(det(b)) > 0:
                break
        self.b = b
        self.b_inv = invert(b)

    def sign(self, target):
        coeffs = [sum(Fraction(t) * self.b_inv[j][i] for j, t in enumerate(target)) for i in range(self.n)]
        k = [round(c) for c in coeffs]
        return [sum(k[i] * self.b[i][j] for i in range(self.n)) for j in range(self.n)]


def det(m):
    return _gauss(m)[0]


def invert(m):
    return _gauss(m)[1]


def _gauss(m):
    n = len(m)
    a = [[Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(m)]
    d = Fraction(1)
    for col in range(n):
        piv = next((r for r in range(col, n) if a[r][col] != 0), None)
        if piv is None:
            return Fraction(0), None
        if piv != col:
            a[col], a[piv] = a[piv], a[col]
            d = -d
        d *= a[col][col]
        p = a[col][col]
        a[col] = [x / p for x in a[col]]
        for r in range(n):
            if r != col and a[r][col] != 0:
                f = a[r][col]
                a[r] = [x - f * y for x, y in zip(a[r], a[col])]
    return d, [row[n:] for row in a]


def _cholesky(m):
    n = len(m)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            acc = m[i][j] - sum(low[i][t] * low[j][t] for t in range(j))
            low[i][j] = math.sqrt(acc) if i == j else acc / low[j][j]
    return low


def learn_parallelepiped(samples, rng, delta=0.7, max_iter=200):
    """Recover the rows of B, up to sign, from points v = x B with x uniform in [-1, 1]^n."""
    n, count = len(samples[0]), len(samples)
    # step 1: G = B^T B is about 3 E[v^T v]
    g = [[3.0 * sum(v[i] * v[j] for v in samples) / count for j in range(n)] for i in range(n)]
    # step 2: L with G^-1 = L L^T; then C = B L is orthogonal
    g_inv = [[float(x) for x in row] for row in invert([[Fraction(x) for x in row] for row in g])]
    low = _cholesky(g_inv)
    us = [[sum(v[i] * low[i][j] for i in range(n)) for j in range(n)] for v in samples]
    low_inv = [[float(x) for x in row] for row in invert([[Fraction(x) for x in row] for row in low])]

    def mom4(w):
        return sum(sum(a * b for a, b in zip(u, w)) ** 4 for u in us) / count

    def grad(w):
        out = [0.0] * n
        for u in us:
            d3 = sum(a * b for a, b in zip(u, w)) ** 3
            for j in range(n):
                out[j] += d3 * u[j]
        return [4 * x / count for x in out]

    def project(w, found):
        for f in found:
            dot = sum(a * b for a, b in zip(w, f))
            w = [a - dot * b for a, b in zip(w, f)]
        norm = math.sqrt(sum(a * a for a in w))
        return [a / norm for a in w]

    # step 3: gradient descent on the fourth moment over the unit sphere
    found = []
    for _ in range(n):
        w = project([rng.gauss(0, 1) for _ in range(n)], found)
        cur = mom4(w)
        for _ in range(max_iter):
            gr = grad(w)
            nxt = project([a - delta * b for a, b in zip(w, gr)], found)
            val = mom4(nxt)
            if val >= cur:
                break
            w, cur = nxt, val
        found.append(w)
    # step 4: map back, row = c L^-1, and round
    return [[round(sum(c[i] * low_inv[i][j] for i in range(n))) for j in range(n)] for c in found]


def attack_ggh(signer, count, rng, span=10 ** 6):
    """Collect count signatures on random targets and learn the secret basis."""
    samples = []
    for _ in range(count):
        target = [rng.randint(-span, span) for _ in range(signer.n)]
        sig = signer.sign(target)
        samples.append([2 * (t - s) for t, s in zip(target, sig)])
    return learn_parallelepiped(samples, rng)
