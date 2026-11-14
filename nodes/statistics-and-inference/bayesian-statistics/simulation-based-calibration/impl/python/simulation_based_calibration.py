# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simulation-based-calibration/. The authors are listed in prov/GB2WNE.jsonl.
"""Simulation-based calibration (Talts, Betancourt, Simpson, Vehtari and Gelman 2018).

Draw a parameter from the prior, simulate data from it, ask the sampler under test for L
posterior draws given those data, and record the rank of the true parameter among the
draws. If the sampler returns independent draws from the true posterior, the ranks are
uniform on {0, ..., L}. Ties are broken at random, which keeps the ranks uniform when the
quantity has atoms.
"""

import math
import random
from typing import Callable, Sequence


def rank_with_ties(f_true: float, f_draws: Sequence[float], rng: random.Random) -> int:
    """Number of draws below f_true, plus a uniform share of the draws equal to it."""
    below = sum(1 for v in f_draws if v < f_true)
    ties = sum(1 for v in f_draws if v == f_true)
    return below + (rng.randint(0, ties) if ties else 0)


def sbc(
    prior_draw: Callable,
    simulate: Callable,
    posterior_draws: Callable,
    f: Callable,
    n_reps: int,
    n_draws: int,
    rng: random.Random,
) -> list[int]:
    """Return the counts of the ranks 0..n_draws over n_reps replications.

    posterior_draws(y, n_draws, rng) is the sampler under test.
    """
    counts = [0] * (n_draws + 1)  # @line L1
    for _ in range(n_reps):  # @line L2
        theta = prior_draw(rng)  # @line L3
        y = simulate(theta, rng)  # @line L4
        draws = posterior_draws(y, n_draws, rng)  # @line L5
        r = rank_with_ties(f(theta), [f(t) for t in draws], rng)  # @line L6
        counts[r] += 1  # @line L7
    return counts  # @line L8


def bin_counts(counts: Sequence[int], n_bins: int) -> list[int]:
    """Merge the L + 1 rank counts into n_bins equal bins; n_bins must divide L + 1."""
    width, rem = divmod(len(counts), n_bins)
    if rem:
        raise ValueError("the number of bins must divide L + 1")
    return [sum(counts[b * width:(b + 1) * width]) for b in range(n_bins)]


def chi2_sf(x: float, k: int) -> float:
    """P(X >= x) for X chi-squared with k degrees of freedom, in closed form.

    Even k: exp(-x/2) sum_{j < k/2} (x/2)^j / j!.
    Odd k: erfc(sqrt(x/2)) + exp(-x/2) sum_{j < (k-1)/2} (x/2)^(j+1/2) / Gamma(j + 3/2).
    """
    if x <= 0:
        return 1.0
    h = x / 2
    if k % 2 == 0:
        term, total = 1.0, 1.0
        for j in range(1, k // 2):
            term *= h / j
            total += term
        return math.exp(-h) * total
    total = math.erfc(math.sqrt(h))
    term = math.sqrt(h) / math.gamma(1.5)
    for j in range((k - 1) // 2):
        total += math.exp(-h) * term
        term *= h / (j + 1.5)
    return total


def chi2_uniformity(counts: Sequence[int]) -> tuple[float, float]:
    """Pearson's chi-squared statistic against equal expected counts, and its p-value."""
    n, b = sum(counts), len(counts)
    e = n / b
    stat = math.fsum((c - e) ** 2 / e for c in counts)
    return stat, chi2_sf(stat, b - 1)


def thin(chain: Sequence, step: int, n: int) -> list:
    """Every step-th state of the chain, n of them (Talts et al., Algorithm 2)."""
    out = list(chain[step - 1::step])[:n]
    if len(out) < n:
        raise ValueError("chain too short for this thinning")
    return out


# A conjugate test model: theta ~ N(0, 1), y_1..y_m ~ N(theta, 1);
# the posterior is N(sum(y) / (m + 1), 1 / (m + 1)).

def normal_model(m: int):
    def prior_draw(rng):
        return rng.gauss(0.0, 1.0)

    def simulate(theta, rng):
        return [rng.gauss(theta, 1.0) for _ in range(m)]

    def posterior(y):
        return sum(y) / (m + 1), 1.0 / (m + 1)

    return prior_draw, simulate, posterior


def gaussian_sampler(posterior: Callable, scale: float = 1.0, shift: float = 0.0) -> Callable:
    """Independent draws from N(mean + shift * sd, (scale * sd)^2); scale 1 and shift 0 is correct."""
    def draws(y, n, rng):
        mu, v = posterior(y)
        sd = math.sqrt(v)
        return [rng.gauss(mu + shift * sd, scale * sd) for _ in range(n)]
    return draws


def ar1_sampler(posterior: Callable, rho: float, step: int = 1) -> Callable:
    """A Markov chain with the exact posterior as its stationary law, started at a
    posterior draw: x' = mu + rho (x - mu) + sqrt(1 - rho^2) sd e. Keeps every step-th state."""
    def draws(y, n, rng):
        mu, v = posterior(y)
        sd = math.sqrt(v)
        x = rng.gauss(mu, sd)
        c = math.sqrt(1 - rho * rho) * sd
        chain = []
        for _ in range(n * step):
            x = mu + rho * (x - mu) + c * rng.gauss(0.0, 1.0)
            chain.append(x)
        return thin(chain, step, n)
    return draws
