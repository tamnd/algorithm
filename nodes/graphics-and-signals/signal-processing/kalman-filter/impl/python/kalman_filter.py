# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kalman-filter/. The authors are listed in prov/74AZEE.jsonl.

"""The Kalman filter for the linear Gaussian state-space model

    x_t = A x_{t-1} + q_t,   q_t ~ N(0, Q)
    y_t = C x_t + r_t,       r_t ~ N(0, R),   x_0 ~ N(m0, P0),

with independent noise terms. For t = 1..T it returns the mean m_t and the
covariance P_t of x_t given y_1..y_t. Matrices are lists of rows; with
Fraction entries every value is exact. Each step costs O(n^3 + n^2 k + n k^2 + k^3)
for a state of size n and an observation of size k.
"""

from typing import Sequence

Matrix = list[list]


def matmul(a: Sequence[Sequence], b: Sequence[Sequence]) -> Matrix:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: Sequence[Sequence]) -> Matrix:
    return [list(col) for col in zip(*a)]


def add(a: Sequence[Sequence], b: Sequence[Sequence], sign: int = 1) -> Matrix:
    return [[x + sign * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def inverse(a: Sequence[Sequence]) -> Matrix:
    """Gauss-Jordan inverse with partial pivoting; exact on Fraction."""
    n = len(a)
    m = [list(row) + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda i: abs(m[i][c]))
        if m[piv][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[piv] = m[piv], m[c]
        pv = m[c][c]
        m[c] = [v / pv for v in m[c]]
        for i in range(n):
            if i != c and m[i][c] != 0:
                f = m[i][c]
                m[i] = [u - f * v for u, v in zip(m[i], m[c])]
    return [row[n:] for row in m]


def kalman_step(m: Sequence[Sequence], p: Sequence[Sequence], y: Sequence[Sequence],
                a: Sequence[Sequence], q: Sequence[Sequence],
                c: Sequence[Sequence], r: Sequence[Sequence]) -> tuple[Matrix, Matrix, Matrix, Matrix]:
    """One predict and update step. m and y are column vectors (lists of 1-element rows).

    Returns the new mean, the new covariance, the innovation v and its covariance S.
    """
    m_pred = matmul(a, m)  # @line L3
    p_pred = add(matmul(matmul(a, p), transpose(a)), q)  # @line L4
    v = add(y, matmul(c, m_pred), -1)  # @line L5
    s = add(matmul(matmul(c, p_pred), transpose(c)), r)  # @line L6
    k = matmul(matmul(p_pred, transpose(c)), inverse(s))  # @line L7
    m_new = add(m_pred, matmul(k, v))  # @line L8
    p_new = add(p_pred, matmul(matmul(k, s), transpose(k)), -1)  # @line L9
    return m_new, p_new, v, s


def kalman_filter(m0: Sequence[Sequence], p0: Sequence[Sequence], a: Sequence[Sequence],
                  q: Sequence[Sequence], c: Sequence[Sequence], r: Sequence[Sequence],
                  ys: Sequence[Sequence[Sequence]]) -> list[tuple[Matrix, Matrix]]:
    """Run the filter on observations y_1..y_T; return [(m_t, P_t) for t = 1..T]."""
    m, p = [list(row) for row in m0], [list(row) for row in p0]  # @line L1
    out = []
    for y in ys:  # @line L2
        m, p, _, _ = kalman_step(m, p, y, a, q, c, r)
        out.append((m, p))  # @line L10
    return out


def scalar_kalman(m0, p0, a, q, c, r, ys: Sequence) -> list[tuple]:
    """The filter for a scalar state and scalar observations, as numbers."""
    out = kalman_filter([[m0]], [[p0]], [[a]], [[q]], [[c]], [[r]], [[[y]] for y in ys])
    return [(m[0][0], p[0][0]) for m, p in out]
