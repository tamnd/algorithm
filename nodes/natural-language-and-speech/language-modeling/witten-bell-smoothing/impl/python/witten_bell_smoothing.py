# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/witten-bell-smoothing/. The authors are listed in prov/FME53F.jsonl.

"""Interpolated Witten-Bell smoothing of an n-gram language model, exact in Fraction.

A corpus is a list of sentences, and a sentence is a list of str tokens.
Each sentence is padded with n - 1 copies of "<s>" on the left and one
"</s>" on the right. "</s>" is predicted and counted; "<s>" is never
predicted. The recursion is

    P(w | h) = (c(h w) + T(h) P(w | h')) / (c(h) + T(h))   if c(h) > 0
    P(w | h) = P(w | h')                                  if c(h) = 0

where h' is h without its first token, c(h) is the number of times h is
followed by a token, and T(h) = N_1+(h .) is the number of distinct tokens
that follow h. Below the unigrams sits the uniform distribution 1 / |V|.
"""

from collections import Counter
from fractions import Fraction
from typing import Iterable, Sequence

BOS, EOS, UNK = "<s>", "</s>", "<unk>"


def count_ngrams(corpus: Iterable[Sequence[str]], n: int):
    """Return (c, ch, t): the counts of the m-grams for m = 1 to n, the history counts and T(h)."""
    c: Counter = Counter()
    ch: Counter = Counter()
    t: Counter = Counter()
    for sent in corpus:
        toks = [BOS] * (n - 1) + list(sent) + [EOS]
        for i in range(n - 1, len(toks)):
            for m in range(1, n + 1):
                g = tuple(toks[i - m + 1 : i + 1])
                if c[g] == 0:
                    t[g[:-1]] += 1
                c[g] += 1
                ch[g[:-1]] += 1
    return c, ch, t


class WittenBellLM:
    """An interpolated Witten-Bell n-gram model over a closed vocabulary."""

    def __init__(self, corpus: Iterable[Sequence[str]], n: int, vocab: Iterable[str] | None = None):
        if n < 1:
            raise ValueError("the order n must be at least 1")
        corpus = [list(s) for s in corpus]
        self.n = n
        self.c, self.ch, self.t = count_ngrams(corpus, n)
        seen = {g[0] for g in self.c if len(g) == 1}
        self.vocab = set(seen) if vocab is None else set(vocab)
        self.vocab.add(EOS)
        if BOS in self.vocab:
            raise ValueError("<s> is never predicted, so it is not in the vocabulary")
        if not seen <= self.vocab:
            raise ValueError("the vocabulary must hold every training token; map the others to <unk>")

    def prob(self, w: str, history: Sequence[str] = ()) -> Fraction:
        """P(w | the last n - 1 tokens of history)."""
        if w not in self.vocab:
            raise KeyError(f"{w!r} is not in the vocabulary")
        h = tuple(history)[-(self.n - 1) :] if self.n > 1 else ()
        return self._prob(w, h)

    def _prob(self, w: str, h: tuple) -> Fraction:
        if h:  # @line L1
            lower = self._prob(w, h[1:])
        else:
            lower = Fraction(1, len(self.vocab))
        ch = self.ch[h]
        if ch == 0:  # @line L2
            return lower
        lam = Fraction(ch, ch + self.t[h])  # @line L3
        return lam * Fraction(self.c[h + (w,)], ch) + (1 - lam) * lower  # @line L4

    def distribution(self, history: Sequence[str] = ()) -> dict[str, Fraction]:
        """The full conditional distribution over the vocabulary."""
        return {w: self.prob(w, history) for w in sorted(self.vocab)}

    def sentence_prob(self, sent: Sequence[str]) -> Fraction:
        """The probability of a sentence, with its </s>."""
        toks = [BOS] * (self.n - 1) + list(sent) + [EOS]
        p = Fraction(1)
        for i in range(self.n - 1, len(toks)):
            p *= self.prob(toks[i], toks[:i])
        return p
