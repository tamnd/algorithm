# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-interpolation-material-point/. The authors are listed in prov/4J3GZH.jsonl.
"""The generalized interpolation material point (GIMP) method in 1D.

Each material point p has a domain [x_p - l_p, x_p + l_p]. The grid uses the
linear hats N_i(x) = max(0, 1 - |x - x_i| / dx), x_i = i dx. The GIMP weight
of node i is the mean of N_i over the domain,

    S_ip = (1 / (2 l_p)) * integral of N_i over [x_p - l_p, x_p + l_p],

and its gradient with respect to x_p is

    dS_ip = (N_i(x_p + l_p) - N_i(x_p - l_p)) / (2 l_p).

In 1D the domain follows the deformation: l_p = F_p l_p^0 (the "contiguous
particle" form, cpGIMP). The rest of the step is the update-stress-last MPM
step with the FLIP velocity update.

Cost per step: Theta(N + n) time for N points and n nodes, if l_p <= dx.
"""

import math
from dataclasses import dataclass, field


def hat(t: float) -> float:
    """N(t) = max(0, 1 - |t|) in units of dx."""
    return max(0.0, 1.0 - abs(t))


def hat_integral(t: float) -> float:
    """Phi(t) = integral of N from -infinity to t, in units of dx."""
    if t <= -1:
        return 0.0
    if t <= 0:
        return (t + 1) ** 2 / 2
    if t <= 1:
        return 1 - (1 - t) ** 2 / 2
    return 1.0


def gimp_weights(x: float, lp: float, dx: float) -> list[tuple[int, float, float]]:
    """(i, S_ip, dS_ip) for every node i whose hat overlaps the domain [x - lp, x + lp]; lp > 0."""
    a, b = x - lp, x + lp
    out = []
    for i in range(math.floor(a / dx) - 1, math.floor(b / dx) + 2):  # @line L2
        s = dx * (hat_integral((b - i * dx) / dx) - hat_integral((a - i * dx) / dx)) / (2 * lp)  # @line L3
        g = (hat((b - i * dx) / dx) - hat((a - i * dx) / dx)) / (2 * lp)  # @line L4
        if s != 0.0 or g != 0.0:
            out.append((i, s, g))
    return out


@dataclass
class Points:
    x: list[float]
    v: list[float]
    m: list[float]
    vol0: list[float]
    l0: list[float]
    F: list[float] = field(default_factory=list)
    stress: list[float] = field(default_factory=list)

    def __post_init__(self):
        if not self.F:
            self.F = [1.0] * len(self.x)
        if not self.stress:
            self.stress = [0.0] * len(self.x)


def grid_force(ps: Points, dx: float, n: int) -> list[float]:
    """f_i = -sum_p V_p sigma_p dS_ip with V_p = F_p V_p^0 and l_p = F_p l_p^0."""
    f = [0.0] * n
    for p in range(len(ps.x)):
        for i, _, g in gimp_weights(ps.x[p], ps.F[p] * ps.l0[p], dx):
            f[i] -= ps.F[p] * ps.vol0[p] * ps.stress[p] * g
    return f


def gimp_step(ps: Points, dx: float, n: int, young: float, h: float, fixed: frozenset = frozenset()) -> Points:
    """One update-stress-last step with GIMP weights, for sigma_dot = E eps_dot."""
    mass, mom = [0.0] * n, [0.0] * n
    weights = []
    for p in range(len(ps.x)):  # @line L1
        ws = gimp_weights(ps.x[p], ps.F[p] * ps.l0[p], dx)
        weights.append(ws)
        for i, s, _ in ws:
            mass[i] += s * ps.m[p]  # @line L5
            mom[i] += s * ps.m[p] * ps.v[p]  # @line L5
    f = grid_force(ps, dx, n)  # @line L6
    v_old = [mom[i] / mass[i] if mass[i] > 0 else 0.0 for i in range(n)]  # @line L7
    v_new = [v_old[i] + h * f[i] / mass[i] if mass[i] > 0 else 0.0 for i in range(n)]  # @line L7
    for i in fixed:  # @line L7
        v_new[i] = 0.0  # @line L7
    acc = [(v_new[i] - v_old[i]) / h for i in range(n)]  # @line L7
    out = Points(list(ps.x), list(ps.v), list(ps.m), list(ps.vol0), list(ps.l0), list(ps.F), list(ps.stress))
    for p, ws in enumerate(weights):  # @line L8
        out.v[p] = ps.v[p] + h * sum(s * acc[i] for i, s, _ in ws)  # @line L9
        out.x[p] = ps.x[p] + h * sum(s * v_new[i] for i, s, _ in ws)  # @line L9
        rate = sum(g * v_new[i] for i, _, g in ws)  # @line L10
        out.F[p] = ps.F[p] * (1 + h * rate)  # @line L10
        out.stress[p] = ps.stress[p] + young * h * rate  # @line L10
    return out  # @line L11


def vibrating_bar(cells: int, ppc: int, length: float, rho: float, v0: float):
    """Points of a bar on [0, length] in its first mode, with domains that tile the bar."""
    dx = length / cells
    xs, vs, ms, vols, ls = [], [], [], [], []
    for c in range(cells):
        for k in range(ppc):
            x = (c + (k + 0.5) / ppc) * dx
            xs.append(x)
            vs.append(v0 * math.sin(math.pi * x / (2 * length)))
            vols.append(dx / ppc)
            ms.append(rho * dx / ppc)
            ls.append(dx / (2 * ppc))
    return Points(xs, vs, ms, vols, ls), dx, cells + 3
