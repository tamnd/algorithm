# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/homogenization-method/. The authors are listed in prov/MKGHFA.jsonl.

"""The homogenization method for topology optimization, scalar form.

Bendsoe and Kikuchi (1988) gave every point of the design domain a periodic
microstructure: a square cell with a rectangular hole. The effective stiffness
of the cell comes from the cell problem of homogenization theory, and the
optimizer changes the hole sizes and the angle of the cell. Their model is
linear elasticity. This file uses the scalar problem (heat conduction, or
antiplane shear), where the conductivity of a point is a 2 x 2 tensor, so the
cell problem has two load cases instead of three and the code stays short.

All finite elements are bilinear squares (Q4) of side 1. The solvers work on
any number type, so the tests run the cell problem exactly in Fraction.
"""

import math

# The corners of the unit element, counterclockwise from the origin.
CORNERS = ((0, 0), (1, 0), (1, 1), (0, 1))


def _hat_product(a, b):
    """The integral over [0, 1] of phi_a phi_b, with phi_0 = 1 - t and phi_1 = t."""
    return (1 / 3) if a == b else (1 / 6)


def _exact_tables():
    """Kxx, Kyy, Kxy and the gradient integrals Gx, Gy of the unit Q4 element,
    as numerator / 12 integers, so they can be scaled in any number type."""
    kxx = [[0] * 4 for _ in range(4)]
    kyy = [[0] * 4 for _ in range(4)]
    kxy = [[0] * 4 for _ in range(4)]
    for i, (xi, yi) in enumerate(CORNERS):
        for j, (xj, yj) in enumerate(CORNERS):
            sxi, syi, sxj, syj = 2 * xi - 1, 2 * yi - 1, 2 * xj - 1, 2 * yj - 1
            kxx[i][j] = sxi * sxj * (4 if yi == yj else 2)  # times 1/12: 1/3 or 1/6
            kyy[i][j] = syi * syj * (4 if xi == xj else 2)
            kxy[i][j] = sxi * syj * 3  # 1/4 = 3/12
    gx = [6 * (2 * x - 1) for x, _ in CORNERS]  # 1/2 = 6/12
    gy = [6 * (2 * y - 1) for _, y in CORNERS]
    return kxx, kyy, kxy, gx, gy


KXX, KYY, KXY, GX, GY = _exact_tables()


def element_matrix(a11, a12, a22):
    """The 4 x 4 matrix of the integral of grad N_i . A grad N_j on the unit square."""
    return [[(a11 * KXX[i][j] + a22 * KYY[i][j] + a12 * (KXY[i][j] + KXY[j][i])) / 12 for j in range(4)] for i in range(4)]


def solve_spd(k, rhs, bw=None):
    """Solve k x = b for every b in rhs by Gaussian elimination without
    pivoting, which is safe for a symmetric positive definite k. Only the
    band |i - j| <= bw is touched, so a banded k costs O(n bw^2)."""
    n = len(k)
    bw = n if bw is None else bw
    m = [row[:] for row in k]
    bs = [b[:] for b in rhs]
    for c in range(n):
        top = min(n, c + bw + 1)
        piv = m[c][c]
        row_c = m[c]
        for r in range(c + 1, top):
            if m[r][c] == 0:
                continue
            t = m[r][c] / piv
            row_r = m[r]
            for j in range(c, top):
                row_r[j] -= t * row_c[j]
            for b in bs:
                b[r] -= t * b[c]
    out = []
    for b in bs:
        x = [b[0] * 0] * n
        for r in range(n - 1, -1, -1):
            top = min(n, r + bw + 1)
            s = b[r]
            for j in range(r + 1, top):
                s -= m[r][j] * x[j]
            x[r] = s / m[r][r]
        out.append(x)
    return out


def cell_tensor(a):
    """The effective conductivity tensor of a periodic cell.

    a[r][c] is the conductivity of the element in row r (y) and column c (x) of
    an N x N cell. For each unit vector e_j the cell problem asks for a periodic
    chi_j with the integral of a (e_j + grad chi_j) . grad v equal to 0 for all
    periodic v. Then A_ij is the mean of a (e_i + grad chi_i) . e_j. Returns
    ((A11, A12), (A12, A22)).
    """
    n = len(a)
    zero = a[0][0] * 0
    nodes = n * n

    def node(i, j):
        return (j % n) * n + (i % n)

    k = [[zero] * nodes for _ in range(nodes)]
    g = [[zero] * nodes, [zero] * nodes]
    total = zero
    for r in range(n):
        for c in range(n):
            ae = a[r][c]
            total += ae
            ids = [node(c + dx, r + dy) for dx, dy in CORNERS]
            ke = element_matrix(ae, zero, ae)
            for p in range(4):
                g[0][ids[p]] += ae * GX[p] / 12
                g[1][ids[p]] += ae * GY[p] / 12
                for q in range(4):
                    k[ids[p]][ids[q]] += ke[p][q]
    # chi is defined up to a constant: fix the value at node 0.
    kf = [row[1:] for row in k[1:]]
    chi = solve_spd(kf, [[-v for v in g[0][1:]], [-v for v in g[1][1:]]])
    chi = [[zero] + x for x in chi]
    out = [[zero, zero], [zero, zero]]
    for i in range(2):
        for j in range(2):
            s = sum(g[j][t] * chi[i][t] for t in range(nodes))
            out[i][j] = ((total if i == j else zero) + s) / nodes
    return out


def hole_cell(mu, gamma, n, void=1e-3):
    """A cell of N x N elements with a rectangular hole of size (1 - mu) by
    (1 - gamma). The material is a wall of width mu along y and a wall of
    width gamma along x. The hole sits in a corner: in a periodic cell this is
    the same structure as a centered hole. mu N and gamma N must be integers."""
    hx = round((1 - mu) * n)
    hy = round((1 - gamma) * n)
    return [[void if (c < hx and r < hy) else 1.0 for c in range(n)] for r in range(n)]


def make_table(grid=5, n=10, void=1e-3):
    """L1: A11 and A22 of the hole cell for mu, gamma in {0, 1/grid, ..., 1}.
    By symmetry A12 = 0 and A22(mu, gamma) = A11(gamma, mu)."""
    a11 = [[0.0] * (grid + 1) for _ in range(grid + 1)]
    a22 = [[0.0] * (grid + 1) for _ in range(grid + 1)]
    for i in range(grid + 1):
        for j in range(i, grid + 1):
            t = cell_tensor(hole_cell(i / grid, j / grid, n, void))
            a11[i][j], a22[i][j] = t[0][0], t[1][1]
            a11[j][i], a22[j][i] = t[1][1], t[0][0]
    return {"grid": grid, "a11": a11, "a22": a22, "void": void}


def interpolate(table, name, mu, gamma):
    """Bilinear interpolation of a table entry and its derivatives in mu and gamma."""
    g = table["grid"]
    t = table[name]
    s, u = mu * g, gamma * g
    i, j = min(int(s), g - 1), min(int(u), g - 1)
    fs, fu = s - i, u - j
    v00, v10, v01, v11 = t[i][j], t[i + 1][j], t[i][j + 1], t[i + 1][j + 1]
    val = (1 - fs) * (1 - fu) * v00 + fs * (1 - fu) * v10 + (1 - fs) * fu * v01 + fs * fu * v11
    dmu = g * ((1 - fu) * (v10 - v00) + fu * (v11 - v01))
    dga = g * ((1 - fs) * (v01 - v00) + fs * (v11 - v10))
    return val, dmu, dga


def density(mu, gamma):
    return 1 - (1 - mu) * (1 - gamma)


def rotate(a11, a22, th):
    """R diag(a11, a22) R^T with R the rotation by th: returns (b11, b12, b22)."""
    c, s = math.cos(th), math.sin(th)
    return a11 * c * c + a22 * s * s, (a11 - a22) * c * s, a11 * s * s + a22 * c * c


class Problem:
    """A grid of nx by ny unit elements. Node (i, j) has the number i (ny + 1) + j,
    so the stiffness matrix has half bandwidth ny + 2. fixed: nodes with u = 0.
    load: the load vector f over all nodes."""

    def __init__(self, nx, ny, fixed, load):
        self.nx, self.ny = nx, ny
        self.fixed = set(fixed)
        self.load = load
        self.free = [p for p in range((nx + 1) * (ny + 1)) if p not in self.fixed]
        self.pos = {p: t for t, p in enumerate(self.free)}

    def element_nodes(self, ex, ey):
        h = self.ny + 1
        return [(ex + dx) * h + ey + dy for dx, dy in CORNERS]

    def elements(self):
        for ex in range(self.nx):
            for ey in range(self.ny):
                yield ex * self.ny + ey, self.element_nodes(ex, ey)


def bar_problem(nx, ny, force=1.0):
    """The left edge is held at u = 0 and the right edge carries the total load
    force, spread as consistent nodal loads."""
    h = ny + 1
    load = [0.0] * ((nx + 1) * h)
    for j in range(ny):
        load[nx * h + j] += force / ny / 2
        load[nx * h + j + 1] += force / ny / 2
    return Problem(nx, ny, [j for j in range(h)], load)


def sink_problem(nx, ny):
    """Uniform heat source in every element and a small sink (u = 0) at the
    middle of the left edge: the volume to point problem."""
    h = ny + 1
    load = [0.0] * ((nx + 1) * h)
    prob = Problem(nx, ny, [], load)
    for _, ids in prob.elements():
        for p in ids:
            load[p] += 0.25
    mid = ny // 2
    return Problem(nx, ny, [mid - 1, mid, mid + 1], load)


def solve(prob, tensors):
    """Assemble K from the element tensors (b11, b12, b22), solve K u = f on the
    free nodes, and return (u, compliance f . u)."""
    nf = len(prob.free)
    k = [[0.0] * nf for _ in range(nf)]
    for e, ids in prob.elements():
        ke = element_matrix(*tensors[e])
        for p in range(4):
            if ids[p] not in prob.pos:
                continue
            row = k[prob.pos[ids[p]]]
            for q in range(4):
                if ids[q] in prob.pos:
                    row[prob.pos[ids[q]]] += ke[p][q]
    f = [prob.load[p] for p in prob.free]
    (uf,) = solve_spd(k, [f], prob.ny + 2)
    u = [0.0] * len(prob.load)
    for p, t in prob.pos.items():
        u[p] = uf[t]
    return u, sum(prob.load[p] * u[p] for p in range(len(u)))


def energy(ue, b):
    """u_e^T K_e(B) u_e for the element tensor B = (b11, b12, b22)."""
    ke = element_matrix(*b)
    return sum(ue[p] * ke[p][q] * ue[q] for p in range(4) for q in range(4))


GAUSS = (0.5 - 0.5 / math.sqrt(3), 0.5 + 0.5 / math.sqrt(3))


def gradient(ue, x, y):
    """The gradient of the bilinear u at the point (x, y) of the unit element."""
    return (1 - y) * (ue[1] - ue[0]) + y * (ue[2] - ue[3]), (1 - x) * (ue[3] - ue[0]) + x * (ue[2] - ue[1])


def flux_moment(ue, b):
    """S = sum over the 2 x 2 Gauss points of w q q^T, with the flux q = B grad u."""
    s11 = s12 = s22 = 0.0
    for x in GAUSS:
        for y in GAUSS:
            gx, gy = gradient(ue, x, y)
            qx, qy = b[0] * gx + b[1] * gy, b[1] * gx + b[2] * gy
            s11 += qx * qx / 4
            s12 += qx * qy / 4
            s22 += qy * qy / 4
    return s11, s12, s22


def best_angle(ue, b, a11, a22):
    """L6: the angle that puts the stiffer axis of the cell along the main
    direction of the flux moment S. It minimizes the complementary energy
    tr(R diag(a11, a22)^-1 R^T S) of the old flux over the angle."""
    s11, s12, s22 = flux_moment(ue, b)
    th = 0.5 * math.atan2(2 * s12, s11 - s22)
    return th if a11 >= a22 else th + math.pi / 2


def complementary(ue, b, a11, a22, th):
    """The sum over the Gauss points of w q . A(th)^-1 q, with q the flux of ue under b."""
    s11, s12, s22 = flux_moment(ue, b)
    c, s = math.cos(th), math.sin(th)
    # A(th)^-1 = R diag(1/a11, 1/a22) R^T
    i11, i12, i22 = c * c / a11 + s * s / a22, (1 / a11 - 1 / a22) * c * s, s * s / a11 + c * c / a22
    return i11 * s11 + 2 * i12 * s12 + i22 * s22


def tensors_of(table, mu, gamma, th):
    out = []
    for m, g, t in zip(mu, gamma, th):
        a11 = interpolate(table, "a11", m, g)[0]
        a22 = interpolate(table, "a22", m, g)[0]
        out.append(rotate(a11, a22, t))
    return out


def sensitivities(prob, table, u, mu, gamma, th):
    """L7: dc/dmu_e and dc/dgamma_e, each equal to -u_e^T (dK_e) u_e."""
    dmu, dga = [], []
    for e, ids in prob.elements():
        ue = [u[p] for p in ids]
        _, a11m, a11g = interpolate(table, "a11", mu[e], gamma[e])
        _, a22m, a22g = interpolate(table, "a22", mu[e], gamma[e])
        dmu.append(-energy(ue, rotate(a11m, a22m, th[e])))
        dga.append(-energy(ue, rotate(a11g, a22g, th[e])))
    return dmu, dga


def _oc_factor(dc, drho, lam):
    """The optimality criteria factor -dc / (lam drho), with the limits made explicit."""
    if drho <= 0:
        return math.inf if dc < 0 else 1.0
    return max(0.0, -dc) / (lam * drho)


def oc_update(mu, gamma, dmu, dga, volume, move=0.2, eta=0.5):
    """L8: the optimality criteria step for both widths, with a bisection on
    the multiplier lam in log scale so that the volume is at most the target."""

    def trial(lam):
        nm, ng = [], []
        for m, g, cm, cg in zip(mu, gamma, dmu, dga):
            bm = _oc_factor(cm, 1 - g, lam) ** eta
            bg = _oc_factor(cg, 1 - m, lam) ** eta
            nm.append(min(1.0, m + move, max(0.0, m - move, m * bm)))
            ng.append(min(1.0, g + move, max(0.0, g - move, g * bg)))
        return nm, ng

    lo, hi = -40.0, 40.0
    for _ in range(100):
        mid = (lo + hi) / 2
        nm, ng = trial(10**mid)
        if sum(density(a, b) for a, b in zip(nm, ng)) > volume:
            lo = mid
        else:
            hi = mid
    return trial(10**hi)


def homogenize(prob, fraction, table=None, move=0.2, eta=0.5, maxit=60, tol=1e-3):
    """Run the homogenization method. Returns (mu, gamma, theta, history)."""
    if table is None:
        table = make_table()  # @line L1
    n = prob.nx * prob.ny
    volume = fraction * n
    s = 1 - math.sqrt(1 - fraction)
    mu, gamma, th = [s] * n, [s] * n, [0.0] * n  # @line L2
    hist = []
    for _ in range(maxit):  # @line L3
        tens = tensors_of(table, mu, gamma, th)  # @line L4
        u, c = solve(prob, tens)  # @line L5
        hist.append(c)
        th = [best_angle([u[p] for p in ids], tens[e], interpolate(table, "a11", mu[e], gamma[e])[0], interpolate(table, "a22", mu[e], gamma[e])[0]) for e, ids in prob.elements()]  # @line L6
        dmu, dga = sensitivities(prob, table, u, mu, gamma, th)  # @line L7
        nm, ng = oc_update(mu, gamma, dmu, dga, volume, move, eta)  # @line L8
        change = max(max(abs(a - b) for a, b in zip(nm, mu)), max(abs(a - b) for a, b in zip(ng, gamma)))
        mu, gamma = nm, ng
        if change < tol:  # @line L9
            break
    return mu, gamma, th, hist  # @line L10


def bar_lower_bound(prob, force, volume, void):
    """F^2 L^2 / (V (1 - void) + n void): no design of volume at most V does better."""
    n = prob.nx * prob.ny
    return force**2 * prob.nx**2 / (volume * (1 - void) + n * void)
