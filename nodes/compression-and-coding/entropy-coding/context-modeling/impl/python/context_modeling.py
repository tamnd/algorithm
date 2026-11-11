# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/context-modeling/. The authors are listed in prov/SDA0PS.jsonl.

"""Order-k context models and their ideal code lengths.

An order-k model predicts each symbol from the k symbols before it: it keeps
one adaptive model (here the KT estimator, counts plus 1/2) per context. Near
the start, where fewer than k symbols precede, the context is the shorter
prefix. The code length is -lg of the product of the predictions; an
arithmetic coder comes within a few bits of it.

The empirical conditional entropy H_k of a sequence is the length per symbol
under the best order-k model chosen after seeing the whole sequence.
"""

import math
import random
from collections import defaultdict


def order_k_length(seq: list[int], k: int, sigma: int, delta: float = 0.5) -> float:
    """The adaptive code length in bits of seq under an order-k model with additive delta."""
    counts: dict[tuple, list[int]] = defaultdict(lambda: [0] * sigma)
    totals: dict[tuple, int] = defaultdict(int)
    bits = 0.0
    for i, s in enumerate(seq):
        ctx = tuple(seq[max(0, i - k):i])
        c = counts[ctx]
        bits -= math.log2((c[s] + delta) / (totals[ctx] + sigma * delta))
        c[s] += 1
        totals[ctx] += 1
    return bits


def empirical_conditional_entropy(seq: list[int], k: int) -> float:
    """H_k in bits per symbol: the sum over contexts of n_w H_0(the symbols after w), over n."""
    follow: dict[tuple, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for i, s in enumerate(seq):
        follow[tuple(seq[max(0, i - k):i])][s] += 1
    total = 0.0
    for nxt in follow.values():
        m = sum(nxt.values())
        total += sum(c * math.log2(m / c) for c in nxt.values())
    return total / len(seq) if seq else 0.0


def random_markov_source(order: int, sigma: int, seed: int, sharpness: float = 3.0) -> dict[tuple, list[float]]:
    """A random transition table: for each context of `order` symbols, a skewed distribution."""
    rng = random.Random(seed)
    table = {}
    for idx in range(sigma ** order):
        ctx = tuple((idx // sigma ** j) % sigma for j in range(order - 1, -1, -1))
        w = [rng.random() ** sharpness for _ in range(sigma)]
        z = sum(w)
        table[ctx] = [x / z for x in w]
    return table


def sample(table: dict[tuple, list[float]], order: int, sigma: int, n: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    seq = [rng.randrange(sigma) for _ in range(order)]
    while len(seq) < n:
        seq.append(rng.choices(range(sigma), weights=table[tuple(seq[len(seq) - order:])])[0])
    return seq[:n]


def entropy_rate(table: dict[tuple, list[float]], order: int, sigma: int, rounds: int = 2000) -> float:
    """The entropy rate of the Markov source: sum over contexts of pi(ctx) H(next | ctx)."""
    ctxs = list(table)
    pi = {c: 1 / len(ctxs) for c in ctxs}
    for _ in range(rounds):
        new = {c: 0.0 for c in ctxs}
        for c, p in pi.items():
            for s, q in enumerate(table[c]):
                new[c[1:] + (s,)] += p * q
        pi = new
    return sum(pi[c] * -sum(q * math.log2(q) for q in table[c] if q > 0) for c in ctxs)
