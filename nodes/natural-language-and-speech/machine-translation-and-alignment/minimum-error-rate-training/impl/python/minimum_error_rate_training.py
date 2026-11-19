# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-error-rate-training/. The authors are listed in prov/P668TA.jsonl.

"""Minimum error rate training (Och 2003): exact line search on n-best lists.

An n-best list holds, for each tuning sentence, candidates (h, stats): h is the
feature vector of the log-linear model and stats is a tuple of sufficient
statistics of the metric (for BLEU: the clipped n-gram matches, the candidate
n-gram counts, the candidate length and the reference length). The metric of a
corpus is metric(sum of the stats of the chosen candidates), to be maximized.

Along the line w + gamma d, the model score of each candidate is the linear
function (w . h) + gamma (d . h). The decoder picks the highest line, so the
chosen candidate of a sentence changes only where the upper envelope of its
lines changes. line_search finds these points exactly, sweeps them in order,
and returns a gamma inside the best interval.
"""

import math
from collections import Counter
from typing import Callable, Optional, Sequence

Cand = tuple[Sequence[float], tuple]
Metric = Callable[[tuple], float]


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def add(a: tuple, b: tuple, sign: int = 1) -> tuple:
    return tuple(x + sign * y for x, y in zip(a, b))


def upper_envelope(lines: list[tuple[float, float, int]]) -> list[tuple[float, int]]:
    """lines: (slope, intercept, index). Returns [(gamma_start, index), ...] with
    gamma_start increasing; index is the highest line from gamma_start to the
    next start. The first start is -inf. Among identical lines the smallest
    index wins."""
    order = sorted(lines, key=lambda x: (x[0], x[1], -x[2]))  # @line U1
    hull: list[tuple[float, float, int, float]] = []  # @line U2
    for k, (b, a, c) in enumerate(order):  # @line U3
        if k + 1 < len(order) and order[k + 1][0] == b:
            continue  # a later line has the same slope and is at least as high
        start = -math.inf
        while hull:  # @line U4
            b0, a0, _, s0 = hull[-1]
            x = (a0 - a) / (b - b0)  # @line U5
            if x <= s0:  # @line U6
                hull.pop()
            else:
                start = x
                break
        hull.append((b, a, c, start))  # @line U7
    return [(s, c) for _, _, c, s in hull]  # @line U8


def line_search(
    w: Sequence[float], d: Sequence[float], nbest: list[list[Cand]], metric: Metric
) -> tuple[float, float]:
    """Return (gamma, value): a step gamma inside an interval where the metric of
    the choices on the line w + gamma d is largest, and that largest value."""
    events = []  # @line L1
    total: Optional[tuple] = None
    for i, cands in enumerate(nbest):  # @line L2
        lines = [(dot(d, h), dot(w, h), c) for c, (h, _) in enumerate(cands)]  # @line L3
        env = upper_envelope(lines)  # @line L4
        first = cands[env[0][1]][1]  # @line L5
        total = first if total is None else add(total, first)
        for (_, c_prev), (g, c) in zip(env, env[1:]):  # @line L6
            events.append((g, add(cands[c][1], cands[c_prev][1], -1)))
    assert total is not None
    events.sort(key=lambda e: e[0])  # @line L7
    best = metric(total)  # @line L8
    best_gamma = events[0][0] - 1.0 if events else 0.0
    k = 0
    while k < len(events):  # @line L9
        g = events[k][0]
        while k < len(events) and events[k][0] == g:
            total = add(total, events[k][1])
            k += 1
        nxt = events[k][0] if k < len(events) else None
        value = metric(total)
        if value > best:
            best = value
            best_gamma = g + 1.0 if nxt is None else (g + nxt) / 2
    return best_gamma, best  # @line L10


def choose(w: Sequence[float], cands: list[Cand]) -> int:
    """The decoder's choice: the highest model score, the smallest index on ties."""
    return max(range(len(cands)), key=lambda c: (dot(w, cands[c][0]), -c))


def corpus_value(w: Sequence[float], nbest: list[list[Cand]], metric: Metric) -> float:
    total = None
    for cands in nbest:
        s = cands[choose(w, cands)][1]
        total = s if total is None else add(total, s)
    return metric(total)


def mert(
    nbest: list[list[Cand]],
    w0: Sequence[float],
    metric: Metric,
    max_rounds: int = 20,
    extra_directions: Sequence[Sequence[float]] = (),
    eps: float = 1e-12,
) -> tuple[list[float], float]:
    """Coordinate ascent with exact line searches along each unit vector (and
    along extra_directions), until a round improves the metric by at most eps."""
    w = list(w0)
    dim = len(w)
    value = corpus_value(w, nbest, metric)
    directions = [[1.0 if k == j else 0.0 for k in range(dim)] for j in range(dim)]
    directions += [list(x) for x in extra_directions]
    for _ in range(max_rounds):
        improved = False
        for d in directions:
            gamma, v = line_search(w, d, nbest, metric)
            if v > value + eps:
                w = [x + gamma * y for x, y in zip(w, d)]
                value = v
                improved = True
        if not improved:
            break
    return w, value


# ---- BLEU as a metric on summed sufficient statistics (Papineni et al. 2002)


def ngrams(tokens: Sequence[str], n: int) -> Counter:
    return Counter(tuple(tokens[k : k + n]) for k in range(len(tokens) - n + 1))


def bleu_stats(cand: Sequence[str], refs: Sequence[Sequence[str]], max_n: int = 4) -> tuple:
    """(matches_1..max_n, counts_1..max_n, candidate length, effective reference
    length). Clipping uses the largest count in any one reference; the
    effective reference length is the closest one, the shorter on ties."""
    matches, counts = [], []
    for n in range(1, max_n + 1):
        c = ngrams(cand, n)
        clip: Counter = Counter()
        for r in refs:
            for g, k in ngrams(r, n).items():
                clip[g] = max(clip[g], k)
        matches.append(sum(min(k, clip[g]) for g, k in c.items()))
        counts.append(sum(c.values()))
    r = min((abs(len(x) - len(cand)), len(x)) for x in refs)[1]
    return tuple(matches) + tuple(counts) + (len(cand), r)


def bleu(stats: tuple, max_n: int = 4) -> float:
    """Corpus BLEU from summed statistics, without smoothing, on a 0 to 1 scale."""
    matches, counts = stats[:max_n], stats[max_n : 2 * max_n]
    c, r = stats[2 * max_n], stats[2 * max_n + 1]
    if c == 0 or any(x == 0 for x in matches):
        return 0.0
    log_p = sum(math.log(mt / ct) for mt, ct in zip(matches, counts)) / max_n
    bp = 1.0 if c > r else math.exp(1 - r / c)
    return bp * math.exp(log_p)
