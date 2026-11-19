# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-beam-search/. The authors are listed in prov/G3YHYE.jsonl.

"""Stochastic beam search (Kool, van Hoof and Welling 2019).

A model is a function that takes the prefix y_1 ... y_t (a tuple of strings)
and returns a dict from each token to log p(w | prefix), in natural log. The
end token is the string "</s>". The code takes these log probabilities as
given; it does not run or train a network.

The search draws k distinct finished outputs. They are a sample without
replacement from the model: the first is a draw from p, the second a draw
from p restricted to the other outputs, and so on.
"""

import math
import random
from typing import Callable, Dict, List, Tuple

from nlslog import NEG_INF

EOS = "</s>"

Model = Callable[[Tuple[str, ...]], Dict[str, float]]
Node = Tuple[Tuple[str, ...], float, float]  # (tokens, log p, perturbed log p)


def gumbel(phi: float, rng: random.Random) -> float:
    """Return a sample of Gumbel(phi): phi - log(-log U) with U uniform on (0, 1)."""
    u = rng.random()
    while u == 0.0:
        u = rng.random()
    return phi - math.log(-math.log(u))


def log1mexp(a: float) -> float:
    """Return log(1 - exp(a)) for a <= 0, stably. log1mexp(0) is NEG_INF."""
    if a > 0:
        raise ValueError("log1mexp needs a <= 0")
    if a == 0:
        return NEG_INF
    if a > -math.log(2.0):
        return math.log(-math.expm1(a))
    return math.log1p(-math.exp(a))


def shift(target: float, z: float, g: float) -> float:
    """Return -log(exp(-target) - exp(-z) + exp(-g)), computed stably.

    The children of a node get Gumbels g with maximum z. The shifted values
    have maximum target, and the order among them does not change.
    """
    v = target - g + log1mexp(g - z)
    return target - max(0.0, v) - math.log1p(math.exp(-abs(v)))


def stochastic_beam_search(
    model: Model, max_len: int, k: int, rng: random.Random
) -> List[Tuple[List[str], float, float]]:
    """Return k distinct outputs as (tokens, log p, perturbed log p).

    The outputs come in decreasing order of the perturbed log probability,
    which is the order in which a sampling without replacement draws them.
    Fewer than k outputs are returned if the model has fewer outputs of at
    most max_len tokens. A node that is still open after max_len tokens is
    dropped, so the model should put "</s>" within max_len tokens.
    """
    if k < 1 or max_len < 1:
        raise ValueError("k and max_len must be at least 1")
    beam: List[Node] = [((), 0.0, 0.0)]  # @line L1
    for _ in range(max_len):  # @line L2
        if all(y and y[-1] == EOS for y, _, _ in beam):
            break
        cand: List[Node] = []  # @line L3
        for y, phi, g in beam:  # @line L4
            if y and y[-1] == EOS:
                cand.append((y, phi, g))
                continue
            children = [(y + (w,), phi + lp) for w, lp in model(y).items() if lp > NEG_INF]  # @line L5
            gs = [gumbel(cphi, rng) for _, cphi in children]  # @line L6
            z = max(gs)
            for (cy, cphi), cg in zip(children, gs):
                cand.append((cy, cphi, shift(g, z, cg)))  # @line L7
        order = sorted(range(len(cand)), key=lambda i: (-cand[i][2], i))  # @line L8
        beam = [cand[i] for i in order[:k]]  # @line L9
    return [(list(y), phi, g) for y, phi, g in beam if y and y[-1] == EOS]  # @line L10
