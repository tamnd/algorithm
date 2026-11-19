# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modified-kneser-ney-smoothing/. The authors are listed in prov/R2ZAVZ.jsonl.

"""Interpolated modified Kneser-Ney smoothing (Chen and Goodman), exact in Fraction.

A corpus is a list of sentences, and a sentence is a list of str tokens.
Each sentence is padded with n - 1 copies of "<s>" on the left and one
"</s>" on the right. "</s>" is predicted and counted; "<s>" is never
predicted.

Level n uses raw counts and each lower level m < n uses the continuation
counts N_1+(. g). A count k loses D(k): 0 for k = 0, D1 for k = 1, D2 for
k = 2 and D3+ for k >= 3. With T(h) = sum_x a(h x) and N_r(h .) the number
of x with a(h x) = r (N_3+ for r >= 3),

    P_m(w | h) = (a(h w) - D(a(h w))) / T(h) + gamma(h) P_m-1(w | h')
    gamma(h)   = (D1 N_1(h .) + D2 N_2(h .) + D3+ N_3+(h .)) / T(h)

and P_m(w | h) = P_m-1(w | h') when T(h) = 0. Below level 1 sits the
uniform distribution 1 / |V|. The discounts of level 1 are 0 by default.
"""

import math
from collections import Counter
from fractions import Fraction
from typing import Iterable, Sequence

BOS, EOS = "<s>", "</s>"

Discounts = tuple[Fraction, Fraction, Fraction]


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
        for g in a[m + 1]:
            a[m][g[1:]] += 1  # @line L2
    return a


def chen_goodman_discounts(counts: Counter) -> Discounts:
    """D1, D2, D3+ from the counts of counts n_1 to n_4 of one level (Chen and Goodman, eq. 17)."""
    cc = Counter(counts.values())
    n1, n2, n3, n4 = cc[1], cc[2], cc[3], cc[4]
    if n1 == 0 or n2 == 0 or n3 == 0:
        raise ValueError("n_1, n_2 and n_3 must be positive; give the discounts explicitly")
    y = Fraction(n1, n1 + 2 * n2)  # @line L3
    d1 = 1 - 2 * y * Fraction(n2, n1)
    d2 = 2 - 3 * y * Fraction(n3, n2)
    d3 = 3 - 4 * y * Fraction(n4, n3)
    return check_discounts((d1, d2, d3))


def check_discounts(d: Sequence[Fraction | int]) -> Discounts:
    """Return the three discounts as Fractions; each D(k) must lie in [0, k]."""
    if len(d) != 3:
        raise ValueError("give three discounts D1, D2, D3+")
    d1, d2, d3 = (Fraction(x) for x in d)
    if not (0 <= d1 <= 1 and 0 <= d2 <= 2 and 0 <= d3 <= 3):
        raise ValueError(f"discounts out of range: D1 in [0, 1], D2 in [0, 2], D3+ in [0, 3], got {d1}, {d2}, {d3}")
    return d1, d2, d3


class ModifiedKneserNeyLM:
    """An interpolated modified Kneser-Ney n-gram model over a closed vocabulary."""

    def __init__(
        self,
        corpus: Iterable[Sequence[str]],
        n: int,
        discounts: Sequence[Sequence[Fraction | int]] | None = None,
        vocab: Iterable[str] | None = None,
    ):
        """discounts[m - 1] = (D1, D2, D3+) for level m. By default level 1 has (0, 0, 0)."""
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
            discounts = [(0, 0, 0)] + [chen_goodman_discounts(self.a[m]) for m in range(2, n + 1)]
        if len(discounts) != n:
            raise ValueError("give three discounts for each order 1 to n")
        self.d = {m: check_discounts(discounts[m - 1]) for m in range(1, n + 1)}
        if self.vocab != seen and self.d[1] == (0, 0, 0):
            raise ValueError("a vocabulary larger than the training tokens needs discounts at level 1")
        # T(h), and N_1(h .), N_2(h .), N_3+(h .) for every history of every level.
        self.total = {m: Counter() for m in range(1, n + 1)}
        self.nr = {m: {} for m in range(1, n + 1)}
        for m in range(1, n + 1):
            for g, k in self.a[m].items():
                h = g[:-1]
                self.total[m][h] += k
                row = self.nr[m].setdefault(h, [0, 0, 0])
                row[min(k, 3) - 1] += 1

    def discount(self, m: int, k: int) -> Fraction:
        """D(k) at level m."""
        return Fraction(0) if k == 0 else self.d[m][min(k, 3) - 1]

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
        d1, d2, d3 = self.d[m]
        n1, n2, n3 = self.nr[m][h]
        gamma = (d1 * n1 + d2 * n2 + d3 * n3) / t  # @line L7
        k = self.a[m][h + (w,)]
        return (k - self.discount(m, k)) / t + gamma * lower  # @line L8

    def distribution(self, tokens: Sequence[str] = ()) -> dict[str, Fraction]:
        """The full conditional distribution over the vocabulary."""
        return {w: self.prob(w, tokens) for w in sorted(self.vocab)}

    def sentence_logprob(self, sent: Sequence[str]) -> float:
        """The natural log of the probability of the sentence, </s> included, summed in log space."""
        sent = list(sent)
        total = 0.0
        for i, w in enumerate(sent + [EOS]):
            p = self.prob(w, sent[:i])
            total += math.log(p.numerator) - math.log(p.denominator)
        return total
