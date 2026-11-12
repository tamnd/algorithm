# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-kalman-filter/.

"""Extended Kalman filter for a nonlinear state space model with additive
Gaussian noise.

Model: x_0 ~ N(m0, P0), x_t = f(x_(t-1)) + q_t with q_t ~ N(0, Q),
y_t = h(x_t) + r_t with r_t ~ N(0, R), for t = 1..T.

f and h map a vector (a list) to a vector. F_jac and H_jac return their
Jacobian matrices (lists of rows) at a given point. With linear f and h the
filter is the Kalman filter, and it runs exactly on fractions.Fraction.
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
                g = m[r][c]
                m[r] = [x - g * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def extended_kalman_filter(f, F_jac, h, H_jac, Q, R, m0, P0, ys):
    """Return the filtered means and covariances; index 0 is the prior and
    index t is the estimate of x_t given y_1..y_t."""
    m, P = list(m0), [list(r) for r in P0]  # @line L1
    means, covs = [m], [P]
    for y in ys:  # @line L2
        F = F_jac(m)  # @line L3
        mp = f(m)  # @line L4
        Pp = mat_add(mat_mul(mat_mul(F, P), transpose(F)), Q)
        H = H_jac(mp)  # @line L5
        Ht = transpose(H)
        S = mat_add(mat_mul(mat_mul(H, Pp), Ht), R)  # @line L6
        K = mat_mul(mat_mul(Pp, Ht), inverse(S))
        m = vec_add(mp, mat_vec(K, vec_add(y, h(mp), -1)))  # @line L7
        P = mat_add(Pp, mat_mul(mat_mul(K, S), transpose(K)), -1)
        means.append(m)
        covs.append(P)
    return means, covs  # @line L8
