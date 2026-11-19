# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-hmm-tagging/. The authors are listed in prov/FKE3K3.jsonl.

"""Collapsed Gibbs sampling for a first-order Bayesian HMM tagger.

Model. Tags are 1..k; 0 is the sentence boundary, used before the first word
and after the last word. Each row a in 0..k has transition probabilities
tau_a ~ Dirichlet(alpha) over the k + 1 outcomes 0..k, and each tag t has
emission probabilities omega_t ~ Dirichlet(beta) over the W word types.
Integrating out tau and omega gives the marginal P(t, w) of a tagging, and
the conditional of one tag given all the others is a product of three count
ratios (line L5). Goldwater and Griffiths (2007) use the same construction
for a second-order model; this file keeps the first-order case.

The arithmetic is generic: with Fraction hyperparameters the conditional
and the marginal are exact rationals.
"""

import math
import random
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple


class Counts:
    """The sufficient statistics of a tagging: transition and emission counts."""

    def __init__(self, k: int, W: int):
        self.k, self.W = k, W
        self.trans = [[0] * (k + 1) for _ in range(k + 1)]  # n_{a,b}
        self.out = [0] * (k + 1)  # n_a = sum_b n_{a,b}
        self.emit = [[0] * W for _ in range(k + 1)]  # n_{t,w}
        self.ntag = [0] * (k + 1)  # n_t = sum_w n_{t,w}

    def add_trans(self, a: int, b: int, d: int) -> None:
        self.trans[a][b] += d
        self.out[a] += d

    def add_emit(self, t: int, w: int, d: int) -> None:
        self.emit[t][w] += d
        self.ntag[t] += d


def build_counts(words: Sequence[Sequence[int]], tags: Sequence[Sequence[int]], k: int, W: int) -> Counts:
    c = Counts(k, W)
    for ws, ts in zip(words, tags):
        prev = 0
        for w, t in zip(ws, ts):
            c.add_trans(prev, t, 1)
            c.add_emit(t, w, 1)
            prev = t
        c.add_trans(prev, 0, 1)
    return c


def conditional(c: Counts, a: int, w: int, b: int, alpha, beta) -> List:
    """Unnormalized P(t_i = t | all other tags, words) for t = 1..k.

    c must hold the counts without position i: without (a, t_i), (t_i, b)
    and (t_i, w). Entry 0 of the result is 0 (the boundary is not a tag).
    """
    K1 = c.k + 1
    p = [0 * alpha]
    for t in range(1, c.k + 1):
        e = (c.emit[t][w] + beta) / (c.ntag[t] + c.W * beta)  # @line L5
        t1 = (c.trans[a][t] + alpha) / (c.out[a] + K1 * alpha)
        same = 1 if a == t else 0
        t2 = (c.trans[t][b] + (1 if (a == t and t == b) else 0) + alpha) / (c.out[t] + same + K1 * alpha)
        p.append(e * t1 * t2)
    return p


def gibbs(words: Sequence[Sequence[int]], k: int, W: int, alpha: float, beta: float,
          sweeps: int, seed: int, init=None):
    """Run collapsed Gibbs sampling. Return (the final tags, the list of samples).

    Each sample is the tagging after one sweep, as a tuple of tuples. words
    holds word ids in 0..W-1. init is an optional starting tagging.
    """
    rng = random.Random(seed)
    if init is None:
        tags = [[rng.randint(1, k) for _ in ws] for ws in words]  # @line L1
    else:
        tags = [list(ts) for ts in init]
    c = build_counts(words, tags, k, W)
    samples = []
    for _ in range(sweeps):  # @line L2
        for s, ws in enumerate(words):
            ts = tags[s]
            n = len(ws)
            for i in range(n):  # @line L3
                a = ts[i - 1] if i > 0 else 0
                b = ts[i + 1] if i + 1 < n else 0
                old = ts[i]
                c.add_trans(a, old, -1)  # @line L4
                c.add_trans(old, b, -1)
                c.add_emit(old, ws[i], -1)
                p = conditional(c, a, ws[i], b, alpha, beta)
                r = rng.random() * sum(p)  # @line L6
                new = 1
                acc = p[1]
                while acc <= r and new < k:
                    new += 1
                    acc += p[new]
                ts[i] = new
                c.add_trans(a, new, 1)  # @line L7
                c.add_trans(new, b, 1)
                c.add_emit(new, ws[i], 1)
        samples.append(tuple(tuple(ts) for ts in tags))  # @line L8
    return tags, samples  # @line L9


def rising(x, n: int):
    """The rising factorial x (x + 1) ... (x + n - 1) = Gamma(x + n) / Gamma(x)."""
    r = 1
    for j in range(n):
        r = r * (x + j)
    return r


def marginal(words, tags, k: int, W: int, alpha, beta):
    """P(tags, words | alpha, beta) with tau and omega integrated out.

    Each Dirichlet-multinomial factor is prod_b rising(alpha, n_b) / rising(K alpha, n).
    With Fraction hyperparameters the result is exact.
    """
    c = build_counts(words, tags, k, W)
    p = Fraction(1) if isinstance(alpha, Fraction) else 1.0
    for a in range(k + 1):
        for b in range(k + 1):
            p *= rising(alpha, c.trans[a][b])
        p /= rising((k + 1) * alpha, c.out[a])
    for t in range(1, k + 1):
        for w in range(W):
            p *= rising(beta, c.emit[t][w])
        p /= rising(W * beta, c.ntag[t])
    return p


def all_taggings(words, k: int):
    """Every tagging of the corpus with tags 1..k (k^N of them)."""
    out = [[]]
    for ws in words:
        nxt = []
        for prefix in out:
            seqs = [[]]
            for _ in ws:
                seqs = [s + [t] for s in seqs for t in range(1, k + 1)]
            for s in seqs:
                nxt.append(prefix + [s])
        out = nxt
    return out


def exact_posterior(words, k: int, W: int, alpha, beta) -> Dict[Tuple, object]:
    """P(tags | words) for every tagging, by enumeration and normalization."""
    ps = {}
    for tg in all_taggings(words, k):
        ps[tuple(tuple(ts) for ts in tg)] = marginal(words, tg, k, W, alpha, beta)
    z = sum(ps.values())
    return {key: v / z for key, v in ps.items()}


def many_to_one_accuracy(gold: Sequence[Sequence[str]], pred: Sequence[Sequence[int]]) -> float:
    """Map each induced tag to the gold tag it most often meets, then count matches."""
    table: Dict[int, Dict[str, int]] = {}
    for gs, ps in zip(gold, pred):
        for g, p in zip(gs, ps):
            row = table.setdefault(p, {})
            row[g] = row.get(g, 0) + 1
    hit = sum(max(row.values()) for row in table.values())
    total = sum(len(gs) for gs in gold)
    return hit / total if total else 1.0


def log_marginal(words, tags, k: int, W: int, alpha: float, beta: float) -> float:
    """log P(tags, words) with lgamma, for corpora too large for exact rationals."""
    c = build_counts(words, tags, k, W)
    s = 0.0
    for a in range(k + 1):
        for b in range(k + 1):
            s += math.lgamma(c.trans[a][b] + alpha) - math.lgamma(alpha)
        s -= math.lgamma(c.out[a] + (k + 1) * alpha) - math.lgamma((k + 1) * alpha)
    for t in range(1, k + 1):
        for w in range(W):
            s += math.lgamma(c.emit[t][w] + beta) - math.lgamma(beta)
        s -= math.lgamma(c.ntag[t] + W * beta) - math.lgamma(W * beta)
    return s
