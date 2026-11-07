# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divide-and-conquer-eigensolver/. The authors are listed in prov/J2346G.jsonl.
"""Cuppen's divide-and-conquer method for the symmetric tridiagonal eigenproblem,
with Dongarra-Sorensen deflation and the Gu-Eisenstat (Loewner) eigenvectors.
Python standard library only.

eigh_tridiagonal(a, b) returns (lam, q, stats) with lam[0] >= ... >= lam[n-1],
q[:, i] the unit eigenvector of lam[i], for the matrix with diagonal a and
off-diagonal b. The recursion depth is about log2(n).
"""
import math

U = 2.0 ** -53


def _secular_root(i, d, zsq, rho, stats):
    """Root of f(x) = 1 + rho sum zsq_j / (d_j - x) in (d_i, d_i+1), or above d_last.

    d is strictly increasing, zsq > 0 and rho > 0. Returns (org, tau): the root is
    d[org] + tau, and d[j] - root is computed as (d[j] - d[org]) - tau."""
    k = len(d)
    if i < k - 1:
        mid = (d[i] + d[i + 1]) / 2.0
        fmid = 1.0 + rho * sum(zsq[j] / (d[j] - mid) for j in range(k))
        org = i if fmid >= 0 else i + 1
        lo, hi = (0.0, mid - d[i]) if org == i else (mid - d[i + 1], 0.0)
    else:
        org, lo, hi = k - 1, 0.0, rho * sum(zsq)
    delta = [d[j] - d[org] for j in range(k)]
    tau = (lo + hi) / 2.0
    for _ in range(200):
        stats["secular_its"] += 1
        psi = dpsi = phi = dphi = erretm = 0.0
        for j in range(k):
            t = zsq[j] / (delta[j] - tau)
            if j <= i:
                psi += t
                dpsi += t / (delta[j] - tau)
            else:
                phi += t
                dphi += t / (delta[j] - tau)
            erretm += abs(t)
        f = 1.0 + rho * (psi + phi)
        if abs(f) <= 8 * k * U * (1.0 + rho * erretm) or hi - lo <= 4 * U * max(abs(lo), abs(hi)):
            break
        if f < 0:
            lo = tau
        else:
            hi = tau
        # rational model: rho psi ~ p + q / (delta_i - x), rho phi ~ r + s / (delta_i+1 - x)
        q = rho * dpsi * (delta[i] - tau) ** 2
        p = rho * psi - rho * dpsi * (delta[i] - tau)
        if i < k - 1:
            s = rho * dphi * (delta[i + 1] - tau) ** 2
            r = rho * phi - rho * dphi * (delta[i + 1] - tau)
            c0 = 1.0 + p + r
            # c0 (a - x)(b - x) + q (b - x) + s (a - x) = 0 with a = delta_i, b = delta_i+1
            a_, b_ = delta[i], delta[i + 1]
            qa = c0
            qb = -(c0 * (a_ + b_) + q + s)
            qc = c0 * a_ * b_ + q * b_ + s * a_
            x = None
            if qa == 0.0:
                x = -qc / qb if qb != 0 else None
            else:
                disc = qb * qb - 4 * qa * qc
                if disc >= 0:
                    sq = math.sqrt(disc)
                    w = -(qb + math.copysign(sq, qb)) / 2.0
                    cands = [w / qa] + ([qc / w] if w != 0 else [])
                    inside = [y for y in cands if lo < y < hi]
                    x = inside[0] if inside else None
        else:
            c0 = 1.0 + p
            x = delta[i] + q / c0 if c0 > 0 else None
        tau = x if (x is not None and lo < x < hi) else (lo + hi) / 2.0
    return org, tau


def _merge(dvals, qmat, z, rho, stats):
    """Eigen-decomposition of Q (D + rho z z^T) Q^T. Returns (lam, vecs) ascending."""
    n = len(dvals)
    nz = math.sqrt(sum(t * t for t in z))
    if nz == 0.0 or rho == 0.0:
        order = sorted(range(n), key=lambda i: dvals[i])
        return [dvals[i] for i in order], [[row[i] for i in order] for row in qmat]
    sign = 1.0 if rho > 0 else -1.0
    rho = abs(rho) * nz * nz
    z = [t / nz for t in z]
    d = [sign * t for t in dvals]  # solve with rho > 0; negate the eigenvalues at the end
    order = sorted(range(n), key=lambda i: d[i])
    d = [d[i] for i in order]
    z = [z[i] for i in order]
    q = [[row[i] for i in order] for row in qmat]
    tol = 8 * U * max(max(abs(t) for t in d), rho)
    deflated, kept = [], []
    for i in range(n):  # @line L5
        if rho * abs(z[i]) <= tol:
            deflated.append(i)
            stats["deflated"] += 1
            continue
        if kept:
            j = kept[-1]
            r = math.hypot(z[j], z[i])
            c, s = z[i] / r, z[j] / r
            if abs(c * s * (d[i] - d[j])) <= tol:
                dj = c * c * d[j] + s * s * d[i]
                d[i] = s * s * d[j] + c * c * d[i]
                d[j] = dj
                z[j], z[i] = 0.0, r
                for row in q:
                    qj, qi = row[j], row[i]
                    row[j], row[i] = c * qj - s * qi, s * qj + c * qi
                kept.pop()
                deflated.append(j)
                stats["deflated"] += 1
        kept.append(i)
    kept.sort(key=lambda i: d[i])
    dk = [d[i] for i in kept]
    k = len(kept)
    for t in range(k - 1):
        if not dk[t] < dk[t + 1]:  # equal poles after rotation: deflation missed; nudge
            dk[t + 1] = dk[t] + 2 * U * max(abs(dk[t]), tol)
    stats["roots"] += k
    zk = [z[i] for i in kept]
    zsq = [t * t for t in zk]
    roots = [_secular_root(i, dk, zsq, rho, stats) for i in range(k)]  # @line L6
    diff = [[(dk[j] - dk[org]) - tau for (org, tau) in roots] for j in range(k)]  # d_j - lam_i
    zhat = []
    for j in range(k):  # @line L7
        prod = -diff[j][j] / rho  # (lam_j - d_j) / rho
        for i in range(k):
            if i != j:
                prod *= -diff[j][i] / (dk[i] - dk[j])
        zhat.append(math.copysign(math.sqrt(max(prod, 0.0)), zk[j]))
    lam, vecs = [], []
    for i in range(k):
        s = [zhat[j] / diff[j][i] for j in range(k)]  # @line L8
        ns = math.sqrt(sum(t * t for t in s))
        s = [t / ns for t in s]
        lam.append(dk[roots[i][0]] + roots[i][1])
        vecs.append([sum(q[r][kept[j]] * s[j] for j in range(k)) for r in range(n)])  # @line L9
    for i in deflated:
        lam.append(d[i])
        vecs.append([q[r][i] for r in range(n)])
    lam = [sign * t for t in lam]
    order = sorted(range(n), key=lambda i: lam[i])
    lam = [lam[i] for i in order]
    cols = [vecs[i] for i in order]
    return lam, [[cols[c][r] for c in range(n)] for r in range(n)]


def _dc(a, b, stats):
    n = len(a)
    if n == 1:  # @line L1
        return [a[0]], [[1.0]]
    m = n // 2  # @line L2
    rho = b[m - 1]
    a1 = a[:m]
    a2 = a[m:]
    a1[-1] -= rho
    a2[0] -= rho
    d1, q1 = _dc(a1, b[:m - 1], stats)  # @line L3
    d2, q2 = _dc(a2, b[m:], stats)
    stats["merges"] += 1
    z = q1[-1][:] + q2[0][:]  # @line L4
    qmat = [row + [0.0] * (n - m) for row in q1] + [[0.0] * m + row for row in q2]
    return _merge(d1 + d2, qmat, z, rho, stats)


def eigh_tridiagonal(a, b):
    """Eigenvalues in descending order, unit eigenvectors as columns, and counters."""
    stats = {"merges": 0, "deflated": 0, "roots": 0, "secular_its": 0}
    if not a:
        return [], [], stats
    lam, q = _dc([float(t) for t in a], [float(t) for t in b], stats)
    lam = lam[::-1]  # @line L10
    q = [row[::-1] for row in q]
    return lam, q, stats
