# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stupid-backoff/. The authors are listed in prov/0ZTM89.jsonl.

"""Stupid backoff scores for an n-gram model (Brants, Popat, Xu, Och and Dean 2007).

A corpus is a list of sentences, and a sentence is a list of str tokens.
Each sentence is padded with n - 1 copies of "<s>" on the left and one
"</s>" on the right. "</s>" is predicted and counted; "<s>" is never
predicted. The score is

    S(w | h) = c(h w) / c(h)        if c(h w) > 0
    S(w | h) = alpha S(w | h')      otherwise
    S(w)     = c(w) / N

where c(h) = sum_x c(h x) is the number of times h is followed by a
predicted token, h' is h without its first token, and N is the number of
predicted tokens. The scores are not probabilities: after a seen history
they sum to at least 1, and the sum can be larger.
"""

import math
from collections import Counter
from fractions import Fraction
from typing import Iterable, Sequence

BOS, EOS = "<s>", "</s>"
ALPHA = Fraction(2, 5)  # 0.4, the value Brants et al. set by hand


class StupidBackoff:
    """Raw n-gram counts of every order and the stupid backoff score."""

    def __init__(self, corpus: Iterable[Sequence[str]], n: int, alpha: Fraction | float = ALPHA):
        if n < 1:
            raise ValueError("the order n must be at least 1")
        if not 0 <= alpha <= 1:
            raise ValueError("alpha must be in [0, 1]")
        self.n = n
        self.alpha = alpha
        self.c: Counter = Counter()  # c(g) for every m-gram g, m = 1 to n, ending at a predicted token
        self.ch: Counter = Counter()  # c(h) = sum_x c(h x)
        for sent in corpus:
            toks = [BOS] * (n - 1) + list(sent) + [EOS]
            for i in range(n - 1, len(toks)):
                for m in range(1, n + 1):
                    g = tuple(toks[i - m + 1 : i + 1])
                    self.c[g] += 1
                    self.ch[g[:-1]] += 1
        self.vocab = {g[0] for g in self.c if len(g) == 1}

    def history(self, tokens: Sequence[str]) -> tuple:
        """The last n - 1 tokens of <s> ... <s> tokens."""
        if self.n == 1:
            return ()
        return tuple([BOS] * (self.n - 1) + list(tokens))[-(self.n - 1) :]

    def score(self, w: str, tokens: Sequence[str] = ()) -> Fraction | float:
        """S(w | the sentence so far). A word never seen in training scores 0."""
        return self._score(w, self.history(tokens))

    def _score(self, w: str, h: tuple) -> Fraction | float:
        k = self.c[h + (w,)]
        if k > 0:  # @line L1
            return Fraction(k, self.ch[h])  # @line L2
        if not h:  # @line L3
            return Fraction(0)
        return self.alpha * self._score(w, h[1:])  # @line L4

    def scores(self, tokens: Sequence[str] = ()) -> dict[str, Fraction | float]:
        """The score of every vocabulary word after the sentence so far."""
        return {w: self.score(w, tokens) for w in sorted(self.vocab)}

    def sentence_logscore(self, sent: Sequence[str]) -> float:
        """The sum of the natural logs of the scores, </s> included. Not a log probability."""
        sent = list(sent)
        total = 0.0
        for i, w in enumerate(sent + [EOS]):
            s = self.score(w, sent[:i])
            if s == 0:
                return -math.inf
            if isinstance(s, Fraction):
                total += math.log(s.numerator) - math.log(s.denominator)
            else:
                total += math.log(s)
        return total
