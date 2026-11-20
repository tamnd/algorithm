# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ghost-fluid-method/. The authors are listed in prov/73K8P0.jsonl.
"""The ghost fluid method of Fedkiw, Aslam, Merriman and Osher (1999) in one
space dimension, for two ideal gases with different ratios of specific heats,
and the ghost fluid discretization of Liu, Fedkiw and Kang (2000) for the 1D
Poisson equation (beta u')' = f with jumps [u] = a and [beta u'] = b.

Gas states are tuples (rho, rho u, E). The level set phi is negative in
fluid 0 and positive in fluid 1. Boundaries are transmissive.
"""

import math


def prim(U, g):
    rho, m, E = U
    if rho <= 0:
        raise ValueError("nonpositive density")
    u = m / rho
    return rho, u, (g - 1) * (E - 0.5 * rho * u * u)


def cons(rho, u, p, g):
    return rho, rho * u, p / (g - 1) + 0.5 * rho * u * u


def phys_flux(U, g):
    rho, u, p = prim(U, g)
    return rho * u, rho * u * u + p, (U[2] + p) * u


def speed(U, g):
    rho, u, p = prim(U, g)
    return abs(u) + math.sqrt(g * max(p, 0.0) / rho)


def rusanov(UL, UR, gl, gr):
    """Rusanov flux; gl and gr are the ratios of specific heats of the two states."""
    FL, FR = phys_flux(UL, gl), phys_flux(UR, gr)
    s = max(speed(UL, gl), speed(UR, gr))
    return tuple(0.5 * (fl + fr) - 0.5 * s * (ur - ul)
                 for fl, fr, ul, ur in zip(FL, FR, UL, UR))


def fv_step(U, gs, dx, dt):
    """One conservative Rusanov step with cell-wise gamma gs and transmissive ends."""
    m = len(U)
    E = [U[0]] + U + [U[-1]]
    G = [gs[0]] + gs + [gs[-1]]
    F = [rusanov(E[i], E[i + 1], G[i], G[i + 1]) for i in range(m + 1)]
    lam = dt / dx
    return [tuple(U[i][c] - lam * (F[i + 1][c] - F[i][c]) for c in range(3)) for i in range(m)]


def advect_level_set(phi, vel, dx, dt):
    """First-order upwind step for phi_t + u phi_x = 0 with cell velocities."""
    m = len(phi)
    out = []
    for i in range(m):
        u = vel[i]
        if u >= 0:
            d = phi[i] - phi[i - 1] if i > 0 else phi[1] - phi[0]
        else:
            d = phi[i + 1] - phi[i] if i < m - 1 else phi[-1] - phi[-2]
        out.append(phi[i] - dt / dx * u * d)
    return out


def _nearest(side, k):
    """Index of the nearest cell with side == k, for every cell (None if none)."""
    m = len(side)
    left, right = [None] * m, [None] * m
    last = None
    for i in range(m):
        if side[i] == k:
            last = i
        left[i] = last
    last = None
    for i in range(m - 1, -1, -1):
        if side[i] == k:
            last = i
        right[i] = last
    out = []
    for i in range(m):
        a, b = left[i], right[i]
        if a is None:
            out.append(b)
        elif b is None or i - a <= b - i:
            out.append(a)
        else:
            out.append(b)
    return out


def ghost_states(W, side, k, g):
    """Primitive states seen by fluid k: real cells of fluid k, ghost cells elsewhere."""
    near = _nearest(side, k)
    ext = []
    for i, (rho, u, p) in enumerate(W):
        if side[i] == k:
            ext.append((rho, u, p))
        else:
            r0, _, p0 = W[near[i]]
            s = p0 / r0 ** g                       # entropy of the nearest fluid-k cell
            ext.append(((p / s) ** (1.0 / g), u, p))
    return ext


def gfm_step(U, phi, gammas, dx, dt):
    side = [0 if v <= 0 else 1 for v in phi]
    W = [prim(U[i], gammas[side[i]]) for i in range(len(U))]
    new = {}
    for k in (0, 1):
        if k not in side:
            continue
        g = gammas[k]
        # @line L1: ghost cells of fluid k take p and u of the real fluid and the entropy of fluid k
        ext = ghost_states(W, side, k, g)
        # @line L2: one step of the single-fluid scheme for fluid k on the whole grid
        new[k] = fv_step([cons(r, u, p, g) for r, u, p in ext], [g] * len(U), dx, dt)
    # @line L3: move the level set with the fluid velocity
    phi = advect_level_set(phi, [w[1] for w in W], dx, dt)
    # @line L4: each cell keeps the new state of the fluid that the new level set gives
    U = [new[0 if phi[i] <= 0 else 1][i] for i in range(len(U))]
    return U, phi


def naive_step(U, phi, gammas, dx, dt):
    """Conservative one-fluid scheme with the gamma of each cell from the level set."""
    side = [0 if v <= 0 else 1 for v in phi]
    gs = [gammas[s] for s in side]
    vel = [prim(U[i], gs[i])[1] for i in range(len(U))]
    return fv_step(U, gs, dx, dt), advect_level_set(phi, vel, dx, dt)


def run(step, U, phi, gammas, dx, T, cfl=0.5):
    t = 0.0
    while t < T - 1e-14:
        side = [0 if v <= 0 else 1 for v in phi]
        smax = max(speed(U[i], gammas[side[i]]) for i in range(len(U)))
        dt = min(cfl * dx / smax, T - t)
        U, phi = step(U, phi, gammas, dx, dt)
        t += dt
    return U, phi


def primitives(U, phi, gammas):
    return [prim(U[i], gammas[0 if phi[i] <= 0 else 1]) for i in range(len(U))]


def gfm_poisson_1d(n, alpha, beta_minus, beta_plus, f, a, b, u_left, u_right):
    """Solve (beta u')' = f on [0, 1] with u(0), u(1) given and an interface at alpha.

    beta = beta_minus on [0, alpha) and beta_plus on (alpha, 1]. The jumps are
    u(alpha+) - u(alpha-) = a and beta u'(alpha+) - beta u'(alpha-) = b.
    Nodes x_i = i / n; returns the list of nodes and the values u_0, ..., u_n.
    """
    h = 1.0 / n
    x = [i * h for i in range(n + 1)]
    k = int(alpha / h)
    if not (0 < k < n - 1) or x[k] > alpha or alpha >= x[k + 1]:
        raise ValueError("interface must lie strictly inside the grid")
    theta = (alpha - x[k]) / h
    bhat = beta_minus * beta_plus / (beta_plus * theta + beta_minus * (1 - theta))
    face = []                                     # beta at faces i + 1/2, i = 0..n-1
    for i in range(n):
        face.append(bhat if i == k else (beta_minus if i < k else beta_plus))
    lo, di, up, rhs = [], [], [], []
    for i in range(1, n):
        lo.append(face[i - 1] / h ** 2)
        di.append(-(face[i - 1] + face[i]) / h ** 2)
        up.append(face[i] / h ** 2)
        r = f(x[i])
        if i == k:
            r += bhat * a / h ** 2 + bhat * b * (1 - theta) / (beta_plus * h)
        elif i == k + 1:
            r += -bhat * a / h ** 2 + bhat * b * theta / (beta_minus * h)
        rhs.append(r)
    rhs[0] -= lo[0] * u_left
    rhs[-1] -= up[-1] * u_right
    # Thomas algorithm (the matrix is symmetric and negative definite)
    m = n - 1
    c, d = [0.0] * m, [0.0] * m
    c[0], d[0] = up[0] / di[0], rhs[0] / di[0]
    for i in range(1, m):
        den = di[i] - lo[i] * c[i - 1]
        c[i] = up[i] / den
        d[i] = (rhs[i] - lo[i] * d[i - 1]) / den
    u = [0.0] * m
    u[-1] = d[-1]
    for i in range(m - 2, -1, -1):
        u[i] = d[i] - c[i] * u[i + 1]
    return x, [u_left] + u + [u_right]
