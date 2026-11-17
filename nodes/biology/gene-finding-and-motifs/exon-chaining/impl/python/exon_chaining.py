# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exon-chaining/. The authors are listed in prov/BSR162.jsonl.
"""Exon chaining: a set of non-overlapping candidate exons of maximum total weight.

Coordinates follow the page: an exon is the closed interval [left, right] of
1-based genome positions, with left <= right. Two exons overlap when they share
a position, so an exon that starts at the position where another ends overlaps
it. A chain is a set of pairwise non-overlapping exons; the empty chain has
weight 0.
"""

from typing import List, NamedTuple, Sequence, Tuple, Union

Number = Union[int, float]

LEFT, RIGHT = 0, 1  # at equal positions, left points sort before right points


class Exon(NamedTuple):
    """A candidate exon: the positions left to right (1-based, inclusive) and a weight."""

    left: int
    right: int
    weight: Number


def exon_chaining(exons: Sequence[Exon]) -> Tuple[Number, List[int]]:
    """Return (best, chain): the largest total weight of a chain and one chain with it.

    chain lists indices into exons from left to right along the genome. Weights
    may be any numbers; an exon with weight <= 0 is never used, and if no
    exon has a positive weight the result is (0, []). Among chains with the
    best weight, the one whose last exon has the leftmost right end point is
    returned (the strict test of line L7).

    Cost: O(n log n) time for the sort and O(n) for the scan, O(n) space.
    """
    n = len(exons)
    for e in exons:
        if e.left > e.right:
            raise ValueError("an exon needs left <= right")
    points = [(e.left, LEFT, j) for j, e in enumerate(exons)]  # @line L1
    points += [(e.right, RIGHT, j) for j, e in enumerate(exons)]
    points.sort()  # @line L2
    best: Number = 0  # @line L3
    last = -1
    s: List[Number] = [0] * n
    pred = [-1] * n
    for _, side, j in points:  # @line L4
        if side == LEFT:  # @line L5
            s[j], pred[j] = best, last  # @line L6
        elif s[j] + exons[j].weight > best:  # @line L7
            best, last = s[j] + exons[j].weight, j  # @line L8
    chain: List[int] = []  # @line L9
    j = last
    while j != -1:  # @line L10
        chain.append(j)
        j = pred[j]
    chain.reverse()
    return best, chain  # @line L11


def is_chain(exons: Sequence[Exon], chain: Sequence[int]) -> bool:
    """True if the listed exons are distinct, in genome order and pairwise non-overlapping."""
    for a, b in zip(chain, chain[1:]):
        if exons[a].right >= exons[b].left:
            return False
    return len(set(chain)) == len(chain)


def chain_weight(exons: Sequence[Exon], chain: Sequence[int]) -> Number:
    """The total weight of the listed exons."""
    return sum((exons[j].weight for j in chain), 0)
