# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-marginal-relevance/. The authors are listed in prov/2ZKYCZ.jsonl.
"""Maximal marginal relevance (Carbonell and Goldstein, 1998).

Greedy selection of k items from a candidate list. At each step the item
with the largest

    lam * rel(d) - (1 - lam) * max over chosen j of sim(d, j)

is added; for the first pick the maximum over the empty set is taken as 0.
Ties go to the smaller id. The largest similarity of each remaining item
to the chosen set is kept up to date, so each step costs one similarity
per remaining item.
"""


def mmr_steps(candidates, rel, sim, lam, k):
    """Return the list of (id, MMR score at the time it was picked)."""
    if not 0.0 <= lam <= 1.0:
        raise ValueError("lam must lie in [0, 1]")
    remaining = sorted(set(candidates))  # @line L1
    chosen = []  # @line L2
    closest = {d: 0.0 for d in remaining}  # @line L3
    while remaining and len(chosen) < k:  # @line L4
        best, best_score = None, None
        for d in remaining:  # @line L5
            score = lam * rel[d] - (1.0 - lam) * closest[d]  # @line L6
            if best_score is None or score > best_score:  # ties keep the smaller id
                best, best_score = d, score
        chosen.append((best, best_score))  # @line L7
        remaining.remove(best)
        for d in remaining:  # @line L8
            s = sim(d, best)
            if len(chosen) == 1 or s > closest[d]:
                closest[d] = s  # @line L9
    return chosen  # @line L10


def mmr(candidates, rel, sim, lam, k):
    """Return the ids that MMR picks, in order."""
    return [d for d, _ in mmr_steps(candidates, rel, sim, lam, k)]
