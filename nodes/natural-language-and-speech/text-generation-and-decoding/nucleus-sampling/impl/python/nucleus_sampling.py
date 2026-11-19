# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nucleus-sampling/. The authors are listed in prov/G371BC.jsonl.

"""Nucleus (top-p) sampling of the next token.

A next-token distribution is a list of probabilities, one per token of the
vocabulary, in the order of the vocabulary. The values can be floats or
Fractions; with Fractions the set and the distribution are exact, and the
threshold p should then be a Fraction too. The random source is any object
with a random() method that returns u in [0, 1), such as
random.Random(seed). The code takes the probabilities of the model as
given; it does not run or train a network.
"""

from typing import List, Sequence

from nlslog import softmax


def _check(p) -> None:
    if not 0 < p <= 1:
        raise ValueError("the threshold p must be in (0, 1]")


def nucleus_set(probs: Sequence, p) -> List[int]:
    """Return the nucleus: the shortest prefix of the sorted tokens with mass >= p.

    The tokens are sorted by probability from high to low, with the smaller
    index first on ties. If rounding keeps the running sum below p up to the
    end, every token of positive probability is kept.
    """
    _check(p)
    order = sorted(range(len(probs)), key=lambda i: (-probs[i], i))  # @line L1
    c = probs[order[0]] * 0  # @line L2
    for t, i in enumerate(order):  # @line L3
        c = c + probs[i]  # @line L4
        if c >= p:  # @line L5
            return order[: t + 1]
    return [i for i in order if probs[i] > 0]


def nucleus_distribution(probs: Sequence, p) -> list:
    """Return the renormalized distribution on the nucleus, 0 elsewhere."""
    kept = nucleus_set(probs, p)
    z = sum(probs[i] for i in kept)
    q = [probs[i] * 0 for i in range(len(probs))]
    for i in kept:
        q[i] = probs[i] / z
    return q


def nucleus_sample(probs: Sequence, p, rng) -> int:
    """Draw one token index from the nucleus distribution of probs.

    The draw is inverse transform sampling over the nucleus in sorted order,
    with r = u Z for the nucleus mass Z, so nothing is divided.
    """
    kept = nucleus_set(probs, p)  # @line L1
    z = sum(probs[i] for i in kept)  # @line L6
    r = rng.random() * z  # @line L7
    c = probs[kept[0]] * 0
    for i in kept:  # @line L8
        c = c + probs[i]  # @line L9
        if r < c:  # @line L10
            return i
    return [i for i in kept if probs[i] > 0][-1]  # @line L11


def nucleus_sample_logits(logits: Sequence[float], p, rng, temperature: float = 1.0) -> int:
    """Nucleus sampling from logits: softmax with the temperature, then nucleus_sample.

    Unlike top-k, the nucleus depends on the temperature: a lower T makes the
    distribution peaked and the nucleus smaller.
    """
    return nucleus_sample(softmax(logits, temperature), p, rng)
