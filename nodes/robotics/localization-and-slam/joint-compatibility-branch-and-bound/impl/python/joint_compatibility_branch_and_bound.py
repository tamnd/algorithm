# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joint-compatibility-branch-and-bound/. The authors are listed in prov/V4AT33.jsonl.

"""Joint compatibility branch and bound (JCBB), after Neira and Tardos (2001).

The inputs describe one step of a Kalman filter with a state estimate of
covariance P (n_x by n_x):

  z[i]     the readings, each a vector of size d (i = 0 .. m-1)
  h[j]     the predicted reading of feature j (j = 0 .. n-1)
  H[j]     the Jacobian of that prediction with respect to the state (d by n_x)
  R        the covariance of the noise of one reading (d by d)

A hypothesis assigns to each reading a feature index or None (no feature).
For the set of its non-null pairings, the stacked innovation is
nu = (z[i] - h[j]) and its covariance is C = Hs P Hs^T + diag(R, ..., R),
where Hs stacks the H[j]. The hypothesis is jointly compatible if
D2 = nu^T C^(-1) nu is at most the chi-square quantile with d k degrees of
freedom at the given level, where k is the number of pairings.

JCBB searches the interpretation tree in the order of the readings and
returns the hypothesis with the most pairings among those that it can reach:
every pairing passes the individual test, and every prefix of the hypothesis
is jointly compatible. By default two readings may pair with the same feature,
as in the paper; unique=True forbids it.
"""

import math

import rbm

# ---------------------------------------------------------------- chi-square quantiles


def chi2_cdf(x, dof):
    """Return P(X <= x) for X chi-square with dof degrees of freedom.

    This is the regularized lower incomplete gamma function P(dof/2, x/2),
    by its power series, which converges for every x >= 0.
    """
    if x <= 0.0:
        return 0.0
    a, y = dof / 2.0, x / 2.0
    term = 1.0 / a
    total = term
    k = 1
    while term > total * 1e-17:
        term *= y / (a + k)
        total += term
        k += 1
    return math.exp(-y + a * math.log(y) - math.lgamma(a)) * total


def chi2_quantile(level, dof):
    """Return x with chi2_cdf(x, dof) = level, by bisection to about 1e-12."""
    lo, hi = 0.0, 1.0
    while chi2_cdf(hi, dof) < level:
        hi *= 2.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if chi2_cdf(mid, dof) < level:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-12 * hi:
            break
    return (lo + hi) / 2.0


# ---------------------------------------------------------------- the joint test


class Problem:
    """Precomputed blocks H[j] P H[k]^T, so that each joint test is cheap."""

    def __init__(self, z, h, hjac, p, r, level=0.95):
        self.z = [list(map(float, zi)) for zi in z]
        self.h = [list(map(float, hj)) for hj in h]
        self.r = r
        self.d = len(r)
        self.level = level
        hp = [rbm.mul(hj, p) for hj in hjac]
        self.blk = [[rbm.mul(hp[j], rbm.transpose(hjac[k])) for k in range(len(h))] for j in range(len(h))]
        self._quant = {}

    def threshold(self, dof):
        if dof not in self._quant:
            self._quant[dof] = chi2_quantile(self.level, dof)
        return self._quant[dof]

    def d2(self, pairs):
        """Return the joint squared Mahalanobis distance of a list of (i, j) pairs."""
        if not pairs:
            return 0.0
        d = self.d
        nu = []
        for i, j in pairs:
            nu.extend(a - b for a, b in zip(self.z[i], self.h[j]))
        k = len(pairs)
        c = rbm.zeros(d * k, d * k)
        for a, (ia, ja) in enumerate(pairs):
            for b, (ib, jb) in enumerate(pairs):
                blk = self.blk[ja][jb]
                for u in range(d):
                    for v in range(d):
                        c[a * d + u][b * d + v] = blk[u][v] + (self.r[u][v] if ia == ib else 0.0)
        y = rbm.solve(c, nu)
        return sum(p * q for p, q in zip(nu, y))

    def individually_compatible(self, i, j):
        return self.d2([(i, j)]) <= self.threshold(self.d)

    def jointly_compatible(self, pairs):
        return self.d2(pairs) <= self.threshold(self.d * len(pairs))


def pairs_of(hyp):
    """Return the non-null pairings (i, j) of a hypothesis."""
    return [(i, j) for i, j in enumerate(hyp) if j is not None]


# ---------------------------------------------------------------- JCBB


def jcbb(z, h, hjac, p, r, level=0.95, unique=False, tie_break=True):
    """Return (hypothesis, D2, nodes): the JCBB association and the number of nodes visited.

    hypothesis[i] is the feature of reading i or None. With tie_break, a
    hypothesis with as many pairings as the best one replaces it if its D2 is
    smaller; without it, the first one found is kept, as in the paper.
    """
    prob = Problem(z, h, hjac, p, r, level)
    m, n = len(z), len(h)
    ic = [[prob.individually_compatible(i, j) for j in range(n)] for i in range(m)]
    best = {"hyp": [None] * m, "k": 0, "d2": 0.0}
    nodes = [0]

    def better(k, d2):
        if k != best["k"]:
            return k > best["k"]
        return tie_break and d2 < best["d2"]

    def search(hyp, pairs, d2, i):  # @line L1
        nodes[0] += 1
        if i == m:  # @line L2
            if better(len(pairs), d2):  # @line L3
                best.update(hyp=list(hyp), k=len(pairs), d2=d2)  # @line L4
            return
        for j in range(n):  # @line L5
            if not ic[i][j] or (unique and any(jj == j for _, jj in pairs)):  # @line L6
                continue
            cand = pairs + [(i, j)]
            cd2 = prob.d2(cand)
            if cd2 <= prob.threshold(prob.d * len(cand)):  # @line L7
                search(hyp + [j], cand, cd2, i + 1)  # @line L8
        k_max = len(pairs) + m - i - 1  # @line L9
        if k_max > best["k"] or (tie_break and k_max == best["k"] and d2 < best["d2"]):  # @line L10
            search(hyp + [None], pairs, d2, i + 1)  # @line L11

    search([], [], 0.0, 0)
    return best["hyp"], best["d2"], nodes[0]  # @line L12


# ---------------------------------------------------------------- baselines


def nearest_neighbor(z, h, hjac, p, r, level=0.95):
    """Return the individual compatibility nearest neighbor association.

    Each reading takes the individually compatible feature with the smallest
    D2, independently of the other readings.
    """
    prob = Problem(z, h, hjac, p, r, level)
    out = []
    for i in range(len(z)):
        best, best_d2 = None, math.inf
        for j in range(len(h)):
            d2 = prob.d2([(i, j)])
            if d2 <= prob.threshold(prob.d) and d2 < best_d2:
                best, best_d2 = j, d2
        out.append(best)
    return out


def reachable(prob, hyp, unique=False):
    """True if JCBB can reach hyp: each pairing is individually compatible and each prefix is jointly compatible."""
    pairs = []
    for i, j in enumerate(hyp):
        if j is None:
            continue
        if not prob.individually_compatible(i, j):
            return False
        if unique and any(jj == j for _, jj in pairs):
            return False
        pairs.append((i, j))
        if not prob.jointly_compatible(pairs):
            return False
    return True


def brute_force(z, h, hjac, p, r, level=0.95, unique=False):
    """Return (hypothesis, D2) by enumeration of all (n + 1)^m hypotheses.

    Among the reachable hypotheses, take the most pairings, then the smallest D2.
    """
    prob = Problem(z, h, hjac, p, r, level)
    m, n = len(z), len(h)
    best, best_key = [None] * m, (0, 0.0)
    total = (n + 1) ** m
    for code in range(total):
        hyp, c = [], code
        for _ in range(m):
            c, rem = divmod(c, n + 1)
            hyp.append(None if rem == n else rem)
        if not reachable(prob, hyp, unique):
            continue
        k = sum(1 for j in hyp if j is not None)
        d2 = prob.d2(pairs_of(hyp))
        if k > best_key[0] or (k == best_key[0] and d2 < best_key[1]):
            best, best_key = hyp, (k, d2)
    return best, best_key[1]
