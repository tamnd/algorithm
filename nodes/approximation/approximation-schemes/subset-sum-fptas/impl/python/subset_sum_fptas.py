# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subset-sum-fptas/. The authors are listed in prov/MWFG11.jsonl.

from fractions import Fraction
from typing import Iterator, Optional, Union

Number = Union[int, Fraction, float]
# A chosen subset is a linked list (index of the last item, the rest), so
# that the lists share their tails and each step costs O(1) per entry.
Chain = Optional[tuple[int, "Chain"]]


def trim(values: list[tuple[int, Chain]], delta: Fraction) -> list[tuple[int, Chain]]:
    """Keep y_1 and each y_k > last * (1 + delta), where last is the last kept value.

    The input is sorted by value with no repeated values. Each removed value
    y has a kept value z with y / (1 + delta) <= z <= y. Time O(len(values)).
    """
    kept = [values[0]]  # @line L8
    last = values[0][0]
    for y in values[1:]:  # @line L9
        if y[0] > last * (1 + delta):  # @line L10
            kept.append(y)
            last = y[0]
    return kept  # @line L11


def trimmed_lists(x: list[int], t: int, eps: Number) -> Iterator[list[tuple[int, Chain]]]:
    """Yield the list L_i after the step for item i, for i = 1 .. n.

    Each entry is (sum, chain of the items that give the sum). Precondition:
    positive integers x, an integer t >= 0, 0 < eps <= 1.
    """
    e = Fraction(eps)
    if not 0 < e <= 1:
        raise ValueError("eps must be in (0, 1]")
    n = len(x)
    if n == 0:
        return
    delta = e / (2 * n)  # @line L1
    cur: list[tuple[int, Chain]] = [(0, None)]  # @line L2
    for i in range(n):  # @line L3
        shifted = [(s + x[i], (i, c)) for s, c in cur]
        merged: list[tuple[int, Chain]] = []  # @line L4
        a = b = 0
        while a < len(cur) or b < len(shifted):
            if b == len(shifted) or (a < len(cur) and cur[a][0] <= shifted[b][0]):
                y = cur[a]
                a += 1
            else:
                y = shifted[b]
                b += 1
            if not merged or merged[-1][0] != y[0]:
                merged.append(y)
        cur = trim(merged, delta)  # @line L5
        cur = [y for y in cur if y[0] <= t]  # @line L6
        yield cur


def approx_subset_sum(x: list[int], t: int, eps: Number) -> tuple[int, list[int]]:
    """Return (z, indices): a subset of x with sum z <= t and z >= OPT / (1 + eps).

    OPT is the largest subset sum that is at most t, and z >= (1 - eps) * OPT.
    The time is O(n^2 log(t) / eps) and each list has at most
    log_(1 + eps / 2n) t + 2 entries (Cormen et al., Section 35.5).
    """
    best: tuple[int, Chain] = (0, None)
    for cur in trimmed_lists(x, t, eps):
        best = cur[-1]
    z, chain = best  # @line L7
    chosen = []
    while chain is not None:
        chosen.append(chain[0])
        chain = chain[1]
    return z, sorted(chosen)
