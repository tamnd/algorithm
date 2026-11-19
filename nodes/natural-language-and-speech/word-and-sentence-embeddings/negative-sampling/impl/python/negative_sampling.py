# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/negative-sampling/. The authors are listed in prov/9W46SG.jsonl.

"""Negative sampling for the skip-gram model (Mikolov, Sutskever et al. 2013).

For an observed pair (w, c) and k noise words n_1 ... n_k drawn from
P_n(u) = count(u)^(3/4) / Z, the loss is

    -log sigma(u_c . v_w) - sum_i log sigma(-u_{n_i} . v_w).

v are the input (word) vectors and u the output (context) vectors. Like the
released word2vec code, the sampler drops a noise word equal to c. The
subsampling rule discards a token of relative frequency f with probability
max(0, 1 - sqrt(t / f)), the formula of the paper (the released code uses a
slightly different one).
"""

import bisect
import math
import random
from typing import Sequence


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def log_sigmoid(x: float) -> float:
    return -math.log1p(math.exp(-x)) if x >= 0 else x - math.log1p(math.exp(x))


def noise_distribution(counts: Sequence[int], power: float = 0.75) -> list[float]:
    z = sum(c ** power for c in counts)
    return [c ** power / z for c in counts]


class NoiseSampler:
    def __init__(self, counts: Sequence[int], power: float = 0.75):
        acc, self.cdf = 0.0, []
        for p in noise_distribution(counts, power):
            acc += p
            self.cdf.append(acc)

    def draw(self, rng: random.Random) -> int:
        return min(bisect.bisect_right(self.cdf, rng.random() * self.cdf[-1]), len(self.cdf) - 1)

    def negatives(self, rng: random.Random, k: int, context: int) -> list[int]:
        """k draws; a draw equal to the true context is skipped, as in word2vec."""
        out = []
        for _ in range(k):  # @line L1
            u = self.draw(rng)
            if u != context:
                out.append(u)
        return out


def discard_probability(freq: float, t: float = 1e-5) -> float:
    return max(0.0, 1.0 - math.sqrt(t / freq))


def pair_loss(vin, uout, w: int, c: int, negatives: Sequence[int]) -> float:
    h = vin[w]
    dot = lambda u: sum(a * b for a, b in zip(uout[u], h))  # noqa: E731
    return -log_sigmoid(dot(c)) - sum(log_sigmoid(-dot(u)) for u in negatives)


def pair_gradient(vin, uout, w: int, c: int, negatives: Sequence[int]):
    """(gradient of v_w, dict of gradients of the output rows)."""
    h = vin[w]
    d = len(h)
    gv = [0.0] * d
    gu: dict[int, list[float]] = {}
    for u, label in [(c, 1.0)] + [(u, 0.0) for u in negatives]:  # @line L2
        e = sigmoid(sum(a * b for a, b in zip(uout[u], h))) - label  # @line L3
        row = gu.setdefault(u, [0.0] * d)
        for k in range(d):
            gv[k] += e * uout[u][k]  # @line L4
            row[k] += e * h[k]  # @line L5
    return gv, gu


def sgd_step(vin, uout, w: int, c: int, negatives: Sequence[int], lr: float) -> None:
    gv, gu = pair_gradient(vin, uout, w, c, negatives)
    for u, g in gu.items():
        for k in range(len(g)):
            uout[u][k] -= lr * g[k]
    for k in range(len(gv)):
        vin[w][k] -= lr * gv[k]  # @line L6


def train(corpus, vocab_size: int, d: int = 8, window: int = 2, k: int = 5, epochs: int = 5,
          lr: float = 0.05, seed: int = 0):
    """Skip-gram with negative sampling on a corpus of word ids. Returns (vin, uout)."""
    rng = random.Random(seed)
    counts = [0] * vocab_size
    for sent in corpus:
        for w in sent:
            counts[w] += 1
    sampler = NoiseSampler([max(c, 1) for c in counts])
    vin = [[(rng.random() - 0.5) / d for _ in range(d)] for _ in range(vocab_size)]
    uout = [[0.0] * d for _ in range(vocab_size)]
    for _ in range(epochs):
        for sent in corpus:
            for t, w in enumerate(sent):
                for j in range(max(0, t - window), min(len(sent), t + window + 1)):
                    if j != t:
                        sgd_step(vin, uout, w, sent[j], sampler.negatives(rng, k, sent[j]), lr)
    return vin, uout


def expected_local_objective(x: float, n_wc: float, n_w: float, n_c: float, total: float, k: int) -> float:
    """n(w,c) log sigma(x) + k n(w) n(c) / total * log sigma(-x), the cell objective of Levy and Goldberg."""
    return n_wc * log_sigmoid(x) + k * n_w * n_c / total * log_sigmoid(-x)
