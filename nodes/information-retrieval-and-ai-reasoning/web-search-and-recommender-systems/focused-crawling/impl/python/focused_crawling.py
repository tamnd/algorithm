# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/focused-crawling/. The authors are listed in prov/CT80NW.jsonl.
"""A best-first focused crawler in the style of Chakrabarti, van den Berg and Dom (1999).

The crawler fetches pages from a frontier ordered by priority. The
priority of an unfetched URL is the largest relevance of a fetched page
that links to it (soft focus). With hard focus, the links of a page are
followed only when its relevance is at least a threshold. Seeds have
priority 1. Ties go to the smaller URL. The heap uses lazy deletion: an
entry whose priority is no longer the current one is skipped.

A small multinomial naive Bayes classifier gives a relevance score in [0, 1].
"""

import heapq
import math
from collections import Counter
from typing import Callable, Hashable, Iterable, Optional


def focused_crawl(links: Callable[[Hashable], Iterable[Hashable]], seeds: Iterable[Hashable], relevance: Callable[[Hashable], float], budget: int, hard: Optional[float] = None) -> list[Hashable]:
    """Return the fetched URLs in the order of fetching, at most `budget` of them.

    links(u) gives the out-links of page u (the fetch). relevance(u) is in [0, 1].
    hard is None for soft focus, or the threshold for hard focus.
    """
    prio: dict = {}
    heap: list = []
    for s in seeds:  # @line L1
        if s not in prio:
            prio[s] = 1.0
            heapq.heappush(heap, (-1.0, s))
    fetched: set = set()  # @line L2
    order: list = []
    while heap and len(order) < budget:  # @line L3
        p, u = heapq.heappop(heap)  # @line L4
        if u in fetched or -p < prio[u]:  # @line L5
            continue
        out = list(links(u))  # @line L6
        fetched.add(u)
        order.append(u)
        r = relevance(u)
        if hard is not None and r < hard:  # @line L7
            continue
        for v in out:  # @line L8
            if v in fetched:
                continue
            if v not in prio or r > prio[v]:  # @line L9
                prio[v] = r  # @line L10
                heapq.heappush(heap, (-r, v))
    return order  # @line L11


def harvest_rate(order: list, relevant: Callable[[Hashable], bool]) -> float:
    """The fraction of fetched pages that are relevant."""
    if not order:
        return 0.0
    return sum(1 for u in order if relevant(u)) / len(order)


class NaiveBayes:
    """Multinomial naive Bayes for two classes (1 = on topic), with add-one smoothing."""

    def __init__(self, docs: list[list[str]], labels: list[int]) -> None:
        if set(labels) != {0, 1}:
            raise ValueError("need examples of both classes")
        self.count = [Counter(), Counter()]
        ndocs = [0, 0]
        for d, y in zip(docs, labels):
            self.count[y].update(d)
            ndocs[y] += 1
        self.vocab = set(self.count[0]) | set(self.count[1])
        self.total = [sum(c.values()) for c in self.count]
        self.prior = [math.log(n / len(docs)) for n in ndocs]

    def log_score(self, doc: list[str], y: int) -> float:
        v = len(self.vocab)
        s = self.prior[y]
        for w in doc:
            if w in self.vocab:  # words never seen in training are ignored
                s += math.log((self.count[y][w] + 1) / (self.total[y] + v))
        return s

    def prob(self, doc: list[str]) -> float:
        """P(on topic | doc) under the model."""
        d = self.log_score(doc, 0) - self.log_score(doc, 1)
        if d > 0:
            e = math.exp(-d)
            return e / (1.0 + e)
        return 1.0 / (1.0 + math.exp(d))
