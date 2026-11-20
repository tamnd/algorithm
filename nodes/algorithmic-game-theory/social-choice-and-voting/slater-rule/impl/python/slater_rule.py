# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slater-rule/. The authors are listed in prov/DWARFM.jsonl.

from typing import Sequence

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


def slater_cost(profile: Sequence[Ranking], m: int, ranking: Ranking) -> int:
    """Return the number of pairs that the ranking puts against a strict majority."""
    M = margin_matrix(profile, m)
    return sum(1 for i, a in enumerate(ranking) for b in ranking[i + 1:] if M[b][a] > 0)


def _table(profile: Sequence[Ranking], m: int) -> tuple[list[int], list[int]]:
    """Return (lose, cost): lose[v] is the bit set of the u with a positive margin over v, and
    cost[S] is the least number of majority disagreements of a ranking of the set S."""
    M = margin_matrix(profile, m)
    lose = [sum(1 << u for u in range(m) if M[u][v] > 0) for v in range(m)]  # @line L1
    cost = [0] * (1 << m)  # @line L2
    for S in range(1, 1 << m):  # @line L3
        best = None
        T = S
        while T:
            v = (T & -T).bit_length() - 1
            T &= T - 1
            rest = S & ~(1 << v)
            c = (lose[v] & rest).bit_count() + cost[rest]  # @line L4
            if best is None or c < best:
                best = c
        cost[S] = best
    return lose, cost


def slater_ranking(profile: Sequence[Ranking], m: int) -> tuple[int, ...]:
    """Return the lexicographically smallest ranking with the fewest majority disagreements."""
    lose, cost = _table(profile, m)
    S = (1 << m) - 1  # @line L5
    out = []
    while S:  # @line L6
        for v in range(m):
            if S >> v & 1:
                rest = S & ~(1 << v)
                if (lose[v] & rest).bit_count() + cost[rest] == cost[S]:  # @line L7
                    break
        out.append(v)  # @line L8
        S = rest
    return tuple(out)  # @line L9


def slater_winners(profile: Sequence[Ranking], m: int) -> frozenset[int]:
    """Return the candidates that are on top of some ranking with the fewest disagreements."""
    lose, cost = _table(profile, m)
    full = (1 << m) - 1
    return frozenset(v for v in range(m)
                     if (lose[v] & (full & ~(1 << v))).bit_count() + cost[full & ~(1 << v)]
                     == cost[full])


def slater(profile: Sequence[Ranking], m: int) -> int:
    """Return the Slater winner; a tie goes to the candidate with the smallest index."""
    return slater_ranking(profile, m)[0]
