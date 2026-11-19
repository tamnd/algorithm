# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/span-ranking-coreference/. The authors are listed in prov/YCRS0W.jsonl.

"""The span-ranking coreference model of Lee, He, Lewis and Zettlemoyer (2017).

The network is not trained here. The mention scores s_m(span) and the pair
scores s_a(span, antecedent) are given as numbers. This file implements the
algorithm around them:

- enumerate all spans of width at most L;
- prune to at most floor(lambda n) spans by mention score, without crossing
  spans, and keep at most K antecedents per span;
- the antecedent distribution P(y | i), with the dummy antecedent EPS of
  score 0;
- the marginal log likelihood loss of the gold antecedents and its gradient
  with respect to every s_m and s_a value;
- the decoding: the best antecedent of each span, and the clusters it implies.

Spans use fencepost indices: (a, b) covers the tokens a + 1 .. b of a document
of n tokens, with 0 <= a < b <= n. Logs are natural logs.

Tie rules: pruning sorts by score, then by start, then by end; the decoder
takes the first best antecedent in the order EPS, then nearest first.
"""

import math
from typing import Dict, List, Sequence, Tuple

from nlslog import argmax, log_softmax, log_sum

Span = Tuple[int, int]
EPS = None  # the dummy antecedent: the span starts a new cluster or is not a mention


def all_spans(n: int, max_width: int) -> List[Span]:
    """All spans (a, b) with 0 <= a < b <= n and b - a <= max_width, by start, then end."""
    return [(a, b) for a in range(n) for b in range(a + 1, min(n, a + max_width) + 1)]  # @line L1


def crosses(s: Span, t: Span) -> bool:
    """True if the two spans overlap and neither contains the other."""
    (a, b), (c, d) = s, t
    return a < c < b < d or c < a < d < b


def prune(n: int, s_m: Dict[Span, float], max_width: int, lam: float) -> List[Span]:
    """Keep at most floor(lam n) spans with the highest mention scores and no crossing pair.

    Spans are taken in order of score (highest first); a span that crosses a span
    already kept is skipped. The kept spans are returned in order of start, then end.
    """
    limit = int(math.floor(lam * n + 1e-9))
    order = sorted(all_spans(n, max_width), key=lambda s: (-s_m[s], s[0], s[1]))  # @line L2
    kept: List[Span] = []
    for s in order:  # @line L3
        if len(kept) >= limit:
            break
        if not any(crosses(s, t) for t in kept):
            kept.append(s)
    return sorted(kept)  # @line L4


def candidates(spans: Sequence[Span], k: int) -> List[List[int]]:
    """For each kept span i, the indices of the up to k nearest earlier kept spans, nearest first."""
    return [list(range(i - 1, max(-1, i - 1 - k), -1)) for i in range(len(spans))]  # @line L5


def scores(spans: Sequence[Span], cands: List[List[int]], s_m: Dict[Span, float],
           s_a: Dict[Tuple[Span, Span], float]) -> List[List[float]]:
    """The scores of [EPS] + cands[i] for each span i: 0, then s_m(i) + s_m(j) + s_a(i, j)."""
    out = []
    for i, cs in enumerate(cands):
        si = spans[i]
        out.append([0.0] + [s_m[si] + s_m[spans[j]] + s_a[(si, spans[j])] for j in cs])  # @line L6
    return out


def gold_sets(spans: Sequence[Span], cands: List[List[int]],
              clusters: Sequence[Sequence[Span]]) -> List[List[int]]:
    """For each span, the positions in [EPS] + cands[i] of its gold antecedents.

    Position 0 is EPS. A span with no gold cluster, or whose gold antecedents were
    all pruned, gets [0].
    """
    cid = {}
    for c, cl in enumerate(clusters):
        for s in cl:
            cid[s] = c
    out = []
    for i, cs in enumerate(cands):
        c = cid.get(spans[i])
        g = [p + 1 for p, j in enumerate(cs) if c is not None and cid.get(spans[j]) == c]
        out.append(g if g else [0])  # @line L8
    return out


def loss_and_grad(spans, cands, s_m, s_a, clusters):
    """Return (loss, d_m, d_a): the negative marginal log likelihood and its gradient.

    loss = - sum over spans i of log sum over y in GOLD(i) of P(y | i).
    d_m maps each kept span to d loss / d s_m, and d_a each candidate pair to d loss / d s_a.
    """
    sc = scores(spans, cands, s_m, s_a)
    gold = gold_sets(spans, cands, clusters)
    loss = 0.0
    d_m = {s: 0.0 for s in spans}
    d_a = {}
    for i, row in enumerate(sc):
        logp = log_softmax(row)  # @line L7
        lg = log_sum(logp[y] for y in gold[i])
        loss -= lg  # @line L9
        gset = set(gold[i])
        for p, j in enumerate(cands[i]):
            y = p + 1
            q = math.exp(logp[y] - lg) if y in gset else 0.0  # P(y | i) given that y is gold
            g = math.exp(logp[y]) - q  # d loss / d s(i, y)
            d_a[(spans[i], spans[j])] = g
            d_m[spans[i]] += g
            d_m[spans[j]] += g
    return loss, d_m, d_a


def decode(spans, cands, s_m, s_a) -> Tuple[List, List[List[Span]]]:
    """Return (antecedent, clusters): the best antecedent of each span and the clusters.

    antecedent[i] is a span or EPS. Clusters with one span are not returned.
    """
    sc = scores(spans, cands, s_m, s_a)
    ante = []
    cluster_of: Dict[int, int] = {}
    clusters: List[List[Span]] = []
    for i, row in enumerate(sc):
        y = argmax(row)  # @line L10
        if y == 0:
            ante.append(EPS)
            continue
        j = cands[i][y - 1]
        ante.append(spans[j])
        if j not in cluster_of:  # @line L11
            cluster_of[j] = len(clusters)
            clusters.append([spans[j]])
        cluster_of[i] = cluster_of[j]
        clusters[cluster_of[j]].append(spans[i])
    return ante, clusters


def resolve(n, s_m, s_a, max_width, lam, k, clusters=None):
    """The whole pipeline: prune, list antecedents, decode, and the loss if gold clusters are given."""
    spans = prune(n, s_m, max_width, lam)
    cands = candidates(spans, k)
    ante, pred = decode(spans, cands, s_m, s_a)
    loss = None
    if clusters is not None:
        loss = loss_and_grad(spans, cands, s_m, s_a, clusters)[0]
    return spans, ante, pred, loss
