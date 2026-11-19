# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmm-part-of-speech-tagger/. The authors are listed in prov/GZMMN9.jsonl.

"""An HMM part-of-speech tagger of order m (m = 1 bigram, m = 2 trigram as in TnT).

Training counts tag n-grams in a tagged corpus. Each sentence gets m start
tags <s> and one end tag </s>, so a sentence of n tokens gives n + 1
predicted events. The transition model is the linear interpolation of
maximum likelihood estimates of orders 0 to m, with weights from Brants's
deleted interpolation (TnT, Figure 1). Known words use the maximum
likelihood emission f(w, t) / f(t). Unknown words use the TnT suffix model.
Decoding is the Viterbi algorithm in log space over states that are the
last m tags, so it costs O(n k^(m + 1)) time.

Tie rules:
- deleted interpolation: when two of the deleted estimates are equal, the
  higher order wins (the first maximum in the order m, m - 1, ..., 0);
- Viterbi: among equal scores, the first predecessor state and the first
  final state in the enumeration order win (tags in sorted order).
"""

import math
from fractions import Fraction
from itertools import product
from typing import Callable, Dict, List, Sequence, Tuple

from nlslog import NEG_INF, safe_log

BOS = "<s>"
EOS = "</s>"


def tag_events(tag_seqs: Sequence[Sequence[str]], m: int):
    """Count the predicted events of an order m tag model.

    Return (ngram, hist, N). ngram[g] is the count of the tag n-gram g, for
    lengths 1 to m + 1, where the last tag of g is a predicted tag (a real
    tag or EOS). hist[h] is the number of predicted events whose history ends
    with h, for lengths 1 to m. N is the number of predicted events.
    """
    ngram: Dict[Tuple[str, ...], int] = {}
    hist: Dict[Tuple[str, ...], int] = {}
    N = 0
    for tags in tag_seqs:  # @line L1
        seq = [BOS] * m + list(tags) + [EOS]
        for i in range(m, len(seq)):
            N += 1
            for j in range(0, m + 1):
                g = tuple(seq[i - j:i + 1])
                ngram[g] = ngram.get(g, 0) + 1
                if j > 0:
                    h = g[:-1]
                    hist[h] = hist.get(h, 0) + 1
    return ngram, hist, N


def _ratio(a: int, b: int) -> Fraction:
    """a / b, and 0 when b is 0 (the rule under Brants's Figure 1)."""
    return Fraction(0) if b == 0 else Fraction(a, b)


def deleted_interpolation(tag_seqs: Sequence[Sequence[str]], m: int) -> List[Fraction]:
    """Return [lambda_0, ..., lambda_m], the weights of orders 0 to m.

    For each (m + 1)-gram g with count c > 0, compare the deleted estimates
    (f(g[j:]) - 1) / (hist(g[j:-1]) - 1) for j = 0 .. m (order m - j), and
    (f(t) - 1) / (N - 1) for order 0. Add c to the weight of the largest.
    """
    ngram, hist, N = tag_events(tag_seqs, m)
    lam = [0] * (m + 1)
    for g, c in sorted(ngram.items()):  # @line L2
        if len(g) != m + 1:
            continue
        best_order, best = -1, Fraction(-1)
        for order in range(m, -1, -1):  # higher order first: it wins ties
            tail = g[m - order:]
            if order == 0:
                v = _ratio(ngram[tail] - 1, N - 1)
            else:
                v = _ratio(ngram[tail] - 1, hist[tail[:-1]] - 1)
            if v > best:
                best_order, best = order, v
        lam[best_order] += c
    total = sum(lam)
    return [Fraction(x, total) for x in lam]


class HMMTagger:
    """A trained tagger. corpus is a list of (words, tags) pairs."""

    def __init__(self, corpus: Sequence[Tuple[Sequence[str], Sequence[str]]], m: int = 2,
                 max_suffix: int = 10, rare: int = 10):
        if m < 1:
            raise ValueError("the order m must be at least 1")
        self.m = m
        tag_seqs = [list(t) for _, t in corpus]
        self.tags = sorted({t for ts in tag_seqs for t in ts})
        self.ngram, self.hist, self.N = tag_events(tag_seqs, m)
        self.lam = deleted_interpolation(tag_seqs, m)
        self.wt: Dict[Tuple[str, str], int] = {}
        self.ft: Dict[str, int] = {}
        self.fw: Dict[str, int] = {}
        for words, tags in corpus:
            if len(words) != len(tags):
                raise ValueError("words and tags differ in length")
            for w, t in zip(words, tags):
                self.wt[(w, t)] = self.wt.get((w, t), 0) + 1
                self.ft[t] = self.ft.get(t, 0) + 1
                self.fw[w] = self.fw.get(w, 0) + 1
        self.max_suffix = max_suffix
        self._suffix_init(rare)

    # Transition model ------------------------------------------------------

    def trans(self, h: Tuple[str, ...], t: str) -> Fraction:
        """P(t | h) = sum_j lambda_j P^(t | last j tags of h), for h of length m."""
        p = self.lam[0] * Fraction(self.ngram.get((t,), 0), self.N)  # @line L3
        for j in range(1, self.m + 1):
            ctx = tuple(h[self.m - j:])
            p += self.lam[j] * _ratio(self.ngram.get(ctx + (t,), 0), self.hist.get(ctx, 0))
        return p

    # Emission model --------------------------------------------------------

    def _suffix_init(self, rare: int) -> None:
        """Count (suffix, tag) over the tokens of rare words (all words if none is rare)."""
        rare_words = {w for w, c in self.fw.items() if c <= rare} or set(self.fw)
        self.sfx: Dict[str, Dict[str, int]] = {}
        for (w, t), c in sorted(self.wt.items()):
            if w not in rare_words:
                continue
            for i in range(0, min(self.max_suffix, len(w)) + 1):
                s = w[len(w) - i:]
                row = self.sfx.setdefault(s, {})
                row[t] = row.get(t, 0) + c
        total = sum(self.ft.values())
        ps = [self.ft[t] / total for t in self.tags]
        mean = sum(ps) / len(ps)
        s = len(ps)
        self.theta = math.sqrt(sum((p - mean) ** 2 for p in ps) / (s - 1)) if s > 1 else 1.0

    def suffix_dist(self, w: str) -> Dict[str, float]:
        """TnT suffix model: P(t | longest seen suffix of w), at most max_suffix letters."""
        row = self.sfx[""]
        tot = sum(row.values())
        p = {t: row.get(t, 0) / tot for t in self.tags}
        for i in range(1, min(self.max_suffix, len(w)) + 1):
            row = self.sfx.get(w[len(w) - i:])
            if row is None:
                break
            tot = sum(row.values())
            p = {t: (row.get(t, 0) / tot + self.theta * p[t]) / (1 + self.theta) for t in self.tags}
        return p

    def log_emit(self, w: str, t: str) -> float:
        """log P(w | t) for a known word; log P(t | suffix) / P(t) for an unknown word."""
        if w in self.fw:  # @line L4
            return safe_log(Fraction(self.wt.get((w, t), 0), self.ft[t]))
        prior = self.sfx[""]
        p0 = prior.get(t, 0) / sum(prior.values())
        if p0 == 0:
            return NEG_INF
        return safe_log(self.suffix_dist(w)[t] / p0)

    def log_trans(self, h: Tuple[str, ...], t: str) -> float:
        return safe_log(self.trans(h, t))

    def tag(self, words: Sequence[str]) -> List[str]:
        return viterbi(words, self.tags, self.m, self.log_trans, self.log_emit)[0]


def viterbi(words: Sequence[str], tags: Sequence[str], m: int,
            log_trans: Callable[[Tuple[str, ...], str], float],
            log_emit: Callable[[str, str], float]):
    """Return (best tags, best log P(x, y)) for an order m HMM.

    A state is the tuple of the last m tags; BOS fills the tuple at the start.
    log_trans(h, t) is log P(t | h) for a history h of m tags (t may be EOS).
    Raises ValueError for an empty sentence or if every tag sequence has
    probability 0.
    """
    n = len(words)
    if n == 0:
        raise ValueError("empty sentence")
    start = (BOS,) * m
    delta = {start: 0.0}  # @line L5
    back: List[Dict[Tuple[str, ...], Tuple[str, ...]]] = []
    lt: Dict[Tuple[Tuple[str, ...], str], float] = {}

    def tr(h, t):
        key = (h, t)
        if key not in lt:
            lt[key] = log_trans(h, t)
        return lt[key]

    for i in range(n):  # @line L6
        new: Dict[Tuple[str, ...], float] = {}
        bp: Dict[Tuple[str, ...], Tuple[str, ...]] = {}
        for t in tags:
            e = log_emit(words[i], t)
            if e == NEG_INF:
                continue
            for g, s in delta.items():  # @line L7
                v = s + tr(g, t) + e
                h = g[1:] + (t,)
                if h not in new or v > new[h]:
                    new[h], bp[h] = v, g
        delta = new
        back.append(bp)
    best_h, best = None, NEG_INF
    for h, s in delta.items():  # @line L8
        v = s + tr(h, EOS)
        if best_h is None or v > best:
            best_h, best = h, v
    if best_h is None or best == NEG_INF:
        raise ValueError("every tag sequence has probability 0")
    out = []
    h = best_h
    for i in range(n - 1, -1, -1):  # @line L9
        out.append(h[-1])
        h = back[i][h]
    out.reverse()
    return out, best  # @line L10


def log_joint(words: Sequence[str], ys: Sequence[str], m: int,
              log_trans: Callable, log_emit: Callable) -> float:
    """log P(x, y) for one tag sequence, by the product formula (for brute force)."""
    h = (BOS,) * m
    s = 0.0
    for w, t in zip(words, ys):
        s += log_trans(h, t) + log_emit(w, t)
        h = h[1:] + (t,)
    return s + log_trans(h, EOS)


def brute_force(words: Sequence[str], tags: Sequence[str], m: int,
                log_trans: Callable, log_emit: Callable):
    """The best tag sequence by listing all k^n of them (first maximum wins)."""
    best_y, best = None, NEG_INF
    for ys in product(tags, repeat=len(words)):
        v = log_joint(words, ys, m, log_trans, log_emit)
        if best_y is None or v > best:
            best_y, best = list(ys), v
    return best_y, best
