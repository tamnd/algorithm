# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kld-sampling/. The authors are listed in prov/ZKY15F.jsonl.

"""KLD-sampling: Monte Carlo localization with an adaptive number of particles.

The notation follows Fox (2003) and Thrun, Burgard and Fox (2005), Section 8.3.7.
A belief is a list of (pose, weight) pairs; the weights need not sum to 1.
The models are callables:

  sample_motion(rng, x, u)   one draw of x_t from p(x_t | u_t, x_{t-1} = x, m)
  likelihood(z, x)           p(z_t | x_t = x, m), a number >= 0
  bin_of(x)                  a hashable key of the grid bin that holds x

rng is a random.Random.
"""

import bisect
import math
from statistics import NormalDist


def kld_bound(k, epsilon, delta):
    """Return the number of samples of the KLD bound for k occupied bins.

    n = chi^2_{k-1, 1-delta} / (2 epsilon), with the quantile of the
    chi-square distribution approximated by Wilson and Hilferty:
    n = (k-1) / (2 epsilon) * (1 - 2/(9(k-1)) + sqrt(2/(9(k-1))) z_{1-delta})^3.
    For k <= 1 the bound is 0. The value is a real number; the sampler
    stops at the first integer count that reaches it.
    """
    if not (epsilon > 0.0 and 0.0 < delta < 1.0):
        raise ValueError("need epsilon > 0 and 0 < delta < 1")
    if k <= 1:
        return 0.0
    z = NormalDist().inv_cdf(1.0 - delta)
    a = 2.0 / (9.0 * (k - 1))
    return (k - 1) / (2.0 * epsilon) * (1.0 - a + math.sqrt(a) * z) ** 3


def kld_mcl(belief, u, z, sample_motion, likelihood, bin_of, rng, epsilon=0.05, delta=0.01, n_min=10, n_max=100000):
    """One step of KLD-sampling MCL.

    Draw particles from the previous weighted belief one at a time, move
    them, weight them and count the occupied bins, until the number of
    particles reaches both the KLD bound for the current number of bins
    and n_min, or reaches n_max. Return the new list of (pose, weight).
    """
    if not belief:
        raise ValueError("empty belief")
    if not 1 <= n_min <= n_max:
        raise ValueError("need 1 <= n_min <= n_max")
    cum, total = [], 0.0
    for _, w in belief:
        if w < 0.0:
            raise ValueError("negative weight")
        total += w
        cum.append(total)
    if total <= 0.0:
        raise ValueError("every particle has weight 0")
    new, bins = [], set()  # @line L1
    n, n_chi, k = 0, 0.0, 0
    while True:  # @line L2
        i = bisect.bisect_right(cum, rng.random() * total)  # @line L3
        i = min(i, len(belief) - 1)
        x = sample_motion(rng, belief[i][0], u)  # @line L4
        new.append((x, likelihood(z, x)))  # @line L5
        b = bin_of(x)
        if b not in bins:  # @line L6
            bins.add(b)  # @line L7
            k += 1
            if k > 1:
                n_chi = kld_bound(k, epsilon, delta)  # @line L8
        n += 1  # @line L9
        if (n >= n_chi and n >= n_min) or n >= n_max:  # @line L10
            return new  # @line L11
