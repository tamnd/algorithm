# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/level-set-topology-optimization/. The authors are listed in prov/H8FVX0.jsonl.

"""A toy level set method for minimum compliance, after Wang, Wang and Guo (2003)
and Allaire, Jouve and Toader (2004). This is a demonstration, not a production code.

The level set function phi has one value per element of an nelx x nely grid of
unit square Q4 elements. Element e is solid if phi_e < 0 and is ersatz material
of stiffness eps otherwise. Each iteration solves the finite element model,
takes the strain energy density w_e = u_e^T k0 u_e as the shape sensitivity,
and moves the boundary with one upwind step of the Hamilton-Jacobi equation
phi_t + V |grad phi| = 0 with the normal speed V = w / max(w) - l. The
multiplier l in [0, 1] is found by bisection so that the solid volume stays at
most the bound. Every few iterations phi is reset to a signed distance by a
brute force search over the zero crossings.

The finite element part is in fem2d.py, a shared helper.
"""

import math

from fem2d import element_energies, q4_stiffness, solve


def at(phi, nelx, nely, i, j):
    """phi at the element (i, j), with the edge values repeated outside the grid."""
    i = min(max(i, 0), nelx - 1)
    j = min(max(j, 0), nely - 1)
    return phi[i * nely + j]


def upwind_gradients_sq(phi, nelx, nely, i, j):
    """The squares of the Osher-Sethian upwind gradient norms (grad+, grad-) at (i, j)."""
    c = at(phi, nelx, nely, i, j)
    dxm = c - at(phi, nelx, nely, i - 1, j)  # @line L10
    dxp = at(phi, nelx, nely, i + 1, j) - c
    dym = c - at(phi, nelx, nely, i, j - 1)
    dyp = at(phi, nelx, nely, i, j + 1) - c
    zero = 0 * c
    gp = max(dxm, zero) ** 2 + min(dxp, zero) ** 2 + max(dym, zero) ** 2 + min(dyp, zero) ** 2  # @line L11
    gm = min(dxm, zero) ** 2 + max(dxp, zero) ** 2 + min(dym, zero) ** 2 + max(dyp, zero) ** 2
    return gp, gm


def hj_step(phi, nelx, nely, speed, dt, sqrt=math.sqrt):
    """One explicit upwind step of phi_t + V |grad phi| = 0 (grid spacing 1)."""
    out = []
    for i in range(nelx):
        for j in range(nely):
            e = i * nely + j
            gp, gm = upwind_gradients_sq(phi, nelx, nely, i, j)
            v = speed[e]
            out.append(phi[e] - dt * (max(v, 0) * sqrt(gp) + min(v, 0) * sqrt(gm)))  # @line L12
    return out


def zero_crossings(phi, nelx, nely):
    """Points where phi changes sign between the centers of neighbouring elements."""
    pts = []
    for i in range(nelx):
        for j in range(nely):
            a = phi[i * nely + j]
            for di, dj in ((1, 0), (0, 1)):
                if i + di < nelx and j + dj < nely:
                    b = phi[(i + di) * nely + j + dj]
                    if (a < 0) != (b < 0):
                        t = a / (a - b)  # in (0, 1]
                        pts.append((i + 0.5 + di * t, j + 0.5 + dj * t))
    return pts


def reinitialize(phi, nelx, nely):
    """Replace phi by the signed distance to its zero crossings; the sign of each element is kept."""
    pts = zero_crossings(phi, nelx, nely)  # @line L13
    if not pts:
        return list(phi)
    out = []
    for i in range(nelx):
        for j in range(nely):
            d = min(math.hypot(i + 0.5 - x, j + 0.5 - y) for x, y in pts)
            out.append(-d if phi[i * nely + j] < 0 else d)  # @line L14
    return out


def smooth_field(w, nelx, nely):
    """The mean over the element and its 4 neighbours inside the grid."""
    out = []
    for i in range(nelx):
        for j in range(nely):
            vals = [w[a * nely + b] for a, b in ((i, j), (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))
                    if 0 <= a < nelx and 0 <= b < nely]
            out.append(sum(vals) / len(vals))
    return out


def solid_count(phi):
    return sum(1 for v in phi if v < 0)


def compliance_of(nelx, nely, ke, solid, force, fixed, eps):
    scale = [1.0 if s else eps for s in solid]
    u = solve(nelx, nely, ke, scale, force, fixed)
    return sum(v * u[k] for k, v in force.items()), u


def level_set_topology(nelx, nely, volfrac, phi0, force, fixed, iters=60, dt=0.5,
                       eps=1e-3, reinit_every=5, nu=0.3, steps=40, smooth=1):
    """Return (phi, history): the final level set and the compliance of each iteration."""
    ke = [[float(v) for v in row] for row in q4_stiffness(nu)]
    bound = int(volfrac * nelx * nely)
    phi = list(phi0)  # @line L1
    history = []
    for it in range(1, iters + 1):  # @line L2
        solid = [v < 0 for v in phi]  # @line L3
        c, u = compliance_of(nelx, nely, ke, solid, force, fixed, eps)  # @line L4
        history.append(c)
        w = element_energies(nelx, nely, ke, u)
        for _ in range(smooth):
            w = smooth_field(w, nelx, nely)
        top = max(w)
        w = [x / top for x in w]  # @line L5

        def trial(lam):
            return hj_step(phi, nelx, nely, [x - lam for x in w], dt)

        lo, hi = 0.0, 1.0  # @line L6
        if solid_count(trial(hi)) <= bound:
            for _ in range(steps):
                mid = (lo + hi) / 2
                if solid_count(trial(mid)) <= bound:
                    hi = mid
                else:
                    lo = mid
        phi = trial(hi)  # @line L7
        if it % reinit_every == 0:  # @line L8
            phi = reinitialize(phi, nelx, nely)
    solid = [v < 0 for v in phi]
    history.append(compliance_of(nelx, nely, ke, solid, force, fixed, eps)[0])
    return phi, history  # @line L9


def holes_start(nelx, nely, volfrac, kx=4, ky=2):
    """A start with a regular pattern of holes, shifted so that the solid volume meets the bound."""
    base = [-math.cos(2 * math.pi * kx * (i + 0.5) / nelx) * math.cos(2 * math.pi * ky * (j + 0.5) / nely)
            for i in range(nelx) for j in range(nely)]
    bound = int(volfrac * nelx * nely)
    # the shift that leaves exactly `bound` negative values (ties are broken by the sort)
    order = sorted(base)
    shift = (order[bound - 1] + order[bound]) / 2 if bound < len(order) else order[-1] + 1
    return [b - shift for b in base]


def cantilever(nelx, nely):
    """Left edge clamped, unit load down at the middle of the right edge."""
    n = nelx * (nely + 1) + nely // 2
    force = {2 * n + 1: -1.0}
    fixed = [k for j in range(nely + 1) for k in (2 * j, 2 * j + 1)]
    return force, fixed


def show(phi, nelx, nely):
    return "\n".join("".join("#" if phi[i * nely + j] < 0 else "." for i in range(nelx))
                     for j in range(nely - 1, -1, -1))


if __name__ == "__main__":
    nelx, nely, vf = 32, 16, 0.5
    force, fixed = cantilever(nelx, nely)
    phi0 = holes_start(nelx, nely, vf)
    print(show(phi0, nelx, nely))
    phi, hist = level_set_topology(nelx, nely, vf, phi0, force, fixed)
    print(show(phi, nelx, nely))
    print("start", round(hist[0], 2), "end", round(hist[-1], 2), "min", round(min(hist), 2),
          "solid", solid_count(phi), "of", nelx * nely)
