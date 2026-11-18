# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morfessor/. The authors are listed in prov/TM8W3C.jsonl.

"""Morfessor Baseline search of Creutz and Lagus, with the two-part cost of 2002.

The corpus is a dict from word types to counts. An analysis gives each word
type a list of morphs whose concatenation is the word. The morph counts c(m)
are the sums of the word counts over the uses of m, and C is their total.

    cost = sum over morph tokens of -ln(c(m) / C)  +  K * (sum over morph types of len(m))
         = C ln C - sum_m c(m) ln c(m)            +  K * (total length of the lexicon)

All logs are natural logs, so the cost is in nats. K is the cost of one
character of the lexicon: 5 bits, that is 5 ln 2 nats, by default.

The search reprocesses the word types in a random order. For each word it
removes the word's morphs, tries the word whole and every split into two
parts, takes the cheapest, and recurses on the two parts. If the new analysis
of the word costs more than the old one, the old one is put back, so the cost
never rises. The search is greedy and finds a local optimum.
"""

import math
import random
from typing import Dict, List, Optional, Tuple

from nlslog import safe_log

K_DEFAULT = 5 * math.log(2)


def _xlogx(c: int) -> float:
    return c * safe_log(c) if c > 0 else 0.0


def cost_of(corpus: Dict[str, int], analysis: Dict[str, List[str]], k: float = K_DEFAULT) -> float:
    """The two-part cost of an analysis, computed from scratch."""
    counts: Dict[str, int] = {}
    for w, f in corpus.items():
        for m in analysis[w]:
            counts[m] = counts.get(m, 0) + f
    total = sum(counts.values())
    data = _xlogx(total) - math.fsum(_xlogx(c) for c in counts.values())
    return data + k * sum(len(m) for m in counts)


class Model:
    """Morph counts with the cost kept up to date."""

    def __init__(self, k: float = K_DEFAULT):
        self.k = k
        self.counts: Dict[str, int] = {}
        self.total = 0
        self.sum_xlogx = 0.0
        self.lexicon_chars = 0

    def add(self, m: str, d: int) -> None:
        """Add d (which may be negative) to the count of the morph m."""
        old = self.counts.get(m, 0)
        new = old + d
        if new < 0:
            raise ValueError("negative morph count")
        self.sum_xlogx += _xlogx(new) - _xlogx(old)
        self.total += d
        if old == 0 and new > 0:
            self.lexicon_chars += len(m)
        if old > 0 and new == 0:
            self.lexicon_chars -= len(m)
        if new == 0:
            self.counts.pop(m, None)
        else:
            self.counts[m] = new

    def cost(self) -> float:
        return _xlogx(self.total) - self.sum_xlogx + self.k * self.lexicon_chars

    def cost_with(self, morphs: List[str], f: int) -> float:
        """The cost if each morph of the list were added f times."""
        for m in morphs:
            self.add(m, f)
        c = self.cost()
        for m in morphs:
            self.add(m, -f)
        return c


def resplit(model: Model, s: str, f: int) -> List[str]:
    """Analyze s (with count f) by recursive binary splitting; add its morphs to the model."""
    best, cut = model.cost_with([s], f), None  # @line R1
    for i in range(1, len(s)):  # @line R2
        c = model.cost_with([s[:i], s[i:]], f)  # @line R3
        if c < best - 1e-12:  # @line R4
            best, cut = c, i
    if cut is None:  # @line R5
        model.add(s, f)
        return [s]
    left = resplit(model, s[:cut], f)  # @line R6
    return left + resplit(model, s[cut:], f)  # @line R7


def morfessor(corpus: Dict[str, int], rng: random.Random, k: float = K_DEFAULT,
              tol: float = 1e-9, max_epochs: int = 50,
              start: Optional[Dict[str, List[str]]] = None) -> Tuple[Dict[str, List[str]], List[float]]:
    """Return the analysis and the cost after each epoch (the first value is the start)."""
    model = Model(k)
    analysis = {w: list(start[w]) if start else [w] for w in corpus}  # @line M1
    for w, f in corpus.items():
        for m in analysis[w]:
            model.add(m, f)
    trace = [cost_of(corpus, analysis, k)]
    for _ in range(max_epochs):  # @line M2
        order = sorted(corpus)
        rng.shuffle(order)
        for w in order:  # @line M3
            f = corpus[w]
            before = model.cost()
            for m in analysis[w]:  # @line M4
                model.add(m, -f)
            new = resplit(model, w, f)  # @line M5
            if model.cost() > before + 1e-12:  # @line M6
                for m in new:
                    model.add(m, -f)
                for m in analysis[w]:
                    model.add(m, f)
            else:
                analysis[w] = new
        trace.append(cost_of(corpus, analysis, k))  # @line M7
        if trace[-2] - trace[-1] < tol:
            break
    return analysis, trace  # @line M8


def segment(word: str, lexicon: Dict[str, int]) -> List[str]:
    """Segment a new word with a learned lexicon (morph counts): the most probable
    split into known morphs by a Viterbi pass in the TROPICAL semiring over
    costs -ln(c(m) / C); a word with no such split is returned whole."""
    total = sum(lexicon.values())
    n = len(word)
    best = [math.inf] * (n + 1)
    back = [0] * (n + 1)
    best[0] = 0.0
    for j in range(1, n + 1):
        for i in range(j):
            m = word[i:j]
            if m in lexicon and best[i] < math.inf:
                c = best[i] - safe_log(lexicon[m] / total)
                if c < best[j]:
                    best[j], back[j] = c, i
    if best[n] == math.inf:
        return [word]
    out, j = [], n
    while j > 0:
        out.append(word[back[j]:j])
        j = back[j]
    return out[::-1]


def lexicon_of(corpus: Dict[str, int], analysis: Dict[str, List[str]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for w, f in corpus.items():
        for m in analysis[w]:
            counts[m] = counts.get(m, 0) + f
    return counts
