# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/entropy-based-ngram-pruning/. The authors are listed in prov/AG7MBF.jsonl.

"""Entropy-based pruning of a backoff n-gram model (Stolcke 1998).

A corpus is a list of sentences, and a sentence is a list of str tokens.
Each sentence is padded with n - 1 copies of "<s>" on the left and one
"</s>" on the right. "</s>" is predicted; "<s>" is never predicted.

The model is a backoff model with absolute discounting:

    p(w | h) = (c(h w) - d) / c(h)          if (h, w) is explicit
    p(w | h) = alpha(h) p(w | h')           otherwise
    p(w)     = c(w) / N

where h' is h without its first token and alpha(h) makes the row sum to 1.
Pruning removes explicit n-grams of order 2 or more. The cost of removing
(h, w) alone is the relative entropy D between the model and the model
without it, which only changes the row of h. All costs are computed on the
original model, the n-grams with exp(D) - 1 < theta are removed, and the
backoff weights are computed again.
"""

import math
from collections import Counter, defaultdict
from fractions import Fraction
from typing import Iterable, Sequence

BOS, EOS = "<s>", "</s>"


def log_fraction(p: Fraction) -> float:
    """ln p for a positive Fraction, without float underflow."""
    return math.log(p.numerator) - math.log(p.denominator)


class BackoffLM:
    """A backoff n-gram model with absolute discounting and an explicit n-gram set."""

    def __init__(self, corpus: Iterable[Sequence[str]], n: int, d: Fraction = Fraction(1, 2)):
        if n < 1:
            raise ValueError("the order n must be at least 1")
        if not 0 < d < 1:
            raise ValueError("the discount d must be in (0, 1)")
        self.n, self.d = n, Fraction(d)
        self.c: Counter = Counter()  # c(g) for every m-gram g ending at a predicted token
        self.ch: Counter = Counter()  # c(h) = sum_x c(h x)
        for sent in corpus:
            toks = [BOS] * (n - 1) + list(sent) + [EOS]
            for i in range(n - 1, len(toks)):
                for m in range(1, n + 1):
                    g = tuple(toks[i - m + 1 : i + 1])
                    self.c[g] += 1
                    self.ch[g[:-1]] += 1
        self.vocab = sorted(g[0] for g in self.c if len(g) == 1)
        self.total = self.ch[()]
        self.explicit: dict[tuple, set] = defaultdict(set)  # h -> the words w with (h, w) explicit
        for g in self.c:
            if len(g) >= 2:
                self.explicit[g[:-1]].add(g[-1])
        self._finish()

    def _finish(self) -> None:
        """Compute alpha(h) for every history with explicit words."""
        self._memo: dict = {}
        self.alpha: dict[tuple, Fraction] = {}
        for h, ws in self.explicit.items():
            if not ws:
                continue
            num = 1 - sum(self.pstar(h + (w,)) for w in ws)
            den = 1 - sum(self.prob(w, h[1:]) for w in ws)
            if den == 0:
                raise ValueError(f"every word was seen after {h}; nothing is left to back off to")
            self.alpha[h] = num / den

    def pstar(self, g: tuple) -> Fraction:
        """The discounted estimate of an explicit n-gram g = h w."""
        return (self.c[g] - self.d) / self.ch[g[:-1]]

    def num_explicit(self) -> int:
        return sum(len(ws) for ws in self.explicit.values())

    def history(self, tokens: Sequence[str]) -> tuple:
        if self.n == 1:
            return ()
        return tuple([BOS] * (self.n - 1) + list(tokens))[-(self.n - 1) :]

    def prob(self, w: str, h: tuple) -> Fraction:
        """p(w | h) for a history tuple of at most n - 1 tokens."""
        key = (w, h)
        if key not in self._memo:
            if not h:
                p = Fraction(self.c[(w,)], self.total)
            elif w in self.explicit.get(h, ()):
                p = self.pstar(h + (w,))
            else:
                p = self.alpha.get(h, Fraction(1)) * self.prob(w, h[1:])
            self._memo[key] = p
        return self._memo[key]

    def distribution(self, h: tuple) -> dict[str, Fraction]:
        return {w: self.prob(w, h) for w in self.vocab}

    def history_prob(self, h: tuple) -> Fraction:
        """p(h) by the chain rule of the model; the leading <s> pads have probability 1."""
        p = Fraction(1)
        for i, x in enumerate(h):
            if x != BOS:
                p *= self.prob(x, h[:i][-(self.n - 1) :] if self.n > 1 else ())
        return p

    def sentence_logprob(self, sent: Sequence[str]) -> float:
        sent = list(sent)
        return sum(log_fraction(self.prob(w, self.history(sent[:i]))) for i, w in enumerate(sent + [EOS]))

    def without(self, removed: Iterable[tuple]) -> "BackoffLM":
        """A copy of the model with the explicit n-grams in removed taken out and alpha recomputed."""
        new = object.__new__(BackoffLM)
        new.n, new.d, new.c, new.ch, new.vocab, new.total = self.n, self.d, self.c, self.ch, self.vocab, self.total
        new.explicit = defaultdict(set, {h: set(ws) for h, ws in self.explicit.items()})
        for g in removed:
            if len(g) < 2:
                raise ValueError("unigrams are never pruned")
            new.explicit[g[:-1]].discard(g[-1])
        new._finish()
        return new


def pruning_cost(lm: BackoffLM, g: tuple, sums: dict | None = None) -> float:
    """D(p || p') when only the explicit n-gram g = h w is removed from lm."""
    h, w = g[:-1], g[-1]
    if w not in lm.explicit.get(h, ()):
        raise ValueError(f"{g} is not an explicit n-gram")
    if sums is None or h not in sums:
        s1 = sum(lm.pstar(h + (v,)) for v in lm.explicit[h])
        s2 = sum(lm.prob(v, h[1:]) for v in lm.explicit[h])
        if sums is not None:
            sums[h] = (s1, s2)
    else:
        s1, s2 = sums[h]
    ph = lm.history_prob(h)  # @line L2
    p, lower = lm.pstar(g), lm.prob(w, h[1:])
    alpha = lm.alpha[h]
    alpha_new = (1 - s1 + p) / (1 - s2 + lower)  # @line L3
    backed_off = alpha * (1 - s2)  # @line L4
    cost = ph * (p * (log_fraction(p) - log_fraction(alpha_new * lower)))
    if backed_off > 0:
        cost += ph * backed_off * (log_fraction(alpha) - log_fraction(alpha_new))
    return max(float(cost), 0.0)  # @line L5


def prune(lm: BackoffLM, theta: float) -> tuple[BackoffLM, list[tuple]]:
    """Remove every explicit n-gram whose relative perplexity increase exp(D) - 1 is below theta."""
    if theta < 0:
        raise ValueError("theta must be at least 0")
    sums: dict = {}
    marked = []
    for h in sorted(lm.explicit):
        for w in sorted(lm.explicit[h]):  # @line L1
            if math.expm1(pruning_cost(lm, h + (w,), sums)) < theta:  # @line L6
                marked.append(h + (w,))
    return lm.without(marked), marked  # @line L7
