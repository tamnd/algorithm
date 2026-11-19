# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/textrank/. The authors are listed in prov/FCW45A.jsonl.

"""TextRank of Mihalcea and Tarau (2004): sentence extraction and keywords.

Sentences are lists of str tokens; the module does no tokenization, no stop
word removal and no part of speech tagging. Words are compared after lower
casing.

The ranking is the weighted PageRank of the paper,

    WS(i) = (1 - d) + d * sum over j of w[j][i] / out(j) * WS(j),

with out(j) the sum of the weights on the edges of j, d = 0.85 and all scores
starting at 1. A vertex with no edges keeps the score 1 - d. The iteration
stops when the 1-norm of the change is below eps.

Sentence similarity: the number of distinct words that two sentences share,
divided by log |S_i| + log |S_j| (natural logarithm, lengths in tokens). The
weight is 0 when the sentences share no word or when the denominator is not
positive (two one-word sentences, or an empty sentence).
"""

import math
from typing import Callable, Dict, List, Sequence, Tuple

Matrix = List[List[float]]


def overlap_similarity(a: Sequence[str], b: Sequence[str]) -> float:
    """Return |a and b| / (log |a| + log |b|), or 0 where it is not defined."""
    if not a or not b:
        return 0.0
    common = len({w.lower() for w in a} & {w.lower() for w in b})
    den = math.log(len(a)) + math.log(len(b))
    if common == 0 or den <= 0.0:
        return 0.0
    return common / den


def similarity_matrix(sentences: Sequence[Sequence[str]]) -> Matrix:
    """Return the symmetric weight matrix of the sentence graph, with a zero diagonal."""
    n = len(sentences)
    w = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w[i][j] = w[j][i] = overlap_similarity(sentences[i], sentences[j])  # @line L1
    return w


def weighted_pagerank(
    w: Matrix, d: float = 0.85, eps: float = 1e-4, max_iter: int = 1000
) -> Tuple[List[float], int]:
    """Iterate the weighted PageRank of TextRank on the weight matrix w.

    w[j][i] is the weight of the edge from j to i. Returns the scores and the
    number of iterations.
    """
    n = len(w)
    out = [sum(row) for row in w]  # @line L2
    ws = [1.0] * n  # @line L3
    it = 0
    while it < max_iter:  # @line L4
        it += 1
        new = []
        for i in range(n):
            s = 0.0
            for j in range(n):
                if w[j][i] > 0.0:
                    s += w[j][i] / out[j] * ws[j]
            new.append((1.0 - d) + d * s)  # @line L5
        delta = sum(abs(x - y) for x, y in zip(new, ws))  # @line L6
        ws = new  # @line L7
        if delta < eps:  # @line L8
            break
    return ws, it


def textrank_scores(
    sentences: Sequence[Sequence[str]], d: float = 0.85, eps: float = 1e-4
) -> List[float]:
    """Return the TextRank score of every sentence."""
    return weighted_pagerank(similarity_matrix(sentences), d, eps)[0]


def textrank_summarize(
    sentences: Sequence[Sequence[str]], k: int, d: float = 0.85, eps: float = 1e-4
) -> List[int]:
    """Return the indices of the k best sentences in document order (ties to the earlier one)."""
    ws = textrank_scores(sentences, d, eps)
    order = sorted(range(len(sentences)), key=lambda i: (-ws[i], i))
    return sorted(order[:k])  # @line L9


def cooccurrence_graph(
    tokens: Sequence[str], is_candidate: Callable[[str], bool], window: int = 2
) -> Tuple[List[str], Matrix]:
    """Build the unweighted keyword graph.

    The candidates are the tokens that pass the filter, lower cased, in order.
    Two candidates are joined when they occur fewer than `window` positions
    apart in that filtered sequence (window = 2 joins neighbours).
    """
    seq = [t.lower() for t in tokens if is_candidate(t)]
    words: List[str] = []
    index: Dict[str, int] = {}
    for t in seq:
        if t not in index:
            index[t] = len(words)
            words.append(t)
    n = len(words)
    w = [[0.0] * n for _ in range(n)]
    for i in range(len(seq)):
        for j in range(i + 1, min(i + window, len(seq))):
            a, b = index[seq[i]], index[seq[j]]
            if a != b:
                w[a][b] = w[b][a] = 1.0
    return words, w


def textrank_keywords(
    tokens: Sequence[str],
    is_candidate: Callable[[str], bool],
    window: int = 2,
    d: float = 0.85,
    eps: float = 1e-4,
) -> List[str]:
    """Return the keywords of a text: the top third of the vertices, with adjacent ones joined.

    The top T = max(1, n // 3) vertices are marked in the text, and each maximal
    run of adjacent marked tokens becomes one keyword. Keywords are returned in
    order of first occurrence, without repeats.
    """
    words, w = cooccurrence_graph(tokens, is_candidate, window)
    if not words:
        return []
    ws, _ = weighted_pagerank(w, d, eps)
    t = max(1, len(words) // 3)
    order = sorted(range(len(words)), key=lambda i: (-ws[i], i))
    top = {words[i] for i in order[:t]}
    out: List[str] = []
    run: List[str] = []
    for tok in list(tokens) + [""]:
        low = tok.lower()
        if tok and is_candidate(tok) and low in top:
            run.append(low)
        else:
            if run:
                phrase = " ".join(run)
                if phrase not in out:
                    out.append(phrase)
            run = []
    return out
