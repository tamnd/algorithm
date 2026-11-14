# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/electrostatics-based-placement/. The authors are listed in prov/KESX1E.jsonl.

"""Electrostatics-based global placement in the style of ePlace, on a small grid.

Pins 0 .. n-1 are the movable cells and pins n, n+1, ... are the fixed pads.
A cell position is its center, and every pin sits at the center of its cell.
The region is [0, M B] x [0, M B], cut into M x M bins of side B.
The cosine transforms are direct separable sums in O(M^3) time; ePlace computes
the same transforms by the FFT in O(M^2 log M) time.
The wirelength model is log-sum-exp (ePlace itself uses the weighted average model).
"""

import math


# ---------- wirelength ----------

def lse_wirelength(x, y, nets, weights, pads, gamma):
    """Return (W, gx, gy): the total LSE wirelength and its gradient over the cells."""
    n = len(x)
    gx, gy = [0.0] * n, [0.0] * n
    total = 0.0
    for e, w in zip(nets, weights):
        for coord, grad, k in ((x, gx, 0), (y, gy, 1)):
            vals = [coord[p] if p < n else pads[p - n][k] for p in e]
            hi, lo = max(vals), min(vals)
            ea = [math.exp((v - hi) / gamma) for v in vals]
            eb = [math.exp((lo - v) / gamma) for v in vals]
            sa, sb = sum(ea), sum(eb)
            total += w * (hi + gamma * math.log(sa) - lo + gamma * math.log(sb))
            for p, a, b in zip(e, ea, eb):
                if p < n:
                    grad[p] += w * (a / sa - b / sb)
    return total, gx, gy


def hpwl(x, y, nets, weights, pads):
    n = len(x)
    total = 0.0
    for e, w in zip(nets, weights):
        xs = [x[p] if p < n else pads[p - n][0] for p in e]
        ys = [y[p] if p < n else pads[p - n][1] for p in e]
        total += w * (max(xs) - min(xs) + max(ys) - min(ys))
    return total


# ---------- density and the Poisson equation ----------

def bin_density(x, y, W, H, M, B):
    """rho[u][v] = cell area inside bin (u, v), divided by the bin area B^2."""
    rho = [[0.0] * M for _ in range(M)]
    for i in range(len(x)):
        x0, x1 = x[i] - W[i] / 2, x[i] + W[i] / 2
        y0, y1 = y[i] - H[i] / 2, y[i] + H[i] / 2
        for u in range(max(0, int(x0 // B)), min(M, int(x1 // B) + 1)):
            ox = min(x1, (u + 1) * B) - max(x0, u * B)
            if ox <= 0:
                continue
            for v in range(max(0, int(y0 // B)), min(M, int(y1 // B) + 1)):
                oy = min(y1, (v + 1) * B) - max(y0, v * B)
                if oy > 0:
                    rho[u][v] += ox * oy / (B * B)
    return rho


def _table(M, f):
    """T[u][x] = f(pi u (x + 1/2) / M), the basis at the bin centers."""
    return [[f(math.pi * u * (x + 0.5) / M) for x in range(M)] for u in range(M)]


def dct2(rho):
    """Coefficients a[u][v] with rho[x][y] = sum_uv a[u][v] cos(w_u (x + 1/2)) cos(w_v (y + 1/2)),
    w_u = pi u / M. Separable direct sums."""
    M = len(rho)
    C = _table(M, math.cos)
    c = [1.0 / M] + [2.0 / M] * (M - 1)
    t = [[c[v] * sum(rho[x][y] * C[v][y] for y in range(M)) for v in range(M)] for x in range(M)]
    return [[c[u] * sum(t[x][v] * C[u][x] for x in range(M)) for v in range(M)] for u in range(M)]


def _synth(A, fu, fv):
    """S[x][y] = sum_uv A[u][v] fu[u][x] fv[v][y]."""
    M = len(A)
    t = [[sum(A[u][v] * fv[v][y] for v in range(M)) for y in range(M)] for u in range(M)]
    return [[sum(t[u][y] * fu[u][x] for u in range(M)) for y in range(M)] for x in range(M)]


def potential_and_field(rho, B):
    """Solve -lap psi = rho - mean(rho) with zero normal derivative on the border, by the cosine series.
    Return (a, psi, ex, ey) at the bin centers; the field is xi = -grad psi, in length units."""
    M = len(rho)
    a = dct2(rho)  # @line L5
    w = [math.pi * u / M for u in range(M)]
    Ap = [[0.0 if u == v == 0 else a[u][v] / (w[u] ** 2 + w[v] ** 2) for v in range(M)] for u in range(M)]
    Ax = [[Ap[u][v] * w[u] for v in range(M)] for u in range(M)]
    Ay = [[Ap[u][v] * w[v] for v in range(M)] for u in range(M)]
    C, S = _table(M, math.cos), _table(M, math.sin)
    psi = _synth(Ap, C, C)
    ex = [[val / B for val in row] for row in _synth(Ax, S, C)]
    ey = [[val / B for val in row] for row in _synth(Ay, C, S)]
    return a, psi, ex, ey


def psi_at(a, tx, ty):
    """The potential at a point (tx, ty) in bin units, from the coefficients."""
    M = len(a)
    total = 0.0
    for u in range(M):
        for v in range(M):
            if u == v == 0:
                continue
            wu, wv = math.pi * u / M, math.pi * v / M
            total += a[u][v] / (wu * wu + wv * wv) * math.cos(wu * tx) * math.cos(wv * ty)
    return total


def overflow(rho, area_total, B, target=1.0):
    """tau = sum over bins of the area above the target density, divided by the total cell area."""
    return sum(max(0.0, r - target) for row in rho for r in row) * B * B / area_total


# ---------- the placer ----------

def eplace(n, nets, pads, W, H, M, B, gamma=None, tau_stop=0.1, max_iter=300, start=None, history=None):
    """Return the cell centers after Nesterov's method on W_gamma + lambda N, as in ePlace."""
    X = M * B
    weights = [1.0] * len(nets)
    q = [W[i] * H[i] for i in range(n)]
    area = sum(q)
    deg = [0] * n
    for e in nets:
        for p in e:
            if p < n:
                deg[p] += 1
    if gamma is None:
        gamma = 0.5 * B
    if start is None:
        start = [(X / 2, X / 2)] * n
    lo = [(W[i] / 2, H[i] / 2) for i in range(n)]
    hi = [(X - W[i] / 2, X - H[i] / 2) for i in range(n)]

    def clamp(px, py):
        return ([min(max(px[i], lo[i][0]), hi[i][0]) for i in range(n)],
                [min(max(py[i], lo[i][1]), hi[i][1]) for i in range(n)])

    def gradients(px, py):
        _, wx, wy = lse_wirelength(px, py, nets, weights, pads, gamma)
        rho = bin_density(px, py, W, H, M, B)  # @line L4
        _, _, fx, fy = potential_and_field(rho, B)
        cx, cy = [], []
        for i in range(n):
            u = min(M - 1, max(0, int(px[i] // B)))
            v = min(M - 1, max(0, int(py[i] // B)))
            cx.append(fx[u][v])
            cy.append(fy[u][v])
        return wx, wy, cx, cy, rho

    vx, vy = clamp([p[0] for p in start], [p[1] for p in start])  # @line L1
    wx, wy, cx, cy, rho = gradients(vx, vy)
    dens = sum(abs(q[i] * cx[i]) + abs(q[i] * cy[i]) for i in range(n))
    lam = sum(abs(g) for g in wx + wy) / dens if dens > 0 else 1.0  # @line L2
    ux, uy = vx, vy
    a = 1.0
    prev = None
    for it in range(max_iter):  # @line L3
        if it > 0:
            wx, wy, cx, cy, rho = gradients(vx, vy)
        tau = overflow(rho, area, B)
        if history is not None:
            history.append((tau, hpwl(vx, vy, nets, weights, pads)))
        if tau <= tau_stop:  # @line L11
            ux, uy = vx, vy
            break
        gx = [(wx[i] - lam * q[i] * cx[i]) / (deg[i] + lam * q[i]) for i in range(n)]  # @line L6
        gy = [(wy[i] - lam * q[i] * cy[i]) / (deg[i] + lam * q[i]) for i in range(n)]
        if prev is None:
            alpha = 0.1 * B  # @line L7
        else:
            dv = math.sqrt(sum((vx[i] - prev[0][i]) ** 2 + (vy[i] - prev[1][i]) ** 2 for i in range(n)))
            dg = math.sqrt(sum((gx[i] - prev[2][i]) ** 2 + (gy[i] - prev[3][i]) ** 2 for i in range(n)))
            alpha = dv / dg if dg > 0 else 0.1 * B
            alpha = min(alpha, B)
        prev = (vx, vy, gx, gy)
        nux, nuy = clamp([vx[i] - alpha * gx[i] for i in range(n)], [vy[i] - alpha * gy[i] for i in range(n)])  # @line L8
        an = (1 + math.sqrt(4 * a * a + 1)) / 2  # @line L9
        beta = (a - 1) / an
        vx, vy = clamp([nux[i] + beta * (nux[i] - ux[i]) for i in range(n)],
                       [nuy[i] + beta * (nuy[i] - uy[i]) for i in range(n)])
        ux, uy, a = nux, nuy, an
        lam *= 1.1  # @line L10
    return ux, uy  # @line L12
