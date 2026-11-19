# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luhn-summarization/. The authors are listed in prov/JX112C.jsonl.

"""Luhn's significance factor and sentence extraction (Luhn 1958).

The input is a document as a list of sentences, each a list of str tokens.
The module does no sentence splitting and no tokenization.

A word is significant when its key (by default the lower-cased word) is not a
stop word and its frequency in the document is between the two cut offs low
and high, both inclusive. In a sentence, a cluster is a maximal run of
significant words in which two neighbours have at most `gap` non-significant
words between them. The score of a cluster is (significant words)^2 divided by
the length of the cluster from its first to its last significant word, and the
score of a sentence is the largest score of its clusters (0 with none).

Luhn's own rule to merge words with the same beginning is replaced by the
`key` function; pass a stemmer there to get a similar effect. Scores are exact
Fractions.
"""

from collections import Counter
from fractions import Fraction
from typing import Callable, Iterable, List, Sequence, Set, Tuple

Sentence = Sequence[str]


def word_frequencies(
    doc: Sequence[Sentence],
    stop: Iterable[str] = (),
    key: Callable[[str], str] = str.lower,
) -> Counter:
    """Count the keys of all words of the document that are not stop words."""
    stop_keys = {key(w) for w in stop}
    f: Counter = Counter()  # @line L1
    for s in doc:
        for w in s:
            k = key(w)
            if k not in stop_keys:
                f[k] += 1  # @line L2
    return f


def significant_words(
    doc: Sequence[Sentence],
    low: int,
    high: int,
    stop: Iterable[str] = (),
    key: Callable[[str], str] = str.lower,
) -> Set[str]:
    """Return the keys whose frequency is between low and high, inclusive."""
    f = word_frequencies(doc, stop, key)
    return {v for v, c in f.items() if low <= c <= high}  # @line L3


def clusters(
    sentence: Sentence,
    sig: Set[str],
    gap: int = 4,
    key: Callable[[str], str] = str.lower,
) -> List[Tuple[int, int, int]]:
    """Return the clusters of a sentence as (first position, last position, count)."""
    pos = [i for i, w in enumerate(sentence) if key(w) in sig]  # @line L5
    out: List[Tuple[int, int, int]] = []
    a = 0  # @line L6
    for b in range(len(pos)):  # @line L7
        if b == len(pos) - 1 or pos[b + 1] - pos[b] - 1 > gap:  # @line L8
            out.append((pos[a], pos[b], b - a + 1))
            a = b + 1  # @line L11
    return out


def sentence_score(
    sentence: Sentence,
    sig: Set[str],
    gap: int = 4,
    key: Callable[[str], str] = str.lower,
) -> Fraction:
    """Return the significance factor of one sentence: the best cluster score."""
    best = Fraction(0)  # @line L6
    for first, last, m in clusters(sentence, sig, gap, key):
        length = last - first + 1  # @line L9
        best = max(best, Fraction(m * m, length))  # @line L10
    return best


def luhn_scores(
    doc: Sequence[Sentence],
    low: int,
    high: int,
    stop: Iterable[str] = (),
    gap: int = 4,
    key: Callable[[str], str] = str.lower,
) -> List[Fraction]:
    """Return the significance factor of every sentence of the document."""
    sig = significant_words(doc, low, high, stop, key)
    return [sentence_score(s, sig, gap, key) for s in doc]  # @line L4


def luhn_summarize(
    doc: Sequence[Sentence],
    k: int,
    low: int,
    high: int,
    stop: Iterable[str] = (),
    gap: int = 4,
    key: Callable[[str], str] = str.lower,
) -> List[int]:
    """Return the indices of the k sentences with the highest scores, in document order.

    Ties go to the earlier sentence. Sentences with score 0 are never chosen, so
    the result can have fewer than k indices.
    """
    scores = luhn_scores(doc, low, high, stop, gap, key)
    order = sorted(range(len(doc)), key=lambda i: (-scores[i], i))
    chosen = [i for i in order[:k] if scores[i] > 0]
    return sorted(chosen)  # @line L12


def luhn_above(
    doc: Sequence[Sentence],
    cutoff: Fraction,
    low: int,
    high: int,
    stop: Iterable[str] = (),
    gap: int = 4,
    key: Callable[[str], str] = str.lower,
) -> List[int]:
    """Return the indices of the sentences whose score is at least cutoff (Luhn's rule)."""
    scores = luhn_scores(doc, low, high, stop, gap, key)
    return [i for i, x in enumerate(scores) if x >= cutoff]
