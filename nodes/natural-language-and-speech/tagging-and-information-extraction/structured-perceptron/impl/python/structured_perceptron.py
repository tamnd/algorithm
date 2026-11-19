# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structured-perceptron/. The authors are listed in prov/KYD1XY.jsonl.

"""The structured perceptron of Collins (2002) for tagging, with averaging.

The feature vector Phi(x, y) of a sentence x with tags y counts first-order
features: ("T", y[i-1], y[i]) for each transition, with "<s>" before the
first tag and "</s>" after the last one, and ("E", y[i], x[i]) for each word.
The score of y is the dot product w . Phi(x, y). Decoding is Viterbi over
the tags.

Weights are kept in dicts; a missing key means 0. Updates add +1 or -1 to
weights, so the weights stay integers, and the averaged weights are exact
Fractions.
"""

from fractions import Fraction
from itertools import product
from typing import Dict, Hashable, List, Sequence, Tuple

BOS, EOS = "<s>", "</s>"

Weights = Dict[Hashable, int]


def phi(words: Sequence[str], tags: Sequence[str]) -> Dict[Tuple[str, str, str], int]:
    """The global feature vector: counts of transition and emission features."""
    f: Dict[Tuple[str, str, str], int] = {}
    prev = BOS
    for x, y in zip(words, tags):
        for key in (("T", prev, y), ("E", y, x)):
            f[key] = f.get(key, 0) + 1
        prev = y
    key = ("T", prev, EOS)
    f[key] = f.get(key, 0) + 1
    return f


def score(w, words: Sequence[str], tags: Sequence[str]):
    return sum(w.get(k, 0) * v for k, v in phi(words, tags).items())


def viterbi(words: Sequence[str], tagset: Sequence[str], w):
    """Return (tags, score) of a highest-scoring tag sequence. Ties go to the first tag in tagset order."""
    n = len(words)
    if n == 0:
        raise ValueError("empty sentence")
    delta = {t: w.get(("T", BOS, t), 0) + w.get(("E", t, words[0]), 0) for t in tagset}
    back: List[Dict[str, str]] = []
    for i in range(1, n):
        new, bp = {}, {}
        for t in tagset:
            e = w.get(("E", t, words[i]), 0)
            best_g = None
            for g in tagset:
                v = delta[g] + w.get(("T", g, t), 0)
                if best_g is None or v > new[t]:
                    new[t], best_g = v, g
            new[t] += e
            bp[t] = best_g
        delta = new
        back.append(bp)
    last = None
    for t in tagset:
        v = delta[t] + w.get(("T", t, EOS), 0)
        if last is None or v > best:
            last, best = t, v
    out = [last]
    for bp in reversed(back):
        out.append(bp[out[-1]])
    out.reverse()
    return out, best


def brute_force(words: Sequence[str], tagset: Sequence[str], w):
    """The best score over all k^n tag sequences (for tests)."""
    return max(score(w, words, ys) for ys in product(tagset, repeat=len(words)))


def train(data, tagset: Sequence[str], epochs: int):
    """Run the perceptron. Return (w, averaged w, number of mistakes per epoch).

    The average is over the weights after each of the epochs * len(data)
    examples, as in Collins (2002), Section 2.5. It is kept lazily: u adds
    c * d for each update d made when c examples were seen before, and the
    average is w - u / c at the end.
    """
    w: Weights = {}  # @line L1
    u: Weights = {}
    c = 0
    mistakes = []
    for _ in range(epochs):  # @line L2
        m = 0
        for words, gold in data:  # @line L3
            z, _ = viterbi(words, tagset, w)  # @line L4
            if list(z) != list(gold):  # @line L5
                m += 1
                d = dict(phi(words, gold))  # @line L6
                for k, v in phi(words, z).items():
                    d[k] = d.get(k, 0) - v
                for k, v in d.items():  # @line L7
                    if v:
                        w[k] = w.get(k, 0) + v
                        u[k] = u.get(k, 0) + c * v
            c += 1  # @line L8
        mistakes.append(m)
    avg = {k: Fraction(w.get(k, 0)) - Fraction(u.get(k, 0), c) for k in set(w) | set(u)} if c else {}
    return w, avg, mistakes  # @line L9


def train_naive_average(data, tagset: Sequence[str], epochs: int):
    """The same run, with the average computed by summing the weights after every example (for tests)."""
    w: Weights = {}
    total: Dict[Hashable, int] = {}
    c = 0
    for _ in range(epochs):
        for words, gold in data:
            z, _ = viterbi(words, tagset, w)
            if list(z) != list(gold):
                for k, v in phi(words, gold).items():
                    w[k] = w.get(k, 0) + v
                for k, v in phi(words, z).items():
                    w[k] = w.get(k, 0) - v
            c += 1
            for k, v in w.items():
                total[k] = total.get(k, 0) + v
    return {k: Fraction(v, c) for k, v in total.items()}
