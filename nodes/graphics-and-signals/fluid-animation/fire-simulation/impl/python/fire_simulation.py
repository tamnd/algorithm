# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fire-simulation/. The authors are listed in prov/QHWFYD.jsonl.

"""The thin flame model of Nguyen, Fedkiw and Jensen (2002) on a 2D MAC grid.

A level set phi tracks the blue core: phi > 0 in the gaseous fuel, phi < 0
in the hot products, and the front phi = 0 moves with w = u_f + S n, where
n = grad phi / |grad phi| points into the fuel. The fuel and the products are
two incompressible fluids with densities rho_f > rho_h. Across the front the
normal velocity and the pressure jump by the amounts that conservation of
mass and momentum give (the paper's equations 2 and 3).

Sign convention for the jumps. V is the velocity component along
m = -n, the normal that points from the fuel to the products. Then the front
speed is D = V_f - S, V_h = V_f + (rho_f / rho_h - 1) S and
p_h = p_f - (rho_f / rho_h - 1) rho_f S^2.

Storage. g.u and g.v hold one velocity per face: the velocity of the
material at the face (the sign of phi averaged from the two cells). The
other material's velocity at a face is its ghost value (the paper's
equations 12 and 13): add or subtract J m with J = (rho_f / rho_h - 1) S.

Cells: FLUID cells hold fuel or products, AIR cells are an open outlet with
p = 0 (each group of FLUID cells needs one), SOLID cells are walls or
fuel injectors. phi and T are not changed in SOLID cells.
"""

import math

import macgrid
from macgrid import AIR, FLUID, SOLID


class Fire:
    """The state of the fire: a MAC grid g (velocity and labels), phi and T in the cells, and the constants."""

    def __init__(self, g, phi, rho_f=1.0, rho_h=0.2, S=0.5, T_air=300.0, T_ign=1500.0,
                 T_max=2000.0, c_T=3000.0, alpha=0.15):
        if not rho_f >= rho_h > 0.0 or S < 0.0 or not T_air < T_ign <= T_max:
            raise ValueError("need rho_f >= rho_h > 0, S >= 0 and T_air < T_ign <= T_max")
        self.g = g
        self.phi = phi
        self.rho_f, self.rho_h, self.S = rho_f, rho_h, S
        self.T_air, self.T_ign, self.T_max = T_air, T_ign, T_max
        self.c_T, self.alpha = c_T, alpha
        self.T = [[T_ign if phi[i][j] > 0.0 else T_air for j in range(g.ny)] for i in range(g.nx)]

    def J(self):
        """The jump of the normal velocity, V_h - V_f = (rho_f / rho_h - 1) S."""
        return (self.rho_f / self.rho_h - 1.0) * self.S

    def P(self):
        """The jump of the pressure, p_f - p_h = (rho_f / rho_h - 1) rho_f S^2."""
        return (self.rho_f / self.rho_h - 1.0) * self.rho_f * self.S * self.S


def jump_conditions(rho_f, rho_h, S, V_f, p_f):
    """Solve the paper's equations 2 and 3 for the products. Returns (D, V_h, p_h).

    V is along the normal from the fuel to the products. Exact with Fraction input.
    """
    D = V_f - S
    V_h = V_f + (rho_f / rho_h - 1) * S
    p_h = p_f - (rho_f / rho_h - 1) * rho_f * S * S
    return D, V_h, p_h


def solid_fuel_velocity(V_s, rho_s, rho_f, S):
    """The paper's equation 5: the velocity of the gas that leaves a burning solid, V_f = V_s + (rho_s / rho_f - 1) S."""
    return V_s + (rho_s / rho_f - 1) * S


def ghost_velocity(u, m, J, to_hot):
    """Equation 13 for a vector u of one material: the other material's velocity at the same point.

    m is the unit normal from the fuel to the products. The tangential part is
    kept and the normal part changes by +J (fuel to hot) or -J (hot to fuel).
    """
    s = J if to_hot else -J
    return tuple(a + s * b for a, b in zip(u, m))


def _phi_or(phi, i, j, default):
    if 0 <= i < len(phi) and 0 <= j < len(phi[0]):
        return phi[i][j]
    return default


def normals(phi, dx):
    """n = grad phi / |grad phi| at the cell centers by central differences (one sided at the border)."""
    na, nb = len(phi), len(phi[0])
    nx_, ny_ = macgrid.zeros(na, nb), macgrid.zeros(na, nb)
    for i in range(na):
        for j in range(nb):
            a0, a1 = max(i - 1, 0), min(i + 1, na - 1)
            b0, b1 = max(j - 1, 0), min(j + 1, nb - 1)
            gx = (phi[a1][j] - phi[a0][j]) / ((a1 - a0) * dx) if a1 > a0 else 0.0
            gy = (phi[i][b1] - phi[i][b0]) / ((b1 - b0) * dx) if b1 > b0 else 0.0
            r = math.hypot(gx, gy)
            if r > 0.0:
                nx_[i][j], ny_[i][j] = gx / r, gy / r
    return nx_, ny_


def _face_side(st, i0, j0, i1, j1):
    """For the face between cells (i0, j0) and (i1, j1): (phi at the face, m component along the face normal)."""
    phi = st.phi
    g = st.g
    inside = [(a, b) for (a, b) in ((i0, j0), (i1, j1)) if 0 <= a < g.nx and 0 <= b < g.ny]
    pf = sum(phi[a][b] for a, b in inside) / len(inside)
    return pf, inside


def face_data(st):
    """Per face: True if the face holds fuel, and m_n, the component of m = -n along the face normal.

    Returns (fuel_u, mu, fuel_v, mv) indexed like g.u and g.v.
    """
    g = st.g
    nxs, nys = normals(st.phi, g.dx)
    fuel_u = [[False] * g.ny for _ in range(g.nx + 1)]
    fuel_v = [[False] * (g.ny + 1) for _ in range(g.nx)]
    mu = macgrid.zeros(g.nx + 1, g.ny)
    mv = macgrid.zeros(g.nx, g.ny + 1)
    for i in range(g.nx + 1):
        for j in range(g.ny):
            pf, inside = _face_side(st, i - 1, j, i, j)
            fuel_u[i][j] = pf > 0.0
            mu[i][j] = -sum(nxs[a][b] for a, b in inside) / len(inside)
    for i in range(g.nx):
        for j in range(g.ny + 1):
            pf, inside = _face_side(st, i, j - 1, i, j)
            fuel_v[i][j] = pf > 0.0
            mv[i][j] = -sum(nys[a][b] for a, b in inside) / len(inside)
    return fuel_u, mu, fuel_v, mv


def material_fields(st, fd=None):
    """The fuel and the hot velocity fields on all faces, with ghost values on the other side. Returns (uf, vf, uh, vh)."""
    g = st.g
    J = st.J()
    fuel_u, mu, fuel_v, mv = fd if fd is not None else face_data(st)
    uf, uh = macgrid.copy_field(g.u), macgrid.copy_field(g.u)
    vf, vh = macgrid.copy_field(g.v), macgrid.copy_field(g.v)
    for i in range(g.nx + 1):
        for j in range(g.ny):
            if fuel_u[i][j]:
                uh[i][j] = g.u[i][j] + J * mu[i][j]  # @line L3
            else:
                uf[i][j] = g.u[i][j] - J * mu[i][j]
    for i in range(g.nx):
        for j in range(g.ny + 1):
            if fuel_v[i][j]:
                vh[i][j] = g.v[i][j] + J * mv[i][j]
            else:
                vf[i][j] = g.v[i][j] - J * mv[i][j]
    return uf, vf, uh, vh


def level_set_step(st, dt, cfl=0.5):
    """Move phi by the paper's equation 7 with w = u_f + S n and upwind differences, in substeps. Returns the substep count."""
    g = st.g
    dx = g.dx
    uf, vf, _, _ = material_fields(st)
    nxs, nys = normals(st.phi, dx)
    w1 = [[0.5 * (uf[i][j] + uf[i + 1][j]) + st.S * nxs[i][j] for j in range(g.ny)] for i in range(g.nx)]  # @line L1
    w2 = [[0.5 * (vf[i][j] + vf[i][j + 1]) + st.S * nys[i][j] for j in range(g.ny)] for i in range(g.nx)]
    wmax = max(max(abs(a) for col in w1 for a in col), max(abs(a) for col in w2 for a in col))
    steps = max(1, int(math.ceil(dt * wmax / (cfl * dx) - 1e-12)))
    h = dt / steps
    for _ in range(steps):
        phi = st.phi
        new = macgrid.copy_field(phi)
        for i in range(g.nx):
            for j in range(g.ny):
                if g.label[i][j] == SOLID:
                    continue
                a, b = w1[i][j], w2[i][j]
                back_x = (phi[i][j] - phi[i - 1][j]) / dx if i > 0 else None
                fwd_x = (phi[i + 1][j] - phi[i][j]) / dx if i < g.nx - 1 else None
                back_y = (phi[i][j] - phi[i][j - 1]) / dx if j > 0 else None
                fwd_y = (phi[i][j + 1] - phi[i][j]) / dx if j < g.ny - 1 else None
                px = back_x if (a > 0.0 and back_x is not None) or fwd_x is None else fwd_x
                py = back_y if (b > 0.0 and back_y is not None) or fwd_y is None else fwd_y
                new[i][j] = phi[i][j] - h * (a * (px or 0.0) + b * (py or 0.0))  # @line L2
        st.phi = new
    st.phi = redistance(st.phi, dx, g.label)
    return steps


def redistance(phi, dx, label=None):
    """Make phi a signed distance again away from the front, keeping the front.

    Cells next to the front (a neighbor of the other sign) keep their values.
    Every other cell gets its sign times the distance to the nearest crossing
    point of phi = 0 on a grid edge (linear interpolation). This brute force
    search stands in for the fast marching method of the paper; it is Θ(cells
    times crossings). SOLID cells keep their values.
    """
    na, nb = len(phi), len(phi[0])
    pts = []
    near = [[False] * nb for _ in range(na)]
    for i in range(na):
        for j in range(nb):
            for a, b in ((i + 1, j), (i, j + 1)):
                if a < na and b < nb and (phi[i][j] > 0.0) != (phi[a][b] > 0.0):
                    t = phi[i][j] / (phi[i][j] - phi[a][b])
                    pts.append(((i + 0.5 + t * (a - i)) * dx, (j + 0.5 + t * (b - j)) * dx))
                    near[i][j] = near[a][b] = True
    if not pts:
        return macgrid.copy_field(phi)
    out = macgrid.copy_field(phi)
    for i in range(na):
        for j in range(nb):
            if near[i][j] or (label is not None and label[i][j] == SOLID):
                continue
            x, y = (i + 0.5) * dx, (j + 0.5) * dx
            d = math.sqrt(min((x - px) ** 2 + (y - py) ** 2 for px, py in pts))
            out[i][j] = d if phi[i][j] > 0.0 else -d
    return out


def _grid_with(g, u, v):
    t = macgrid.make_grid(g.nx, g.ny, g.dx)
    t.u, t.v, t.label = u, v, g.label
    return t


def advect_velocity(st, dt, phi_old):
    """Advect the fuel field by itself and the hot field by itself; each face keeps the field of its new material."""
    g = st.g
    phi_new = st.phi
    st.phi = phi_old
    uf, vf, uh, vh = material_fields(st)
    st.phi = phi_new
    gf, gh = _grid_with(g, uf, vf), _grid_with(g, uh, vh)
    auf, avf = macgrid.advect_velocity(gf, dt)
    auh, avh = macgrid.advect_velocity(gh, dt)
    fuel_u, _, fuel_v, _ = face_data(st)
    g.u = [[auf[i][j] if fuel_u[i][j] else auh[i][j] for j in range(g.ny)] for i in range(g.nx + 1)]  # @line L4
    g.v = [[avf[i][j] if fuel_v[i][j] else avh[i][j] for j in range(g.ny + 1)] for i in range(g.nx)]
    return gh


def cool(st, T, dt):
    """Integrate T' = -c_T ((T - T_air) / (T_max - T_air))^4 exactly over dt (the source term of equation 17)."""
    if T <= st.T_air:
        return T
    span = st.T_max - st.T_air
    th = (T - st.T_air) / span
    th = th / (1.0 + 3.0 * st.c_T * dt * th ** 3 / span) ** (1.0 / 3.0)
    return st.T_air + span * th


def update_temperature(st, dt, phi_old, gh):
    """Advect T by the hot velocity with the ghost value T_max in the old fuel, set T_ign in the fuel, then cool."""
    g = st.g
    Tg = [[st.T_max if phi_old[i][j] > 0.0 else st.T[i][j] for j in range(g.ny)] for i in range(g.nx)]
    adv = macgrid.advect(gh, Tg, dt)
    for i in range(g.nx):
        for j in range(g.ny):
            if g.label[i][j] == SOLID:
                continue
            if st.phi[i][j] > 0.0:
                st.T[i][j] = st.T_ign
            else:
                st.T[i][j] = cool(st, adv[i][j], dt)  # @line L5


def add_buoyancy(st, dt):
    """The paper's equation 14: v += dt alpha (T - T_air) on faces that do not touch a SOLID cell."""
    g = st.g
    for i in range(g.nx):
        for j in range(1, g.ny):
            if macgrid.is_solid_v_face(g, i, j):
                continue
            Tf = 0.5 * (st.T[i][j - 1] + st.T[i][j])
            g.v[i][j] += dt * st.alpha * (Tf - st.T_air)  # @line L6


def _jump_from(st, fuel_from, fuel_to):
    """The pressure jump p_to - p_from at the front between two materials."""
    if fuel_from == fuel_to:
        return 0.0
    return -st.P() if fuel_from else st.P()


def _rho_hat(st, phi_a, phi_b):
    """The density of a face between two cells (Liu, Fedkiw and Kang 2000): the mix by the length on each side."""
    fa, fb = phi_a > 0.0, phi_b > 0.0
    ra = st.rho_f if fa else st.rho_h
    rb = st.rho_f if fb else st.rho_h
    if fa == fb:
        return ra
    th = abs(phi_a) / (abs(phi_a) + abs(phi_b))
    return th * ra + (1.0 - th) * rb


def _faces_of(g, i, j):
    """The four faces of cell (i, j): (neighbor, 'u' or 'v', face index, sign of the outward normal)."""
    return (((i - 1, j), "u", (i, j), -1.0), ((i + 1, j), "u", (i + 1, j), 1.0),
            ((i, j - 1), "v", (i, j), -1.0), ((i, j + 1), "v", (i, j + 1), 1.0))


def jump_divergence(st, fd=None):
    """The divergence of every FLUID cell, with each face velocity taken as the cell's own material (ghost values)."""
    g = st.g
    J = st.J()
    fuel_u, mu, fuel_v, mv = fd if fd is not None else face_data(st)
    d = macgrid.zeros(g.nx, g.ny)
    for i in range(g.nx):
        for j in range(g.ny):
            if g.label[i][j] != FLUID:
                continue
            fuel = st.phi[i][j] > 0.0
            s = 0.0
            for _, kind, (a, b), sgn in _faces_of(g, i, j):
                if kind == "u":
                    val, ff, m = g.u[a][b], fuel_u[a][b], mu[a][b]
                else:
                    val, ff, m = g.v[a][b], fuel_v[a][b], mv[a][b]
                if ff and not fuel:
                    val += J * m
                elif fuel and not ff:
                    val -= J * m
                s += sgn * val
            d[i][j] = s / g.dx
    return d


def _cg(diag, off, b, tol, max_iter):
    n = len(b)
    x = [0.0] * n
    bmax = max((abs(t) for t in b), default=0.0)
    if bmax == 0.0:
        return x, 0
    r = list(b)
    d = list(r)
    rr = sum(t * t for t in r)
    it = 0
    while it < max_iter and max(abs(t) for t in r) > tol * bmax:
        q = [diag[k] * d[k] - sum(c * d[m] for m, c in off[k]) for k in range(n)]
        dq = sum(d[k] * q[k] for k in range(n))
        if dq <= 0.0:
            break
        a = rr / dq
        for k in range(n):
            x[k] += a * d[k]
            r[k] -= a * q[k]
        rr_new = sum(t * t for t in r)
        beta = rr_new / rr
        rr = rr_new
        for k in range(n):
            d[k] = r[k] + beta * d[k]
        it += 1
    return x, it


def project(st, dt, solid_velocity=None, tol=1e-12):
    """Solve div(grad p / rho) = div u* / dt with the jumps by the ghost fluid method, and subtract the gradient.

    The pressure of a neighbor of the other material is converted to the cell's
    material with the jump P, and each face uses 1 / rho_hat. The matrix is
    symmetric and positive definite when each group of FLUID cells touches an
    AIR cell. Stores p in g.p and returns the CG iteration count.
    """
    g = st.g
    dx = g.dx
    macgrid.set_solid_boundaries(g, solid_velocity)
    fd = face_data(st)
    div = jump_divergence(st, fd)
    idx = {}
    cells = []
    for i in range(g.nx):
        for j in range(g.ny):
            if g.label[i][j] == FLUID:
                idx[(i, j)] = len(cells)
                cells.append((i, j))
    diag, off, b = [], [], []
    for (i, j) in cells:
        fa = st.phi[i][j] > 0.0
        dg, of = 0.0, []
        rhs = -dx * dx / dt * div[i][j]
        for (a, c), _, _, _ in _faces_of(g, i, j):
            lab = macgrid.cell_label(g, a, c)
            if lab == SOLID:
                continue
            coef = 1.0 / _rho_hat(st, st.phi[i][j], st.phi[a][c])
            dg += coef
            rhs += coef * _jump_from(st, st.phi[a][c] > 0.0, fa)  # @line L7
            if lab == FLUID:
                of.append((idx[(a, c)], coef))
        diag.append(dg)
        off.append(of)
        b.append(rhs)
    x, it = _cg(diag, off, b, tol, max(100, 4 * len(cells)))
    g.p = macgrid.zeros(g.nx, g.ny)
    for k, (i, j) in enumerate(cells):
        g.p[i][j] = x[k]
    for i in range(1, g.nx):
        for j in range(g.ny):
            _correct(st, dt, "u", i, j, (i - 1, j), (i, j))
    for i in range(g.nx):
        for j in range(1, g.ny):
            _correct(st, dt, "v", i, j, (i, j - 1), (i, j))
    return it


def _correct(st, dt, kind, i, j, ca, cb):
    g = st.g
    la, lb = g.label[ca[0]][ca[1]], g.label[cb[0]][cb[1]]
    if la == SOLID or lb == SOLID or (la != FLUID and lb != FLUID):
        return
    pa, pb = st.phi[ca[0]][ca[1]], st.phi[cb[0]][cb[1]]
    jump = _jump_from(st, pb > 0.0, pa > 0.0)  # p_b seen in the material of a
    grad = (g.p[cb[0]][cb[1]] + jump - g.p[ca[0]][ca[1]]) / g.dx
    s = dt / _rho_hat(st, pa, pb) * grad
    if kind == "u":
        g.u[i][j] -= s  # @line L8
    else:
        g.v[i][j] -= s


def step(st, dt, solid_velocity=None):
    """One step of the fire: level set, velocity advection with ghost values, temperature, buoyancy and the projection."""
    phi_old = macgrid.copy_field(st.phi)
    level_set_step(st, dt)
    gh = advect_velocity(st, dt, phi_old)
    update_temperature(st, dt, phi_old, gh)
    add_buoyancy(st, dt)
    return project(st, dt, solid_velocity)


def max_jump_divergence(st):
    """The largest |divergence| over FLUID cells, with ghost values."""
    d = jump_divergence(st)
    return max((abs(d[i][j]) for i in range(st.g.nx) for j in range(st.g.ny) if st.g.label[i][j] == FLUID), default=0.0)


def fuel_cells(st):
    """The number of FLUID cells with phi > 0."""
    g = st.g
    return sum(1 for i in range(g.nx) for j in range(g.ny) if g.label[i][j] == FLUID and st.phi[i][j] > 0.0)
