# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffusion-synthetic-acceleration/. The authors are listed in prov/XAVARJ.jsonl.
"""Diffusion synthetic acceleration (DSA) of source iteration for the slab S_N equations with diamond differences.

The slab has M cells with sigma_t[j], sigma_s[j], an isotropic source q[j]
and widths dx[j]. The scalar flux is phi = integral of psi over mu in
[-1, 1], so the emission per unit mu is (sigma_s phi + q) / 2 and the
Gauss-Legendre weights sum to 2. Faces are "vacuum" or "reflect".

One DSA iteration:
    1. sweep with the source of the last iterate: phi_half
    2. the residual R_j = sigma_s,j (phi_half_j - phi_j)
    3. solve a diffusion equation for the correction f with the source R
    4. phi_new = phi_half + f

accel = "consistent": the diffusion equation for the edge values f_i is the
one obtained from the diamond difference P1 equations by eliminating the
current (the method of Alcouffe 1977). With g = 2 / (3 sigma_t dx) and the
absorption sigma_a = sigma_t - sigma_s, the row of edge i between the cells
L (left) and R (right) is

    (-g_L + sa_L dx_L / 2) f_(i-1) + (g_L + g_R + sa_L dx_L / 2 + sa_R dx_R / 2) f_i
        + (-g_R + sa_R dx_R / 2) f_(i+1) = R_L dx_L + R_R dx_R.

A vacuum face adds 1 to its diagonal entry (the Marshak condition
J_out = f / 2), and a reflecting face adds nothing. The cell correction is
the mean of the two edge values.

accel = "inconsistent": the usual cell-centered diffusion equation with the
face coefficient 1 / (dx_L / (2 D_L) + dx_R / (2 D_R)), D = 1 / (3 sigma_t).
This is a correct discretization of diffusion, but not the one consistent with
diamond difference, and it diverges for thick cells.

accel = "none": plain source iteration.
"""

import math

from scisparse import thomas


def legendre(n: int, x: float):
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


def _dd(mu, psi, sigma_t, src, dx):
    m = len(dx)
    cells = [0.0] * m
    for j in (range(m) if mu > 0 else range(m - 1, -1, -1)):
        a = 2.0 * abs(mu) / dx[j]
        cells[j] = (src[j] + a * psi) / (sigma_t[j] + a)
        psi = 2.0 * cells[j] - psi
    return cells, psi


def sweep(mus, ws, sigma_t, src, dx, left="vacuum", right="vacuum"):
    """Scalar flux of one diamond difference sweep of all directions; reflection is exact. Returns (phi, leak_left, leak_right)."""
    n, m = len(mus), len(dx)
    phi = [0.0] * m
    leak_l = leak_r = 0.0
    for k in range(n // 2, n):
        mu, w = mus[k], ws[k]
        if left == "reflect" and right == "reflect":
            _, s1 = _dd(mu, 0.0, sigma_t, src, dx)
            _, t2 = _dd(-mu, 0.0, sigma_t, src, dx)
            r = 1.0
            for st, h in zip(sigma_t, dx):
                tau = st * h / mu
                r *= (2.0 - tau) / (2.0 + tau)
            fwd, out_r = _dd(mu, (r * s1 + t2) / (1.0 - r * r), sigma_t, src, dx)
            bwd, out_l = _dd(-mu, out_r, sigma_t, src, dx)
        elif left == "reflect":
            bwd, out_l = _dd(-mu, 0.0, sigma_t, src, dx)
            fwd, out_r = _dd(mu, out_l, sigma_t, src, dx)
        else:
            fwd, out_r = _dd(mu, 0.0, sigma_t, src, dx)
            bwd, out_l = _dd(-mu, out_r if right == "reflect" else 0.0, sigma_t, src, dx)
        for j in range(m):
            phi[j] += w * (fwd[j] + bwd[j])
        if right != "reflect":
            leak_r += w * mu * out_r
        if left != "reflect":
            leak_l += w * mu * out_l
    return phi, leak_l, leak_r


def consistent_correction(sigma_t, sigma_s, dx, res, left="vacuum", right="vacuum"):
    """Cell corrections from the edge diffusion equation with the source res (the residual sigma_s (phi_half - phi))."""
    m = len(dx)
    n = m + 1
    a, b, c, d = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
    for j in range(m):
        g = 2.0 / (3.0 * sigma_t[j] * dx[j])
        sa = (sigma_t[j] - sigma_s[j]) * dx[j] / 2.0
        # cell j couples its left edge j and its right edge j + 1
        b[j] += g + sa
        c[j] += -g + sa
        a[j + 1] += -g + sa
        b[j + 1] += g + sa
        d[j] += res[j] * dx[j]
        d[j + 1] += res[j] * dx[j]
    if left == "vacuum":
        b[0] += 1.0
    if right == "vacuum":
        b[m] += 1.0
    f = thomas(a, b, c, d)
    return [(f[j] + f[j + 1]) / 2.0 for j in range(m)]


def inconsistent_correction(sigma_t, sigma_s, dx, res, left="vacuum", right="vacuum"):
    """Cell corrections from the cell-centered diffusion equation with Marshak or reflecting faces."""
    m = len(dx)
    D = [1.0 / (3.0 * s) for s in sigma_t]
    a, b, c, d = [0.0] * m, [0.0] * m, [0.0] * m, [0.0] * m
    for j in range(m):
        b[j] = (sigma_t[j] - sigma_s[j]) * dx[j]
        d[j] = res[j] * dx[j]
    for j in range(m - 1):
        g = 1.0 / (dx[j] / (2.0 * D[j]) + dx[j + 1] / (2.0 * D[j + 1]))
        b[j] += g
        b[j + 1] += g
        c[j] -= g
        a[j + 1] -= g
    if left == "vacuum":
        b[0] += 1.0 / (dx[0] / (2.0 * D[0]) + 2.0)
    if right == "vacuum":
        b[-1] += 1.0 / (dx[-1] / (2.0 * D[-1]) + 2.0)
    return thomas(a, b, c, d)


def dsa(n, sigma_t, sigma_s, q, dx, left="vacuum", right="vacuum", accel="consistent",
        tol=1e-10, max_iter=10000, phi0=None):
    """Source iteration with diffusion synthetic acceleration.

    Returns a dict with phi, the leakages, the number of iterations and the list of the largest changes."""
    mus, ws = gauss_legendre(n)
    m = len(dx)
    phi = list(phi0) if phi0 is not None else [0.0] * m  # @line L1
    changes = []
    leak_l = leak_r = 0.0
    it = 0
    for it in range(1, max_iter + 1):  # @line L2
        src = [(sigma_s[j] * phi[j] + q[j]) / 2.0 for j in range(m)]  # @line L3
        half, leak_l, leak_r = sweep(mus, ws, sigma_t, src, dx, left, right)  # @line L4
        res = [sigma_s[j] * (half[j] - phi[j]) for j in range(m)]  # @line L5
        if accel == "consistent":
            corr = consistent_correction(sigma_t, sigma_s, dx, res, left, right)  # @line L6
        elif accel == "inconsistent":
            corr = inconsistent_correction(sigma_t, sigma_s, dx, res, left, right)
        else:
            corr = [0.0] * m
        new = [half[j] + corr[j] for j in range(m)]  # @line L7
        change = max(abs(new[j] - phi[j]) for j in range(m))
        phi = new
        changes.append(change)
        if not math.isfinite(change) or change <= tol * (max(abs(v) for v in phi) or 1.0):  # @line L8
            break
    return {"phi": phi, "leak_left": leak_l, "leak_right": leak_r, "iterations": it, "changes": changes}


def fourier_si(lam, c, mus=None, ws=None):
    """Source iteration factor (c / 2) sum w / (1 + lam^2 mu^2); with mus = None the exact angular integral c atan(lam) / lam."""
    if mus is None:
        return c if lam == 0.0 else c * math.atan(lam) / lam
    return 0.5 * c * sum(w / (1.0 + (lam * mu) ** 2) for mu, w in zip(mus, ws))


def fourier_dsa(lam, c, mus=None, ws=None):
    """DSA factor omega_SI - c (1 - omega_SI) / (1 - c + lam^2 / 3) for the mode with the wave number lam sigma_t."""
    if lam == 0.0:
        return 0.0  # the flat mode is removed exactly; this is also the limit for c = 1
    w = fourier_si(lam, c, mus, ws)
    return w - c * (1.0 - w) / (1.0 - c + lam * lam / 3.0)


def fourier_dsa_dd(theta, c, tau, mus, ws):
    """Consistent DSA with diamond difference on equal cells of optical thickness tau, for the mode cos(theta (j + 1/2))."""
    return fourier_dsa(2.0 * math.tan(theta / 2.0) / tau, c, mus, ws)


def fourier_dsa_inconsistent(theta, c, tau, mus, ws):
    """Inconsistent cell-centered DSA with diamond difference, for the same mode."""
    w = fourier_si(2.0 * math.tan(theta / 2.0) / tau, c, mus, ws)
    return w - c * (1.0 - w) / (1.0 - c + 4.0 * math.sin(theta / 2.0) ** 2 / (3.0 * tau * tau))


def spectral_radius_dsa(c, mus=None, ws=None, samples=4000, lam_max=50.0):
    """The largest |fourier_dsa| on a grid of lam in [0, lam_max]. Returns (radius, lam at the maximum)."""
    best, at = 0.0, 0.0
    for i in range(samples + 1):
        lam = lam_max * i / samples
        v = abs(fourier_dsa(lam, c, mus, ws))
        if v > best:
            best, at = v, lam
    return best, at
