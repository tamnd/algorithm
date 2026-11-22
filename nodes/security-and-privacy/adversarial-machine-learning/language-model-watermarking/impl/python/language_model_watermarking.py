# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/language-model-watermarking/. The authors are listed in prov/635TD2.jsonl.

"""The green list watermark of Kirchenbauer et al. (2023) on a toy language model.

Before each token is drawn, a key and the previous token seed a pseudorandom split of
the vocabulary, and the logits of the green part get a bonus delta. The detector,
which knows the key, counts green tokens and computes the one-proportion z-score
z = (count - gamma T) / sqrt(T gamma (1 - gamma)).

The detector here scores each pair (previous token, token) only once, as the later
versions of the paper advise. Repeated pairs have the same green status, so counting
them again would break the independence that the false-positive bound needs.

The language model is a seeded table of bigram logits over a vocabulary of integers.
There is no real text and no real model here.
"""

import hashlib
import math
import random
from typing import Sequence

import mlkit

Model = list[list[float]]


def toy_bigram_model(rng: random.Random, vocab_size: int, spread: float) -> Model:
    """A seeded table of next-token logits: row u holds the logits after token u.

    The logits are drawn from N(0, spread^2). A large spread gives peaked, low-entropy
    rows; spread 0 gives the uniform distribution.
    """
    return [[rng.gauss(0.0, spread) for _ in range(vocab_size)] for _ in range(vocab_size)]


def green_size(vocab_size: int, gamma: float) -> int:
    """The number of green tokens, floor(gamma |V|), at least 1 and at most |V| - 1."""
    return min(max(int(gamma * vocab_size), 1), vocab_size - 1)


def green_list(key: bytes, prev: int, gamma: float, vocab_size: int) -> frozenset[int]:
    """The green tokens after the token prev, a pseudorandom set seeded by the key and prev."""
    digest = hashlib.sha256(key + b"|" + str(prev).encode()).digest()  # @line L7
    r = random.Random(int.from_bytes(digest[:16], "big"))  # @line L7
    return frozenset(r.sample(range(vocab_size), green_size(vocab_size, gamma)))  # @line L8


def draw(probs: Sequence[float], rng: random.Random) -> int:
    """A draw from a finite distribution by the inverse of its distribution function."""
    u = rng.random()
    acc = 0.0
    for v, p in enumerate(probs):
        acc += p
        if u < acc:
            return v
    return len(probs) - 1


def generate(model: Model, start: int, length: int, gamma: float, delta: float, key: bytes,
             rng: random.Random) -> list[int]:
    """length tokens after start, drawn with the green list bonus delta (delta = 0: no watermark)."""
    vocab_size = len(model)
    text = [start]
    for _ in range(length):  # @line L1
        z = list(model[text[-1]])  # @line L2
        green = green_list(key, text[-1], gamma, vocab_size)  # @line L3
        for v in green:  # @line L4
            z[v] += delta  # @line L4
        text.append(draw(mlkit.softmax(z), rng))  # @line L5
    return text[1:]  # @line L6


def z_score(count: int, scored: int, gamma_eff: float) -> float:
    """The one-proportion z-score of count green tokens among scored tokens."""
    if scored == 0:
        return 0.0
    return (count - gamma_eff * scored) / math.sqrt(scored * gamma_eff * (1.0 - gamma_eff))


def green_count(tokens: Sequence[int], gamma: float, key: bytes, vocab_size: int) -> tuple[int, int]:
    """(green, scored) over the distinct pairs (tokens[t-1], tokens[t]) for t >= 1."""
    count, scored, seen = 0, 0, set()  # @line L9
    for t in range(1, len(tokens)):  # @line L10
        pair = (tokens[t - 1], tokens[t])
        if pair in seen:  # @line L11
            continue  # @line L11
        seen.add(pair)  # @line L12
        scored += 1  # @line L12
        if tokens[t] in green_list(key, tokens[t - 1], gamma, vocab_size):  # @line L13
            count += 1  # @line L13
    return count, scored


def detect(tokens: Sequence[int], gamma: float, key: bytes, vocab_size: int,
           threshold: float) -> tuple[float, bool]:
    """(z, z > threshold) for the token list tokens[0], ..., tokens[T], where tokens[0] is the start.

    Under the null hypothesis (the text does not depend on the key, and the green lists
    behave like independent random sets), the false-positive rate is at most
    exp(-2 threshold^2 gamma' (1 - gamma')), by Hoeffding's inequality.
    """
    count, scored = green_count(tokens, gamma, key, vocab_size)
    gamma_eff = green_size(vocab_size, gamma) / vocab_size
    z = z_score(count, scored, gamma_eff)  # @line L14
    return z, z > threshold  # @line L15


def false_positive_bound(threshold: float, gamma_eff: float) -> float:
    """Hoeffding's bound exp(-2 threshold^2 gamma' (1 - gamma')) on P(z > threshold) under the null."""
    return math.exp(-2.0 * threshold * threshold * gamma_eff * (1.0 - gamma_eff))


def green_probability(probs: Sequence[float], green: frozenset[int], delta: float) -> tuple[float, float]:
    """(q, q') for one step: the green mass before and after the bonus delta.

    q' = e^delta q / (e^delta q + 1 - q), which is at least q.
    """
    q = math.fsum(probs[v] for v in green)
    a = math.exp(delta)
    return q, a * q / (a * q + 1.0 - q)


def spike_entropy(probs: Sequence[float], gamma: float, delta: float) -> float:
    """The spike entropy of Kirchenbauer et al.: the sum of p / (1 + z p) with z = (1 - gamma)(e^delta - 1) / (1 + (e^delta - 1) gamma)."""
    a = math.exp(delta)
    zc = (1.0 - gamma) * (a - 1.0) / (1.0 + (a - 1.0) * gamma)
    return math.fsum(p / (1.0 + zc * p) for p in probs)
