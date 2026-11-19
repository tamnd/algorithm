# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kneser-ney-smoothing/. The authors are listed in prov/M3W0NG.jsonl.

"""Interpolated Kneser-Ney smoothing of an n-gram language model, exact in Fraction.

A corpus is a list of sentences, and a sentence is a list of str tokens.
Each sentence is padded with n - 1 copies of "<s>" on the left and one
"</s>" on the right. "</s>" is predicted and counted; "<s>" is never
predicted.

Level n uses the raw counts a_n(g) = c(g). Each lower level m < n uses the
continuation counts a_m(g) = N_1+(. g), the number of distinct tokens x such
that the (m + 1)-gram x g was seen. With T(h) = sum_x a_m(h x) and
N_1+(h .) the number of x with a_m(h x) > 0, the recursion is

    P_m(w | h) = max(a_m(h w) - D_m, 0) / T(h) + D_m N_1+(h .) / T(h) P_m-1(w | h')
    P_m(w | h) = P_m-1(w | h')                     if T(h) = 0

where h' is h without its first token. Below level 1 sits the uniform
distribution 1 / |V|. The discount of level 1 is 0 by default, so level 1 is
the continuation unigram N_1+(. w) / N_1+(. .).
"""

import math
from collections import Counter
from fractions import Fraction
from typing import Iterable, Sequence

BOS, EOS = "<s>", "</s>"


def pad(sent: Sequence[str], n: int) -> list[str]:
    """Return the sentence with n - 1 copies of <s> in front and </s> at the end."""
    return [BOS] * (n - 1) + list(sent) + [EOS]


def level_counts(corpus: Iterable[Sequence[str]], n: int) -> dict[int, Counter]:
    """Return a[m] for m = 1 to n: raw counts of the n-grams, continuation counts below."""
    a = {n: Counter()}
    for sent in corpus:
        toks = pad(sent, n)
        for i in range(n - 1, len(toks)):
            a[n][tuple(toks[i - n + 1 : i + 1])] += 1  # @line L1
    for m in range(n - 1, 0, -1):
        a[m] = Counter()
        for g in a[m + 1]:  # each distinct (m + 1)-gram x g adds one left context of g
            a[m][g[1:]] += 1  # @line L2
    return a


def default_discount(counts: Counter) -> Fraction:
    """D = n_1 / (n_1 + 2 n_2), from the counts of counts of one level."""
    cc = Counter(counts.values())
    n1, n2 = cc[1], cc[2]
    if n1 == 0:
        raise ValueError("no count equals 1 at this level; give the discounts explicitly")
    return Fraction(n1, n1 + 2 * n2)  # @line L3


class KneserNeyLM:
    """An interpolated Kneser-Ney n-gram model over a closed vocabulary."""

    def __init__(
        self,
        corpus: Iterable[Sequence[str]],
        n: int,
        discounts: Sequence[Fraction | int] | None = None,
        vocab: Iterable[str] | None = None,
    ):
        """discounts[m - 1] is D_m for m = 1 to n. By default D_1 = 0 and D_m = n_1 / (n_1 + 2 n_2)."""
        if n < 1:
            raise ValueError("the order n must be at least 1")
        corpus = [list(s) for s in corpus]
        self.n = n
        self.a = level_counts(corpus, n)
        seen = {g[-1] for g in self.a[n]}
        self.vocab = set(seen) if vocab is None else set(vocab) | {EOS}
        if BOS in self.vocab:
            raise ValueError("<s> is never predicted, so it is not in the vocabulary")
        if not seen <= self.vocab:
            raise ValueError("the vocabulary must hold every training token")
        if discounts is None:
            discounts = [Fraction(0)] + [default_discount(self.a[m]) for m in range(2, n + 1)]
        if len(discounts) != n:
            raise ValueError("give one discount for each order 1 to n")
        self.d = {m: Fraction(discounts[m - 1]) for m in range(1, n + 1)}
        for m, d in self.d.items():
            if not 0 <= d <= 1:
                raise ValueError(f"the discount of order {m} must be in [0, 1]")
        if self.d[1] == 0 and self.vocab != seen:
            raise ValueError("a vocabulary larger than the training tokens needs D_1 > 0")
        # T(h) and N_1+(h .) for every history of every level.
        self.total = {m: Counter() for m in range(1, n + 1)}
        self.types = {m: Counter() for m in range(1, n + 1)}
        for m in range(1, n + 1):
            for g, k in self.a[m].items():
                self.total[m][g[:-1]] += k
                self.types[m][g[:-1]] += 1

    def history(self, tokens: Sequence[str]) -> tuple:
        """The last n - 1 tokens of <s> ... <s> tokens: the history of the next prediction."""
        if self.n == 1:
            return ()
        return tuple([BOS] * (self.n - 1) + list(tokens))[-(self.n - 1) :]

    def prob(self, w: str, tokens: Sequence[str] = ()) -> Fraction:
        """P(w | the sentence so far), where tokens is the sentence so far without <s>."""
        if w not in self.vocab:
            raise KeyError(f"{w!r} is not in the vocabulary")
        return self._prob(w, self.history(tokens))

    def _prob(self, w: str, h: tuple) -> Fraction:
        m = len(h) + 1
        if m == 1:  # @line L4
            lower = Fraction(1, len(self.vocab))
        else:
            lower = self._prob(w, h[1:])
        t = self.total[m][h]  # @line L5
        if t == 0:  # @line L6
            return lower
        d = self.d[m]
        gamma = d * self.types[m][h] / t  # @line L7
        return max(self.a[m][h + (w,)] - d, Fraction(0)) / t + gamma * lower  # @line L8

    def distribution(self, tokens: Sequence[str] = ()) -> dict[str, Fraction]:
        """The full conditional distribution over the vocabulary."""
        return {w: self.prob(w, tokens) for w in sorted(self.vocab)}

    def sentence_logprob(self, sent: Sequence[str]) -> float:
        """The natural log of the probability of the sentence, </s> included, summed in log space."""
        total = 0.0
        sent = list(sent)
        for i, w in enumerate(sent + [EOS]):
            total += log_fraction(self.prob(w, sent[:i]))
        return total


def log_fraction(p: Fraction) -> float:
    """ln p for a positive Fraction, without converting a tiny p to float first."""
    if p <= 0:
        raise ValueError("the log of a probability needs p > 0")
    return math.log(p.numerator) - math.log(p.denominator)
