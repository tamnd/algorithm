# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cori-resource-selection/. The authors are listed in prov/47WHK1.jsonl.
"""CORI resource selection (Callan, Lu and Croft 1995; the form of Callan 2000).

A collection is described by df_i(t), the number of its documents that
contain t, and cw_i, its number of tokens. For a query term t and
collection i, with K collections of which c(t) contain t:

    T = df / (df + 50 + 150 * cw_i / avg_cw)
    I = log((K + 0.5) / c(t)) / log(K + 1.0)
    p(t | i) = b + (1 - b) * T * I,   b = 0.4

The score of a collection is the mean of p(t | i) over the query terms.
The constants 50, 150 and 0.4 were fitted on test data. A term that no
collection contains gives every collection the default belief b.
The ratio of two logarithms does not depend on their base.
"""

import math
from typing import Iterable, Sequence

DF_BASE = 50.0
DF_SIZE = 150.0
B = 0.4


class Description:
    """The statistics that the broker keeps for one collection."""

    def __init__(self, docs: Iterable[Sequence[str]]) -> None:
        self.df: dict[str, int] = {}
        self.cw = 0
        for toks in docs:
            self.cw += len(toks)  # @line L1
            for t in set(toks):
                self.df[t] = self.df.get(t, 0) + 1


def cori_scores(query: Sequence[str], descs: Sequence[Description], b: float = B, df_base: float = DF_BASE, df_size: float = DF_SIZE) -> list[float]:
    """The CORI belief of each collection for the query (a bag of terms, repeats count)."""
    if not query:
        raise ValueError("empty query")
    k = len(descs)
    if k == 0:
        return []
    avg_cw = sum(d.cw for d in descs) / k  # @line L2
    if avg_cw == 0:
        raise ValueError("all collections are empty")
    c = {t: sum(1 for d in descs if d.df.get(t, 0) > 0) for t in set(query)}  # @line L3
    scores = []
    for d in descs:  # @line L4
        s = 0.0  # @line L5
        for t in query:  # @line L6
            if c[t] == 0:  # @line L7
                s += b
                continue
            df = d.df.get(t, 0)
            tt = df / (df + df_base + df_size * d.cw / avg_cw)  # @line L8
            ii = math.log((k + 0.5) / c[t]) / math.log(k + 1.0)  # @line L9
            s += b + (1 - b) * tt * ii  # @line L10
        scores.append(s / len(query))  # @line L11
    return scores


def cori_select(query: Sequence[str], descs: Sequence[Description], n: int, b: float = B) -> list[int]:
    """Indexes of the n collections with the highest belief; ties go to the smaller index."""
    s = cori_scores(query, descs, b)
    return sorted(range(len(descs)), key=lambda i: (-s[i], i))[:n]  # @line L12
