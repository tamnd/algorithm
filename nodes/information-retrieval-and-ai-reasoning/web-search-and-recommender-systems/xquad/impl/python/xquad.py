# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xquad/. The authors are listed in prov/ZHZBK5.jsonl.
"""xQuAD (Santos, Macdonald and Ounis, 2010).

Given the candidates R of a query q, their relevance P(d | q), the aspects
(sub-queries) q_i of q with importance P(q_i | q), and the coverage
P(d | q_i) of each candidate for each aspect, xQuAD builds the list S by
repeatedly taking the candidate with the largest

    (1 - lam) * P(d | q) + lam * sum over i of P(q_i | q) P(d | q_i) * prod over d_j in S of (1 - P(d_j | q_i)).

The product, the probability that no chosen document covers aspect q_i,
is kept per aspect and updated after each pick. Ties go to the smaller id.
"""


def _check(docs, rel, p_aspect, cover, lam):
    if not 0.0 <= lam <= 1.0:
        raise ValueError("lam must lie in [0, 1]")
    for d in docs:
        if d not in rel:
            raise ValueError("every candidate needs a relevance score")
        for a, v in cover.get(d, {}).items():
            if a not in p_aspect or not 0.0 <= v <= 1.0:
                raise ValueError("P(d | q_i) must lie in [0, 1] for a known aspect")


def xquad_steps(docs, rel, p_aspect, cover, lam, k):
    """Return the list of (document, score at the time it was picked)."""
    _check(docs, rel, p_aspect, cover, lam)
    novel = {a: 1.0 for a in p_aspect}  # @line L1
    rest = sorted(set(docs))
    chosen = []  # @line L2
    while rest and len(chosen) < k:  # @line L3
        best, best_score = None, None
        for d in rest:  # @line L4
            div = sum(p_aspect[a] * v * novel[a] for a, v in cover.get(d, {}).items())
            score = (1.0 - lam) * rel[d] + lam * div  # @line L5
            if best_score is None or score > best_score:  # ties keep the smaller id
                best, best_score = d, score
        chosen.append((best, best_score))  # @line L6
        rest.remove(best)
        for a, v in cover.get(best, {}).items():  # @line L7
            novel[a] *= 1.0 - v  # @line L8
    return chosen  # @line L9


def xquad(docs, rel, p_aspect, cover, lam, k):
    """Return the documents that xQuAD picks, in order."""
    return [d for d, _ in xquad_steps(docs, rel, p_aspect, cover, lam, k)]
