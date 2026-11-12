# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lt-codes/. The authors are listed in prov/1YD9K5.jsonl.
"""LT codes (Luby 2002): robust soliton degrees, XOR encoding and peeling decoding.

Source symbols are Python ints (a packet seen as a big integer); an encoded symbol is the
XOR of d distinct source symbols, with d drawn from a degree distribution. The encoder and
decoder share the random choices through a seed per encoded symbol, so a packet only needs
to carry its seed (its ID) and its value.
"""

import bisect
import math
import random
from typing import List, Optional, Sequence, Tuple


def ideal_soliton(k: int) -> List[float]:
    """rho[d] for d = 0..k: rho(1) = 1/k, rho(d) = 1/(d(d-1)) for d = 2..k, rho[0] = 0."""
    rho = [0.0] * (k + 1)
    rho[1] = 1.0 / k
    for d in range(2, k + 1):
        rho[d] = 1.0 / (d * (d - 1))
    return rho


def robust_soliton(k: int, c: float, delta: float) -> Tuple[List[float], float, float]:
    """Luby's robust soliton mu[d], d = 0..k, with R = c ln(k/delta) sqrt(k).

    tau(d) = R/(d k) for d = 1..k/R - 1, tau(k/R) = R ln(R/delta)/k, tau(d) = 0 otherwise,
    beta = sum (rho + tau), mu = (rho + tau)/beta. Luby takes k/R to be an integer; here the
    spike is at d = floor(k/R). Returns (mu, R, beta)."""
    r = c * math.log(k / delta) * math.sqrt(k)
    spike = int(k / r)
    if not 1 <= spike <= k:
        raise ValueError("need 1 <= k/R <= k")
    rho = ideal_soliton(k)
    tau = [0.0] * (k + 1)
    for d in range(1, spike):
        tau[d] = r / (d * k)
    tau[spike] = r * math.log(r / delta) / k
    beta = sum(rho) + sum(tau)
    mu = [(rho[d] + tau[d]) / beta for d in range(k + 1)]
    return mu, r, beta


class Sampler:
    """Draw degrees from a distribution p[0..k] by inverse CDF and binary search."""

    def __init__(self, p: Sequence[float]):
        self.cdf, acc = [], 0.0
        for v in p:
            acc += v
            self.cdf.append(acc)

    def degree(self, rng: random.Random) -> int:
        u = rng.random() * self.cdf[-1]
        return min(bisect.bisect_right(self.cdf, u), len(self.cdf) - 1)


def neighbors(seed: int, k: int, sampler: Sampler) -> List[int]:
    """The source symbols of the encoded symbol with this seed (shared by both sides)."""
    rng = random.Random(seed)
    d = max(1, sampler.degree(rng))
    return rng.sample(range(k), d)


def encode(source: Sequence[int], seeds: Sequence[int], sampler: Sampler) -> List[int]:
    out = []
    for s in seeds:
        v = 0
        for i in neighbors(s, len(source), sampler):
            v ^= source[i]
        out.append(v)
    return out


def decode(k: int, seeds: Sequence[int], values: Sequence[int],
           sampler: Sampler) -> List[Optional[int]]:
    """Peeling decoder: release encoded symbols of degree one, one source symbol at a time.

    The queue of degree-one encoded symbols is the ripple. Returns the source symbols, with
    None for those that are not recovered."""
    sets = [set(neighbors(s, k, sampler)) for s in seeds]
    val = list(values)
    adj: List[List[int]] = [[] for _ in range(k)]
    for j, nb in enumerate(sets):
        for i in nb:
            adj[i].append(j)
    out: List[Optional[int]] = [None] * k
    ripple = [j for j, nb in enumerate(sets) if len(nb) == 1]
    while ripple:
        j = ripple.pop()
        if len(sets[j]) != 1:
            continue
        i = next(iter(sets[j]))
        out[i] = val[j]
        for j2 in adj[i]:
            sets[j2].discard(i)
            val[j2] ^= out[i]
            if len(sets[j2]) == 1:
                ripple.append(j2)
    return out


def success_rate(k: int, overhead: float, sampler: Sampler, trials: int, seed: int) -> float:
    """Fraction of trials in which ceil(k (1 + overhead)) random encoded symbols decode."""
    rng = random.Random(seed)
    n = math.ceil(k * (1 + overhead))
    wins = 0
    for _ in range(trials):
        source = [rng.getrandbits(16) for _ in range(k)]
        seeds = [rng.getrandbits(48) for _ in range(n)]
        got = decode(k, seeds, encode(source, seeds, sampler), sampler)
        wins += got == source
    return wins / trials
