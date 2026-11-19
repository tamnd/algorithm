# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chrf/. The authors are listed in prov/TFBFZV.jsonl.

"""chrF of Popovic (2015), with the settings of sacreBLEU, at the corpus level.

The input is plain text: a hypothesis is a str, and each hypothesis has a list
of one or more reference strs. White space is removed before the character
n-grams are counted, and the case is kept. With word_order > 0 the score is
chrF++ (Popovic 2017): word n-grams of order 1 .. word_order are added to the
average, and a punctuation mark at the start or the end of a word is split off,
as sacreBLEU does.

Effective order: an order counts in the average only if both the hypothesis
side and the reference side have at least one n-gram of that order (summed over
the corpus). With several references, each sentence uses the statistics of the
reference with the highest sentence-level F, the first one on a tie.

The statistics and the averages are exact Fractions. The scores are floats on
the 0 to 1 scale; sacreBLEU prints them times 100.
"""

import string
from collections import Counter
from fractions import Fraction
from typing import List, Sequence, Tuple

Stats = List[Tuple[int, int, int]]  # per order: (matches, hypothesis n-grams, reference n-grams)

PUNCTUATION = frozenset(string.punctuation)


def ngram_counts(units: Sequence, n: int) -> Counter:
    """Return the multiset of the n-grams of a str or a list of words."""
    return Counter(tuple(units[i:i + n]) for i in range(len(units) - n + 1))


def split_words(text: str) -> List[str]:
    """Split on white space, then split one punctuation mark off the end or the start of a word."""
    out = []
    for w in text.split():
        if len(w) > 1 and w[-1] in PUNCTUATION:
            out += [w[:-1], w[-1]]
        elif len(w) > 1 and w[0] in PUNCTUATION:
            out += [w[0], w[1:]]
        else:
            out.append(w)
    return out


def sentence_stats(hyp: str, ref: str, char_order: int = 6, word_order: int = 0,
                   whitespace: bool = False) -> Stats:
    """Return (matches, hypothesis total, reference total) for each order, characters first."""
    h, r = (hyp, ref) if whitespace else ("".join(hyp.split()), "".join(ref.split()))  # @line L3
    stats = []
    units = [(h, r, n) for n in range(1, char_order + 1)]
    hw, rw = split_words(hyp), split_words(ref)
    units += [(hw, rw, n) for n in range(1, word_order + 1)]
    for a, b, n in units:  # @line L4
        ca, cb = ngram_counts(a, n), ngram_counts(b, n)
        m = sum(min(k, cb[g]) for g, k in ca.items())  # @line L5
        stats.append((m, max(len(a) - n + 1, 0), max(len(b) - n + 1, 0)))  # @line L6
    return stats


def f_score(stats: Stats, beta: float = 2) -> Fraction:
    """Return the chrF of summed statistics as a Fraction in [0, 1]."""
    used = [(m, th, tr) for m, th, tr in stats if th > 0 and tr > 0]  # @line L7
    if not used:  # @line L8
        return Fraction(0)
    k = len(used)
    p = sum(Fraction(m, th) for m, th, _ in used) / k  # @line L9
    r = sum(Fraction(m, tr) for m, _, tr in used) / k
    if p + r == 0:  # @line L10
        return Fraction(0)
    b2 = Fraction(beta) ** 2
    return (1 + b2) * p * r / (b2 * p + r)  # @line L11


def best_stats(hyp: str, refs: Sequence[str], char_order: int = 6, word_order: int = 0,
               beta: float = 2, whitespace: bool = False) -> Stats:
    """Return the statistics against the reference with the highest sentence F."""
    if not refs:
        raise ValueError("each hypothesis needs at least one reference")
    best, best_f = None, None
    for ref in refs:
        st = sentence_stats(hyp, ref, char_order, word_order, whitespace)
        f = f_score(st, beta)
        if best is None or f > best_f:
            best, best_f = st, f
    return best


def corpus_stats(hyps: Sequence[str], refs: Sequence[Sequence[str]], char_order: int = 6,
                 word_order: int = 0, beta: float = 2, whitespace: bool = False) -> Stats:
    """Return the statistics summed over the corpus."""
    if len(hyps) != len(refs):
        raise ValueError("one list of references per hypothesis")
    total = [(0, 0, 0)] * (char_order + word_order)  # @line L1
    for hyp, rs in zip(hyps, refs):  # @line L2
        st = best_stats(hyp, rs, char_order, word_order, beta, whitespace)
        total = [(a + x, b + y, c + z) for (a, b, c), (x, y, z) in zip(total, st)]
    return total


def corpus_chrf(hyps: Sequence[str], refs: Sequence[Sequence[str]], char_order: int = 6,
                word_order: int = 0, beta: float = 2, whitespace: bool = False) -> float:
    """Return corpus chrF (chrF++ with word_order = 2) on the 0 to 1 scale."""
    st = corpus_stats(hyps, refs, char_order, word_order, beta, whitespace)
    return float(f_score(st, beta))


def sentence_chrf(hyp: str, refs: Sequence[str], char_order: int = 6, word_order: int = 0,
                  beta: float = 2, whitespace: bool = False) -> float:
    """Return the chrF of one sentence on the 0 to 1 scale."""
    return corpus_chrf([hyp], [refs], char_order, word_order, beta, whitespace)
