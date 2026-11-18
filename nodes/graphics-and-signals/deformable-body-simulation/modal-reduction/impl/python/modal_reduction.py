# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modal-reduction/. The authors are listed in prov/CSEPNJ.jsonl.
"""Linear modal reduction of a 2D triangle mesh.

The rest stiffness K of linear elasticity and the lumped mass M are
assembled, the generalized eigenproblem K phi = lambda M phi is solved by
the cyclic Jacobi method on M^(-1/2) K M^(-1/2), and the r modes with the
smallest eigenvalues form the basis U, with U^T M U = I and
U^T K U = diag(omega^2). The reduced coordinates q follow r independent
oscillators q'' = -omega^2 q + U^T f, advanced by symplectic Euler, and the
shape is u = U q.

Displacements are flat lists (u_x0, u_y0, u_x1, u_y1, ...).
"""

import math

from anim import det, inv, mul, transpose


def lame(young, poisson):
    mu = young / (2.0 * (1.0 + poisson))
    lam = young * poisson / ((1.0 + poisson) * (1.0 - 2.0 * poisson))
    return mu, lam


def grid_mesh(nx, ny, width, height):
    """Nodes of an nx by ny grid on [0, width] x [0, height], two triangles per cell, all counterclockwise."""
    nodes = [(width * i / (nx - 1), height * j / (ny - 1)) for j in range(ny) for i in range(nx)]
    tris = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = j * nx + i
            b, c, d = a + 1, a + nx, a + nx + 1
            tris.append((a, b, d))
            tris.append((a, d, c))
    return nodes, tris


def _edge(p, t):
    return [[p[t[1]][0] - p[t[0]][0], p[t[2]][0] - p[t[0]][0]], [p[t[1]][1] - p[t[0]][1], p[t[2]][1] - p[t[0]][1]]]


def element_linear_forces(dm, area, du, mu, lam):
    """Forces of linear elasticity on the 3 vertices for the vertex displacements du (6 numbers)."""
    dm_inv = inv(dm)
    ds = [[du[2] - du[0], du[4] - du[0]], [du[3] - du[1], du[5] - du[1]]]
    h = mul(ds, dm_inv)
    tr = h[0][0] + h[1][1]
    p = [[mu * (h[i][j] + h[j][i]) + (lam * tr if i == j else 0.0) for j in range(2)] for i in range(2)]
    g = mul(p, transpose(dm_inv))
    f1 = (-area * g[0][0], -area * g[1][0])
    f2 = (-area * g[0][1], -area * g[1][1])
    return [-f1[0] - f2[0], -f1[1] - f2[1], f1[0], f1[1], f2[0], f2[1]]


def stiffness_matrix(nodes, tris, mu, lam):
    n = 2 * len(nodes)
    k = [[0.0] * n for _ in range(n)]
    for t in tris:
        dm = _edge(nodes, t)
        area = det(dm) / 2.0
        dofs = [2 * t[0], 2 * t[0] + 1, 2 * t[1], 2 * t[1] + 1, 2 * t[2], 2 * t[2] + 1]
        for b in range(6):
            unit = [1.0 if c == b else 0.0 for c in range(6)]
            col = element_linear_forces(dm, area, unit, mu, lam)
            for a in range(6):
                k[dofs[a]][dofs[b]] -= col[a]
    return k


def lumped_mass(nodes, tris, rho):
    m = [0.0] * (2 * len(nodes))
    for t in tris:
        share = rho * det(_edge(nodes, t)) / 6.0
        for v in t:
            m[2 * v] += share
            m[2 * v + 1] += share
    return m


def restrict(k, m, free):
    """Keep only the degrees of freedom in the list free."""
    return [[k[i][j] for j in free] for i in free], [m[i] for i in free]


def jacobi_eigen(a, tol=1e-13, max_sweeps=60):
    """Eigenvalues and eigenvectors of a symmetric matrix by cyclic Jacobi rotations.

    Return (values, vectors) with vectors[k] the unit eigenvector of values[k].
    """
    n = len(a)
    a = [list(map(float, row)) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    scale = math.sqrt(sum(x * x for row in a for x in row)) or 1.0
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off <= tol * scale:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = a[p][q]
                if abs(apq) <= 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * apq)
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                rp, rq = a[p], a[q]
                for k in range(n):
                    apk, aqk = rp[k], rq[k]
                    rp[k] = c * apk - s * aqk
                    rq[k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    values = [a[i][i] for i in range(n)]
    vectors = [[v[k][i] for k in range(n)] for i in range(n)]
    return values, vectors


def generalized_eigen(k, m):
    """Solve K phi = lambda M phi for a diagonal M > 0; return the pairs sorted by lambda, with phi^T M phi = 1."""
    n = len(k)
    s = [1.0 / math.sqrt(x) for x in m]
    a = [[s[i] * k[i][j] * s[j] for j in range(n)] for i in range(n)]
    values, vectors = jacobi_eigen(a)
    pairs = sorted(zip(values, vectors), key=lambda pv: pv[0])
    lams = [p[0] for p in pairs]
    phis = [[s[i] * p[1][i] for i in range(n)] for p in pairs]
    return lams, phis


def modal_basis(k, m, r):
    """The r modes with the smallest eigenvalues: (omega^2 list, U as a list of r mode vectors)."""
    lams, phis = generalized_eigen(k, m)  # @line L2
    return lams[:r], phis[:r]  # @line L3


def project(modes, f):
    return [sum(a * b for a, b in zip(phi, f)) for phi in modes]


def reconstruct(modes, q):
    n = len(modes[0])
    return [sum(q[i] * modes[i][j] for i in range(len(modes))) for j in range(n)]


def simulate_modal(modes, omega2, force, h, steps, q0=None, v0=None):
    """Advance q'' = -omega^2 q + U^T f by symplectic Euler; return the list of shapes u = U q."""
    r = len(modes)
    q = list(q0) if q0 else [0.0] * r
    v = list(v0) if v0 else [0.0] * r
    g = project(modes, force)  # @line L4
    shapes = []
    for _ in range(steps):
        for i in range(r):
            v[i] += h * (g[i] - omega2[i] * q[i])  # @line L5
            q[i] += h * v[i]
        shapes.append(reconstruct(modes, q))  # @line L6
    return shapes, q


def simulate_full(k, m, force, h, steps, u0=None, v0=None):
    """The reference: M u'' = -K u + f with the same symplectic Euler step on all degrees of freedom."""
    n = len(k)
    u = list(u0) if u0 else [0.0] * n
    v = list(v0) if v0 else [0.0] * n
    shapes = []
    for _ in range(steps):
        ku = [sum(k[i][j] * u[j] for j in range(n)) for i in range(n)]
        for i in range(n):
            v[i] += h * (force[i] - ku[i]) / m[i]
        for i in range(n):
            u[i] += h * v[i]
        shapes.append(list(u))
    return shapes


def setup(nx, ny, width, height, young, poisson, rho, fix_left):
    """Assemble and restrict a grid; return (nodes, tris, K, M, free dofs)."""
    nodes, tris = grid_mesh(nx, ny, width, height)
    mu, lam = lame(young, poisson)
    k = stiffness_matrix(nodes, tris, mu, lam)  # @line L1
    m = lumped_mass(nodes, tris, rho)
    free = [d for d in range(2 * len(nodes)) if not (fix_left and nodes[d // 2][0] == 0.0)]
    kr, mr = restrict(k, m, free)
    return nodes, tris, kr, mr, free


def stvk_energy(nodes, tris, u, mu, lam):
    """St. Venant-Kirchhoff energy of the displaced mesh, to measure the error of linear modes at large amplitude."""
    total = 0.0
    for t in tris:
        dm = _edge(nodes, t)
        cur = [(nodes[v][0] + u[2 * v], nodes[v][1] + u[2 * v + 1]) for v in t]
        ds = [[cur[1][0] - cur[0][0], cur[2][0] - cur[0][0]], [cur[1][1] - cur[0][1], cur[2][1] - cur[0][1]]]
        f = mul(ds, inv(dm))
        c = mul(transpose(f), f)
        e = [[0.5 * (c[i][j] - (1.0 if i == j else 0.0)) for j in range(2)] for i in range(2)]
        tr = e[0][0] + e[1][1]
        psi = mu * sum(x * x for row in e for x in row) + 0.5 * lam * tr * tr
        total += det(dm) / 2.0 * psi
    return total


def mesh_area(nodes, tris, u):
    total = 0.0
    for t in tris:
        p = [(nodes[v][0] + u[2 * v], nodes[v][1] + u[2 * v + 1]) for v in t]
        total += 0.5 * ((p[1][0] - p[0][0]) * (p[2][1] - p[0][1]) - (p[1][1] - p[0][1]) * (p[2][0] - p[0][0]))
    return total
