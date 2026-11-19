# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/typical-sampling/. The authors are listed in prov/T8X2CS.jsonl.

"""Locally typical sampling of the next token.

A next-token distribution is a list of probabilities, one per token of the
vocabulary, in the order of the vocabulary. The values can be floats or
Fractions; the entropy and the surprisals are floats in nats, while the
masses keep the type of the input, so a Fraction threshold is compared
exactly. The random source is any object with a random() method that
returns u in [0, 1), such as random.Random(seed). The code takes the
probabilities of the model as given; it does not run or train a network.
"""

import math
from typing import List, Sequence

from nlslog import softmax


def entropy(probs: Sequence) -> float:
    """Return the Shannon entropy H = -sum p log p in nats, with 0 log 0 = 0."""
    return -math.fsum(float(x) * math.log(x) for x in probs if x > 0)


def typical_order(probs: Sequence) -> List[int]:
    """Return the tokens of positive probability sorted by |-log p - H|.

    The distance of a token is how far its surprisal -log p is from the
    entropy H of the step. Ties go to the smaller index. Tokens of
    probability 0 have infinite surprisal and are left out.
    """
    h = entropy(probs)  # @line L1
    dist = {i: abs(-math.log(probs[i]) - h) for i in range(len(probs)) if probs[i] > 0}  # @line L2
    return sorted(dist, key=lambda i: (dist[i], i))  # @line L3


def typical_set(probs: Sequence, tau) -> List[int]:
    """Return the shortest prefix of typical_order whose mass is at least tau.

    If rounding keeps the running sum below tau up to the end, every token
    of positive probability is kept.
    """
    if not 0 < tau <= 1:
        raise ValueError("tau must be in (0, 1]")
    order = typical_order(probs)
    if not order:
        raise ValueError("no token has positive probability")
    c = probs[order[0]] * 0  # @line L4
    for t, i in enumerate(order):  # @line L5
        c = c + probs[i]
        if c >= tau:  # @line L6
            return order[: t + 1]
    return order


def typical_distribution(probs: Sequence, tau) -> list:
    """Return the renormalized distribution on the typical set, 0 elsewhere."""
    kept = typical_set(probs, tau)
    z = sum(probs[i] for i in kept)
    q = [probs[i] * 0 for i in range(len(probs))]
    for i in kept:
        q[i] = probs[i] / z
    return q


def typical_sample(probs: Sequence, tau, rng) -> int:
    """Draw one token index from the typical distribution of probs.

    Inverse transform sampling over the typical set in its order, with
    r = u Z for the mass Z of the set.
    """
    kept = typical_set(probs, tau)  # @line L1
    z = sum(probs[i] for i in kept)  # @line L7
    r = rng.random() * z
    c = probs[kept[0]] * 0
    for i in kept:  # @line L8
        c = c + probs[i]  # @line L9
        if r < c:  # @line L10
            return i
    return kept[-1]  # @line L11


def typical_sample_logits(logits: Sequence[float], tau, rng, temperature: float = 1.0) -> int:
    """Typical sampling from logits: softmax with the temperature, then typical_sample."""
    return typical_sample(softmax(logits, temperature), tau, rng)
