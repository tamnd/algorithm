# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rank-join/. The authors are listed in prov/TEN8RX.jsonl.

"""Hash rank join (HRJN) of two inputs sorted by score, with the HRJN* pull rule.

Each input is a list of tuples sorted by the score column, highest first. The
join condition is equality of the key columns, and a NULL key (None) never
matches. The score of a join result is f(score of the left tuple, score of the
right tuple), where f must be monotone: f(x, y) <= f(x2, y2) when x <= x2 and
y <= y2. The default f is the sum.

rank_join returns the join results in non-increasing order of score and stops
after k of them (k=None gives the whole join). The threshold after each read
is the largest score that a combination not yet formed can have:

    T = max(f(top_L, bottom_R), f(bottom_L, top_R)),

where top is the first score of an input and bottom the last score read. A
term is left out when its input is exhausted, and T is minus infinity when
both are. A result in the queue is output once its score is at least T.
"""

import heapq
import itertools
import operator
from collections.abc import Callable, Sequence

NEG_INF = float("-inf")


def _check_sorted(rows: Sequence[tuple], col: int, name: str) -> None:
    for a, b in zip(rows, rows[1:]):
        if a[col] < b[col]:
            raise ValueError(f"input {name} is not sorted by score, highest first")


def rank_join(left: Sequence[tuple], right: Sequence[tuple], k: int | None = None,
              f: Callable = operator.add, strategy: str = "alternate",
              lkey: int = 0, lscore: int = 1, rkey: int = 0, rscore: int = 1):
    """Top-k equi-join of left and right by f(score_l, score_r).

    strategy is "alternate" (read the inputs in turn) or "adaptive" (HRJN*:
    read the input whose term of the threshold is larger). Returns (out, stats)
    where out is a list of (score, l, r) and stats has the depths (tuples read
    from each input), the threshold after each read and the largest queue size.
    """
    if strategy not in ("alternate", "adaptive"):
        raise ValueError("strategy must be 'alternate' or 'adaptive'")
    _check_sorted(left, lscore, "left")
    _check_sorted(right, rscore, "right")
    inputs = (left, right)
    keys = (lkey, rkey)
    scores = (lscore, rscore)
    tables = ({}, {})  # @line L1
    queue: list = []
    tie = itertools.count()
    out: list = []
    stats = {"depth": [0, 0], "thresholds": [], "max_queue": 0}
    limit = float("inf") if k is None else k
    if not left or not right or limit <= 0:  # @line L2
        return out, stats
    depth = stats["depth"]
    top = (left[0][lscore], right[0][rscore])
    bottom = [top[0], top[1]]
    turn = 0

    def exhausted(i: int) -> bool:
        return depth[i] == len(inputs[i])

    while len(out) < limit and not (exhausted(0) and exhausted(1)):  # @line L3
        if depth[0] == 0 or depth[1] == 0:
            i = 0 if depth[0] == 0 else 1
        elif strategy == "alternate":
            i = turn
        else:
            i = 1 if f(top[0], bottom[1]) > f(bottom[0], top[1]) else 0
        if exhausted(i):
            i = 1 - i  # @line L4
        t = inputs[i][depth[i]]
        depth[i] += 1
        bottom[i] = t[scores[i]]  # @line L5
        turn = 1 - i
        key = t[keys[i]]
        if key is not None:
            tables[i].setdefault(key, []).append(t)
            for u in tables[1 - i].get(key, ()):  # @line L6
                l, r = (t, u) if i == 0 else (u, t)
                s = f(l[lscore], r[rscore])
                heapq.heappush(queue, (-s, next(tie), l, r))
        stats["max_queue"] = max(stats["max_queue"], len(queue))
        terms = []
        if not exhausted(1) and depth[1] > 0:
            terms.append(f(top[0], bottom[1]))
        if not exhausted(0) and depth[0] > 0:
            terms.append(f(bottom[0], top[1]))
        if depth[0] == 0 or depth[1] == 0:
            terms.append(f(top[0], top[1]))
        threshold = max(terms) if terms else NEG_INF  # @line L7
        stats["thresholds"].append(threshold)
        while queue and -queue[0][0] >= threshold and len(out) < limit:  # @line L8
            s, _, l, r = heapq.heappop(queue)
            out.append((-s, l, r))
    while queue and len(out) < limit:  # @line L9
        s, _, l, r = heapq.heappop(queue)
        out.append((-s, l, r))
    return out, stats  # @line L10
