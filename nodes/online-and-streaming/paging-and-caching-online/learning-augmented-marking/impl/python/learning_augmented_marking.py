# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-augmented-marking/. The authors are listed in prov/9E8GB1.jsonl.

import random
from fractions import Fraction
from typing import Dict, Hashable, List, Optional, Sequence, Tuple

Page = Hashable


def harmonic(k: int) -> Fraction:
    return sum((Fraction(1, j) for j in range(1, k + 1)), Fraction(0))


def next_arrivals(requests: Sequence[Page]) -> List[int]:
    """y[i] is the next time after i at which requests[i] comes again, or len(requests) if never."""
    n = len(requests)
    y, last = [n] * n, {}
    for i in range(n - 1, -1, -1):
        y[i] = last.get(requests[i], n)
        last[requests[i]] = i
    return y


def prediction_error(requests: Sequence[Page], predictions: Sequence[float]) -> float:
    """The absolute loss eta: the sum over all requests of |predicted - actual next arrival|."""
    return sum(abs(h - y) for h, y in zip(predictions, next_arrivals(requests)))


def predictive_marker(requests: Sequence[Page], k: int, predictions: Sequence[float], rng: Optional[random.Random] = None) -> Tuple[int, List[Dict]]:
    """Predictive Marker of Lykouris and Vassilvitskii (2018) with an empty start cache.

    predictions[i] is the predicted next arrival time of requests[i].
    Returns (misses, log), where each log entry describes one request.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    if len(predictions) != len(requests):
        raise ValueError("one prediction is needed for each request")
    rng = rng or random.Random(0)
    hk = harmonic(k)
    cache: Dict[Page, None] = {}  # resident pages, in load order
    marked: set = set()
    prev: set = set()  # the pages of the previous phase
    chain_of: Dict[Page, int] = {}  # chain of each page evicted in this phase
    length: List[int] = []  # chain lengths in this phase
    pred: Dict[Page, float] = {}
    misses, phase, log = 0, 1, []  # @line L1
    for i, x in enumerate(requests):  # @line L2
        pred[x] = predictions[i]  # @line L3
        entry = {"page": x, "phase": phase, "hit": True, "kind": "hit", "evict": None, "how": None, "chain": None}
        if x in cache:  # @line L4
            marked.add(x)
            log.append(entry)
            continue
        misses += 1  # @line L5
        entry["hit"] = False
        if len(cache) == k and len(marked) == k:  # @line L6
            phase += 1
            prev, marked, chain_of, length = set(marked), set(), {}, []
            entry["phase"] = phase
        if len(cache) < k:  # @line L7
            cache[x] = None
            marked.add(x)
            entry["kind"] = "fill"
            log.append(entry)
            continue
        if x not in prev:  # @line L8
            length.append(1)
            ell = len(length) - 1
            entry["kind"] = "clean"
        else:  # @line L9
            ell = chain_of[x]
            length[ell] += 1
            entry["kind"] = "stale"
        unmarked = [p for p in cache if p not in marked]
        if length[ell] <= hk:  # @line L10
            y = max(unmarked, key=lambda p: pred[p])
            entry["how"] = "pred"
        else:  # @line L11
            y = rng.choice(unmarked)
            entry["how"] = "random"
        del cache[y]  # @line L12
        chain_of[y] = ell
        cache[x] = None
        marked.add(x)
        entry["evict"], entry["chain"] = y, ell
        log.append(entry)
    return misses, log  # @line L13
