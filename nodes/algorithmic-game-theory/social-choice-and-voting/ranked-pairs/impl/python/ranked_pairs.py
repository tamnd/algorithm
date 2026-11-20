# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranked-pairs/. The authors are listed in prov/XQFZVT.jsonl.

from typing import Optional, Sequence

Ranking = Sequence[int]


def margin_matrix(profile: Sequence[Ranking], m: int) -> list[list[int]]:
    """Return M with M[a][b] = (voters who rank a above b) - (voters who rank b above a)."""
    M = [[0] * m for _ in range(m)]
    for r in profile:
        for i, a in enumerate(r):
            for b in r[i + 1:]:
                M[a][b] += 1
                M[b][a] -= 1
    return M


def pair_order(M: list[list[int]], tiebreak: Sequence[int]) -> list[tuple[int, int, int]]:
    """Return the ordered pairs (g, x, y) with g = M[x][y] >= 0, in the order of locking.

    Larger margins come first. Pairs with equal margins are ordered by the tie-breaking ranking
    tiebreak: first by the place of x in it, then by the place of y.
    """
    m = len(M)
    place = {a: i for i, a in enumerate(tiebreak)}
    pairs = [(M[x][y], x, y) for x in range(m) for y in range(m) if x != y and M[x][y] >= 0]
    pairs.sort(key=lambda p: (-p[0], place[p[1]], place[p[2]]))
    return pairs


def ranked_pairs_ranking(profile: Sequence[Ranking], m: int,
                         tiebreak: Optional[Sequence[int]] = None) -> tuple[int, ...]:
    """Return the ranked pairs ranking of the candidates, best first.

    Ties between equal margins are broken by tiebreak, a ranking of the candidates; the default
    is 0, 1, ..., m - 1. Time O(n m^2 + m^3), extra space O(m^2).
    """
    if tiebreak is None:
        tiebreak = tuple(range(m))
    M = margin_matrix(profile, m)  # @line L1
    pairs = pair_order(M, tiebreak)  # @line L2
    reach = [[x == y for y in range(m)] for x in range(m)]  # @line L3
    for _, x, y in pairs:  # @line L4
        if reach[y][x]:  # @line L5
            continue
        row_y = reach[y]
        for z in range(m):  # @line L6
            rz = reach[z]
            if rz[x] and not rz[y]:
                for w in range(m):
                    if row_y[w]:
                        rz[w] = True
    below = [sum(reach[x]) for x in range(m)]
    return tuple(sorted(range(m), key=lambda x: -below[x]))  # @line L7


def ranked_pairs(profile: Sequence[Ranking], m: int,
                 tiebreak: Optional[Sequence[int]] = None) -> int:
    """Return the ranked pairs winner: the top of ranked_pairs_ranking. Precondition: m >= 1."""
    return ranked_pairs_ranking(profile, m, tiebreak)[0]  # @line L8


def locked_edges(profile: Sequence[Ranking], m: int,
                 tiebreak: Optional[Sequence[int]] = None) -> list[tuple[int, int]]:
    """Return the locked pairs (x, y), meaning x over y, in the order in which they were locked."""
    if tiebreak is None:
        tiebreak = tuple(range(m))
    M = margin_matrix(profile, m)
    reach = [[x == y for y in range(m)] for x in range(m)]
    out = []
    for _, x, y in pair_order(M, tiebreak):
        if reach[y][x]:
            continue
        out.append((x, y))
        for z in range(m):
            if reach[z][x] and not reach[z][y]:
                for w in range(m):
                    if reach[y][w]:
                        reach[z][w] = True
    return out
