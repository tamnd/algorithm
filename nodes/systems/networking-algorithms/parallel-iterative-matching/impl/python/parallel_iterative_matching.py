# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-iterative-matching/. The authors are listed in prov/V6ZQKP.jsonl.

"""Parallel iterative matching (PIM) of Anderson, Owicki, Saxe and Thacker (1993).

The input is the request matrix of one time slot of an N x N input-queued
switch: req[i][j] is True when input i has a cell for output j (its virtual
output queue for j is not empty). Each iteration has three phases that all
unmatched ports run in parallel:

1. Request: each unmatched input requests every unmatched output it has a cell for.
2. Grant: each unmatched output that got requests grants one, uniformly at random.
3. Accept: each input that got grants accepts one, uniformly at random.

The accepted pairs join the matching and stay matched in later iterations.
"""

import random


def unresolved(req: list[list[bool]], in_match: list[int], out_match: list[int]) -> int:
    """The number of requests (i, j) with both input i and output j unmatched."""
    n = len(req)
    return sum(
        1
        for i in range(n)
        if in_match[i] < 0
        for j in range(n)
        if out_match[j] < 0 and req[i][j]
    )


def pim(
    req: list[list[bool]], rng: random.Random, max_iterations: int | None = None
) -> tuple[list[int], list[int]]:
    """Run PIM until the matching is maximal, or for max_iterations iterations.

    Returns (match, history): match[i] is the output of input i or -1, and
    history[k] is the number of unresolved requests before iteration k + 1,
    with a last entry for the state at the end.
    """
    n = len(req)
    in_match = [-1] * n  # @line L1
    out_match = [-1] * n
    history = [unresolved(req, in_match, out_match)]
    it = 0
    while history[-1] > 0 and (max_iterations is None or it < max_iterations):  # @line L2
        it += 1
        # Request phase: requests[j] = unmatched inputs that request output j.
        requests: list[list[int]] = [[] for _ in range(n)]
        for i in range(n):  # @line L3
            if in_match[i] < 0:
                for j in range(n):
                    if out_match[j] < 0 and req[i][j]:
                        requests[j].append(i)
        # Grant phase: each output grants one requester at random.
        grants: list[list[int]] = [[] for _ in range(n)]
        for j in range(n):  # @line L4
            if requests[j]:
                i = requests[j][rng.randrange(len(requests[j]))]  # @line L5
                grants[i].append(j)
        # Accept phase: each input accepts one grant at random.
        for i in range(n):  # @line L6
            if grants[i]:
                j = grants[i][rng.randrange(len(grants[i]))]  # @line L7
                in_match[i] = j  # @line L8
                out_match[j] = i
        history.append(unresolved(req, in_match, out_match))
    return in_match, history  # @line L9


def is_matching(req: list[list[bool]], match: list[int]) -> bool:
    """True when each matched pair is a request and no output is used twice."""
    used = [j for j in match if j >= 0]
    return len(used) == len(set(used)) and all(req[i][j] for i, j in enumerate(match) if j >= 0)


def is_maximal(req: list[list[bool]], match: list[int]) -> bool:
    """True when no request joins an unmatched input to an unmatched output."""
    n = len(req)
    taken = set(j for j in match if j >= 0)
    return not any(match[i] < 0 and req[i][j] and j not in taken for i in range(n) for j in range(n))
