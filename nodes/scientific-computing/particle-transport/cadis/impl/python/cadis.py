# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cadis/. The authors are listed in prov/VERVKH.jsonl.
"""CADIS: consistent adjoint driven importance sampling in a one-speed slab.

The slab 0 <= x <= L has M cells of width h = L / M, a total cross section
sigma_t and a scattering cross section sigma_s (cm^-1, the same in all
cells), isotropic scattering and vacuum faces. The source q_i (one value per
cell, isotropic, normalized to one source particle) and the detector
response sigma_d,i (one value per cell) define the response
R = integral of sigma_d phi dx.

CADIS has a deterministic step and a Monte Carlo step:

1. Solve the adjoint problem with the source sigma_d by discrete ordinates.
   With isotropic scattering in a slab, the adjoint angular flux is the
   forward angular flux of the same source with mu reversed, so the scalar
   adjoint flux phi+ comes from a forward solve with the source sigma_d.
2. Estimate R = sum_i q_i phi+_i h, bias the source to q_i phi+_i h / R, give
   a source particle born in cell i the weight R / phi+_i, and set the weight
   window target of cell i to the same value R / phi+_i, with the bounds
   w_L = 2 w / (c_u + 1) and w_U = c_u w_L.
3. Run Monte Carlo with implicit capture and the windows, checked at every
   collision and every cell boundary, and score sigma_d times the track length.

run_monte_carlo with windows=None is the analog game (analog absorption,
unit weights), the reference for the variance comparison.
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
    """Scalar flux phi_i (cell averages) of the fixed source problem by S_N, diamond
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


def cadis_parameters(q, sigma_d, length, sigma_t, sigma_s, c_u=5.0, order=16):
    """The deterministic part of CADIS.

    Returns a dict with the adjoint flux phi+, the estimate R of the response per
    source particle, the biased source probabilities, the birth weights, and the
    window targets and bounds of every cell."""
    m = len(q)
    h = length / m
    total = sum(q) * h
    q = [v / total for v in q]  # one source particle
    adj = sn_solve(sigma_d, length, sigma_t, sigma_s, order)  # @line L1
    r = sum(qi * a * h for qi, a in zip(q, adj))  # @line L2
    p_biased = [qi * a * h / r for qi, a in zip(q, adj)]  # @line L3
    target = [r / a for a in adj]  # @line L4
    lower = [2.0 * w / (c_u + 1.0) for w in target]  # @line L5
    upper = [c_u * w for w in lower]
    return {"adjoint": adj, "response": r, "source_pdf": p_biased, "birth_weight": target, "target": target, "lower": lower, "upper": upper, "q": q}


def apply_window(x, mu, w, cell, lower, upper, target, rng, stack, max_split=10):
    """The weight window game in one cell. Returns the weight to continue with, or 0.0.

    Above the window the particle splits into n = ceil(w / w_U) copies of weight
    w / n (at most max_split); the extra copies go on the stack. Below the
    window it plays Russian roulette with survival weight equal to the target."""
    if w > upper[cell]:  # @line L11
        n = min(max_split, math.ceil(w / upper[cell]))
        w /= n
        for _ in range(n - 1):
            stack.append((x, mu, w, cell))
        return w
    if w < lower[cell]:  # @line L12
        if rng.random() < w / target[cell]:
            return target[cell]
        return 0.0
    return w


def run_monte_carlo(n, length, sigma_t, sigma_s, sigma_d, rng, params=None, q=None, windows=True):
    """Monte Carlo estimate of R per source particle with its standard error.

    With params (from cadis_parameters) and windows=True: CADIS (biased source,
    implicit capture, weight windows). With params=None: the analog game with the
    source q. Returns (mean, standard error, number of flights)."""
    m = len(sigma_d)
    h = length / m
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
    biased = params is not None and windows
    c = sigma_s / sigma_t
    s1 = s2 = 0.0
    flights = 0
    for _ in range(n):  # @line L6
        u = rng.random() * acc
        cell = next((i for i, v in enumerate(cdf) if u < v), m - 1)  # @line L7
        stack = [((cell + rng.random()) * h, 2.0 * rng.random() - 1.0, wbirth[cell], cell)]
        score = 0.0
        while stack:  # @line L8
            x, mu, w, cell = stack.pop()
            while w > 0.0:
                flights += 1
                s = -math.log(1.0 - rng.random()) / sigma_t  # @line L9
                edge = (cell + 1) * h if mu > 0 else cell * h
                d = (edge - x) / mu if mu != 0.0 else math.inf
                if s >= d:  # the particle reaches the cell boundary first
                    score += w * sigma_d[cell] * d  # @line L10
                    cell += 1 if mu > 0 else -1
                    x = edge
                    if cell < 0 or cell >= m:
                        break  # leakage
                    if biased:
                        w = apply_window(x, mu, w, cell, lower, upper, target, rng, stack)
                    continue  # a new flight; the exponential law has no memory
                score += w * sigma_d[cell] * s
                x += mu * s
                if biased:
                    w *= c  # implicit capture
                    mu = 2.0 * rng.random() - 1.0  # every split copy gets this new direction
                    w = apply_window(x, mu, w, cell, lower, upper, target, rng, stack)
                elif rng.random() >= c:
                    break  # analog absorption
                else:
                    mu = 2.0 * rng.random() - 1.0
        s1 += score  # @line L13
        s2 += score * score
    mean = s1 / n
    var = max(s2 / n - mean * mean, 0.0) * n / (n - 1)
    return mean, math.sqrt(var / n), flights
