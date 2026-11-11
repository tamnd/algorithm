# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-sampling-over-lattices/. The authors are listed in prov/MWVGYZ.jsonl.
"""Discrete Gaussian sampling over Z and over a lattice given by a basis.

Notation: rho_s(x) = exp(-pi |x - c|^2 / s^2) and D_{L,s,c}(v) is
rho_s(v - c) / rho_s(L - c) for v in the lattice L. The standard deviation
of the continuous Gaussian with parameter s is sigma = s / sqrt(2 pi).

* CDTSampler: a cumulative distribution table for D_{Z,s} (center 0),
  cut at tau * sigma, searched with a random number (inversion sampling).
* sample_z_rejection: D_{Z,s,c} for any real center c by rejection from the
  uniform distribution on the integers in [c - tau sigma, c + tau sigma].
* klein: the randomized nearest plane algorithm of Klein (2000) as used by
  Gentry, Peikert and Vaikuntanathan (2008): walk the Gram-Schmidt vectors
  from the last to the first and sample each coefficient from a 1D discrete
  Gaussian centered at the current projection.

For study only. The samplers use floating point and branch on secret
values, so they leak through timing; they must not be used in a real
signature scheme.
"""

import math
import random
from fractions import Fraction

TAU = 12


class CDTSampler:
    """Inversion sampling for D_{Z,s} with a table of cumulative probabilities."""

    def __init__(self, s, tau=TAU):
        # @line L1
        sigma = s / math.sqrt(2 * math.pi)
        self.bound = int(math.ceil(tau * sigma))
        self.values = list(range(-self.bound, self.bound + 1))
        weights = [math.exp(-math.pi * x * x / (s * s)) for x in self.values]
        total = sum(weights)
        self.pmf = [w / total for w in weights]
        acc, self.cdf = 0.0, []
        for p in self.pmf:
            acc += p
            self.cdf.append(acc)

    def sample(self, rng):
        # @line L2
        u = rng.random()
        lo, hi = 0, len(self.cdf) - 1
        while lo < hi:  # binary search: first index with cdf >= u
            mid = (lo + hi) // 2
            if self.cdf[mid] < u:
                lo = mid + 1
            else:
                hi = mid
        return self.values[lo]


def sample_z_rejection(s, c, rng, tau=TAU):
    """D_{Z,s,c} by rejection: uniform integer x near c, accept with prob rho_s(x - c)."""
    sigma = s / math.sqrt(2 * math.pi)
    lo, hi = math.floor(c - tau * sigma), math.ceil(c + tau * sigma)
    while True:
        # @line L3
        x = rng.randint(lo, hi)
        # @line L4
        if rng.random() < math.exp(-math.pi * (x - c) ** 2 / (s * s)):
            return x


def gram_schmidt(basis):
    """Gram-Schmidt vectors of the rows of basis, as floats (exact fractions inside)."""
    gs = []
    for b in basis:
        v = [Fraction(x) for x in b]
        for u in gs:
            mu = sum(x * y for x, y in zip(v, u)) / sum(y * y for y in u)
            v = [x - mu * y for x, y in zip(v, u)]
        gs.append(v)
    return [[float(x) for x in v] for v in gs]


def klein(basis, s, center, rng, gs=None):
    """One sample close to D_{L(B), s, center}; needs s >= max |b~_i| * eta for closeness."""
    # @line L5
    gs = gs or gram_schmidt(basis)
    # @line L6
    c = list(map(float, center))
    v = [0] * len(basis[0])
    # @line L7
    for i in range(len(basis) - 1, -1, -1):
        # @line L8
        g = gs[i]
        gg = sum(x * x for x in g)
        ci = sum(x * y for x, y in zip(c, g)) / gg
        si = s / math.sqrt(gg)
        # @line L9
        z = sample_z_rejection(si, ci, rng)
        # @line L10
        c = [x - z * y for x, y in zip(c, basis[i])]
        v = [x + z * y for x, y in zip(v, basis[i])]
    # @line L11
    return v


def smoothing_parameter_z_bound(eps):
    """Upper bound on eta_eps(Z): sqrt(ln(2 (1 + 1/eps)) / pi) (Micciancio and Regev 2007, Lemma 3.3 for n = 1)."""
    return math.sqrt(math.log(2 * (1 + 1 / eps)) / math.pi)


def demo(seed=0):
    rng = random.Random(seed)
    basis = [[2, 1], [1, 3]]
    return [klein(basis, 8.0, (0.5, 0.25), rng) for _ in range(5)]
