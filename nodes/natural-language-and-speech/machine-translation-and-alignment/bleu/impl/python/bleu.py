# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bleu/. The authors are listed in prov/FSSX1F.jsonl.

"""BLEU of Papineni, Roukos, Ward and Zhu (2002), at the corpus level.

The input is pre-tokenized: a candidate is a list of str tokens, and each
candidate has a list of one or more references, each a list of tokens. The
score depends on the tokenization; to compare with published numbers, tokenize
with the 13a tokenizer of sacreBLEU first. This module does no tokenization.

The clipped counts and the precisions are exact Fractions. The final score is
a float on the 0 to 1 scale.

Effective reference length: for each candidate, the reference length closest
to the candidate length, and the shorter one on a tie (as in sacreBLEU).

Smoothing: "none" (the paper), or "exp", method 3 of Chen and Cherry (2014):
the k-th order with zero matches gets the precision 1 / (2^k * t_n). An order
with no candidate n-grams at all (t_n = 0) gives the score 0 in both modes.
"""

import math
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence, Tuple

Tokens = Sequence[str]


def ngram_counts(tokens: Tokens, n: int) -> Counter:
    """Return the multiset of the n-grams of tokens, as a Counter of tuples."""
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def closest_ref_length(c: int, ref_lengths: Sequence[int]) -> int:
    """Return the reference length closest to c, the shorter one on a tie."""
    return min(ref_lengths, key=lambda r: (abs(r - c), r))


@dataclass
class BleuStats:
    """The sufficient statistics of corpus BLEU."""

    matches: List[int]  # m_n, the clipped matches of order n = 1 .. N
    totals: List[int]  # t_n, the candidate n-grams of order n
    c: int  # the total candidate length
    r: int  # the total effective reference length


def sentence_stats(candidate: Tokens, references: Sequence[Tokens], max_n: int = 4) -> BleuStats:
    """Return the BLEU statistics of one candidate against its references."""
    if not references:
        raise ValueError("each candidate needs at least one reference")
    c = len(candidate)  # @line L4
    r = closest_ref_length(c, [len(x) for x in references])  # @line L5
    matches, totals = [], []
    for n in range(1, max_n + 1):  # @line L6
        cand = ngram_counts(candidate, n)  # @line L7
        best = Counter()
        for ref in references:
            for g, k in ngram_counts(ref, n).items():
                if k > best[g]:
                    best[g] = k
        # clip each count at its largest count in one reference
        matches.append(sum(min(k, best[g]) for g, k in cand.items()))  # @line L8
        totals.append(max(c - n + 1, 0))  # @line L9
    return BleuStats(matches, totals, c, r)


def add_stats(a: BleuStats, b: BleuStats) -> BleuStats:
    """Return the sum of two sets of statistics."""
    return BleuStats([x + y for x, y in zip(a.matches, b.matches)],
                     [x + y for x, y in zip(a.totals, b.totals)], a.c + b.c, a.r + b.r)


def precisions(stats: BleuStats) -> List[Fraction]:
    """Return the clipped precisions p_n = m_n / t_n as Fractions (0 when t_n = 0)."""
    return [Fraction(m, t) if t else Fraction(0) for m, t in zip(stats.matches, stats.totals)]


def brevity_penalty(c: int, r: int) -> float:
    """Return BP = 1 if c > r, else exp(1 - r / c). BP is 0 for c = 0."""
    if c > r:  # @line L11
        return 1.0
    if c == 0:
        return 0.0
    return math.exp(1 - r / c)


def bleu_from_stats(stats: BleuStats, smoothing: str = "none") -> float:
    """Return BLEU = BP * exp(sum_n (1/N) log p_n) from the statistics."""
    if smoothing not in ("none", "exp"):
        raise ValueError("smoothing must be 'none' or 'exp'")
    big_n = len(stats.matches)
    logs = []
    k = 0
    for m, t in zip(stats.matches, stats.totals):
        if t == 0:
            return 0.0
        if m == 0:  # @line L10
            if smoothing == "none":
                return 0.0
            k += 1
            logs.append(-math.log(2 ** k * t))
        else:
            logs.append(math.log(m) - math.log(t))
    return brevity_penalty(stats.c, stats.r) * math.exp(sum(logs) / big_n)  # @line L12


def corpus_stats(candidates: Sequence[Tokens], references: Sequence[Sequence[Tokens]],
                 max_n: int = 4) -> BleuStats:
    """Return the summed statistics of a corpus."""
    if len(candidates) != len(references):
        raise ValueError("one list of references per candidate")
    zeros = [0] * max_n  # @line L1
    total = BleuStats(zeros, list(zeros), 0, 0)  # @line L2
    for cand, refs in zip(candidates, references):  # @line L3
        total = add_stats(total, sentence_stats(cand, refs, max_n))
    return total


def corpus_bleu(candidates: Sequence[Tokens], references: Sequence[Sequence[Tokens]],
                max_n: int = 4, smoothing: str = "none") -> float:
    """Return corpus BLEU on the 0 to 1 scale. It is not the mean of sentence BLEU."""
    return bleu_from_stats(corpus_stats(candidates, references, max_n), smoothing)


def sentence_bleu(candidate: Tokens, references: Sequence[Tokens], max_n: int = 4,
                  smoothing: str = "exp") -> float:
    """Return BLEU of one sentence, smoothed by default (method 3 of Chen and Cherry)."""
    return bleu_from_stats(sentence_stats(candidate, references, max_n), smoothing)


def bleu_details(candidates: Sequence[Tokens], references: Sequence[Sequence[Tokens]],
                 max_n: int = 4) -> Tuple[List[Fraction], float, float]:
    """Return the precisions, the brevity penalty and the unsmoothed BLEU."""
    st = corpus_stats(candidates, references, max_n)
    return precisions(st), brevity_penalty(st.c, st.r), bleu_from_stats(st)
