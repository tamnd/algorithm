# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/top-k-sampling/. The authors are listed in prov/CNGCHZ.jsonl.

"""Top-k sampling of the next token.

A next-token distribution is a list p of probabilities, one per token of the
vocabulary, in the order of the vocabulary. The values can be floats or
Fractions; with Fractions the distribution functions are exact. The random
source is any object with a random() method that returns u in [0, 1), such
as random.Random(seed). The code takes the probabilities of the model as
given; it does not run or train a network.
"""

from typing import List, Sequence

from nlslog import softmax


def top_k_set(probs: Sequence, k: int) -> List[int]:
    """Return the indices of the min(k, |V|) most probable tokens.

    The list is sorted by probability from high to low. On ties the smaller
    index comes first, so the result does not depend on the sort algorithm.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    order = sorted(range(len(probs)), key=lambda i: (-probs[i], i))  # @line L1
    return order[: min(k, len(probs))]  # @line L2


def top_k_distribution(probs: Sequence, k: int) -> list:
    """Return the truncated and renormalized distribution q of top-k sampling.

    q[i] = p[i] / Z for the kept tokens, where Z is their total mass, and 0
    for the others. Raise ValueError if the kept mass is 0.
    """
    kept = top_k_set(probs, k)
    z = sum(probs[i] for i in kept)
    if not z > 0:
        raise ValueError("the kept tokens have no mass")
    q = [probs[i] * 0 for i in range(len(probs))]
    for i in kept:
        q[i] = probs[i] / z
    return q


def top_k_sample(probs: Sequence, k: int, rng) -> int:
    """Draw one token index from the top-k distribution of probs.

    The draw is inverse transform sampling over the kept tokens in sorted
    order: r = u Z, and the first index whose running sum exceeds r wins.
    Nothing is divided, and a token of probability 0 is never returned.
    """
    kept = top_k_set(probs, k)  # @line L1
    z = sum(probs[i] for i in kept)  # @line L3
    if not z > 0:
        raise ValueError("the kept tokens have no mass")
    r = rng.random() * z  # @line L4
    c = probs[kept[0]] * 0  # @line L5
    for i in kept:  # @line L6
        c = c + probs[i]  # @line L7
        if r < c:  # @line L8
            return i
    return [i for i in kept if probs[i] > 0][-1]  # @line L9


def top_k_sample_logits(logits: Sequence[float], k: int, rng, temperature: float = 1.0) -> int:
    """Top-k sampling from logits: softmax with the temperature, then top_k_sample.

    The kept set is the same for every temperature, because dividing by a
    positive T keeps the order of the logits.
    """
    return top_k_sample(softmax(logits, temperature), k, rng)
