# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-learning-control/. The authors are listed in prov/0W0JD2.jsonl.

"""Iterative learning control for a discrete-time plant that repeats a task.

The plant is x(k+1) = A x(k) + B u(k), y(k) = C x(k), with a single input
and a single output and C B != 0 (relative degree one). Each trial starts
from the same state x0 and lasts N samples: the input u(0), ..., u(N-1)
gives the outputs y(1), ..., y(N). In lifted form y = P u + d, where P is
the N by N lower triangular Toeplitz matrix of the Markov parameters
P[i][j] = C A^(i-j) B and d is the free response from x0.

The learning law is u_(j+1) = Q (u_j + L e_j) with e_j = y_d - y_j. For
Q = I the error obeys e_(j+1) = (I - P L) e_j exactly.

With int or Fraction data every routine is exact (Fraction arithmetic).
"""

from ctlmat import eye, matvec, mul, solve, sub, transpose, add, scale

__all__ = ["run_trial", "lifted_matrix", "ilc", "p_type", "plant_inverse", "norm_optimal", "error_map"]


def run_trial(A, B, C, x0, u):
    """Simulate one trial and return y(1), ..., y(N) for the inputs u(0..N-1)."""
    x = list(x0)
    ys = []
    for uk in u:
        x = [s + b * uk for s, b in zip(matvec(A, x), B)]
        ys.append(sum(c * v for c, v in zip(C, x)))
    return ys


def lifted_matrix(A, B, C, N):
    """Return the lifted plant P with P[i][j] = C A^(i-j) B for i >= j."""
    h = []
    v = list(B)
    for _ in range(N):
        h.append(sum(c * w for c, w in zip(C, v)))
        v = matvec(A, v)
    return [[h[i - j] if i >= j else 0 for j in range(N)] for i in range(N)]


def p_type(gamma, N):
    """The P-type (Arimoto) learning matrix L = gamma I."""
    return scale(gamma, eye(N))


def plant_inverse(P):
    """The inverse learning matrix L = P^(-1); one trial removes the error."""
    return solve(P, eye(len(P)))


def norm_optimal(P, w):
    """The norm-optimal learning matrix L = (P^T P + w I)^(-1) P^T, w > 0."""
    Pt = transpose(P)
    return solve(add(mul(Pt, P), scale(w, eye(len(P)))), Pt)


def ilc(trial, yd, u0, L, trials, Q=None):
    """Run the learning loop for a number of trials.

    trial(u) runs the plant once and returns the outputs. Returns (us, es):
    the inputs and errors of trials 0, ..., trials (one more than the number
    of updates).
    """
    u = list(u0)  # @line L1
    us, es = [], []
    for _ in range(trials + 1):  # @line L2
        y = trial(u)  # @line L3
        e = [r - v for r, v in zip(yd, y)]  # @line L4
        us.append(u)
        es.append(e)
        u = [a + b for a, b in zip(u, matvec(L, e))]  # @line L5
        if Q is not None:
            u = matvec(Q, u)
    return us, es  # @line L6


def error_map(P, L):
    """Return I - P L, the matrix that maps e_j to e_(j+1) when Q = I."""
    return sub(eye(len(P)), mul(P, L))
