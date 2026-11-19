# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deleted-interpolation/. The authors are listed in prov/S7TPCG.jsonl.

"""Deleted interpolation of n-gram estimates, with weights fitted by EM.

A corpus is a list of sentences, and a sentence is a list of str tokens.
Each sentence is padded with n - 1 copies of "<s>" on the left and one
"</s>" on the right; "</s>" is predicted and counted, "<s>" is never
predicted. The model is a mixture

    P(w | h) = sum_j lambda_(b, j) P_j(w | h)

of the maximum likelihood estimates P_j of the orders m, m - 1, ..., 1 and
the uniform distribution 1 / |V|, where m is the longest order whose history
was seen in training. The weights depend on the bucket b = (m, the bit length
of c(h_m)) and are fitted by EM on held-out tokens. In the deleted version the
corpus is cut into parts, each part is held out in turn against the counts of
the others, and the final model uses the counts of the whole corpus.
"""

import math
from collections import Counter
from typing import Iterable, Sequence

BOS, EOS = "<s>", "</s>"
MAX_BUCKET = 8


def count_ngrams(corpus: Iterable[Sequence[str]], n: int):
    """Return (c, ch): the m-gram counts for m = 1 to n and the history counts."""
    c: Counter = Counter()
    ch: Counter = Counter()
    for sent in corpus:
        toks = [BOS] * (n - 1) + list(sent) + [EOS]
        for i in range(n - 1, len(toks)):
            for m in range(1, n + 1):
                g = tuple(toks[i - m + 1 : i + 1])
                c[g] += 1
                ch[g[:-1]] += 1
    return c, ch


def events(corpus: Iterable[Sequence[str]], n: int):
    """Yield (w, h) for every predicted token, with h the n - 1 tokens before it."""
    for sent in corpus:
        toks = [BOS] * (n - 1) + list(sent) + [EOS]
        for i in range(n - 1, len(toks)):
            yield toks[i], tuple(toks[i - n + 1 : i])


class Components:
    """The maximum likelihood estimates of every order, plus the uniform distribution."""

    def __init__(self, corpus: Iterable[Sequence[str]], n: int, vocab: set[str]):
        self.n, self.vocab = n, vocab
        self.c, self.ch = count_ngrams(corpus, n)
        if self.ch[()] == 0:
            raise ValueError("the training corpus has no tokens")

    def __call__(self, w: str, h: tuple) -> tuple[tuple, list[float]]:
        """Return the bucket and the component probabilities of w after h."""
        m = len(h)
        while self.ch[h[len(h) - m :]] == 0:
            m -= 1
        hm = h[len(h) - m :]
        probs = [self.c[hm[j:] + (w,)] / self.ch[hm[j:]] for j in range(m + 1)]
        probs.append(1 / len(self.vocab))
        return (m, min(self.ch[hm].bit_length(), MAX_BUCKET)), probs


def fit_weights(rows: dict[tuple, list[list[float]]], max_iter: int = 200, tol: float = 1e-12):
    """EM for the mixture weights of each bucket. Return (weights, log likelihood after each step)."""
    lam = {b: [1 / len(ps[0])] * len(ps[0]) for b, ps in rows.items()}  # @line L4
    trace = []
    for _ in range(max_iter):  # @line L5
        ll = 0.0
        new = {}
        for b, ps in rows.items():
            e = [0.0] * len(lam[b])
            for p in ps:  # @line L6
                z = sum(l * q for l, q in zip(lam[b], p))
                ll += math.log(z)
                for j, (l, q) in enumerate(zip(lam[b], p)):
                    e[j] += l * q / z
            new[b] = [x / len(ps) for x in e]  # @line L7
        trace.append(ll)
        lam = new
        if len(trace) > 1 and trace[-1] - trace[-2] < tol:  # @line L8
            break
    return lam, trace


def collect_rows(train: list[list[str]], held: list[list[str]], n: int, vocab: set[str], rows: dict):
    """Add the component probabilities of every held-out token, under the training counts."""
    comp = Components(train, n, vocab)  # @line L2
    for w, h in events(held, n):  # @line L3
        b, p = comp(w, h)
        rows.setdefault(b, []).append(p)


class InterpolatedLM:
    """The interpolated model with fixed weights and the counts of a corpus."""

    def __init__(self, corpus: Iterable[Sequence[str]], n: int, weights: dict, vocab: set[str]):
        self.n, self.weights, self.vocab = n, weights, vocab
        self.comp = Components(corpus, n, vocab)

    def prob(self, w: str, history: Sequence[str] = ()) -> float:
        """P(w | the last n - 1 tokens of history)."""
        if w not in self.vocab:
            raise KeyError(f"{w!r} is not in the vocabulary")
        h = ((BOS,) * (self.n - 1) + tuple(history))[len(history) :]
        b, p = self.comp(w, h)
        lam = self.weights.get(b) or [1 / len(p)] * len(p)  # a bucket never seen in held-out data
        return sum(l * q for l, q in zip(lam, p))  # @line L9

    def distribution(self, history: Sequence[str] = ()) -> dict[str, float]:
        """The full conditional distribution over the vocabulary."""
        return {w: self.prob(w, history) for w in sorted(self.vocab)}

    def log_likelihood(self, corpus: Iterable[Sequence[str]]) -> float:
        """The natural log of the probability of a corpus, with every </s>."""
        return sum(math.log(self.prob(w, h)) for w, h in events(corpus, self.n))


def make_vocab(corpus: Iterable[Sequence[str]], vocab: Iterable[str] | None) -> set[str]:
    seen = {w for s in corpus for w in s} | {EOS}
    v = set(seen) if vocab is None else set(vocab) | {EOS}
    if BOS in v:
        raise ValueError("<s> is never predicted, so it is not in the vocabulary")
    if not seen <= v:
        raise ValueError("the vocabulary must hold every token; map the others to <unk>")
    return v


def heldout_interpolation(train, held, n: int, vocab: Iterable[str] | None = None) -> InterpolatedLM:
    """Fit the weights on one held-out set; the model keeps the training counts only."""
    train, held = [list(s) for s in train], [list(s) for s in held]
    v = make_vocab(train + held, vocab)
    rows: dict = {}
    collect_rows(train, held, n, v, rows)
    weights, _ = fit_weights(rows)
    return InterpolatedLM(train, n, weights, v)


def deleted_interpolation(corpus, n: int, parts: int = 2, vocab: Iterable[str] | None = None) -> InterpolatedLM:
    """Hold out each of the parts in turn, fit one set of weights, and count the whole corpus."""
    if n < 1 or parts < 2:
        raise ValueError("need n >= 1 and at least two parts")
    corpus = [list(s) for s in corpus]
    if len(corpus) < parts:
        raise ValueError("need at least one sentence in each part")
    v = make_vocab(corpus, vocab)
    rows: dict = {}
    for j in range(parts):  # @line L1
        held = corpus[j::parts]
        train = [s for i, s in enumerate(corpus) if i % parts != j]
        collect_rows(train, held, n, v, rows)
    weights, _ = fit_weights(rows)
    return InterpolatedLM(corpus, n, weights, v)
