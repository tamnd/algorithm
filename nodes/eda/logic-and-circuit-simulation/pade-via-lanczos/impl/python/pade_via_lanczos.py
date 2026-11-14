# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pade-via-lanczos/. The authors are listed in prov/JW00K7.jsonl.
"""Pade via Lanczos (PVL) for a linear circuit G x + s C x = b u, y = l^T x.

With the expansion point s0, K = G + s0 C, A = -K^{-1} C and r = K^{-1} b,
the transfer function is H(s0 + sigma) = l^T (I - sigma A)^{-1} r, whose
Taylor coefficients are the moments m_k = l^T A^k r. The nonsymmetric Lanczos
process on A with the start vectors r and l gives a q x q tridiagonal T_q, and
H_q(s0 + sigma) = (l^T r) e1^T (I - sigma T_q)^{-1} e1 matches m_0..m_{2q-1}.

The code works with float or Fraction entries; with Fraction it is exact.
Vectors are scaled by their largest entry, which keeps Fractions exact.
"""

import sim3dense


class Breakdown(ArithmeticError):
    """w_k^T v_k = 0 with nonzero v_k, w_k: the process needs look-ahead."""


def lu_factor(a):
    """Partial-pivoting LU of a square matrix: returns (lu, perm)."""
    n = len(a)
    lu = [list(row) for row in a]
    perm = list(range(n))
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(lu[i][k]))
        if lu[p][k] == 0:
            raise sim3dense.SingularMatrixError(f"zero pivot in column {k}")
        lu[k], lu[p] = lu[p], lu[k]
        perm[k], perm[p] = perm[p], perm[k]
        for i in range(k + 1, n):
            f = lu[i][k] / lu[k][k]
            lu[i][k] = f
            if f != 0:
                for j in range(k + 1, n):
                    lu[i][j] -= f * lu[k][j]
    return lu, perm


def lu_solve(fac, b):
    """Solve K x = b with the factors of K."""
    lu, perm = fac
    n = len(lu)
    y = [b[p] for p in perm]
    for i in range(n):
        y[i] = y[i] - sum(lu[i][k] * y[k] for k in range(i))
    for i in range(n - 1, -1, -1):
        y[i] = (y[i] - sum(lu[i][k] * y[k] for k in range(i + 1, n))) / lu[i][i]
    return y


def lu_solve_transposed(fac, b):
    """Solve K^T x = b with the same factors (P K = L U, so K^T = U^T L^T P)."""
    lu, perm = fac
    n = len(lu)
    z = list(b)
    for i in range(n):
        z[i] = (z[i] - sum(lu[k][i] * z[k] for k in range(i))) / lu[i][i]
    for i in range(n - 1, -1, -1):
        z[i] = z[i] - sum(lu[k][i] * z[k] for k in range(i + 1, n))
    x = [0 * z[0]] * n
    for i, p in enumerate(perm):
        x[p] = z[i]
    return x


def _dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def _scale(x):
    return max(abs(v) for v in x)


def pvl(G, C, b, l, s0, q, tol=0.0):
    """Run q steps of PVL. Returns (m0, T) with T the q x q tridiagonal matrix."""
    n = len(G)
    K = [[G[i][j] + s0 * C[i][j] for j in range(n)] for i in range(n)]
    fac = lu_factor(K)  # @line L1
    r = lu_solve(fac, b)
    rho, eta = _scale(r), _scale(l)
    if rho == 0 or eta == 0:
        raise ValueError("b and l must be nonzero")
    v, w = [x / rho for x in r], [x / eta for x in l]
    d = _dot(w, v)  # @line L2
    if abs(d) <= tol * _scale(v) * _scale(w) * n or d == 0:
        raise Breakdown("l^T r = 0")
    m0 = rho * eta * d
    alpha, beta, sub = [], [], []
    v_prev, w_prev, d_prev = [0 * x for x in v], [0 * x for x in w], None
    rho_k, eta_k = None, None
    for k in range(q):  # @line L3
        cv = sim3dense.matvec(C, v)
        av = [-x for x in lu_solve(fac, cv)]  # @line L4
        y = lu_solve_transposed(fac, w)
        aw = [-x for x in sim3dense.matvec(sim3dense.transpose(C), y)]
        a = _dot(w, av) / d  # @line L5
        bt = eta_k * d / d_prev if k else 0 * a
        gm = rho_k * d / d_prev if k else 0 * a
        alpha.append(a)
        if k:
            beta.append(bt)
        if k == q - 1:
            break
        vt = [x - a * y1 - bt * y0 for x, y1, y0 in zip(av, v, v_prev)]  # @line L6
        wt = [x - a * y1 - gm * y0 for x, y1, y0 in zip(aw, w, w_prev)]
        rho_k, eta_k = _scale(vt), _scale(wt)
        if rho_k == 0 or eta_k == 0:  # an invariant subspace: H_k is exact
            break
        v_prev, w_prev, d_prev = v, w, d
        v, w = [x / rho_k for x in vt], [x / eta_k for x in wt]
        d = _dot(w, v)  # @line L7
        if d == 0 or abs(d) <= tol * n:
            raise Breakdown(f"w^T v = 0 at step {k + 2}")
        sub.append(rho_k)
    size = len(alpha)
    T = [[0 * m0] * size for _ in range(size)]  # @line L8
    for i in range(size):
        T[i][i] = alpha[i]
        if i + 1 < size:
            T[i + 1][i] = sub[i]
            T[i][i + 1] = beta[i]
    return m0, T  # @line L9


def model_eval(m0, T, s0, s):
    """H_q(s) = m0 e1^T (I - (s - s0) T)^{-1} e1."""
    sig = s - s0
    n = len(T)
    M = [[(1 if i == j else 0) - sig * T[i][j] for j in range(n)] for i in range(n)]
    e1 = [1] + [0] * (n - 1)
    return m0 * sim3dense.solve(M, e1)[0]


def model_moments(m0, T, count):
    """m0 e1^T T^k e1 for k < count."""
    n = len(T)
    x = [1] + [0 * m0] * (n - 1)
    out = []
    for _ in range(count):
        out.append(m0 * x[0])
        x = [sum(T[i][j] * x[j] for j in range(n)) for i in range(n)]
    return out


def exact_moments(G, C, b, l, s0, count):
    """m_k = l^T A^k r, computed by repeated solves (as in AWE)."""
    n = len(G)
    fac = lu_factor([[G[i][j] + s0 * C[i][j] for j in range(n)] for i in range(n)])
    x = lu_solve(fac, b)
    out = []
    for _ in range(count):
        out.append(_dot(l, x))
        x = [-v for v in lu_solve(fac, sim3dense.matvec(C, x))]
    return out


def awe(moments, q):
    """Pade [q-1/q] from 2q moments by the Hankel system (AWE).

    Returns (num, den): num has q coefficients, den has q + 1 with den[0] = 1.
    """
    m = moments
    H = [[m[q + i - j - 1] for j in range(q)] for i in range(q)]
    rhs = [-m[q + i] for i in range(q)]
    tail = sim3dense.solve(H, rhs)
    den = [1] + tail
    num = [sum(den[j] * m[i - j] for j in range(i + 1)) for i in range(q)]
    return num, den


def rational_eval(num, den, sig):
    def poly(c):
        acc = 0
        for x in reversed(c):
            acc = acc * sig + x
        return acc

    return poly(num) / poly(den)


def transfer(G, C, b, l, s):
    n = len(G)
    Y = [[G[i][j] + s * C[i][j] for j in range(n)] for i in range(n)]
    return _dot(l, sim3dense.solve(Y, [complex(x) for x in b]))


def rlc_line(sections, r, ind, cap, rs, rl):
    """MNA matrices of a lumped RLC line: a 1 A source with resistance rs drives
    node 1; each section has a series r and ind and a cap to ground; rl
    terminates the far end. Unknowns: the node voltages, then the inductor
    currents. The output is the far-end voltage."""
    n = sections + 1  # nodes 0..sections, plus the inductor-current unknowns
    N = n + sections
    G = [[0.0] * N for _ in range(N)]
    C = [[0.0] * N for _ in range(N)]
    G[0][0] += 1 / rs
    G[n - 1][n - 1] += 1 / rl
    for k in range(sections):
        a, c, j = k, k + 1, n + k  # node a - r - L - node c, current j
        # the series r and L as one branch: e_a - e_c - r j - ind dj/dt = 0
        G[a][j] += 1
        G[c][j] -= 1
        G[j][a] += 1
        G[j][c] -= 1
        G[j][j] -= r
        C[j][j] -= ind
        C[c][c] += cap
    b = [0.0] * N
    b[0] = 1.0
    l = [0.0] * N
    l[n - 1] = 1.0
    return G, C, b, l
