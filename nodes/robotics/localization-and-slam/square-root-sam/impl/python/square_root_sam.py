# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/square-root-sam/. The authors are listed in prov/ZY48RG.jsonl.

"""Square root SAM (Dellaert and Kaess 2006) on a small planar SLAM problem.

The variables are poses ("x", t) = (x, y, theta) and point landmarks
("l", j) = (x, y). The factors are:
  prior(v, mean, sigmas)            the pose v is near mean
  odometry(i, j, z, sigmas)         the pose j seen from the pose i is z
  bearing_range(i, j, z, sigmas)    the landmark j is at (range, bearing) z from i
The noise of each factor is Gaussian with a diagonal covariance, given by
the standard deviations "sigmas". Each row of the Jacobian is divided by
its sigma (whitened), so the problem is min ||A delta - b||^2.

Each Gauss-Newton step:
  1. builds the whitened Jacobian A and the right side b at the estimate,
     with the columns in a fixed variable order,
  2. factors A = Q R by Givens rotations, one row at a time, and applies the
     same rotations to b, which gives d = Q^T b,
  3. solves R delta = d by back substitution, and
  4. adds delta to the estimate.

The column order matters only for the speed and the fill-in of R, not for
the solution. block_minimum_degree() gives a fill-reducing order on the
graph of the variables. cholesky_factor() gives the same R from A^T A, as a
second method.

R is stored sparse: a dict from the pivot column to the row, and each row
is a dict from the column to the value. The right side is the key "rhs".
"""

import math

RHS = "rhs"


def wrap(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def dim(v):
    return 3 if v[0] == "x" else 2


# ---------------------------------------------------------------- factors


class Factor:
    def __init__(self, kind, keys, z, sigmas):
        self.kind = kind
        self.keys = keys
        self.z = list(z)
        self.sigmas = list(sigmas)

    def error_and_jacobians(self, theta):
        """Return (e, [J_k for each key]) with e the unwhitened error h(theta) - z."""
        if self.kind == "prior":
            x = theta[self.keys[0]]
            e = [x[0] - self.z[0], x[1] - self.z[1], wrap(x[2] - self.z[2])]
            return e, [[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]]
        if self.kind == "odometry":
            a, b = theta[self.keys[0]], theta[self.keys[1]]
            c, s = math.cos(a[2]), math.sin(a[2])
            dx, dy = b[0] - a[0], b[1] - a[1]
            e = [c * dx + s * dy - self.z[0], -s * dx + c * dy - self.z[1], wrap(b[2] - a[2] - self.z[2])]
            ja = [[-c, -s, -s * dx + c * dy], [s, -c, -c * dx - s * dy], [0.0, 0.0, -1.0]]
            jb = [[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]]
            return e, [ja, jb]
        if self.kind == "bearing_range":
            x, m = theta[self.keys[0]], theta[self.keys[1]]
            dx, dy = m[0] - x[0], m[1] - x[1]
            q = dx * dx + dy * dy
            r = math.sqrt(q)
            e = [r - self.z[0], wrap(math.atan2(dy, dx) - x[2] - self.z[1])]
            jx = [[-dx / r, -dy / r, 0.0], [dy / q, -dx / q, -1.0]]
            jm = [[dx / r, dy / r], [-dy / q, dx / q]]
            return e, [jx, jm]
        raise ValueError("unknown factor kind")


def prior(v, mean, sigmas):
    return Factor("prior", [v], mean, sigmas)


def odometry(i, j, z, sigmas):
    return Factor("odometry", [i, j], z, sigmas)


def bearing_range(i, j, z, sigmas):
    return Factor("bearing_range", [i, j], z, sigmas)


# ---------------------------------------------------------------- ordering


def variable_graph(factors):
    adj = {}
    for f in factors:
        for u in f.keys:
            adj.setdefault(u, set())
            for v in f.keys:
                if v != u:
                    adj[u].add(v)
    return adj


def block_minimum_degree(factors):
    """Return a variable order: repeatedly eliminate a variable of least degree.

    The degree counts scalar columns, so a pose weighs 3 and a landmark 2.
    Ties go to the smallest variable in sort order, so the order is fixed.
    """
    adj = {u: set(n) for u, n in variable_graph(factors).items()}
    order = []
    while adj:
        u = min(adj, key=lambda v: (sum(dim(w) for w in adj[v]), v))
        nb = adj.pop(u)
        for a in nb:
            adj[a].discard(u)
            adj[a] |= nb - {a}
        order.append(u)
    return order


def columns(order):
    """Return (start column of each variable, total number of columns)."""
    start, n = {}, 0
    for v in order:
        start[v] = n
        n += dim(v)
    return start, n


# ---------------------------------------------------------------- the linear system


def linearize(factors, theta, order):
    """Return the whitened rows of [A | b] as sparse dicts, with b = -e / sigma."""
    start, _ = columns(order)
    rows = []
    for f in factors:
        e, js = f.error_and_jacobians(theta)
        for r in range(len(e)):
            row = {}
            for v, jv in zip(f.keys, js):
                for c in range(dim(v)):
                    if jv[r][c] != 0.0:
                        row[start[v] + c] = jv[r][c] / f.sigmas[r]
            row[RHS] = -e[r] / f.sigmas[r]
            rows.append(row)
    return rows


def givens_qr(rows, n):
    """Return R (dict pivot -> row) by Givens rotations applied row by row.

    Each new row is rotated against the rows of R with the same leading
    column until it has a new leading column or becomes zero. The count of
    rotations is returned as well.
    """
    r = {}  # @line L9
    count = 0
    for row in rows:  # @line L10
        a = {k: v for k, v in row.items() if k == RHS or v != 0.0}
        while True:
            cols = [k for k in a if k != RHS]
            if not cols:
                break
            c = min(cols)  # @line L11
            if c not in r:
                r[c] = a  # @line L12
                break
            p = r[c]
            x, y = p[c], a[c]
            h = math.hypot(x, y)
            cs, sn = x / h, y / h
            new_p, new_a = {}, {}
            for k in set(p) | set(a):
                u, w = p.get(k, 0.0), a.get(k, 0.0)
                new_p[k] = cs * u + sn * w  # @line L13
                new_a[k] = -sn * u + cs * w
            new_p[c] = h
            new_a.pop(c, None)
            r[c] = {k: v for k, v in new_p.items() if k == RHS or abs(v) > 1e-300}
            a = {k: v for k, v in new_a.items() if k == RHS or abs(v) > 1e-14 * h}
            count += 1
    if len(r) != n:
        raise ValueError("the system is rank deficient: add a prior")
    return r, count  # @line L14


def back_substitute(r, n):
    """Solve R delta = d, with d in the column RHS of R."""
    delta = [0.0] * n
    for c in range(n - 1, -1, -1):
        row = r[c]
        s = row.get(RHS, 0.0) - sum(v * delta[k] for k, v in row.items() if k != RHS and k > c)
        delta[c] = s / row[c]
    return delta


def nnz(r):
    return sum(1 for row in r.values() for k, v in row.items() if k != RHS and v != 0.0)


def dense(rows, n):
    """Return (A, b) as dense lists."""
    a = [[row.get(c, 0.0) for c in range(n)] for row in rows]
    return a, [row.get(RHS, 0.0) for row in rows]


def cholesky_factor(rows, n):
    """Return the upper triangular R with R^T R = A^T A, by the Cholesky method (dense)."""
    a, _ = dense(rows, n)
    m = [[sum(a[k][i] * a[k][j] for k in range(len(a))) for j in range(n)] for i in range(n)]
    r = [[0.0] * n for _ in range(n)]
    for i in range(n):
        s = m[i][i] - sum(r[k][i] ** 2 for k in range(i))
        if s <= 0.0:
            raise ValueError("A^T A is not positive definite")
        r[i][i] = math.sqrt(s)
        for j in range(i + 1, n):
            r[i][j] = (m[i][j] - sum(r[k][i] * r[k][j] for k in range(i))) / r[i][i]
    return r


def retract(theta, order, delta):
    start, _ = columns(order)
    out = {}
    for v in order:
        s = start[v]
        x = [a + b for a, b in zip(theta[v], delta[s:s + dim(v)])]
        if v[0] == "x":
            x[2] = wrap(x[2])
        out[v] = x
    return out


def total_error(factors, theta):
    """Return the sum of the squared whitened errors."""
    tot = 0.0
    for f in factors:
        e, _ = f.error_and_jacobians(theta)
        tot += sum((ei / si) ** 2 for ei, si in zip(e, f.sigmas))
    return tot


def square_root_sam(factors, theta, order=None, iterations=20, tol=1e-10):
    """Return (theta, R, number of iterations) by Gauss-Newton with QR."""
    if order is None:
        order = block_minimum_degree(factors)  # @line L1
    _, n = columns(order)
    r = None
    it = 0
    for it in range(1, iterations + 1):  # @line L2
        rows = linearize(factors, theta, order)  # @line L3
        r, _ = givens_qr(rows, n)  # @line L4
        delta = back_substitute(r, n)  # @line L5
        theta = retract(theta, order, delta)  # @line L6
        if max(abs(d) for d in delta) < tol:  # @line L7
            break
    return theta, r, it  # @line L8
