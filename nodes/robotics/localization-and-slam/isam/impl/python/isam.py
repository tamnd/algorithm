# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isam/. The authors are listed in prov/CYW7G6.jsonl.

"""iSAM (Kaess, Ranganathan and Dellaert 2008) on a small planar SLAM problem.

The variables are poses ("x", t) = (x, y, theta) and point landmarks
("l", j) = (x, y). The factors are a prior on a pose, odometry between two
poses, and a range and bearing measurement of a landmark from a pose. The
noise is Gaussian with diagonal standard deviations, and each row of the
Jacobian is divided by its standard deviation.

iSAM keeps the linearization point theta, a column order of the variables,
and the upper triangular factor R with the right side d, such that
R^T R = A^T A and R^T d = A^T b, where A delta = b is the whitened linear
system of all factors so far at theta. The estimate is theta + delta with
R delta = d.

UPDATE(new values, new factors):
  1. append the new variables to the end of the column order,
  2. linearize the new factors at theta and rotate each new row into R by
     Givens rotations, one leading entry at a time,
  3. every k updates: move theta to the estimate, find a new minimum degree
     order, and factor all rows again (the batch step),
  4. solve R delta = d by back substitution.

R is sparse: a dict from the pivot column to the row, and a row is a dict
from the column to the value, with the right side under the key "rhs".
"""

import math

RHS = "rhs"


def wrap(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def dim(v):
    return 3 if v[0] == "x" else 2


class Factor:
    def __init__(self, kind, keys, z, sigmas):
        self.kind = kind
        self.keys = keys
        self.z = list(z)
        self.sigmas = list(sigmas)

    def error_and_jacobians(self, theta):
        """Return (e, [J for each key]) with e = h(theta) - z, not whitened."""
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


def squared_error(factors, theta):
    tot = 0.0
    for f in factors:
        e, _ = f.error_and_jacobians(theta)
        tot += sum((a / s) ** 2 for a, s in zip(e, f.sigmas))
    return tot


def fill_reducing_order(factors, variables):
    """Minimum degree on the variable graph, with the degree in scalar columns."""
    nb = {v: set() for v in variables}
    for f in factors:
        for u in f.keys:
            nb[u] |= set(f.keys) - {u}
    order = []
    while nb:
        u = min(nb, key=lambda v: (sum(dim(w) for w in nb[v]), v))
        around = nb.pop(u)
        for a in around:
            nb[a].discard(u)
            nb[a] |= around - {a}
        order.append(u)
    return order


class ISAM:
    def __init__(self, k=10):
        self.k = k  # the period of the batch step
        self.theta = {}  # the linearization point
        self.order = []
        self.start = {}
        self.n = 0
        self.r = {}
        self.factors = []
        self.delta = []
        self.updates = 0
        self.last_givens = 0
        self.total_givens = 0
        self.batch_steps = 0

    # ---------------------------------------------------------- helpers

    def _append(self, v):
        self.order.append(v)
        self.start[v] = self.n
        self.n += dim(v)
        self.delta.extend([0.0] * dim(v))

    def rows(self, factors):
        """The whitened rows of [A | b] of the factors at theta, as sparse dicts."""
        out = []
        for f in factors:
            e, js = f.error_and_jacobians(self.theta)
            for i in range(len(e)):
                row = {}
                for v, jv in zip(f.keys, js):
                    for c in range(dim(v)):
                        if jv[i][c] != 0.0:
                            row[self.start[v] + c] = jv[i][c] / f.sigmas[i]
                row[RHS] = -e[i] / f.sigmas[i]
                out.append(row)
        return out

    def _rotate_in(self, row):
        """Eliminate one row into R by Givens rotations; return the rotation count."""
        count = 0
        a = dict(row)
        while True:  # @line L4
            cols = [c for c in a if c != RHS]
            if not cols:
                return count
            c = min(cols)  # @line L5
            if c not in self.r:
                self.r[c] = a  # @line L6
                return count
            p = self.r[c]
            h = math.hypot(p[c], a[c])
            cs, sn = p[c] / h, a[c] / h
            new_p, new_a = {}, {}
            for j in set(p) | set(a):
                u, w = p.get(j, 0.0), a.get(j, 0.0)
                new_p[j] = cs * u + sn * w  # @line L7
                new_a[j] = -sn * u + cs * w
            new_p[c] = h
            new_a.pop(c, None)
            self.r[c] = {j: x for j, x in new_p.items() if j == RHS or x != 0.0}
            a = {j: x for j, x in new_a.items() if j == RHS or abs(x) > 1e-14 * h}
            count += 1

    def _solve(self):
        delta = [0.0] * self.n
        for c in range(self.n - 1, -1, -1):
            row = self.r[c]
            s = row.get(RHS, 0.0) - sum(x * delta[j] for j, x in row.items() if j != RHS and j > c)
            delta[c] = s / row[c]
        return delta

    def estimate(self):
        out = {}
        for v in self.order:
            s = self.start[v]
            x = [a + b for a, b in zip(self.theta[v], self.delta[s:s + dim(v)])]
            if v[0] == "x":
                x[2] = wrap(x[2])
            out[v] = x
        return out

    def nnz(self):
        return sum(1 for row in self.r.values() for j in row if j != RHS)

    # ---------------------------------------------------------- the update

    def update(self, new_values, new_factors):
        for v in sorted(new_values):
            self.theta[v] = list(new_values[v])
            self._append(v)  # @line L1
        self.factors.extend(new_factors)
        count = 0
        for row in self.rows(new_factors):  # @line L2
            count += self._rotate_in(row)  # @line L3
        self.updates += 1
        if self.updates % self.k == 0:  # @line L8
            self.theta = self.estimate()  # @line L9
            self.order = fill_reducing_order(self.factors, list(self.theta))
            self.start, self.n = {}, 0
            for v in list(self.order):
                self.start[v] = self.n
                self.n += dim(v)
            self.r = {}
            for row in self.rows(self.factors):  # @line L10
                count += self._rotate_in(row)
            self.batch_steps += 1
        if len(self.r) != self.n:
            raise ValueError("the system is rank deficient: a variable is not constrained")
        self.delta = self._solve()  # @line L11
        self.last_givens = count
        self.total_givens += count
        return self.estimate()  # @line L12
