# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/span-f1-score/. The authors are listed in prov/Q2NAGZ.jsonl.

"""Span-level precision, recall and F1, with exact match of boundaries and type.

A span (i, j, X) uses fencepost indices: it covers the tokens i+1 .. j of the
sentence (0-based tokens i .. j-1) and has the type X. A predicted span is
correct only if a gold span has the same i, the same j and the same X. Counts
are summed over all sentences before the ratios are taken (micro average).
All values are exact Fractions.

bio_to_spans reads B/I/O tags as the CoNLL chunk rules do: a B-X starts a
span; an I-X starts a span when it follows O, the sentence start or a tag of
another type; a span ends before O, before a tag that starts a span, or at the
end of the sentence. This reads valid IOB2 and IOB1 tags, and any other
sequence of O, B-X and I-X tags.
"""

from fractions import Fraction
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

Span = Tuple[int, int, str]


def split(tag: str) -> Tuple[str, Optional[str]]:
    if tag == "O":
        return "O", None
    prefix, _, label = tag.partition("-")
    if prefix not in ("B", "I") or not label:
        raise ValueError("bad tag: " + tag)
    return prefix, label


def bio_to_spans(tags: Sequence[str]) -> List[Span]:
    spans: List[Span] = []
    start, cur = 0, None
    for p, tag in enumerate(tags):
        prefix, label = split(tag)
        starts = prefix == "B" or (prefix == "I" and label != cur)  # @line L1
        if cur is not None and (prefix == "O" or starts):  # @line L2
            spans.append((start, p, cur))
            cur = None
        if starts:
            start, cur = p, label
    if cur is not None:
        spans.append((start, len(tags), cur))
    return spans


def counts(gold: Iterable[Set[Span]], pred: Iterable[Set[Span]]) -> Tuple[int, int, int]:
    """True positives, false positives and false negatives, summed over the sentences."""
    tp = fp = fn = 0
    for g, p in zip(gold, pred):
        g, p = set(g), set(p)
        hit = len(g & p)  # @line L3
        tp += hit
        fp += len(p) - hit  # @line L4
        fn += len(g) - hit  # @line L5
    return tp, fp, fn


def prf(tp: int, fp: int, fn: int) -> Tuple[Fraction, Fraction, Fraction]:
    """Precision, recall and F1. A ratio with a zero denominator is taken as 0."""
    p = Fraction(tp, tp + fp) if tp + fp else Fraction(0)  # @line L6
    r = Fraction(tp, tp + fn) if tp + fn else Fraction(0)  # @line L7
    f = 2 * p * r / (p + r) if p + r else Fraction(0)  # @line L8
    return p, r, f


def span_f1(gold_tags: Sequence[Sequence[str]], pred_tags: Sequence[Sequence[str]]):
    """Micro-averaged precision, recall and F1 over sentences given as tag sequences."""
    for g, p in zip(gold_tags, pred_tags):
        if len(g) != len(p):
            raise ValueError("gold and predicted sentences differ in length")
    return prf(*counts([set(bio_to_spans(g)) for g in gold_tags], [set(bio_to_spans(p)) for p in pred_tags]))


def per_type(gold: Sequence[Set[Span]], pred: Sequence[Set[Span]]) -> Dict[str, Tuple[Fraction, Fraction, Fraction]]:
    """Precision, recall and F1 for each type separately."""
    types = sorted({x for s in list(gold) + list(pred) for _, _, x in s})
    out = {}
    for x in types:
        g = [{s for s in sent if s[2] == x} for sent in gold]
        p = [{s for s in sent if s[2] == x} for sent in pred]
        out[x] = prf(*counts(g, p))
    return out


def macro_f1(gold: Sequence[Set[Span]], pred: Sequence[Set[Span]]) -> Fraction:
    """The mean of the per-type F1 values."""
    table = per_type(gold, pred)
    return sum((f for _, _, f in table.values()), Fraction(0)) / len(table) if table else Fraction(0)


def token_accuracy(gold_tags: Sequence[Sequence[str]], pred_tags: Sequence[Sequence[str]]) -> Fraction:
    pairs = [(a, b) for g, p in zip(gold_tags, pred_tags) for a, b in zip(g, p)]
    return Fraction(sum(a == b for a, b in pairs), len(pairs))
