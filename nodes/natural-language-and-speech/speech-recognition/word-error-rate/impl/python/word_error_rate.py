# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-error-rate/. The authors are listed in prov/8WQ3ZQ.jsonl.

"""Word error rate: WER = (S + D + I) / N.

S, D and I are the substitutions, deletions and insertions of a minimum edit
alignment of the hypothesis to the reference with unit costs, and N is the
number of reference words. The edit distance is the Wagner-Fischer dynamic
program. Among the minimum alignments, the traceback prefers a match or a
substitution, then a deletion, then an insertion; the sum S + D + I is the same
for every minimum alignment, but the split into S, D and I can differ.
"""

from fractions import Fraction
from typing import List, Sequence, Tuple


def normalize(text: str) -> List[str]:
    """The normalization of this file: lower case, split on white space, and strip
    the punctuation . , ? ! ; : and double quotes at the ends of each word."""
    words = [w.strip('.,?!;:"') for w in text.lower().split()]
    return [w for w in words if w]


def align(ref: Sequence[str], hyp: Sequence[str]) -> Tuple[int, int, int, List[Tuple[str, str, str]]]:
    """Return (S, D, I, ops) of a minimum edit alignment. ops lists (op, ref word, hyp word)
    with op in "=", "S", "D", "I"; a missing word is ""."""
    n, m = len(ref), len(hyp)
    E = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        E[i][0] = i
    for j in range(1, m + 1):
        E[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sub = E[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1])
            E[i][j] = min(sub, E[i - 1][j] + 1, E[i][j - 1] + 1)
    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and E[i][j] == E[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]):
            ops.append(("=" if ref[i - 1] == hyp[j - 1] else "S", ref[i - 1], hyp[j - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and E[i][j] == E[i - 1][j] + 1:
            ops.append(("D", ref[i - 1], ""))
            i -= 1
        else:
            ops.append(("I", "", hyp[j - 1]))
            j -= 1
    ops.reverse()
    S = sum(op == "S" for op, _, _ in ops)
    D = sum(op == "D" for op, _, _ in ops)
    I = sum(op == "I" for op, _, _ in ops)
    assert S + D + I == E[n][m]
    return S, D, I, ops


def wer(ref: Sequence[str], hyp: Sequence[str]) -> Fraction:
    """Sentence WER as an exact fraction. Raise ValueError for an empty reference."""
    if not ref:
        raise ValueError("WER is undefined for an empty reference")
    S, D, I, _ = align(ref, hyp)
    return Fraction(S + D + I, len(ref))


def corpus_wer(pairs: Sequence[Tuple[Sequence[str], Sequence[str]]]) -> Fraction:
    """Corpus WER: the total errors over the total reference words (not the mean of sentence WERs)."""
    errors = words = 0
    for ref, hyp in pairs:
        S, D, I, _ = align(ref, hyp)
        errors += S + D + I
        words += len(ref)
    if words == 0:
        raise ValueError("WER is undefined for an empty reference")
    return Fraction(errors, words)
