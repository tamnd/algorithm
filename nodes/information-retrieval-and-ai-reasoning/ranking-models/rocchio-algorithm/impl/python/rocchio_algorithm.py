# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rocchio-algorithm/. The authors are listed in prov/SMAEPR.jsonl.

from typing import Any, Hashable, Mapping, Sequence

Vector = Mapping[Hashable, float]


def centroid(docs: Sequence[Vector]) -> dict[Any, float]:
    """Return the mean of sparse vectors, as a dict of the nonzero coordinates."""
    out: dict[Any, float] = {}
    for v in docs:
        for t, w in v.items():
            out[t] = out.get(t, 0) + w / len(docs)
    return out


def rocchio(
    query: Vector,
    relevant: Sequence[Vector],
    nonrelevant: Sequence[Vector],
    alpha: float = 1.0,
    beta: float = 0.75,
    gamma: float = 0.15,
    clamp: bool = True,
) -> dict[Any, float]:
    """Return alpha q + beta centroid(relevant) - gamma centroid(nonrelevant).

    The vectors are sparse dicts from terms to weights. An empty set adds nothing. With
    clamp=True, terms whose weight is 0 or less are dropped from the new query.
    """
    new = {t: alpha * w for t, w in query.items()}  # @line L1
    if relevant:  # @line L2
        for t, w in centroid(relevant).items():
            new[t] = new.get(t, 0) + beta * w
    if nonrelevant:  # @line L3
        for t, w in centroid(nonrelevant).items():
            new[t] = new.get(t, 0) - gamma * w
    if clamp:  # @line L4
        new = {t: w for t, w in new.items() if w > 0}
    return new  # @line L5


def top_terms(query: Vector, m: int) -> dict[Any, float]:
    """Keep the m terms of largest weight, ties by term."""
    keep = sorted(query, key=lambda t: (-query[t], t))[:m]
    return {t: query[t] for t in keep}
