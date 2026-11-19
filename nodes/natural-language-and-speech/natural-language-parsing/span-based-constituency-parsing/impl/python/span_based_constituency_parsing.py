# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/span-based-constituency-parsing/. The authors are listed in prov/M9QEWS.jsonl.

"""Span-based constituency parsing: the chart decoder over given span scores.

The code takes the network outputs as given: label_scores[(i, j)] is a list of
L real numbers, the score of each label for the fencepost span (i, j), which
covers the words i + 1 to j (words i to j - 1 counted from 0). Label 0 is the
empty label, which marks a span that exists only in the binarized tree.
span_scores[(i, j)] is an optional extra score for the span, 0 by default.

A binary tree over n words has exactly 2n - 1 spans. Its score is the sum over
its spans (i, j, l) of label_scores[(i, j)][l] + span_scores[(i, j)]. The chart
decoder finds a tree of largest score in O(n^3 + n^2 L) time and O(n^2) space.
The output tree drops the spans with the empty label, which can make it n-ary.
"""

from typing import Dict, List, Optional, Sequence, Set, Tuple

Span = Tuple[int, int]
LabeledSpan = Tuple[int, int, int]
EMPTY = 0


def _best_label(scores: Sequence[float]) -> int:
    best = 0
    for k in range(1, len(scores)):
        if scores[k] > scores[best]:
            best = k
    return best


def chart_parse(n: int, label_scores: Dict[Span, Sequence[float]],
                span_scores: Optional[Dict[Span, float]] = None) -> Tuple[float, List[LabeledSpan]]:
    """Return (best score, the 2n - 1 labeled spans of a best binary tree).

    The label of a span and the split below it are chosen independently, so
    the label max costs O(L) per span and the split max O(n) per span.
    """
    if n < 1:
        raise ValueError("a tree needs at least one word")
    span_scores = span_scores or {}
    best: Dict[Span, float] = {}
    split: Dict[Span, int] = {}
    label: Dict[Span, int] = {}
    for length in range(1, n + 1):  # @line L1
        for i in range(n - length + 1):  # @line L2
            j = i + length  # @line L3
            scores = label_scores[(i, j)]
            lab = _best_label(scores)  # @line L4
            v = scores[lab] + span_scores.get((i, j), 0.0)
            if length == 1:  # @line L5
                best[(i, j)] = v
            else:
                k_best = i + 1
                for k in range(i + 2, j):  # @line L6
                    if best[(i, k)] + best[(k, j)] > best[(i, k_best)] + best[(k_best, j)]:
                        k_best = k
                best[(i, j)] = v + best[(i, k_best)] + best[(k_best, j)]  # @line L7
                split[(i, j)] = k_best
            label[(i, j)] = lab  # @line L8
    spans: List[LabeledSpan] = []
    stack = [(0, n)]
    while stack:  # @line L9
        i, j = stack.pop()
        spans.append((i, j, label[(i, j)]))
        if j - i > 1:
            k = split[(i, j)]
            stack.append((k, j))
            stack.append((i, k))
    return best[(0, n)], spans  # @line L10


def tree_score(spans: Sequence[LabeledSpan], label_scores: Dict[Span, Sequence[float]],
               span_scores: Optional[Dict[Span, float]] = None) -> float:
    """Return the score of a tree given as its labeled spans."""
    span_scores = span_scores or {}
    return sum(label_scores[(i, j)][lab] + span_scores.get((i, j), 0.0) for i, j, lab in spans)


def labeled_spans(spans: Sequence[LabeledSpan]) -> Set[LabeledSpan]:
    """Return the spans with a label other than the empty label: the n-ary tree."""
    return {(i, j, lab) for i, j, lab in spans if lab != EMPTY}


def to_tree(n: int, spans: Sequence[LabeledSpan], labels: Sequence[str]):
    """Return the n-ary tree (label, children) of the spans, with the words as
    the integers 0 to n - 1. Spans with the empty label are dropped. If the
    root span is empty, the root gets the label of index 0 as a placeholder."""
    kept = sorted(((i, j, lab) for i, j, lab in spans if lab != EMPTY or (i, j) == (0, n)),
                  key=lambda s: (s[0], -s[1]))
    if not kept or kept[0][:2] != (0, n):
        raise ValueError("the spans have no root span (0, n)")
    root = (labels[kept[0][2]], [])
    stack = [(0, n, root)]  # a chain of nested open spans
    w = 0

    def emit_words_before(end: int) -> None:
        nonlocal w
        while w < end:
            while stack[-1][1] <= w:
                stack.pop()
            stack[-1][2][1].append(w)
            w += 1

    for i, j, lab in kept[1:]:
        emit_words_before(i)
        while not (stack[-1][0] <= i and j <= stack[-1][1]):
            stack.pop()
        node = (labels[lab], [])
        stack[-1][2][1].append(node)
        stack.append((i, j, node))
    emit_words_before(n)
    return root


def top_down_greedy(n: int, label_scores: Dict[Span, Sequence[float]],
                    span_scores: Optional[Dict[Span, float]] = None) -> Tuple[float, List[LabeledSpan]]:
    """The greedy top-down decoder: pick the best label of each span and the split
    k of largest span_scores[(i, k)] + span_scores[(k, j)], from the root down.
    O(n^2 + n L) time; not optimal in general."""
    span_scores = span_scores or {}
    spans: List[LabeledSpan] = []
    stack = [(0, n)]
    while stack:
        i, j = stack.pop()
        spans.append((i, j, _best_label(label_scores[(i, j)])))
        if j - i > 1:
            k_best = max(range(i + 1, j),
                         key=lambda k: (span_scores.get((i, k), 0.0) + span_scores.get((k, j), 0.0), -k))
            stack.append((k_best, j))
            stack.append((i, k_best))
    return tree_score(spans, label_scores, span_scores), spans


def loss_augmented_scores(n: int, label_scores: Dict[Span, Sequence[float]],
                          gold: Sequence[LabeledSpan]) -> Dict[Span, List[float]]:
    """Add 1 to every label that differs from the gold label of the span.

    gold is the binarized gold tree as labeled spans. A span that is not in it
    has the gold label EMPTY. Decoding with these scores maximizes
    score + Hamming loss over the spans of the tree."""
    gold_label = {(i, j): lab for i, j, lab in gold}
    out: Dict[Span, List[float]] = {}
    for (i, j), scores in label_scores.items():
        g = gold_label.get((i, j), EMPTY)
        out[(i, j)] = [s + (0.0 if lab == g else 1.0) for lab, s in enumerate(scores)]
    return out


def hinge_loss(n: int, label_scores: Dict[Span, Sequence[float]], gold: Sequence[LabeledSpan],
               span_scores: Optional[Dict[Span, float]] = None) -> float:
    """max(0, max over trees T of [s(T) + Hamming(T, gold)] - s(gold))."""
    aug = loss_augmented_scores(n, label_scores, gold)
    top, _ = chart_parse(n, aug, span_scores)
    return max(0.0, top - tree_score(gold, label_scores, span_scores))
