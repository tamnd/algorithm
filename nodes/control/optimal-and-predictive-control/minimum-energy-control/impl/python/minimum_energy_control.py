# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-energy-control/. The authors are listed in prov/H8NC6E.jsonl.

"""Minimum-energy control of a linear system, in continuous and discrete time.

Continuous time: steer x' = A x + B u from x(0) = x0 to x(t1) = x1 with the
least energy, the integral of |u(t)|^2 over [0, t1]. The answer is

    u(t) = B^T e^(A^T (t1 - t)) W^(-1) d,   d = x1 - e^(A t1) x0,

with the controllability Gramian W = int_0^t1 e^(A s) B B^T e^(A^T s) ds,
and the least energy is d^T W^(-1) d. The Gramian comes from one matrix
exponential of size 2n (Van Loan's block method). Floating point.

Discrete time: steer x_(k+1) = A x_k + B u_k from x0 to x_N = x1 with the
least sum of |u_k|^2. The answer uses the N-step Gramian
W_N = sum_j A^j B B^T (A^T)^j. Exact with int and Fraction data.
"""

from fractions import Fraction
from typing import Callable, List, Sequence, Tuple, Union

import ctlmat as cm

Num = Union[int, float, Fraction]
Matrix = List[List[Num]]


def gramian(A: Sequence[Sequence[Num]], B: Sequence[Sequence[Num]], t1: float) -> List[List[float]]:
    """Return W(t1) = int_0^t1 e^(A s) B B^T e^(A^T s) ds.

    Van Loan: the exponential of [[-A, B B^T], [0, A^T]] t1 is
    [[., G], [0, F]] with F = e^(A^T t1) and G = e^(-A t1) W(t1), so
    W(t1) = F^T G. Cost: one exponential of a 2n by 2n matrix, O(n^3 log(|A| t1)).
    """
    n = len(A)
    a = [[float(v) for v in row] for row in A]
    b = [[float(v) for v in row] for row in B]
    bbt = cm.mul(b, cm.transpose(b))
    m = cm.block([[cm.scale(-1.0, a), bbt], [0, cm.transpose(a)]])
    e = cm.expm(cm.scale(float(t1), m))
    g = [row[n:] for row in e[:n]]
    f = [row[n:] for row in e[n:]]
    w = cm.mul(cm.transpose(f), g)
    return [[(w[i][j] + w[j][i]) / 2 for j in range(n)] for i in range(n)]


def minimum_energy_control(
    A: Sequence[Sequence[Num]],
    B: Sequence[Sequence[Num]],
    x0: Sequence[Num],
    x1: Sequence[Num],
    t1: float,
    rel_tol: float = 1e-12,
) -> Tuple[Callable[[float], List[float]], float, List[float]]:
    """Return (u, energy, eta) for the transfer from x0 at time 0 to x1 at time t1.

    u(t) is the optimal input as a list of m floats, energy is the least value
    of int_0^t1 |u|^2 dt, and eta = W^(-1) d. Precondition: t1 > 0. Raises
    ValueError if the Gramian is not positive definite within rel_tol times its
    largest entry, that is, if (A, B) is not controllable in the precision used.
    Cost: O(n^3 log(|A| t1)) once, then O(n^3 log(|A| t1)) per call of u.
    """
    if not t1 > 0:
        raise ValueError("t1 must be positive")
    a = [[float(v) for v in row] for row in A]
    b = [[float(v) for v in row] for row in B]
    w = gramian(a, b, t1)  # @line L1
    big = max(abs(v) for row in w for v in row)
    if big == 0.0 or not cm.is_pos_def(w, rel_tol * big):  # @line L2
        raise ValueError("the Gramian is singular: x1 cannot be reached from every x0")
    phi = cm.expm(cm.scale(float(t1), a))
    d = [float(v) - s for v, s in zip(x1, cm.matvec(phi, [float(v) for v in x0]))]  # @line L3
    eta = cm.solve(w, d)  # @line L4
    bt, at = cm.transpose(b), cm.transpose(a)

    def u(t: float) -> List[float]:
        return cm.matvec(bt, cm.matvec(cm.expm(cm.scale(t1 - t, at)), eta))  # @line L5

    energy = cm.dot(d, eta)  # @line L6
    return u, energy, eta


def reach_matrix(A: Sequence[Sequence[Num]], B: Sequence[Sequence[Num]], N: int) -> Matrix:
    """Return [A^(N-1) B, A^(N-2) B, ..., B], so that x_N = A^N x0 + C u for u = (u_0, ..., u_(N-1))."""
    blocks = []
    p = [list(row) for row in B]
    for _ in range(N):
        blocks.append(p)
        p = cm.mul(A, p)
    blocks.reverse()
    return [sum((blk[i] for blk in blocks), []) for i in range(len(A))]


def minimum_energy_discrete(
    A: Sequence[Sequence[Num]],
    B: Sequence[Sequence[Num]],
    x0: Sequence[Num],
    x1: Sequence[Num],
    N: int,
) -> Tuple[List[List[Num]], Num]:
    """Return (us, energy): the inputs u_0, ..., u_(N-1) of least sum |u_k|^2 with x_N = x1.

    us[k] = B^T (A^T)^(N-1-k) W_N^(-1) d with d = x1 - A^N x0 and
    W_N = C C^T for C = reach_matrix(A, B, N); energy = d^T W_N^(-1) d.
    Exact (Fraction) with int and Fraction data. Raises ValueError if W_N is
    singular. Cost: O(N n^2 m + n^3).
    """
    if N < 1:
        raise ValueError("N must be at least 1")
    c = reach_matrix(A, B, N)
    w = cm.mul(c, cm.transpose(c))
    d = [v - s for v, s in zip(x1, cm.matvec(cm.mat_power(A, N), list(x0)))]
    eta = cm.solve(w, d)
    flat = cm.matvec(cm.transpose(c), eta)
    m = len(B[0])
    us = [flat[k * m:(k + 1) * m] for k in range(N)]
    return us, cm.dot(d, eta)
