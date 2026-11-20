# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-ordinates-method/. The authors are listed in prov/S57PHM.jsonl.
"""The discrete ordinates (S_N) method for one-speed transport in a slab.

The slab 0 <= x <= L is cut into M cells of widths dx[j], each with a total
cross section sigma_t[j], a scattering cross section sigma_s[j] (both in
cm^-1) and an isotropic source q[j] per unit length. Scattering is isotropic.
The convention is phi(x) = integral of psi(x, mu) over mu in [-1, 1], so the
emission density per unit mu is (sigma_s phi + q) / 2 and the weights of the
Gauss-Legendre rule sum to 2.

The angular variable is replaced by the N Gauss-Legendre directions mu_n
(N even). The space variable is discretized by diamond differences: in each
cell, psi_cell = (psi_in + psi_out) / 2. The coupled equations are solved by
source iteration: a transport sweep for each direction with the scattering
source of the last iterate.

Boundary conditions: "vacuum" (no incoming flux), "reflect" (the incoming
flux at a face is the outgoing flux in the mirror direction, from the last
iteration), or a list of incoming angular fluxes, one per direction that
enters the slab at that face (in the order of the rule).
"""

import math


def legendre(n: int, x: float):
    """P_n(x) and its derivative, by the three-term recurrence."""
    p0, p1 = 1.0, x
    if n == 0:
        return 1.0, 0.0
    for k in range(2, n + 1):
        p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
    dp = n * (x * p1 - p0) / (x * x - 1.0)
    return p1, dp


def gauss_legendre(n: int):
    """Nodes (in increasing order) and weights of the n-point Gauss-Legendre rule on [-1, 1]."""
    nodes, weights = [0.0] * n, [0.0] * n
    for i in range((n + 1) // 2):
        x = math.cos(math.pi * (i + 0.75) / (n + 0.5))  # a start near the i-th largest root
        for _ in range(100):
            p, dp = legendre(n, x)
            dx = p / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        p, dp = legendre(n, x)
        w = 2.0 / ((1.0 - x * x) * dp * dp)
        nodes[n - 1 - i], weights[n - 1 - i] = x, w
        nodes[i], weights[i] = -x, w
    return nodes, weights


def sweep_cell(mu_abs: float, psi_in: float, sigma_t: float, src: float, dx: float):
    """Diamond difference in one cell. Returns (cell average, outgoing flux)."""
    a = 2.0 * mu_abs / dx
    psi_c = (src + a * psi_in) / (sigma_t + a)
    return psi_c, 2.0 * psi_c - psi_in


def sweep(mu: float, psi_in: float, sigma_t, src, dx):
    """Sweep one direction through all cells in the direction of flight.

    Returns (cell averages in cell order, outgoing flux at the far face)."""
    m = len(dx)
    cells = [0.0] * m
    order = range(m) if mu > 0 else range(m - 1, -1, -1)
    psi = psi_in
    for j in order:
        cells[j], psi = sweep_cell(abs(mu), psi, sigma_t[j], src[j], dx[j])
    return cells, psi


def discrete_ordinates(n, sigma_t, sigma_s, q, dx, left="vacuum", right="vacuum", tol=1e-10, max_iter=100000):
    """Solve the S_N equations with diamond differences by source iteration.

    Returns a dict with phi (cell-average scalar flux), psi (psi[n][j]),
    the outgoing angular fluxes at both faces, the partial currents that
    leave at both faces, and the number of iterations."""
    mus, ws = gauss_legendre(n)  # @line L1
    m = len(dx)
    pos = [k for k in range(n) if mus[k] > 0]
    neg = [k for k in range(n) if mus[k] < 0]
    mirror = {k: n - 1 - k for k in range(n)}
    out_left = {k: 0.0 for k in neg}  # psi leaving at x = 0
    out_right = {k: 0.0 for k in pos}  # psi leaving at x = L
    phi = [0.0] * m  # @line L2
    psi = [[0.0] * m for _ in range(n)]
    for it in range(1, max_iter + 1):  # @line L3
        src = [(sigma_s[j] * phi[j] + q[j]) / 2.0 for j in range(m)]  # @line L4
        new_left, new_right = {}, {}
        for idx, k in enumerate(pos):  # @line L5
            if left == "vacuum":  # @line L6
                psi_in = 0.0
            elif left == "reflect":
                psi_in = out_left[mirror[k]]
            else:
                psi_in = left[idx]
            psi[k], new_right[k] = sweep(mus[k], psi_in, sigma_t, src, dx)  # @line L7
        for idx, k in enumerate(neg):  # @line L8
            if right == "vacuum":
                psi_in = 0.0
            elif right == "reflect":
                psi_in = out_right[mirror[k]]
            else:
                psi_in = right[idx]
            psi[k], new_left[k] = sweep(mus[k], psi_in, sigma_t, src, dx)
        out_left, out_right = new_left, new_right
        new_phi = [sum(ws[k] * psi[k][j] for k in range(n)) for j in range(m)]  # @line L9
        change = max(abs(new_phi[j] - phi[j]) for j in range(m))
        scale = max(abs(v) for v in new_phi) or 1.0
        phi = new_phi
        if change <= tol * scale:  # @line L10
            break
    j_left = sum(ws[k] * abs(mus[k]) * out_left[k] for k in neg)
    j_right = sum(ws[k] * mus[k] * out_right[k] for k in pos)
    return {"phi": phi, "psi": psi, "mu": mus, "w": ws, "out_left": out_left, "out_right": out_right,
            "leak_left": j_left, "leak_right": j_right, "iterations": it}
