# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triad-method/. The authors are listed in prov/FY3PHK.jsonl.

"""The TRIAD method of Black (1964) for the attitude from two vector pairs.

Vectors are lists of 3 floats and matrices are lists of rows, as in rbm.py.
The reference vectors r1, r2 are known in the space frame {s} (for example
the direction of the Sun and the magnetic field from a model). The body
vectors b1, b2 are the same directions measured in the body frame {b}.
The method returns the attitude matrix A = R_bs, so that b_i = A r_i for
noise-free data. The rotation R_sb of the body in space is A^T.

The first pair is matched exactly: A r1 / |r1| = b1 / |b1|. The second pair
only fixes the rotation about that direction. The method is not the least
squares solution of Wahba's problem.
"""

import rbm

COLLINEAR_TOL = 1e-12  # |b1 x b2| / (|b1| |b2|) below this counts as collinear


def _unit(v):
    n = rbm.norm(v)
    if n == 0.0:
        raise ValueError("zero vector")
    return [x / n for x in v]


def _triad_frame(v1, v2):
    """Return the columns t1, t2, t3 of the orthonormal frame built from v1, v2."""
    t1 = _unit(v1)  # @line L1
    c = rbm.cross(v1, v2)  # @line L2
    if rbm.norm(c) <= COLLINEAR_TOL * rbm.norm(v1) * rbm.norm(v2):  # @line L3
        raise ValueError("the two vectors are collinear; TRIAD needs two independent directions")
    t2 = _unit(c)  # @line L4
    t3 = rbm.cross(t1, t2)  # @line L5
    return t1, t2, t3


def triad(b1, b2, r1, r2):
    """Return A = R_bs with A r1 parallel to b1, from two body and two reference vectors."""
    tb = _triad_frame(b1, b2)  # @line L1
    tr = _triad_frame(r1, r2)  # @line L1
    # A = [t1 t2 t3]_b [t1 t2 t3]_r^T, a sum of three outer products
    return [[sum(tb[k][i] * tr[k][j] for k in range(3)) for j in range(3)] for i in range(3)]  # @line L6


def wahba_loss(A, bs, rs, weights):
    """Return L(A) = 1/2 sum a_i |b_i - A r_i|^2 (the cost of Wahba's problem)."""
    total = 0.0
    for a, b, r in zip(weights, bs, rs):
        d = rbm.sub(b, rbm.matvec(A, r))
        total += 0.5 * a * rbm.dot(d, d)
    return total
