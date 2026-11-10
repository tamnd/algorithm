# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/srpt/. The authors are listed in prov/1YRN1P.jsonl.

import heapq
from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]


def srpt(jobs: list[tuple[Number, Number]]) -> tuple[list[Number], list[tuple[Number, Number, int]]]:
    """Run SRPT on one machine of speed 1.

    jobs[j] = (r_j, p_j) with r_j >= 0 and p_j > 0. Return the completion
    times C[j] and the schedule as a list of pieces (start, end, job).
    Ties in the remaining work go to the job with the smaller index.
    """
    n = len(jobs)
    order = sorted(range(n), key=lambda j: (jobs[j][0], j))
    heap: list[tuple[Number, int]] = []  # @line L1
    t: Number = 0
    i = 0
    done: list[Number] = [0] * n
    pieces: list[tuple[Number, Number, int]] = []
    while i < n or heap:  # @line L2
        if not heap and t < jobs[order[i]][0]:  # @line L3
            t = jobs[order[i]][0]
        while i < n and jobs[order[i]][0] <= t:  # @line L4
            j = order[i]
            heapq.heappush(heap, (jobs[j][1], j))
            i += 1
        q, j = heapq.heappop(heap)  # @line L5
        nxt = jobs[order[i]][0] if i < n else None  # @line L6
        if nxt is None or t + q <= nxt:  # @line L7
            pieces.append((t, t + q, j))
            t = t + q
            done[j] = t
        else:  # @line L8
            pieces.append((t, nxt, j))
            heapq.heappush(heap, (q - (nxt - t), j))
            t = nxt
    return done, merge_pieces(pieces)  # @line L9


def merge_pieces(pieces: list[tuple[Number, Number, int]]) -> list[tuple[Number, Number, int]]:
    """Join adjacent pieces of the same job, and drop empty pieces."""
    out: list[tuple[Number, Number, int]] = []
    for a, b, j in pieces:
        if b <= a:
            continue
        if out and out[-1][2] == j and out[-1][1] == a:
            out[-1] = (out[-1][0], b, j)
        else:
            out.append((a, b, j))
    return out


def total_flow_time(jobs: list[tuple[Number, Number]], completion: list[Number]) -> Number:
    """Return the sum of C_j - r_j."""
    return sum(c - r for (r, _), c in zip(jobs, completion))
