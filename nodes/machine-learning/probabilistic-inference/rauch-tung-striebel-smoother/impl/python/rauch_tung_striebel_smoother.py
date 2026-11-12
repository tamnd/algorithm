# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rauch-tung-striebel-smoother/. The authors are listed in prov/Z7JZYG.jsonl.

"""Rauch-Tung-Striebel smoother for a linear Gaussian state space model.

Model: x_0 ~ N(m0, P0), x_t = A x_(t-1) + q_t with q_t ~ N(0, Q),
y_t = H x_t + r_t with r_t ~ N(0, R), for t = 1..T.

Vectors are lists, matrices are lists of rows. The code uses only +, -, *
and / so it runs exactly on fractions.Fraction entries.
"""


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def mat_vec(a, v):
    return [sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def mat_add(a, b, sign=1):
    return [[x + sign * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def vec_add(a, b, sign=1):
    return [x + sign * y for x, y in zip(a, b)]


def inverse(a):
    """Gauss-Jordan elimination with partial pivoting."""
    n = len(a)
    m = [list(a[i]) + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def kalman_filter(A, Q, H, R, m0, P0, ys):
    """Return the predicted and filtered moments; index 0 of the filtered
    lists is the prior at t = 0, index t is time t."""
    At, Ht = transpose(A), transpose(H)
    mf, Pf = [list(m0)], [[list(r) for r in P0]]  # @line L1
    mp, Pp = [None], [None]
    for y in ys:  # @line L2
        m = mat_vec(A, mf[-1])  # @line L3
        P = mat_add(mat_mul(mat_mul(A, Pf[-1]), At), Q)
        S = mat_add(mat_mul(mat_mul(H, P), Ht), R)  # @line L4
        K = mat_mul(mat_mul(P, Ht), inverse(S))
        mp.append(m)
        Pp.append(P)
        mf.append(vec_add(m, mat_vec(K, vec_add(y, mat_vec(H, m), -1))))  # @line L5
        Pf.append(mat_add(P, mat_mul(mat_mul(K, S), transpose(K)), -1))
    return mp, Pp, mf, Pf


def rts_smoother(A, Q, H, R, m0, P0, ys):
    """Return the smoothed means and covariances of x_0, ..., x_T."""
    mp, Pp, mf, Pf = kalman_filter(A, Q, H, R, m0, P0, ys)
    T = len(ys)
    ms, Ps = [None] * (T + 1), [None] * (T + 1)
    ms[T], Ps[T] = mf[T], Pf[T]  # @line L6
    At = transpose(A)
    for t in range(T - 1, -1, -1):  # @line L7
        C = mat_mul(mat_mul(Pf[t], At), inverse(Pp[t + 1]))  # @line L8
        ms[t] = vec_add(mf[t], mat_vec(C, vec_add(ms[t + 1], mp[t + 1], -1)))  # @line L9
        D = mat_add(Ps[t + 1], Pp[t + 1], -1)
        Ps[t] = mat_add(Pf[t], mat_mul(mat_mul(C, D), transpose(C)))  # @line L10
    return ms, Ps  # @line L11
