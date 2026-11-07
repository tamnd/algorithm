# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mrrr-algorithm/. The authors are listed in prov/B3BDXW.jsonl.

"""The MRRR algorithm (multiple relatively robust representations).

mrrr(a, b) computes all eigenvalues and orthonormal eigenvectors of the real
symmetric tridiagonal matrix T with diagonal a[0..n-1] and off-diagonal
b[0..n-2]. The matrix is split where an off-diagonal entry is negligible. For
each unreduced block, a shift sigma below the spectrum gives a positive
definite root representation T - sigma I = L D L^T. Eigenvalues of a
representation are found by bisection on the stationary qd count, to high
relative accuracy. Eigenvalues with a relative gap of at least gaptol get their
eigenvector from one twisted factorization; a cluster gets a new
representation L D L^T - tau I = L+ D+ L+^T with tau at one end of the
cluster, which pulls the cluster apart in the relative sense. The tree of
representations is walked with an explicit stack.

Pure Python, standard library only. Vectors are lists; result.vectors[k] is
the unit eigenvector for result.values[k], in increasing order of the values.
"""

import math
from typing import NamedTuple

U = 2.0**-53  # unit roundoff
TINY = 2.0**-1000  # replaces a zero pivot, which keeps the counts defined
GROWTH1 = 8.0  # accept a new representation at once if max |D+| <= GROWTH1 * spectral diameter
GROWTH2 = 2.0**20  # otherwise accept the least growth seen, if below this multiple of the diameter
TRIES = 4  # the number of times the distance of the shift from the cluster is doubled


class MRRRResult(NamedTuple):
    values: list  # eigenvalues in increasing order
    vectors: list  # vectors[k] is the unit eigenvector for values[k]
    max_depth: int  # depth of the representation tree (0: only root representations)
    representations: int  # the number of representations L D L^T built
    counts: int  # the number of O(n) qd count sweeps used by bisection
    twisted: int  # the number of twisted factorizations (one per eigenvector)
    fallbacks: int  # clusters finished by Gram-Schmidt because no new representation was found


def root_ldl(a, b, sigma):
    """(d, l) with T - sigma I = L D L^T, or None if a pivot is not positive."""
    n = len(a)
    d = [0.0] * n
    l = [0.0] * (n - 1)
    d[0] = a[0] - sigma
    for i in range(n - 1):
        if not d[i] > 0:
            return None
        l[i] = b[i] / d[i]
        d[i + 1] = a[i + 1] - sigma - l[i] * b[i]
    return (d, l) if d[n - 1] > 0 else None


def stqds(d, l, tau):
    """Stationary qd: (D+, L+, s) with L D L^T - tau I = L+ D+ L+^T."""
    n = len(d)
    dp = [0.0] * n
    lp = [0.0] * (n - 1)
    s = [0.0] * n
    s[0] = -tau
    for i in range(n - 1):
        dp[i] = d[i] + s[i]
        if dp[i] == 0:
            dp[i] = -TINY
        lp[i] = d[i] * l[i] / dp[i]
        s[i + 1] = lp[i] * l[i] * s[i] - tau
    dp[n - 1] = d[n - 1] + s[n - 1]
    return dp, lp, s


def negcount(d, l, tau):
    """The number of eigenvalues of L D L^T less than tau: negative pivots of stationary qd."""
    count = 0
    s = -tau
    n = len(d)
    for i in range(n - 1):
        dp = d[i] + s
        if dp == 0:
            dp = -TINY
        if dp < 0:
            count += 1
        s = (d[i] * l[i] / dp) * l[i] * s - tau
    if d[n - 1] + s < 0:
        count += 1
    return count


def dqds_progressive(d, l, mu):
    """Progressive qd from the bottom: (p, U-) with L D L^T - mu I = U- D- U-^T, D-(i) = p(i) for i = 0."""
    n = len(d)
    p = [0.0] * n
    um = [0.0] * (n - 1)
    p[n - 1] = d[n - 1] - mu
    for i in range(n - 2, -1, -1):
        dm = d[i] * l[i] * l[i] + p[i + 1]
        if dm == 0:
            dm = -TINY
        t = d[i] / dm
        um[i] = l[i] * t
        p[i] = p[i + 1] * t - mu
    return p, um


def twisted_vector(d, l, mu, r=None):
    """Eigenvector of L D L^T for the eigenvalue approximation mu, by a twisted factorization.

    The twist index r defaults to the one with the least |gamma_r|. Returns (z, r, rho) with z of
    unit norm and (L D L^T - mu I) z = rho e_r, so |rho| is the residual norm.
    """
    n = len(d)
    _, lp, s = stqds(d, l, mu)
    p, um = dqds_progressive(d, l, mu)
    gamma = [s[k] + p[k] + mu for k in range(n)]
    if r is None:
        r = min(range(n), key=lambda k: abs(gamma[k]))
    z = [0.0] * n
    z[r] = 1.0
    for i in range(r - 1, -1, -1):  # upward with L+
        if z[i + 1] != 0:
            z[i] = -lp[i] * z[i + 1]
        else:  # use row i+1 of the matrix: d l z_i + (...) z_(i+1) + d l z_(i+2) = 0
            z[i] = -(d[i + 1] * l[i + 1] / (d[i] * l[i])) * z[i + 2]
    for i in range(r, n - 1):  # downward with U-
        if z[i] != 0:
            z[i + 1] = -um[i] * z[i]
        else:
            z[i + 1] = -(d[i - 1] * l[i - 1] / (d[i] * l[i])) * z[i - 1]
    nz = math.sqrt(sum(x * x for x in z))
    return [x / nz for x in z], r, gamma[r] / nz


def twist_order(d, l, mu):
    """Twist indices sorted by |gamma_k|, the candidates for independent vectors in a tight cluster."""
    _, _, s = stqds(d, l, mu)
    p, _ = dqds_progressive(d, l, mu)
    return sorted(range(len(d)), key=lambda k: abs(s[k] + p[k] + mu))


class _Counter:
    def __init__(self):
        self.counts = 0

    def bisect(self, d, l, k, lo, hi):
        """The k-th smallest (1-based) eigenvalue of L D L^T, to high relative accuracy.

        The bracket [lo, hi] is widened until negcount(lo) < k <= negcount(hi).
        """
        width = max(hi - lo, abs(lo), abs(hi), TINY)
        while True:
            self.counts += 1
            if negcount(d, l, lo) < k:
                break
            lo -= width
            width *= 2
        width = max(hi - lo, TINY)
        while True:
            self.counts += 1
            if negcount(d, l, hi) >= k:
                break
            hi += width
            width *= 2
        floor = U * U * max(abs(lo), abs(hi))
        for _ in range(400):
            mid = lo + 0.5 * (hi - lo)
            if mid in (lo, hi) or hi - lo <= max(2 * U * max(abs(lo), abs(hi)), floor):
                break
            self.counts += 1
            if negcount(d, l, mid) >= k:
                hi = mid
            else:
                lo = mid
        return lo + 0.5 * (hi - lo)


def _groups(lam, gaptol):
    """Split sorted eigenvalues into maximal runs whose neighbours have relative gap < gaptol."""
    out = [[0]]
    for i in range(1, len(lam)):
        if lam[i] - lam[i - 1] < gaptol * max(abs(lam[i]), abs(lam[i - 1])):
            out[-1].append(i)
        else:
            out.append([i])
    return out


def _jacobi(h):
    """Eigenvectors of a small symmetric matrix by cyclic Jacobi; returns (values, columns as lists)."""
    g = len(h)
    a = [row[:] for row in h]
    v = [[float(i == j) for j in range(g)] for i in range(g)]
    for _ in range(50):
        off = sum(a[i][j] ** 2 for i in range(g) for j in range(g) if i != j)
        if off <= (U * U) * sum(a[i][i] ** 2 for i in range(g)) or off == 0:
            break
        for p in range(g - 1):
            for q in range(p + 1, g):
                if a[p][q] == 0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(g):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(g):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(g):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    order = sorted(range(g), key=lambda i: a[i][i])
    return [a[i][i] for i in order], [[v[k][i] for k in range(g)] for i in order]


def _shifted_product(d, l, mu, v):
    """(L D L^T - mu I) v in factored form."""
    n = len(d)
    w = [d[i] * (v[i] + (l[i] * v[i + 1] if i < n - 1 else 0.0)) for i in range(n)]  # D L^T v
    return [w[i] + (l[i - 1] * w[i - 1] if i > 0 else 0.0) - mu * v[i] for i in range(n)]


def _cluster_fallback(d, l, lam, stats):
    """Orthonormal vectors for a cluster that got no new representation.

    For each member, try twisted vectors at the twist indices in order of increasing |gamma_k| and keep
    the first whose part orthogonal to the vectors already kept has norm at least 1/2. In a cluster of
    g eigenvalues equal to working precision, g different twist indices give independent vectors. A
    Rayleigh-Ritz step inside the span then pairs the vectors with the eigenvalues in order.
    """
    n = len(d)
    g = len(lam)
    kept = []
    for mu in lam:
        best = None
        for r in twist_order(d, l, mu):
            z, _, _ = twisted_vector(d, l, mu, r)
            stats["twisted"] += 1
            for _ in range(2):
                for w in kept:
                    c = sum(x * y for x, y in zip(z, w))
                    z = [x - c * y for x, y in zip(z, w)]
            nz = math.sqrt(sum(x * x for x in z))
            if best is None or nz > best[0]:
                best = (nz, z)
            if nz >= 0.5:
                break
        nz, z = best
        kept.append([x / nz for x in z])
    mu = sum(lam) / g
    mv = [_shifted_product(d, l, mu, v) for v in kept]
    h = [[sum(x * y for x, y in zip(kept[i], mv[j])) for j in range(g)] for i in range(g)]
    h = [[0.5 * (h[i][j] + h[j][i]) for j in range(g)] for i in range(g)]
    _, cols = _jacobi(h)
    return [[sum(c[k] * kept[k][i] for k in range(g)) for i in range(n)] for c in cols]


def _block(a, b, gaptol, maxdepth, ctr, stats):
    """MRRR on one unreduced block. Returns (values, vectors) in increasing order."""
    m = len(a)
    # Gershgorin interval and the root shift below it
    gl = min(a[i] - (abs(b[i - 1]) if i > 0 else 0) - (abs(b[i]) if i < m - 1 else 0) for i in range(m))
    gu = max(a[i] + (abs(b[i - 1]) if i > 0 else 0) + (abs(b[i]) if i < m - 1 else 0) for i in range(m))
    spdiam = gu - gl
    margin = 2 * m * U * max(spdiam, abs(gl), abs(gu))
    rep = None
    while rep is None:  # @line L2
        sigma = gl - margin
        rep = root_ldl(a, b, sigma)
        margin *= 2
    stats["reps"] += 1
    d, l = rep
    lam = [ctr.bisect(d, l, k, 0.0, gu - sigma) for k in range(1, m + 1)]  # @line L3
    values = [0.0] * m
    vectors = [None] * m
    stack = [(d, l, sigma, list(range(m)), lam, 0)]  # @line L4
    while stack:  # @line L5
        d, l, sigma, idx, lam, depth = stack.pop()
        stats["depth"] = max(stats["depth"], depth)
        for g in _groups(lam, gaptol):  # @line L6
            if len(g) == 1:  # a singleton: one twisted factorization  # @line L7
                i = g[0]
                z, _, _ = twisted_vector(d, l, lam[i])  # @line L8
                stats["twisted"] += 1
                values[idx[i]] = sigma + lam[i]
                vectors[idx[i]] = z
                continue
            child = None  # a cluster: find a new representation at one of its ends  # @line L9
            if depth < maxdepth:
                lo_l, hi_l = lam[g[0]], lam[g[-1]]
                delta = 4 * U * max(abs(lo_l), abs(hi_l)) + U * U * spdiam
                best = None
                for _ in range(TRIES):
                    for tau in (lo_l - delta, hi_l + delta):
                        dp, lp, _ = stqds(d, l, tau)
                        growth = max(abs(x) for x in dp)
                        if not math.isfinite(growth):
                            continue
                        if best is None or growth < best[0]:
                            best = (growth, dp, lp, tau, delta)
                        if growth <= GROWTH1 * spdiam:
                            child = (dp, lp, tau)
                            break
                    if child:
                        break
                    delta *= 2
                if child is None and best is not None and best[0] <= GROWTH2 * spdiam:
                    _, dp, lp, tau, delta = best  # moderate element growth: accept the least bad shift
                    child = (dp, lp, tau)
            if child is None:  # no representation: finish the cluster like inverse iteration
                stats["fallbacks"] += 1
                zs = _cluster_fallback(d, l, [lam[i] for i in g], stats)
                for i, z in zip(g, zs):
                    values[idx[i]] = sigma + lam[i]
                    vectors[idx[i]] = z
                continue
            dp, lp, tau = child
            stats["reps"] += 1
            # positions in the block are preserved by the shift; refine in the child  # @line L10
            ks = [idx[i] + 1 for i in g]
            new = [ctr.bisect(dp, lp, k, lam[i] - tau - delta, lam[i] - tau + delta) for k, i in zip(ks, g)]
            stack.append((dp, lp, sigma + tau, [idx[i] for i in g], new, depth + 1))  # @line L11
    return values, vectors


def mrrr(a, b, gaptol=1e-3, maxdepth=12):
    """Return an MRRRResult for the symmetric tridiagonal matrix with diagonal a and off-diagonal b."""
    n = len(a)
    if len(b) != max(n - 1, 0):
        raise ValueError("b must have length len(a) - 1")
    a = [float(x) for x in a]
    b = [float(x) for x in b]
    ctr = _Counter()
    stats = {"reps": 0, "depth": 0, "twisted": 0, "fallbacks": 0}
    tnorm = max([abs(x) for x in a] + [abs(x) for x in b] + [0.0])
    values, vectors = [], []
    start = 0
    for i in range(n):  # split where an off-diagonal entry is negligible  # @line L1
        if i == n - 1 or abs(b[i]) <= 2 * U * tnorm:
            m = i + 1 - start
            if m == 1:
                vals, vecs = [a[start]], [[1.0]]
            else:
                vals, vecs = _block(a[start : i + 1], b[start:i], gaptol, maxdepth, ctr, stats)
            for v, z in zip(vals, vecs):
                values.append(v)
                vectors.append([0.0] * start + z + [0.0] * (n - start - m))
            start = i + 1
    order = sorted(range(n), key=lambda k: values[k])
    return MRRRResult(  # @line L12
        [values[k] for k in order],
        [vectors[k] for k in order],
        stats["depth"],
        stats["reps"],
        ctr.counts,
        stats["twisted"],
        stats["fallbacks"],
    )
