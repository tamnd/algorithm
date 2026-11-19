# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stack-decoding/. The authors are listed in prov/A0NEW4.jsonl.

"""Stack decoding: best-first (A*) search over partial word sequences.

The model is the one of the time-synchronous beam search page: a lexicon
word -> tuple of phones, one emitting state per phone with a self loop (log
probability loop) and a forward move (log probability fwd, also used for the
word exit), emission scores emit[t][phone], and a bigram lm[(v, w)] in log
probability. Scores are log probabilities, higher is better. The score of a
word sequence with a segmentation is

    sum of emissions + transitions + sum over words of (lm_weight * lm + ip)
  + lm_weight * lm(last word, </s>).

A partial hypothesis is (words, t): the words cover frames 0..t-1 exactly. Its
score g is the best score of that prefix. The search pops the hypothesis with
the largest g + h(t), where h(t) is an upper bound on the score of frames
t..T-1:

    h(t) = sum over u >= t of max_phone emit[u][phone] + (T - t) * max(0, ip).

This bound is valid (admissible) when loop <= 0, fwd <= 0, lm <= 0 and
lm_weight >= 0, since then every transition and language model term is at
most 0 and at most T - t more words fit. It is also consistent: extending by
one word never raises g + h. So the first complete hypothesis that is popped
is the best one, and a hypothesis (last word, t) can be closed after its first
pop, because its future depends only on the last word and t.

The search is not limited to a fixed number of words. A stack limit max_stack
drops the worst entries and makes the search inexact; so does a heuristic that
is not an upper bound.
"""

import heapq
import itertools
import math
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from nlslog import NEG_INF

BOS = "<s>"
EOS = "</s>"


def word_scores(phones: Sequence[str], emit: Sequence[Dict[str, float]], t: int, loop: float, fwd: float) -> Dict[int, float]:
    """Return {t1: best log score of the word occupying frames t..t1-1, exit included}."""
    T = len(emit)
    k = len(phones)
    alpha = [NEG_INF] * k
    alpha[0] = emit[t][phones[0]]
    out: Dict[int, float] = {}
    for u in range(t, T):
        if u > t:
            new = [NEG_INF] * k
            for j in range(k):
                best = alpha[j] + loop
                if j > 0:
                    best = max(best, alpha[j - 1] + fwd)
                new[j] = best + emit[u][phones[j]]
            alpha = new
        if alpha[k - 1] > NEG_INF:
            out[u + 1] = alpha[k - 1] + fwd
    return out


def default_heuristic(emit: Sequence[Dict[str, float]], ip: float) -> List[float]:
    """Return h[t] for t = 0..T: the admissible bound of the module docstring."""
    T = len(emit)
    h = [0.0] * (T + 1)
    for t in range(T - 1, -1, -1):
        h[t] = h[t + 1] + max(emit[t].values()) + max(0.0, ip)
    return h


def decode(
    lexicon: Dict[str, Sequence[str]],
    lm: Dict[Tuple[str, str], float],
    emit: Sequence[Dict[str, float]],
    lm_weight: float = 1.0,
    ip: float = 0.0,
    loop: float = math.log(0.5),
    fwd: float = math.log(0.5),
    heuristic: Optional[Callable[[int], float]] = None,
    max_stack: Optional[int] = None,
):
    """Return (words, ends, score, pops): the best hypothesis found and the number of pops.

    ends[i] is the last frame of words[i]. Return ([], [], -inf, pops) if no
    complete hypothesis is found.
    """
    T = len(emit)
    if heuristic is None:
        table = default_heuristic(emit, ip)
        heuristic = table.__getitem__
    memo: Dict[Tuple[str, int], Dict[int, float]] = {}

    def seg(w: str, t: int) -> Dict[int, float]:
        if (w, t) not in memo:
            memo[(w, t)] = word_scores(lexicon[w], emit, t, loop, fwd)
        return memo[(w, t)]

    counter = itertools.count()
    # Entries: (-priority, order, complete, g, words, ends)
    stack: List = [(-heuristic(0), next(counter), False, 0.0, (), ())]  # @line L1
    closed = set()
    pops = 0
    while stack:  # @line L2
        _, _, complete, g, words, ends = heapq.heappop(stack)  # @line L3
        pops += 1
        if complete:  # @line L4
            return list(words), list(ends), g, pops
        t = ends[-1] + 1 if ends else 0
        last = words[-1] if words else BOS
        if (last, t) in closed:  # @line L5
            continue
        closed.add((last, t))
        for w in sorted(lexicon):  # @line L6
            lm_w = lm.get((last, w), NEG_INF)
            if lm_w == NEG_INF:
                continue
            for t1, s in seg(w, t).items():
                g1 = g + s + lm_weight * lm_w + ip
                if t1 == T:  # @line L7
                    end = lm.get((w, EOS), NEG_INF)
                    if end > NEG_INF:
                        total = g1 + lm_weight * end
                        heapq.heappush(stack, (-total, next(counter), True, total, words + (w,), ends + (t1 - 1,)))
                elif (w, t1) not in closed:  # @line L8
                    heapq.heappush(stack, (-(g1 + heuristic(t1)), next(counter), False, g1, words + (w,), ends + (t1 - 1,)))
        if max_stack is not None and len(stack) > max_stack:  # @line L9
            stack = heapq.nsmallest(max_stack, stack)
            heapq.heapify(stack)
    return [], [], NEG_INF, pops  # @line L10
