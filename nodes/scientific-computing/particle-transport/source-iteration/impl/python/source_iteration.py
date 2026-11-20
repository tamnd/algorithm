# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/source-iteration/. The authors are listed in prov/ZGYN85.jsonl.
"""Source iteration for the one-speed S_N equations in a slab.

The slab has M cells of widths dx[j] with the total cross section sigma_t[j],
the scattering cross section sigma_s[j] (both in cm^-1) and an isotropic
source q[j]. Scattering is isotropic. The scalar flux is phi = integral of
psi over mu in [-1, 1], so the emission per unit mu is (sigma_s phi + q) / 2
and the Gauss-Legendre weights sum to 2. Space is discretized by diamond
differences.

Source iteration: phi_(l+1) = sweep of the source (sigma_s phi_l + q) / 2,
integrated with the weights. Each sweep inverts the streaming and collision
operator exactly, direction by direction.

Faces: "vacuum", "reflect", or a list of incoming angular fluxes (one per
entering direction, in the order of the rule). Reflection is exact inside
each sweep, not lagged: with one reflecting face the directions that leave
through it are swept first; with two reflecting faces the incoming value of
each pair of mirror directions is found from the scalar equation
a = R2 (R1 a + s1) + t2, which uses that a diamond difference sweep is affine
in its incoming value.
"""

import math


def legendre(n: int, x: float):
    """P_n(x) and its derivative, by the three-term recurrence."""
    if n == 0:
        return 1.0, 0.0
    p0, p1 = 1.0, x
    for k in range(2, n + 1):
        p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
    return p1, n * (x * p1 - p0) / (x * x - 1.0)


def gauss_legendre(n: int):
    """Nodes in increasing order and weights of the n-point Gauss-Legendre rule on [-1, 1]."""
    nodes, weights = [0.0] * n, [0.0] * n
    for i in range((n + 1) // 2):
        x = math.cos(math.pi * (i + 0.75) / (n + 0.5))
        for _ in range(100):
            p, dp = legendre(n, x)
            step = p / dp
            x -= step
            if abs(step) < 1e-16:
                break
        p, dp = legendre(n, x)
        w = 2.0 / ((1.0 - x * x) * dp * dp)
        nodes[n - 1 - i], weights[n - 1 - i] = x, w
        nodes[i], weights[i] = -x, w
    return nodes, weights


def dd_sweep(mu: float, psi_in: float, sigma_t, src, dx):
    """Diamond difference sweep of one direction. Returns (cell values, outgoing value)."""
    m = len(dx)
    cells = [0.0] * m
    order = range(m) if mu > 0 else range(m - 1, -1, -1)
    psi = psi_in
    for j in order:
        a = 2.0 * abs(mu) / dx[j]
        cells[j] = (src[j] + a * psi) / (sigma_t[j] + a)
        psi = 2.0 * cells[j] - psi
    return cells, psi


def transmission_factor(mu: float, sigma_t, dx):
    """R = product of (2 - tau_j) / (2 + tau_j): the outgoing value per unit incoming value without a source."""
    r = 1.0
    for st, h in zip(sigma_t, dx):
        tau = st * h / abs(mu)
        r *= (2.0 - tau) / (2.0 + tau)
    return r


def sweep_all(mus, ws, sigma_t, src, dx, left="vacuum", right="vacuum"):
    """Sweep every direction with the cell source src. Returns (phi, leak_left, leak_right).

    leak_left and leak_right are the partial currents that leave at x = 0 and at x = L."""
    n, m = len(mus), len(dx)
    phi = [0.0] * m
    leak_left = leak_right = 0.0
    pos = [k for k in range(n) if mus[k] > 0]
    for idx, k in enumerate(pos):
        kb = n - 1 - k  # the mirror direction, mus[kb] = -mus[k]
        mu, w = mus[k], ws[k]
        if left == "reflect" and right == "reflect":
            _, s1 = dd_sweep(mu, 0.0, sigma_t, src, dx)
            _, t2 = dd_sweep(-mu, 0.0, sigma_t, src, dx)
            r = transmission_factor(mu, sigma_t, dx)
            a = (r * s1 + t2) / (1.0 - r * r)
            fwd, out_r = dd_sweep(mu, a, sigma_t, src, dx)
            bwd, out_l = dd_sweep(-mu, out_r, sigma_t, src, dx)
        elif left == "reflect":
            b = 0.0 if right == "vacuum" else right[len(pos) - 1 - idx]
            bwd, out_l = dd_sweep(-mu, b, sigma_t, src, dx)
            fwd, out_r = dd_sweep(mu, out_l, sigma_t, src, dx)
        elif right == "reflect":
            a = 0.0 if left == "vacuum" else left[idx]
            fwd, out_r = dd_sweep(mu, a, sigma_t, src, dx)
            bwd, out_l = dd_sweep(-mu, out_r, sigma_t, src, dx)
        else:
            a = 0.0 if left == "vacuum" else left[idx]
            b = 0.0 if right == "vacuum" else right[len(pos) - 1 - idx]
            fwd, out_r = dd_sweep(mu, a, sigma_t, src, dx)
            bwd, out_l = dd_sweep(-mu, b, sigma_t, src, dx)
        for j in range(m):
            phi[j] += w * (fwd[j] + bwd[j])
        if right != "reflect":
            leak_right += w * mu * out_r
        if left != "reflect":
            leak_left += w * mu * out_l
    return phi, leak_left, leak_right


def source_iteration(n, sigma_t, sigma_s, q, dx, left="vacuum", right="vacuum",
                     tol=1e-10, max_iter=100000, phi0=None):
    """Iterate phi <- sweep((sigma_s phi + q) / 2) until the largest change is at most tol times the largest phi.

    Returns a dict with phi, the leakages, the number of iterations and the
    list of the largest changes (one per iteration)."""
    mus, ws = gauss_legendre(n)
    m = len(dx)
    phi = list(phi0) if phi0 is not None else [0.0] * m  # @line L1
    changes = []
    leak_left = leak_right = 0.0
    it = 0
    for it in range(1, max_iter + 1):  # @line L2
        src = [(sigma_s[j] * phi[j] + q[j]) / 2.0 for j in range(m)]  # @line L3
        new, leak_left, leak_right = sweep_all(mus, ws, sigma_t, src, dx, left, right)  # @line L4
        change = max(abs(new[j] - phi[j]) for j in range(m))  # @line L5
        phi = new
        changes.append(change)
        if change <= tol * (max(abs(v) for v in phi) or 1.0):  # @line L6
            break
    return {"phi": phi, "leak_left": leak_left, "leak_right": leak_right,
            "iterations": it, "changes": changes}


def fourier_continuous(lam: float, c: float) -> float:
    """Eigenvalue of source iteration for the error mode exp(i lam sigma_t x) in an infinite medium, exact angle and space."""
    if lam == 0.0:
        return c
    return c * math.atan(lam) / lam


def fourier_sn(lam: float, c: float, mus, ws) -> float:
    """The same with the S_N quadrature in angle and exact space: (c / 2) sum of w / (1 + lam^2 mu^2)."""
    return 0.5 * c * sum(w / (1.0 + (lam * mu) ** 2) for mu, w in zip(mus, ws))


def fourier_dd(theta: float, c: float, tau_cell: float, mus, ws) -> float:
    """The same with S_N and diamond differences on equal cells of optical thickness tau_cell, for the mode exp(i theta j)."""
    lam = 2.0 * math.tan(theta / 2.0) / tau_cell
    return fourier_sn(lam, c, mus, ws)


def error_bound(change: float, rho: float) -> float:
    """Bound on the remaining error when the error contracts by rho < 1 per iteration and the last change was change."""
    return rho / (1.0 - rho) * change
