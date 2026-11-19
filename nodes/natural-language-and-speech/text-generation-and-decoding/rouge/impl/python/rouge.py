# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rouge/. The authors are listed in prov/MTNGKQ.jsonl.

"""ROUGE-N, ROUGE-L and ROUGE-S (Lin 2004) with exact fractions.

Texts are lists of tokens; the caller does the tokenization, the lower
casing, the stemming and the removal of stop words. A summary for the
summary-level ROUGE-L is a list of sentences, each a list of tokens.
"""

from collections import Counter
from fractions import Fraction
from typing import Callable, Hashable, List, Optional, Sequence, Set, Tuple

Tokens = Sequence[Hashable]
Score = Tuple[Fraction, Fraction, Fraction]


def ngrams(tokens: Tokens, n: int) -> Counter:
    """The multiset of n-grams of a token list."""
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def f_measure(r: Fraction, p: Fraction, beta: Fraction = Fraction(1)) -> Fraction:
    """F = (1 + beta^2) R P / (R + beta^2 P), and 0 when R = P = 0."""
    den = r + beta * beta * p
    if den == 0:
        return Fraction(0)
    return (1 + beta * beta) * r * p / den


def ratio(a: int, b: int) -> Fraction:
    return Fraction(a, b) if b else Fraction(0)


def rouge_n(cand: Tokens, ref: Tokens, n: int) -> Score:
    """(R, P, F with beta = 1) of ROUGE-N for one reference, with clipped counts."""
    c, r = ngrams(cand, n), ngrams(ref, n)
    match = sum(min(k, c[g]) for g, k in r.items())
    rec = ratio(match, sum(r.values()))
    prec = ratio(match, sum(c.values()))
    return rec, prec, f_measure(rec, prec)


def rouge_n_pooled(cand: Tokens, refs: Sequence[Tokens], n: int) -> Fraction:
    """Equation 1 of Lin (2004): matches and reference n-grams summed over all references."""
    c = ngrams(cand, n)
    match = total = 0
    for ref in refs:
        r = ngrams(ref, n)
        match += sum(min(k, c[g]) for g, k in r.items())
        total += sum(r.values())
    return ratio(match, total)


def rouge_multi(
    cand: Tokens, refs: Sequence[Tokens], score: Callable[[Tokens, Tokens], Fraction]
) -> Fraction:
    """Several references: the largest of the pairwise scores (Section 2.1)."""
    return max(score(cand, ref) for ref in refs)


def jackknife(
    cand: Tokens, refs: Sequence[Tokens], score: Callable[[Tokens, Tokens], Fraction]
) -> Fraction:
    """The mean over the M sets of M - 1 references of the best pairwise score."""
    m = len(refs)
    if m == 1:
        return score(cand, refs[0])
    total = Fraction(0)
    for k in range(m):
        total += rouge_multi(cand, [refs[i] for i in range(m) if i != k], score)
    return total / m


def lcs_table(a: Tokens, b: Tokens) -> List[List[int]]:
    """t[i][j] = length of a longest common subsequence of a[:i] and b[:j]."""
    t = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                t[i][j] = t[i - 1][j - 1] + 1
            else:
                t[i][j] = max(t[i - 1][j], t[i][j - 1])
    return t


def lcs_length(a: Tokens, b: Tokens) -> int:
    return lcs_table(a, b)[len(a)][len(b)]


def rouge_l(cand: Tokens, ref: Tokens, beta: Fraction = Fraction(1)) -> Score:
    """Sentence-level ROUGE-L: R = LCS / |ref|, P = LCS / |cand|, and F with beta."""
    k = lcs_length(cand, ref)
    rec, prec = ratio(k, len(ref)), ratio(k, len(cand))
    return rec, prec, f_measure(rec, prec, beta)


def lcs_positions(ref: Tokens, cand: Tokens) -> Set[int]:
    """The positions in ref of one longest common subsequence, found by tracing back."""
    t = lcs_table(ref, cand)
    i, j, out = len(ref), len(cand), set()
    while i > 0 and j > 0:
        if ref[i - 1] == cand[j - 1]:
            out.add(i - 1)
            i -= 1
            j -= 1
        elif t[i - 1][j] >= t[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return out


def union_lcs(ref_sentence: Tokens, cand_sentences: Sequence[Tokens]) -> int:
    """The number of reference positions in the union of the LCS with each candidate sentence."""
    hit: Set[int] = set()
    for c in cand_sentences:
        hit |= lcs_positions(ref_sentence, c)
    return len(hit)


def rouge_l_summary(
    cand_sentences: Sequence[Tokens], ref_sentences: Sequence[Tokens], beta: Fraction = Fraction(1)
) -> Score:
    """Summary-level ROUGE-L (Section 3.2), as computed by ROUGE-Lsum.

    The union LCS of each reference sentence is counted once per position;
    the clipping of repeated words used by some packages is not applied.
    """
    hits = sum(union_lcs(r, cand_sentences) for r in ref_sentences)
    m = sum(len(r) for r in ref_sentences)
    n = sum(len(c) for c in cand_sentences)
    rec, prec = ratio(hits, m), ratio(hits, n)
    return rec, prec, f_measure(rec, prec, beta)


def skip_bigrams(tokens: Tokens, max_gap: Optional[int] = None) -> Counter:
    """Pairs of tokens in order; with max_gap = k, at most k tokens between them."""
    out: Counter = Counter()
    for i in range(len(tokens)):
        last = len(tokens) if max_gap is None else min(len(tokens), i + max_gap + 2)
        for j in range(i + 1, last):
            out[(tokens[i], tokens[j])] += 1
    return out


def rouge_s(cand: Tokens, ref: Tokens, max_gap: Optional[int] = None,
            beta: Fraction = Fraction(1)) -> Score:
    """ROUGE-S: skip-bigram recall, precision and F."""
    c, r = skip_bigrams(cand, max_gap), skip_bigrams(ref, max_gap)
    match = sum(min(k, c[g]) for g, k in r.items())
    rec, prec = ratio(match, sum(r.values())), ratio(match, sum(c.values()))
    return rec, prec, f_measure(rec, prec, beta)
