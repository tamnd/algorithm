# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grow-diag-final-symmetrization/. The authors are listed in prov/00FY52.jsonl.

"""Grow-diag-final symmetrization of two word alignments, as in the Moses documentation.

A link is a pair (j, i): source position j in 1 .. m and target position i in
1 .. l (1-based, null links are not links). a1 and a2 are the link sets of the
two directions. The procedure follows the GROW-DIAG-FINAL pseudocode of the
Moses training documentation: the outer loop runs over the target (English)
positions i, the inner loop over the source (foreign) positions j, a new link
is visible at once, the neighbours are tried in the listed order, and FINAL is
applied to a1 and then to a2 (Moses: FINAL(e2f), then FINAL(f2e)). The order
matters: another loop order can give another result.

Options: diag=False uses only the four direct neighbours (grow-final);
final=False stops after the growing step (grow-diag); final_and=True adds a
link in the final step only if both of its words are unaligned
(grow-diag-final-and).
"""

from typing import FrozenSet, Iterable, Set, Tuple

Link = Tuple[int, int]  # (j, i)

# (delta i, delta j), the order of the Moses pseudocode, which lists (e, f) offsets.
NEIGHBOURS_DIAG = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
NEIGHBOURS_GROW = NEIGHBOURS_DIAG[:4]


class _State:
    """The current link set with the alignment status of each word, O(1) per query."""

    def __init__(self, links: Iterable[Link], m: int, l: int) -> None:
        self.links: Set[Link] = set()
        self.src = [0] * (m + 2)
        self.tgt = [0] * (l + 2)
        for p in links:
            self.add(p)

    def add(self, p: Link) -> None:
        if p not in self.links:
            self.links.add(p)
            self.src[p[0]] += 1
            self.tgt[p[1]] += 1

    def either_unaligned(self, p: Link) -> bool:
        return self.src[p[0]] == 0 or self.tgt[p[1]] == 0

    def both_unaligned(self, p: Link) -> bool:
        return self.src[p[0]] == 0 and self.tgt[p[1]] == 0


def _check(links: Iterable[Link], m: int, l: int) -> FrozenSet[Link]:
    s = frozenset(links)
    for j, i in s:
        if not (1 <= j <= m and 1 <= i <= l):
            raise ValueError(f"link {(j, i)} is outside 1..{m} x 1..{l}")
    return s


def grow_diag_final(a1: Iterable[Link], a2: Iterable[Link], m: int, l: int,
                    diag: bool = True, final: bool = True, final_and: bool = False) -> Set[Link]:
    """Return the symmetrized link set. Cost O((m l)^2) in the worst case, see the page."""
    a1, a2 = _check(a1, m, l), _check(a2, m, l)
    union = a1 | a2
    state = _State(a1 & a2, m, l)  # @line L1
    neighbours = NEIGHBOURS_DIAG if diag else NEIGHBOURS_GROW
    while True:  # @line L2
        added = False  # @line L3
        for i in range(1, l + 1):  # @line L4
            for j in range(1, m + 1):
                if (j, i) in state.links:  # @line L5
                    for di, dj in neighbours:  # @line L6
                        p = (j + dj, i + di)  # @line L7
                        if p in union and state.either_unaligned(p):  # @line L8
                            state.add(p)
                            added = True
        if not added:  # @line L9
            break
    if final:
        for b in (a1, a2):  # @line L10
            for i in range(1, l + 1):  # @line L11
                for j in range(1, m + 1):
                    p = (j, i)
                    ok = state.both_unaligned(p) if final_and else state.either_unaligned(p)
                    if p in b and ok:  # @line L12
                        state.add(p)
    return set(state.links)  # @line L13


def grow_diag_final_and(a1: Iterable[Link], a2: Iterable[Link], m: int, l: int) -> Set[Link]:
    """The variant whose final step needs both words unaligned."""
    return grow_diag_final(a1, a2, m, l, final_and=True)


def links_from_alignment(a: Iterable[int]) -> Set[Link]:
    """Links of a one-directional alignment a_1 .. a_m of p(f | e); a_j = 0 is the null word."""
    return {(j, i) for j, i in enumerate(a, start=1) if i > 0}


def links_from_reverse(b: Iterable[int]) -> Set[Link]:
    """Links of an alignment b_1 .. b_l of the other direction p(e | f), turned into (j, i) pairs."""
    return {(j, i) for i, j in enumerate(b, start=1) if j > 0}
