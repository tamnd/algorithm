# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truncated-channel-inversion/. The authors are listed in prov/PEF750.jsonl.

"""Truncated channel inversion over a fading channel.

gamma is the SNR the receiver would see at the average power. Truncated
channel inversion sends nothing when gamma < gamma0 and otherwise sends the
power P(gamma) / Pbar = sigma / gamma, so the received SNR is the constant
sigma. The average power constraint gives sigma = 1 / E[1/gamma; gamma >= gamma0],
and the rate is log2(1 + sigma) * Pr(gamma >= gamma0) bits per channel use.

truncated_inversion() works on a discrete distribution of states (for
example a quantized channel or an empirical sample) and finds the best cutoff
among the states in O(K log K). The Rayleigh functions use the closed form
sigma = gbar / E1(gamma0 / gbar) and Pr = exp(-gamma0 / gbar).
"""

import math

EULER_GAMMA = 0.5772156649015329


def truncated_inversion(gammas, probs=None):
    """Best cutoff for states gammas[k] > 0 with probabilities probs[k].

    Returns (gamma0, sigma, rate, powers), where powers[k] is P / Pbar in state k.
    probs defaults to equal weights (an empirical sample).
    """
    if not gammas or any(not g > 0 for g in gammas):
        raise ValueError("need at least one state and positive SNR values")
    if probs is None:
        probs = [1 / len(gammas)] * len(gammas)
    if len(probs) != len(gammas) or any(p < 0 for p in probs) or abs(sum(probs) - 1) > 1e-9:
        raise ValueError("probs must be a probability vector of the same length")
    merged = {}
    for g, p in zip(gammas, probs):
        merged[g] = merged.get(g, 0.0) + p
    states = sorted(((g, p) for g, p in merged.items() if p > 0), reverse=True)  # @line L1
    s, q, best = 0.0, 0.0, (0.0, None, None)  # @line L2
    for g, p in states:  # @line L3
        s, q = s + p / g, q + p  # @line L4
        rate = q * math.log2(1 + 1 / s)  # @line L5
        if rate > best[0]:  # @line L6
            best = (rate, g, 1 / s)
    rate, gamma0, sigma = best  # @line L7
    powers = [sigma / g if g >= gamma0 else 0.0 for g in gammas]
    return gamma0, sigma, rate, powers  # @line L8


def zero_outage_rate(gammas, probs=None):
    """Full channel inversion: log2(1 + 1 / E[1/gamma])."""
    if probs is None:
        probs = [1 / len(gammas)] * len(gammas)
    return math.log2(1 + 1 / sum(p / g for g, p in zip(gammas, probs)))


def expint_e1(x: float) -> float:
    """The exponential integral E1(x) for x > 0."""
    if not x > 0:
        raise ValueError("E1 needs x > 0")
    if x <= 1:
        total, term, k = -EULER_GAMMA - math.log(x), 1.0, 1
        while True:
            term *= -x / k
            add = -term / k
            total += add
            if abs(add) < 1e-17 * abs(total):
                return total
            k += 1
    # Continued fraction (modified Lentz), valid for x > 0, fast for x >= 1.
    tiny = 1e-300
    b = x + 1
    c = 1 / tiny
    d = 1 / b
    h = d
    for i in range(1, 1000):
        a = -i * i
        b += 2
        d = 1 / (a * d + b)
        c = b + a / c
        delta = c * d
        h *= delta
        if abs(delta - 1) < 1e-16:
            break
    return h * math.exp(-x)


def rayleigh_rate(gamma0: float, gbar: float) -> float:
    """Rate of truncated inversion with cutoff gamma0 on Rayleigh fading with mean SNR gbar."""
    if not gamma0 > 0 or not gbar > 0:
        raise ValueError("need gamma0 > 0 and gbar > 0")
    x = gamma0 / gbar
    sigma = gbar / expint_e1(x)
    return math.log2(1 + sigma) * math.exp(-x)


def rayleigh_best_cutoff(gbar: float, iters: int = 200) -> tuple[float, float]:
    """(gamma0, rate) of the best cutoff on Rayleigh fading: a log grid, then golden section."""
    grid = [gbar * 10 ** (e / 20) for e in range(-120, 41)]
    k = max(range(len(grid)), key=lambda j: rayleigh_rate(grid[j], gbar))
    lo = math.log(grid[max(k - 1, 0)])
    hi = math.log(grid[min(k + 1, len(grid) - 1)])
    r = (math.sqrt(5) - 1) / 2
    for _ in range(iters):
        a, b = hi - r * (hi - lo), lo + r * (hi - lo)
        if rayleigh_rate(math.exp(a), gbar) < rayleigh_rate(math.exp(b), gbar):
            lo = a
        else:
            hi = b
    g0 = math.exp((lo + hi) / 2)
    return g0, rayleigh_rate(g0, gbar)
