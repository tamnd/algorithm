# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quest-algorithm/. The authors are listed in prov/Z02XZG.jsonl.

"""QUEST, the quaternion estimator of Shuster and Oh (1981), for Wahba's problem.

Vectors are lists of 3 floats and matrices are lists of rows, as in rbm.py.
The conventions are those of the q-method page: b_i = A r_i with A = R_bs,
B = sum a_i b_i r_i^T, sigma = tr B, S = B + B^T, z = sum a_i b_i x r_i,
and K = [[sigma, z^T], [z, S - sigma I]]. The result is the Hamilton
quaternion q (scalar first) of R_sb = A^T.

QUEST finds lambda_max of K as the largest root of the characteristic
polynomial

    psi(l) = l^4 - (a + b) l^2 - c l + (a b + c sigma - d),
    a = sigma^2 - kappa, b = sigma^2 + z^T z, c = Delta + z^T S z,
    d = z^T S^2 z, kappa = tr adj S, Delta = det S,

by Newton's method from lambda0 = sum a_i. The eigenvector is a column of
adj(l I - K), which is (gamma, x) with

    alpha = l^2 - sigma^2 + kappa, beta = l - sigma,
    gamma = (l + sigma) alpha - Delta, x = (alpha I + beta S + S^2) z.

That column is psi'(l) q0 q, so it vanishes when q0 = 0 (a rotation by pi).
The method of sequential rotations then rotates the reference vectors by
pi about a coordinate axis and solves again.
"""

import rbm

NEWTON_TOL = 1e-15  # stop when the Newton step is below this times lambda0
NEWTON_MAX_ITER = 50


def _unit(v):
    n = rbm.norm(v)
    if n == 0.0:
        raise ValueError("zero vector")
    return [x / n for x in v]


def attitude_profile(bs, rs, weights):
    """Return B = sum a_i b_i r_i^T and lambda0 = sum a_i, after making all vectors unit."""
    if not (len(bs) == len(rs) == len(weights)) or len(bs) == 0:
        raise ValueError("need the same positive number of body vectors, reference vectors and weights")
    bmat = rbm.zeros(3, 3)
    for a, b, r in zip(weights, bs, rs):
        if a <= 0.0:
            raise ValueError("weights must be positive")
        bu, ru = _unit(b), _unit(r)
        for i in range(3):
            for j in range(3):
                bmat[i][j] += a * bu[i] * ru[j]
    return bmat, float(sum(weights))


def profile_terms(bmat):
    """Return sigma, S, z, kappa, Delta for the attitude profile matrix B."""
    sigma = bmat[0][0] + bmat[1][1] + bmat[2][2]
    s = [[bmat[i][j] + bmat[j][i] for j in range(3)] for i in range(3)]
    z = [bmat[1][2] - bmat[2][1], bmat[2][0] - bmat[0][2], bmat[0][1] - bmat[1][0]]
    # kappa = trace of the adjugate = sum of the principal 2x2 minors
    kappa = (s[1][1] * s[2][2] - s[1][2] * s[2][1]) + (s[0][0] * s[2][2] - s[0][2] * s[2][0]) + (
        s[0][0] * s[1][1] - s[0][1] * s[1][0]
    )
    delta = rbm.det(s)
    return sigma, s, z, kappa, delta


def char_poly(bmat):
    """Return (p2, p1, p0) with psi(l) = l^4 + p2 l^2 + p1 l + p0 = det(l I - K)."""
    sigma, s, z, kappa, delta = profile_terms(bmat)
    sz = rbm.matvec(s, z)
    a = sigma * sigma - kappa
    b = sigma * sigma + rbm.dot(z, z)
    c = delta + rbm.dot(z, sz)
    d = rbm.dot(sz, sz)
    return -(a + b), -c, a * b + c * sigma - d


def newton_lambda(bmat, lam0, tol=NEWTON_TOL, max_iter=NEWTON_MAX_ITER):
    """Return (lambda_max, number of Newton steps), starting from lambda0."""
    p2, p1, p0 = char_poly(bmat)  # @line L2
    lam = lam0  # @line L3
    for it in range(1, max_iter + 1):
        psi = ((lam * lam + p2) * lam + p1) * lam + p0  # @line L4
        dpsi = (4.0 * lam * lam + 2.0 * p2) * lam + p1  # @line L4
        if dpsi == 0.0:
            return lam, it
        step = psi / dpsi  # @line L4
        # From above, every exact Newton step is positive. A step that is not
        # positive, or tiny, means rounding has taken over: stop there.
        if step <= tol * lam0:
            if step > 0.0:
                lam -= step
            return lam, it
        lam -= step  # @line L4
    raise ArithmeticError("Newton did not converge")


def adjugate_column(bmat, lam):
    """Return (gamma, x) = the first column of adj(lam I - K), and psi'(lam)."""
    sigma, s, z, kappa, delta = profile_terms(bmat)
    alpha = lam * lam - sigma * sigma + kappa  # @line L6
    beta = lam - sigma  # @line L6
    gamma = (lam + sigma) * alpha - delta  # @line L6
    sz = rbm.matvec(s, z)
    ssz = rbm.matvec(s, sz)
    x = [alpha * z[i] + beta * sz[i] + ssz[i] for i in range(3)]  # @line L6
    p2, p1, _ = char_poly(bmat)
    dpsi = (4.0 * lam * lam + 2.0 * p2) * lam + p1
    return [gamma] + x, dpsi


def _rotated_profile(bmat, k):
    """Return B P_k, the profile after the reference vectors turn by pi about axis k."""
    if k is None:
        return bmat
    sign = [1.0 if j == k else -1.0 for j in range(3)]
    return [[bmat[i][j] * sign[j] for j in range(3)] for i in range(3)]


def quest(bs, rs, weights, tol=NEWTON_TOL, max_iter=NEWTON_MAX_ITER):
    """Return (q, loss, info) for Wahba's problem.

    q is the Hamilton quaternion of R_sb with q0 >= 0, loss = lambda0 - lambda_max,
    and info holds the number of Newton steps and the frame used (None, 0, 1 or 2).
    """
    bmat, lam0 = attitude_profile(bs, rs, weights)  # @line L1
    lam, iters = newton_lambda(bmat, lam0, tol, max_iter)  # @line L4
    best = None
    for k in (None, 0, 1, 2):  # @line L5
        col, dpsi = adjugate_column(_rotated_profile(bmat, k), lam)  # @line L6
        n = rbm.norm(col)
        if best is None or n > best[0]:
            best = (n, k, col)
        if n >= 0.5 * abs(dpsi):  # |q0| >= 1/2 in this frame  # @line L7
            break
    n, k, col = best
    if n == 0.0:
        raise ArithmeticError("no frame gave a nonzero eigenvector; lambda_max is not simple")
    qk = [x / n for x in col]  # @line L8
    if k is None:
        q = qk
    else:
        # R_sb = P_k R'_sb, and the quaternion of P_k is (0, e_k).
        p = [0.0, 0.0, 0.0, 0.0]
        p[k + 1] = 1.0
        q = rbm.quat_mul(p, qk)  # @line L8
    if q[0] < 0.0:
        q = [-x for x in q]
    return q, max(0.0, lam0 - lam), {"iterations": iters, "frame": k}  # @line L9


def attitude_matrix(q):
    """Return A = R_bs for the Hamilton quaternion q of R_sb."""
    return rbm.transpose(rbm.quat_to_rot(q))


def wahba_loss(amat, bs, rs, weights):
    """Return L(A) = 1/2 sum a_i |b_i - A r_i|^2 with unit vectors."""
    total = 0.0
    for a, b, r in zip(weights, bs, rs):
        d = rbm.sub(_unit(b), rbm.matvec(amat, _unit(r)))
        total += 0.5 * a * rbm.dot(d, d)
    return total
