# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pose-graph/. The authors are listed in prov/4A941D.jsonl.

"""A planar pose graph: poses on SE(2) as vertices, relative pose measurements as edges.

A pose is a tuple (x, y, theta) in meters and radians. It stands for the
transform T = [[R(theta), (x, y)], [0, 1]]. An edge (i, j, Z, Omega) says
that the pose of j seen from i was measured as Z, with the 3 by 3
information matrix Omega (the inverse of the covariance).

The residual of an edge is e = Log(Z^-1 X_i^-1 X_j) in the coordinates
(rho_x, rho_y, theta) of the Lie algebra se(2). Jacobians use the right
perturbation X exp(delta), by central differences with the step H.

The module holds the structure and its operations: add a vertex, add an
edge, list the edges at a vertex, compute residuals and the cost, set
initial poses from a spanning tree, and assemble the sparse Gauss-Newton
system in 3 by 3 blocks. It does not solve the system.
"""

import math
from collections import deque

H = 1e-6  # the step of the central differences, in the units of delta


def wrap(a):
    """Return the angle a wrapped to [-pi, pi)."""
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def compose(a, b):
    """Return the pose a b (b expressed in the frame of a)."""
    c, s = math.cos(a[2]), math.sin(a[2])
    return (a[0] + c * b[0] - s * b[1], a[1] + s * b[0] + c * b[1], wrap(a[2] + b[2]))


def inverse(a):
    """Return the pose a^-1."""
    c, s = math.cos(a[2]), math.sin(a[2])
    return (-c * a[0] - s * a[1], s * a[0] - c * a[1], wrap(-a[2]))


def _v_coeffs(t):
    """Return (A, B) with V(t) = [[A, -B], [B, A]], A = sin t / t, B = (1 - cos t) / t."""
    if abs(t) < 1e-6:
        return 1.0 - t * t / 6.0, t / 2.0 - t ** 3 / 24.0
    return math.sin(t) / t, (1.0 - math.cos(t)) / t


def exp_se2(v):
    """Return the pose exp(v) for v = (rho_x, rho_y, theta)."""
    a, b = _v_coeffs(v[2])
    return (a * v[0] - b * v[1], b * v[0] + a * v[1], wrap(v[2]))


def log_se2(p):
    """Return v = (rho_x, rho_y, theta) with exp(v) = p and theta in [-pi, pi)."""
    t = wrap(p[2])
    a, b = _v_coeffs(t)
    d = a * a + b * b
    return ((a * p[0] + b * p[1]) / d, (-b * p[0] + a * p[1]) / d, t)


class PoseGraph:
    """Vertices hold poses; edges hold relative pose measurements."""

    def __init__(self):
        self.X = {}  # vertex id -> pose
        self.adj = {}  # vertex id -> list of edge indices
        self.E = []  # list of (i, j, Z, Omega)

    def add_vertex(self, i, pose=(0.0, 0.0, 0.0)):
        if i in self.X:
            raise ValueError("vertex exists")
        self.X[i] = tuple(pose)  # @line L1
        self.adj[i] = []

    def add_edge(self, i, j, z, omega):
        if i not in self.X or j not in self.X or i == j:
            raise ValueError("an edge needs two distinct vertices")
        k = len(self.E)
        self.E.append((i, j, tuple(z), [list(r) for r in omega]))  # @line L2
        self.adj[i].append(k)  # @line L3
        self.adj[j].append(k)
        return k

    def neighbors(self, i):
        """Return the vertices that share an edge with i."""
        out = []
        for k in self.adj[i]:
            a, b = self.E[k][0], self.E[k][1]
            out.append(b if a == i else a)
        return out

    def residual(self, k, xi=None, xj=None):
        """Return e = Log(Z^-1 X_i^-1 X_j) of edge k, optionally at other poses."""
        i, j, z, _ = self.E[k]
        xi = self.X[i] if xi is None else xi
        xj = self.X[j] if xj is None else xj
        return log_se2(compose(inverse(z), compose(inverse(xi), xj)))  # @line L4

    def edge_cost(self, k):
        e = self.residual(k)
        om = self.E[k][3]
        return sum(e[a] * om[a][b] * e[b] for a in range(3) for b in range(3))

    def cost(self):
        """Return the sum over the edges of e^T Omega e."""
        return sum(self.edge_cost(k) for k in range(len(self.E)))

    def initialize(self, root):
        """Set every pose reachable from root by composing edges along a BFS tree.

        The root keeps its pose. Return the set of vertices that were reached.
        """
        seen = {root}  # @line L5
        q = deque([root])
        while q:  # @line L6
            i = q.popleft()  # @line L7
            for k in self.adj[i]:  # @line L8
                a, b, z, _ = self.E[k]
                j = b if a == i else a  # @line L9
                if j not in seen:  # @line L10
                    if a == i:
                        self.X[j] = compose(self.X[i], z)  # @line L11
                    else:
                        self.X[j] = compose(self.X[i], inverse(z))
                    seen.add(j)  # @line L12
                    q.append(j)
        return seen

    def jacobians(self, k):
        """Return (A, B), the 3 by 3 derivatives of the residual of edge k
        with respect to the right perturbations of X_i and X_j."""
        i, j, _, _ = self.E[k]
        xi, xj = self.X[i], self.X[j]
        a = [[0.0] * 3 for _ in range(3)]
        b = [[0.0] * 3 for _ in range(3)]
        for c in range(3):
            d = [0.0, 0.0, 0.0]
            d[c] = H
            dm = [0.0, 0.0, 0.0]
            dm[c] = -H
            ep = self.residual(k, compose(xi, exp_se2(d)), xj)
            em = self.residual(k, compose(xi, exp_se2(dm)), xj)
            fp = self.residual(k, xi, compose(xj, exp_se2(d)))
            fm = self.residual(k, xi, compose(xj, exp_se2(dm)))
            for r in range(3):
                a[r][c] = _diff(ep[r], em[r], r) / (2 * H)
                b[r][c] = _diff(fp[r], fm[r], r) / (2 * H)
        return a, b

    def assemble(self):
        """Return (Hb, g): the Gauss-Newton blocks H_uv = sum J_u^T Omega J_v
        and g_u = sum J_u^T Omega e, as dicts keyed by vertex pairs and vertices.

        A block H_uv with u != v exists only if an edge joins u and v.
        """
        hb, g = {}, {}  # @line L13
        for k, (i, j, _, om) in enumerate(self.E):  # @line L14
            e = self.residual(k)  # @line L15
            a, b = self.jacobians(k)
            for u, ju in ((i, a), (j, b)):
                ou = _mtm(ju, om)  # J_u^T Omega
                for v, jv in ((i, a), (j, b)):
                    blk = hb.setdefault((u, v), [[0.0] * 3 for _ in range(3)])
                    m = _mm(ou, jv)
                    for r in range(3):  # @line L16
                        for c in range(3):
                            blk[r][c] += m[r][c]
                gv = g.setdefault(u, [0.0, 0.0, 0.0])
                for r in range(3):  # @line L17
                    gv[r] += sum(ou[r][c] * e[c] for c in range(3))
        return hb, g  # @line L18


def _diff(p, m, r):
    """Difference of two residual components; the angle is wrapped."""
    return wrap(p - m) if r == 2 else p - m


def _mtm(j, om):
    """Return J^T Omega."""
    return [[sum(j[k][r] * om[k][c] for k in range(3)) for c in range(3)] for r in range(3)]


def _mm(a, b):
    return [[sum(a[r][k] * b[k][c] for k in range(3)) for c in range(3)] for r in range(3)]
