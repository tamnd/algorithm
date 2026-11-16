# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/davenport-q-method/. The authors are listed in prov/98191D.jsonl.

"""Davenport's q-method for Wahba's problem.

Vectors are lists of 3 floats and matrices are lists of rows, as in rbm.py.
The reference vectors r_i are known in the space frame {s}; the body vectors
b_i are the same directions measured in the body frame {b}. The attitude
matrix is A = R_bs, so that b_i = A r_i for noise-free data. Wahba's loss is

    L(A) = 1/2 sum_i a_i |b_i - A r_i|^2,

with unit vectors and weights a_i > 0. The method returns the Hamilton
quaternion q (scalar first) of R_sb = A^T, so A = quat_to_rot(q)^T. With
B = sum_i a_i b_i r_i^T, the loss is lambda0 - q^T K q, where
lambda0 = sum_i a_i and K is Davenport's symmetric 4x4 matrix. The best q is
a unit eigenvector of K for its largest eigenvalue.
"""

import math

import rbm

JACOBI_TOL = 1e-15  # stop when the off-diagonal norm is below this times |K|
JACOBI_MAX_SWEEPS = 50


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


def davenport_matrix(bmat):
    """Return K = [[sigma, z^T], [z, S - sigma I]] for the attitude profile matrix B."""
    sigma = bmat[0][0] + bmat[1][1] + bmat[2][2]  # @line L2
    s = [[bmat[i][j] + bmat[j][i] for j in range(3)] for i in range(3)]  # @line L2
    # z = sum a_i b_i x r_i, read off the skew part of B: z_k = eps_kij B_ij
    z = [bmat[1][2] - bmat[2][1], bmat[2][0] - bmat[0][2], bmat[0][1] - bmat[1][0]]  # @line L2
    k = [[sigma, z[0], z[1], z[2]]]  # @line L3
    for i in range(3):
        k.append([z[i]] + [s[i][j] - (sigma if i == j else 0.0) for j in range(3)])
    return k


def jacobi_eigen(a, tol=JACOBI_TOL, max_sweeps=JACOBI_MAX_SWEEPS):
    """Return (eigenvalues, V) of a symmetric matrix by the cyclic Jacobi method.

    The columns of V are orthonormal eigenvectors: a V = V diag(eigenvalues).
    """
    n = len(a)
    m = [list(map(float, row)) for row in a]
    v = rbm.eye(n)
    scale = math.sqrt(sum(x * x for row in m for x in row)) or 1.0
    for _ in range(max_sweeps):
        off = math.sqrt(sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off <= tol * scale:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = (1.0 if theta >= 0.0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):  # columns p and q of m
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p] = c * mkp - s * mkq
                    m[k][q] = s * mkp + c * mkq
                for k in range(n):  # rows p and q of m
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k] = c * mpk - s * mqk
                    m[q][k] = s * mpk + c * mqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    else:
        raise ArithmeticError("Jacobi did not converge")
    return [m[i][i] for i in range(n)], v


def q_method(bs, rs, weights):
    """Return (q, loss): the optimal Hamilton quaternion of R_sb and the minimal Wahba loss."""
    bmat, lam0 = attitude_profile(bs, rs, weights)  # @line L1
    k = davenport_matrix(bmat)  # @line L3
    vals, vecs = jacobi_eigen(k)  # @line L4
    j = max(range(4), key=lambda i: vals[i])  # @line L5
    q = [vecs[i][j] for i in range(4)]  # @line L6
    n = rbm.norm(q)
    q = [x / n for x in q]
    if q[0] < 0.0:  # q and -q give the same rotation  # @line L6
        q = [-x for x in q]
    return q, max(0.0, lam0 - vals[j])  # @line L7


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
