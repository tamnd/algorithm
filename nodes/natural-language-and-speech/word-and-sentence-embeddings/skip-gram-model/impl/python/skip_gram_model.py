# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skip-gram-model/. The authors are listed in prov/PV50G4.jsonl.

"""The skip-gram model of Mikolov, Chen, Corrado and Dean 2013, with a full softmax.

Each word w has an input vector v_w (a row of vin) and an output vector u_w
(a row of uout). The model gives P(c | w) = exp(u_c . v_w) / sum_j exp(u_j . v_w).
The training pairs come from a window of random radius R, uniform in 1 to C,
drawn again at each position. The code takes the corpus as a list of lists of
word ids. It is the full softmax form; negative sampling and hierarchical
softmax have their own pages.
"""

import math
import random
from typing import Sequence


def log_softmax(scores: Sequence[float]) -> list[float]:
    m = max(scores)
    z = m + math.log(sum(math.exp(s - m) for s in scores))
    return [s - z for s in scores]


def training_pairs(corpus: Sequence[Sequence[int]], c_max: int, rng: random.Random) -> list[tuple[int, int]]:
    """(center, context) pairs with a window radius R drawn uniformly from 1 to C."""
    pairs = []
    for sent in corpus:
        n = len(sent)
        for t in range(n):  # @line L1
            r = rng.randint(1, c_max)  # @line L2
            for j in range(max(0, t - r), min(n, t + r + 1)):  # @line L3
                if j != t:
                    pairs.append((sent[t], sent[j]))
    return pairs


def inclusion_probability(distance: int, c_max: int) -> float:
    """P(a context word at the given distance is used) = (C - distance + 1) / C."""
    return max(0, c_max - distance + 1) / c_max


def probabilities(vin, uout, w: int) -> list[float]:
    """P(. | w) over the whole vocabulary."""
    h = vin[w]
    return [math.exp(x) for x in log_softmax([sum(a * b for a, b in zip(u, h)) for u in uout])]


def pair_loss(vin, uout, w: int, c: int) -> float:
    """-log P(c | w)."""
    h = vin[w]  # @line L4
    scores = [sum(a * b for a, b in zip(u, h)) for u in uout]  # @line L5
    return -log_softmax(scores)[c]  # @line L6


def pair_gradient(vin, uout, w: int, c: int):
    """Gradient of pair_loss: (gradient of v_w, gradient of every u_j)."""
    p = probabilities(vin, uout, w)
    h = vin[w]
    d = len(h)
    gv = [0.0] * d
    gu = []
    for j, u in enumerate(uout):
        e = p[j] - (1.0 if j == c else 0.0)
        gu.append([e * a for a in h])
        for k in range(d):
            gv[k] += e * u[k]
    return gv, gu


def corpus_loss(vin, uout, pairs) -> float:
    return sum(pair_loss(vin, uout, w, c) for w, c in pairs)


def train(corpus, vocab_size: int, d: int = 8, c_max: int = 2, epochs: int = 5,
          lr: float = 0.1, seed: int = 0):
    """Plain SGD over the pairs. Returns (vin, uout)."""
    rng = random.Random(seed)
    vin = [[(rng.random() - 0.5) / d for _ in range(d)] for _ in range(vocab_size)]
    uout = [[0.0] * d for _ in range(vocab_size)]
    for _ in range(epochs):
        for w, c in training_pairs(corpus, c_max, rng):
            gv, gu = pair_gradient(vin, uout, w, c)
            for j in range(vocab_size):
                for k in range(d):
                    uout[j][k] -= lr * gu[j][k]
            for k in range(d):
                vin[w][k] -= lr * gv[k]
    return vin, uout


def free_score_optimum(pairs, vocab_size: int) -> dict[int, list[float]]:
    """With a free score for every (w, c), the loss is least at P(c | w) = n(w, c) / n(w)."""
    counts: dict[int, list[int]] = {}
    for w, c in pairs:
        counts.setdefault(w, [0] * vocab_size)[c] += 1
    return {w: [x / sum(row) for x in row] for w, row in counts.items()}
