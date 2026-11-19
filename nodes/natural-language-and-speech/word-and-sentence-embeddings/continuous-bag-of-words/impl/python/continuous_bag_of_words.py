# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/continuous-bag-of-words/. The authors are listed in prov/GERBMV.jsonl.

"""The continuous bag-of-words model (Mikolov, Chen, Corrado and Dean 2013), full softmax.

The context of position t is the words at distance 1 to C on both sides. The
hidden vector h is the mean of their input vectors (rows of vin), and
P(w_t | context) = exp(u_{w_t} . h) / sum_j exp(u_j . h) with the output
vectors u (rows of uout). mean=False uses the sum instead of the mean.
The corpus is a list of lists of word ids.
"""

import math
import random
from typing import Sequence


def log_softmax(scores: Sequence[float]) -> list[float]:
    m = max(scores)
    z = m + math.log(sum(math.exp(s - m) for s in scores))
    return [s - z for s in scores]


def examples(corpus: Sequence[Sequence[int]], c_max: int) -> list[tuple[list[int], int]]:
    """(context ids, center id) for every position with a nonempty context."""
    out = []
    for sent in corpus:
        for t in range(len(sent)):
            ctx = [sent[j] for j in range(max(0, t - c_max), min(len(sent), t + c_max + 1)) if j != t]  # @line L1
            if ctx:
                out.append((ctx, sent[t]))
    return out


def hidden(vin, ctx: Sequence[int], mean: bool = True) -> list[float]:
    d = len(vin[0])
    h = [0.0] * d
    for j in ctx:
        for k in range(d):
            h[k] += vin[j][k]
    if mean:
        h = [x / len(ctx) for x in h]
    return h  # @line L2


def probabilities(vin, uout, ctx, mean: bool = True) -> list[float]:
    h = hidden(vin, ctx, mean)
    return [math.exp(x) for x in log_softmax([sum(a * b for a, b in zip(u, h)) for u in uout])]


def loss(vin, uout, ctx, center: int, mean: bool = True) -> float:
    """-log P(center | context)."""
    h = hidden(vin, ctx, mean)
    scores = [sum(a * b for a, b in zip(u, h)) for u in uout]  # @line L3
    return -log_softmax(scores)[center]  # @line L4


def gradient(vin, uout, ctx, center: int, mean: bool = True):
    """(gradient of each row of vin as a dict, gradient of every row of uout)."""
    h = hidden(vin, ctx, mean)
    d = len(h)
    p = [math.exp(x) for x in log_softmax([sum(a * b for a, b in zip(u, h)) for u in uout])]
    gh = [0.0] * d
    gu = []
    for j, u in enumerate(uout):
        e = p[j] - (1.0 if j == center else 0.0)
        gu.append([e * a for a in h])
        for k in range(d):
            gh[k] += e * u[k]
    scale = 1.0 / len(ctx) if mean else 1.0
    gv: dict[int, list[float]] = {}
    for j in ctx:  # a word that occurs twice in the context gets two shares
        row = gv.setdefault(j, [0.0] * d)
        for k in range(d):
            row[k] += scale * gh[k]
    return gv, gu


def train(corpus, vocab_size: int, d: int = 8, c_max: int = 2, epochs: int = 5,
          lr: float = 0.1, seed: int = 0, mean: bool = True):
    rng = random.Random(seed)
    vin = [[(rng.random() - 0.5) / d for _ in range(d)] for _ in range(vocab_size)]
    uout = [[0.0] * d for _ in range(vocab_size)]
    data = examples(corpus, c_max)
    for _ in range(epochs):
        rng.shuffle(data)
        for ctx, center in data:
            gv, gu = gradient(vin, uout, ctx, center, mean)
            for j in range(vocab_size):
                for k in range(d):
                    uout[j][k] -= lr * gu[j][k]
            for j, g in gv.items():
                for k in range(d):
                    vin[j][k] -= lr * g[k]
    return vin, uout
