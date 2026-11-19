# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/glove/. The authors are listed in prov/S7WPYE.jsonl.

"""GloVe (Pennington, Socher and Manning 2014) on a tiny corpus.

cooccurrence counts each pair of tokens at distance r <= window with the
weight 1 / r, in both directions, as the released cooccur tool does with its
symmetric option. The cost is

    J = sum over X_ij > 0 of f(X_ij) (w_i . wt_j + b_i + bt_j - log X_ij)^2

with f(x) = (x / x_max)^alpha for x < x_max and 1 otherwise. train runs
AdaGrad over the nonzero cells in random order. Each step uses the gradient of
one term of J without its factor 2 (the factor goes into the step size), and
the AdaGrad sums start at 1, as in the released code. The word vectors are
w_i + wt_i.
"""

import math
import random
from typing import Sequence

Cooc = dict[tuple[int, int], float]


def build_vocab(corpus: Sequence[Sequence[str]]) -> dict[str, int]:
    """Word to index, by falling count and then by the word."""
    counts: dict[str, int] = {}
    for sent in corpus:
        for w in sent:
            counts[w] = counts.get(w, 0) + 1
    order = sorted(counts, key=lambda w: (-counts[w], w))
    return {w: i for i, w in enumerate(order)}


def cooccurrence(corpus: Sequence[Sequence[str]], vocab: dict[str, int], window: int = 10) -> Cooc:
    """X[i, j] = sum of 1 / r over the pairs of tokens i and j at distance r <= window."""
    x: Cooc = {}
    for sent in corpus:
        ids = [vocab[w] for w in sent]
        for p, i in enumerate(ids):
            for r in range(1, window + 1):
                if p - r < 0:
                    break
                j = ids[p - r]
                x[(i, j)] = x.get((i, j), 0.0) + 1.0 / r
                x[(j, i)] = x.get((j, i), 0.0) + 1.0 / r
    return x


def weight(x: float, x_max: float = 100.0, alpha: float = 0.75) -> float:
    """f(x) = (x / x_max)^alpha below x_max, else 1; f(0) = 0."""
    return (x / x_max) ** alpha if x < x_max else 1.0


def init_params(n: int, d: int, seed: int = 0) -> dict[str, list]:
    rng = random.Random(seed)
    u = lambda: [(rng.random() - 0.5) / d for _ in range(d)]  # noqa: E731
    return {"w": [u() for _ in range(n)], "wt": [u() for _ in range(n)],
            "b": [0.0] * n, "bt": [0.0] * n}


def residual(p: dict[str, list], i: int, j: int, xij: float) -> float:
    return sum(a * c for a, c in zip(p["w"][i], p["wt"][j])) + p["b"][i] + p["bt"][j] - math.log(xij)


def cost(p: dict[str, list], x: Cooc, x_max: float = 100.0, alpha: float = 0.75) -> float:
    """The weighted least squares cost J over the nonzero cells."""
    return sum(weight(v, x_max, alpha) * residual(p, i, j, v) ** 2 for (i, j), v in x.items())


def gradient(p: dict[str, list], x: Cooc, x_max: float = 100.0, alpha: float = 0.75) -> dict[str, list]:
    """The exact gradient of J with respect to every parameter."""
    n, d = len(p["w"]), len(p["w"][0])
    g = {"w": [[0.0] * d for _ in range(n)], "wt": [[0.0] * d for _ in range(n)],
         "b": [0.0] * n, "bt": [0.0] * n}
    for (i, j), v in x.items():
        e = 2.0 * weight(v, x_max, alpha) * residual(p, i, j, v)
        for k in range(d):
            g["w"][i][k] += e * p["wt"][j][k]
            g["wt"][j][k] += e * p["w"][i][k]
        g["b"][i] += e
        g["bt"][j] += e
    return g


def train(x: Cooc, n: int, d: int, epochs: int = 50, lr: float = 0.05, seed: int = 0,
          x_max: float = 100.0, alpha: float = 0.75) -> tuple[dict[str, list], list[float]]:
    """AdaGrad over the nonzero cells. Returns the parameters and the cost after each epoch."""
    rng = random.Random(seed)
    p = init_params(n, d, seed)  # @line L2
    gs = {"w": [[1.0] * d for _ in range(n)], "wt": [[1.0] * d for _ in range(n)],
          "b": [1.0] * n, "bt": [1.0] * n}
    cells = sorted(x)
    history = []
    for _ in range(epochs):  # @line L3
        rng.shuffle(cells)
        for i, j in cells:  # @line L4
            v = x[(i, j)]
            e = residual(p, i, j, v)  # @line L5
            fe = weight(v, x_max, alpha) * e  # @line L6
            wi, wj = p["w"][i], p["wt"][j]
            for k in range(d):  # @line L7
                gi, gj = fe * wj[k], fe * wi[k]
                wi[k] -= lr * gi / math.sqrt(gs["w"][i][k])
                wj[k] -= lr * gj / math.sqrt(gs["wt"][j][k])
                gs["w"][i][k] += gi * gi
                gs["wt"][j][k] += gj * gj
            p["b"][i] -= lr * fe / math.sqrt(gs["b"][i])
            p["bt"][j] -= lr * fe / math.sqrt(gs["bt"][j])
            gs["b"][i] += fe * fe
            gs["bt"][j] += fe * fe
        history.append(cost(p, x, x_max, alpha))
    return p, history


def word_vectors(p: dict[str, list]) -> list[list[float]]:
    """The sum w_i + wt_i used as the final vector of word i."""
    return [[a + b for a, b in zip(r, s)] for r, s in zip(p["w"], p["wt"])]  # @line L8


def glove(corpus: Sequence[Sequence[str]], d: int, window: int = 10, epochs: int = 50,
          lr: float = 0.05, seed: int = 0, x_max: float = 100.0, alpha: float = 0.75):
    """The whole method: counts, AdaGrad, and the summed vectors, keyed by word."""
    vocab = build_vocab(corpus)
    x = cooccurrence(corpus, vocab, window)  # @line L1
    p, _ = train(x, len(vocab), d, epochs, lr, seed, x_max, alpha)
    vecs = word_vectors(p)
    return {w: vecs[i] for w, i in vocab.items()}
