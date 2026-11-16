# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/se-sync/. The authors are listed in prov/ZTRAGF.jsonl.

"""The SE-Sync pipeline (Rosen, Carlone, Bandeira and Leonard 2019) on small
planar rotation synchronization problems.

The unknowns are n rotations R_i in SO(2). Each edge (i, j, Rt, kappa) is a
measurement Rt of R_i^T R_j with the weight kappa > 0. The cost is

    F(R) = sum over the edges of kappa || R_j - R_i Rt ||_F^2 = tr(Q R^T R),

where R = [R_1 ... R_n] is 2 x 2n and Q is the 2n x 2n connection Laplacian.
In SE-Sync the translations of a pose graph are removed in closed form, which
leaves a problem of this same form with a matrix Q that also holds the
translation terms; the code starts from Q, so it covers the rotation part.

The pipeline:
  1. Relax SO(2) to the Stiefel manifold St(2, r): Y = [Y_1 ... Y_n] is
     r x 2n with Y_i^T Y_i = I. min tr(Q Y^T Y) is the Burer-Monteiro form of
     the semidefinite relaxation min tr(Q Z), Z >= 0, Z_ii = I.
  2. Find a critical point Y by a local search (here block coordinate descent:
     each Y_i has a closed form minimizer, the polar factor).
  3. Certificate: Lambda_i = Sym(sum_j Q_ij Y_j^T Y_i), S = Q - Lambda.
     If S is positive semidefinite, Z = Y^T Y solves the relaxation.
  4. If not, the eigenvector v of the least eigenvalue of S gives a descent
     direction at [Y; 0] in St(2, r + 1): go up one step of the staircase.
  5. Round: take the top 2 rows of U^T Y from the SVD of Y, fix the sign of
     the determinant, and project each block onto SO(2).
The lower bound tr(Q Y^T Y) and the upper bound F(R) bracket the optimum.
"""

import math

# ------------------------------------------------------------- small algebra


def rot(a):
    c, s = math.cos(a), math.sin(a)
    return [[c, -s], [s, c]]


def angle(r):
    return math.atan2(r[1][0], r[0][0])


def matmul(a, b):
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def transpose(a):
    return [list(r) for r in zip(*a)]


def symmetric_eigen(a, tol=1e-14, max_sweeps=100):
    """Cyclic Jacobi: return (eigenvalues ascending, eigenvectors as columns)."""
    n = len(a)
    a = [list(r) for r in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off <= tol * tol * max(1.0, sum(a[i][i] ** 2 for i in range(n))):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                th = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    idx = sorted(range(n), key=lambda i: a[i][i])
    return [a[i][i] for i in idx], [[v[k][i] for i in idx] for k in range(n)]


def polar_factor(g):
    """The r x 2 matrix with orthonormal columns nearest to g: g (g^T g)^(-1/2)."""
    a = sum(row[0] * row[0] for row in g)
    b = sum(row[0] * row[1] for row in g)
    d = sum(row[1] * row[1] for row in g)
    mean, half = 0.5 * (a + d), math.hypot(0.5 * (a - d), b)
    l1, l2 = mean + half, mean - half
    if l2 <= 1e-24 * max(1.0, l1):
        raise ValueError("the block has rank below 2")
    if abs(b) > 1e-300 or abs(a - d) > 1e-300:
        phi = 0.5 * math.atan2(2.0 * b, a - d)
    else:
        phi = 0.0
    c, s = math.cos(phi), math.sin(phi)
    # g^T g = V diag(l1, l2) V^T with V = [[c, -s], [s, c]]
    w1, w2 = 1.0 / math.sqrt(l1), 1.0 / math.sqrt(l2)
    m = [[c * c * w1 + s * s * w2, c * s * (w1 - w2)], [c * s * (w1 - w2), s * s * w1 + c * c * w2]]
    return [[row[0] * m[0][0] + row[1] * m[1][0], row[0] * m[0][1] + row[1] * m[1][1]] for row in g]


# ----------------------------------------------------------- the problem


def connection_laplacian(n, edges):
    q = [[0.0] * (2 * n) for _ in range(2 * n)]
    for i, j, rt, kappa in edges:
        for a in range(2):
            q[2 * i + a][2 * i + a] += kappa
            q[2 * j + a][2 * j + a] += kappa
            for b in range(2):
                q[2 * i + a][2 * j + b] -= kappa * rt[a][b]
                q[2 * j + b][2 * i + a] -= kappa * rt[a][b]
    return q


def objective(edges, rs):
    """F(R) = sum kappa || R_j - R_i Rt ||_F^2."""
    tot = 0.0
    for i, j, rt, kappa in edges:
        p = matmul(rs[i], rt)
        tot += kappa * sum((rs[j][a][b] - p[a][b]) ** 2 for a in range(2) for b in range(2))
    return tot


def block(y, i):
    return [[row[2 * i], row[2 * i + 1]] for row in y]


def set_block(y, i, b):
    for row, br in zip(y, b):
        row[2 * i], row[2 * i + 1] = br[0], br[1]


def relaxed_cost(q, y):
    """tr(Q Y^T Y)."""
    yq = matmul(y, q)
    return sum(yq[k][c] * y[k][c] for k in range(len(y)) for c in range(len(q)))


def neighbors(q, n):
    return [[j for j in range(n) if j != i and any(q[2 * i + a][2 * j + b] != 0.0 for a in range(2) for b in range(2))] for i in range(n)]


def local_search(q, y, n, tol=1e-12, max_sweeps=20000):
    """Block coordinate descent on St(2, r)^n. Each step minimizes over one Y_i.

    With the others fixed, tr(Q Y^T Y) = 2 tr(Y_i^T G_i) + const, with
    G_i = sum_{j != i} Y_j Q_ji, so the minimizer is Y_i = polar(-G_i).
    """
    nb = neighbors(q, n)
    r = len(y)
    last = relaxed_cost(q, y)
    for sweep in range(max_sweeps):
        for i in range(n):
            g = [[0.0, 0.0] for _ in range(r)]
            for j in nb[i]:
                for k in range(r):
                    yk = y[k]
                    for b in range(2):
                        g[k][b] -= yk[2 * j] * q[2 * j][2 * i + b] + yk[2 * j + 1] * q[2 * j + 1][2 * i + b]
            set_block(y, i, polar_factor(g))
        cost = relaxed_cost(q, y)
        if last - cost <= tol * max(1.0, abs(cost)):
            return y, sweep + 1
        last = cost
    return y, max_sweeps


def certificate(q, y, n):
    """Return S = Q - Lambda with Lambda_i = Sym(sum_j Q_ij Y_j^T Y_i)."""
    yty = matmul(transpose(y), y)
    s = [list(row) for row in q]
    for i in range(n):
        lam = [[0.0, 0.0], [0.0, 0.0]]
        for a in range(2):
            for b in range(2):
                lam[a][b] = sum(q[2 * i + a][c] * yty[c][2 * i + b] for c in range(2 * n))
        for a in range(2):
            for b in range(2):
                s[2 * i + a][2 * i + b] -= 0.5 * (lam[a][b] + lam[b][a])
    return s


def riemannian_gradient_norm(q, y, n):
    """|| 2 Y S || in the Frobenius norm; zero exactly at a first order critical point."""
    ys = matmul(y, certificate(q, y, n))
    return 2.0 * math.sqrt(sum(x * x for row in ys for x in row))


def escape(q, y, n, v):
    """Lift Y to [Y; 0] and step along e_{r+1} v^T with a backtracking line search."""
    base = [list(row) for row in y] + [[0.0] * (2 * n)]
    f0 = relaxed_cost(q, base)
    norm = math.sqrt(sum(x * x for x in v))
    alpha = 1.0
    while alpha > 1e-12:
        trial = [list(row) for row in base]
        trial[-1] = [alpha * x / norm for x in v]
        for i in range(n):
            set_block(trial, i, polar_factor(block(trial, i)))
        if relaxed_cost(q, trial) < f0:
            return trial
        alpha *= 0.5
    raise ValueError("no descent along the eigenvector")


def round_solution(y, n):
    """Top 2 rows of U^T Y, sign fix, then the nearest rotation per block."""
    r = len(y)
    yyt = [[sum(a * b for a, b in zip(y[i], y[j])) for j in range(r)] for i in range(r)]
    _, vecs = symmetric_eigen(yyt)
    top = [[vecs[k][r - 1 - c] for k in range(r)] for c in range(2)]  # the two largest
    rr = [[sum(top[c][k] * y[k][col] for k in range(r)) for col in range(2 * n)] for c in range(2)]
    dets = [rr[0][2 * i] * rr[1][2 * i + 1] - rr[0][2 * i + 1] * rr[1][2 * i] for i in range(n)]
    if sum(1 for d in dets if d < 0) > n / 2:
        rr[1] = [-x for x in rr[1]]
    out = []
    for i in range(n):
        a, b = rr[0][2 * i], rr[0][2 * i + 1]
        c, d = rr[1][2 * i], rr[1][2 * i + 1]
        # the nearest rotation to [[a, b], [c, d]] has the angle atan2(c - b, a + d)
        out.append(rot(math.atan2(c - b, a + d)))
    g = transpose(out[0])
    return [matmul(g, x) for x in out]


def spanning_tree_start(n, edges):
    """Compose the measurements along a breadth-first spanning tree from rotation 0."""
    adj = {i: [] for i in range(n)}
    for i, j, rt, _ in edges:
        adj[i].append((j, rt))
        adj[j].append((i, transpose(rt)))
    rs = {0: rot(0.0)}
    queue = [0]
    while queue:
        i = queue.pop(0)
        for j, rt in adj[i]:
            if j not in rs:
                rs[j] = matmul(rs[i], rt)
                queue.append(j)
    if len(rs) != n:
        raise ValueError("the measurement graph is not connected")
    return [rs[i] for i in range(n)]


def se_sync(n, edges, start=None, eps=1e-6, max_rank=10):
    """Return a dict with the rotations, the bounds, the final rank and the history."""
    q = connection_laplacian(n, edges)
    scale = max(abs(x) for row in q for x in row)
    rs = start if start is not None else spanning_tree_start(n, edges)
    y = [[0.0] * (2 * n) for _ in range(2)]
    for i, r in enumerate(rs):
        set_block(y, i, r)  # @line L1
    history = []
    while True:  # @line L2
        y, sweeps = local_search(q, y, n)  # @line L3
        s = certificate(q, y, n)  # @line L4
        vals, vecs = symmetric_eigen(s)  # @line L5
        lam_min = vals[0]
        history.append((len(y), relaxed_cost(q, y), lam_min, sweeps))
        if lam_min >= -eps * scale:  # @line L6
            break
        if len(y) >= max_rank:
            raise ValueError("the staircase reached the largest rank without a certificate")
        v = [vecs[k][0] for k in range(2 * n)]
        y = escape(q, y, n, v)  # @line L7
    lower = relaxed_cost(q, y)
    rounded = round_solution(y, n)  # @line L8
    upper = objective(edges, rounded)  # @line L9
    return {
        "rotations": rounded,
        "lower": lower,
        "upper": upper,
        "rank": len(y),
        "lam_min": lam_min,
        "history": history,
    }
