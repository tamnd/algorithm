# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unigram-language-model-tokenization/. The authors are listed in prov/9PE3NB.jsonl.

"""Unigram language model tokenization of Kudo (2018).

A model is a dict from pieces (nonempty strings) to natural log probabilities.
A segmentation of a word x of n characters is a list of pieces whose
concatenation is x. Positions are fenceposts 0..n, and the piece x[i:j] is the
edge from position i to position j of the lattice.

viterbi       the most probable segmentation, in the VITERBI semiring (max, +)
forward       the log of the total probability of x, in the LOG semiring
expected_counts  the expected number of uses of each piece (forward-backward)
em_step       one EM step on a corpus of word counts
piece_loss    the drop of the corpus log likelihood when one piece is removed
train         seed, then EM and pruning until the vocabulary is small enough

Every log is the natural log. Log-space sums use nlslog.
"""

import math
from typing import Dict, List, Optional, Tuple

from nlslog import LOG, NEG_INF, VITERBI, log_sum, safe_log

Model = Dict[str, float]


def _max_len(model: Model) -> int:
    return max((len(w) for w in model), default=0)


def viterbi(x: str, model: Model) -> Tuple[float, Optional[List[str]]]:
    """Return (log P of the best segmentation, its pieces); (NEG_INF, None) if none."""
    n, m = len(x), _max_len(model)
    best = [VITERBI.zero] * (n + 1)  # @line V1
    back = [0] * (n + 1)
    best[0] = VITERBI.one  # @line V2
    for j in range(1, n + 1):  # @line V3
        for i in range(max(0, j - m), j):  # @line V4
            w = x[i:j]
            if w in model and best[i] != NEG_INF:  # @line V5
                s = VITERBI.times(best[i], model[w])
                if s > best[j]:  # @line V6
                    best[j], back[j] = s, i
    if best[n] == NEG_INF:
        return NEG_INF, None
    pieces, j = [], n  # @line V7
    while j > 0:
        pieces.append(x[back[j]:j])
        j = back[j]
    return best[n], pieces[::-1]  # @line V8


def forward(x: str, model: Model) -> List[float]:
    """alpha[j] = log of the total probability of the segmentations of x[:j]."""
    n, m = len(x), _max_len(model)
    alpha = [LOG.zero] * (n + 1)
    alpha[0] = LOG.one
    for j in range(1, n + 1):
        terms = [LOG.times(alpha[i], model[x[i:j]]) for i in range(max(0, j - m), j) if x[i:j] in model]
        alpha[j] = log_sum(terms)
    return alpha


def backward(x: str, model: Model) -> List[float]:
    """beta[i] = log of the total probability of the segmentations of x[i:]."""
    n, m = len(x), _max_len(model)
    beta = [LOG.zero] * (n + 1)
    beta[n] = LOG.one
    for i in range(n - 1, -1, -1):
        terms = [LOG.times(model[x[i:j]], beta[j]) for j in range(i + 1, min(n, i + m) + 1) if x[i:j] in model]
        beta[i] = log_sum(terms)
    return beta


def log_prob(x: str, model: Model) -> float:
    """log P(x), the log of the sum over all segmentations of the product of piece probabilities."""
    return forward(x, model)[len(x)]


def expected_counts(x: str, model: Model) -> Dict[str, float]:
    """The expected number of uses of each piece in a segmentation of x drawn from P(seg | x)."""
    n, m = len(x), _max_len(model)
    alpha, beta = forward(x, model), backward(x, model)
    z = alpha[n]
    if z == NEG_INF:
        raise ValueError("the word has no segmentation")
    out: Dict[str, float] = {}
    for i in range(n):
        for j in range(i + 1, min(n, i + m) + 1):
            w = x[i:j]
            if w in model:
                lp = alpha[i] + model[w] + beta[j] - z
                if lp != NEG_INF:
                    out[w] = out.get(w, 0.0) + math.exp(lp)
    return out


def corpus_log_likelihood(corpus: Dict[str, int], model: Model) -> float:
    """The sum over the words of count * log P(word)."""
    return math.fsum(c * log_prob(x, model) for x, c in corpus.items())


def em_step(corpus: Dict[str, int], model: Model) -> Model:
    """One EM step: p(w) = (expected count of w) / (sum of the expected counts)."""
    total: Dict[str, float] = {}  # @line E1
    for x, c in corpus.items():  # @line E2
        for w, e in expected_counts(x, model).items():  # @line E3
            total[w] = total.get(w, 0.0) + c * e  # @line E4
    z = math.fsum(total.values())  # @line E5
    return {w: safe_log(total.get(w, 0.0) / z) for w in model}  # @line E6


def remove_piece(model: Model, w: str) -> Model:
    """The model without w, renormalized so that the probabilities sum to 1."""
    rest = {v: lp for v, lp in model.items() if v != w}
    z = log_sum(rest.values())
    return {v: lp - z for v, lp in rest.items()}


def piece_loss(corpus: Dict[str, int], model: Model, w: str) -> float:
    """loss(w) = L(model) - L(model without w), with L the corpus log likelihood."""
    return corpus_log_likelihood(corpus, model) - corpus_log_likelihood(corpus, remove_piece(model, w))


def seed_vocabulary(corpus: Dict[str, int], size: int, max_piece: int) -> Dict[str, int]:
    """Every character of the corpus, plus the most frequent substrings of length 2..max_piece
    inside the words (ties to the shorter, then smaller string), up to size pieces in all."""
    freq: Dict[str, int] = {}
    for x, c in corpus.items():
        for i in range(len(x)):
            for j in range(i + 1, min(len(x), i + max_piece) + 1):
                freq[x[i:j]] = freq.get(x[i:j], 0) + c
    chars = {w: f for w, f in freq.items() if len(w) == 1}
    longer = sorted((w for w in freq if len(w) > 1), key=lambda w: (-freq[w], len(w), w))
    seed = dict(chars)
    for w in longer[: max(0, size - len(chars))]:
        seed[w] = freq[w]
    return seed


def floor_characters(model: Model) -> Model:
    """Give each character of probability 0 the smallest positive probability of the
    model, then renormalize. EM can drive a character to 0 when longer pieces always
    cover it; the floor keeps every word over the alphabet segmentable (a choice of
    this page, not a step of Kudo's paper)."""
    low = min(lp for lp in model.values() if lp != NEG_INF)
    out = {w: (low if lp == NEG_INF and len(w) == 1 else lp) for w, lp in model.items()}
    out = {w: lp for w, lp in out.items() if lp != NEG_INF}
    z = log_sum(out.values())
    return {w: lp - z for w, lp in out.items()}


def train(corpus: Dict[str, int], target: int, seed_size: int = 100, max_piece: int = 8,
          eta: float = 0.8, em_iters: int = 2) -> Model:
    """Kudo's vocabulary learning: EM, then keep the eta share of pieces with the largest loss."""
    seed = seed_vocabulary(corpus, seed_size, max_piece)  # @line T1
    z = sum(seed.values())
    model = {w: safe_log(f / z) for w, f in seed.items()}  # @line T2
    while True:  # @line T3
        for _ in range(em_iters):  # @line T4
            model = em_step(corpus, model)
        model = floor_characters(model)  # @line T5
        chars = [w for w in model if len(w) == 1]
        if len(model) <= target or len(chars) == len(model):  # @line T6
            return model
        loss = {w: piece_loss(corpus, model, w) for w in model if len(w) > 1}  # @line T7
        keep = max(target, int(eta * len(model))) - len(chars)  # @line T8
        kept = sorted(loss, key=lambda w: (-loss[w], w))[: max(0, keep)]  # @line T9
        model = {w: model[w] for w in chars + kept}  # @line T10
        z = log_sum(model.values())
        model = {w: lp - z for w, lp in model.items()}  # @line T11


def segmentations(x: str, model: Model) -> List[List[str]]:
    """All segmentations of x into pieces of the model (for tests and small examples)."""
    if not x:
        return [[]]
    out = []
    for j in range(1, len(x) + 1):
        if x[:j] in model:
            out.extend([[x[:j]] + rest for rest in segmentations(x[j:], model)])
    return out
