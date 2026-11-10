# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gumbel-max-trick/. The authors are listed in prov/J19481.jsonl.

"""The Gumbel-max trick and its top-k form.

With independent standard Gumbel variables G_i = -ln(-ln U_i), the index
argmax_i (phi_i + G_i) equals i with probability exp(phi_i) / sum_j exp(phi_j).
The k largest keys, in order, are a sample of k items without replacement in
the successive (Plackett-Luce) order. The keys order the items in the same
way as the Efraimidis-Spirakis keys U_i^(1 / w_i). Exact for exact reals.
"""

import math
import random
from typing import List, Sequence


def uniform_open(rng: random.Random) -> float:
    """A uniform real in (0, 1)."""
    u = rng.random()
    while u == 0.0:
        u = rng.random()
    return u


def gumbel_keys(log_weights: Sequence[float], us: Sequence[float]) -> List[float]:
    """Keys phi_i + G_i with G_i = -ln(-ln u_i)."""
    return [phi - math.log(-math.log(u)) for phi, u in zip(log_weights, us)]  # @line L1


def gumbel_max(log_weights: Sequence[float], rng: random.Random) -> int:
    """Index i with probability proportional to exp(log_weights[i])."""
    us = [uniform_open(rng) for _ in log_weights]  # @line L1
    keys = gumbel_keys(log_weights, us)  # @line L1
    return max(range(len(keys)), key=keys.__getitem__)  # @line L2


def gumbel_top_k(log_weights: Sequence[float], k: int, rng: random.Random) -> List[int]:
    """k distinct indices, drawn one by one with probability proportional to
    exp(log_weights) among the items not yet drawn."""
    if not 0 <= k <= len(log_weights):
        raise ValueError("need 0 <= k <= n")
    us = [uniform_open(rng) for _ in log_weights]
    keys = gumbel_keys(log_weights, us)
    order = sorted(range(len(keys)), key=keys.__getitem__, reverse=True)  # @line L3
    return order[:k]  # @line L3


def efraimidis_spirakis_top_k(weights: Sequence[float], us: Sequence[float], k: int) -> List[int]:
    """The k items with the largest keys u_i^(1 / w_i), compared in the log domain."""
    keys = [math.log(u) / w for u, w in zip(us, weights)]
    return sorted(range(len(keys)), key=keys.__getitem__, reverse=True)[:k]


def plackett_luce(weights: Sequence[float], seq: Sequence[int]) -> float:
    """The probability that successive sampling without replacement starts with seq."""
    rest = float(sum(weights))
    p = 1.0
    for i in seq:
        p *= weights[i] / rest
        rest -= weights[i]
    return p
