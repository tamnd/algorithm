# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-criticality/. The authors are listed in prov/1ER0M9.jsonl.
"""Monte Carlo criticality calculation: power iteration over fission generations.

The model is one-speed transport in a bare slab 0 <= x <= L with vacuum on
both faces (L = math.inf gives an infinite medium). The medium has a total
cross section sigma_t, a scattering cross section sigma_s and a production
cross section nu_sigma_f, all in cm^-1. Scattering and fission emission are
isotropic. A cycle follows N source neutrons with weight 1 by analog play:

- the flight s = -ln(xi) / sigma_t;
- at a collision, the collision estimate of k gains nu_sigma_f / sigma_t,
  and floor(nu_sigma_f / (sigma_t k) + xi) fission sites are banked, where
  k is the estimate of the previous cycle;
- the neutron scatters with probability sigma_s / sigma_t, else it is absorbed.

The next cycle starts from N sites drawn with replacement from the bank.
The first cycles are inactive: they only let the source converge. The
result is the mean of the cycle estimates of k over the active cycles.

sn_k_eigenvalue is an independent deterministic reference: discrete
ordinates with diamond differences and power iteration on the fission source.
"""

import math


def shannon_entropy(sites, length, bins):
    """H = -sum p_j log2 p_j of the sites over `bins` equal bins of [0, length]."""
    counts = [0] * bins
    for x in sites:
        j = min(bins - 1, max(0, int(x / length * bins)))
        counts[j] += 1
    n = len(sites)
    return -sum(c / n * math.log2(c / n) for c in counts if c > 0)


def run_cycle(source, length, sigma_t, sigma_s, nu_sigma_f, k_prev, rng):
    """Follow every source site once. Returns (bank of fission sites, collision estimate of k)."""
    has_faces = not math.isinf(length)
    p_scatter = sigma_s / sigma_t
    k_score = nu_sigma_f / sigma_t
    bank = []  # @line L3
    total = 0.0
    for x in source:  # @line L4
        mu = 2.0 * rng.random() - 1.0
        while True:  # @line L5
            x += mu * (-math.log(1.0 - rng.random()) / sigma_t)
            if has_faces and (x < 0.0 or x > length):
                break  # the neutron leaks
            total += k_score  # @line L6
            n_sites = int(k_score / k_prev + rng.random())  # @line L7
            bank.extend([x] * n_sites)
            if rng.random() >= p_scatter:  # @line L8
                break  # absorbed
            mu = 2.0 * rng.random() - 1.0
    return bank, total / len(source)


def monte_carlo_criticality(length, sigma_t, sigma_s, nu_sigma_f, n, inactive, active, rng, bins=20, k0=1.0, start=None):
    """Power iteration with n neutrons per cycle.

    The first source is uniform in the slab, or n sites at the point `start`.
    Returns a dict with the mean k over the active cycles, its naive standard
    error (which treats the cycles as independent), the k of every cycle and
    the Shannon entropy of the fission bank of every cycle."""
    if math.isinf(length):
        source = [0.0] * n  # every point of an infinite medium is the same
    elif start is not None:
        source = [start] * n
    else:
        source = [length * rng.random() for _ in range(n)]  # @line L1
    k = k0
    k_cycles, entropies = [], []
    for cycle in range(inactive + active):  # @line L2
        bank, k_c = run_cycle(source, length, sigma_t, sigma_s, nu_sigma_f, k, rng)
        if not bank:
            raise RuntimeError("the fission bank is empty; the system is far below critical or n is too small")
        k = k_c  # @line L9
        k_cycles.append(k_c)
        if not math.isinf(length):
            entropies.append(shannon_entropy(bank, length, bins))
        source = [bank[int(rng.random() * len(bank))] for _ in range(n)]  # @line L10
    act = k_cycles[inactive:]  # @line L11
    mean = sum(act) / len(act)  # @line L12
    var = sum((v - mean) ** 2 for v in act) / (len(act) - 1) if len(act) > 1 else 0.0
    return {"k": mean, "std_error": math.sqrt(var / len(act)), "k_cycles": k_cycles, "entropy": entropies}


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


def sn_sweep(q, h, sigma_t, nodes, weights):
    """Scalar flux of one transport sweep with isotropic source density q per cell and vacuum faces."""
    m = len(q)
    phi = [0.0] * m
    for mu, wt in zip(nodes, weights):
        a = abs(mu) / h
        order = range(m) if mu > 0 else range(m - 1, -1, -1)
        psi_in = 0.0
        for i in order:
            psi_out = ((a - 0.5 * sigma_t) * psi_in + 0.5 * q[i]) / (a + 0.5 * sigma_t)
            phi[i] += wt * 0.5 * (psi_in + psi_out)
            psi_in = psi_out
    return phi


def sn_k_eigenvalue(length, sigma_t, sigma_s, nu_sigma_f, cells=80, order=8, tol=1e-9, parity=1, max_iter=5000):
    """k of the slab by S_N with diamond differences.

    One iteration is one sweep with the source sigma_s phi + nu_sigma_f phi / k,
    which converges to the same fixed point as nested power and source iteration.
    parity=1 starts from a symmetric flux (the fundamental mode); parity=-1 starts
    from an antisymmetric one, which the iteration keeps, and gives the first
    odd mode, so that k_odd / k_even is the dominance ratio.
    Returns (k, phi)."""
    h = length / cells
    nodes, weights = gauss_legendre(order)
    xs = [(i + 0.5) * h for i in range(cells)]
    phi = [1.0 if parity == 1 else math.cos(math.pi * x / length) for x in xs]
    k = 1.0
    for _ in range(max_iter):
        fission = sum(phi) * nu_sigma_f
        q = [sigma_s * p + nu_sigma_f * p / k for p in phi]
        new = sn_sweep(q, h, sigma_t, nodes, weights)
        k_new = k * sum(new) * nu_sigma_f / fission if parity == 1 else k * sum(abs(v) for v in new) / sum(abs(v) for v in phi)
        if abs(k_new - k) < tol and max(abs(a - b) for a, b in zip(new, phi)) < tol * max(abs(v) for v in new):
            return k_new, new
        scale = max(abs(v) for v in new)
        phi = [v / scale for v in new]
        k = k_new
    return k, phi
