# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fw-cadis/. The authors are listed in prov/GNWTPH.jsonl.
"""FW-CADIS: forward-weighted CADIS for a mesh tally in a one-speed slab.

The slab 0 <= x <= L has M cells of width h = L / M, a total cross section
sigma_t and a scattering cross section sigma_s (cm^-1), isotropic scattering
and vacuum faces. The source q_i is isotropic and normalized to one source
particle. The tally is the flux integral T_j over each of B equal bins (a
bin holds M / B cells). The goal is about the same relative error in every
bin, so the method weights each bin by the inverse of its expected value:

1. Solve the forward problem by discrete ordinates: phi_i.
2. Set the adjoint source q+_i = 1 / T_j(i), the inverse of the
   deterministic estimate of the bin that holds cell i, and solve the adjoint
   problem (with isotropic scattering in a slab, a forward solve with the
   source q+ gives the scalar adjoint flux).
3. Do CADIS with this adjoint: bias the source to q_i phi+_i / R, give birth
   weights R / phi+_i, and set the weight window targets to R / phi+_i.
4. Run Monte Carlo with implicit capture and weight windows, and score the
   track length of each particle in each bin.

run_monte_carlo with params=None is the analog game.
"""

import math


def gauss_legendre(order):
    """Nodes and weights of the Gauss-Legendre rule on [-1, 1]; the weights sum to 2."""
    nodes, weights = [], []
    for i in range(order):
        x = math.cos(math.pi * (i + 0.75) / (order + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for m in range(2, order + 1):
                p0, p1 = p1, ((2 * m - 1) * x * p1 - (m - 1) * p0) / m
            dp = order * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        nodes.append(x)
        weights.append(2.0 / ((1.0 - x * x) * dp * dp))
    return nodes, weights


def sn_solve(q, length, sigma_t, sigma_s, order=16, tol=1e-12, max_iter=10000):
    """Scalar flux (cell averages) of the fixed source problem by S_N with diamond
    differences and source iteration. q_i is the isotropic source density in cell i."""
    m = len(q)
    h = length / m
    nodes, weights = gauss_legendre(order)
    phi = [0.0] * m
    for _ in range(max_iter):
        src = [sigma_s * p + s for p, s in zip(phi, q)]
        new = [0.0] * m
        for mu, wt in zip(nodes, weights):
            a = abs(mu) / h
            cells = range(m) if mu > 0 else range(m - 1, -1, -1)
            psi_in = 0.0
            for i in cells:
                psi_out = ((a - 0.5 * sigma_t) * psi_in + 0.5 * src[i]) / (a + 0.5 * sigma_t)
                new[i] += wt * 0.5 * (psi_in + psi_out)
                psi_in = psi_out
        change = max(abs(u - v) for u, v in zip(new, phi))
        phi = new
        if change <= tol * max(phi):
            break
    return phi


def bin_totals(phi, h, bins):
    per = len(phi) // bins
    return [sum(phi[j * per:(j + 1) * per]) * h for j in range(bins)]


def fw_cadis_parameters(q, length, sigma_t, sigma_s, bins, c_u=5.0, order=16):
    """The deterministic part of FW-CADIS. Returns the forward flux, the bin
    estimates, the adjoint flux and the CADIS source and window parameters."""
    m = len(q)
    h = length / m
    per = m // bins
    total = sum(q) * h
    q = [v / total for v in q]
    phi = sn_solve(q, length, sigma_t, sigma_s, order)  # @line L1
    t = bin_totals(phi, h, bins)
    q_adj = [1.0 / t[i // per] for i in range(m)]  # @line L2
    adj = sn_solve(q_adj, length, sigma_t, sigma_s, order)  # @line L3
    r = sum(qi * a * h for qi, a in zip(q, adj))  # @line L4
    pdf = [qi * a * h / r for qi, a in zip(q, adj)]
    target = [r / a for a in adj]  # @line L5
    lower = [2.0 * w / (c_u + 1.0) for w in target]
    upper = [c_u * w for w in lower]
    return {"forward": phi, "bin_estimate": t, "adjoint": adj, "response": r, "source_pdf": pdf, "birth_weight": target, "target": target, "lower": lower, "upper": upper, "q": q}


def apply_window(x, mu, w, cell, lower, upper, target, rng, stack, max_split=10):
    """Split above the window into ceil(w / w_U) copies, roulette below it with
    survival weight equal to the target. Returns the weight to continue with, or 0.0."""
    if w > upper[cell]:
        n = min(max_split, math.ceil(w / upper[cell]))
        w /= n
        for _ in range(n - 1):
            stack.append((x, mu, w, cell))
        return w
    if w < lower[cell]:
        if rng.random() < w / target[cell]:
            return target[cell]
        return 0.0
    return w


def run_monte_carlo(n, length, sigma_t, sigma_s, bins, rng, params=None, q=None):
    """Track-length estimates of the flux integral in each bin per source particle.

    With params from fw_cadis_parameters (or any CADIS parameters): biased source,
    implicit capture and weight windows. With params=None: the analog game with
    the source q. Returns (means, standard errors, number of flights)."""
    m = len(q) if params is None else len(params["target"])
    h = length / m
    per = m // bins
    if params is not None:
        pdf, wbirth = params["source_pdf"], params["birth_weight"]
        lower, upper, target = params["lower"], params["upper"], params["target"]
    else:
        total = sum(q) * h
        pdf, wbirth = [v * h / total for v in q], [1.0] * m
    cdf, acc = [], 0.0
    for v in pdf:
        acc += v
        cdf.append(acc)
    biased = params is not None
    c = sigma_s / sigma_t
    s1, s2 = [0.0] * bins, [0.0] * bins
    flights = 0
    for _ in range(n):  # @line L6
        u = rng.random() * acc
        cell = next((i for i, v in enumerate(cdf) if u < v), m - 1)
        stack = [((cell + rng.random()) * h, 2.0 * rng.random() - 1.0, wbirth[cell], cell)]
        score = [0.0] * bins
        while stack:
            x, mu, w, cell = stack.pop()
            while w > 0.0:
                flights += 1
                s = -math.log(1.0 - rng.random()) / sigma_t
                edge = (cell + 1) * h if mu > 0 else cell * h
                d = (edge - x) / mu if mu != 0.0 else math.inf
                if s >= d:
                    score[cell // per] += w * d  # @line L7
                    cell += 1 if mu > 0 else -1
                    x = edge
                    if cell < 0 or cell >= m:
                        break
                    if biased:
                        w = apply_window(x, mu, w, cell, lower, upper, target, rng, stack)
                    continue
                score[cell // per] += w * s
                x += mu * s
                if biased:
                    w *= c
                    mu = 2.0 * rng.random() - 1.0
                    w = apply_window(x, mu, w, cell, lower, upper, target, rng, stack)
                elif rng.random() >= c:
                    break
                else:
                    mu = 2.0 * rng.random() - 1.0
        for j in range(bins):  # @line L8
            s1[j] += score[j]
            s2[j] += score[j] * score[j]
    means = [v / n for v in s1]
    errors = [math.sqrt(max(b / n - a * a, 0.0) / (n - 1)) for a, b in zip(means, s2)]
    return means, errors, flights


def relative_errors(means, errors):
    return [e / mval if mval > 0 else math.inf for mval, e in zip(means, errors)]
