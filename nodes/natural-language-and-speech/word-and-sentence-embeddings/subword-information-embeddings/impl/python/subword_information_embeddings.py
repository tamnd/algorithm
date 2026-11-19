# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subword-information-embeddings/. The authors are listed in prov/3998JC.jsonl.

"""Subword information skip-gram (Bojanowski, Grave, Joulin and Mikolov 2017).

A word w is the set G_w of its own entry and the character n-grams of <w>,
for n from minn to maxn. Each n-gram is hashed with 32-bit FNV-1a into one of
`buckets` rows. Rows 0 to nwords - 1 of the input matrix Z belong to the
words of the vocabulary, the rows after them to the buckets. The vector of a
word is the sum of its rows (the paper; the released library divides the sum
by |G_w|). The score of a word and a context word c is s(w, c) = sum over g
in G_w of z_g . v_c, trained with negative sampling.

fnv1a_32 has the sign extension of the released library by default: each
byte is read as a signed char before the XOR, which changes the hash of the
bytes 128 to 255 (non-ASCII text). signed_bytes=False gives standard FNV-1a.
"""

import bisect
import math
import random
from typing import Sequence

FNV_OFFSET = 2166136261
FNV_PRIME = 16777619


def fnv1a_32(text: str, signed_bytes: bool = True) -> int:
    h = FNV_OFFSET
    for b in text.encode("utf-8"):
        if signed_bytes and b >= 128:
            b |= 0xFFFFFF00
        h = ((h ^ b) * FNV_PRIME) & 0xFFFFFFFF
    return h


def char_ngrams(word: str, minn: int = 3, maxn: int = 6) -> list[str]:
    """The character n-grams of <word>, by start position and then by length."""
    s = "<" + word + ">"
    out = []
    for i in range(len(s)):
        for n in range(minn, maxn + 1):
            if i + n > len(s):
                break
            out.append(s[i:i + n])
    return out


def subword_rows(word: str, vocab: dict[str, int], buckets: int, minn: int = 3, maxn: int = 6) -> list[int]:
    """Rows of Z for the word: its own row if it is in the vocabulary, then the n-gram buckets."""
    rows = [vocab[word]] if word in vocab else []
    rows += [len(vocab) + fnv1a_32(g) % buckets for g in char_ngrams(word, minn, maxn)]  # @line L1
    return rows


def word_vector(z: Sequence[Sequence[float]], rows: Sequence[int], mean: bool = False) -> list[float]:
    """Sum (or mean) of the rows of the word. Works for words outside the vocabulary."""
    d = len(z[0])
    h = [0.0] * d
    for r in rows:
        for k in range(d):
            h[k] += z[r][k]
    if mean and rows:
        h = [a / len(rows) for a in h]
    return h  # @line L9


def log_sigmoid(x: float) -> float:
    return -math.log1p(math.exp(-x)) if x >= 0 else x - math.log1p(math.exp(x))


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def pair_loss(z, v, rows, context: int, negatives: Sequence[int]) -> float:
    """-log sigma(s(w, c)) - sum over negatives n of log sigma(-s(w, n))."""
    h = word_vector(z, rows)
    score = lambda u: sum(a * b for a, b in zip(h, v[u]))  # noqa: E731
    return -log_sigmoid(score(context)) - sum(log_sigmoid(-score(u)) for u in negatives)


def pair_gradient(z, v, rows, context: int, negatives: Sequence[int]):
    """Gradients of pair_loss: a dict row -> vector for Z and a dict word -> vector for V."""
    h = word_vector(z, rows)
    d = len(h)
    gh = [0.0] * d
    gv: dict[int, list[float]] = {}
    for u, label in [(context, 1.0)] + [(u, 0.0) for u in negatives]:
        e = sigmoid(sum(a * b for a, b in zip(h, v[u]))) - label
        gv.setdefault(u, [0.0] * d)
        for k in range(d):
            gv[u][k] += e * h[k]
            gh[k] += e * v[u][k]
    gz: dict[int, list[float]] = {}
    for r in rows:
        gz.setdefault(r, [0.0] * d)
        for k in range(d):
            gz[r][k] += gh[k]
    return gz, gv


class NoiseSampler:
    """Draw words from the unigram distribution raised to the power 3/4."""

    def __init__(self, counts: Sequence[int], power: float = 0.75):
        acc, self.cdf = 0.0, []
        for c in counts:
            acc += c ** power
            self.cdf.append(acc)

    def draw(self, rng: random.Random) -> int:
        return bisect.bisect_right(self.cdf, rng.random() * self.cdf[-1])


def train(corpus: Sequence[Sequence[str]], d: int = 8, epochs: int = 5, window: int = 2,
          negatives: int = 3, lr: float = 0.05, buckets: int = 2000, minn: int = 3,
          maxn: int = 6, seed: int = 0):
    """Plain SGD with a fixed step. Returns (vocab, Z, V)."""
    rng = random.Random(seed)
    counts: dict[str, int] = {}
    for sent in corpus:
        for w in sent:
            counts[w] = counts.get(w, 0) + 1
    words = sorted(counts, key=lambda w: (-counts[w], w))
    vocab = {w: i for i, w in enumerate(words)}
    rows = {w: subword_rows(w, vocab, buckets, minn, maxn) for w in words}
    z = [[(rng.random() - 0.5) / d for _ in range(d)] for _ in range(len(words) + buckets)]  # @line L2
    v = [[0.0] * d for _ in words]
    noise = NoiseSampler([counts[w] for w in words])
    for _ in range(epochs):  # @line L3
        for sent in corpus:
            for t, w in enumerate(sent):
                for c in range(max(0, t - window), min(len(sent), t + window + 1)):
                    if c == t:
                        continue
                    ctx = vocab[sent[c]]
                    neg = [noise.draw(rng) for _ in range(negatives)]
                    neg = [u for u in neg if u != ctx]
                    h = word_vector(z, rows[w])
                    gh = [0.0] * d
                    for u, label in [(ctx, 1.0)] + [(u, 0.0) for u in neg]:  # @line L4
                        s = sum(a * b for a, b in zip(h, v[u]))  # @line L5
                        e = sigmoid(s) - label  # @line L6
                        for k in range(d):  # @line L7
                            gh[k] += e * v[u][k]
                            v[u][k] -= lr * e * h[k]
                    for r in rows[w]:  # @line L8
                        for k in range(d):
                            z[r][k] -= lr * gh[k]
    return vocab, z, v


def embed(word: str, vocab: dict[str, int], z, buckets: int = 2000, minn: int = 3, maxn: int = 6) -> list[float]:
    """The vector of any word, seen or not."""
    return word_vector(z, subword_rows(word, vocab, buckets, minn, maxn))
