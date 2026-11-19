# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/katz-backoff/. The authors are listed in prov/99DA92.jsonl.

"""Katz backoff for an n-gram language model, exact in Fraction.

A corpus is a list of sentences, and a sentence is a list of str tokens.
Each sentence is padded with n - 1 copies of "<s>" on the left and one
"</s>" on the right; "</s>" is predicted and counted, "<s>" is never
predicted. The vocabulary is the set of predicted training tokens: map rare
or unknown words to "<unk>" before training. The unigram level is the
maximum likelihood estimate c(w) / N.

For an order m >= 2, an m-gram seen r times gets the discount ratio

    d_r = (r* / r - mu) / (1 - mu),  r* = (r + 1) N_(r+1) / N_r,  mu = (k + 1) N_(k+1) / N_1

for 1 <= r <= k, and d_r = 1 for r > k, where N_r counts the m-gram types
seen r times (Katz 1987). If these values are not all in (0, 1], the order
is left undiscounted (d_r = 1 for every r).
"""

from collections import Counter
from fractions import Fraction
from typing import Iterable, Sequence

BOS, EOS = "<s>", "</s>"


def count_ngrams(corpus: Iterable[Sequence[str]], n: int):
    """Return (c, ch, follow): m-gram counts for m = 1 to n, history counts, and the words seen after each history."""
    c: Counter = Counter()
    ch: Counter = Counter()
    follow: dict[tuple, set] = {}
    for sent in corpus:
        toks = [BOS] * (n - 1) + list(sent) + [EOS]
        for i in range(n - 1, len(toks)):
            for m in range(1, n + 1):
                g = tuple(toks[i - m + 1 : i + 1])
                c[g] += 1
                ch[g[:-1]] += 1
                follow.setdefault(g[:-1], set()).add(g[-1])
    return c, ch, follow


def katz_discounts(nr: dict[int, int], k: int) -> dict[int, Fraction]:
    """Return {r: d_r} for 1 <= r <= k, or {} when the Katz discounts are not valid."""
    if k < 1 or nr.get(1, 0) == 0:
        return {}
    mu = Fraction((k + 1) * nr.get(k + 1, 0), nr[1])
    if mu >= 1:
        return {}
    d = {}
    for r in range(1, k + 1):
        if nr.get(r, 0) == 0:
            continue
        rstar = Fraction((r + 1) * nr.get(r + 1, 0), nr[r])
        d[r] = (rstar / r - mu) / (1 - mu)
        if not 0 < d[r] <= 1:
            return {}
    return d


class KatzLM:
    """A Katz backoff n-gram model with Good-Turing discounts for the counts 1 to k."""

    def __init__(self, corpus: Iterable[Sequence[str]], n: int, k: int = 5):
        if n < 1:
            raise ValueError("the order n must be at least 1")
        self.n, self.k = n, k
        self.c, self.ch, self.follow = count_ngrams([list(s) for s in corpus], n)
        self.vocab = {g[0] for g in self.c if len(g) == 1}
        self.total = self.ch[()]
        self.d: dict[int, dict[int, Fraction]] = {}
        for m in range(2, n + 1):
            nr = Counter(v for g, v in self.c.items() if len(g) == m)
            self.d[m] = katz_discounts(dict(nr), k)
        self._alpha: dict[tuple, Fraction] = {}
        self._ml: set[tuple] = set()

    def discounted(self, h: tuple, w: str) -> Fraction:
        """The discounted estimate d_r r / c(h) of a seen m-gram h w."""
        r = self.c[h + (w,)]
        d = 1 if h in self._ml else self.d[len(h) + 1].get(r, 1)
        return d * Fraction(r, self.ch[h])

    def alpha(self, h: tuple) -> Fraction:
        """The backoff weight of the history h, with c(h) > 0."""
        if h not in self._alpha:
            seen = self.follow[h]
            beta = 1 - sum(self.discounted(h, w) for w in seen)  # @line L5
            low = 1 - sum(self._prob(w, h[1:]) for w in seen)  # @line L6
            if low == 0:
                self._ml.add(h)  # nothing to back off to: keep the undiscounted estimates
                self._alpha[h] = Fraction(0)
            else:
                self._alpha[h] = beta / low  # @line L7
        return self._alpha[h]

    def prob(self, w: str, history: Sequence[str] = ()) -> Fraction:
        """P(w | the last n - 1 tokens of history)."""
        if w not in self.vocab:
            raise KeyError(f"{w!r} is not in the vocabulary")
        h = tuple(history)[-(self.n - 1) :] if self.n > 1 else ()
        return self._prob(w, h)

    def _prob(self, w: str, h: tuple) -> Fraction:
        if not h:  # @line L1
            return Fraction(self.c[(w,)], self.total)
        if self.ch[h] == 0:  # @line L2
            return self._prob(w, h[1:])
        a = self.alpha(h)
        if self.c[h + (w,)] > 0:  # @line L3
            return self.discounted(h, w)  # @line L4
        return a * self._prob(w, h[1:])  # @line L8

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
