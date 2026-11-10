# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-histogram/. The authors are listed in prov/DG02CV.jsonl.

"""Histogram by private per-block counts and a fork-join tree of merges.

The input is cut into p blocks of ceil(n / p) consecutive items. Each block is counted
sequentially into its own array of k zeros; then the arrays are added up in a balanced
binary tree, each add being a parallel loop over the k bins. The code runs sequentially
and returns the work and the span in the cost model of the page: a step costs 1, and a
group of r parallel tasks adds r - 1 to the work and ceil(lg r) to the span.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Cost:
    work: int
    span: int


def ceil_lg(r: int) -> int:
    return (r - 1).bit_length() if r > 1 else 0


def _hist(x: list[int], lo: int, hi: int, k: int, size: int) -> tuple[list[int], Cost]:
    """The histogram of the blocks lo .. hi - 1 of x (block b is x[b * size : (b + 1) * size])."""
    if hi - lo == 1:  # @line L1
        h = [0] * k  # @line L2: k steps
        items = x[lo * size : (lo + 1) * size]
        for v in items:  # @line L3: one step per item, in sequence
            h[v] += 1
        steps = k + len(items)
        return h, Cost(steps, steps)  # @line L4
    mid = (lo + hi + 1) // 2  # @line L5: the left half gets the extra block
    h, left = _hist(x, lo, mid, k, size)  # @line L6: spawn
    g, right = _hist(x, mid, hi, k, size)  # @line L7
    # @line L8: sync
    for j in range(k):  # @line L9: parallel for over the k bins
        h[j] += g[j]
    merge = Cost(2 * k - 1, ceil_lg(k) + 1)
    return h, Cost(1 + left.work + right.work + merge.work, 1 + max(left.span, right.span) + merge.span)  # @line L10


def histogram(x: list[int], k: int, p: int) -> tuple[list[int], Cost]:
    """Count the keys of x, each in range(k), with p >= 1 blocks. Returns the counts and the cost."""
    if k < 1 or p < 1:
        raise ValueError("k and p must be at least 1")
    if any(not 0 <= v < k for v in x):
        raise ValueError("a key is out of range")
    size = max(1, -(-len(x) // p))
    return _hist(x, 0, p, k, size)


def work_formula(n: int, k: int, p: int) -> int:
    return n + 3 * p * k - 2 * k


def span_formula(n: int, k: int, p: int) -> int:
    return ceil_lg(p) * (ceil_lg(k) + 2) + k + -(-n // p)
