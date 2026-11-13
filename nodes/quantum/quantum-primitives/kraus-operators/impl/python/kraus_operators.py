# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kraus-operators/. The authors are listed in prov/XS6DA3.jsonl.
"""Kraus operators of a quantum channel, and the Stinespring and Choi forms.

A channel from C^din to C^dout is a list of dout x din matrices K_k. It maps
rho to sum_k K_k rho K_k^dagger. The Choi matrix is ordered output tensor input:
J = sum_ij Phi(|i><j|) tensor |i><j|, with index o * din + i.
"""

import math
from typing import List, Sequence

from qsim import Matrix, I2, X, Y, Z, add, dagger, eigh, identity, matmul, max_abs_diff, scale, trace_out_second, zeros


def apply_channel(kraus: Sequence[Matrix], rho: Matrix) -> Matrix:
    """sum_k K_k rho K_k^dagger."""
    dout = len(kraus[0])
    out = zeros(dout)
    for k in kraus:
        out = add(out, matmul(matmul(k, rho), dagger(k)))
    return out


def completeness(kraus: Sequence[Matrix]) -> Matrix:
    """sum_k K_k^dagger K_k. It equals I exactly when the channel preserves the trace."""
    din = len(kraus[0][0])
    out = zeros(din)
    for k in kraus:
        out = add(out, matmul(dagger(k), k))
    return out


def is_trace_preserving(kraus: Sequence[Matrix], tol: float = 1e-9) -> bool:
    return max_abs_diff(completeness(kraus), identity(len(kraus[0][0]))) <= tol


def stinespring_isometry(kraus: Sequence[Matrix]) -> Matrix:
    """V = sum_k K_k tensor |k>, a (dout * r) x din matrix with row index o * r + k."""
    r, dout, din = len(kraus), len(kraus[0]), len(kraus[0][0])
    return [[kraus[k][o][i] for i in range(din)] for o in range(dout) for k in range(r)]


def apply_by_stinespring(kraus: Sequence[Matrix], rho: Matrix) -> Matrix:
    """Tr_E (V rho V^dagger): embed with the isometry, then trace out the environment."""
    v = stinespring_isometry(kraus)
    return trace_out_second(matmul(matmul(v, rho), dagger(v)), len(kraus[0]), len(kraus))


def choi_matrix(kraus: Sequence[Matrix]) -> Matrix:
    """J = sum_ij Phi(|i><j|) tensor |i><j| (output first)."""
    dout, din = len(kraus[0]), len(kraus[0][0])
    j = zeros(dout * din)
    for i1 in range(din):
        for i2 in range(din):
            unit = [[1 if (r, c) == (i1, i2) else 0 for c in range(din)] for r in range(din)]
            block = apply_channel(kraus, unit)
            for o1 in range(dout):
                for o2 in range(dout):
                    j[o1 * din + i1][o2 * din + i2] = block[o1][o2]
    return j


def kraus_from_choi(j: Matrix, din: int, dout: int, tol: float = 1e-10) -> List[Matrix]:
    """Kraus operators K_k = sqrt(lambda_k) unvec(v_k) from the eigenvectors of J.

    The number of operators is rank J, which is at most din * dout.
    """
    vals, vecs = eigh(j)
    out = []
    for k, lam in enumerate(vals):
        if lam > tol:
            s = math.sqrt(lam)
            out.append([[s * vecs[o * din + i][k] for i in range(din)] for o in range(dout)])
    return out


def mix_kraus(kraus: Sequence[Matrix], u: Matrix) -> List[Matrix]:
    """F_j = sum_k u_jk K_k. For a unitary u this is the same channel."""
    out = []
    for row in u:
        f = zeros(len(kraus[0]), len(kraus[0][0]))
        for c, k in zip(row, kraus):
            f = add(f, scale(c, k))
        out.append(f)
    return out


def compose(second: Sequence[Matrix], first: Sequence[Matrix]) -> List[Matrix]:
    """Kraus operators of 'first, then second': all products B_l A_k."""
    return [matmul(b, a) for b in second for a in first]


# ---------------------------------------------------------------- standard qubit channels


def bit_flip(p: float) -> List[Matrix]:
    """X with probability p."""
    return [scale(math.sqrt(1 - p), I2), scale(math.sqrt(p), X)]


def phase_flip(p: float) -> List[Matrix]:
    """Z with probability p."""
    return [scale(math.sqrt(1 - p), I2), scale(math.sqrt(p), Z)]


def depolarizing(p: float) -> List[Matrix]:
    """rho -> (1 - p) rho + p I / 2, as (1 - 3p/4) rho + (p/4)(X rho X + Y rho Y + Z rho Z)."""
    return [scale(math.sqrt(1 - 3 * p / 4), I2)] + [scale(math.sqrt(p / 4), m) for m in (X, Y, Z)]


def amplitude_damping(gamma: float) -> List[Matrix]:
    """|1> decays to |0> with probability gamma."""
    return [[[1, 0], [0, math.sqrt(1 - gamma)]], [[0, math.sqrt(gamma)], [0, 0]]]


def phase_damping(lam: float) -> List[Matrix]:
    """Off-diagonal entries shrink by sqrt(1 - lam); populations stay."""
    return [[[1, 0], [0, math.sqrt(1 - lam)]], [[0, 0], [0, math.sqrt(lam)]]]
